---
title: Sharding and Scalability
category: tech/system-design
tags: [sharding, consistent-hashing, virtual-nodes, hot-key, read-replica, scale-out, cap-theorem, back-of-envelope, capacity-estimation, range-sharding, directory-sharding, saga-pattern, 2pc, cross-shard]
status: in-progress
priority: high
last_updated: 2026-04-06
created_from_jd:
---

# Sharding and Scalability

## Knowledge Map
- Prerequisites（前置知识）：[[Distributed Systems]], [[Database Indexing]], [[Cache and Consistency]]
- Related Topics（延伸话题）：[[NoSQL Databases]], [[Redis]], [[Message Queue]]
- Management（管理关联）：[[Technical Roadmap]]

## Core Concepts

**Vertical vs Horizontal Scaling（垂直 vs 水平扩展）**
- **Vertical (Scale Up)**: upgrade to a stronger server; simple, no code changes, but hardware has an upper limit — not sustainable; good for early-stage fast iteration
- **Horizontal (Scale Out)**: add more servers; strong scalability, but requires designing partitioning strategies and has migration risk; the inevitable choice after hitting single-machine limits

**Shard Key Selection（分片键选择）**
- Hash the Shard Key and route to the corresponding server; choosing wrong → extremely high cost to migrate later
- Select based on the primary query pattern (query by user_id vs query by username depends on actual usage)
- Good Shard Key: high cardinality (many distinct values), even distribution, matches primary query path

**Hashing Strategies（哈希策略）**
- **Modulo Hash** (`user_id % N`): when adding/removing servers, N changes → almost all data routes change (10 → 11 servers: ~90% data needs migration) — not suitable for production （不可用于生产）
- **Consistent Hashing** (Hash Ring): servers map to points on a ring; data hashes to the nearest clockwise node; adding/removing nodes only affects adjacent node data — migration volume greatly reduced
- **Virtual Nodes**: a more capable server gets more virtual nodes on the ring, handling more data (weighted distribution); used by Cassandra and DynamoDB
- What Consistent Hashing cannot solve: **Hot Key** (some data has extremely high access frequency — no matter how even the hash, it always lands on the same node)

**Three Approaches to Hot Key（热点 Key 三种方案）**
1. **Add cache (Redis)**: put hot data in memory, reduce DB pressure; limitation: Cache Stampede on cache expiration
2. **Multiple read replicas**: add read nodes to distribute read traffic; limitation: primary-replica replication lag, may read stale data
3. **Read-write separation**: writes go to primary, reads go to replicas; limitation: replication lag, unsuitable for strong consistency scenarios
- All three are typically combined; caching is the first line of defense

**Race Condition Risk with Read-Write Separation（读写分离竞态）**
- Celebrity updates avatar: write to primary → delete cache first (prevent stale write-back) → during replica replication lag, replica still has old data
- During replica lag, someone reads from replica and writes stale value back to cache → two solutions:
  - **Force cache miss to read primary** (high consistency, increases primary load)
  - **Set short TTL** (allow brief stale data window; TTL auto-corrects)
- Use option ① for critical business; use option ② for content/feed (AP system)

**Capacity Estimation — Back-of-Envelope（容量估算）**
- Interview first step: clarify requirements — **system scale** (DAU, data volume) + **non-functional requirements** (availability, latency, consistency)
- 100M DAU → average TPS ≈ 100M / 100K seconds ≈ **1,000 TPS**; peak = average × 3–10x ≈ 3,000–10,000 TPS
- Read/write ratio 100:1 + peak 10,000 TPS → peak reads 9,900 TPS, peak writes 100 TPS → read-write separation + multiple read replicas
- Single machine QPS ≈ 10,000–50,000; estimate number of machines needed; every tech decision must be tied to the demand numbers

**Comprehensive Case: Weibo Celebrity Posts Full Chain（综合案例）**
- Write: Client → API Gateway → Service Layer (Consistent Hash routing by user_id) → write primary DB + delete cache
- Primary-replica sync: primary DB → read replicas async sync (content feed AP, accepts brief inconsistency)
- Fan distribution: regular users push (Kafka async writes inboxes); celebrities pull (50 million followers — push infeasible)
- Read scaling: hot data Redis cache + multiple read replicas; Hot Key scenario adds in-process cache

