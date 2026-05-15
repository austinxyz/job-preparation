---
title: DynamoDB
category: tech/system-design
tags: [dynamodb, aws, nosql, key-value, distributed-systems, database, caching]
status: in-progress
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# DynamoDB

## Knowledge Map
- 前置知识：AWS fundamentals, CAP theorem, consistent hashing, B-trees
- 延伸话题：[[Redis]] (caching alternative to DAX), [[Cache and Consistency]], [[Distributed Systems]], [[Sharding and Scalability]], [[AWS Infrastructure]]
- 管理关联：cost modeling (RCU/WCU), vendor lock-in tradeoffs, data modeling discipline

## Core Concepts

- **Fully-managed serverless NoSQL**: AWS handles hardware provisioning, scaling, patching, and replication — no ops burden; schema-less so items in the same table can have different attributes
- **Data model**: Tables → Items (up to 400KB each) → Attributes (scalar, set, nested); no schema enforcement; primary key is mandatory
- **Partition Key + Sort Key**: Partition Key hashed to determine physical node; Sort Key (optional) enables range queries within a partition via B-tree; choose high-cardinality Partition Key to avoid hot partitions
- **Under the hood**: hash-based partitioning (centralized partition map, not peer-to-peer ring) + B-tree per partition for sort key; two-tier design enables horizontal scalability + efficient range queries
- **Secondary Indexes — GSI vs LSI**:
  - GSI: different partition key, separate physical partitions, eventually consistent only, can be added/removed anytime, up to 20 per table
  - LSI: same partition key, co-located with base table, supports strong consistency, must be defined at table creation, up to 5 per table
- **Query vs Scan**: Query = efficient key-based lookup; Scan = reads every item (expensive, avoid at scale); ProjectionExpression reduces network bandwidth but NOT RCU cost
- **Consistency model (per-request, not per-table)**:
  - Eventually consistent (default): any replica, 0.5 RCU per 4KB, lower latency
  - Strongly consistent (`ConsistentRead=true`): routes to leader node, 1 RCU per 4KB, guaranteed latest data; not supported on GSIs
- **ACID Transactions**: `TransactWriteItems` / `TransactGetItems` support serializable isolation across up to 100 items spanning multiple tables
- **Replication**: 3 replicas per partition across 3 AZs (leader + 2 followers); Multi-Paxos consensus; write acknowledged at quorum (2/3); Global Tables for cross-region replication
- **Capacity models**:
  - On-demand: pay per request, best for unpredictable workloads
  - Provisioned: specify RCU/WCU, billed hourly, cost-effective for predictable load
  - Per partition limits: 3,000 RCU + 1,000 WCU (useful for back-of-envelope calculations)
- **DAX (DynamoDB Accelerator)**: purpose-built in-memory cache; microsecond reads; read-through + write-through; does NOT cache strongly consistent reads; stale if DynamoDB written directly bypassing DAX; item cache + query cache always active
- **DynamoDB Streams**: Change Data Capture (CDC); records insert/update/delete events in real-time; triggers Lambda, syncs Elasticsearch, feeds Kinesis for analytics
- **When NOT to use**: complex joins/aggregations → use Aurora/PostgreSQL; extremely high write volume where cost is prohibitive; interviewer requires vendor-neutral solution

**Hello Interview: Key Interview Framing（面试重点框架）**
- **CAP position**: primarily AP (availability + partition tolerance) by default; strongly consistent reads (`ConsistentRead=true`) provide CP semantics for specific operations — not the whole table
- **Pricing model decision**: on-demand for unpredictable/spiky workloads; provisioned capacity for predictable workloads with cost sensitivity (billed hourly, requires capacity planning)
- **Transactions (often forgotten in interviews)**: DynamoDB supports full ACID transactions — `TransactWriteItems` / `TransactGetItems` for atomic multi-item operations across tables; mention this proactively if the problem involves booking, inventory, or financial updates
- **DAX shortcut**: built-in in-memory cache with no application code changes needed; always uses both item cache (GetItem) and query cache (Query/Scan results); does NOT cache strongly consistent reads

## Key Questions

**Q: How does DynamoDB partition and store data internally?**
Answer framework: Partition Key is hashed via centralized partition map (not consistent hash ring) to find storage node; within partition, Sort Key items organized in B-tree enabling range queries; write goes to leader, replicated to 2 followers via Multi-Paxos, acknowledged at quorum; read can go to any replica (eventual) or leader only (strong).

**Q: When would you choose a GSI vs LSI, and what are the trade-offs?**
Answer framework: GSI when you need to query by a different partition key (cross-partition queries); LSI when you need additional sort options within the same partition. Key trade-offs: GSI = eventually consistent only, separate throughput, flexible timing; LSI = strongly consistent supported, shares base table throughput, must define at creation, 10GB per partition key limit.

**Q: A DynamoDB table has hot partition issues — some writes are throttled. How do you diagnose and fix?**
Answer framework: Diagnose via CloudWatch ConsumedWriteCapacityUnits by partition + ThrottledRequests metrics. Fix: increase Partition Key cardinality (use UUID/job_id instead of low-cardinality status fields); add random suffix for write-heavy keys (key sharding); enable DAX to absorb read hot spots; consider on-demand capacity to auto-absorb spikes.

