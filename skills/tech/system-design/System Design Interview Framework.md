---
title: System Design Interview Framework
category: tech/system-design
tags: [interview-framework, system-design, requirements, non-functional, api-design, high-level-design, deep-dive, core-concepts, technology-selection, distributed-systems]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# System Design Interview Framework

## Knowledge Map
- 前置知识：[[Distributed Systems]], [[System Design Numbers]], [[Database Indexing]], [[Networking Fundamentals]], [[Sharding and Scalability]]
- 延伸话题：[[Cache and Consistency]], [[Message Queue]], [[NoSQL Databases]]
- 管理关联：

## Core Concepts

- **Interview timeline (45-min format)**:
  1. **Requirements (Functional + Non-Functional)** — 5 min
  2. **Core Entities** — 2 min
  3. **API / System Interface** — 5 min
  4. **Data Flow** (optional; for backend systems with no direct API, e.g., crawlers) — 5 min
  5. **High-Level Design** (satisfies functional requirements) — 10–15 min
  6. **Deep Dive** (satisfies non-functional requirements) — 10 min

- **Non-Functional Requirements Checklist** — always address these during requirements phase:
  - **CAP**: consistency vs availability trade-off for this system
  - **Latency**: P99 target (e.g., <100ms for reads)
  - **Throughput / Scalability**: expected QPS / TPS at peak; growth trajectory
  - **Durability**: data persistence requirements; acceptable data loss window (RPO)
  - **Fault Tolerance**: expected uptime / availability (99.9% vs 99.99%)
  - **Security**: auth/authz, encryption at rest and in transit
  - **Compliance**: data residency, regulatory requirements (GDPR, HIPAA)
  - **Device / Environment**: mobile constraints, offline support, geographic distribution

- **11 Core System Design Concepts** (Hello Interview taxonomy):
  1. **Scaling** — vertical (bigger machine) vs horizontal (more machines + load balancer); Consistent Hashing for even distribution
  2. **Work Distribution** — load balancers, queue systems; keep load as even as possible across nodes
  3. **Data Distribution** — in-memory caching, database sharding/partitioning, fan-out patterns; introduces synchronization and consistency challenges
  4. **CAP Theorem** — C vs A tradeoff during partitions; strong consistency for inventory/booking/banking; eventual consistency for social feeds
  5. **Locking** — prevent race conditions when multiple clients access shared resources; consider lock granularity, lock duration, and whether optimistic updates can replace locks
  6. **Indexing (general)** — hash maps, sorted lists; read fast at the cost of write overhead
  7. **Database Indexing** — RDBMS B+ tree, DynamoDB secondary indexes, composite/covering/partial indexes
  8. **Specialized Indexes** — geospatial (PostGIS, Redis Geohash), vector databases (high-dimensional similarity), full-text (Elasticsearch via CDC)
  9. **Communication Protocols** — REST (stateless), SSE (one-way push), WebSocket (bidirectional stateful); tradeoffs in simplicity vs scalability
  10. **Security** — authentication/authorization (API gateway), encryption in transit (TLS) and at rest (DB encryption), rate limiting and throttling
  11. **Monitoring** — infrastructure (CPU/memory/disk/network), service-level (latency/error rates/throughput), application-level (active users, business metrics)

- **Technology selection cheat sheet**:

  | Need | Default Choice | Alternative / When |
  |------|---------------|--------------------|
  | Relational data, transactions | PostgreSQL / MySQL | Cloud Spanner (global strong consistency) |
  | High-write NoSQL | Cassandra | DynamoDB (managed, AWS) |
  | Key-value cache | Redis | Memcached (simpler, no persistence) |
  | Full-text search | Elasticsearch | Postgres GIN indexes (simpler, no separate cluster) |
  | Message queue | Kafka | SQS (managed, simpler; no replay by default) |
  | Blob storage | S3 / GCS | Azure Blob |
  | Distributed lock | Redis (Redlock) | Zookeeper (stronger consistency) |
  | Service communication | REST | gRPC (internal, high-perf) |
  | Real-time push | SSE (one-way) | WebSocket (bidirectional) |

- **Common Architectural Patterns** (ready-made for interviews):
  1. **Simple DB-backed CRUD with caching**: API Gateway → Load Balancer → App Servers → DB + Redis cache
  2. **Async job worker pool**: queue (SQS/Kafka) → worker pool; for image/video processing, crawlers; Kafka supports replay
  3. **Two-stage architecture**: Phase 1 fast+approximate (candidate retrieval) → Phase 2 slow+precise (re-ranking); used in recommendation systems, search engines, route planning
  4. **Event-Driven Architecture**: services react to events in real-time; highly responsive, loosely coupled, scalable
  5. **Durable Job Processing**: long-running jobs (hours/days); Kafka or Temporal (Cadence); handles partial failures via workflow state machines
  6. **Proximity-Based Services**: geospatial indexes (PostGIS/Redis Geohash) + region sharding

