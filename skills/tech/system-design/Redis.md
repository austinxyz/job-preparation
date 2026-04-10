---
title: Redis
category: tech/system-design
tags: [redis, cache, in-memory, rdb, aof, zset, skip-list, sentinel, redis-cluster, bloom-filter, hash-slot]
status: in-progress
priority: high
last_updated: 2026-04-10
created_from_jd:
---

# Redis

## Knowledge Map
- Prerequisites（前置知识）：[[Cache and Consistency]], [[Distributed Systems]]
- Related Topics（延伸话题）：[[NoSQL Databases]], [[Sharding and Scalability]], [[Message Queue]]
- Management（管理关联）：[[Platform Team Management]]

## Core Concepts

**Why Redis Is Fast — and Why It Can't Replace Everything（纯内存操作）**
- **Pure in-memory operations**: data in RAM, read/write with no disk IO; memory vs disk latency difference is ~1000x
- Cannot replace a database: ① memory is volatile (data lost on restart); ② limited capacity (memory is far more expensive than disk); ③ no complex queries/Join/ACID transactions
- Redis = high-speed cache layer, not a persistent database

**Persistence: RDB vs AOF（持久化策略）**
- **RDB** (snapshot): periodically snapshots in-memory data to disk; fast recovery, compact file; downside: data written since the last snapshot may be lost
- **AOF** (Append Only File): records every write operation appended to a log; minimal data loss; downside: large file, slow recovery
- **RDB + AOF hybrid**: RDB recovers most data quickly, AOF supplements the delta; recommended for production environments （生产推荐配置）

**Data Structure Selection（数据结构选型）**
- **String**: stores strings or numbers; `INCR` for atomic increment/decrement → video play counts, likes, distributed locks
- **Bitmap**: each bit represents a user/state; 1 billion users ≈ ~125MB → user online status (online=1, offline=0) （极致节省空间）
- **ZSet (Sorted Set)**: each member has a score, auto-sorted → real-time leaderboards (`ZREVRANGE` to get Top K)
- **List**: ordered double-ended queue; `LPUSH` insert at head + `LTRIM` keep the last N → user Feed cache (last 50 items)
- **HyperLogLog**: probabilistic algorithm to estimate set cardinality (UV); has error margin, cannot do membership queries → estimate unique viewer count

**Common Misconceptions（常见误区）**
- Feed cache: use List (ordered) not Set (unordered)
- Leaderboard: use ZSet (precise sorting) not HyperLogLog (only estimates cardinality)
- Large-scale Bitmap: mentally estimate memory — 1 billion users × 10 billion videos ≈ 1.25EB, infeasible → use Bloom Filter instead

**ZSet Internals: Skip List vs B+ Tree（跳表底层实现）**
- ZSet uses a **Skip List** (multi-level sorted linked list) — O(log n) for find/insert/delete
- Why not B+ tree: B+ trees are optimized for disk IO (nodes correspond to disk pages); Skip Lists are suited for pure in-memory operations (pointer connections, insert/delete only change pointers, no page splits, simpler implementation)

**Single-Threaded Model and Slow Operation Risk（单线程风险）**
- Why single-threaded is fast: all operations are in memory, extremely fast; single thread **avoids lock contention and thread context switching**
- Risk: **one slow operation blocks all requests**; `KEYS *` can freeze Redis for several seconds in production
- Safe alternative: **`SCAN` command** — iterative scanning in small batches per call via a cursor, non-blocking

**High Availability: Redis Sentinel（哨兵模式）**
- Multiple Sentinels continuously ping the primary node; if a **Quorum** (majority of Sentinels) determines the primary is unavailable, they trigger Leader Election
- A replica is promoted to primary; all clients are notified to update their connections
- Quorum voting prevents a single Sentinel's network blip from causing false positives （防止误判）
- Sentinel solves: HA (automatic primary failover); **does not solve**: data volume/capacity issues

**Horizontal Scaling: Redis Cluster and Hash Slot（横向扩展）**
- When a single machine's memory is insufficient, use **Redis Cluster**: data is distributed across multiple nodes
- **Hash Slot**: 16,384 slots total; maps keys to slots, then assigns slots to nodes
- vs Consistent Hashing: Hash Slot is simpler and more predictable; node additions/removals only migrate the corresponding slots; suited for Redis (infrequent large-scale scaling)

