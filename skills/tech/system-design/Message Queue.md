---
title: Message Queue
category: tech/system-design
tags: [message-queue, kafka, async, idempotency, at-least-once, exactly-once, partition, replication, isr, pub-sub]
status: draft
priority: high
last_updated: 2026-04-06
created_from_jd:
---

# Message Queue

## Knowledge Map
- Prerequisites（前置知识）：[[Distributed Systems]], [[Cache and Consistency]]
- Related Topics（延伸话题）：[[Kafka]], [[NoSQL Databases]], [[Sharding and Scalability]]
- Management（管理关联）：[[Technical Roadmap]]

## Core Concepts

**Why Message Queues Exist（异步解耦的价值）**
- Problems with synchronous calls: ① any step failure causes the whole flow to fail (email send failure causing order failure is unreasonable); ② serial execution means the user waits for the sum of all step durations
- Message queues solve this with: **async decoupling** (return success on order completion, process the rest asynchronously in the queue) + **parallel processing** (multiple services consume concurrently without blocking each other)

**Message Reliability: ACK Mechanism（ACK 确认机制）**
- Consumer sends an **ACK** after processing; if no ACK is received, the message remains in the queue and is redelivered when the consumer recovers
- Trade-off: **possible duplicate consumption** — idempotency is required (this is the core challenge in designing reliable messaging systems)

**Implementing Idempotency（幂等性实现）**
- **Optimistic locking + version number**: check version number on update; discard if mismatched (suited for handling message redelivery)
- **Deduplication table**: each message has a unique `request_id`; check the table before processing; discard if already processed
- Key: the check-if-already-processed and mark-as-processed operations **must be in the same database transaction** — otherwise two concurrent Consumers can both pass the check and double-process the same message （必须原子操作）

**Three Delivery Guarantees（三种投递保证）**
- **At-most-once**: messages may be lost, no duplicates; suited for log reporting, status updates where loss is acceptable
- **At-least-once**: no message loss, possible duplicates; suited for core operations (deduct inventory, update points) paired with idempotency
- **Exactly-once**: no loss, no duplicates — extremely high implementation cost; industry uses **At-least-once + idempotency** as a substitute
- Why exactly-once is hard: ① producer retries without duplicates; ② Broker durability without loss; ③ consumer offset commit atomic with business processing — any single point breaking this defeats it

**Kafka High Availability — Partition / Replication / ISR / Quorum（高可用机制）**
- **Partition** （分区）: the horizontal scaling unit; messages within the same Topic are spread across multiple Partitions for parallel processing
- **Replication** （副本）: each Partition has a Leader + multiple Followers; on Leader failure, a Follower takes over
- **ISR (In-Sync Replicas)** （同步副本集合）: only messages acknowledged by all ISR members are considered committed; on Leader failure, only ISR members are eligible for Leader election — guarantees no data loss for committed messages
- **Quorum mechanism**: n/2+1 replicas confirm = committed; no need to wait for the slowest node; slow nodes are automatically removed from ISR
- 5 replicas, Quorum=3: tolerates 2 node failures; reducing replicas from 5→3 trades fault tolerance for write speed

**Peak Traffic Handling — Double 11 Scenario（峰值处理）**
- Monitor queue depth; trigger alerts and auto-scaling (more Consumer instances + more Partitions) when thresholds are exceeded
- Tiered degradation by Topic priority: core Topics (inventory deduction, points) maintain at-least-once, no drop; non-core Topics (email, notification) can be degraded
- **Key principle**: when degrading, explicitly state "which to drop, which to protect" — don't vaguely say "drop messages"

## Key Questions

**Q: What is the core value of a message queue? When should you introduce one?**
Answer framework: Async decoupling (downstream failure doesn't affect main flow) + peak buffering (absorbs burst writes) + parallel processing (multiple Consumers consume concurrently); when to introduce: synchronous calls have obvious serial waiting, multiple downstream systems need the same data, or there are clear traffic peaks to buffer.
> 中文提示：三大价值：异步解耦 + 流量削峰 + 并行处理；引入时机：同步串行等待明显、多下游、有峰值

**Q: A consumer crashes mid-processing — what happens to the message? How do you prevent double processing?**
Answer framework: ACK mechanism (no ACK → message stays in queue for redelivery); this inevitably creates duplicate consumption risk; solution: idempotency — dedup table (request_id + transaction) or optimistic locking (version number); atomicity is critical — check + mark must be atomic, or two concurrent Consumers can both pass the check.
> 中文提示：ACK 机制导致 at-least-once；幂等方案：去重表（查+更新必须同一事务）或乐观锁

**Q: What are the use cases for each delivery guarantee? How does industry achieve Exactly-once semantics?**
Answer framework: At-most-once for losable scenarios (logs, status updates); At-least-once + idempotency is the industry standard (covers 95% of cases); Exactly-once is too costly (producer dedup + Broker durability + consumer offset atomic with business — all three must hold), so industry rarely implements it directly.
> 中文提示：工业界标准是 At-least-once + 幂等；Exactly-once 三点全保证代价太高，基本用组合方案替代

**Q: How does Kafka guarantee high availability? What is ISR?**
Answer framework: Partition + Replication (Leader + Follower); ISR = set of replicas that are fully synced; only ISR members confirm before a message is committed; on Leader failure, only ISR is eligible for election — guarantees no data loss for committed messages; Quorum mechanism avoids waiting for the slowest node (same thinking as Raft/etcd Quorum).
> 中文提示：ISR = 已同步副本集合；只有 ISR 内确认才算 committed；Leader 崩溃只从 ISR 选，保证不丢已提交消息

**Q: Kafka consumer lag is growing during peak traffic (Double 11). How do you handle it?**
Answer framework: Three-layer response: ① monitoring alerts (queue depth threshold); ② scale out (add Consumers + Partitions); ③ tiered degradation by Topic (core at-least-once, non-core degradable); proactively state "which to drop, which to protect" — don't vaguely say "degrade."
> 中文提示：三层：监控 → 扩容 → 分级降级；必须说清楚"丢哪些、保哪些"，不要笼统说降级

## Summary

A message queue is the core decoupling component of distributed systems — its essence is transforming synchronous request chains into asynchronous event streams. ACK + idempotency is the foundation of the entire reliable messaging system: ACK ensures "no loss" (at-least-once), idempotency ensures "duplication is harmless" — combining the two achieves truly usable message processing. Industry uses this combination to replace the nearly impossible-to-perfectly-implement Exactly-once.

Kafka's ISR mechanism is the key design that balances "high throughput vs data consistency": don't wait for all replicas (avoids slow nodes dragging down performance), but don't allow non-ISR replicas to become Leaders (guarantees data completeness). Quorum parameter tuning (replica count + min.insync.replicas) lets the system calibrate between reliability and performance based on business requirements.

From an AI Infra perspective, message queues are critically important in: ① training job scheduling (job submission decoupled from actual execution); ② async notifications of model evaluation results; ③ buffering between stages in data preprocessing pipelines (data ingestion / preprocessing / training run at different rates). The ISR/Quorum trade-off thinking also directly maps to the Quorum fault-tolerance design in AI training AllReduce.

> 面试重点：ACK 机制 → 幂等性（去重表/乐观锁）→ 三种投递保证（工业界用 at-least-once + 幂等）→ Kafka ISR 高可用 → 峰值分级降级（说清楚丢哪些保哪些）

## Raw Material
- [[raw_material/tech/system-design/sd-messagequeue]]
