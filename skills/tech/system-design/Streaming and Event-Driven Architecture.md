---
title: Streaming and Event-Driven Architecture
category: tech/system-design
tags: [kafka, streaming, event-driven, pub-sub, kinesis, flink, real-time, message-queue, backpressure]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: "[[positions/Manager 3, Service Builder Platform - Intuit]]"
---

# Streaming and Event-Driven Architecture

## Knowledge Map
- 前置知识：Message Queue, Distributed Systems, Kafka basics
- 延伸话题：Kafka internals (partitions, consumer groups, offsets, compaction), Flink/Spark Streaming for stateful stream processing, backpressure mechanisms, exactly-once semantics, event sourcing vs CQRS, Kinesis vs Kafka vs Pub/Sub comparison, stream-table duality
- 管理关联：streaming platform as internal service (SLO for latency/throughput), capacity planning for high-throughput workloads, streaming vs batch trade-off decisions

## Core Concepts

**Apache Flink — Distributed Stream Processing**

- **Core purpose**: distributed stream processing framework that handles unbounded data streams with stateful computation, windowing, and exactly-once semantics; contrasts with batch processing (bounded datasets) by operating on continuous, real-time data flows
- **Dataflow model — Source → Transform → Sink**: Source (Kafka, files, sockets) → Transformation (map, filter, aggregate, join) → Sink (database, Kafka, files); each step is a parallel operator; the DAG of operators is the Flink job
- **State**: maintained across events within an operator; enables aggregation over time (e.g., running count of clicks per user); state is checkpointed to durable storage (HDFS, S3) for fault tolerance; RocksDB state backend handles large state that doesn't fit in memory
- **Windowing**: partitions the stream into finite buckets for aggregation — Tumbling (fixed non-overlapping, e.g., 1-min counts), Sliding (overlapping windows, e.g., last 5 min updated every 1 min), Session (gap-based, groups events by inactivity period); window choice dramatically impacts accuracy and resource usage
- **Event time vs processing time**: event time = when the event actually occurred (embedded in the event payload); processing time = when Flink processes the event; event time is correct but out-of-order events arrive late; processing time is simpler but inaccurate if there's network delay or consumer lag
- **Watermarks**: logical timestamps that track progress through the event-time stream; a watermark at time T declares "all events with timestamp ≤ T have arrived"; enables Flink to close windows and trigger computation despite out-of-order delivery; `allowedLateness` handles stragglers after watermark
- **Exactly-once semantics**: Flink takes periodic distributed snapshots (Chandy-Lamport algorithm); on failure, restores from last checkpoint and replays only uncommitted events; combined with transactional sinks (Kafka transactions), achieves end-to-end exactly-once; adds latency and complexity — confirm you actually need it vs at-least-once
- **When to use Flink**: aggregating click/event streams in real-time (e.g., ads click aggregation), complex stateful processing across events, exactly-once requirements, multiple consumers with different processing logic from the same stream
- **When Flink is overkill**: simple message transformation (Kafka consumer + service is sufficient), stateless per-event processing (no aggregation needed), small data volume where Lambda (batch + stream) is acceptable
- **Operational complexity**: requires deploying + monitoring + scaling a dedicated Flink cluster; state management is the biggest operational challenge — must plan for state growth, checkpoint frequency, and recovery time; slot-based resource management isolates parallel tasks

**Near Real-Time Configuration (interview defaults)**
- Tumbling windows of 1–2 seconds for sub-5s latency
- 10–20 parallel tasks per operator
- RocksDB state backend for large states
- Watermarks with small allowed lateness (e.g., 5–10s) for late-arriving events

## Key Questions

**Q: When would you introduce Flink vs just consuming from Kafka directly in a service?**
Answer framework: Direct Kafka consumer is sufficient for stateless per-event processing (transform and write). Introduce Flink when: (1) stateful aggregation across events is needed (e.g., count clicks per ad per minute — requires maintaining per-key state), (2) windowing logic is complex (tumbling/sliding/session), (3) exactly-once guarantees matter (e.g., billing), (4) multiple downstream consumers need different processing logic from the same stream. Flink adds significant operational overhead — only justified when the stateful/windowing requirements exceed what a simple consumer can cleanly handle.

**Q: What is the difference between event time and processing time in Flink? Why does it matter?**
Answer framework: Processing time = when the event arrives at Flink; simple to implement but inaccurate if there's consumer lag or network delay. Event time = when the event actually occurred (timestamp in payload); produces correct results even with late-arriving or out-of-order events. Event time requires watermarks to know when a window can close. Matters in practice: if ad click data is delayed 30 seconds in Kafka, processing-time windows will miscount ads that occurred in the previous window. For billing or SLA-critical aggregations, event time is required.

