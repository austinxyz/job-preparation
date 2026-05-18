---
title: "Hello Interview — Key Technology: Redis"
source: "https://www.notion.so/1faafa27ec7280ddbc4afac8827b565c"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/Redis]]"
---

# Key Technology: Redis

## Core Characteristics

- **In-memory**, written in C, **single-threaded** (atomic operations guaranteed)
- ~100K requests/second throughput
- Data structures: Strings, Hashes, Lists, Sets, **Sorted Sets**, Bloom Filters, Geospatial Indexes, Time Series
- Pub/Sub, Streams
- Key-value store; values can be any supported data structure

## Deployment Modes

- **Single node**: simplest
- **Replicated**: primary + replicas (async replication)
- **Cluster**: data sharded across nodes via consistent hashing; gossip protocol for node awareness; all data for a request must be on a single node

## Common Use Cases

### Cache with TTL

Standard caching with expiration.

### Distributed Lock (TicketMaster, Uber)

`SET key value NX EX ttl` — atomic set-if-not-exists with expiration:
- `INCR` to acquire lock (if response = 1, we own it; if >1, someone else has it)
- `DEL` to release
- **Redlock algorithm** for multi-node distributed lock

### Leaderboard (Sorted Set)

- `ZADD` to add/update score
- `ZRANGEBYRANK` / `ZRANGE` to get top N
- `ZRANK` for user's current rank

### Rate Limiting

- `INCR` on request key; check against limit N
- `EXPIRE` to reset window after W seconds
- If count > N → wait; if ≤ N → proceed

### Proximity Search (Geospatial)

- `GEOADD` to add coordinates
- `GEOSEARCH FROMLONLAT BYRADIUS` for nearby queries
- Used in: Uber driver locations, Tinder profile proximity

### Pub/Sub (Chat, Real-Time Notifications)

- `PUBLISH channel message`
- `SUBSCRIBE channel`
- Messages NOT persisted; at-most-once delivery
- Pub/Sub clients use single connection per node (not per channel)

### Streams (Durable Queue)

- `XADD` to append events
- `XREADGROUP` / `XCLAIM` for consumer groups and work queues
- Messages persisted; unlike Pub/Sub

## Shortcomings & Remediations

**Hot Key Issues** (one key getting disproportionate traffic):
1. Add in-memory cache on clients (reduce Redis calls)
2. Store same data in multiple keys + randomize requests
3. Add read replica instances

**Memory management**: data disappears if Redis crashes → Sentinel for auto-recovery, multi-node setup, RDB snapshots to disk
