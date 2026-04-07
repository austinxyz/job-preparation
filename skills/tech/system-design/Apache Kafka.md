---
title: Apache Kafka
category: tech/system-design
tags: [kafka, distributed-systems, message-queue, event-streaming, partitioning, replication, isr, consumer-group, offset, hot-partition, dlq, throughput]
status: draft
priority: high
last_updated: 2026-04-06
created_from_jd:
---

# Apache Kafka

## Knowledge Map
- Prerequisites（前置知识）：[[Message Queue]], [[Distributed Systems]], [[Sharding and Scalability]]
- Related Topics（延伸话题）：[[Stream Processing]], [[NoSQL Databases]], [[Cache and Consistency]]
- Management（管理关联）：[[Technical Roadmap]]

## Core Concepts

**What Kafka Is（核心定位）**
- Open-source distributed **event streaming platform** — can function as a message queue or a stream processing system
- Used by 80% of Fortune 100; designed for high throughput, low latency, and durability
- Core philosophy: **distributed commit log** — append-only, immutable, position tracked by offset
- 核心哲学：不可变的顺序日志，靠 offset 定位，而非消费后删除

**Core Architecture Terms（基础架构术语）**
- **Broker**: A server node in the Kafka cluster; stores data and serves clients. Single broker capacity ≈ 1TB / 1M messages per second （单节点估算上限）
- **Topic**: Logical grouping of messages by category (e.g., `soccer-events`, `basketball-events`) （业务维度的逻辑分组）
- **Partition**: Physical shard of a topic; an append-only log file; the unit of horizontal scaling; messages within a partition are ordered （水平扩展的核心单位，同 Partition 内有序）
- **Producer**: Process that writes messages to a topic; message fields: `value`, `key`, `timestamp`, `headers`
- **Consumer**: Process that pulls messages from a topic; uses a **pull model** (consumers poll brokers) to avoid overwhelming slow consumers （主动拉取，避免压垮慢消费者）
- **Consumer Group**: A group of consumers where each partition is assigned to exactly **one** consumer in the group (default at-least-once — duplicates possible) （每个 Partition 只分配给组内一个 Consumer）

**Partition Key — The Most Important Design Decision（Partition Key 是最核心的设计决策）**
- Routing formula: `partition = hash(key) % num_partitions` (default: murmur2 hash)
- Same key → same partition → **ordering guaranteed within that key**
- No key: modern clients use a sticky partitioner (batch to one partition, then rotate for roughly even distribution)
- **Key selection determines everything**: bad key → hot partition → performance bottleneck
- 面试必说：Key 选择决定顺序保证和负载均衡，要主动讨论 hot partition 风险

**Offset and Consumer Progress（Offset 与消费进度）**
- Each message in a partition has a unique sequential **offset** (timestamps do NOT determine order)
- Consumers commit offsets back to Kafka to record progress; on restart, resume from last committed offset
- **Default at-least-once delivery**: if consumer crashes after processing but before committing → message reprocessed → business logic must be idempotent（需业务侧幂等）
- Exactly-once requires: idempotent producer + transactional API — high overhead, rarely used directly

**Replication and ISR（副本 + ISR 高可用）**
- Each partition has 1 Leader + N Followers (typical replication factor = 3)
- Leader handles all writes (Kafka 2.4+ allows follower reads to reduce latency)
- **ISR (In-Sync Replicas)**: the set of replicas that are fully caught up with the leader
- `acks=all`: message is only acknowledged when **all ISR members** have written it → strongest durability guarantee
- On leader failure, new leader is elected **only from ISR** → no data loss for committed messages
- Slow replicas are automatically removed from ISR; Kafka trades strict majority quorum for higher throughput
- Controller (a role within the broker cluster) manages leader election and partition metadata

**Message Queue Mode vs Stream Mode（两种使用模式的区别）**
| | Message Queue Mode | Stream Mode |
|---|---|---|
| Consumption | Each message processed by one consumer group, then "done" | Log retained; multiple consumer groups read independently |
| Replay | No (effectively consumed) | Yes — consumers can replay from any offset |
| Use case | Async tasks, ordered processing, service decoupling | Real-time aggregation, pub/sub broadcast, event replay |

**Hot Partition Strategies（热分区应对策略）**
1. **No key (default partitioning)**: Even distribution, but ordering within related messages is lost — use when ordering doesn't matter 牺牲顺序换均匀分布
2. **Random salting**: Append a random suffix to the key (e.g., `adId + random(0,N)`) to spread traffic; consumer must re-aggregate 消费侧需要合并聚合
3. **Compound key**: Use `adId + region` or `adId + userSegment` — distributes load while preserving partial ordering
4. **Back pressure**: Producer monitors partition lag and slows down when it's too high 限速生产者