**Partitioning vs Sharding（分区 vs 分片）**
- **Partitioning**: split large tables within a single DB instance without adding machines; horizontal partition (by row — e.g., by year) / vertical partition (by column — e.g., cold vs hot columns)
- **Sharding**: horizontal partitioning across multiple machines; each Shard is an independent database with its own CPU/memory/storage; purpose is to break through single-machine storage and throughput limits
- Core difference: Partitioning doesn't cross machine boundaries; Sharding distributes data across multiple independent machines

**Shard Key Selection Criteria（分片键选择标准）**
- **High Cardinality**: many distinct values; a boolean field can have at most 2 Shards — meaningless
- **Even Distribution**: values must be evenly spread; sharding by `country` with 90% users in the US causes severe skew
- **Query Alignment**: common queries should hit only one Shard; if most operations are "fetch all data for a user," then `user_id` is the perfect choice
- Good examples: `user_id` (millions of users, even, query by user dimension), `order_id` (high cardinality, even)
- Bad examples: `is_premium` (cardinality 2), `created_at` (all new writes concentrate on the latest Shard — write hotspot)

**Three Sharding Strategies（三种分片策略）**
- **Range-Based Sharding**: partition by value range (e.g., user_id 1–1M → Shard1); pros: efficient range queries, simple implementation; cons: time-based sharding concentrates new writes on the latest Shard (write hotspot); suited for multi-tenant systems (one range per company, mutually isolated)
- **Hash-Based Sharding** (default): `shard = hash(key) % N`; pros: even distribution, no write hotspot; cons: N changes when adding/removing Shards → large data migration, needs Consistent Hash; the interview default
- **Directory-Based Sharding**: maintains a lookup table (`user_id → shard`); pros: flexible, can move any key to a dedicated Shard at any time; cons: every request requires a lookup, lookup service is a single point of failure (whole system stops if down); only for special requirements — generally not recommended in interviews

**Cross-Shard Queries（跨分片查询）**
- Queries without Shard Key filter (e.g., "global Top 10 hot posts") require broadcasting to all Shards and aggregating — overhead = N × single Shard latency
- Mitigation strategies:
  1. **Cache**: cache results for 5 minutes; 1,000 requests → only one full-Shard broadcast; suited for eventual consistency scenarios (leaderboards, trending)
  2. **Denormalization**: redundantly store related data in the same Shard (e.g., posts include user info); trade storage for single-Shard queries
  3. **Accept occasional cross-Shard queries**: admin dashboard "total user count" — low-frequency, slow queries acceptable
- Interview signal: if common paths frequently cross Shards, the Shard Key design or data model needs reconsideration

**Distributed Consistency: 2PC vs Saga（分布式事务）**
- Cross-Shard transactions cannot use single-machine DB transactions; two approaches:
- **Two-Phase Commit (2PC)**: coordinator asks all Shards "are you ready?"; on universal confirmation, commits; guarantees consistency but slow and fragile (any Shard or coordinator failure can deadlock the entire transaction); rarely used in production
- **Saga Pattern**: splits the transaction into steps, each with a corresponding compensating operation; on failure, executes compensations in reverse (e.g., transfer: deduct A success + credit B failure → compensate by reversing deduct A); eventual consistency rather than strong consistency
- **Best design: avoid cross-Shard transactions**: put all data belonging to the same user on the same Shard — transactions are naturally single-Shard
- Rule of thumb: if distributed transactions are frequently needed, the Shard Key or Shard boundaries are wrong

**Modern Database Sharding Support（现代数据库分片支持）**
- **NoSQL**: Cassandra (Murmur3 Consistent Hash + virtual nodes), DynamoDB (partition key hash, auto-split/merge), MongoDB (range-based chunks + optional hash shard key + auto balancer)
- **SQL**: Vitess (MySQL sharding layer, supports operator-driven online resharding), Citus (PostgreSQL extension), AWS Aurora, Cloud Spanner
- Standard interview phrasing: "use DynamoDB with user_id as the partition key" or "use Vitess to shard MySQL by user_id, plan to use online resharding for scaling" — no need to write custom sharding logic

