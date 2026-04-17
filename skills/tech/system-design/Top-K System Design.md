---
title: Top-K System Design
category: tech/system-design
tags: [system-design, streaming, top-k, kafka, flink, redis, count-min-sketch, leaderboard]
status: draft
priority: high
last_updated: 2026-04-16
created_from_jd:
---

# Top-K System Design

## Knowledge Map
- 前置知识：[[Streaming and Event-Driven Architecture]], [[Apache Kafka]], [[Cache and Consistency]], [[Sharding and Scalability]], [[Database Indexing]]
- 延伸话题：[[Redis]], [[Distributed Systems]], Count-Min Sketch, Flink, TimescaleDB
- 管理关联：

## Core Concepts

- **Problem variants** — Top-K problems span many use cases: top viewed videos, trending hashtags, most-purchased products. Requirements clarification is load-bearing because small changes (precise vs. approximate, time window type, max K) dramatically change the design.

- **Windowing: tumbling vs. sliding**
  - *Tumbling windows*: fixed boundary intervals (e.g., 9:00–10:00); simpler, each event belongs to exactly one window.
  - *Sliding windows*: continuously advancing window (e.g., last 60 minutes from now); more accurate but requires tracking decrements when events age out — significantly more complex.
  - Default recommendation in interviews: propose tumbling windows, let the interviewer object.

- **Precise vs. approximate results**
  - *Precise*: requires full count storage per video per window — expensive at massive scale (64 GB+ for 3.6B videos).
  - *Approximate*: **Count-Min Sketch (CMS)** reduces memory from GB to MB by using hash functions to map items to a 2D counter array; paired with a min-heap to maintain top-K candidates. Trade-off: no exact counts, possible overcounting, but no false negatives on high-view items.

- **Ingestion pipeline design**
  - Kafka as the ingestion layer (partitioned by videoId) decouples view events from processing; allows consumer parallelism and replay on failure.
  - *Naive*: one DB write per view event → 700K TPS at YouTube scale, far beyond single Postgres.
  - *Batching via Flink*: aggregate view counts in memory over tumbling windows, flush hourly/minutely to DB → 10–100x write reduction; `BoundedOutOfOrdernessWatermarkStrategy` handles late events (30s–1min buffer).

- **Scaling writes: sharding**
  - Shard DB by videoId; each Kafka partition consumer writes to its own shard.
  - Need ~70 shards for 700K TPS at 10K TPS/shard; batching reduces this to 5–10 shards.
  - Top-K cron queries top-K from each shard and merges (mathematically sound: top-K per shard guarantees the global top-K is included).

- **Scaling reads: precomputation + caching**
  - The query for top-K over a time window requires a full scan + sort — O(N) over billions of rows if run ad hoc.
  - Solution: maintain per-window aggregate tables (`VideoViewsLastHour`, `VideoViewsLastDay`, `VideoViewsLastMonth`) with indexes on `views`; queries become O(K).
  - Cron job updates cache on fixed intervals (every minute); read path hits Redis/Memcached only → low tens of ms latency.
  - Cache TTL kept longer than cron interval so stale data serves during cron delays rather than cache misses hitting the DB.

- **Full Flink pipeline (advanced approach)**
  - Flink maintains rolling window aggregates and top-K heap in its distributed state (RocksDB for off-heap), writes directly to Redis sorted set.
  - Eliminates separate DB + cron; Kafka offset checkpointing handles failure recovery.
  - Downside: requires deep Flink knowledge; interviewers may ask for lower-level explanation.

- **Sliding window implementation**
  - Flink aggregates at minute grain; each new minute: increment current views, decrement views from T-60 min.
  - Requires keeping minute-grain data for full window duration (1 month = large storage).
  - Alternative: two Kafka consumer groups — one increments, one consumes on a lag and decrements.
  - CMS supports removal if items are only decremented after being previously incremented — enables approximate sliding windows.

- **Specialized databases**
  - TimescaleDB: Postgres extension with time-based partitioning and continuous aggregates; fits the per-window aggregate pattern naturally; still needs caching for low-latency reads.
  - Druid/Pinot/ClickHouse: real-time OLAP with materialized rollups; powerful but requires deep familiarity to defend in interviews.
  - Guideline: understand *why* primitives (Kafka + Flink + Redis + sharded DB) work before reaching for specialized tech — interviewers probe underlying understanding.

- **Back-of-envelope anchors (YouTube scale)**
  - 70B views/day ÷ 100K s/day = **700K TPS ingestion**
  - 1 hr content/s ÷ 6 min/video × 100K s/day = **1M new videos/day**; 10 years ≈ **3.6B total videos**
  - Naive storage for ID + count per video: **~64 GB** (useful reference for every design layer)

## Key Questions

**Q: Walk me through how you'd design a top-K trending videos system for YouTube.**
Answer framework: State requirements clarifications first (tumbling vs. sliding, precise vs. approximate, time windows, max K). Sketch the happy path: Kafka → consumer → DB with per-video counts → top-K query with index. Then systematically address each bottleneck: write throughput (sharding + Flink batching), read latency (per-window aggregate tables + caching/precomputation), freshness SLA (cron every minute, 1-min event buffer). Mention approximate option (CMS) if time allows.

**Q: What's the difference between tumbling and sliding windows and when would you choose each?**
Answer framework: Define both precisely. Tumbling = fixed boundary, simpler implementation, suitable when exact real-time accuracy isn't critical (e.g., hourly leaderboard). Sliding = always reflects the last N minutes from now, more accurate for trending, but requires decrement mechanics (more complex and storage-intensive). In most interviews, start with tumbling and offer to extend to sliding if asked.

