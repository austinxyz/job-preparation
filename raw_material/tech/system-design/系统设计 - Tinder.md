---
title: 系统设计 - Tinder
source:
date_saved: 2026-04-11
processed: false
skill_note:
---

# 系统设计 - Tinder

<!-- Paste original article content below. Do not edit — keep raw. -->
<!-- Run raw-material-processor skill to distill this into the linked skill note. -->
NFR
- availability for profile, consistency for swipe
- latency
- scalability
- no previous candidate

Deepdive
- consistency
1. 用Cassandra petition key = small;large，保证两条记录在single petition node，这样可以有强一致性
2. 用redis的key包含两条记录，lua来保证set swipe和check match在一起

- search - elastic search (geo), CDC

- 没有出现之前的，bloomfilter

- cache precomputed

- notification - APNS, FCM

![[raw_material/tech/system-design/images/tinder.png]]