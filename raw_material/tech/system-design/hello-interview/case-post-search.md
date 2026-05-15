---
title: Hello Interview — Case: Post Search (Inverted Index)
source: "https://www.notion.so/1f4afa27ec7280e8b996e4f553347aed"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/System Design Case - Post Search]]"
---

# Case: Post Search (Inverted Index)

## Key Design Questions & Answers

### Create Posts & Likes

1. Post Service + Like Service store to primary Post DB
2. Events published to Kafka post queue
3. Ingestion Service consumes queue: splits post into keywords, builds `keyword → Set<postId>` inverted index, stores in Inverted Index DB

### Keyword Search

1. User queries via Search Service → API Gateway
2. Search Service queries Inverted Index DB by keyword → returns matching postIds
3. Fetches post details from primary DB for those postIds

### Sort by Recency and Like Count

**Redis Sorted Sets**:
1. Two sorted sets per keyword: one sorted by `creationTime`, one by `like_count`
2. Ingestion Service updates both sets when processing new posts/likes
3. Search Service returns appropriate sorted set based on sort parameter

### Scale to Trillions of Posts

1. **Kafka** for post queue: partitioned by postId, easy horizontal scaling
2. Multiple Ingestion Service instances as consumer group
3. Multiple Redis instances: keyword as partition key
4. **CDN** caches search results (short TTL since results change frequently)
5. Search Service first checks search result cache in Redis; CDN for global edge caching

### Hot Keywords (Millions of Posts)

1. CDN + search result cache with short TTL
2. Ingestion: aggregate likes over 30s periods → reduce write frequency to inverted index
3. **Exponential like_count update**: only update sorted set at powers of 2 (1, 2, 4, 8…) → reduces write load
4. **Two-phase search**: fetch 2x target size from Redis (approximate like_count), then query primary DB for exact like_count, re-sort → return top N
5. For most popular keyword: `keyword+seq` → distribute across multiple Redis instances → merge in Search Service

### Multi-Keyword Queries ("taylor AND swift")

1. **Bigrams**: index consecutive word pairs (e.g., "taylor swift" as single keyword)
2. Search for "taylor swift" → use bigram directly
3. Boolean operations: AND → use bigram; OR → merge results of individual keywords
4. N-grams for longer phrases, but selective: only store meaningful n-grams (noun+verb combinations)

### N-gram Storage Optimization

1. Prioritize noun/verb combinations; exclude prepositions/articles
2. Periodic cleanup: remove n-grams whose postId count hasn't grown for 1 hour
3. Add n-grams based on actual user search queries: if keyword searched N times (N=10), add to meaningful n-grams set

### Storage Optimization

1. Hot keywords in Redis; cold keywords (few postIds, rarely searched) → migrate to S3 cold cache
2. Cron job checks keyword temperature; migrates cold keywords to S3
3. Search Service: check search result cache → Redis inverted index → S3 cold cache (higher latency, rarely accessed)
4. Promote: search service tracks query frequency; popular cold keywords promoted back to Redis
