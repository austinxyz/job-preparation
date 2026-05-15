---
title: API Design
category: tech/system-design
tags: [api, rest, graphql, grpc, http, protobuf, websocket, sse, api-design, microservices]
status: in-progress
priority: medium
last_updated: 2026-05-14
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

**REST Deep Dive: Resource Modeling and Data Passing**

- **Resources = nouns, not verbs**: REST resources represent things in your system, not actions. `/bookings` not `/createBooking`; `PATCH /games/{id} {"status":"started"}` not `/startGame`. Resources should always be plural nouns.
- **Nested resources vs query params**: Use nested paths (`/events/{id}/tickets`) when the parent relationship is *required* — the request doesn't make sense without it. Use query params (`/tickets?event_id=123`) when the filter is *optional* — you might want all tickets or filtered tickets. Path params are structural; query params are modifiers.
- **Three ways to pass data**: ① **Path params** — identify the specific resource (required, e.g. `/events/123`); ② **Query params** — optional filters, sorts, pagination (e.g. `?city=NYC&limit=20`); ③ **Request body** — complex payload for create/update (JSON, too large or sensitive for URL).
- **HTTP method idempotency**: GET, PUT, DELETE are idempotent (repeating the call leaves the server in the same final state). POST creates new resources — NOT idempotent (calling twice creates two bookings). PATCH is not guaranteed idempotent. Idempotency matters when networks fail and clients retry — you don't want duplicate payments. Solution: **Idempotency Key** in request header for non-idempotent operations.

**Pagination**

- **Offset-based** (`?offset=20&limit=10`): simple, widely used, but unstable under concurrent writes — new records shift positions, causing duplicates or gaps during pagination. Good default for simple, low-write data.
- **Cursor-based** (`?cursor=<encoded_pointer>&limit=10`): response includes a `next_cursor` pointing to the last record. Stable under writes because it tracks a specific record, not a position. Cannot easily "jump to page 5" but preferred for real-time or high-write data. Interview default: offset is fine unless interviewer asks about high-volume/real-time scenarios.

**API Versioning**

- **URL versioning** (`/v1/events`, `/v2/events`): explicit, easy to understand and test in browsers, most common. Recommended default.
- **Header versioning** (`Accept-Version: v2`): cleaner URLs, follows HTTP standards, but less obvious to developers and harder to test directly. Most interviewers don't care — mention URL versioning briefly and move on.

**Authentication and Authorization**

- **Authentication** (who are you?) vs **Authorization** (are you allowed?): always keep these separate conceptually. Auth checks a valid JWT/session; authz checks whether that user owns the booking they're trying to cancel.
- **API keys**: for server-to-server and 3rd-party developer access. Not for user-facing sessions — users shouldn't manage cryptographic strings. Stored in `Authorization: Bearer sk_live_...` header.
- **JWT (JSON Web Tokens)**: encode user context (user_id, role, exp) in a signed token. Stateless — any service with the verification key can validate without a DB lookup. Ideal for user sessions in distributed systems. Use API keys for service-to-service; JWTs for user sessions.
- **RBAC (Role-Based Access Control)**: assign roles to users, permissions to roles (e.g. `customer` can book; `venue_manager` can create events; `admin` can access everything). In interviews, briefly note which endpoints require which roles — don't over-engineer.
- **Rate limiting**: restrict requests per time window. Common: per-user (1000 req/hr authenticated), per-IP (100 req/hr unauthenticated), per-endpoint (10 booking attempts/min to prevent scalping). Return `429 Too Many Requests`. Implement at API gateway or middleware.

**API Gateway Architecture**

