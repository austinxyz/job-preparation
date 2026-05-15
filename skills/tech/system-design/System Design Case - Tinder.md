---
title: System Design Case - Tinder
category: tech/system-design
tags: [system-design-case, geospatial, elasticsearch, redis, bloom-filter, cdc, feed-generation, matching]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# System Design Case - Tinder

## Knowledge Map
- 前置知识：Geospatial indexing (geohash, quadtree), ElasticSearch, Redis sorted sets, Bloom Filter, CDC, atomic operations in Redis
- 延伸话题：[[System Design Case - Yelp]] (geospatial + ElasticSearch), [[System Design Case - Instagram]] (feed pre-computation), [[System Design Case - Post Search]] (Redis sorted sets)
- 管理关联：

## Core Concepts

- **ElasticSearch for geospatial profile search**: User profile queries combine location (geo_distance), age range, and interests simultaneously. ElasticSearch's compound query support handles this natively; a standard relational DB with separate indexes on each field degrades under multi-criteria filtering.
- **CDC to sync profiles to ElasticSearch**: Profile updates go to the primary User Profile DB first; CDC propagates changes to ElasticSearch. This keeps the write path simple while providing a search-optimized read replica.
- **Redis atomic operations for match detection**: Redis is single-threaded, making set membership checks and insertions atomic without locks. The match check (`is targetUser's set ∋ userId?`) and the reciprocal insert happen atomically, preventing the race condition where two simultaneous mutual likes both create match records.
- **Pre-computed recommendation stack via cron job**: Computing a personalized geo+age+interest-filtered stack in real time on every `GET /matches` is expensive. Instead, a cron job pre-computes stacks and stores them in Redis cache. The User Search Service hits cache first; a cache miss falls back to ElasticSearch.
- **Two-tier swipe history filtering**: Small swipe history → check Redis set directly (fast). Large swipe history → use a Bloom Filter (probabilistic data structure). Bloom Filters guarantee no false negatives (never show a swiped profile) but allow rare false positives (occasionally skip an un-swiped profile), which is an acceptable UX trade-off given the large pool of potential matches.
- **Periodic eviction of old swipe data from Redis**: Swipe history in Redis grows indefinitely. A background job moves old swipes to persistent Swipe DB, keeping Redis memory bounded. The Bloom Filter is rebuilt from the persistent store as needed.
- **Redis cluster sharding by userId**: Each user's swipe set and recommendation cache is isolated to one shard, enabling horizontal scaling while keeping per-user atomicity.

## Key Questions

**Q: Why use Redis atomic operations for match detection instead of a DB transaction?**
Answer framework: A DB transaction for match detection requires two reads and potentially two writes (check if targetUser liked user, create match record). Under high concurrency, two simultaneous mutual likes could both pass the "no match yet" check before either writes. Redis is single-threaded — its set operations are inherently atomic, making the check-and-set pattern race-free without distributed locking overhead.

**Q: What is a Bloom Filter and why is it appropriate for swipe history filtering?**
Answer framework: A Bloom Filter is a probabilistic data structure that answers "is X in this set?" with guaranteed no false negatives (if it says "not seen," it's correct) and small false positive rate (occasionally says "seen" for an unseen item). For Tinder, a false positive means a user occasionally misses a potential match — acceptable given millions of profiles. A false negative (showing a swiped profile) is the unacceptable case, and Bloom Filters prevent this. Memory is O(n) with a much smaller constant than storing the full set.

**Q: How does the pre-computed recommendation stack handle profile changes (e.g., user updates location)?**
Answer framework: The cron job runs periodically to refresh stacks. For real-time accuracy, the profile update also triggers an async refresh for affected users' caches (or the cache entry is invalidated). The fall-back to ElasticSearch live query handles cache misses after invalidation. The trade-off is slight staleness vs. low-latency feed delivery.

**Q: How do you scale geospatial queries to hundreds of millions of users?**
Answer framework: ElasticSearch's geospatial index (geohash/quadtree) partitions users by location into cells. A radius search becomes a set of cell lookups. For extreme scale, shard ElasticSearch by geographic region, keeping nearby-user data co-located for efficient geo queries. CDN-style geographic routing ensures users query the shard closest to their location.

**Q: How does the reconciliation process work for match data consistency between Redis and DB?**
Answer framework: The reconciliation process periodically reads match records from the DB match table and compares them to what Redis shows as mutual likes. Discrepancies (Redis shows mutual like but no DB match record, or vice versa) are resolved by writing the authoritative state to the DB. This handles rare edge cases where the match creation step succeeded in Redis but failed to commit to DB.

**Q: Why pre-compute stacks with a cron job rather than computing on demand per request?**
Answer framework: Real-time computation requires: geo query (ElasticSearch), age/interest filter, deduplication against swipe history. For a user with 10K nearby profiles, this is non-trivial. At scale with millions of active users all requesting feeds concurrently, on-demand computation creates an ElasticSearch hotspot. Pre-computation amortizes this cost, and the slight staleness (stack computed minutes ago) is acceptable for a dating app.

**Q: How would you handle very densely populated areas (e.g., NYC) where millions of users are within a small geo radius?**
Answer framework: The ElasticSearch geo query returns too many candidates. Solutions: (1) increase specificity of the preference filter (stricter age range, interests); (2) add a relevance score beyond proximity (common connections, interests); (3) sample from the candidate set rather than sorting all candidates. The pre-computed stack can apply these additional filters at cron time rather than at query time.

## Summary

Tinder combines geospatial profile discovery with a real-time match system. The key insight is that these are two separate problems with different latency and consistency requirements. Feed generation is latency-sensitive and can tolerate slight staleness — hence pre-computation. Match detection is correctness-sensitive (can't miss a mutual like) and must be atomic — hence Redis.

The non-obvious design choices are: (1) using Redis set atomicity instead of DB transactions for match detection — avoiding lock contention at high swipe volume; (2) Bloom Filter for swipe history deduplication — trading a small false positive rate for O(1) lookup at any history size; (3) two-tier approach (Redis for small history, Bloom Filter for large) rather than picking one solution for all users.

What interviewers are really testing: the ability to make principled data structure choices (Bloom Filter), understand when Redis atomicity replaces DB transactions, and separate the feed generation problem (throughput/latency) from the match detection problem (correctness/atomicity).

## Key Terms

**Technologies**
- `ElasticSearch` · `Redis` · `Bloom Filter` · `CDC` · `DynamoDB/PostgreSQL`

**Patterns**
- `atomic check-and-set` · `pre-computed feed` · `two-tier deduplication (Redis + Bloom Filter)` · `CDC for search index sync` · `cron-based pre-computation`

**Decision Points**
- `Redis atomic ops vs DB transaction for match detection` · `Bloom Filter vs full set for swipe history` · `pre-computed vs on-demand feed` · `geohash vs quadtree`

## Raw Material
- [[raw_material/tech/system-design/hello-interview/case-tinder.md]]
