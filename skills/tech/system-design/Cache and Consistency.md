---
title: Cache and Consistency
category: tech/system-design
tags: [cache, consistency, lru, lfu, ttl, cache-stampede, cap-theorem, cache-aside, write-through, fanout]
status: in-progress
priority: high
last_updated: 2026-04-06
created_from_jd:
---

# Cache and Consistency

## Knowledge Map
- Prerequisites（前置知识）：[[Distributed Systems]], [[Database Indexing]]
- Related Topics（延伸话题）：[[Redis]], [[Message Queue]], [[NoSQL Databases]]
- Management（管理关联）：[[Technical Roadmap]]

## Core Concepts

**Cache Eviction Policies（缓存淘汰策略）**
- **LRU** (Least Recently Used): evicts data that hasn't been accessed the longest; simple but doesn't consider importance （最近最少使用）
- **LFU** (Least Frequently Used): evicts data with the lowest historical access count; better at sensing "hotness" but higher maintenance cost （最低频率）
- **TTL** (Time-To-Live): auto-expires at deadline; simplest fallback mechanism
- For important-but-cold data being evicted: **isolate by type into separate cache instances** (simplest solution, more practical than tuning complex weights)

**Cache Consistency: Cache-Aside and Double Delete（缓存一致性）**
- **Cache-Aside**: on read miss, query DB and write back to cache; on update: delete cache first → update DB → delete cache again (Double Delete)
- Race condition with "delete cache first, then update DB": Thread A deletes cache → Thread B reads miss → reads old value from DB → writes back to cache → A writes new value to DB → cache still holds old value
- **Double Delete**: delete cache again after updating DB, reducing the inconsistency window; when the second delete fails, **TTL serves as the final safety net** （最终兜底）
- **Write-Through**: write to cache only, cache asynchronously syncs to DB; data won't be lost but write path is complex

**Cache Stampede（缓存雪崩/穿透）**
- Massive requests simultaneously find the cache expired and all hit the database
- Solution ①: **Single Flight / Request Coalescing**: only allow one request to query DB; others wait for the same result
- Solution ②: **Multiple read replicas** to distribute concurrent load
- Solution ③: **Async pre-refresh**: background refresh before TTL expires — avoids the expiration spike
- When the cache lock itself becomes a bottleneck: shard with multiple replicas to reduce single-point pressure; return stale data non-blocking or a retry hint

**CAP Theorem and Consistency Models（CAP 定理）**
- C (Consistency), A (Availability), P (Partition Tolerance) — choose two; large systems must have P, so the real choice is **CP vs AP**
- CP example: ZooKeeper (stale data has high cost); AP example: Cassandra/DynamoDB (unavailability is worse than stale data)
- Practical SLA for "eventual" consistency: product team defines the time bound (e.g., 99% of messages delivered within 3 seconds) → monitor the metric → breach triggers incident

**Social Feed: Push vs Pull Fan-out（推拉模式）**
- **Push (Fan-out on Write)**: when a post is created, write to all followers' inboxes; for regular users with few followers — low read latency （普通用户用推）
- **Pull (Fan-out on Read)**: aggregate all followed users' posts at read time; for celebrities — push to 50 million followers is infeasible （名人用拉）
- Celebrity posting: **Kafka async processing** (posting triggers a message → Consumer asynchronously writes inboxes, avoids blocking on 50 million synchronous writes)
- Hybrid mode: follower count threshold (e.g., 100K) as the push/pull switch

**Load Shedding（负载降级）**
- Proactively drop some requests/messages to keep core services available
- Applicable: AP systems (content feeds — dropping a few posts is acceptable); not applicable: CP systems (finance — every transaction must be processed)
- When degrading, must distinguish priorities: core Topics (inventory/points) → at-least-once; non-core (email/notification) → can be degraded

