---
title: "Hello Interview — Case: Ads Click Aggregation"
source: "https://www.notion.so/1f7afa27ec728098a1f6f9c5dc482f9d"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/System Design Case - Ads Click Aggregation]]"
---

# Case: Ads Click Aggregation

## Key Design Questions & Answers

### High-Level Design

1. Ad Placement Service fetches from Ad DB → displays ads with tracking links
2. User clicks ad → **server-side redirect** (prevents client-side bypass) → Ad Click Processor logs event
3. Click events stored in Cassandra (raw events)
4. Cron job triggers Spark task periodically to aggregate events
5. Aggregated results stored in Ads Metrics DB (OLAP: Redshift/Snowflake)
6. Advertisers query Ads Analysis Service → Ads Metrics DB

### Scale to 100K Clicks/Second

**Kafka + Flink**:
1. Ad Click Processor publishes click events to Kafka (partitioned by adId)
2. Flink processes Kafka events in real-time; multiple instances handle different shards
3. Flink stores aggregation results in Ads Metrics DB with checkpointing for fault tolerance
4. Capacity: 100K clicks × 100 bytes = ~10MB/s; each partition handles 50-100MB/s → 1-10 Kafka partitions

### Kafka Outage Handling

1. Circuit breaker in Ad Click Processor: on Kafka outage → switch to Cassandra event DB fallback
2. Circuit breaker periodically checks Kafka availability; on recovery → switch back
3. **Replay Service**: reads Cassandra events sorted by timestamp → republishes to Kafka in correct order → Flink continues processing

### Idempotent Click Tracking (Deduplication)

1. Ad Placement Service generates **impression ID** per ad link (based on user secret)
2. Click event carries impression ID
3. Ad Click Processor checks if impression ID exists in Redis impression list:
   - If exists → duplicate, drop event
   - If not → send to Kafka + add impression ID to Redis list with TTL (e.g., 10 days)
4. TTL balances deduplication accuracy with Redis memory capacity
5. Redis cluster with Sentinel for HA; local buffer on Redis failure → circuit breaker pattern

### Low-Latency Advertiser Queries

**Pre-aggregation**:
1. Cron jobs run at fixed intervals (per minute, hour, day, week, month)
2. Per-hour job: aggregates per-minute click counts for each AdId → stores hourly total
3. Old granular data deleted after retention period (e.g., per-minute data older than 7 days)
4. Advertiser queries date range (e.g., 1 day + 2 hours) → Analysis Service fetches day metrics + hour metrics → merges
5. **Reconcile job**: reads Cassandra event DB daily, regenerates metrics, fixes gaps vs. Flink results; latest 24h highest priority

### Hot Partition Handling (Popular Ads)

1. Detect hot ad: `>10K clicks within 1 minute`; Flink aggregation confirms pattern 5+ times
2. Switch partition key from `adId` to `adId+seq` (e.g., adId:1, adId:2, … adId:10)
3. Apply same composite key to Redis, Cassandra, Flink sharding
4. Pre-calculated jobs aggregate metrics across all `adId+seq` → report by original adId
5. During transition: both `adId` and `adId+seq` events in flight; Flink handles both; aggregation merges all

### Near Real-Time Queries (<5s)

1. Flink with **tumbling windows of 1-2 seconds**, 10-20 parallel tasks per operator
2. Store per-second metrics in Ads Metrics DB → **ClickHouse or Druid** (columnar store) for sub-second query with pre-aggregation + materialized views + in-memory cache
3. Reconcile job runs after real-time pipeline to fix any data loss or delay
4. Show advertisers: timely (near real-time, possibly incomplete) vs. eventually complete metrics (after reconcile)
