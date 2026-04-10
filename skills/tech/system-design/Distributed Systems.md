---
title: Distributed Systems
category: tech/system-design
tags: [distributed, consistency, availability, cap-theorem, consensus, sharding, caching, consistent-hashing, async, layered-architecture, high-concurrency]
status: in-progress
priority: high
last_updated: 2026-04-10
created_from_jd:
---

# Distributed Systems

## Knowledge Map
- Prerequisites（前置知识）：[[Networking Fundamentals]], [[Storage Systems]]
- Related Topics（延伸话题）：[[Consensus Algorithms]], [[Distributed Storage]], [[Message Queues]], [[Cache and Consistency]], [[Sharding and Scalability]], [[Layered Architecture]], [[Async Processing Patterns]]
- Management（管理关联）：[[Engineering Reliability Culture]], [[SRE Practices and SLO Engineering]]

## Core Concepts

- **CAP Theorem**: A distributed system can only guarantee 2 of 3 properties — Consistency (all nodes see the same data), Availability (every request gets a response), Partition Tolerance (system works during network failures). Since partitions are unavoidable, the real choice is **C vs A during a partition**.
  - **CP systems** (e.g., HBase, Zookeeper): refuse to serve stale data, may reject requests during partition
  - **AP systems** (e.g., Cassandra, DynamoDB): always respond, may return stale data until partition heals

- **Consistency models**:
  - **Strong consistency**: all nodes return the same value; requires coordination before responding; adds latency. Use for money, inventory, bookings.
  - **Eventual consistency**: nodes will converge given no new updates; no coordination cost; allows stale reads. Use for social feeds, recommendations, analytics.
  - **PACELC extends CAP**: even without partitions, tradeoff exists — strong consistency adds Latency; eventual consistency reduces it. Real-world design always involves this P-A/C and E-L/C tradeoff.

- **Sharding**: split data across multiple independent servers when a single DB hits storage (TBs), write throughput (>10K TPS), or read limits.
  - **Hash-based**: `hash(key) % N` → even distribution, avoids hot spots. Most common default.
  - **Range-based**: split by value ranges (e.g., user_id 0–10M on shard A) → risk of hot spots if traffic skews.
  - **Directory-based**: lookup table routes to correct shard → flexible but adds latency + dependency.
  - **Critical rule**: design shard key around your most common query. Queries within one shard are fast; cross-shard fan-out is expensive. Choose wisely upfront — resharding is painful.

- **Consistent hashing**: solves the shard rebalancing problem. Place both servers and keys on a virtual ring; a key belongs to the next server clockwise. Adding/removing a server only moves ~1/N fraction of keys (vs ~(N-1)/N with naive modulo). Used in: Redis Cluster, Cassandra, DynamoDB, some load balancers.

- **Caching** (distributed): store hot data in fast memory (Redis ~1ms) to avoid DB reads (~20-50ms). Core pattern: **cache-aside** — check cache first, on miss query DB and store result with TTL.
  - **Cache invalidation**: delete/update cache entries after writes; or use short TTLs and tolerate staleness.
  - **Cache stampede**: if Redis goes down, all traffic hits DB simultaneously → can cascade and take down the system. Mitigations: in-process L1 cache, circuit breakers, request coalescing.
  - **Don't cache everything**: only hot, infrequently-changing data. Caching frequently-updated data adds complexity with no benefit.

- **Data distribution tradeoffs**:
  - **Normalization**: data split across tables, no duplication → consistent, but joins get expensive at scale.
  - **Denormalization**: duplicate data to avoid joins → fast reads, but write fan-out complexity (update in N places).
  - Safe approach: start normalized, denormalize only hot read paths once you've measured the bottleneck.
  - **NoSQL (DynamoDB)**: requires upfront access pattern design. Partition key determines which queries are fast. Great for known, predictable access patterns; poor for ad-hoc querying.

- **Latency numbers every engineer should know**:
  - Memory access: ~1ns | SSD read: ~100μs | Network in same datacenter: 1–10ms | Cross-continent: 80–300ms
  - Implication: geographic distribution only matters when you need <50ms latency globally.