**Scalability（扩展性）**
- Horizontal scaling: add Brokers — but **must also increase partition count** to benefit from new brokers (under-partitioned topics can't use new brokers) 分区数不够，新 Broker 利用不上
- Max consumer parallelism in a group = number of partitions (extra consumers beyond partition count sit idle)
- Anti-pattern: don't store large blobs in Kafka — store in S3, put the S3 pointer in the Kafka message 大文件存 S3，Kafka 只存指针

**Consumer Failure and Retry（Consumer 失败与重试）**
- **Rebalancing**: when a consumer leaves a group, Kafka redistributes its partitions to remaining consumers
- **Offset commit timing matters**: don't commit until business processing is confirmed complete (e.g., in Web Crawler: store HTML in blob storage first, then commit offset) — otherwise data loss on crash 处理完成再 commit，否则数据丢失
- Kafka does **not** natively support consumer retries — must implement: retry topic → DLQ (Dead Letter Queue) pattern
- AWS SQS has built-in retry and DLQ — prefer SQS when you don't want to manage retry logic yourself

**Performance Optimizations（性能优化）**
- **Batch sends**: include multiple messages in a single `send()` call — reduces network round trips 减少网络开销
- **Compression**: GZIP / Snappy / LZ4 — significantly reduces message size for high-throughput scenarios
- **Partition key uniformity**: the single biggest lever — even key distribution maximizes parallelism 最大影响因素

**Retention Policy（消息保留策略）**
- Controlled by `retention.ms` (default: 7 days) and `retention.bytes`
- Streaming use cases may configure longer retention to support replay; watch storage costs

## Key Questions

**Q: What is the difference between a Topic and a Partition? Why is the Partition count so important for scaling?**
Answer framework: Topic is a logical grouping (business layer); Partition is a physical shard (storage layer) — an append-only log. Partition count sets the ceiling for consumer parallelism; adding brokers without adding partitions gains nothing. The partition key determines message routing and ordering guarantees.
> 中文提示：Topic = 业务分类，Partition = 物理分片；分区数 = 消费并行上限；增加 Broker 不增加 Partition 则新 Broker 空闲

**Q: How should you choose a partition key? What happens if you choose a bad one?**
Answer framework: Goal is dual — keep related messages (that need ordering) on the same partition, AND distribute load evenly. Bad example: using `ad_id` as key — a viral ad floods one partition. Mitigations: salting, compound key, or keyless distribution + consumer-side aggregation. In interviews, proactively mention hot partition risk and remediation.
> 中文提示：Key 选择要兼顾"顺序保证"和"负载均衡"；面试要主动提 hot partition 风险和对策

**Q: How does Kafka guarantee message durability? What is the relationship between `acks=all` and ISR?**
Answer framework: Write path: Producer → Leader → ISR followers. `acks=all` requires acknowledgment from all ISR members before confirming to producer. ISR is dynamic — slow replicas are evicted to protect throughput. On leader failure, new leader only elected from ISR → committed data is never lost. Trade-off: `acks=all` increases write latency.
> 中文提示：ISR 是动态集合，慢节点自动移出；`acks=all` 保强持久性，代价是写延迟

**Q: What happens to message processing state when a consumer crashes? Can messages be processed twice?**
Answer framework: Consumer resumes from last committed offset on restart. Default at-least-once: crash after processing but before offset commit → reprocessed. Solution: business logic must be idempotent (deduplication table with `request_id` + transaction, or optimistic locking with version number). Key design tip: commit offset only after confirming business processing is done.
> 中文提示：默认 at-least-once；crash 后重新消费；需业务侧幂等（去重表 / 乐观锁）

**Q: When would you choose Kafka over SQS, or vice versa?**
Answer framework: Choose Kafka when: high throughput (millions/sec), need message replay, multiple independent consumer groups must read the same data, or streaming use case. Choose SQS when: team doesn't want Kafka ops overhead, need built-in retry + DLQ without custom implementation, or already in AWS ecosystem with moderate throughput needs.
> 中文提示：Kafka = 高吞吐/回放/多消费者；SQS = 托管/内置重试/无需运维

**Q: Your Kafka consumer lag is growing during peak traffic (e.g., Double 11). How do you handle it?**
Answer framework: Three-layer response: ① Monitoring + alerting (partition lag thresholds) ② Scale out (add consumer instances + increase partition count) ③ Tiered degradation (protect critical topics at at-least-once; allow non-critical topics like notifications to drop or delay). Interview tip: explicitly say "drop which topics, protect which topics" — don't just say "degrade."
> 中文提示：三层：监控预警 → 扩容 → 分级降级；必须说清楚"丢哪些、保哪些"

**Q: How does Kafka's ISR consistency model compare to Raft/Paxos?**
Answer framework: Both use quorum-style thinking. Difference: Kafka's ISR is a dynamic set (slow replicas evicted), not a fixed majority. This means Kafka doesn't require a strict majority quorum — it only requires all current ISR members to confirm. Kafka trades some distributed consistency guarantees for significantly higher throughput, making it suitable for "high availability, eventually consistent" messaging use cases.
> 中文提示：ISR 动态集合 ≠ 固定多数派；Kafka 用更灵活的 Quorum 换取更高吞吐

## Summary

Apache Kafka is an event streaming platform built around a **distributed commit log**: an ordered, immutable, append-only sequence of messages partitioned across brokers. Unlike traditional message queues that delete messages after consumption, Kafka retains messages according to a retention policy — enabling multiple independent consumer groups to replay or process the same data stream. This dual-mode capability (queue + stream) makes Kafka the standard data bus in large-scale distributed systems.

Kafka's scalability and reliability both hinge on **Partitions**. The number of partitions sets the ceiling for consumer parallelism; the partition key determines message routing (same key → same partition → ordering guaranteed) and load distribution (bad key → hot partition → bottleneck). The ISR + `acks=all` combination provides strong durability: only committed data is used in leader election, ensuring no data loss. Offset commit timing is equally critical — commit only after confirming business processing is complete, and pair at-least-once delivery with idempotent business logic.

From an AI Infra perspective, Kafka excels in: training job scheduling (decouple job submission from execution), feature pipeline buffering (data ingestion / preprocessing / training run at different rates), and model evaluation result broadcasting (multiple downstream services consume the same evaluation event). In system design interviews, lead with partition strategy + hot partition handling, then cover at-least-once + idempotency, and close with Kafka vs SQS trade-off when relevant.

> 面试重点顺序：① Partition 策略（Key 选择 + hot partition 应对）→ ② at-least-once + 幂等 → ③ ISR 高可用 → ④ Kafka vs SQS 选型

## Raw Material
- [[raw_material/tech/system-design/kafka]]
