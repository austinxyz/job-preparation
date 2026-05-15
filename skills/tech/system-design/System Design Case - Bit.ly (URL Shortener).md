---
title: System Design Case - Bit.ly (URL Shortener)
category: tech/system-design
tags: [system-design-case, url-shortener, base62, hashing, redis-cache, cdn, dynamodb, analytics, read-heavy]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# System Design Case - Bit.ly (URL Shortener)

## Knowledge Map
- 前置知识：Base62 encoding, MD5/SHA-256 hashing, Redis LRU cache, CDN, HTTP 301 vs 302 redirects, DynamoDB/Cassandra key-value patterns, Kafka + Flink for analytics
- 延伸话题：[[System Design Case - Ads Click Aggregation]] (click analytics pipeline), [[System Design Case - Post Search]] (CDN caching)
- 管理关联：

## Core Concepts

- **Counter-based Base62 encoding is the canonical approach**: Auto-increment ID → Base62 encode (a-zA-Z0-9). 7 characters = 62^7 ≈ 3.5 trillion unique codes — more than enough for 1 billion URLs. No collision handling needed (unlike hash-based). Trade-off: sequential IDs are enumerable/guessable, which may be a security concern for private URLs.
- **Hash-based approach needs collision handling**: Hash the long URL (MD5/SHA-256), take the first 7 characters. Same long URL always produces same short code (idempotent). Collision probability is low but non-zero; on collision, append a counter or use a secondary hash and retry.
- **301 vs 302 redirect is a critical trade-off**: 301 Permanent Redirect — browser caches it, subsequent visits skip the server entirely (better for CDN/browser cache hit rate, lower server load). 302 Temporary Redirect — every redirect hits the server (worse performance, but enables accurate per-redirect analytics and supports expiration checks). For analytics-heavy use cases like Bit.ly, 302 is the right choice.
- **Read-heavy workload drives the caching strategy**: 100M DAU × 10 redirects/day ≈ 12K RPS reads vs. ~115 WPS writes (100:1 read/write ratio). Redis LRU cache for hot short codes (Pareto: top 20% codes drive 80% of traffic). CDN at edge for geographically distributed caching of redirect responses.
- **DynamoDB (or Cassandra) as the primary store**: Simple key-value access pattern (`shortCode → longURL + metadata`). Partition by shortCode for O(1) lookups. DynamoDB scales horizontally without manual sharding. 1B URLs × ~500 bytes = ~500GB — manageable with replicas and on-demand capacity.
- **Scale numbers**: 1B URLs total, 100M DAU, ~12K redirect RPS, ~115 write RPS, ~500GB storage. These numbers make the case for a horizontally scalable NoSQL store (not a relational DB) and aggressive caching.
- **Analytics pipeline mirrors Ads Click**: Log each redirect event (shortCode, timestamp, user-agent, IP, referrer) → Kafka → Flink or Spark aggregation → ClickHouse/Redshift for dashboard queries. This is the exact same pipeline as Ads Click Aggregation at smaller scale.

## Key Questions

**Q: Why choose counter-based Base62 over hash-based shortening?**
Answer framework: Counter-based has zero collision probability (each ID is unique by construction), simpler implementation (no collision retry logic), and the encoded IDs are compact (7 chars for 3.5 trillion URLs). Hash-based has a natural benefit: same long URL always maps to the same short code (request idempotency). For most systems, counter-based is preferred unless idempotency is a hard requirement. Security concern: counter-based IDs are enumerable — add access control or randomize if needed.

