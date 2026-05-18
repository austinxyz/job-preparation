---
title: "Hello Interview — Case: Robinhood (Stock Trading)"
source: "https://www.notion.so/1efafa27ec7280a39805dea1dfe09c17"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/System Design Case - Robinhood]]"
---

# Case: Robinhood (Stock Trading)

## Key Design Questions & Answers

### Live Stock Price Display

1. `GET /symbols/:name` → Symbol Service
2. Symbol Service: fetches price from Symbol Cache; registers `symbol: Set<userId>` in Redis; stores SSE connection in user set
3. Symbol Updater: periodically queries Exchange API for latest prices → stores in Symbol Cache + pushes to Symbol Service
4. Symbol Service gets latest price → fetches user list for symbol → sends via SSE connection to each user

### Create Stock Orders

1. `POST /orders` → Order Service
2. Order Service creates order in OrderDB; calls Order Gateway → sends to Exchange API → gets externalOrderId → stored in OrderDB
3. Order Processor: fetches processing orders from OrderDB; uses externalOrderId to query Exchange API for status; updates OrderDB
4. User polls `GET /orders/:id` for status updates
5. On status update: notification via APN to mobile app

### Real-Time Price Updates (At Scale)

**Redis Pub/Sub**:
1. User subscribes to symbol → Symbol Service creates `symbol: Set<User>` in Redis + channel for symbol + SSE connection
2. Symbol Updater fetches latest price → publishes to Redis symbol channel
3. Symbol Service subscribed to channel → receives latest price → sends to all users in Set via SSE
4. **Symbol Manager**: assigns Symbol Updators to specific symbols; monitors load + heartbeats; reassigns symbols if updator crashes
5. Popular symbols: dedicated powerful updator; multiple Redis channels to distribute load
6. Throttling: only publish if price change >0.1%, add 500ms intervals to reduce update frequency

### High Order Consistency

**Status tracking + reconciliation**:
1. Create order in DB first (status=pending) — ensures order intent is recorded before exchange call
2. Call Order Gateway to get externalOrderId → update order with externalOrderId + status=submitted
3. Shard OrderDB by userId (all orders for a user on same partition → read-your-writes consistency)
4. Exchange updates → Order Service sets status = filled/failed
5. Failure paths:
   - Failed to create in DB: return error to user, retry
   - Failed to call exchange: set status=failed
   - Exchange call succeeded but processor failed to update DB: cleanup processor queries exchange → reconciles status
6. Cleanup processor: periodically gets failed/pending orders, retries; after extended period → shows to user
