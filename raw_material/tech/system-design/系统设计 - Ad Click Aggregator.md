---
title: 系统设计 - Ad Click Aggregator
source:
date_saved: 2026-04-11
processed: false
skill_note:
---

# 系统设计 - Ad Click Aggregator

<!-- Paste original article content below. Do not edit — keep raw. -->
<!-- Run raw-material-processor skill to distill this into the linked skill note. -->
Requirement
- click an ad and redirected to ad website
- advertisers can query ad click metrics

NFR
- latency
- scalability
- fault tolerant and data accuracy 
- near realtime, see data as soon as after click
- idempotent click tracking

Deepdive
	- Ad placement service, 302 server-side redirection
	- Streaming - kafka/kinesis
	- Streaming processor - flink/spark
 - scalability - click processor service (auto-scaling), stream/sharding(adId), stream processor (add more tasks/jobs), OLAP DB (snowflake/BigQueue)
 - Hot Shards - salt 0-n
 - no click data lost - stream (fault-tolerant, HA), retention period - 7 days, flink - checkpoint (not valid for this case, since aggregation window is small), replay from a known timestamp
	 - reconcile - raw click data in S3 - periodic batch job (spark), compare the result
- idempotent - impression ID (signed), cache , write to stream and then add into cache
- query metrics at low latency - pre-aggregating 
![[raw_material/tech/system-design/images/adclick.png]]