**Q: What are watermarks in Flink? How do you handle late-arriving events?**
Answer framework: A watermark is a special record in the stream that says "I have seen all events up to time T." Flink uses watermarks to decide when to close a time window — it closes the window when the watermark passes the window end. For late events (arriving after the watermark), options: (1) `allowedLateness` — hold the window open for an additional buffer period; (2) side output — route late events to a separate stream for separate handling; (3) drop them (acceptable if small fraction). The lateness tolerance is a trade-off: larger tolerance → more accurate results but higher memory and latency.

**Q: How does Flink achieve fault tolerance? What is the checkpoint mechanism?**
Answer framework: Flink takes periodic distributed snapshots using the Chandy-Lamport algorithm — it injects checkpoint barriers into the data stream; each operator saves its state to durable storage (S3, HDFS) when it receives the barrier; once all operators have saved, the checkpoint is complete. On failure, Flink restores all operator states from the last successful checkpoint and replays in-flight events from the source (Kafka offsets are rewound). Combined with Kafka transactions at the sink, this achieves end-to-end exactly-once. Recovery time = checkpoint frequency + replay duration.

**Q: How would you design a real-time ads click aggregation system using Flink?**
Answer framework: Source = Kafka topic (click events with ad_id, user_id, timestamp); Flink job with keyed stream on `ad_id` → tumbling 1-minute windows → count clicks per ad per window; state backend = RocksDB (click counts per ad persist across events); watermarks handle late-arriving click events (allow 10s lateness for mobile app delay); sink = write aggregated counts to Redis (for real-time read) and to a time-series DB (for analytics). Checkpoint every 30s. This pattern recurs in interview questions: "design an ad click counter", "design a leaderboard", "count active users."

**Q: What is exactly-once processing? When is it worth the cost?**
Answer framework: Exactly-once means each input event affects the output exactly once — no duplicates, no missing events. Flink implements this via checkpointing + transactional sinks (e.g., Kafka transactions or idempotent writes). Cost: checkpoint overhead adds latency (checkpoint intervals of 30s–5min), transactional sinks reduce throughput, state size grows. Worth it for: billing, financial aggregations, inventory deduction — where duplicate processing has real monetary consequences. Not worth it for: approximate analytics, metrics dashboards, log aggregation where at-least-once is acceptable and duplicates are tolerable.

## Summary

Apache Flink is the production standard for stateful stream processing — it handles aggregating, joining, and transforming unbounded data streams with exactly-once guarantees and millisecond latency. The key concepts that distinguish it from a simple Kafka consumer are: stateful operators (aggregations that persist across events), windowing (tumbling/sliding/session), and event-time processing with watermarks (correct results despite out-of-order delivery).

The architectural insight generalizable beyond Flink: event time vs. processing time is a fundamental choice in any streaming system; watermarks are the mechanism for making progress in an ordered computation over unordered data; and checkpointing (Chandy-Lamport snapshots) is the standard approach to fault tolerance in distributed stateful systems — it appears in Spark Streaming, Kafka Streams, and cloud-native equivalents.

For AI Infra interviews, Flink appears in: real-time feature computation for ML models (aggregating user behavior streams into features), online training data pipelines, monitoring/anomaly detection on inference request streams, and experiment event logging. The pattern "Kafka → Flink → feature store" is a canonical real-time ML feature pipeline. Operationally, Flink clusters require careful capacity planning: state size growth, checkpoint storage cost, and recovery time are the three key SLO dimensions.

## Key Terms

**핵심 구성요소**
- `Source` · `Transformation` · `Sink` · `operator` · `dataflow DAG` · `Flink job`

**상태 관리**
- `stateful processing` · `keyed state` · `operator state` · `RocksDB` state backend · `in-memory` state backend
- `checkpoint` · `savepoint` · Chandy-Lamport algorithm · `checkpoint barrier`

**시간 / 윈도우**
- `event time` · `processing time` · `ingestion time`
- `watermark` · `allowedLateness` · side output
- `tumbling window` · `sliding window` · `session window`

**전달 보장**
- `exactly-once` · `at-least-once` · `at-most-once`
- transactional sink · idempotent write · offset rewind

**운영**
- `slot` · `task manager` · `job manager` · parallelism · `backpressure`
- checkpoint interval · state size · recovery time

**관련 시스템**
- `Kafka` · `Kafka Streams` · `Spark Streaming` · `Kinesis Data Analytics` · `Dataflow (GCP)`

**반패턴**
- Flink for stateless per-event processing (overkill — use plain Kafka consumer)
- Exactly-once when at-least-once suffices (unnecessary latency overhead)
- Processing time when event time correctness is required

## Raw Material
- [[raw_material/tech/system-design/hello-interview/tech-flink.md]]