| | Redis Sentinel | Redis Cluster |
|---|---|---|
| Problem Solved | HA (primary failover) | Data volume + horizontal scaling |
| Mechanism | Primary-replica replication + auto failover | Data sharding (Hash Slot) |
| Complementary | ✅ Can be used together (Cluster with multiple nodes, each node has Sentinel-monitored primary-replica) |

**Bloom Filter（布隆过滤器）**
- Scenario: 1 billion users × 10 billion videos — determine "has the user watched this video?"; pure Bitmap ≈ 1.25EB, infeasible
- Principle: hash the element k times, set the corresponding k bits to 1; query by checking if all k bits are 1
- **False Positive**: hash collision mistakenly judges "exists" (acceptable — at worst recommends one already-watched video); **No False Negative**: if a bit is 0, the element definitely doesn't exist
- Does not support deletion (multiple elements share bits); does not support exact queries
- **Counting Bloom Filter**: each bit becomes a counter, supports deletion; cost is increased memory

**Performance Numbers (benchmark context)**
- Write throughput: **O(100k) writes/second**; read latency: often in the **microsecond range**
- These numbers change what's feasible: 100 serial Redis calls is tolerable where 100 SQL queries would be unacceptable. Still avoid unnecessary round trips (use pipelines or Lua scripts), but don't over-optimize.
- All of this is a consequence of pure in-memory + single-threaded model: no disk IO, no lock contention.

**Distributed Lock Patterns**
- Simplest lock: `SET key value NX EX ttl` — atomic set-if-not-exists with expiry. If SET succeeds, you hold the lock; if it returns nil, someone else does.
- INCR-based lock (Hello Interview pattern): `INCR key` → if result is 1, you hold the lock; if > 1, wait. Set TTL immediately after. Less safe — INCR and EXPIRE are two operations (not atomic unless wrapped in Lua).
- **Redlock algorithm**: acquire locks on N/2+1 independent Redis nodes with the same key and TTL; only proceed if majority acquired within a time window smaller than TTL. Guards against single-node failure. Add **fencing tokens** (monotonically increasing lock version) to prevent stale lock holders from taking effect after TTL expiry.
- Caution: distributed locks in Redis are *not* as safe as locks in Zookeeper/etcd (which have stronger consistency guarantees). For most use cases, single-node SET NX EX is sufficient; Redlock is for high-stakes scenarios where correctness > simplicity.

**Rate Limiting with Redis**
- **Fixed-window**: on each request, `INCR user:123:ratelimit` and check against limit N; `EXPIRE` the key with window duration W so it resets automatically. Simple, low latency. Weakness: burst at window boundary (up to 2N requests in one real-world second spanning two windows).
- **Sliding window (log-based)**: store timestamps in a Sorted Set per user; on each request: `ZREMRANGEBYSCORE` to remove old entries, `ZCARD` to count current entries, `ZADD` to add the new request timestamp. Run in a Lua script to keep it atomic. Accurate but higher memory per user.
- **Sliding window (approximate)**: blend two fixed windows weighted by time elapsed — lower memory, still accurate enough for most rate-limiting use cases.
- Interview tip: start with fixed-window (simple, fast), then describe the boundary burst problem, then offer sliding window as the fix with the memory/accuracy tradeoff.

**Proximity Search (Geospatial)**
- `GEOADD key longitude latitude member` — indexes a location
- `GEOSEARCH key FROMLONLAT lon lat BYRADIUS r unit` — finds members within radius; runs in O(N + log M)
- Internally uses **geohashes**: encodes lat/lon into a single string; nearby locations share a prefix. Candidate search fetches a bounding box of geohash cells, then a second pass filters to the exact radius.
- Good fit for: Uber driver location lookup, restaurant proximity search, anything needing "find N nearest." Not a replacement for PostGIS for complex polygon queries.

