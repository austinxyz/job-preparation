---
title: 系统设计 - Distributed Cache
source:
date_saved: 2026-04-11
processed: false
skill_note:
---

# 系统设计 - Distributed Cache

<!-- Paste original article content below. Do not edit — keep raw. -->
<!-- Run raw-material-processor skill to distill this into the linked skill note. -->
Requirement
- put/get/delete
- expiration time
- LRU

NFR
- availability
- latency
- scalability

HashMap + double-linkedList + Janitor

Deepdive
- High available, fault tolerant, replication (async, peer-to-peer/gossip)
	- Asynchronous replication for a good balance of availability and simplicity
	- Peer-to-peer for maximum scalability
- scalability, shard. 1TB -> 50 nodes
- even distribution - consistent hashing
- hot key
	- read - salt, multiple copies
	- write - write batch, hot key with suffixes, randomly updated one shard, query - sum all shard.
- connection pooling.
![[raw_material/tech/system-design/images/cache.png]]