- **Throughput benchmarks** (for capacity planning / when to scale):

  | Component | Typical Limit | Scale Trigger |
  |-----------|--------------|---------------|
  | Cache (Redis) | 100K ops/sec, ~1ms | Hit rate < 80%, latency > 1ms |
  | Database (Postgres) | 50K TPS, 64TB+ storage | Writes > 10K TPS, storage in TBs |
  | App servers | 100K concurrent connections | CPU > 70%, latency > SLA |
  | Kafka | 1M msgs/sec per broker | Partition count ~200K/cluster |

- **Scale-up vs Scale-out** — two fundamental strategies for handling more load:
  - **Scale-up (垂直扩展)**: buy bigger hardware (more CPU/RAM). Simple, no distributed complexity. Limited by hardware ceiling and cost curve. Right choice early-stage or when distributed overhead exceeds benefit.
  - **Scale-out (水平扩展)**: add more nodes to a distributed cluster. Breaks single-machine ceiling; used by all large-scale internet systems. Introduces new challenges: node failure handling, state synchronization, transparent node addition/removal.
  - Rule of thumb: scale-up first until the cost or ceiling is hit; then scale-out. Never scale-out prematurely — distributed systems are fundamentally harder to operate.

- **Async processing**: decouple request receipt from request completion to absorb traffic bursts and reduce response latency.
  - **Sync**: caller blocks until callee finishes → simple but propagates latency; a slow downstream cascades into caller slowness and eventual overload.
  - **Async**: caller submits work to a queue and returns immediately; worker processes at own pace; caller is notified via callback / event / polling when done.
  - Classic example: ticket booking systems (e.g., 12306) — queue the reservation request, return "processing" immediately, notify user when confirmed. This lets the web tier shed load quickly and prevents thundering-herd failures during peak demand.
  - Key enabler: **message queues** (Kafka, RocketMQ, RabbitMQ). Producer publishes; consumer processes independently. Queue absorbs bursts and provides natural backpressure.
  - Tradeoff: async adds eventual-consistency semantics; users must tolerate delayed confirmation. Not suitable for operations where immediate confirmation is required (e.g., payment deduction).

- **Layered architecture** (分层架构): divide a system into horizontal layers, each with a single responsibility. Standard web system: Presentation → Logic → Data Access. Alibaba's extended model adds an **Open API layer** (gateway, auth, rate-limiting) and a **Manager layer** (generic business operations: cache/storage strategies, third-party API wrappers) between Logic (Service) and DAO.
  - Benefits: (1) separation of concerns — each team owns one layer; (2) reusability — the Manager layer can be shared across multiple Service implementations; (3) enables targeted horizontal scaling — CPU-bound logic layer can scale independently of the stateless presentation layer.
  - Rules: data flows only between adjacent layers; no layer skipping (presentation → DAO directly creates brittle coupling and kills maintainability).
  - Tradeoffs: adds code complexity and indirection; each extra layer adds a network hop in service-oriented architectures ("多一跳" problem). Worth it at scale; avoid premature layering for simple systems.

- **三高 goals — the north star for high-concurrency system design**:
  - **高性能 (High Performance)**: system responds fast under load (millisecond-level latency at high QPS). Achieved via caching, async, horizontal scaling, efficient algorithms.
  - **高可用 (High Availability)**: system remains operational over time (target: "五个九" = 99.999% uptime = <5 min downtime/year). Achieved via redundancy, no single points of failure, fast failover, and graceful degradation.
  - **可扩展 (Scalability/Extensibility)**: system can grow to handle traffic spikes and business evolution without complete rewrites. Achieved via layered architecture, loose coupling, stateless services, and clear extension points.
  - These three are interdependent but have tensions: high availability requires redundancy (cost); high performance may sacrifice consistency; scalability adds architectural complexity.

