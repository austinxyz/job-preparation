---
title: 系统设计 - Robinhood
source:
date_saved: 2026-04-11
processed: false
skill_note:
---

# 系统设计 - Robinhood

Requirement
- see the live prices of stock
- manage order (market/limit, create/cancel)

NFR
- high consistency for order, availability for view stock
- scalability
- latency
- minimize the active clients to external exchange API

Entity
- user
- symbol
- order

Deep dive
- SSE - live price update
- Order Dispatch Gateway / Order DB / Trade Processer（webhook）
- Scale up
	- Redis pub/sub - SSE
- track order updates - externalOrder Metadata (RocksDB)
- order consistency
	- failed to store order - response to client
	- failed to submit to exchange - mark as failed
	- failed to process order after exchange submission - clean-up / externalOrderId
	-cancel flow
	- failed update status to pending_cancel - response to client
	- failed canceling order - clean up process
	- failed storing canceled status in DB clean up process
![[raw_material/tech/system-design/images/robinhood.png]]