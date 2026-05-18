---
title: "Hello Interview — Case: Auction System"
source: "https://www.notion.so/1efafa27ec728023878cfb7276cb9a30"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/System Design Case - Auction System]]"
---

# Case: Auction System

## Key Design Questions & Answers

### Post an Auction Item

1. `POST /auctions` with item, start price, end time → API Gateway → Auction Service
2. Auction Service creates Auction + Item records in Auction DB
3. Returns auction entity to user

### Place Bids

1. `POST /auctions/:id/bid` → Bid Service
2. Bid Service checks maxBidPrice: if `bidPrice > maxBidPrice` → accept, create Bid record; otherwise reject
3. Returns accept/reject response

### View Current Highest Bid

1. When bid accepted: Bid Service updates Auction record with maxBidPrice
2. `GET /auctions/:id` → returns Auction info including current maxBidPrice
3. Client polls this endpoint for live updates (basic approach; SSE/WebSocket for real-time in deep dive)

### Strong Consistency for Bids

**Optimistic Concurrency Control with PostgreSQL**:
1. Add `maxBidPrice` + `maxBidId` to Auction table
2. Transaction flow: `SELECT maxBidId FOR UPDATE` (row-level lock), verify `originalMaxBid.price < currentBid.price`, then `UPDATE maxBidId = currentBidId WHERE maxBidId = originalBidId`
3. On transaction failure (concurrent bid changed price): exponential backoff retry
4. For popular items near end time: retry storm risk → exponential backoff strategy

### Fault Tolerance (No Lost Bids)

**Kafka as durable buffer**:
1. All bid events published to Kafka (Kafka persists to disk); partition by auctionId
2. Multiple Bid Service instances consume bid queue
3. Consumer only commits offset after successfully processing + storing bid in DB
4. If consumer crashes: Kafka redelivers uncommitted messages to another consumer
5. Idempotency: Bid producer generates global unique bidId; Bid Service deduplicates by bidId

### Real-Time Highest Bid to 100M+ Users

**SSE + Redis Pub/Sub**:
1. User places bid → Bid Service calls Connection Management Service
2. Connection Management Service: shards by auctionId → finds Redis instance → stores `auctionId: SSE connections` + subscribes to auctionId event
3. When Bid Service accepts new bid: publishes `auctionId/bid` to all Redis instances
4. Subscribed Redis instances get bid info → retrieve SSE connection list → push to clients
5. Redis instances send heartbeat to Connection Management; failed heartbeat → re-create SSE in another Redis instance

### Scale to 50K Concurrent Writes + 50TB Data

**Redis + batch archival**:
1. Only live auctions in Redis; shard by auctionId (~50 instances)
2. Redis single-threaded → strong consistency for maxBid updates (Lua script)
3. Redis Sentinel + periodic snapshot to local storage against data loss
4. On auction completion: batch job migrates completed auction data from Redis to Auction DB (runs during off-peak)
5. Historical auction data partitioned by startTime in historical DB (less frequent queries after completion)
