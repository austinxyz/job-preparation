---
title: System Design Case - Uber
category: tech/system-design
tags: [system-design-case, geospatial, redis, distributed-locking, kafka, matching, real-time]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# System Design Case - Uber

## Knowledge Map
- 前置知识：Redis geospatial (GEORADIUS), geohashing, distributed locking (SETNX), Kafka partitioning, A*/Dijkstra algorithms, push notifications (APN)
- 延伸话题：surge pricing, driver earnings/payments, trip history, safety features (share ride), ETA accuracy, multi-modal transport
- 管理关联：

## Core Concepts

- **Redis Geospatial for Driver Location**: Drivers send location updates at variable intervals (active: every 30s, idle: every 5 min). Redis stores each driver's location as a geohash. `GEORADIUS` command finds all drivers within a specified radius in a single O(N+log M) query. In-memory Redis handles millions of concurrent location reads efficiently.
- **Redis SET NX EX for Driver Lock (One Ride Per Driver)**: When Matching Service selects a driver, it atomically sets `key=driverId, value=rideRequestId` with TTL. If the driver is already matched (key exists), skip. If driver doesn't respond within TTL, the key auto-expires and the driver is available again. Local in-memory cache as first-check layer reduces Redis calls.
- **Fare Estimation with Road Graph**: Ride Service calls a Fare Estimation Service that uses A* or Dijkstra on road graph data (from Google Maps API) plus traffic conditions to compute estimated travel time. Fee = distance-based rate + time-based rate. Results cached in Ride DB.
- **Kafka Partitioned by Geo Region**: Ride requests are queued in Kafka, partitioned by geographic region (not hash of rideId). This is critical because proximity search is location-based — all matching for a given area must happen on the same Matching Service instance (or at least the same partition) to avoid cross-partition location joins.
- **Driver Notification via APN**: After matching, the Matching Service pushes a notification to the driver's mobile app (Apple Push Notification service or Firebase). Driver accepts/rejects via the app, which updates the Ride DB status. The async nature of mobile push is handled by the TTL on the Redis lock.
- **Redis Sentinel + Disk Snapshots for Location Durability**: Location data loss on crash is acceptable (drivers resend updates every 30s), but complete cluster failure is not. Redis Sentinel provides auto-failover. Periodic snapshots to disk provide recovery point. Multiple replica nodes prevent single-node data loss.
- **Circuit Breaker for Peak Demand**: During surge events, Kafka queue depth grows. Matching Service scales based on queue depth. Extreme spikes trigger circuit breaker: requests stored in secondary storage; resume when capacity recovers. Circuit breaker prevents cascading failure into the DB.

## Key Questions

**Q: How do you efficiently find all available drivers within 5 miles of a rider?**
Answer framework: Redis geospatial index. Each driver update calls `GEOADD` to update their position. On ride request, `GEORADIUS` returns all driver keys within the specified radius. Filter by availability status. Sort by distance, rating, and driver status. This is an in-memory operation — no database query needed for the proximity search itself.

**Q: Two riders request rides and both get matched to the same driver. How do you prevent this?**
Answer framework: Redis SET NX EX (atomic set-if-not-exists with TTL). When the Matching Service selects a driver, it atomically writes `driverId → rideRequestId` with a TTL. Only the first caller succeeds — the second call finds the key exists and moves to the next available driver. If the driver doesn't respond, TTL expires and the driver becomes available again automatically.

**Q: Why partition Kafka by geo region rather than by rideId?**
Answer framework: Proximity search is inherently geographic. If ride requests for the same area go to different Matching Service instances, each instance would need to query location data across all regions for every match — expensive cross-partition joins. Geo-partitioning collocates ride requests with nearby driver data, making matching a local operation per Matching Service instance.

**Q: How do you handle the driver location DB under high write volume (millions of active drivers)?**
Answer framework: Redis is specifically chosen over a relational DB here. In-memory storage handles the high write rate. Location data is ephemeral — 30s staleness is acceptable (active drivers re-report frequently). Redis GEORADIUS is an efficient indexed spatial query, not a full table scan. For true durability, Redis Sentinel + periodic snapshots provide acceptable durability at this data's freshness requirements.

**Q: Walk through the full flow from ride request to driver pickup.**
Answer framework: (1) Rider submits request → Ride Service creates Ride record (status=requested). (2) Ride request enqueued to Kafka (geo-partitioned). (3) Matching Service dequeues → `GEORADIUS` for nearby available drivers → sort by distance/rating → attempt Redis lock on best driver. (4) Lock acquired → send APN push to driver. (5) Driver accepts → update Ride status in DB, remove Redis lock. (6) Driver location tracked in Redis until trip completes.

**Q: How do you compute surge pricing?**
Answer framework: Surge is a multiplier on base fare. Requires real-time supply/demand ratio per geographic area. Supply: count active drivers from Redis geospatial index. Demand: count pending ride requests from Kafka queue depth by geo partition. Surge multiplier = f(demand/supply). Pre-computed per region on a short interval (every 1-5 min). Cached in Redis for fast read. Display to rider before confirmation.

## Summary

Uber's core challenge is real-time geospatial matching: connecting a rider to the nearest available driver within seconds, at scale (millions of concurrent drivers globally). Functional requirements: fare estimation, ride request, driver matching, location tracking, and trip status updates.

The architectural backbone is Redis for two distinct purposes: geospatial driver tracking (`GEORADIUS` for proximity queries) and distributed locking (`SET NX EX` to prevent double-matching a driver). These two uses are often conflated — they're separate Redis use cases solving separate problems. Location storage requires high write frequency and tolerates some data loss (drivers re-report); the lock requires atomicity and automatic expiry.

The Kafka partitioning by geo region is the non-obvious architectural decision. Matching is a location-aware operation — co-locating ride requests with matching logic for the same geographic area avoids expensive cross-partition joins. This pattern (partition by the dimension that determines co-location) generalizes to other geospatial systems. The interview tests whether candidates understand why geo-partitioning beats rideId hashing here.

## Key Terms

**Technologies**
- `Redis GEORADIUS` · `Redis SET NX EX` · `Kafka` · `APN / Firebase` · `Redis Sentinel` · `A* / Dijkstra`

**Patterns**
- `Geospatial Distributed Lock` · `Geo-Partitioned Queue` · `Variable-Frequency Location Updates` · `Circuit Breaker for Demand Spikes`

**Decision Points**
- `Redis vs. PostGIS for location` · `geo-partition vs. rideId-partition in Kafka` · `TTL duration for driver lock` · `push notification vs. polling for driver`

## Raw Material
- [[raw_material/tech/system-design/hello-interview/case-uber.md]]
