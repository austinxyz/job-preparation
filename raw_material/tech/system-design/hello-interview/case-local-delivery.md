---
title: "Hello Interview — Case: Local Delivery Service"
source: "https://www.notion.so/1eeafa27ec7280748cebdf1c54bae1ec"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/System Design Case - Local Delivery]]"
---

# Case: Local Delivery Service

## Key Design Questions & Answers

### Query Item Availability Within Fixed Distance

1. Customer sends availability request (location + item keyword) to Inventory Service
2. Inventory Service calls Nearby Service with location → returns list of fulfillment centers within fixed distance (Euclidean distance)
3. Inventory Service queries Inventory DB by keyword + fulfillment center IDs → aggregates quantities across centers
4. Uses **PostGIS** (PostgreSQL extension) for efficient geospatial fulfillment center lookups
5. Returns `item: count` format

### Extend to 1-Hour Delivery Window

1. Nearby Service returns candidate fulfillment centers within 60 miles
2. Add **Estimation Time Service** that calls third-party API (e.g., Google Maps) considering geography + traffic conditions
3. Only fulfillment centers that can deliver within 1 hour are returned
4. Replaces pure Euclidean distance with actual travel time

### Placing Orders (ACID Transactions)

1. Order Service handles order creation
2. Customer submits order with item list + quantities
3. PostgreSQL ACID transaction:
   - Verify fulfillment center inventory meets order requirements
   - Create Order record + Order Items
   - For each order item: decrement inventory at relevant fulfillment centers until order quantity satisfied
   - Commit on success; rollback on failure
4. Serialized isolation level guarantees strong consistency, prevents race conditions

### Fast and Available Inventory Lookups

1. **Redis cache** for item + inventory data
   - Short TTL for inventory (changes frequently)
   - Long TTL for fulfillment center info (changes rarely)
2. **PostgreSQL read replicas** for inventory queries (slight staleness acceptable → eventual consistency)
3. **Sharding by centerId**: lookup table maps centerId → DB instance
4. Availability Service uses lookup table to aggregate inventory from appropriate DB instances
5. Nearby Service: cache fulfillment center list with geohash prefix as cache key (small location changes → same cache hit); each instance maintains local cache