**Cache Hierarchy — Where to Cache（缓存层次）**
- **External Cache (Redis/Memcached)**: standalone cache service between app and DB; shared across multiple App Servers; supports LRU eviction and TTL; default answer in interviews
- **CDN**: geographically distributed edge cache; for static media (images/video); origin → edge on first request, subsequent users hit cache (250ms → 20ms); Cloudflare, Fastly, Akamai; mention in interviews only when the system needs large-scale media distribution
- **In-Process Cache**: app-process-local cache in memory; faster than Redis (no network RTT); suited for small-volume high-frequency reads that change rarely (config, feature flags, hot keys); downside: not shared across instances, invalidation broadcast is hard; supplement Redis in interviews as an optimization layer
- **Client-Side Cache**: browser HTTP Cache, LocalStorage, app local storage; backend has weak control — relies mainly on Cache-Control headers and ETags

**Write-Behind (Write-Back)（写后置）**
- App only writes to cache; cache asynchronously batch-writes to DB (background flush)
- Pros: extremely fast writes; cons: data written to cache but not yet flushed is lost if cache crashes
- Suited for: high write throughput + tolerable occasional data loss (analytics/event tracking pipelines)

**Read-Through（读穿透）**
- Cache acts as a smart proxy: app only interacts with cache; on cache miss, the cache automatically fetches from DB, stores the result, and returns it
- vs Cache-Aside: Cache-Aside has the app handle the fetch logic; Read-Through is handled by the cache framework
- CDN is essentially Read-Through; Cache-Aside is more common at the Redis application layer
- Rarely proposed in interviews (except when discussing CDN)

**Hot Keys（热点 Key）**
- A single cache key receives extremely high request volume (e.g., celebrity user profile, viral product) — can overwhelm a single Redis node even if overall hit rate is high
- Solution ①: **Key Replication**: store the same value under multiple replica keys (user:taylorswift:0 ~ user:taylorswift:9), randomly route reads to distribute load
- Solution ②: **In-Process Fallback**: cache the hottest key in the process's own memory, bypassing the single Redis node
- Solution ③: Rate Limiting — limit concurrent requests to the specific key

**Systematic Framework for Introducing Caching in Interviews（面试系统化引入框架）**
1. **Identify Bottleneck**: quantify the problem first ("500 QPS hitting DB, each 30ms — this is the bottleneck")
2. **Decide What to Cache**: high-frequency reads, low-frequency writes, expensive computations; design the cache key (user:123:profile)
3. **Choose Architecture**: default Cache-Aside; high consistency → Write-Through; high write volume + tolerable loss → Write-Behind
4. **Set Eviction Policy**: LRU is the safe default; TTL prevents stale data
5. **Address Downsides**: proactively discuss Cache Invalidation, Stampede, and fallback on Cache Failure (circuit breaker)

## Key Questions

**Q: How do you guarantee cache consistency? What is the race condition in Double Delete?**
Answer framework: Race condition in "delete cache first, then update DB" (Thread B reads miss and writes back stale value); Double Delete (delete cache again after updating DB); TTL as final safety net; short TTL for important frequently-updated data, at the cost of lower Cache Hit Rate.
> 中文提示：先删后更新的竞态；Double Delete 减少不一致窗口；TTL 是最终兜底；短 TTL 换一致性但降低命中率

**Q: What is Cache Stampede? What are the solutions and their limitations?**
Answer framework: Massive requests simultaneously find cache expired and hit DB; three solutions: Single Flight (the lock itself can become a bottleneck — shard with replicas), multiple read replicas (increased cost), async pre-refresh (best but complex implementation); combine based on data hotness and consistency requirements.
> 中文提示：三种解法各有代价；Single Flight 锁可能成瓶颈；异步预刷新最优但实现复杂

**Q: How do you decide between strong consistency and eventual consistency in a system design?**
Answer framework: Three-question framework: ① cost of wrong data (money/inventory → strong consistency); ② cost of unavailability (unavailability worse than stale data → AP); ③ how extreme are peak traffic levels (design Load Shedding proactively); give concrete examples: fund transfer = strong consistency, friend circle likes = eventual consistency.
> 中文提示：三问：数据错的代价 + 不可用的代价 + 峰值极端程度；用具体例子（转账 vs 朋友圈点赞数）说明

