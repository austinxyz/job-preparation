---
title: System Design Case - Ads Click Aggregation
category: tech/system-design
tags: [system-design-case, stream-processing, kafka, flink, olap, idempotency, hot-partition, cassandra, clickhouse]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# System Design Case - Ads Click Aggregation

## Knowledge Map
- 前置知识：Kafka (partitions, consumer groups), Flink (streaming, checkpointing, tumbling windows), OLAP stores (ClickHouse, Druid, Redshift), Cassandra, circuit breaker pattern, hot partition problem
- 延伸话题：[[System Design Case - Post Search]] (Kafka + hot partition), [[System Design Case - Bit.ly (URL Shortener)]] (Kafka analytics pipeline)
- 管理关联：

## Core Concepts

- **Server-side redirect to capture clicks**: The ad link goes through the server before redirecting to the target URL. This prevents client-side bypass (JavaScript disabled, tracking blocked) and ensures every click is recorded. The client never directly hits the advertiser URL without the server logging the click first.
- **Cassandra as raw event store**: Raw click events (high write throughput, time-ordered) are stored in Cassandra. Cassandra's LSM tree architecture is optimized for high write throughput. These raw events serve as the ground-truth replay source for the Kafka Replay Service and the daily Reconcile job.
- **Kafka + Flink for real-time aggregation at 100K RPS**: Click events are published to Kafka (partitioned by adId). Flink consumes in real-time with multiple parallel tasks, aggregating click counts per time window. Checkpointing ensures exactly-once processing semantics even if a Flink task fails. Scale: 100K clicks × 100 bytes = ~10MB/s → 1-10 Kafka partitions sufficient.
- **Impression ID deduplication at Redis layer**: Each ad impression generates a unique impression ID (based on user secret + ad placement). When a click event arrives, the Ad Click Processor checks Redis for the impression ID — if seen, it's a duplicate and is dropped. New impression IDs are added to Redis with TTL (10 days). This prevents one ad click from being counted multiple times.
- **Pre-aggregated metrics for low-latency advertiser queries**: Cron jobs aggregate click counts at multiple granularities (per-minute, per-hour, per-day). Advertisers query a date range; the Analysis Service combines the appropriate pre-aggregated rows. Old fine-grained data is deleted after retention period (e.g., per-minute data older than 7 days). This avoids full-scan aggregation at query time.
- **Hot partition detection and `adId+seq` sharding**: When an ad gets >10K clicks per minute (confirmed 5+ times by Flink), the partition key switches from `adId` to `adId+seq` (e.g., adId:1, adId:2, …, adId:10). This distributes a popular ad's events across 10 Kafka partitions, 10 Redis shards, and 10 Flink tasks. Aggregation jobs merge across all `adId+seq` variants when reporting.
- **Kafka outage fallback to Cassandra**: A circuit breaker in the Ad Click Processor detects Kafka unavailability and routes events directly to Cassandra. On Kafka recovery, the Replay Service reads Cassandra events in timestamp order and republishes them to Kafka, resuming the normal pipeline.

## Key Questions

**Q: Why use server-side redirect instead of a client-side tracking pixel or JavaScript beacon?**
Answer framework: Client-side tracking is blockable (ad blockers, NoScript, privacy browsers). Server-side redirect is the only reliable mechanism — the client must pass through the server to reach the destination URL. The trade-off is slightly higher latency (one extra server hop), but this is typically <50ms and non-negotiable for accurate billing.

**Q: How does the impression ID prevent duplicate click counting?**
Answer framework: The Ad Placement Service generates an impression ID when serving the ad. This ID is embedded in the tracking link. When the user clicks, the click event carries the impression ID. The Ad Click Processor checks Redis: if the ID exists, drop the event (duplicate); if not, process it and add to Redis with TTL. The TTL limits Redis memory growth while covering the realistic "same user clicks twice" window.