**When and How to Introduce Sharding in Interviews（面试时机与框架）**
- **When to propose sharding**: calculate capacity first (storage/write throughput/read throughput), prove single machine can't handle it before proposing; common triggers:
  - Storage: 500M users × 5KB = 2.5TB, barely fits one machine, 10x growth requires sharding
  - Write throughput: peak 50K writes/s exceeds single-machine limit
  - Read throughput: even adding read replicas isn't enough
- **Most common mistake**: saying "we need to shard" before doing the math — prove necessity first
- **Interview four steps**: ① propose Shard Key and rationale (query-pattern-driven) → ② choose distribution strategy (default Hash + Consistent Hash) → ③ state trade-offs (how to handle cross-Shard queries) → ④ state scaling plan (Consistent Hash or online resharding)

## Key Questions

**Q: What is the difference between Modulo Hash and Consistent Hashing? When do you use Consistent Hashing?**
Answer framework: Modulo Hash changes most routes when adding/removing nodes (10→11 servers: 90% data migrated) — not suitable for dynamic scaling; Consistent Hash minimizes migration (only adjacent nodes affected) when adding/removing nodes; Virtual Nodes solve uneven capacity distribution; Cassandra/DynamoDB both use Consistent Hash + Virtual Nodes.
> 中文提示：取模 Hash 加减节点迁移 90% 数据（不可用）；一致性 Hash 只迁移相邻节点数据；虚拟节点解决能力不均

**Q: How do you solve the Hot Key problem? What are the limitations of each approach?**
Answer framework: Cache (Cache Stampede risk) + multiple read replicas (replication lag) + read-write separation (unsuitable for strong consistency); all three typically combined; emphasize cache as the first line of defense; proactively state the race condition under replica lag and two solutions (force read primary on cache miss vs short TTL).
> 中文提示：缓存是第一道防线；主动说出 Replica 延迟下的竞态和两种解法

