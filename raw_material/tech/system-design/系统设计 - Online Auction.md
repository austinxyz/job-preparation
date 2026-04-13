---
title: 系统设计 - Online Auction
source:
date_saved: 2026-04-11
processed: false
skill_note:
---

# 系统设计 - Online Auction

<!-- Paste original article content below. Do not edit — keep raw. -->
<!-- Run raw-material-processor skill to distill this into the linked skill note. -->
Requirement
- post an item
- bid
- view an auction

NFR
- availability for view, consistence for bid
- fault tolerant and duration, no bid drop
- latency
- scalability 

Deepdive
1. strong consistence, OCC (Optimistic concurrency control). max_bid 作为版本号
2. fault tolerant - message queue, Kafka - partition/replication
3. display the latest highest bid in time - SSE  + Pub/sub
4. push notification, APNS/FCM
5. Dynamic auction end times - delay task scheduler

![[raw_material/tech/system-design/images/auction.png]]