---
title: Memcached
category: tech/system-design
tags: [memcached, cache, in-memory, distributed-cache, key-value, slab-allocation, consistent-hashing, cache-cluster, mcrouter, extstore]
status: draft
priority: high
last_updated: 2026-04-21
created_from_jd: "[[positions/Manager II, Engineering - Infra - Pinterest]]"
---

# Memcached

## Knowledge Map
- 前置知识：[[Cache and Consistency]], [[Distributed Systems]], [[Kubernetes]]
- 延伸话题：[[Redis]], [[Sharding and Scalability]], ZooKeeper, mcrouter (L7 proxy), extstore (NVMe tier), consistent hashing
- 管理关联：cache capacity planning, fleet cost optimization, cross-zone HA strategy, hot-key incident response, upstream contribution policy

## Core Concepts

### Architecture fundamentals
- **Pure in-memory key-value store** — no data structures beyond string value, no persistence, no replication. Simplicity is the design philosophy: "do one thing well, let the system around it handle the rest."
- **Multithreaded event loop** — unlike single-threaded Redis, Memcached uses libevent with per-thread event loops, scaling to tens of thousands of concurrent connections on a single node. A single `r5.2xlarge` sustains 100K+ RPS without latency degradation (Pinterest).
- **No clustering awareness** — a Memcached node knows nothing about other nodes. Clustering, sharding, failover all live in the **client library or proxy** (typically mcrouter). This is why "running Memcached at scale" means "running mcrouter correctly."

### Memory management — the slab allocator
- **Memory divided into 1 MB pages**, assigned to **slab classes**. Each class has a fixed chunk size (e.g. class 1 = 80B, class 2 = 104B, class 3 = 136B, progressing up to 1 MB).
- **Items stored in nearest-fit class** — a 50B item in an 80B chunk wastes 30B. The tradeoff: fast O(1) allocation and no fragmentation, at the cost of up to ~30% wasted bytes per item.
- **Slab calcification is the #1 operational pain**: once a page is assigned to a class, it cannot be reassigned. If your workload shifts (older items were big, newer items are small), pages assigned to the old size become stranded — even though the new size is full, the old class won't release pages. Mitigations: slab rebalancer (moves pages between classes), or restart.
- **Item overhead**: ~32 bytes (no CAS) or ~40 bytes (with CAS) per item on 32-bit; larger on 64-bit. For tiny values this overhead dominates.

### Eviction — per-class LRU
- **Each slab class has its own LRU**. Eviction only considers items in the same class — evicting a large item won't free space for a small item.
- **Expired items reclaimed before evicting live ones**: on cache miss, tail of LRU is scanned for expired entries first. Active crawler (v1.5+) periodically walks the cache to proactively free expired items.
- **Consequence**: LRU behavior is per-size-class, not global. Hot small items don't protect cold large items and vice versa.

### Scaling beyond RAM — extstore
- **Extstore = secondary NVMe tier** — keeps hot items in DRAM, demotes cold items to flash. Raises per-instance capacity from ~55 GB to ~1.7 TB on r5.2xlarge class hardware (Pinterest).
- Latency stays acceptable because only cold items hit flash. Transforms Memcached from "fast but tiny" to "fast and large" for capacity-bound workloads.

### Sharding — consistent hashing (client-side)
- **Clients** (or mcrouter) hash each key and route to a specific node. Memcached itself has no knowledge of sharding.
- **Consistent hashing** vs naive modulo: when a node is added/removed, only ~1/N of keys remap, not all of them. Essential for scaling the fleet without mass cache miss storms.
- Pinterest uses this plus **AZ-affinity routing** and **L1/L2 tier routing** layered through mcrouter.

### Failure handling — gutter pool pattern (Facebook)
- **Do NOT redistribute keys from a failed node to other nodes** — that causes cascade overload (the other nodes get 2x load and their hot keys may evict).
- **Instead: dedicate ~1% of the fleet as a "gutter" pool**. When a client can't reach its shard, it tries gutter. If gutter misses, client queries DB and writes to gutter. Failed node's load is absorbed by gutter, not peers.
- Pinterest's equivalent: mcrouter auto-redirects to a shared fallback cluster with health checks.