- **Evolutionary architecture principle**: systems should grow incrementally in response to actual problems, not anticipated ones.
  - Stage 1: simplest design that satisfies current business + traffic; use the most familiar tech stack.
  - Stage 2: fix specific bottlenecks as they appear (single points of failure, hot spots, slow components). Prefer mature community solutions over custom-built.
  - Stage 3: when incremental fixes no longer suffice, do targeted large-scale refactoring. Taobao's "五彩石" project — monolith → SOA — happened only after years of organic growth made it unavoidable.
  - **Anti-pattern**: copying hyperscaler architecture (Taobao, WeChat) from day one. Their systems are massively complex because they were forced to be by actual scale. Premature complexity kills startups and wastes engineering capacity.

## Key Questions

**Q: How does the CAP theorem affect a real system design decision you'd make?**
Answer framework: Acknowledge CAP is about partition behavior specifically. Pick a concrete example (e.g., shopping cart vs. inventory count) and explain why one needs AP (user experience) and the other needs CP (overselling = revenue loss). Extend to PACELC: even in healthy network, strong consistency adds latency, so use it only where stale data causes real harm.

**Q: Walk me through how you'd choose a shard key for a large-scale system.**
Answer framework: Start by identifying the most common query patterns. Choose a shard key that makes the hottest queries single-shard lookups. Discuss the tradeoff: fast for the chosen access pattern, slow/expensive for others (cross-shard fan-out). Give a concrete example (user_id for user-centric queries) and name the problematic query (trending posts across all users). Mention hot shard risk (celebrity problem) and how to mitigate (add randomness to key, or special-case high-traffic entities).

**Q: Explain consistent hashing — why does it matter and when would you use it?**
Answer framework: Start with the problem it solves (adding a node to naive modulo-sharding causes massive data movement). Explain the ring mechanism at a high level. State the key property: only ~1/N keys move on node addition/removal. Say where it's used (Redis Cluster, Cassandra, Memcached). In interviews, you can mention it as "we'd use consistent hashing to make node addition practical without bulk data migration" — you rarely need to explain the ring math unless specifically asked.

**Q: When should you use strong consistency vs eventual consistency?**
Answer framework: Default to eventual consistency. Use strong consistency only when stale data causes a real, quantifiable problem: inventory (overselling), payments (double-spend), bookings (double-booking). Everything else — feeds, recommendations, analytics, notifications — works fine eventually consistent. Point out you can mix models in the same system (product descriptions eventually consistent, checkout process strongly consistent).

**Q: How do you prevent a cache stampede, and why does it matter in production?**
Answer framework: Describe the failure mode (Redis down → all requests hit DB simultaneously → DB overwhelmed → cascading failure). Three mitigations: (1) in-process L1 cache as short-lived fallback, (2) request coalescing / mutex-lock to let only one request populate the cache, (3) circuit breaker to shed load and return degraded responses rather than overload DB. Emphasize this is a reliability design concern, not just a performance one.

**Q: A service is slow. You suspect the database. How do you decide between adding indexes, adding a cache, or sharding?**
Answer framework: First measure — is it reads or writes? For reads: check if an index covers the query; if yes, add index first (no infrastructure change). If still slow due to volume, add caching for hot reads. Only shard if write throughput exceeds ~10K TPS or storage is hitting TB scale. Propose sharding last — it's irreversible and adds operational complexity. Use the throughput benchmarks to justify each decision with numbers.

**Q: Compare PostgreSQL and DynamoDB — when do you choose each?**
Answer framework: Postgres for structured data with complex relationships, strong consistency requirements, and varied/ad-hoc query needs (reports, joins). DynamoDB for known access patterns at massive scale, when you can design partition + sort key upfront, and when horizontal scaling is a hard requirement. Key gotcha: DynamoDB forces you to know your queries before designing the schema — if access patterns change, you may need to remodel.

**Q: How does geographic distribution affect your system design?**
Answer framework: Cross-continent latency is ~80-300ms from physics (speed of light through fiber). If you need <50ms globally, you need regional deployments. That creates data synchronization complexity: replication lag, conflict resolution, consistency model choice per region. Most systems use active-passive (writes to one region, reads from nearest); active-active is possible but requires careful conflict handling. CDN handles static assets separately.

