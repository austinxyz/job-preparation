---
title: 系统设计 - Price Tracking
source:
date_saved: 2026-04-11
processed: false
skill_note:
---

# 系统设计 - Price Tracking

Requirement
- Price history for Amazon products (website or chrome extension)
- subscribe the price drop with threshold

NFR
- availability
- latency
- scalability
- notification < 1 hour

Entity
- User
- Product
- Price
- Subscription

Deepdive
- scalability - 500M products, Chrome Extension + Selective Crawling
- potential malicious price update, Trust-But-Verify (Verify by crawl) - priority queue + more crawl jobs.
- notification in-time, 
	- CDC -> price change queue, notification work handles message
	- dual-write (filter out tiny changes)
- fast price history - TimescaleDB/ClickHouse 
![[raw_material/tech/system-design/images/pricetracking.png]]