**Q: How do you do capacity estimation in an interview?**
Answer framework: Clarify DAU and read/write ratio first; DAU ÷ 100K seconds = average TPS; peak × 3–10x; read/write ratio derives architecture (few writes, many reads → read-write separation + cache); single machine QPS 10K–50K, estimate server count; every tech decision should be supported by numbers (don't say "need distributed," say "because 500M DAU + high read/write ratio, shard by X").
> 中文提示：DAU÷10万秒=平均 TPS；峰值×3-10倍；每个技术决策用数字支撑；不要没算就说要分片

**Q: What are the risks of read-write separation? How do you handle replica lag?**
Answer framework: Primary-replica async replication has a latency window during which reads from replicas may return stale data; double race condition of write+delete cache and replica lag (someone reads stale value from replica and writes back to cache); two solutions: force read primary on cache miss (high consistency, more primary load) vs short TTL fallback (accepts brief inconsistency); choose based on business consistency requirements.
> 中文提示：Replica 延迟 + 缓存删除的双重竞态；强一致场景 cache miss 读主节点；AP 场景短 TTL 兜底

**Q: When should you use horizontal scaling instead of vertical scaling?**
Answer framework: Vertical scaling is simple (upgrade machines), good for early-stage fast iteration; switch to horizontal when hitting single-machine limits or unsustainable cost; horizontal requires Shard Key design and partitioning strategy with high migration risk; key judgment: whether data volume and QPS are approaching single-machine limits, and whether the Shard Key can distribute evenly.
> 中文提示：垂直先用（简单），单机瓶颈后切水平；水平扩展需要 Shard Key 设计，迁移风险高

**Q: What are the pros and cons of Range-based, Hash-based, and Directory-based sharding? How do you choose?**
Answer framework: Range is simple and supports range scans, but time fields create write hotspots; Hash distributes evenly — the default choice, but adding/removing nodes requires Consistent Hash to avoid large migrations; Directory is most flexible but every request adds a lookup and the lookup service is a single point of failure — only for special requirements. Interview default: Hash + Consistent Hash, unless multi-tenant range isolation or extreme flexibility is needed.
> 中文提示：Range 简单支持范围查询但时间字段写热点；Hash 均匀是默认选择；Directory 灵活但单点故障，面试一般不推荐

**Q: How do you handle cross-Shard queries? Use "global leaderboard" as an example.**
Answer framework: State cross-Shard cost explicitly (broadcast N Shards + result aggregation = high latency) → three mitigations: ① cache results (eventual consistency acceptable for leaderboards/trending — first choice); ② denormalize data to the same Shard; ③ low-frequency scenarios accept slow queries directly; interview focus: first ask "how frequent is this query?" — high-frequency paths absolutely cannot accept full-Shard broadcast.
> 中文提示：先问查询频率；高频路径绝不接受全 Shard 广播；三种缓解：缓存（最常用）+ 反范式化 + 低频接受慢查询

**Q: How do you ensure consistency in cross-Shard transactions? What scenarios do 2PC and Saga each suit?**
Answer framework: 2PC is strongly consistent but slow and has single point of failure risk (coordinator failure can deadlock) — rarely used in production; Saga splits into steps with compensating operations, eventual consistency, suited for most scenarios; best design is putting the same user's data on the same Shard to completely avoid cross-Shard transactions; if cross-Shard transactions are frequently needed, the Shard Key or boundaries are wrong.
> 中文提示：最佳设计是避免跨分片事务；2PC 强一致但慢且有死锁风险；Saga 最终一致适合大多数场景

**Q: In a system design interview, when should you propose sharding and how do you introduce it naturally?**
Answer framework: Do capacity estimation first to prove necessity (don't introduce without cause); triggers: storage exceeds single-machine limit, write throughput exceeds single-machine QPS, read replicas still insufficient; four steps: ① Shard Key and rationale (query-pattern-driven) ② distribution strategy (default Hash) ③ trade-offs (how to handle cross-Shard queries) ④ scaling plan (Consistent Hash / online resharding); most common mistake: saying "we need to shard" before doing the math.
> 中文提示：先算容量证明必要性；四步框架：Shard Key + 策略 + trade-off + 扩容方案；最常见失误是没算就说要分片

## Summary

The core of sharding and scalability design comes down to two questions: **how to partition data** (Shard Key selection + Hash strategy) and **how to handle hotspots** (Hot Key three approaches). Modulo Hash is simple but doesn't support dynamic scaling; Consistent Hash + Virtual Nodes is the production-grade standard for distributed systems (Cassandra/DynamoDB/Redis Cluster). Hot Key is the problem that remains even after even distribution from hashing — requires a combination of cache/multiple replicas/read-write separation.

There are three sharding strategies: **Hash-based** (default, even distribution, use Consistent Hash for resharding), **Range-based** (range-query-friendly, be cautious with time fields), **Directory-based** (flexible but with single point of failure risk — generally not recommended in interviews). Three criteria for Shard Key selection: high cardinality, even distribution, matches primary query path. Good design makes 99% of queries single-Shard operations — cross-Shard queries should be handled via caching, denormalization, or low-frequency acceptance, not treated as normal paths; cross-Shard transactions should be eliminated through design rather than relying on 2PC; when needed, use Saga for eventual consistency.

Capacity estimation (Back-of-envelope) is the foundation of system design interviews — its value is not in number precision but in **driving design decisions with numbers**: DAU → TPS, TPS and read/write ratio → architecture direction (cache/read-write separation/sharding), then server count after sharding. Architecture proposals without numerical backing are just intuition in interviews; numerical backing makes them judgments. The correct order for introducing sharding: first prove single machine can't handle it (capacity estimation), then propose Shard Key + strategy, then trade-offs (cross-Shard queries/resharding plan). From an AI Infra perspective, GPU cluster scalability problems directly map to this section: the GPU "Shard Key" is job ID or user group, "Hot Key" is high-priority users, and Karpenter's dynamic node scaling is essentially automation of Scale Out.

> 面试重点：容量估算驱动设计决策 → Shard Key 三个标准（高基数/均匀/匹配查询）→ 三种分片策略（默认 Hash）→ Hot Key 三方案 → 跨分片查询处理（缓存/反范式化）→ 避免而非解决跨分片事务

## Raw Material
- [[raw_material/tech/system-design/sd-sharding]]
- [[raw_material/tech/system-design/sharding]]
