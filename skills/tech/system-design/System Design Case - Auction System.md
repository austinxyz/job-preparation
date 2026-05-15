---
title: System Design Case - Auction System
category: tech/system-design
tags: [system-design-case, redis, kafka, optimistic-locking, sse, pub-sub, concurrency, consistency]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# System Design Case - Auction System

## Knowledge Map
- 前置知识：optimistic concurrency control, PostgreSQL row-level locking (SELECT FOR UPDATE), Kafka partitioning, Redis Lua scripts, SSE, Redis pub/sub
- 延伸话题：Dutch auctions, reserve prices, auction sniping countermeasures (auto-extend), anti-fraud for shill bidding, escrow/payment integration
- 管理关联：

## Core Concepts

- **Optimistic Concurrency Control (OCC) for Bid Consistency**: Two concurrent bids on the same item must not both succeed if only one can be the highest. OCC: `SELECT maxBidId FOR UPDATE` (row-level lock) → compare prices → `UPDATE maxBidId WHERE maxBidId = originalId`. If another bid changed `maxBidId` between read and write, the update affects 0 rows → retry with exponential backoff. Avoids holding locks for the full bid processing time.
- **Kafka as Durable Bid Buffer**: Bids are published to Kafka before DB processing. Kafka persists to disk — bids survive Bid Service crashes. Partitioned by auctionId so all bids for one auction are ordered. Consumers commit offset only after successful DB write → at-least-once delivery. Idempotency via global unique bidId prevents double-processing on redelivery.
- **Redis Single-Threaded for High-Write Auctions**: For auctions with very high bid rates, Redis's single-threaded execution model provides natural serialization (no concurrent modifications). Lua scripts for atomic read-compare-write (equivalent to OCC but in-memory). Redis Sentinel + periodic snapshots for durability. Live auction data in Redis; completed auctions archived to PostgreSQL.
- **SSE + Redis Pub/Sub for 100M+ Real-Time Viewers**: Connection Management Service shards by auctionId → Redis instance. Each Redis instance stores `auctionId → list of SSE connections` and subscribes to `auctionId` events. When a bid is accepted, Bid Service publishes to all Redis instances (fan-out). Each subscribed instance pushes to its SSE client list.
- **Batch Archival for Scale (50TB Historical Data)**: Only live auction data lives in Redis (in-memory, expensive). On auction completion, a batch job migrates data from Redis to Auction DB. Historical auction data is partitioned by `startTime` in a separate historical DB optimized for analytics queries. This keeps the hot path (active auctions) fast and the cold path (historical) cost-efficient.
- **Retry Storm Risk Near Auction End**: Popular items see exponentially increasing bids in the final seconds. Each failed OCC retry with exponential backoff could trigger many retries simultaneously. Mitigation: exponential backoff with jitter (randomized delay) to spread retries over time. Redis Lua script approach avoids the retry problem entirely by serializing at the in-memory layer.
- **Connection Management Service Sharding**: Maintains the mapping `auctionId → set of SSE connections`. Shards by auctionId to Redis instances for locality. When a Redis instance fails, Connection Management detects via heartbeat and recreates SSE connections on a new Redis instance. Ensures no permanent connection loss.

## Key Questions

**Q: Two users place bids simultaneously. How do you guarantee only the higher bid wins and no data is corrupted?**
Answer framework: Optimistic Concurrency Control with PostgreSQL row-level lock. `SELECT maxBidPrice, maxBidId FROM auctions WHERE id = ? FOR UPDATE` → compare `newBid.price > maxBidPrice` → `UPDATE auctions SET maxBidId = newBidId WHERE maxBidId = originalBidId`. If update affects 0 rows, another bid won the race — retry with exponential backoff. Row-level lock ensures reads within the transaction see current state.

**Q: The Bid Service crashes while processing a bid. How do you ensure the bid isn't lost?**
Answer framework: Kafka as durable buffer. Bids are published to Kafka (partitioned by auctionId) before processing. Consumers use offset commit only after successful DB write. If the service crashes mid-processing, the uncommitted message is redelivered to another consumer instance. Idempotent processing via global bidId prevents the redelivered message from creating a duplicate bid.