**Q: When should you use 301 vs 302 for the redirect response?**
Answer framework: 301 (Permanent): browser and CDN cache the mapping indefinitely. Users get sub-millisecond redirects from cache; server sees zero traffic for cached URLs. Bad for analytics (can't count visits) and for URLs that might expire. 302 (Temporary): every redirect hits the redirect server. Enables accurate click counting, expiration checks, and A/B testing. Bit.ly uses 302 because analytics is the core business value. Choose based on whether analytics or performance dominates.

**Q: How does the system handle custom aliases?**
Answer framework: The user provides a desired alias. The service checks DynamoDB for existence of that alias as a key. If available, it stores the mapping and returns the alias. If taken, it returns an error (the user must try another alias or accept a generated one). Rate limiting per user prevents abuse (bulk alias reservation). Aliases occupy the same key space as generated codes — no separate namespace needed.

**Q: How does expiration work without a full table scan?**
Answer framework: Store `expiresAt` timestamp in the record. On each redirect request, check if `expiresAt < now` — if expired, return 404. A background cleanup job (cron) periodically scans for records where `expiresAt < now` and deletes them. DynamoDB's TTL feature natively handles this: set TTL on the record and DynamoDB auto-deletes expired items within 48 hours (eventual deletion, not guaranteed-on-time). For immediate expiration accuracy, the check-at-read-time approach is needed.

**Q: How would you design the system to prevent the same long URL from generating multiple short codes?**
Answer framework: Add a secondary index on `longURL` → `shortCode`. Before creating a new short code, check this index. If a mapping exists, return the existing short code (idempotent). The trade-off: secondary index adds storage and write overhead. For Bit.ly's use case (URLs shared many times), deduplication is valuable. Alternatively, use hash-based shortening — same long URL always produces the same hash, so deduplication is free.

**Q: How do you handle traffic spikes (e.g., a viral tweet with a Bit.ly link gets 10M clicks in an hour)?**
Answer framework: Three layers of protection: (1) CDN edge caches the 302 response for a short TTL — most traffic is absorbed at the edge; (2) Redis cache handles the remaining cache-hit traffic before reaching DynamoDB; (3) DynamoDB on-demand capacity auto-scales for the DynamoDB read path. The combination means the actual DynamoDB traffic for a viral URL is minimal. For truly extreme spikes, the CDN layer is the most important defense.

**Q: Why is this a good "warm-up" system design problem, and what are interviewers looking for?**
Answer framework: URL shortener has all the components of a real system at small scale: API design, key generation strategy, storage schema, caching, and basic analytics. Interviewers assess: (1) can the candidate pick the right data structure (counter vs hash with clear trade-off analysis?); (2) do they know the 301 vs 302 trade-off?; (3) do they think through the read-heavy nature and propose caching?; (4) do they mention scale numbers and calculate storage? This problem is simple enough to finish in 30 minutes but rich enough to probe several dimensions.

## Summary

Bit.ly (URL Shortener) is a canonical warm-up system design problem. The functional requirements are simple (shorten URL, redirect URL), but the design choices are non-trivial: counter-based vs hash-based shortening, 301 vs 302 redirects, and a caching hierarchy proportional to the 100:1 read/write ratio.

The key scale insight: 12K RPS redirects at 100M DAU means this is read-dominated. The solution is cache-first: CDN for geographic distribution, Redis LRU for hot codes, DynamoDB only for cold codes and write path. With this hierarchy, the DynamoDB read load is a small fraction of total redirect traffic.

The 301 vs 302 decision deserves more emphasis than most candidates give it: 301 optimizes for performance (browser/CDN caching), 302 optimizes for analytics accuracy (every redirect logged). For a business that monetizes analytics (like Bit.ly), 302 is non-negotiable. This is an example of a business requirement (analytics accuracy) driving a technical protocol choice.

## Key Terms

**Technologies**
- `Base62 encoding` · `MD5/SHA-256` · `DynamoDB / Cassandra` · `Redis (LRU)` · `CDN` · `Kafka` · `Flink / Spark`

**Patterns**
- `counter-based ID generation` · `hash-based shortening` · `301 vs 302 redirect` · `LRU cache for hot codes` · `background expiration cleanup` · `secondary index for deduplication`

**Decision Points**
- `counter-based vs hash-based` · `301 Permanent vs 302 Temporary redirect` · `DynamoDB vs relational DB` · `CDN edge caching vs server-side caching`

**Scale Numbers**
- `1B URLs` · `100M DAU` · `~12K redirect RPS` · `~115 write RPS` · `~500GB storage`

## Raw Material
- [[raw_material/tech/system-design/hello-interview/tech-design-bitly.md]]
