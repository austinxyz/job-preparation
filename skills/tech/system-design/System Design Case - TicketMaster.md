---
title: System Design Case - TicketMaster
category: tech/system-design
tags: [system-design-case, distributed-locking, redis, sse, elasticsearch, concurrency]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# System Design Case - TicketMaster

## Knowledge Map
- 前置知识：Redis SETNX, distributed locking, ElasticSearch, CDC (Change Data Capture), SSE, Kafka pub/sub, Redis Sorted Sets
- 延伸话题：payment systems, inventory reservation patterns, flash sale systems, two-phase commit vs. optimistic locking
- 管理关联：

## Core Concepts

- **Two-Phase Booking (Reserve → Confirm)**: Separating reservation from payment prevents double-booking while allowing users time to complete checkout. Redis holds the reservation lock with a TTL. If payment completes before TTL expires, the ticket is confirmed. If TTL expires without payment, the reservation is released automatically.
- **Redis SETNX for Atomic Reservation**: `SETNX ticketId reservationId` is atomic — only one client can set a key that doesn't exist. This prevents race conditions at the moment of reservation without needing database-level locking. The key's existence signals "locked"; absence signals "available."
- **TTL-Based Lock Expiry**: No explicit unlock needed for abandoned checkouts — the TTL expires automatically. The race condition at payment time requires an additional check: verify the Redis key still exists before finalizing payment (confirms the lock hasn't expired due to timeout).
- **ElasticSearch for Event Search**: Relational DB queries can't efficiently serve full-text search (event name, artist, category). ElasticSearch supports composite indexes, field boosting (event name match scores higher than description match), and parallel processing of multi-criteria `bool` queries. CDC syncs changes from the primary DB to ES asynchronously.
- **SSE for Seat Map Real-Time Updates**: When a seat is booked, the server pushes an update to all clients viewing that seat map via SSE. For popular events with thousands of viewers, Kafka pub/sub distributes booking events across multiple SSE servers. Each server tracks which clients it's serving.
- **Redis Sorted Set for Virtual Waiting Room**: For highly-anticipated event releases (Taylor Swift tickets), a waiting room prevents system overload. Users are enqueued with timestamp as score (FIFO). Every N minutes, a batch is granted access. Unique tokens allow reconnecting users to reclaim their position within a time window.
- **Read Scaling for Event Data**: 10M concurrent readers for popular events. Redis cache with write-through invalidation handles the majority. Cassandra/MongoDB for the backing store (partition by eventId, secondary index on date and name). Auto-scaling stateless event service instances handle traffic spikes.

## Key Questions

**Q: Two users try to book the last ticket simultaneously. How do you prevent double-booking?**
Answer framework: Redis SETNX is atomic — only one client can successfully set a key that doesn't exist. The first caller gets the reservation lock (key = ticketId, value = reservationId, with TTL). The second caller finds the key already exists and receives "unavailable." No database transaction needed for the reservation phase; the DB update happens only after successful payment.

**Q: A user starts checkout but their browser crashes. How does the seat become available again?**
Answer framework: The Redis reservation key has a TTL (e.g., 10 minutes). If the user doesn't complete payment within TTL, the key expires automatically and the ticket becomes available for others. No cleanup job needed. The system must verify key existence at payment time to handle the edge case where TTL expires just before payment completes.

**Q: How would you build the seat map that updates in real-time for thousands of concurrent viewers?**
Answer framework: SSE for the client connection (server-push, lower overhead than WebSocket for one-way updates). When a booking completes, the event is published to Kafka. Multiple SSE server instances consume from Kafka as a consumer group. A coordinator tracks which server handles which event's viewer connections. Kafka partitioned by eventId ensures all booking events for one event go to the same partition.

**Q: Why use ElasticSearch instead of just adding database indexes for search?**
Answer framework: Relational DB indexes work for exact-match or range queries, but can't efficiently handle full-text search (partial artist name, fuzzy matching), multi-criteria parallel evaluation, or field boosting. ElasticSearch's inverted index is purpose-built for this. The trade-off is eventual consistency — CDC introduces a small lag between DB writes and ES index updates. For ticket availability (strong consistency required), dual-write directly to ES.

**Q: How do you handle 10M concurrent users reading event data for a popular concert announcement?**
Answer framework: Redis cache for event data (write-through invalidation on update). Stateless event service instances auto-scale behind a load balancer. Cassandra for event storage (horizontal scale, read/write splitting). CDN for static event assets (images, venue maps). Monitor latency and CPU to trigger auto-scaling before cache hit rate degrades.

**Q: Walk through the virtual waiting room design for a high-demand ticket sale.**
Answer framework: Redis Sorted Set with userId as member and arrival timestamp as score (FIFO ordering). Users are redirected to the waiting room UI. Every N minutes, a batch of users is granted access via ZRANGE + ZREM. Users receive a unique access token with its own TTL. Heartbeat mechanism detects disconnections; token allows reconnecting users to bypass re-queuing within the token window.

## Summary

TicketMaster must handle high-concurrency ticket reservation for popular events while ensuring correctness (no double-booking) and a real-time seat map for all viewers. Core functional requirements: event browsing, seat selection, two-phase booking (reserve + pay), and seat map updates.

The architectural centerpiece is the Redis-based distributed lock for reservation. SETNX provides atomic reservation without database transactions, and TTL handles abandoned checkouts automatically. This is a classic inventory reservation pattern with a time-bounded lock — the trade-off being that the lock window (TTL) must be long enough for checkout but short enough to not frustrate other buyers.

The hardest part of this case is the combination of read scale (10M concurrent event viewers) and write correctness (no double-booking). These require different tools: caching + CDN for reads, Redis atomic operations for write correctness. The virtual waiting room and real-time seat map are common deep-dive targets — both rely on Redis Sorted Sets and pub/sub patterns that generalize across many systems.

## Key Terms

**Technologies**
- `Redis SETNX` · `Redis Sorted Sets` · `ElasticSearch` · `CDC` · `SSE` · `Kafka` · `Cassandra`

**Patterns**
- `Two-Phase Booking (Reserve → Confirm)` · `TTL-Based Lock Expiry` · `Virtual Waiting Room` · `Write-Through Cache Invalidation`

**Decision Points**
- `TTL duration for reservation` · `ES vs. DB search` · `CDC eventual consistency for search` · `SSE vs. WebSocket for seat map`

## Raw Material
- [[raw_material/tech/system-design/hello-interview/case-ticketmaster.md]]