**Streams for Event Sourcing / Work Queues**
- Redis Streams = append-only log, similar to Kafka topics but simpler.
- `XADD stream * field value` — appends an entry; `*` auto-generates a timestamp-based ID.
- **Consumer groups**: multiple workers share a stream; each message is delivered to exactly one worker in the group. `XREADGROUP` to read, `XACK` to acknowledge, `XCLAIM` to re-assign a message whose worker died (detected via PEL — Pending Entries List).
- vs Kafka: Redis Streams are simpler to operate but have less retention and replication guarantees. Good for moderate-scale queues (job dispatch, async task pipelines) where you don't need Kafka's throughput or replay across consumer groups independently.
- vs Pub/Sub: Streams persist messages; Pub/Sub does not. If consumers can go offline, use Streams.

**Pub/Sub — Capabilities and Limits**
- `SPUBLISH channel message` / `SSUBSCRIBE channel` — sharded pub/sub (S prefix); one connection per node in cluster, not per channel.
- Delivery guarantee: **at-most-once**. If a subscriber is offline when a message is published, the message is lost entirely.
- When to use: real-time notifications, chat, ephemeral fan-out where missing a message is acceptable.
- When NOT to use: any scenario requiring delivery guarantees, offline consumers, or message replay → use Streams or Kafka instead.
- Common misconception: old Redis Pub/Sub required a connection per channel → modern sharded Pub/Sub uses one connection per node regardless of channel count.

**Hot Key Problem and Remediations**
- Cause: one key receives disproportionate traffic, overloading the single node that holds it (hash slot assignment is deterministic).
- Remediations (with tradeoffs):
  1. **Local in-process cache** on application servers: absorb repetitive reads before hitting Redis. Simplest; introduces cache-per-instance staleness.
  2. **Key replication with randomization**: store hot data at N keys (`product:123:0` … `product:123:9`); reads pick a random replica. Writes must update all N keys. Good for read-heavy hot keys.
  3. **Read replicas per hot shard**: dynamically spin up read replicas for the overloaded node and load-balance reads. Operationally complex but doesn't require application changes.
- Interview signal: spotting hot key risk proactively (before the interviewer asks) and proposing a mitigation with tradeoffs = strong candidate signal.

## Key Questions

**Q: What scenarios are String/Bitmap/ZSet/List/HyperLogLog each suited for?**
Answer framework: Four-scenario quick reference (video play count → String INCR; user online status → Bitmap; real-time leaderboard → ZSet; Feed cache → List); state common misconceptions (Feed uses List not Set; leaderboard uses ZSet not HyperLogLog); for large-scale Bitmap, proactively estimate memory (demonstrates numerical sensitivity).
> 中文提示：四场景速查；主动说出常见误区；大规模 Bitmap 心算内存体现数字敏感度

**Q: What are the pros and cons of RDB and AOF? How should production be configured?**
Answer framework: RDB = snapshot, fast recovery but may lose data since last snapshot; AOF = every write appended, complete data but slow recovery and large file; production recommends RDB + AOF hybrid (balances recovery speed and data completeness); selection basis: cache scenarios that tolerate data loss can use RDB; critical business data should use AOF or hybrid.
> 中文提示：RDB 恢复快但丢数据；AOF 数据完整但恢复慢；生产推荐混合模式

**Q: Why is Redis single-threaded fast? What is the risk? How do you avoid it?**
Answer framework: Pure in-memory operations are extremely fast (no disk IO) + single-threaded avoids lock contention and context switching; risk: one slow operation blocks all requests (`KEYS *` is the classic production incident cause); avoid by replacing `KEYS *` with `SCAN` (progressive scanning, cursor-based iteration, each call is fast).
> 中文提示：`KEYS *` 是生产事故元凶；用 `SCAN` 替代（渐进式 cursor 迭代，每次调用都快）

**Q: What different problems do Redis Sentinel and Redis Cluster solve?**
Answer framework: Sentinel solves HA (auto primary failover when primary fails), does not solve data volume; Cluster solves capacity (Hash Slot sharding across multiple nodes); complementary: production standard is Cluster with multiple nodes, each node has Sentinel-monitored primary-replica.
> 中文提示：Sentinel = HA 高可用；Cluster = 数据量 + 横向扩展；两者互补，生产通常同时使用

