---
title: System Design Case - Yelp
category: tech/system-design
tags: [system-design-case, geospatial, elasticsearch, cdc, full-text-search, optimistic-locking, reviews]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# System Design Case - Yelp

## Knowledge Map
- 前置知识：Geospatial indexing (geohash, quadtree), ElasticSearch bool queries, CDC (Change Data Capture), optimistic locking, composite primary keys
- 延伸话题：[[System Design Case - Tinder]] (geospatial + ElasticSearch), [[System Design Case - Post Search]] (search indexing patterns)
- 管理关联：

## Core Concepts

- **Geospatial index as the core read path**: Location-based search is the primary query. The Business DB needs a geospatial index (geohash or quadtree) to efficiently answer "businesses within X km of point P" without full table scans.
- **ElasticSearch for complex multi-criteria queries**: When users combine location + category + name keywords + rating filters, a relational DB with multiple indexes struggles. ElasticSearch natively handles compound queries via `bool` with `must`/`should`/`geo_distance` clauses.
- **CDC to sync to ElasticSearch**: Rather than dual-write, CDC captures changes from the Business DB and streams them to ElasticSearch. This keeps the search index eventually consistent without complicating the write path. Slight lag is acceptable for a review system.
- **Optimistic locking for concurrent rating updates**: The `totalReviewNumber` field acts as a version counter. A rating update computes the new average and conditionally writes only if the version hasn't changed. This avoids distributed locks while handling concurrent reviews safely.
- **Composite primary key to enforce one-review-per-user**: `(creator, businessId)` as composite key in the reviews table makes duplicate review detection a DB constraint rather than application logic — works across all service instances without coordination.
- **Buffer + batch for high-volume review ingestion**: Under write spikes (popular restaurants, viral moments), buffering reviews and batch-recalculating ratings reduces DB write frequency significantly, trading slight staleness of average for write stability.
- **Redis cache for hot search results**: Frequently searched queries (e.g., "pizza in downtown SF") can be cached with short TTL in Redis, reducing ElasticSearch load for popular searches.

## Key Questions

**Q: Why add ElasticSearch when you already have a relational DB with indexes?**
Answer framework: Relational DBs handle single-column or simple compound queries well but struggle with simultaneous full-text search + geospatial filter + rating sort. ElasticSearch was built for compound search; its `bool` query engine scores and filters across multiple dimensions natively. The trade-off is operational complexity and eventual consistency via CDC.

**Q: How does the system prevent two users from both submitting a review for the same business at the same time?**
Answer framework: Composite primary key `(creator, businessId)` in the reviews table enforces uniqueness at the DB layer. Any duplicate attempt raises a constraint violation; the service catches it and converts the operation to an update instead. No application-level deduplication needed.

**Q: What happens if the CDC pipeline from Business DB to ElasticSearch falls behind?**
Answer framework: Search results may temporarily show stale data (e.g., old ratings, missing new businesses). This is acceptable for Yelp — a user searching for "coffee shops" can tolerate data that's seconds to minutes stale. If freshness is critical, you can reduce CDC lag by tuning batch size and flush intervals, or by doing a synchronous dual-write for the most critical fields.

**Q: How do you calculate average rating accurately under concurrent review submissions?**
Answer framework: Optimistic locking using `totalReviewNumber` as version. Compute new average with the formula `(currentRating * totalReviewCount + newRating) / (totalReviewCount + 1)`, attempt update where `totalReviewCount = [read value]`. On conflict, re-read and retry. For very high volume, buffer reviews and batch-recalculate.

**Q: How would you handle geospatial queries as the business dataset grows to 100M+ locations?**
Answer framework: Geohash or quadtree index partitions space into buckets; a radius query becomes a set of bucket lookups rather than a distance scan of every record. ElasticSearch's `geo_distance` filter uses this internally. For extreme scale, pre-compute geohash cells and shard the index by geographic region.

**Q: What's the difference between using geohash and quadtree, and when would you choose each?**
Answer framework: Geohash divides Earth into a fixed grid of cells at multiple precision levels — easy to implement, good for uniform distributions. Quadtree recursively subdivides space until each cell has few enough points — better for non-uniform distributions (urban vs. rural density). ElasticSearch uses geohash internally; PostGIS uses r-tree variants. For an interview, either is acceptable with a clear explanation of the trade-off.

**Q: Why is the `businessId` indexed in the review table rather than just relying on joins?**
Answer framework: The access pattern is "given a businessId, return all its reviews paginated." Without an index on `businessId`, this requires a full table scan as the review table grows. A secondary index on `businessId` makes this O(log n) lookup, critical for popular businesses with thousands of reviews.

## Summary

Yelp's core challenge is multi-criteria local search: users filter by location, category, name, rating, and hours simultaneously. A straightforward relational DB with B-tree indexes handles simple lookups but degrades on compound queries. The design pivots on adding ElasticSearch as a search-optimized read replica, kept in sync via CDC — this separates the write-optimized storage path from the query-optimized search path.

The non-obvious design choice is treating average rating as a derived field with its own optimistic concurrency mechanism rather than computing it on every read from raw reviews. This is a classic denormalization trade-off: slightly more complex writes (with retry logic) in exchange for O(1) rating reads. The composite primary key for reviews is a clean example of pushing business rules (one review per user per business) into the DB constraint layer, avoiding distributed application-level coordination.

The progression from simple relational queries to ElasticSearch is the key design arc interviewers want to see: start simple, identify the compound query bottleneck, introduce the right tool, and explain the consistency implications of adding a second store.

## Key Terms

**Technologies**
- `ElasticSearch` · `geohash` · `quadtree` · `CDC (Change Data Capture)` · `Redis`

**Patterns**
- `optimistic locking` · `CDC sync` · `composite primary key constraint` · `buffer + batch writes` · `read replica for search`

**Decision Points**
- `relational DB vs ElasticSearch for search` · `geohash vs quadtree` · `optimistic lock vs pessimistic lock for rating` · `CDC vs dual-write for sync`

## Raw Material
- [[raw_material/tech/system-design/hello-interview/case-yelp.md]]