**Q: In a social feed, how do you handle a celebrity (50 million followers) posting?**
Answer framework: Pure push = 50 million synchronous writes — infeasible; use Kafka async push (posting triggers a message, Consumer asynchronously writes inboxes); hybrid mode (regular users push, celebrities pull, fan count threshold switches) is WeChat's actual approach; extend to recommendation Feed (highly personalized, not suited to caching the Feed list itself).
> 中文提示：名人 5000 万粉丝用 Kafka 异步推；混合模式（粉丝数阈值切推/拉）是微信实际方案

**Q: How do you choose a cache eviction policy? How do you protect important-but-rarely-accessed data?**
Answer framework: Don't over-optimize with complex weight tuning; the simplest solution is isolating by importance into separate cache instances; LRU suits most scenarios; LFU suits scenarios needing historical hotness sensing; TTL is the universal safety net — short TTL trades Cache Hit Rate for consistency.
> 中文提示：最简方案是隔离重要数据到独立缓存实例；LRU 是安全默认值；TTL 通用兜底

**Q: How do you handle Hot Keys in the system?**
Answer framework: First identify the scenario (celebrity user/viral product), explain why a single Redis node can be overwhelmed even with high hit rate; three solutions: Key Replication (most direct), In-Process Cache fallback (for the hottest keys), Rate Limiting (symptomatic treatment); weigh complexity vs benefit based on system scale.
> 中文提示：先识别场景，解释为何单节点会被打垮；三种解法：Key 复制（最直接）+ 进程内缓存（极热）+ 限流（治标）

**Q: How do you systematically introduce caching in an interview?**
Answer framework: 5-step framework: quantify bottleneck → decide what to cache (high-frequency low-change) → choose architecture (default Cache-Aside) → set eviction policy (LRU + TTL) → proactively surface and solve downsides (Stampede, Invalidation, failure fallback); scoring points come from proactively discussing trade-offs, not just saying "use Redis."
> 中文提示：五步框架；得分点在于主动讨论 trade-off，而非只说"用 Redis"

**Q: Write-Through vs Write-Behind vs Cache-Aside — what scenarios does each suit?**
Answer framework: Cache-Aside (most common) → read-heavy, moderate consistency requirements; Write-Through → updates cache and DB in sync on write, strong consistency but slower writes; Write-Behind → writes only to cache, async flush, fast writes but data loss risk; in interviews: start with Cache-Aside, introduce others based on scenario constraints.
> 中文提示：默认 Cache-Aside；高一致性需求选 Write-Through；高写吞吐且可容忍丢数据选 Write-Behind

## Summary

The core tension in cache system design is the **trade-off between performance and consistency**. Understanding this trade-off requires first clarifying the business's tolerance for data consistency (the CP vs AP choice from CAP theorem), then deciding on caching strategy (Cache-Aside / Write-Through) and invalidation strategy (TTL / Double Delete). There is no universal answer — only trade-offs based on business constraints.

Cache Stampede is the most common failure mode in cache systems under high concurrency. Single Flight is the most direct solution — philosophically aligned with Circuit Breaker's Half-Open probe: both are about "controlling traffic and giving the system a chance to recover gradually" rather than "letting everything through and causing a second crash."

The social feed push/pull hybrid is a classic example of "no perfect answer, only an answer that fits the context": pure push is too heavy (celebrity write amplification), pure pull is too slow (every read aggregates); hybrid is the engineering balance. This trade-off discussion framework can be directly applied to AI model result caching strategies (whether to cache model predictions, caching granularity, TTL settings).

The key to introducing caching in an interview is **first establishing the context for why caching is needed** (quantify the DB bottleneck), then systematically walking through the 5-step framework (what to cache → which pattern → eviction → downsides). Hot Keys and Cache Stampede are the depth-probing questions — candidates who proactively raise them and provide layered solutions stand out. The cache hierarchy (External → CDN → In-Process) also demonstrates understanding of overall system architecture, not just "use Redis."

> 面试重点：Cache-Aside + Double Delete（竞态问题）→ Cache Stampede 三种解法 → CAP 定理（CP vs AP 选型框架）→ 推拉混合模式 → Hot Key 三种解法 → 五步系统化引入缓存框架

## Raw Material
- [[raw_material/tech/system-design/sd-cache]]
- [[raw_material/tech/system-design/caching]]