- **Purpose**: single entry point for all client requests in a microservices architecture; manages routing, cross-cutting concerns (auth, rate limiting, caching), and protocol translation; adds value when multiple backend services need a unified interface; unnecessary overhead for monolithic or simple single-backend architectures
- **Routing**: primary function; routes requests based on URL paths, HTTP methods, query parameters, and headers to the appropriate backend service; enables independent deployment of services behind a stable external API surface
- **Authentication at the gateway**: verify identity before forwarding to backend services; offloads auth logic from every individual service; common patterns: JWT validation, API key lookup, OAuth token introspection; backend services can trust requests that passed the gateway
- **Rate limiting**: throttle traffic per client/endpoint before requests reach backend services; per-user limits (e.g., 1000 req/hr), per-IP limits (e.g., 100 req/hr unauthenticated), per-endpoint limits (e.g., 10 attempts/min for sensitive operations); return `429 Too Many Requests`; protects backends from overload without burdening individual services
- **Request handling**: validation (URL, headers, body format), size limits; SSL termination (decrypt HTTPS at the gateway — backends communicate over plain HTTP internally); compression; CORS headers; response timeouts; API versioning routing (`/v1/` → service-v1, `/v2/` → service-v2)
- **Caching**: cache full responses or partial data for infrequently-changing data; TTL-based or event-based invalidation; reduces backend load for read-heavy endpoints; careful with personalized responses (don't cache per-user data globally)
- **Horizontal scaling**: API gateways are stateless — scale by adding more instances behind a load balancer; global distribution via regional deployments + DNS-based routing (GeoDNS) routes users to nearest gateway; configuration (routing rules, auth policies) must be synchronized across regions
- **Popular implementations**: AWS API Gateway (REST/WebSocket, deep AWS integration), Azure API Management (policy-based configuration), Google Cloud Endpoints (gRPC support), Kong (open-source, built on Nginx, plugin ecosystem), Tyk (GraphQL support, multi-data-center), Express Gateway (Node.js-based)
- **Protocol translation**: gateway can accept REST externally and translate to gRPC internally — enables external stability (REST) with internal performance (gRPC); this is the standard hybrid architecture pattern at large companies

**GraphQL: N+1 Problem and Field-Level Auth**

- **N+1 problem**: querying events with venue details may fire 1 query for N events, then N separate queries for each venue = N+1 DB queries instead of 2. Solution: **DataLoader** pattern — batches and deduplicates all DB calls within a single GraphQL request execution. Adds complexity not present with REST.
- **Field-level authorization**: GraphQL authorizes at the field resolver level (user can see event name/date but not internal cost data), not at the endpoint level like REST. This adds implementation complexity but enables fine-grained access control.

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

**Q: When should you use cursor-based pagination vs offset-based? What's the trade-off?**
Answer framework: Offset-based is simple and familiar but unstable under concurrent writes — if new records are inserted while a client is paginating, records shift and duplicates/gaps appear. Cursor-based uses an opaque pointer to a specific record (usually last record's ID or timestamp), so insertions don't affect ongoing pagination. Use cursor-based for real-time feeds, social timelines, or any data with frequent inserts; offset-based for static or low-write data where "jump to page N" matters. Most interviewers care more that you remembered to include pagination than which approach.

**Q: When would you recommend API keys vs JWT for authentication? What are the failure modes of each?**
Answer framework: API keys are for programmatic, server-to-server or 3rd-party developer access — they're long-lived and don't carry user context, so they're wrong for user sessions. JWTs encode user identity and expiry in a signed token, enabling stateless verification by any service with the public key — ideal for user sessions in distributed systems. JWT failure modes: token leakage (can't revoke until expiry without a token blacklist), clock skew issues with short expiry, large token size. API key failure modes: no automatic rotation, no user context. In interviews: say JWT for user auth, API keys for service-to-service.

**Q: What is the N+1 problem in GraphQL and how do you solve it?**
Answer framework: When a GraphQL query fetches a list of N events each with their venue, the naive resolver fires 1 query for events then N queries for venues = N+1 total DB queries. This degrades to O(N) DB calls as result size grows. The solution is the DataLoader pattern — it batches all venue lookups that occur within the same request execution tick into a single `SELECT ... WHERE id IN (...)` query, reducing N+1 to 2. DataLoader also deduplicates repeated lookups. This is a known complexity of adopting GraphQL that doesn't exist with REST.

**Q: A client is seeing duplicate orders after a network retry. How do you fix this at the API level?**
Answer framework: This is the POST idempotency problem. POST is not idempotent by default — each call creates a new resource. The solution is an **Idempotency Key**: the client generates a unique key (UUID or `user_id+timestamp`) and includes it in a header (`Idempotency-Key: <uuid>`). The server checks if this key was already processed, and if so, returns the previous response without re-executing. The check-and-mark operation must be atomic (single DB transaction or Redis SETNX). This is the standard pattern for payment APIs (Stripe uses it explicitly).

## Summary

API design paradigm selection is fundamentally a trade-off between **development efficiency, performance, and flexibility**. REST's resource-centered design is simple and intuitive — the right choice for the vast majority of public APIs; GraphQL hands query flexibility to clients, most valuable in fast-iteration frontend/backend scenarios; gRPC uses binary protocol + HTTP/2 for extreme performance in internal service communication.

The most common interview mistake is over-designing the protocol layer ("we use gRPC because it's fast") without clarifying the specific bottleneck. The correct approach: start with REST by default; consider gRPC when serialization/network is proven to be the bottleneck; start with SSE, switch to WebSocket when bidirectional communication is truly needed. **Premature optimization is the root of all evil** — API protocol selection especially so.

From an AI Infra perspective, gRPC is the common choice for model serving APIs: TensorFlow Serving and Triton Inference Server both natively support gRPC (Protobuf defines inference request/response formats). SSE suits streaming generated output (LLM streaming token push to frontend); WebSocket suits multi-turn conversations with context; REST suits simple single-inference APIs. The selection principles are identical to general system design.

> 面试重点：三范式选型框架（默认 REST → 需要灵活查询时 GraphQL → 内部高性能时 gRPC）→ SSE vs WebSocket 选型 → Idempotency Key 设计 → 混合架构（外部 REST + 内部 gRPC）

## Key Terms

**API 范式**
- `REST` · `GraphQL` · `gRPC` · `RPC` · `WebSocket` · `SSE` · `WebRTC`

**REST 核心**
- `resource modeling` · plural nouns · `path parameter` · `query parameter` · `request body`
- `GET` · `POST` · `PUT` · `PATCH` · `DELETE`
- `idempotent` · `Idempotency Key` · `stateless`

**gRPC / Protobuf**
- `Protocol Buffers` · `.proto` · `HTTP/2` · `binary serialization`
- `Apache Thrift` · bidirectional streaming · compile-time type safety

**状态码速查**
- `200` · `201` · `204` · `400` · `401` · `403` · `404` · `429` · `500` · `502` · `503`
- 4xx (client error) vs 5xx (server error)

**分页**
- `offset-based pagination` · `cursor-based pagination` · `next_cursor`

**版本控制**
- `URL versioning` (`/v1/`) · `header versioning` (`Accept-Version`)

**认证鉴权**
- `API key` · `JWT` · `RBAC` · `authentication` vs `authorization`
- `Bearer token` · `exp` claim · stateless validation

**限流**
- `rate limiting` · `per-user limit` · `per-IP limit` · `429 Too Many Requests`

**GraphQL 特有**
- `N+1 problem` · `DataLoader` · `over-fetching` · `under-fetching`
- `schema` · `resolver` · field-level authorization · `query` · `mutation`

**API Gateway**
- `API Gateway` · `reverse proxy` · `SSL termination` · `routing`
- `rate limiting` · `authentication gateway` · `JWT validation`
- `Kong` · `AWS API Gateway` · `Azure API Management` · `Google Cloud Endpoints` · `Tyk`
- `GeoDNS` · `regional deployment` · `stateless gateway` · horizontal scaling
- `protocol translation` · REST → gRPC translation · `middleware`

**反模式 / 面试陷阱**
- verb-based URLs (`/createBooking`) → use noun resources
- POST without Idempotency Key for payment
- GraphQL by default (adds complexity; use REST unless over/under-fetching is the explicit problem)
- spending >5 min on API design in interviews
- API Gateway for monolithic/single-backend architectures (unnecessary overhead)

## Raw Material
- [[raw_material/tech/system-design/network-essential]]
- [[raw_material/tech/system-design/API Design - Hello Interview]]
- [[raw_material/tech/system-design/hello-interview/tech-api-gateway.md]]