**Q: How does Flink handle failures without losing click counts?**
Answer framework: Flink uses checkpointing to periodically save aggregation state to a distributed store. On failure, Flink restarts from the last checkpoint and reprocesses Kafka offsets from that point. Combined with Kafka's offset tracking, this provides exactly-once semantics — counts are neither lost nor double-counted. The checkpoint interval is the trade-off: shorter intervals = lower data loss on failure but higher overhead.

**Q: How do you handle the scenario where an advertiser queries for the last 25 hours of data?**
Answer framework: The Analysis Service decomposes the range: 24 hours = 1 pre-aggregated "day" row, 1 hour = 1 pre-aggregated "hour" row. It fetches and sums these rows rather than scanning individual minute-level events. This turns a potentially slow aggregation into a small number of indexed row lookups. The granularity hierarchy (second → minute → hour → day → week → month) must be kept consistent in the pre-aggregation cron jobs.

**Q: How does the hot partition transition work without losing events in flight?**
Answer framework: When the hot ad is detected, the partition key changes from `adId` to `adId+seq`. During the transition window, both `adId` and `adId+seq` events coexist in Kafka. Flink is configured to recognize both key formats and aggregates them together. The pre-aggregation cron jobs query all `adId+seq` partitions and sum them when reporting by the original `adId`. Once the transition is complete and no old-format events remain, the routing logic is cleaned up.

**Q: What's the purpose of the daily Reconcile job if Flink already provides exactly-once semantics?**
Answer framework: Flink's exactly-once applies within the Flink pipeline. But there are failure modes outside it: Kafka outage (events fell to Cassandra fallback), network partitions, or delayed events arriving after the tumbling window closes. The Reconcile job reads from Cassandra (raw event ground truth) daily, recomputes metrics, and fills any gaps in the Flink output. It prioritizes the last 24 hours and runs after the real-time pipeline to patch discrepancies.

**Q: Why use ClickHouse or Druid for sub-second queries rather than a standard OLAP like Redshift?**
Answer framework: ClickHouse and Druid are optimized for time-series aggregation with pre-aggregated materialized views and columnar storage. For near-real-time queries (<5s latency) on per-second metrics, they offer sub-second query times with in-memory cache. Redshift and Snowflake are batch-oriented — they're designed for multi-second to multi-minute queries over historical data. For an advertiser dashboard requiring near-real-time updates, ClickHouse/Druid are better fits.

## Summary

Ads click aggregation is a high-throughput data pipeline problem with strict accuracy requirements (financial billing depends on it). The system processes 100K clicks/second, deduplicates in real time, aggregates for low-latency queries, and reconciles to catch any gaps. The core pipeline is Kafka → Flink → OLAP, with Cassandra as a raw event safety net.

The non-obvious design decisions are: (1) server-side redirect as a non-negotiable correctness requirement for tracking; (2) impression ID deduplication at the ingress point (Redis check before Kafka publish) rather than downstream — cheaper to stop duplicates early; (3) the `adId+seq` hot partition pattern — the same pattern as hot key handling in any sharded system, applied to Kafka partitions and Flink tasks simultaneously.

What interviewers are testing: understanding of stream processing (Kafka + Flink) vs batch processing trade-offs, hot partition detection and mitigation, idempotency as a first-class design constraint, and multi-granularity pre-aggregation for query performance.

## Key Terms

**Technologies**
- `Kafka` · `Flink` · `Cassandra` · `Redis` · `ClickHouse` · `Druid` · `Redshift/Snowflake`

**Patterns**
- `server-side redirect` · `impression ID deduplication` · `Flink checkpointing (exactly-once)` · `pre-aggregated metrics hierarchy` · `hot partition (adId+seq)` · `circuit breaker with Cassandra fallback` · `daily reconcile job`

**Decision Points**
- `server-side vs client-side click tracking` · `Flink vs Spark for real-time aggregation` · `ClickHouse/Druid vs Redshift for near-real-time queries` · `impression ID TTL balance`

## Raw Material
- [[raw_material/tech/system-design/hello-interview/case-ads-click.md]]