### Thundering herd & stale writes — leases (Facebook)
- **Lease token** issued per key on cache miss. Only the lease holder fetches from DB and writes back; concurrent requesters retry and read the (now-populated) cache.
- **Leases also prevent stale sets**: a write with an old lease token is rejected if the key was invalidated in between. Solves the classic "reader writes stale value after invalidation" race.
- Leases are rate-limited per key — if 1000 clients all miss on the same key, only a few leases are issued per second, limiting DB fan-in.

### Multi-region consistency
- **Master-slave region model**: one region writes to MySQL master, others read slaves. Cache invalidations piggyback on MySQL commit log, so invalidation always arrives *after* the DB replica has the new value (avoids stale-repopulation races).
- **Remote marker**: if a web server just wrote to master, it sets a marker in local cache telling other readers in the same region "go read from the master region for consistency" — used for the small window where replica hasn't caught up.
- Accepts **eventual consistency** within replication lag; uses markers to paper over the worst cases.

### Pool separation
- **Different workloads have different churn rates**. Mixing high-churn keys (e.g. transient session data) with low-churn keys (e.g. static profile info) in one pool → high-churn evicts low-churn via LRU.
- **Solution: separate pools**. Each pool sized for its working set. Reduces unwanted evictions, simplifies capacity planning.

### The unsolved problem — hot keys
- When one key gets disproportionate traffic (e.g. celebrity profile, trending post), a single shard gets hammered. No amount of consistent hashing fixes this because all requests hash to the same node.
- **Pinterest explicitly acknowledges this remains unsolved.** Partial mitigations: local in-process caching for hottest keys, key splitting (foo → foo:shard1, foo:shard2, client picks randomly), multi-tier caching with L1 in-process cache.

## Key Questions

**Q: When would you choose Memcached over Redis? Give me a concrete decision framework.**
Answer framework: Memcached wins when (1) workload is pure key-value with no need for lists/sets/sorted sets, (2) you want multi-core throughput from a single node, (3) you need extstore for flash-tier capacity expansion, (4) you want the simplest possible cache layer and plan to build HA/replication at the proxy layer (mcrouter) rather than in the data store. Redis wins when you need persistence, replication, pub/sub, transactions, Lua, or rich data types. Pinterest and Facebook both picked Memcached despite having Redis available — the reason is mostly the simplicity-plus-mcrouter pattern scaling better than Redis Cluster at their fleet size.

**Q: Explain the slab allocator. What is slab calcification and how would you diagnose it?**
Answer framework: Slab allocator carves memory into 1 MB pages, each assigned to a size class with fixed chunk size. Items go in the nearest-fit class. Once a page belongs to a class, it stays there. Calcification = workload shifts so that class A is full but has stranded pages that class B desperately needs. Diagnose via `stats slabs` to see per-class utilization and eviction rates — if class A has high eviction while class B has free chunks, you're calcified. Fix: enable slab rebalancer, or in extreme cases restart. Prevention: provision enough headroom and monitor class distribution in production.

**Q: How would you design failure handling for a 1000-node Memcached cluster? What's wrong with "just rehash the keys from the failed node"?**
Answer framework: Rehashing failed-node keys to peers causes cascade failure — each healthy node now takes extra load, their hot keys start evicting, and a secondary node tips over, triggering another rehash, and so on until the whole fleet dies. Correct pattern is Facebook's gutter pool: dedicate ~1% of the fleet as standby, when a client can't reach its shard it tries gutter, gutter absorbs the failed node's load without touching peers. Pinterest does the equivalent with mcrouter auto-redirecting to a shared fallback cluster. Key insight: in a cache, better to temporarily miss and hit the DB than to cascade-kill the cache.

**Q: A single cache key is getting 10M QPS and overloading one shard. Walk me through mitigations.**
Answer framework: First acknowledge this is the "hot key" problem and even Pinterest admits it's unsolved in general. Partial mitigations in order of preference: (1) L1 in-process cache — every app instance caches the hot key locally for a few seconds, dropping shard load by 1000x; (2) Key splitting — replace the hot key with N replica keys (foo:0 through foo:9), client picks one at random, reduces hot shard load by N; (3) Dedicated replicated pool for the hot key with cross-zone replicas; (4) Upstream fix: why is this key so hot? Often it's a legitimate celebrity / viral content problem that needs product-layer caching (CDN, edge cache). Escalation order matters — try (1) in 10 minutes, (2) in an hour, (4) as the real fix.