**Q: When would you use async processing instead of synchronous calls, and what are the tradeoffs?**
Answer framework: Use async when (1) the operation is long-running and the caller doesn't need an immediate result, (2) you need to absorb traffic bursts without blocking web-tier resources, or (3) downstream services are unreliable and you want to decouple failure propagation. Describe the mechanism (message queue, worker pool, callback/notification). State the tradeoff clearly: async introduces eventual-consistency semantics — callers must handle "pending" states and delayed notifications, which complicates UX. Reserve sync calls for operations where the caller needs an immediate guaranteed result (payment confirmation, inventory reservation).

**Q: How do you decide when a system needs to be redesigned vs. incrementally improved?**
Answer framework: Start from current pain points — are bottlenecks isolated (single component) or systemic (architectural)? Isolated: fix the component (add index, add cache, scale that service). Systemic: consider a targeted refactor (e.g., extract a layer, introduce a message queue). Full rewrites are a last resort. Give an example: Taobao moved monolith → SOA only after organic growth made further incremental fixes impractical. The risk of big-bang rewrites is high — prefer strangler-fig patterns that migrate incrementally.

**Q: Design the architecture for a system that needs to handle a 10x traffic spike during peak events (e.g., flash sale, live event).**
Answer framework: Three-layered approach: (1) **Absorb** — async queue at the entry point; web tier returns immediately and queues the work; prevents thundering herd from reaching backend. (2) **Distribute** — scale-out horizontally; stateless web/logic tier; consistent-hashing cache layer. (3) **Protect** — rate limiting at the API gateway; graceful degradation (serve cached/approximate data rather than failing); circuit breakers on downstream calls. Emphasize: don't scale everything uniformly — profile to find the actual bottleneck first (usually DB writes or a specific service), then scale that layer surgically.

## Summary

Distributed systems fundamentals are the vocabulary of every system design interview. The core theoretical framework is the CAP theorem: in a distributed system, network partitions are unavoidable, so you're always choosing between Consistency (all nodes return the same data) and Availability (every request gets a response) during failure events. The PACELC extension matters more in practice: even in healthy networks, strong consistency adds latency because nodes must coordinate before responding, while eventual consistency removes that coordination cost.

The practical design consequence: default to eventual consistency for most data (feeds, recommendations, analytics) and reserve strong consistency for domains where stale reads cause real harm — inventory, payments, bookings. You can and should mix consistency models within the same system, scoped to individual data types rather than applied globally. For horizontal data scaling, sharding splits data across servers with the shard key as the pivotal decision: it determines which queries are fast (single-shard lookups) and which require expensive fan-out (cross-shard aggregations). Consistent hashing makes elastic scaling practical by limiting key movement to ~1/N when adding nodes, vs the near-total redistribution that naive modulo hashing causes.

For engineering manager interviews, the differentiating skill is knowing *when* to apply each technique — not just *how*. Proposing sharding at 500GB or caching every data type signals inexperience. The benchmark numbers are your anchors: single Postgres handles ~50K TPS and TBs of data; Redis handles ~100K ops/sec; Kafka handles ~1M msgs/sec per broker. Drive architectural decisions with math ("we're at X TPS, which means Y"), and treat complexity escalation (sharding, distributed caching, geographic replication) as a last resort after simpler measures (indexes, read replicas, single-node tuning) have been exhausted.

The Chinese internet engineering tradition provides a useful mental model: the **三高** framework (高性能、高可用、可扩展) defines the three goals of any high-concurrency system. All architectural decisions — scale-up vs scale-out, sync vs async, monolith vs services — are evaluated against these three axes. Async processing via message queues is particularly powerful for absorbing burst traffic: the web tier queues work immediately and returns, decoupling request acceptance from request processing. This is how 12306 survived peak booking windows and how Taobao processes Double 11 orders. Finally, the most important meta-principle is evolutionary architecture: start simple, let actual load and pain points drive complexity. The graveyard of engineering is littered with systems that copied hyperscaler architecture before they had hyperscaler problems.

## Raw Material
- [[raw_material/tech/system-design/Distributed Systems - resources]]
- [[raw_material/tech/system-design/高并发系统]]
