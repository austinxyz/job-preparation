---
title: 系统设计 - Tinder
source:
date_saved: 2026-04-11
processed: false
skill_note:
---

# 系统设计 - Yelp

<!-- Paste original article content below. Do not edit — keep raw. -->
<!-- Run raw-material-processor skill to distill this into the linked skill note. -->
NFR
- availability
- latency
- scalability

Deepdive

- Elastic search - CDC, full text + geospatial + b-tree index

- 只评价一次 - 用db constraint

- 快速得到评价，记录count和average rate, new average rate = (（old rate * count）+ new rate) / (count+1), 用count来做乐观锁的check

- geo_shape (ploygons) - search predefined location

![[raw_material/tech/system-design/images/yelp.png]]