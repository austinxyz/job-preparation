---
title: System Design Case - Robinhood
category: tech/system-design
tags: [system-design-case, websocket, sse, redis-pubsub, financial-systems, consistency, trading]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# System Design Case - Robinhood

## Knowledge Map
- 前置知识：SSE (Server-Sent Events), Redis Pub/Sub, WebSocket, consistent hashing, optimistic locking, financial order lifecycle
- 延伸话题：[[System Design Case - Ads Click Aggregation]] (real-time event processing), [[System Design Case - WhatsApp]] (WebSocket at scale)
- 管理关联：

## Core Concepts

- **SSE for live price display**: Server-Sent Events (not WebSocket) is chosen because price updates are unidirectional server→client; SSE is simpler and auto-reconnects. Each Symbol Service instance stores an in-memory `symbol → Set<userId>` map plus the SSE connections.
- **Redis Pub/Sub for fan-out at scale**: Symbol Updater publishes price changes to a Redis channel per symbol; all Symbol Service instances subscribed to that channel forward updates to their connected users. This decouples price ingestion from delivery at scale.
- **Symbol Manager for operational resilience**: A dedicated coordinator assigns specific symbols to Symbol Updater workers, monitors heartbeats, and reassigns symbols on worker crash. Popular symbols get dedicated powerful updaters to avoid starvation.
- **Throttling to reduce noise**: Only publish if price change exceeds 0.1%, and enforce 500ms minimum intervals. This prevents UI thrash and reduces Redis write load without losing meaningful data.
- **Write-first order consistency**: Order is persisted to DB with status=pending before the exchange is called. This ensures intent is always recorded. The `externalOrderId` is added on exchange acknowledgment; a cleanup processor reconciles any gap where exchange succeeded but DB update failed.
- **Sharding by userId for read-your-writes**: Orders partitioned by userId ensure a user always reads from the same DB shard, providing read-your-writes consistency without distributed coordination.
- **Cleanup processor as safety net**: A periodic background job queries for stuck pending/failed orders and retries exchange reconciliation. After an extended timeout, orders are surfaced to the user for manual review.

## Key Questions

**Q: Why use SSE instead of WebSocket for live stock prices?**
Answer framework: Price updates are unidirectional (server→client only); SSE is a simpler HTTP-based protocol that handles this natively with automatic reconnection. WebSocket adds bidirectional complexity that isn't needed for read-only price streams.

**Q: How does the system avoid flooding users and the exchange API with too-frequent updates?**
Answer framework: Two throttling layers — Symbol Updater only publishes if price delta >0.1% (ignores noise) and enforces 500ms intervals between publishes. This reduces Redis channel traffic and downstream SSE delivery without missing meaningful price moves.

**Q: What happens if a Symbol Updater crashes mid-operation?**
Answer framework: Symbol Manager monitors heartbeats per updater. On missing heartbeat, it reassigns the affected symbols to other updater instances and updates internal routing. Symbols for popular stocks can have dedicated backup updaters to minimize reassignment delay.

**Q: How is the order creation made consistent when two steps (DB write, exchange call) can fail independently?**
Answer framework: Step 1 always writes to DB with status=pending before touching the exchange. If exchange call succeeds but DB update fails, the cleanup processor queries the exchange using the stored `externalOrderId` and reconciles. The DB record is the source of truth; the exchange is a downstream dependency.

**Q: How does the system handle a scenario where the exchange accepts the order but the response is never received (network drop)?**
Answer framework: The order stays in status=submitted with an `externalOrderId`. The Order Processor periodically polls the exchange using that ID and updates status to filled/failed. The cleanup processor catches orders that stay stuck too long and escalates to user visibility.

**Q: How do you scale to millions of users watching the same popular stock simultaneously?**
Answer framework: Popular symbols get dedicated powerful Symbol Updater instances. Multiple Redis channels are created for the same symbol to distribute subscriber load across Symbol Service instances. Throttling ensures the per-channel publish rate stays bounded regardless of how many users subscribe.

**Q: Why shard OrderDB by userId rather than by orderId?**
Answer framework: Users primarily query their own orders. Sharding by userId co-locates all of a user's orders on the same shard, enabling read-your-writes consistency and efficient `GET /orders` queries without cross-shard joins.

## Summary

Robinhood requires two distinct real-time systems: a live price display system and an order management system. The price feed handles 1-to-many broadcast (one symbol update → millions of viewers), while orders are low-throughput but demand strict consistency (financial correctness matters more than speed).

For price display, the non-obvious choice is SSE over WebSocket — unidirectional updates need a simpler protocol. The Redis Pub/Sub fan-out pattern decouples ingestion from delivery: Symbol Updaters write to channels, Symbol Service instances subscribe and forward to users. The Symbol Manager adds operational resilience by treating updater assignment as a distributed coordination problem. Throttling at the publisher level prevents cascading load from price volatility.

For orders, the key insight is that the system must tolerate partial failures across two external boundaries (the DB and the exchange). The write-first pattern plus a cleanup reconciliation processor ensures no order is permanently lost even if either side fails. Sharding by userId trades global ordering for predictable read locality. The design acknowledges that a financial system cannot rely on a single request succeeding atomically — it builds a durable state machine with recovery paths for every failure mode.

## Key Terms

**Technologies**
- `SSE` · `Redis Pub/Sub` · `WebSocket` · `APN (push notification)` · `ZooKeeper` (referenced conceptually)

**Patterns**
- `fan-out via pub/sub` · `write-first consistency` · `reconciliation processor` · `heartbeat-based failover` · `throttling by delta + interval`

**Decision Points**
- `SSE vs WebSocket` · `userId sharding for read-your-writes` · `Symbol Manager as coordinator` · `cleanup processor vs synchronous retry`

## Raw Material
- [[raw_material/tech/system-design/hello-interview/case-robinhood.md]]
