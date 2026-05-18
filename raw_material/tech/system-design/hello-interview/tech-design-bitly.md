---
title: "Hello Interview — Design: Bit.ly (URL Shortener)"
source: "https://www.notion.so/2d5afa27ec728098bb14ebdb85029603"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/System Design Case - Bit.ly (URL Shortener)]]"
---

# Design: Bit.ly (URL Shortener)

## Functional Requirements

1. Users submit a long URL → receive a shortened version
2. Users can optionally provide a custom alias and/or expiration for the shortened URL
3. Users access the original URL via the shortened URL (redirect)

## Scale

- 1 billion shortened URLs
- 100M DAU

## Key Design Considerations

### URL Shortening Strategy

- **Hash-based**: hash long URL → take first N characters of hash (MD5, SHA-256); collision handling needed
- **Counter-based**: auto-increment ID → Base62 encode (a-z, A-Z, 0-9); 7 characters = 62^7 = ~3.5 trillion URLs; no collision, but predictable/enumerable
- **Custom alias**: user-provided short code; check availability in DB before accepting

### Redirect Mechanism

- `GET /short-code` → 301 Permanent Redirect (cached by browser; no repeat server calls) or 302 Temporary Redirect (every redirect hits server; better for analytics)
- Redirect service queries URL DB → returns Location header with original URL

### Storage

- Simple key-value: `shortCode → {longURL, createdAt, expiresAt, userId}`
- Read-heavy (redirects >> shortening); read/write ratio ~100:1
- DynamoDB or Cassandra: partition by shortCode for fast lookups

### Caching

- Cache frequently accessed short codes in Redis (hot URLs get most traffic)
- CDN for edge caching of redirect responses
- LRU eviction for cache management

### Scale Calculations

- 100M DAU × 10 redirects/day = 1B reads/day ≈ 12K RPS
- 100M DAU × 0.1 shortenings/day = 10M writes/day ≈ 115 WPS
- 1B URLs × ~500 bytes/record = ~500GB total storage → manageable on single DB with replicas

### Custom Aliases

- User provides alias → check uniqueness in DB → store if available
- Rate limiting per user to prevent abuse

### Expiration

- Store `expiresAt` timestamp
- On redirect: check if expired → return 404 or redirect to expiration page
- Background cleanup job removes expired records periodically

### Analytics

- Log each redirect event: shortCode, timestamp, user-agent, IP, referrer
- Stream to Kafka → aggregate in Flink or batch process in Spark
- Store aggregated metrics in OLAP DB (ClickHouse/Redshift) for advertiser dashboards
