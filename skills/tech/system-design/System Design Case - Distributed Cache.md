---
title: System Design Case - Distributed Cache
category: tech/system-design
tags: [system-design-case, distributed-systems, caching, lru-eviction, consistent-hashing, replication, fault-tolerance]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# System Design Case - Distributed Cache

## Knowledge Map
- 前置知识：hash maps, doubly linked lists, consistent hashing, primary-replica replication, leader election, quorum writes
- 延伸话题：Redis internals, Memcached vs. Redis, cache stampede, write-through vs. write-behind, read-through vs. cache-aside
- 管理关联：

## Core Concepts

- **LRU via Doubly Linked List + HashMap**: O(1) get/set/delete. HashMap maps `key → node` for O(1) lookup. Doubly linked list maintains access order (most recent at head, LRU at tail). On get: find node via map, move to head. On set: if full, evict tail node from both list and map, insert new node at head. All operations O(1) — no O(N) scan needed.
- **TTL Implementation (Tuple Storage + Background Janitor)**: Store `(value, expiration_timestamp)` tuples. On Get: check if `expiration > now` before returning (lazy eviction). Background janitor runs periodically (every minute) to proactively remove expired entries. Two-layer approach: lazy eviction for accuracy, janitor for memory reclamation.
- **Consistent Hashing for Horizontal Scale**: Hash ring maps keys to nodes. Adding/removing a node only remaps keys from/to adjacent nodes — not all keys. Virtual nodes (multiple ring positions per physical node) distribute load more evenly and reduce the impact of hotspot nodes.
- **Primary-Replica Replication for HA**: Writes go to primary; primary replicates asynchronously to replicas. Reads can serve from replicas (may be slightly stale). On primary failure, leader election promotes a replica. Janitor must propagate TTL expirations to all replicas to maintain consistency.
- **Scale Estimate: ~50 Nodes for 1TB**: 32GB RAM per instance, ~24GB usable after OS/overhead. 1TB / 24GB ≈ 42 nodes, rounded up to ~50 with headroom. Auto-scale trigger: >80% memory usage. New node insertion migrates keys from the adjacent node on the ring.
- **Background Data Migration During Rebalancing**: When a new node joins, keys must be migrated from the neighbor. During migration, reads for migrating keys fall back to the source node. This allows zero-downtime rebalancing without serving stale or missing data.
- **Quorum Writes for Network Partition**: In a partitioned network, split-brain (two primaries accepting writes) can cause data divergence. Quorum-based writes (majority of replicas must acknowledge) prevent split-brain. Detection: monitor write acknowledgment counts; if below quorum, reject writes.

## Key Questions

**Q: Implement LRU eviction in O(1) time for all operations.**
Answer framework: HashMap for O(1) key lookup + Doubly Linked List for O(1) access-order maintenance. Get: lookup node in map, move to list head (unlink + relink head). Set (existing): update value, move to head. Set (new, full cache): evict tail node (unlink from list, remove from map), insert new node at head and map. Delete: move to tail (or unlink directly and remove from map). Every operation is O(1) — no scan.

**Q: How do you handle TTL expiration efficiently?**
Answer framework: Two-layer approach. Lazy eviction: on every Get, check if `expiration_timestamp > now`; if expired, delete and return null. This is accurate but doesn't reclaim memory until the key is accessed. Background janitor: runs every minute, scans all keys, removes expired ones. The janitor handles memory for keys that are never accessed again after expiration.

**Q: You need to add a new cache node to a 50-node cluster. How do you avoid rehashing all keys?**
Answer framework: Consistent hashing. The new node is inserted at a position on the hash ring. It only takes keys from its clockwise neighbor (the previous owner of that ring segment). All other nodes are unaffected. Virtual nodes distribute the migration load. During migration, reads for affected keys fall back to the source node until migration completes.

**Q: A primary node fails. How does the cache recover?**
Answer framework: Heartbeat monitoring detects primary failure. Replicas hold an election (Raft or similar) to select a new primary. The new primary begins accepting writes. Any writes lost in the async replication lag between last replication and crash are gone (trade-off of async replication). To reduce this window, use synchronous replication for critical data, or accept the small loss window for cache data.

**Q: How do you handle a network partition (split-brain)?**
Answer framework: Quorum-based writes: a write succeeds only if a majority of replicas acknowledge it. If a partition isolates a minority, writes to that partition are rejected. On partition resolution, the minority catches up from the majority's log. Split-brain detection via monitoring acknowledgment counts.

**Q: What is the difference between your distributed cache and Redis?**
Answer framework: Redis is production-hardened with many eviction policies (LRU, LFU, allkeys-random), data structures (sorted sets, hashes, lists), persistence (AOF, RDB), clustering (Redis Cluster with hash slots), and Sentinel for HA. A custom implementation would cover the same core primitives but without the operational maturity. In practice: use Redis for production, implement from scratch only to demonstrate understanding.

## Summary

Building a distributed cache from scratch tests understanding of data structure fundamentals, distributed systems theory, and operational concerns. The single-node foundation is a HashMap + Doubly Linked List for O(1) LRU eviction, with TTL implemented as stored timestamps + background janitor.

Scaling to 1TB across ~50 nodes requires consistent hashing — the key insight being that node addition/removal only affects keys on adjacent ring segments, not the entire keyspace. This is fundamentally different from modular hashing (where adding a node requires rehashing everything). Virtual nodes smooth out load distribution.

High availability comes from primary-replica replication with leader election on primary failure. The hardest design question is the consistency trade-off: async replication achieves high throughput but means some writes may be lost on primary failure. Quorum writes provide stronger guarantees at latency cost. For a cache (where stale reads are already a known trade-off), async replication is usually the right default — but interviewers probe whether candidates understand the failure modes and can articulate the trade-off explicitly.

## Key Terms

**Technologies**
- `HashMap` · `Doubly Linked List` · `Consistent Hashing` · `Virtual Nodes` · `Redis Sentinel` · `Raft (Leader Election)`

**Patterns**
- `LRU Eviction` · `Lazy TTL Eviction + Background Janitor` · `Primary-Replica Replication` · `Quorum Writes` · `Read Fallback During Migration`

**Decision Points**
- `sync vs. async replication` · `quorum size vs. latency` · `janitor frequency vs. memory waste` · `virtual node count for load balancing`

## Raw Material
- [[raw_material/tech/system-design/hello-interview/case-distributed-cache.md]]