**Q: What is the principle of a Bloom Filter? What is a false positive?**
Answer framework: Multiple hash functions set bits + query checks if all bits are 1; false positive (hash collision mistakenly judges "exists") is acceptable (at worst recommends one already-watched video); no false negative (bit=0 means definitely doesn't exist); suited for "check existence" scenarios where a small error rate is acceptable at large scale; doesn't support deletion (use Counting Bloom Filter instead).
> 中文提示：假阳性可接受（顶多多推一个），无假阴性（bit=0 绝对不存在）；不支持删除

**Q: How would you implement a distributed rate limiter using Redis?**
Answer framework: Start with fixed-window (INCR + EXPIRE) — explain the implementation, then name the boundary burst problem. Upgrade to sliding window using a Sorted Set per user (ZADD timestamps, ZREMRANGEBYSCORE, ZCARD) wrapped in a Lua script for atomicity. State the tradeoff: fixed-window is O(1) memory per user; sliding-window log is O(requests-per-window) but accurate. For most production rate limiting, fixed-window is sufficient; sliding-window is for strict SLA enforcement.

**Q: When would you use Redis Pub/Sub vs Redis Streams vs Kafka?**
Answer framework: Pub/Sub = ephemeral, real-time, at-most-once — good for live notifications where missing a message is acceptable. Streams = durable, consumer groups with ACK, message replay — good for work queues and async pipelines at moderate scale. Kafka = high-throughput, long retention, independent consumer groups replaying at different offsets — good for event sourcing and data pipelines. Decision factors: durability requirements, replay needs, scale, operational complexity tolerance.

**Q: How would you implement a distributed lock in Redis? What are the failure modes?**
Answer framework: Simple case: SET NX EX — atomic, correct for single-node. Failure modes: (1) lock TTL expires before work completes → another process acquires while first still holds; fix with fencing tokens. (2) Node failure before replication → lock lost; fix with Redlock across N nodes. Emphasize: for most applications single-node SET NX EX is sufficient; Redlock adds complexity and is rarely needed. Close with: if you need guaranteed correctness under network partition, use ZooKeeper/etcd rather than Redis.

**Q: You're designing a "nearby drivers" feature. How would you use Redis?**
Answer framework: GEOADD to store driver lat/lon with driver ID as member; GEOSEARCH to find drivers within radius on each request. Discuss update frequency (driver location updates every N seconds — GEOADD is idempotent, just overwrites). Discuss hot key risk (all drivers in one city → one slot). If city-level sharding is needed, use city as part of the key to control slot distribution. Mention geohash internals at depth if pressed: bounding-box candidate fetch + exact-radius filter second pass.

## Summary

Redis's value is as the high-speed cache layer of distributed systems: trade memory for speed, and match data structures precisely to use cases. Choosing the right data structure is central to Redis usage: String for counting, Bitmap for status bitmaps, ZSet for leaderboards, List for time-ordered queues — each structure is optimized for specific query patterns; choosing wrong loses performance or functionality.

Redis's two most common production risks: ① slow operations in single-threaded mode (`KEYS *` blocks the entire instance); ② failover latency when the primary goes down (Sentinel triggers Leader Election with second-level delay). The former is avoided with `SCAN`; the latter requires application-layer retry and connection pool configuration.

From an AI Infra perspective, Redis is important for: ① training job scheduling queues (ZSet for priority-based scheduling); ② GPU resource allocation state caching (fast lookup of which GPUs are available); ③ distributed locks (`SET NX EX` for training job mutual exclusion); ④ inference service request deduplication (Bloom Filter to filter duplicate inference requests). Sentinel's Quorum voting mechanism and Raft consensus share the same idea — both use majority quorum to avoid single-point false positives — a distributed consensus foundation that runs through etcd, Kafka ISR, and Redis Sentinel.

> 面试重点：数据结构选型（四场景）→ RDB+AOF 持久化配置 → 单线程 SCAN vs KEYS* → Sentinel vs Cluster 互补 → Bloom Filter 原理

## Raw Material
- [[raw_material/tech/system-design/sd-redis]]
- [[raw_material/tech/system-design/Redis - Hello Interview]]
