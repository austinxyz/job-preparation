---
title: System Design Case - Local Delivery
category: tech/system-design
tags: [system-design-case, geospatial, postgis, acid-transactions, redis, inventory, sharding]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# System Design Case - Local Delivery

## Knowledge Map
- 前置知识：PostGIS, geohashing, ACID transactions, serializable isolation, PostgreSQL read replicas, Redis caching, horizontal sharding
- 延伸话题：delivery route optimization, real-time driver tracking, inventory forecasting, warehouse management systems, same-day delivery SLAs
- 管理关联：

## Core Concepts

- **PostGIS for Geospatial Fulfillment Center Lookup**: PostgreSQL extension providing spatial indexes and functions. `ST_DWithin` (distance-based filter) and `ST_Distance` (precise distance calculation) operate on indexed geography columns. More expressive than Redis geospatial for complex spatial queries (polygon containment, driving distance vs. radius).
- **Two-Stage Availability Query (Nearby + Inventory)**: Stage 1: Nearby Service finds fulfillment centers within the geographic constraint (radius or delivery window). Stage 2: Inventory Service queries Inventory DB for item availability across only those centers. This avoids scanning all inventory for all centers globally.
- **Estimation Time Service for 1-Hour Window**: Pure Euclidean/geographic distance doesn't account for traffic. A third-party API (Google Maps Distance Matrix) calculates actual driving time from fulfillment center to customer address, considering real-time traffic. Only centers that can deliver within 1 hour pass the filter.
- **PostgreSQL ACID Transaction with Serializable Isolation**: Order placement must atomically verify inventory AND decrement it. Serializable isolation prevents two concurrent orders from both seeing available inventory and both decrementing — preventing oversell. The transaction: `SELECT FOR UPDATE` → verify → `UPDATE inventory` → commit. Rollback on any failure.
- **Redis Cache with Differentiated TTL**: Inventory data changes frequently (short TTL, e.g., 60s). Fulfillment center metadata (location, hours) changes rarely (long TTL, e.g., 1h or until invalidated). Using different TTLs for different data volatility reduces both cache miss rate and stale data risk.
- **Sharding by centerId + Lookup Table**: Inventory DB is sharded by fulfillment center ID. A lookup table maps `centerId → DB instance`. The Availability Service consults this lookup table to aggregate inventory from the correct DB instances for a given set of nearby centers. Avoids cross-shard joins.
- **Geohash-Based Cache Key for Nearby Centers**: Nearby Service caches fulfillment center lists with geohash prefix as cache key. Small location changes (within the same geohash cell) hit the same cache entry. Coarser geohash = larger cells = higher cache hit rate, but less precision. Tunable based on fulfillment center density.

## Key Questions

**Q: How do you find which fulfillment centers can deliver a specific item to a customer within 1 hour?**
Answer framework: Three-stage pipeline: (1) Nearby Service uses PostGIS `ST_DWithin` to find all fulfillment centers within ~60 miles of the customer (geographic filter). (2) Estimation Time Service calls Google Maps API to compute actual driving time from each candidate center to the customer address, filtering to those ≤ 60 minutes. (3) Inventory Service queries Inventory DB for item availability at the filtered centers.

**Q: Two customers simultaneously order the last unit of an item. How do you prevent overselling?**
Answer framework: PostgreSQL ACID transaction with serializable isolation. The transaction uses `SELECT ... FOR UPDATE` on the inventory row (row-level lock), verifies quantity is sufficient, decrements it, and commits. The second concurrent transaction will wait for the first to release its lock. If the first depletes inventory to zero, the second transaction finds 0 quantity and rolls back, returning "out of stock" to the second customer.

**Q: Inventory lookups need to be fast. The database is getting overloaded. What do you do?**
Answer framework: Multi-layer: (1) Redis cache with short TTL for inventory counts (slight staleness acceptable for browsing, not for ordering). (2) PostgreSQL read replicas for inventory queries (eventual consistency OK for availability checks; ACID transaction on primary for actual order placement). (3) Shard Inventory DB by centerId; lookup table routes queries to the correct shard. (4) Nearby Service caches fulfillment center lists by geohash prefix — reduces Nearby lookups.

**Q: Why use PostGIS instead of Redis geospatial for this use case?**
Answer framework: Redis `GEORADIUS` is fast but limited to radius-based queries. PostGIS supports more complex spatial operations: polygon-based delivery zones, driving distance (not straight-line), `ST_DWithin` with proper geographic accuracy. The trade-off is that PostGIS queries go to a database (I/O bound) while Redis is in-memory. For this use case, fulfillment center lists are small (hundreds of centers), so PostGIS performance is adequate and geohash caching mitigates latency.

**Q: How does the geohash cache key work and what are the trade-offs?**
Answer framework: The customer's lat/lng is converted to a geohash string (e.g., 6-character = ~1.2km precision). The cache key is the geohash prefix. Two customers in the same geohash cell get the same cached list of nearby centers — no cache miss for nearby queries. Trade-off: coarser geohash (fewer characters) = larger cells = higher hit rate but less precise matching. Fine-tune based on fulfillment center density. Edge case: customer near a geohash boundary might miss a nearby center — handle with slight radius expansion.

**Q: How would you handle a fulfillment center going offline mid-day?**
Answer framework: Nearby Service's cache TTL ensures eventual consistency (cache expires and the center drops from results). For immediate response: event-driven cache invalidation when center status changes (webhook from center management system → invalidate cache). Inventory DB queries to that shard return errors → Availability Service treats that center as unavailable. Order Service marks orders from that center as failed and triggers rerouting logic.

## Summary

A local delivery service must answer "can item X be delivered to my address within 1 hour?" and process orders with inventory correctness guarantees. The design must handle the dual challenge of geospatial queries (which fulfillment centers are close enough?) and ACID-compliant inventory management (no overselling).

The geographic filtering is a two-stage funnel: geographic proximity (PostGIS radius filter) → actual delivery time (Google Maps ETA). The second stage is the non-obvious addition that differentiates a naive distance-based filter from a production design: a center might be geographically close but unreachable in time due to traffic or geography.

Order placement uses serializable isolation — the strongest PostgreSQL isolation level — specifically to prevent the "last unit" race condition. This is stronger than the default "read committed" isolation and has a throughput cost, but correctness is non-negotiable for inventory. The caching layer (Redis with differentiated TTLs, geohash cache keys, read replicas) handles the read-heavy browsing workload without putting it on the ACID transaction path.

## Key Terms

**Technologies**
- `PostGIS` · `ST_DWithin` · `Redis` · `PostgreSQL` · `Google Maps Distance Matrix API` · `Geohashing`

**Patterns**
- `Two-Stage Geographic Funnel` · `ACID Transaction with Serializable Isolation` · `Differentiated Cache TTL` · `Sharding by centerId + Lookup Table` · `Geohash Cache Key`

**Decision Points**
- `PostGIS vs. Redis GEORADIUS` · `serializable vs. read-committed isolation` · `short vs. long TTL for different data types` · `shard by centerId vs. by region`

## Raw Material
- [[raw_material/tech/system-design/hello-interview/case-local-delivery.md]]
