---
title: API Design
category: tech/system-design
tags: [api, rest, graphql, grpc, http, protobuf, websocket, sse, api-design, microservices]
status: draft
priority: medium
last_updated: 2026-04-06
created_from_jd:
---

# API Design

## Knowledge Map
- Prerequisites（前置知识）：[[Networking Fundamentals]], [[Distributed Systems]]
- Related Topics（延伸话题）：[[Service Mesh and Istio]], [[Message Queue]]
- Management（管理关联）：[[Technical Roadmap]]

## Core Concepts

**Three API Paradigm Comparison（三大 API 范式对比）**

| Paradigm | Default Choice | Suited For | Not Suited For |
|----------|---------------|------------|----------------|
| **REST** | ✅ Yes (default for public APIs) | Public APIs, simple CRUD, familiar to team | Ultra-high-performance internal services |
| **GraphQL** | No | Flexible frontend queries, mobile bandwidth savings | Fixed-requirement backend services, simple APIs |
| **gRPC** | No | High-performance internal service communication, binary data | Public APIs, direct browser access |

**REST: Simple and Flexible — the Interview Default（面试默认选项）**
- Core idea: Resource + HTTP method (GET/POST/PUT/PATCH/DELETE); resource-centered, not operation-centered
- `GET /users/{id}` = read; `POST /users` = create; `PUT /users/{id}` = full update; `PATCH /users/{id}` = partial update; `DELETE /users/{id}` = delete
- Nested resources express relationships: `GET /users/{id}/posts` (all posts by a user)
- **Stateless**: each request is independent; server maintains no client state; easy to scale horizontally
- Interview trap: don't say `updateUser` or `startGame` — those are operations, not resources; REST should be `PUT /users/{id}` and `PATCH /games/{id} { "status": "started" }`

**GraphQL: Flexible Queries — Solves Over/Under Fetching（解决 Over/Under Fetching）**
- Solves: REST over-fetching (returning many unneeded fields) and under-fetching (multiple requests needed to get all required data)
- Clients specify exactly which fields and nested structures they need; backend returns precisely that
- Suited for: separate frontend/backend teams, mobile clients needing bandwidth savings, frequently changing requirements (frontend adjusts Query freely without backend changes)
- Interview advice: only propose GraphQL when the problem explicitly requires "frontend flexibility" or "uncertain requirements"; for fixed-requirement interview design, GraphQL gains are limited and adds complexity

**gRPC: High-Performance Internal Service Communication（内部高性能通信）**
- Underlying: **HTTP/2** (multiplexing) + **Protocol Buffers** (binary serialization)
- Protocol Buffers vs JSON: JSON includes schema field names, text format, verbose; Protobuf binary encoding, fields use numeric tags, 3–10x smaller size, 5–10x faster parsing
- Strongly typed: `.proto` files define service interfaces, compile to generate client/server stubs, type errors caught at compile time
- gRPC features: supports streaming (unidirectional/bidirectional), Deadline propagation, client-side load balancing
- **Recommended usage**: internal services use gRPC (high performance, strong typing); external APIs use REST (mature toolchain, browser support); hybrid: external REST → internal gateway converts → internal gRPC

