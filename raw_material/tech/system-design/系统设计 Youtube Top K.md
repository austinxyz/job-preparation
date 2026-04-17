---
title: 系统设计 Youtube Top K
source: https://www.hellointerview.com/learn/system-design/problem-breakdowns/top-k
date_saved: 2026-04-15
processed: false
skill_note:
---

# 系统设计 Youtube Top K

Requirement
- query top K videos for all-times
- query tumbling windows of 1 hour, day, month

NFR
- availability
- latency, 1m delay for write, 10-110ms results
- precise not approximate
- scalability (views, number of videos)

Entity
- Video
- View
- Time Window

Deepdive
- latency/scalable, reduce DB query, Precompute the top K for each time window
- Sharded by VideoId
- Kafka + Flink (Aggregation in Memory)
-