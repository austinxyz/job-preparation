---
title: Redis
category: tech/system-design
tags: [redis, cache, in-memory, rdb, aof, zset, skip-list, sentinel, redis-cluster, bloom-filter, hash-slot]
status: draft
priority: high
last_updated: 2026-04-06
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

## Summary

Redis's value is as the high-speed cache layer of distributed systems: trade memory for speed, and match data structures precisely to use cases. Choosing the right data structure is central to Redis usage: String for counting, Bitmap for status bitmaps, ZSet for leaderboards, List for time-ordered queues — each structure is optimized for specific query patterns; choosing wrong loses performance or functionality.

Redis's two most common production risks: ① slow operations in single-threaded mode (`KEYS *` blocks the entire instance); ② failover latency when the primary goes down (Sentinel triggers Leader Election with second-level delay). The former is avoided with `SCAN`; the latter requires application-layer retry and connection pool configuration.

From an AI Infra perspective, Redis is important for: ① training job scheduling queues (ZSet for priority-based scheduling); ② GPU resource allocation state caching (fast lookup of which GPUs are available); ③ distributed locks (`SET NX EX` for training job mutual exclusion); ④ inference service request deduplication (Bloom Filter to filter duplicate inference requests). Sentinel's Quorum voting mechanism and Raft consensus share the same idea — both use majority quorum to avoid single-point false positives — a distributed consensus foundation that runs through etcd, Kafka ISR, and Redis Sentinel.

> 面试重点：数据结构选型（四场景）→ RDB+AOF 持久化配置 → 单线程 SCAN vs KEYS* → Sentinel vs Cluster 互补 → Bloom Filter 原理

## Raw Material
- [[raw_material/tech/system-design/sd-redis]]
