---
title: Hello Interview — Case: Tinder (Dating App)
source: "https://www.notion.so/1f3afa27ec72801d98e0c668a6d681ec"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/System Design Case - Tinder]]"
---

# Case: Tinder (Dating App)

## Key Design Questions & Answers

### Create Profile & Set Preferences

1. `POST /profiles` → User Profile Service
2. Creates UserProfile in DB: ageRange, interests, interestGender, maxDistance
3. Returns profile to user

### Recommended Match Stack

1. `GET /matches?location&page` → User Search Service (gets userId from JWT/session)
2. Fetches user's profile (maxDistance, interests, ageRange, gender)
3. Queries User Profile DB (user table + location table) with filters
4. ViewHistory table filters out previously viewed profiles
5. Returns paginated list of recommended users

### Swipe (Left/Right) & Match Detection

1. `POST /swipe` (targetUserId, action=like/unlike) → Swipe Service
2. Swipe Service: query Swipe table for `(userId, targetUserId)`, update or create record
3. Check if `targetUser` already liked `userId` (mutual like) → if yes, create Match record
4. If matched: return match to current user + send APN notification to targetUser

### Fast + Consistent Match Processing

**Redis Atomic Operations**:
1. Redis cache: `userId → Set<likedTargetUserIds>` (single-threaded Redis = atomic operations)
2. On right swipe: atomically add targetUserId to user's set; check if targetUser's set contains userId
3. If mutual like: create Match record in DB + notify both users
4. Redis cluster: shard by userId
5. Periodically move old swipe data from Redis to persistent Swipe DB (memory management)
6. **Reconciliation process**: compares Redis match data with DB match table periodically to fix inconsistencies

### Low Latency Feed Generation

1. **ElasticSearch** as secondary DB: sync user profile + location via CDC
2. ElasticSearch geospatial index (geohash/quadtree) for fast proximity queries
3. Pagination to reduce response size
4. **Cron job** pre-computes recommended stacks and stores in Redis cache → User Search Service checks cache first, falls back to ElasticSearch if cache miss

### Avoiding Previously Swiped Profiles

**Two-tier approach**:
1. Small swipe history: check Redis `userId → targetUserList` directly to filter
2. Large swipe history: **Bloom Filter** — generates fingerprint for user's swipe history
   - Lookup: constant-time regardless of history size; much less memory than full list
   - False positive (may skip un-swiped profile): acceptable given large pool of profiles
   - False negative: never shows a definitely-swiped profile (correct behavior)
   - Tune false positive rate by adjusting bloom filter parameters