- **Database selection heuristic** (Hello Interview):
  - Product design interviews → default SQL (transactions, joins, structured schema)
  - Infrastructure/scale design interviews → default NoSQL (scalability, known access patterns)
  - Don't do explicit SQL vs NoSQL comparisons; focus on *how each resolves the specific problem*
  - Know one SQL deeply (MySQL/Postgres) and one NoSQL deeply (Cassandra/DynamoDB)

- **Blob storage facts** (frequently missing from candidates):
  - Amazon S3, Google Cloud Storage, Azure Blob — for large unstructured data (images, video, model checkpoints)
  - Upload → get URL; download via URL; CDN sits in front as cache
  - Durability via replication + erasure coding
  - Cost: ~$0.023/GB vs ~$1.25/GB for traditional DB — 50× cheaper; don't store blobs in SQL
  - Chunked upload: multipart upload API supports resuming interrupted uploads

- **Distributed Lock facts**:
  - ACID transactions use row-level locks (short-term, same DB)
  - Distributed locks span services/DBs: Redis Redlock or Zookeeper
  - Key properties: Lock Expiry (TTL prevents deadlock from crashed holder), Lock Granularity (fine-grained = more concurrency, more complexity), Deadlock conditions (Mutual Exclusion + Hold-and-Wait + No Preemption + Circular Wait)
  - Prefer optimistic locking (version/CAS) over distributed locks when contention is low

- **Cache strategy summary**:
  - Eviction policies: LRU (most common), LFU (frequency-aware), FIFO
  - Write strategies: Write-Through (dual-write, consistent), Write-Around (skip cache on write, cache on read), Write-Back (write cache first, async flush to DB — risk of data loss)
  - Cache invalidation: explicit delete on write (preferred), TTL expiry (simpler, tolerates some staleness)
  - Use case: save aggregated/expensive computation results; reduce DB query count; speed up hot read paths

- **Queue/stream design considerations**:
  - Message ordering: FIFO, priority queues
  - Retry: exponential backoff + dead-letter queue (DLQ) for poison messages
  - Scaling: partition by key → each partition consumed by one consumer group member
  - Backpressure: slow consumers signal producers to slow down
  - Event sourcing / Kafka streams: retain event history for configurable period; replay for recovery or analytics; windowing for hourly/daily aggregates

## Key Questions

