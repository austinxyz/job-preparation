---
title: System Design Case - Post Search
category: tech/system-design
tags: [system-design-case, inverted-index, redis-sorted-sets, kafka, full-text-search, bloom-filter, n-grams, hot-partition]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# System Design Case - Post Search

## Knowledge Map
- 前置知识：Inverted index, Redis sorted sets, Kafka consumer groups, CDN, n-grams/bigrams, hot key problem, cold storage tiering
- 延伸话题：[[System Design Case - Ads Click Aggregation]] (Kafka + hot partition handling), [[System Design Case - Yelp]] (search indexing)
- 管理关联：

## Core Concepts

- **Inverted index as the core data structure**: Text search requires mapping keywords to the posts that contain them. The `Ingestion Service` splits posts into keywords and builds a `keyword → Set<postId>` map in an Inverted Index DB. This is the same structure underlying all major search engines.
- **Redis sorted sets for ranking**: Two sorted sets per keyword — one scored by `creationTime` (for recency sort) and one by `like_count` (for popularity sort). The Search Service returns the appropriate set based on the user's sort parameter. Redis sorted sets support O(log N) insertion and O(log N + K) range queries.
- **Kafka for decoupled async ingestion**: Posts and likes flow through Kafka (partitioned by postId). Ingestion Service instances form a consumer group, enabling horizontal scaling of the indexing pipeline independently from the write path.
- **Exponential like_count updates to reduce write load**: Only update the sorted set at powers of 2 (when a post reaches 1, 2, 4, 8 like count). This reduces sorted set write frequency by log2(N) for popular posts, without losing the ability to sort by approximate popularity.
- **Bigrams for multi-keyword queries**: Instead of computing AND/OR logic across single-keyword sets at query time, consecutive word pairs ("taylor swift") are indexed as a single keyword (bigram). This makes common phrase searches a single inverted index lookup rather than a set intersection.
- **Hot keyword partitioning**: When a keyword becomes extremely popular (millions of matching posts), its sorted set on a single Redis instance becomes a hotspot. The solution: shard the keyword as `keyword+seq` across multiple Redis instances; Search Service queries all shards and merges results.
- **Two-tier cold storage for keywords**: Active keywords live in Redis (fast, expensive). Keywords that haven't been searched recently and have few matching posts are migrated to S3 (cheap, slow). A cron job manages promotion/demotion. The Search Service has a three-tier lookup: search cache → Redis → S3.

## Key Questions

**Q: Why build a custom inverted index instead of using ElasticSearch?**
Answer framework: This case study is teaching the inverted index concept, not necessarily arguing against ElasticSearch. In practice, ElasticSearch would be the right choice for most systems. The custom inverted index in Redis is useful when you need ultra-low-latency sorted lookups (Redis in-memory vs ElasticSearch network call) and want full control over the ranking logic. The trade-off is operational complexity and lack of full-text search features.

**Q: How does the two-phase search for popular keywords work?**
Answer framework: Fetch 2x the target count from the Redis sorted set (using approximate `like_count`). Then query the primary DB for the exact like count of those candidates. Re-sort by exact count and return the top N. This handles the staleness in the sorted set (exponential updates mean some like counts are slightly stale) while keeping Redis as the primary filter to reduce DB load.

**Q: Why use bigrams instead of AND intersection across two single-keyword inverted lists?**
Answer framework: AND intersection requires fetching both postId sets and computing the intersection — O(min(|set1|, |set2|)) time. For common phrases searched millions of times, this overhead adds up. Bigrams pre-compute the intersection at index time (during ingestion). The trade-off: significantly more storage (O(n) bigrams per n-word post vs n single keywords), but O(1) query time. Selective bigram generation (noun+verb combinations, user-searched phrases) controls storage growth.

**Q: How do you handle the hot keyword problem where one keyword has billions of matching posts?**
Answer framework: Split the keyword's sorted set across multiple Redis instances using `keyword+seq` sharding. The Search Service queries all shards in parallel and merges the top-N results (a parallel merge of sorted lists). Coordinating cron jobs aggregate per-`seq` results into the unified metric.

**Q: How does the cold storage tiering work in practice?**
Answer framework: A cron job runs periodically, checking keyword access frequency and postId set size. Keywords below thresholds on both dimensions are moved from Redis to S3. On a query for a cold keyword, the Search Service falls back to S3 (accepting higher latency). If the cold keyword starts getting searched frequently, a promotion job (triggered by access frequency tracking in Search Service) moves it back to Redis.

**Q: How do you prevent the inverted index from growing stale after posts are deleted or edited?**
Answer framework: Post deletion or edit events flow through the same Kafka queue. The Ingestion Service processes delete events by removing postIds from the corresponding keyword sets. For edits, it's a remove (old keywords) + add (new keywords) operation. Redis sorted set supports O(log N) removal by member. This keeps the index consistent with the primary DB.

**Q: What's the CDN's role in a search system, and what are its limitations?**
Answer framework: CDN caches the rendered search result pages (or JSON responses) at edge nodes, so repeated identical queries (same keyword + same sort + same page) are served without hitting the Search Service. TTL is short (minutes) because results change as new posts/likes arrive. The limitation: CDN only helps for repeated identical queries. Personalized or location-specific search results can't be CDN-cached.

## Summary

Post Search teaches the inverted index pattern — the data structure behind all search systems. The design builds this from scratch with Kafka for ingestion, Redis sorted sets for ranking, and a three-tier storage hierarchy for cost management. The scale challenges (trillions of posts, hot keywords with billions of matches) drive the most interesting design decisions.

The non-obvious choices are: (1) exponential like_count updates — a clever trick to bound write frequency on popular posts to O(log like_count) updates instead of one per like; (2) bigrams for phrase search — trading storage for query-time simplicity; (3) `keyword+seq` hot partition splitting — the same pattern used in Kafka hot partition handling, applied here to Redis.

What interviewers are testing: understanding of the inverted index as a fundamental data structure, ability to handle skewed data distributions (hot keywords), and knowledge of when to trade storage for query-time efficiency (bigrams vs. intersection).

## Key Terms

**Technologies**
- `Redis sorted sets` · `Kafka` · `CDN` · `S3` · `Inverted Index DB`

**Patterns**
- `inverted index` · `bigram indexing` · `exponential update (powers of 2)` · `hot key sharding (keyword+seq)` · `three-tier storage hierarchy` · `two-phase search`

**Decision Points**
- `custom inverted index vs ElasticSearch` · `bigrams vs AND intersection` · `exponential vs per-event like updates` · `CDN vs Redis for result caching`

## Raw Material
- [[raw_material/tech/system-design/hello-interview/case-post-search.md]]