**Q: Your system needs to query training jobs by status (e.g., "all running jobs") — how do you model this in DynamoDB?**
Answer framework: "status" as partition key is a hot partition anti-pattern (all running jobs on one shard). Instead: use `job_id` (UUID) as partition key; add GSI with `status` as partition key and `created_at` as sort key for status-based queries; accept GSI's eventual consistency for this read path; or use write sharding on status key.

**Q: Compare DynamoDB eventual vs strong consistency — when would you choose each?**
Answer framework: Default to eventual consistency for read-heavy, latency-sensitive paths (feature lookups, metadata reads); use `ConsistentRead=true` for correctness-critical reads (booking confirmation, inventory check). Strong consistency costs 2× RCU and routes to leader — don't use by default. Note: strong consistency not available on GSIs.

**Q: How would you use DynamoDB Streams in an ML pipeline?**
Answer framework: Streams emit CDC events for every table change; use cases: trigger Lambda to invalidate DAX cache on model artifact update; sync job metadata to Elasticsearch for search; fan out to Kinesis → Firehose → S3 for analytics. Key caveat: Kinesis Data Streams needed as intermediary before Firehose (Firehose can't read DynamoDB Streams directly).

**Q: Back-of-envelope: you need to store 10M writes/sec in DynamoDB. Is it feasible and what's the cost?**
Answer framework: Each partition handles 1,000 WCU (1KB writes). 10M WPS → ~10,000 partitions. DynamoDB auto-shards, so technically feasible. Cost: 10M WCU × $0.00065/WCU-hour × 24hrs ≈ $156K/day — likely prohibitive; at this scale consider batch writes, stream aggregation (Kinesis), or alternative store.

## Summary

DynamoDB is AWS's fully-managed, serverless NoSQL database offering single-digit millisecond latency at any scale. It uses hash-based partitioning to distribute data across nodes and B-trees within each partition for sort key range queries. The schema-less design and automatic scaling make it operationally simple — there are no servers to manage, and capacity adjusts automatically in on-demand mode. In AI Infra contexts, DynamoDB is the go-to choice for metadata stores: artifact registries (job_id → S3 path), pipeline job status tracking, and feature store indexes where access patterns are key-based and latency requirements are strict.

Data modeling is DynamoDB's most critical discipline. The Partition Key choice determines data distribution and query efficiency — hot partitions (from low-cardinality keys like "status") are the most common performance failure. Secondary indexes (GSI for cross-partition queries, LSI for within-partition sort variations) extend query flexibility, but GSIs only support eventual consistency and LSIs must be defined at table creation. For caching, DAX provides microsecond reads as a drop-in layer without introducing Redis/Memcached, though it has nuances around stale data when DynamoDB is written directly. DynamoDB Streams enables event-driven architectures and CDC patterns — connecting to Lambda, Elasticsearch, or Kinesis for real-time processing.

DynamoDB's main limitations are complex queries (no joins or ad-hoc aggregations — use Aurora/PostgreSQL instead), high-volume write cost at extreme scale, and AWS vendor lock-in. In system design interviews, it's a strong default choice for most persistence needs given its scalability, durability, transactions support, and ease of use — but the answer should always be grounded in access pattern analysis: show you chose the Partition Key to match the dominant query, and that you've thought about hot partition risk.

From the Hello Interview perspective, the key interview differentiators for DynamoDB are: (1) it is primarily AP but supports per-operation CP via strongly consistent reads — a nuance interviewers test; (2) ACID transactions are available and often forgotten by candidates — proactively mention `TransactWriteItems` for booking/inventory scenarios; (3) DAX as zero-code-change caching layer; (4) pricing model choice (on-demand vs provisioned) maps directly to workload predictability. Use case sweet spot: serverless AWS-native apps with key-value access patterns, unpredictable traffic, and sub-millisecond latency requirements.

## Key Terms

**Core Data Model**
- `Partition Key` · `Sort Key` · `Composite Primary Key` · `Item` · `Attribute` · `Table`

**Indexing**
- `GSI` · `LSI` · `Global Secondary Index` · `Local Secondary Index` · `ProjectionExpression`

**Consistency & Transactions**
- `ConsistentRead` · `Eventual Consistency` · `Strong Consistency` · `TransactWriteItems` · `TransactGetItems` · `Multi-Paxos` · `quorum`

**Capacity & Performance**
- `RCU` · `WCU` · `On-demand capacity` · `Provisioned capacity` · `hot partition` · `key sharding` · `write sharding`

**Advanced Features**
- `DAX` · `DynamoDB Accelerator` · `DynamoDB Streams` · `CDC` · `Global Tables` · `PartiQL`

**Access Patterns**
- `Query` · `Scan` · `GetItem` · `BatchGetItem` · `KeyConditionExpression`

**Anti-patterns**
- `hot partition` · `low-cardinality partition key` · `sequential prefix` · `unbounded scan`

## Raw Material
- [[raw_material/tech/system-design/DynamoDB - Hello Interview]]
- [[raw_material/tech/system-design/hello-interview/tech-dynamodb.md]]