**Real-Time Communication Selection — Paired With REST/gRPC（实时通信选型）**
- **SSE (Server-Sent Events)**: persistent HTTP connection, server-to-client unidirectional push (data as `data:` lines); simple to implement; limitations: intermediate proxies may buffer (batch send), needs client reconnect logic (EventSource auto-reconnects)
- **WebSocket**: HTTP Upgrade → full-duplex bidirectional; arbitrary binary messages; requires full-stack support (LB, firewall); stateful connection, horizontal scaling needs cross-server routing (Redis pub/sub)
- **WebRTC**: P2P direct connection (STUN/TURN assists NAT traversal), UDP-based, low latency; only for audio/video calls and real-time collaboration (complex implementation, most scenarios don't need it)

**HTTP Status Codes — Interview Quick Reference（常用状态码速查）**
- `200 OK` / `201 Created` / `204 No Content`
- `301 Moved Permanently` / `302 Found` (temporary redirect)
- `400 Bad Request` / `401 Unauthorized` (not authenticated) / `403 Forbidden` (authenticated but no permission) / `404 Not Found` / `429 Too Many Requests`
- `500 Server Error` / `502 Bad Gateway` (invalid upstream response) / `503 Service Unavailable`

## Key Questions

**Q: REST vs GraphQL vs gRPC — how do you choose in an interview?**
Answer framework: Default REST (public API, simple and clear); GraphQL for frontend/backend split + frequent requirement changes + mobile bandwidth saving (limited value in fixed-requirement interview design); gRPC for internal microservice communication (high performance, strong typing, binary); hybrid architecture: external REST, internal gRPC; don't over-optimize protocol selection early (fix bigger bottlenecks first).
> 中文提示：默认 REST；GraphQL 适合前后端分离+需求频变；gRPC 适合内部高性能服务；混合架构是大厂标准

**Q: Why is gRPC faster than REST + JSON? When is it worth introducing?**
Answer framework: Two-layer optimization: ① Protocol Buffers binary encoding (3–10x smaller size, 5–10x faster parsing); ② HTTP/2 multiplexing (concurrent requests on one connection, no head-of-line blocking); worth introducing when: internal service latency and throughput are the bottleneck, data volume is large, many services; not worth it: public APIs (browser doesn't support), team lacks Protobuf experience, simple requirements.
> 中文提示：两层优化：Protobuf 二进制（体积小解析快）+ HTTP/2 多路复用；内部服务瓶颈时才引入

**Q: How do you choose between WebSocket and SSE? When would you use WebRTC?**
Answer framework: SSE = server-to-client unidirectional push (simple, HTTP-based, no special LB config); WebSocket = bidirectional real-time (chat, gaming, needs full-stack WebSocket support and cross-server routing); don't use WebSocket when SSE suffices (simpler); WebRTC only for audio/video calls (P2P, UDP, extremely complex implementation — don't use for other scenarios).
> 中文提示：SSE 单向推送（简单）；WebSocket 双向实时（复杂）；能用 SSE 的场景不用 WebSocket；WebRTC 仅音视频

**Q: How do you design a REST API to prevent duplicate submissions (idempotency)?**
Answer framework: GET/DELETE are naturally idempotent; POST is not idempotent — introduce **Idempotency Key** (client generates a unique key, places it in the request Header; server checks if the key was already processed, returns previous result if so); payment scenarios: key = user_id + date or UUID; server uses a DB transaction to ensure "check-if-processed + mark-as-processed" are atomic.
> 中文提示：POST 不幂等需引入 Idempotency Key（Header 中的唯一 key）；查询+标记必须在同一事务中

**Q: How do you design an API layer that supports both browser access and high-performance service-to-service communication?**
Answer framework: Hybrid architecture — external API Gateway (REST/HTTP) accepts browser requests, internal services use gRPC (high-performance binary); API Gateway handles protocol translation (REST → gRPC); benefits: stable external interface easy to test, efficient internal communication; this is the standard pattern at Google, Netflix, and other large companies.
> 中文提示：外部 REST + 内部 gRPC + API Gateway 做协议转换；大厂标准模式

## Summary

API design paradigm selection is fundamentally a trade-off between **development efficiency, performance, and flexibility**. REST's resource-centered design is simple and intuitive — the right choice for the vast majority of public APIs; GraphQL hands query flexibility to clients, most valuable in fast-iteration frontend/backend scenarios; gRPC uses binary protocol + HTTP/2 for extreme performance in internal service communication.

The most common interview mistake is over-designing the protocol layer ("we use gRPC because it's fast") without clarifying the specific bottleneck. The correct approach: start with REST by default; consider gRPC when serialization/network is proven to be the bottleneck; start with SSE, switch to WebSocket when bidirectional communication is truly needed. **Premature optimization is the root of all evil** — API protocol selection especially so.

From an AI Infra perspective, gRPC is the common choice for model serving APIs: TensorFlow Serving and Triton Inference Server both natively support gRPC (Protobuf defines inference request/response formats). SSE suits streaming generated output (LLM streaming token push to frontend); WebSocket suits multi-turn conversations with context; REST suits simple single-inference APIs. The selection principles are identical to general system design.

> 面试重点：三范式选型框架（默认 REST → 需要灵活查询时 GraphQL → 内部高性能时 gRPC）→ SSE vs WebSocket 选型 → Idempotency Key 设计 → 混合架构（外部 REST + 内部 gRPC）

## Raw Material
- [[raw_material/tech/system-design/network-essential]]
