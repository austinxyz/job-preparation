---
title: Hello Interview — Case: Yelp (Business Reviews)
source: "https://www.notion.so/1f0afa27ec7280a089a0c554e43db1c5"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/System Design Case - Yelp]]"
---

# Case: Yelp (Business Reviews)

## Key Design Questions & Answers

### Search for Businesses

1. `GET /businesses?conditions` (location, name, category, pagination) → Business Service
2. Business Service queries Business DB with WHERE clauses on name, category, location
3. Indexes: category index, geospatial index (geohash or quadtree), full-text search on name field
4. Returns businesses + reviews (paginated)

### View Business Details & Reviews

1. `GET /businesses/:id` → returns business details
2. `GET /businesses/:id/reviews?page&pagination` → paginated reviews
3. businessId indexed in review table for fast lookup

### Leave Reviews

1. `POST /businesses/:id/reviews` → Review Service
2. Creates review record with rating, text, creator info
3. Recalculates and updates avgRating on Business record

### Efficiently Calculate Average Rating

**Optimistic locking**:
1. Business table has `currentRating` + `totalReviewNumber` fields
2. New rating: `newRating = (currentRating * totalReviewNumber + rating) / (totalReviewNumber + 1)`
3. `totalReviewNumber` acts as version number for optimistic lock
4. Update fails if `totalReviewNumber` has changed concurrently → retry with fresh values
5. High-volume reviews: buffer reviews, batch-calculate ratings to reduce DB write frequency

### One Review Per User Per Business

1. Composite primary key on `(creator, businessId)` in reviews table
2. DB-level unique constraint prevents duplicate reviews
3. Duplicate attempt → unique constraint violation → update existing review instead
4. Constraint enforced at DB layer → works across all service instances

### Complex Search Queries (ElasticSearch)

1. Add **ElasticSearch** for full-text search + geospatial queries
2. Index business data including name, categories, descriptions, locations
3. **CDC (Change Data Capture)** to sync Business DB → ElasticSearch (slight eventual consistency lag is acceptable)
4. Business Service queries ElasticSearch for complex multi-criteria queries
5. Cache frequently queried results in Redis for speed boost
6. ElasticSearch `bool` queries: `must` clauses for exact matches, `should` for fuzzy, `geo_distance` filter for location-based search
