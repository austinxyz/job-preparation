---
title: 系统设计 - FB Live Comments
source:
date_saved: 2026-04-11
processed: false
skill_note:
---

# 系统设计 - FB Live Comments

<!-- Paste original article content below. Do not edit — keep raw. -->
<!-- Run raw-material-processor skill to distill this into the linked skill note. -->
Requirement
- post comments
- see new comments/comments

NFR
- availability
- latency
- scalability 

Deepdive
1. cursor pagination
2. SSE 
	1. Partitioned (videoId) Pub/Sub with viewer co-location
		![[raw_material/tech/system-design/images/pubsub-comment.png]]
	2. Dispatcher Service
		![[raw_material/tech/system-design/images/dispatcher-comment.png]]
3. Mega-Streams
	poll CDN (periodic snapshots) latency 1-2 second from 200ms
	threshold, SSE -> CDN
4. client disconnections 
	Last_Event_ID, localstorage/app storage, replay, shared Redis cache