**Q: How would you handle 700K view events per second without overwhelming your database?**
Answer framework: Two complementary strategies. First, sharding by videoId — partition Kafka by videoId, align DB shards to the same scheme, each consumer writes to its own shard. Second, batching with Flink — aggregate in memory over a window, write sums instead of individual events, reducing writes by 10–100x. Calculate: 70B/day → 700K TPS → need ~70 shards at 10K TPS each; with Flink batching, reduce to 5–10 shards.

**Q: How do you achieve sub-100ms query latency for top-K given the data volumes involved?**
Answer framework: Ad hoc queries over billions of rows are out — even with indexes, the windowed GROUP BY + ORDER BY requires full scans. Solution: precompute per-window aggregate tables maintained by the Flink job; index on `views` makes O(K) queries possible. Serve reads exclusively from a Redis/Memcached cache that is warmed by a cron every minute. Cache TTL exceeds cron interval to serve stale on delay rather than missing entirely.

**Q: How does Count-Min Sketch help with top-K and what are its trade-offs?**
Answer framework: CMS uses d hash functions mapping each item to d counters in a 2D array. `add(item)` increments all d counters; `estimate(item)` returns the minimum of d counters (overcounts, never undercounts). Paired with a min-heap to maintain top-K candidates. Memory drops from 64 GB (full hash table) to hundreds of MB. Trade-off: estimates may overcount due to hash collisions; no false negatives for genuinely high-count items. Not suitable when exact counts are required (e.g., financial leaderboards). Supports approximate sliding windows via `remove()` — decrement counters when events age out.

**Q: How would you extend the system to support sliding windows?**
Answer framework: Two approaches. (1) DB-based: Flink aggregates at minute grain; each minute, write new views and subtract views from T-60min. Requires storing minute-grain data for entire window period (expensive for month window). (2) Dual Kafka consumer groups: one consumer group increments on arrival, second consumer group reads the same events on a 1-hour lag and decrements. Avoids storing minute-grain data long-term; requires long Kafka retention. Mention that CMS's native sliding window in Flink multiplies memory by 43,200x — impractical; use the remove-based approach instead.

**Q: When should you use Flink vs. a simpler Kafka consumer + DB approach?**
Answer framework: Flink adds value when: (a) batching/aggregation logic is complex (multi-window, late event handling, stateful computation), (b) failure recovery with exactly-once semantics is required, (c) you need to avoid a separate DB layer for aggregation. Downside: operational complexity, requires interviewer/candidate to be familiar with Flink. For simpler systems, a Kafka consumer + DB with a cron for precomputation achieves similar results with fewer moving parts. Recommend simple approach first, offer Flink as optimization.

## Summary

Top-K is one of the most flexible and frequently varied system design problems because the right design depends heavily on whether the system must be precise or approximate, whether time windows are tumbling or sliding, and the scale of the event stream. The first priority in any Top-K interview is requirements clarification: propose tumbling windows, cap K at 1K, and default to precise results — then let the interviewer adjust. These three decisions determine the complexity of everything downstream.

The core architecture for YouTube-scale Top-K consists of three layers: an ingestion pipeline (Kafka partitioned by videoId → Flink aggregator that batches writes per window), a storage layer (sharded DB with per-window aggregate tables indexed on `views`, enabling O(K) queries), and a read path (Redis cache warmed every minute by a cron, serving all client queries with sub-100ms latency). The key insight is that precomputing per-window aggregates — `VideoViewsLastHour`, `VideoViewsLastDay` — transforms an O(N) scan into an O(K) index read, which is what makes low-latency queries possible. Without precomputation, even a well-indexed DB cannot serve windowed top-K queries at speed.

For approximate requirements, Count-Min Sketch (CMS) pairs with a min-heap to reduce memory from 64 GB to hundreds of MB at the cost of potential overcounting. Sliding windows are significantly more complex: they require either minute-grain data retention + decrement mechanics, or a dual-consumer-group Kafka pattern that amortizes the decrement over time. The advanced Flink-native solution (state in RocksDB, direct write to Redis) is the most elegant but requires deep Flink knowledge. In most interviews, build from primitives (Kafka + batching + sharded DB + caching) rather than reaching for Flink or specialized databases first — understanding the primitives demonstrates the judgment that allowed those specialized tools to be built.

## Key Terms

**Windowing**
- `tumbling window` · `sliding window` · `window boundary` · `window grain`

**Ingestion & Streaming**
- `Kafka` · `partition by videoId` · `consumer group` · `offset checkpointing` · `BoundedOutOfOrdernessWatermarkStrategy` · `late event buffer` · `Flink` · `RollingWindowAggregator` · `RocksDB state backend`

**Storage & Aggregation**
- `per-window aggregate table` · `views index` · `sharding` · `WAL` · `unlogged table` · `continuous aggregate` · `TimescaleDB hypertable` · `Druid` · `Pinot` · `ClickHouse`

**Read Path**
- `precomputation` · `cron warm` · `cache TTL` · `Redis sorted set` · `Memcached` · `O(K) query`

**Approximation**
- `Count-Min Sketch (CMS)` · `hash function` · `2D counter array` · `min-heap` · `estimate overcount` · `CMS.DECRBY` · `remove operation`

**Scale Anchors**
- `700K TPS` · `3.6B videos` · `64 GB naive storage` · `70 shards` · `5-10 shards with batching`

## Raw Material
- [[raw_material/tech/system-design/YouTube Top K - Hello interview]]
