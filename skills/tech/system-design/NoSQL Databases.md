---
title: NoSQL Databases
category: tech/system-design
tags: [nosql, cassandra, dynamodb, wide-column, partition-key, clustering-key, hot-key, salting, cap-theorem, acid]
status: draft
priority: medium
last_updated: 2026-04-06
created_from_jd:
---

# NoSQL Databases

## Knowledge Map
- Prerequisites（前置知识）：[[Distributed Systems]], [[Database Indexing]], [[Cache and Consistency]]
- Related Topics（延伸话题）：[[Redis]], [[Sharding and Scalability]], [[Message Queue]]
- Management（管理关联）：[[Technical Roadmap]]

## Core Concepts

**Why NoSQL Exists（为什么需要 NoSQL）**
- Two bottlenecks of relational databases: ① data model misfit (variable fields, document, graph, KV structures); ② scale bottleneck (millions of writes per second, PB-level data — hard to scale horizontally)
- The essential difference between NoSQL and "manually sharded relational DB": NoSQL **sacrifices ACID** in exchange for automatic sharding and scalability; relational retains ACID but cross-shard transactions are extremely hard
- Most NoSQL systems choose AP (availability + partition tolerance); relational databases choose CP

**Cassandra: Wide Column Store（宽列模型）**
- Data hierarchy: Keyspace (≈ Database) → Table → Row → Column (each row can have different columns, schema-free)
- **Partition Key**: determines which node stores the data (routing) （路由）; **Clustering Key**: determines the sort order within a partition （节点内排序）
- Query in two steps: use Partition Key to route to the node, then use Clustering Key to search sorted data within the node
- Why write performance is extremely high: **WAL (Write-Ahead Log)** = write operations are appended sequentially to a log first, no random disk writes — naturally suited for high write volumes

**Cassandra Table Design in Practice — Chat System（设计实战：聊天系统）**
- Requirement: query chat history between users A and B, sorted by time descending
- Partition Key: `min(userA_id, userB_id) + "_" + max(userA_id, userB_id)` (A→B and B→A queries resolve to the same key)
- Clustering Key: `created_at DESC` (data within the Partition is sorted in descending time order — no additional sorting needed at query time)
- **Hot Key problem**: if user A has chat records with 10,000 people, all conversations land on the same Partition → **Salting**: append a numbered suffix to the key (`userA_001`/`userA_002`), splitting data across multiple nodes
- After salting, querying all conversations requires scanning multiple Partitions → cache the conversation list in Redis + paginated loading

**DynamoDB vs Cassandra**
| Dimension | Cassandra | DynamoDB |
|-----------|-----------|----------|
| Architecture | Decentralized, all nodes equal （去中心化）| AWS managed, zero ops overhead |
| Cost | Predictable, more economical at large scale | Usage-based billing, convenient for small teams but can be expensive at high traffic |
| Risk | Self-managed, full control | Vendor lock-in |

- DynamoDB capacity modes: **Provisioned** (pre-set RCU/WCU, cheaper, suited for predictable traffic) vs **On-Demand** (auto-scales, pay per use, suited for sporadic peaks)

**NoSQL vs Relational — Decision Framework（选型决策框架）**
- Choose relational: money/inventory involved (ACID non-negotiable), complex queries / multi-field indexes needed, complex data relationships requiring Joins
- Choose NoSQL: data volume requires automatic sharding, extremely high write volume (WAL sequential write), frequently changing fields (schema-free), simple fixed query patterns (direct lookup by Partition Key)

## Key Questions

**Q: What is the real difference between NoSQL and "manually sharded relational databases"?**
Answer framework: Manual sharding still retains ACID, but cross-shard transactions are extremely hard (distributed transaction complexity is high); NoSQL drops ACID by design in exchange for automatic sharding, providing eventual consistency; choice depends on business: money → relational, massive writes → NoSQL.
> 中文提示：手动分库分表保 ACID 但跨分片事务极难；NoSQL 牺牲 ACID 换分片自动化；涉及钱用关系型

**Q: What are the roles of Cassandra's Partition Key and Clustering Key?**
Answer framework: Partition Key determines routing (which node stores the data); Clustering Key determines within-node ordering (supports efficient range queries); design Partition Key to avoid Hot Keys (even distribution); design Clustering Key to match the query's sort requirement, avoiding application-level re-sorting.
> 中文提示：Partition Key = 路由（在哪个节点）；Clustering Key = 节点内排序（支持范围查询）

**Q: Design a Cassandra table that supports querying "chat history between two users in reverse chronological order."**
Answer framework: Partition Key = min/max combination (ensures A→B and B→A resolve to the same Partition); Clustering Key = created_at DESC; if a user has a Hot Key (chats with many people), apply Salting (add suffix to split across nodes); after Salting, cache the conversation list in Redis to reduce multi-Partition scans.
> 中文提示：Partition Key 用 min/max 组合保证双向查同一 Partition；Hot Key 用 Salting 分散；Salting 后用 Redis 缓存减少读放大

**Q: How do you choose between DynamoDB's Provisioned and On-Demand modes?**
Answer framework: Provisioned = pre-set RCU/WCU, cheaper, suited for **predictable** traffic (fixed evening peaks each day); On-Demand = pay per actual usage, suited for **unpredictable** sporadic peaks (a few promotions per year); decision criterion: ratio of peak to annual baseline — low ratio → On-Demand is cheaper, high ratio → Provisioned is cheaper.
> 中文提示：可预测流量用 Provisioned（便宜）；不可预测偶发峰值用 On-Demand；峰值占比低 → On-Demand 省

**Q: How do you decide whether to use NoSQL or a relational database?**
Answer framework: Proactively state concrete criteria (not "it depends"): data volume exceeds X billion / write rate exceeds Y/s / field structure changes frequently → NoSQL; involves transactions / complex queries / strong consistency → relational; real systems often mix both (Ticketmaster: orders in relational, venue info in NoSQL; TikTok: video metadata in NoSQL, payments in relational).
> 中文提示：给出具体标准而非"看情况"；实际系统通常混用，举具体例子体现工程判断

## Summary

NoSQL databases' core value is the design trade-off of "sacrificing ACID for horizontal scalability," addressing the bottlenecks of relational databases at massive scale. Cassandra's wide column model and WAL write mechanism make it excel in write-intensive scenarios (chat, logging, time-series data); DynamoDB uses fully managed infrastructure to lower the operational barrier, suited for teams that don't want to manage their own infrastructure.

Partition Key design is the most important decision in NoSQL schema design: the right choice distributes data evenly and queries efficiently; the wrong choice creates Hot Keys with a single node overloaded. Salting is the general remedy for Hot Keys, but the cost is that queries must scan multiple Partitions — typically mitigated with caching (Redis) to compensate for read amplification.

From an AI Infra perspective, NoSQL commonly appears in: ① model experiment logs (schema changes frequently, write-intensive); ② the underlying storage for Feature Stores (time-series + large-scale writes); ③ training job status tracking (direct lookup by job_id, simple fixed query patterns). Cassandra's WAL sequential write and AI training checkpoint writes have similar performance requirements — a knowledge transfer point between the two domains.

> 面试重点：NoSQL vs 关系型的取舍（ACID vs 扩展性）→ Partition Key + Clustering Key 设计 → Hot Key + Salting → DynamoDB 容量模式选择

## Raw Material
- [[raw_material/tech/system-design/sd-nosql]]
