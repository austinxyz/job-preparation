---
title: 系统设计 - Tinder
source:
date_saved: 2026-04-11
processed: false
skill_note:
---

# 系统设计 - WhatsApp

<!-- Paste original article content below. Do not edit — keep raw. -->
<!-- Run raw-material-processor skill to distill this into the linked skill note. -->
NFR
- availability
- guarantee deliverability
- scalability
- delete message in central server
- high resilient

Deepdive
- 多个chatserver，用Redis pub/sub来保证不同server的message转发

- inbox放message，ack之后删除，多client，inbox中有client id

- media，用S3，单独download/upload

- GSI，participants，partition key，chatid or participant id - threshold

- Websocket connections fails， server -> heartbeats

- Redis fails to deliver a message, heartbeats 带有message id信息，message id是seq，单调递增，可以用Redis INCR

- Last seen, 通过active的websocket来update

![[raw_material/tech/system-design/images/WhatsApp.png]]