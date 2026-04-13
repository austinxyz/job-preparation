---
title: 系统设计 - Web Crawler
source:
date_saved: 2026-04-11
processed: false
skill_note:
---

# 系统设计 - Web Crawler

<!-- Paste original article content below. Do not edit — keep raw. -->
<!-- Run raw-material-processor skill to distill this into the linked skill note. -->
Requirement
- crawl the web from seed URLs
- extract data

NFR
- fault tolerant 
- politeness
- efficiency - under days
- scaliability

Deepdive
1. fault tolerant
	1. URL Fetcher - frontier queue - SQS exponential backoff
	2. Text & URL extraction - parsing queue
2. politeness
	1. robots.txt - allowed and interval(crawl-delay)
	2. ratelimit - Redis, jitter
3. 10B pages
	1. 200Gbps - 3.75 K pages /second, 10 B /3.75 -> 30.9 days. -> 8 machines
	2. auto-scale, based on queue
	3. DNS - caching, multiple provider
	4. URL deduplication - bloom filter
	5. max depth
	![[raw_material/tech/system-design/images/crawl.png]]