**Q: How do you structure the first 5 minutes of a system design interview?**
Answer framework: Clarify functional requirements (what features are in scope, what's out of scope) AND non-functional requirements (scale: DAU/QPS; latency SLO; consistency model; durability). Then identify 2–3 core entities. This framing drives every subsequent decision. Common mistake: jumping to the design before establishing requirements — the interviewer can't evaluate if your design is correct without agreed-upon requirements.

**Q: An interviewer asks "walk me through your high-level design." What's the structure?**
Answer framework: Start by satisfying functional requirements end-to-end (happy path): client → API → data layer → response. Name every component, state what it does, and why you chose it. Use the common pattern that fits (CRUD+cache, async worker, event-driven). Reserve non-functional concerns (fault tolerance, latency optimization, consistency model) for the deep dive phase. Don't pre-optimize — show the clean functional design first, then layer in complexity.

**Q: What belongs in the deep dive phase vs the high-level design phase?**
Answer framework: High-level = functional correctness (does it work?). Deep dive = non-functional quality (is it fast/reliable/scalable enough?). Deep dive topics: (1) bottleneck identification using back-of-envelope numbers; (2) sharding/replication strategy if scale requires it; (3) consistency model choice and rationale; (4) failure handling (retries, circuit breakers, idempotency); (5) specific index or caching strategy for hot paths. A good deep dive is triggered by "what happens at 10× scale?" or "what's the failure mode of component X?"

**Q: How do you choose between SQL and NoSQL for a new system?**
Answer framework: SQL (Postgres/MySQL) for: structured data with complex relationships, strong ACID transactions, ad-hoc query flexibility, joins across entities. NoSQL for: known and fixed access patterns at massive scale, horizontal write scalability as a hard requirement, schema flexibility (document model). Key gotcha: NoSQL forces you to design the schema around queries upfront — changing access patterns later requires re-modeling. If in doubt in a product design interview, start with SQL. In an infrastructure design interview where the write scale is stated to be very high, default to NoSQL (Cassandra/DynamoDB).

**Q: The interviewer asks "how would you make this system handle 10× more traffic?" How do you structure your answer?**
Answer framework: Apply the scaling ladder systematically. (1) Identify the bottleneck — is it reads, writes, or compute? Use the throughput benchmarks to determine which component is saturated. (2) For reads: add read replicas + cache. (3) For writes: add sharding if writes exceed ~10K TPS. (4) For compute: scale-out app servers horizontally (they're stateless). (5) For coordination: introduce a message queue to decouple burst absorption from processing. Justify each step with numbers — don't add distributed complexity without proving the simpler layer is exhausted.

**Q: What monitoring would you add to a production system?**
Answer framework: Three layers. (1) Infrastructure: CPU, memory, disk, network on each node (Datadog, New Relic). (2) Service-level: request latency (P50/P99), error rates, throughput (Prometheus + Grafana). (3) Application-level: active users, key business metrics (booking count, failed payments, active sessions) — Google Analytics, Mixpanel, or custom dashboards. For an on-call engineer, the hierarchy is: business metric alert fires → trace to service-level error spike → trace to infrastructure resource exhaustion. Alert on symptoms (latency/error rate), diagnose with metrics.

**Q: When would you use a distributed lock vs optimistic locking?**
Answer framework: Optimistic locking (version check / CAS) for low-contention scenarios — no lock acquisition overhead, scales well, but requires retry logic on conflict. Distributed lock (Redis Redlock, Zookeeper) for high-contention scenarios where retrying is expensive, or where you need to guarantee exactly-one execution (e.g., cron job that must not run concurrently on multiple nodes). Key considerations for distributed locks: always set a TTL to prevent deadlock if the holder crashes; minimize lock duration; make the critical section idempotent so TTL expiry + re-acquisition is safe.

**Q: How would you design an asynchronous job processing system for video encoding?**
Answer framework: Producer (upload service) → Kafka/SQS queue → worker pool (video encoding jobs). Key design decisions: (1) Kafka for replay capability (re-encode failed jobs without re-uploading); SQS for simplicity (managed, at-least-once). (2) Heartbeat mechanism: worker sends periodic heartbeats to queue; if heartbeat stops, job is re-queued (handles worker crashes). (3) Dead-letter queue for poison messages (jobs that fail repeatedly). (4) Idempotent workers (same job processed twice = same output). (5) Scale workers horizontally by partition count. This is the "async job worker pool" pattern.

## Summary

The Hello Interview framework provides a time-boxed structure that turns a 45-minute system design interview into a predictable sequence: requirements (5 min) → entities (2 min) → API (5 min) → optional data flow (5 min) → high-level design (10–15 min) → deep dive (10 min). The structure matters because interviewers evaluate process as much as output — a candidate who clarifies requirements and justifies every decision signals engineering maturity, even if the design isn't perfect.

The 11 core concepts (scaling, work distribution, data distribution, CAP, locking, indexing, DB indexing, specialized indexes, communication protocols, security, monitoring) form the vocabulary of every system design interview answer. Each concept has a standard pattern: Consistent Hashing for scaling, circuit breaker for fault tolerance, geospatial indexes for proximity, Kafka for async decoupling. Internalizing these patterns lets you navigate any novel prompt by pattern-matching: "this is a proximity service — geospatial index + regional sharding"; "this is a fan-out-heavy write — push vs pull model + async queue."

For an AI Infra Manager candidate, this framework has direct practical value: you will be asked to design ML training infrastructure, model serving pipelines, and data processing systems — not just web CRUD apps. The same patterns apply: training job scheduling is async worker pool with durable job processing; model serving is a two-stage architecture (retrieval → scoring); feature stores are distributed caches with consistency tradeoffs. The Hello Interview framework is language that translates between standard web systems knowledge and AI infrastructure design.

## Key Terms

**Interview Structure**
- `functional requirements` · `non-functional requirements` · `core entities` · `API design` · `high-level design` · `deep dive`

**Non-Functional Checklist**
- `CAP` · `latency SLO` · `throughput/scalability` · `durability (RPO)` · `fault tolerance` · `security` · `compliance`

**Core Concepts**
- `consistent hashing` · `work distribution` · `data distribution` · `locking` · `indexing` · `CAP` · `communication protocols` · `monitoring`

**Common Patterns**
- `CRUD + cache` · `async worker pool` · `two-stage architecture` · `event-driven` · `durable job processing` · `proximity service`

**Technology Defaults**
- `Postgres (SQL)` · `Cassandra/DynamoDB (NoSQL)` · `Redis (cache + lock)` · `Kafka/SQS (queue)` · `S3/GCS (blob)` · `Elasticsearch (full-text)` · `REST (public API)` · `gRPC (internal)`

## Raw Material
- [[raw_material/tech/system-design/hello-interview/hello-interview-framework.md]]