**Q: What is mcrouter and why is it essentially required for production Memcached?**
Answer framework: Memcached itself has no clustering, no failover, no replication — all of that lives in the client. Mcrouter is Facebook's L7 Memcached protocol proxy that provides routing (consistent hashing, AZ affinity), failover (auto-redirect on failure), replication (cross-zone copies), and observability (per-key-prefix metrics, percentile latencies) at the proxy layer rather than in each app. Run it as a sidecar on every app instance: apps talk to localhost mcrouter, mcrouter talks to the fleet. Decouples control plane (topology, pool config) from data plane (routing rules). Without mcrouter or an equivalent, each application has to reimplement cluster logic — not scalable across many services.

**Q: How do you keep a Memcached deployment consistent across regions? What are the failure modes?**
Answer framework: Facebook's model: one master region writes MySQL, other regions read slaves. Cache invalidations ride on the MySQL commit log — invalidation arrives only after the replica has the new value, preventing stale-repopulation. Use "remote markers" when a writer in region A wants readers to bypass local cache temporarily and read from master until replication catches up. Accept eventual consistency within replication lag. Failure modes: (1) invalidation storm on big writes, (2) replication lag spike causing stale reads, (3) marker cache poisoned causing permanent master hits. Manager-level answer: don't chase strong consistency across regions — design the app to tolerate a few seconds of staleness; reserve cross-region reads for truly consistency-critical paths.

**Q: How would you plan capacity for a Memcached fleet? What signals drive scaling decisions?**
Answer framework: Key signals — (1) hit rate (target 95%+ for most caches; below 90% means cache is undersized), (2) eviction rate per slab class (high evictions = class-local calcification or overall undersize), (3) p99 latency (target sub-ms on LAN; spike = overloaded node), (4) memory utilization (target ~90% steady state, leaves headroom for growth), (5) connection count (per-node limit, usually ~10K+ per r5.2xlarge). Separate high-churn and low-churn pools. For capacity-bound workloads, add extstore to expand per-node capacity 30x on NVMe. For throughput-bound workloads, shard more (add nodes) — multithreading means scaling up is viable up to ~100K+ RPS per node before scaling out.

**Q: A team proposes using Memcached as the primary store for a new feature "because it's fast." What's your response as a manager?**
Answer framework: Push back — Memcached is a cache, not a database. No persistence means any restart or crash loses all data. No replication means no HA. No durability means no recovery. Correct pattern: DB is source of truth, Memcached fronts it. If they want "fast key-value DB," point them at DynamoDB (managed, persistent, replicated) or Redis with AOF (if they need data structures too). If they persist on using Memcached, force them to document how they'll handle total data loss — usually that conversation ends the idea. Manager angle: part of the job is preventing junior engineers from reinventing outages that were solved 15 years ago.

## Key Terms

**Architecture**
- `slab allocator` · `slab class` · `chunk size` · `1MB page` · `per-class LRU` · `libevent` · `multithreaded event loop` · `CAS` · `extstore`

**Operational patterns**
- `consistent hashing` · `client-side sharding` · `AZ-affinity routing` · `L1/L2 tier routing` · `slab rebalancer` · `stats slabs`

**Facebook-scale mechanisms**
- `lease token` · `stale set` · `thundering herd` · `gutter pool` · `pool separation` · `wildcard pool` · `remote marker` · `master/slave region` · `cold cluster warmup` · `sliding window` · `incast congestion` · `connection coalescing`

**Proxy / fleet management**
- `mcrouter` · `sidecar proxy` · `L7 memcached protocol` · `control plane vs data plane` · `shadow traffic` · `TTL manipulation`

**Failure modes**
- `slab calcification` · `cache stampede` · `hot key` · `cascade failure` · `stale read` · `key splitting`

**Decision points (vs Redis)**
- `pure key-value only` · `no persistence` · `no replication` · `no pub/sub` · `multi-core vs single-thread` · `simplicity + proxy` vs `rich features in-store`

## Raw Material
- [[raw_material/tech/system-design/Memcached Raw Materials]]
