---
title: "Hello Interview — Case: TicketMaster"
source: "https://www.notion.so/1e5afa27ec72806ea999f77715bd0831"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/System Design Case - TicketMaster]]"
---

# Case: TicketMaster

## Key Design Questions & Answers

### Two-Phase Booking: Seat Reservation + Confirmation

**Core Pattern: Redis Distributed Lock**

1. Introduce a global lock service via Redis (distributed cache, single-threaded)
2. When user books via booking service: add record into Redis with ticketId + reservationId + TTL
3. If another user tries to book the same ticket: Redis record exists → show "ticket locked, unable to reserve"
4. Redis supports atomic operation for one key: SETNX command (only sets if key doesn't exist)
5. During TTL: user completes payment → ticket status changed to "booked" → others cannot reserve
6. If user doesn't complete checkout during TTL: record expires → other users can reserve
7. Race condition handling: during payment, check cache expiration; only if key exists in cache is payment allowed to complete

### Scale to 10M concurrent users reading event data

1. API Gateway + Load Balancer for multiple stateless event service instances (auto-scaling)
2. Redis event cache for majority of reads; write-through invalidation when event updates in DB
3. Cassandra or MongoDB for event storage (easy to scale, supports read/write splitting)
4. Event ID as partition key; date as index; Global Secondary Index (e.g., name)
5. Monitoring: watch latency, CPU/memory → trigger auto-scaling

### Improve search with complex queries

1. ElasticSearch for full-text search on event name, type, category; composite index with field mapping
2. Field boosting: high scores for matching event name vs. description
3. CDC (Change Data Capture) to sync from Cassandra to ElasticSearch; dual write for ticket status (needs strong consistency)
4. Cache hot search results in Redis or CDN

**Elasticsearch bool queries** for complex multi-criteria: "must" clauses for exact date matches, "should" clauses for artist name variations, geo-distance filters for location — all processed in parallel.

### Real-time seat map refresh

Server-Sent Events (SSE):
1. User views seat map → client establishes SSE connection to Booking Service
2. When booking completes → push SSE to related clients → update seat map
3. For thousands of viewers: introduce pub/sub via Kafka; record which server handles which set of clients
4. Client restart: record timestamp periodically in client local; on restart, fetch whole event info with latest stored timestamp

### Virtual Waiting Room (for popular events)

Redis Sorted Sets:
- Users redirected to waiting room; session IDs added to sorted set with timestamp as score (FIFO)
- Every N minutes, pull users from front with ZRANGE; grant access in controlled manner
- Handle disconnection/reconnection: issue unique tokens allowing users to reclaim position within a time window, or heartbeat mechanism to detect disconnections
