---
title: System Design Case - Strava
category: tech/system-design
tags: [system-design-case, mobile-first, offline-sync, geospatial, redis, leaderboard, gps-tracking]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# System Design Case - Strava

## Knowledge Map
- 前置知识：GPS data handling, Vincenty formula, Redis sorted sets, conflict resolution strategies, mobile offline storage, incremental sync
- 延伸话题：route matching/segment detection, Strava KOM/QOM, social feed, heart rate + wearable data, privacy zones
- 管理关联：

## Core Concepts

- **Client-Side Distance Calculation (Vincenty Formula)**: For long-distance activities, simple Euclidean distance accumulates error. The Vincenty formula accounts for Earth's curvature and gives accurate distance for routes > a few km. Calculated on-device every 30s on batched GPS points — server only receives incremental totals, not raw recalculations.
- **Batch + Incremental GPS Sync**: Client records GPS every 5s into in-memory buffer → persists to local temp file every 3s. Every longer interval, batch uploads route data + current incremental distance to Activity Service. This reduces API call frequency and server load while keeping server data reasonably fresh.
- **Offline-First Activity Recording**: GPS points are persisted to local device storage continuously. Network connectivity is not required during the activity. On reconnection, the client batch-uploads all stored route data. Sync checkpointing (chunks of 50 points) ensures partial syncs can resume without re-sending already-synced data.
- **Conflict Resolution for Offline Syncs**: If the server has newer data for the same activity (e.g., user paused/resumed on another device), resolution strategies: version field (higher version wins), client-first (local data is authoritative during offline period), or server-first (server is source of truth). Version field is most principled for distributed editing.
- **Redis Sorted Set for Leaderboard**: `ZADD leaderboard userId totalDistance` on activity completion. `ZRANGE` gets top N. Risk: Redis data loss → reconcile service periodically reads Activity DB and reconciles Redis sorted set. At millions of users, hierarchical leaderboards: regional sorted sets → merge top N per region into global board.
- **Activity Status State Machine**: CREATED → STARTED → PAUSED → RESUMED → COMPLETED. Each PATCH call carries the new status + timestamp. Paused durations are excluded from active time calculation (sum of RESUMED - PAUSED intervals). Server stores timestamps for each transition.
- **Polling for Friend Activity**: Friend activity tracking uses polling (`GET /activities?status=inprogress&type=friend`) rather than WebSocket, intentionally keeping the server stateless. Active foreground: short poll interval. Background: longer interval. Redis cache for hot in-progress activities under high polling load.

## Key Questions

**Q: A user runs a 50km ultramarathon. Their phone GPS records 36,000 points. How do you handle storage and transmission?**
Answer framework: On-device batching: GPS recorded every 5s into memory, persisted to local file every 3s. Batch uploads at longer intervals (e.g., every 30s or 500m of movement). Incremental distance calculated on-device using Vincenty formula — server only receives the delta, not raw points for recalculation. After completion, full route is uploaded. For very long activities, reduce GPS precision for older points to manage local storage.

**Q: The user's phone loses network at mile 20. How does the system handle the offline period?**
Answer framework: GPS recording continues to local storage uninterrupted — offline doesn't affect data capture. The Activity record on the server shows the last known state. On reconnection, client detects unsynced chunks and batch-uploads them in checkpointed segments (e.g., 50-point chunks). The server reconciles the route data with the existing activity record. Conflict resolution: use client-first policy (local data during offline period is authoritative) with a version field to detect concurrent edits.

**Q: How do you accurately calculate active duration when the user pauses mid-activity?**
Answer framework: Activity status state machine tracks transition timestamps. Active duration = sum of (RESUMED_timestamp - PAUSED_timestamp) intervals, plus time since last RESUMED if currently active. Each PATCH call to change status carries the current timestamp. The server stores all transitions and computes active time on read (or materializes it on completion). Paused intervals are explicitly excluded.

**Q: How do you build a global leaderboard for total distance run this month?**
Answer framework: Redis sorted set: ZADD with userId and their monthly total distance on each activity completion. ZRANGE for top N. Monthly reset: swap the sorted set key at month boundary (keep old one for historical). Data loss mitigation: reconcile service periodically reads Activity DB aggregates and updates Redis. At scale: regional sorted sets (ZADD into region-specific keys), then merge top N per region into global board to reduce single-key contention.

**Q: A friend starts a run. How does a follower see their real-time progress?**
Answer framework: Follower's app polls `GET /activities?status=inprogress&type=friend` to discover active activities. For a specific friend's route: poll `GET /activities/:id/routes` every 5s to get latest GPS points. Redis caches hot in-progress activities. Polling keeps the server stateless — no persistent connections. For large friend lists, priority-based polling (close friends first, rate-limited).

**Q: Why use polling instead of WebSocket for friend activity tracking?**
Answer framework: Stateless server is a significant operational advantage at scale: no session affinity, simpler load balancing, easier horizontal scaling, no reconnection management. The update frequency (every 5s) is not demanding enough to justify the complexity of WebSocket connection management. Friend tracking is a secondary feature — it can tolerate 5s staleness. WebSocket would be justified if sub-second latency were required (competitive racing applications).

## Summary

Strava tracks physical activities (running, cycling) with GPS data, calculating distance/speed/duration and sharing to social features like leaderboards. The defining characteristic is mobile-first with offline capability — the system must function without network connectivity during the activity itself.

The key architectural decisions stem from the mobile-offline constraint. GPS points are persisted locally first, synced in batches. Distance calculation is done on-device (Vincenty formula) to reduce server load and allow offline accuracy. Sync uses checkpointing to allow partial resume. This client-heavy design is the non-obvious pattern — most system design defaults to server-authoritative, but activity recording must be client-authoritative during offline periods.

The leaderboard and friend-tracking features test the candidate's ability to apply known patterns (Redis sorted sets, polling) to domain-specific requirements. The non-obvious challenge is Redis data loss for the leaderboard: the reconcile service that periodically re-derives Redis state from the DB is the reliability mechanism that most candidates miss. The interview probes both the offline sync design (conflict resolution strategies) and the leaderboard scale path (regional rollup).

## Key Terms

**Technologies**
- `Vincenty Formula` · `Redis Sorted Sets` · `DynamoDB / PostgreSQL` · `GPS Batch Upload`

**Patterns**
- `Offline-First with Local Persistence` · `Incremental Sync with Checkpointing` · `Client-Side Distance Calculation` · `Hierarchical Leaderboard Rollup` · `Redis Reconcile Service`

**Decision Points**
- `client-first vs. server-first conflict resolution` · `polling vs. WebSocket for friend tracking` · `Vincenty vs. Haversine` · `GPS frequency vs. battery life`

## Raw Material
- [[raw_material/tech/system-design/hello-interview/case-strava.md]]