**Q: How do you broadcast the new highest bid to 100 million concurrent viewers in real-time?**
Answer framework: SSE for client connections (unidirectional push). Connection Management Service shards SSE connections by auctionId across Redis instances. Each Redis instance stores a list of SSE connections for its auctions and subscribes to bid events for those auctions. Bid Service publishes new bids to all Redis instances (fan-out at the Redis layer). Each Redis instance pushes to its SSE connection list. This scales horizontally — add more Redis instances as auction count grows.

**Q: An auction ends and has 10 years of bid history. How do you manage 50TB of data?**
Answer framework: Tier the data. Live auctions: Redis (fast, expensive, in-memory). Active DB: recent/ongoing auctions in PostgreSQL. Historical DB: completed auctions partitioned by `startTime` (range partitioning for time-based queries). Batch archival job runs during off-peak: migrates completed auction data from Redis → Active DB → Historical DB based on age. Historical DB can use columnar storage (Parquet/Redshift) for analytics.

**Q: What happens if a user places a bid 1 millisecond before an auction ends?**
Answer framework: Bids are timestamped on receipt. If the bid timestamp is before the auction end time, it's valid. Kafka ordering within the auctionId partition ensures sequential processing. The final bid processing includes a validation step: `bid.timestamp < auction.endTime`. Any bids arriving with timestamps after end time are rejected. The "auction sniping" countermeasure is auto-extending: if a bid arrives within N seconds of end time, extend the auction by M minutes.

**Q: Why use Redis with Lua scripts instead of PostgreSQL for high-frequency bidding?**
Answer framework: PostgreSQL with `SELECT FOR UPDATE` serializes at the row level but involves disk I/O, network round trips, and transaction overhead. Under very high bid rates (e.g., 50K bids/sec near auction end), the lock contention and I/O overhead create queuing delays. Redis single-threaded execution with Lua scripts achieves the same atomicity (read-compare-write) in microseconds, in memory. The trade-off: Redis data is volatile (mitigated by Sentinel + snapshots) and doesn't support complex SQL queries. Use Redis for the hot write path; PostgreSQL for the durable record.

## Summary

An auction system must handle concurrent bids with strict consistency (no two winners, highest bid always wins), deliver real-time bid updates to potentially hundreds of millions of viewers, and store decades of auction history efficiently. The core tension is between write correctness (strong consistency for bids) and read scale (fan-out to millions of viewers).

Bid consistency uses Optimistic Concurrency Control: PostgreSQL row-level locking for the compare-and-swap. This is lighter than full pessimistic locking but still provides correctness. For ultra-high bid rates, Redis single-threaded Lua scripts replace PostgreSQL for the hot write path — effectively serializing bids in memory without lock contention. Kafka acts as a durable buffer between bid receipt and DB processing, eliminating data loss on service crashes.

The real-time broadcast to 100M+ viewers is the scaling challenge that dominates the deep dive. The SSE + Redis pub/sub architecture shards connection management by auctionId — keeping fan-out local to the Redis instance managing that auction's connections. The interview tests whether candidates can design the connection management layer (sharding, failure recovery) rather than just saying "use WebSocket/SSE."

## Key Terms

**Technologies**
- `PostgreSQL (SELECT FOR UPDATE)` · `Kafka` · `Redis Lua Scripts` · `SSE` · `Redis Pub/Sub` · `Redis Sentinel`

**Patterns**
- `Optimistic Concurrency Control (OCC)` · `Kafka Durable Buffer` · `SSE + Redis Pub/Sub Fan-Out` · `Tiered Storage (Redis → DB → Historical)` · `Exponential Backoff with Jitter`

**Decision Points**
- `OCC vs. pessimistic locking` · `Redis vs. PostgreSQL for hot write path` · `at-least-once + idempotency vs. exactly-once` · `live data in Redis vs. DB from the start`

## Raw Material
- [[raw_material/tech/system-design/hello-interview/case-auction-system.md]]
