---
title: Hello Interview — Case: Uber (Ride Sharing)
source: "https://www.notion.so/1eaafa27ec7280c1b628daf80847d1c4"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/System Design Case - Uber]]"
---

# Case: Uber (Ride Sharing)

## Key Design Questions & Answers

### Estimated Fare Calculation

1. Rider queries Ride Service with start location + destination
2. Ride Service calls Fare Estimation Service: uses A\*/Dijkstra algorithm to find path (road info from Google Maps API)
3. Based on road info (speed limits) and traffic → estimated time; based on distance (fee per mile) → estimated fee
4. Results stored in Ride DB, returned to user

### Ride Request Flow

1. Rider verifies estimated fare is valid → sends ride request to Ride Service
2. Ride Service creates ride with from/to location, rider info, estimated fare, status=requested
3. Returns ride entity as response

### Driver-Rider Matching

1. Driver app sends regular location updates → stored in Location DB
2. On ride request: Matching Service queries Location DB for available drivers near pickup location
3. Sorts by distance, rating, driver status
4. Sends APN notification to driver's mobile app
5. Driver accepts/rejects → updates ride status in Ride DB

### Location Updates & Proximity Search

**Redis Geospatial** approach:
- Redis geohashing for each driver's current location
- Dynamic update intervals: active drivers every 30s, idle drivers every 5 minutes
- Proximity search: `GEORADIUS` command — finds all driver keys within specified radius
- In-memory Redis allows millions of concurrent requests
- Redis Sentinel for auto-recovery; snapshot to disk for durability
- Data loss on crash mitigated by multiple nodes + disk backup

### One Ride Request Per Driver (Distributed Lock)

**Redis SET NX EX** (atomic set-if-not-exists with expiration):
1. When Matching Service matches driver: create Redis record `key=driverId, value=rideRequest` with TTL
2. If record exists → skip, go to next driver
3. Driver accepts → remove record, update ride as accepted
4. Driver no response → TTL expires, record auto-removed
5. Local in-memory cache as first-check layer to reduce Redis dependency

### Peak Demand Queue

1. LB + auto-scaling for stateless Ride Service
2. Kafka for ride request queue; partitioned by **geo region** (proximity search is location-based)
3. Additional queue ordering factors: wait time, premium user status
4. Only Matching Service handles messages; on success, marks request complete in queue
5. Monitor queue size → scale Matching Service instances
6. Circuit break for extreme spikes → store in secondary storage; resume when capacity recovers
