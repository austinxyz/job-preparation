---
title: Networking Fundamentals
category: tech/system-design
tags: [networking, dns, tcp, udp, https, tls, websocket, sse, cdn, circuit-breaker, http, latency, load-balancer, l4, l7, retry, backoff, idempotency, regional-partitioning]
status: draft
priority: high
last_updated: 2026-04-06
created_from_jd:
---

# Networking Fundamentals

## Knowledge Map
- Prerequisites（前置知识）：[[Linux Namespaces]], [[Distributed Systems]]
- Related Topics（延伸话题）：[[InfiniBand and High-Speed Networking]], [[Service Mesh and Istio]], [[Cache and Consistency]], [[API Design]]
- Management（管理关联）：[[Platform Team Management]]

## Core Concepts

**DNS Resolution Hierarchy（DNS 解析层级）**
- Full chain: browser local cache → OS cache → local DNS (ISP) → Root NS → TLD NS → Authoritative NS (returns the final IP)
- In practice most requests are resolved at step 2–3 (OS/ISP cache)
- **TTL**: DNS cache validity period; when migrating servers, reduce TTL from 24 hours to 5 minutes in advance — new IP propagates globally within 5 minutes after migration

**TCP Three-Way Handshake and SYN Flood（三次握手与攻击防护）**
- Three-way handshake = bidirectional confirmation: ensures both sides can send and receive before establishing the connection; two-way handshake risks half-open connections (server allocates resources unilaterally)
- **SYN Flood attack**: attacker sends massive SYN packets without sending ACK, exhausts the server's half-open connection queue, preventing legitimate requests from being processed
- Defense: **SYN Cookie** (don't pre-allocate state; put an encrypted cookie in SYN-ACK; only establish connection on receiving a valid ACK — forged IPs can't complete the handshake) + high-availability nodes (edge traffic scrubbing)

**HTTPS / TLS Handshake（TLS 握手）**
- Flow: Client Hello → server returns certificate (containing public key) → client verifies CA → client encrypts session key with public key → both sides use session key for symmetric encryption
- Asymmetric encryption (slow) only used to exchange the key; symmetric encryption (fast) used for actual data transmission
- CA trust chain: CA signs certificates with its private key; browsers have trusted CA public keys built in; a man-in-the-middle without the CA private key cannot forge valid signatures
- **OCSP Stapling**: server obtains a timestamped revocation status response from CA in advance; sends it to the client during TLS handshake — saves client the extra CA query

**Real-Time Communication: Polling / SSE / WebSocket（实时通信对比）**

| Approach | Direction | Connection | Suited For |
|----------|-----------|------------|------------|
| HTTP Polling | Client actively pulls | Short connections | Low real-time, few clients |
| SSE | Server→Client (unidirectional) | Persistent HTTP long connection | Stock quotes, notification push |
| WebSocket | Bidirectional | HTTP Upgrade (101) → full-duplex | Chat, gaming, collaborative editing |

- **1 billion concurrent WebSocket users challenge**: ① async non-blocking IO (one thread manages tens of thousands of connections, not one-thread-per-connection); ② cross-server routing: Redis pub/sub (lightweight) or Zookeeper (strong consistency)
- Reconnect idempotency: give each message a unique `message_id`; client discards duplicates on receipt of the same ID (at-least-once + idempotency) （消息幂等）

**CDN — Content Delivery Network（内容分发网络）**
- **GeoDNS**: returns the nearest CDN node IP based on user geography; CDN serves from cache if present, otherwise **fetches from origin**
- CDN for dynamic content (chat, real-time prices) still has value: low-latency TCP connection from user to CDN + CDN-to-origin optimized private network reduces overall latency (not just caching)

**TCP vs UDP — How to Choose（如何选择）**
- **TCP** (interview default): reliable ordered delivery, flow control, congestion control; cost: handshake overhead, ACK round-trips, Head-of-Line Blocking
- **UDP**: connectionless, no guarantees, low latency; use cases: real-time audio/video (occasional frame drops acceptable), online gaming (fast beats accurate), VoIP, DNS queries, high-throughput log reporting
- Modern apps often mix: HTTP/TCP for signaling and auth, UDP/WebRTC for audio/video streams
- **QUIC** (HTTP/3 underlying): TCP-like reliability over UDP + TLS 1.3, eliminates Head-of-Line Blocking; growing browser support — mentioning in interviews is a bonus but not required

**Load Balancing: L4 vs L7（负载均衡）**
- **Client-side load balancing**: client gets node list from Service Registry, selects independently (gRPC built-in, Redis Cluster); pros: no extra network hop; cons: slow update (DNS TTL limit)
- **L4 load balancer** (transport layer): routes by IP + Port, doesn't parse application content; forwards TCP connections as-is (connection transparently passed between LB and backend); cannot route by URL/Header （传输层路由）
  - Suited for: WebSocket (persistent connections need sticky routing), high-throughput low-latency (minimal packet inspection overhead)
- **L7 load balancer** (application layer): terminates TCP connection, parses HTTP, routes by URL/Header/Cookie; supports SSL offloading, health check response codes, content routing （应用层路由）
  - Suited for: HTTP/HTTPS traffic (most web services), API Gateway scenarios, content-aware routing
- **Health checks**: LB periodically probes backends (TCP connection check or HTTP status code check); failed nodes auto-removed, auto-added back on recovery
- **Load balancing algorithms**: Round Robin (even distribution, preferred for stateless services) / Least Connections (persistent connection scenarios like SSE/WebSocket, prevents connection pile-up) / IP Hash (Session Sticky)

**Failure Handling: Retry + Backoff + Idempotency（故障处理）**
- **Timeout**: set reasonable timeouts (don't wait indefinitely); trigger retry or fast-fail on timeout
- **Retry with Exponential Backoff**: first retry waits 1s, then 2s, 4s, 8s...; avoids avalanche (many clients retrying simultaneously)
- **Jitter**: add random offset to backoff time (e.g., ±50%); prevents many clients from retrying in sync, forming a "pulse" that crushes a recovering service; interview key phrase: "retry with exponential backoff and jitter" （防重试脉冲）
- **Idempotency Key**: client generates a unique key placed in the request Header; server checks if the key was already processed, returns cached result if so; essential for critical operations like payment/inventory

**Regionalization and Latency（区域化与延迟）**
- Light travels at ~200,000 km/s in fiber; New York → London (~5,600 km) theoretical minimum RTT ≈ 56ms — cannot be optimized away, only processing overhead can be reduced
- **Regional Partitioning**: partition data and services by geographic region (e.g., Uber by city — each region has independent DB and service nodes); local requests hit local DB, minimizing cross-region latency
- CDN is regionalization for static resources; Regional Partitioning is regionalization for stateful data; both together cover most global scenarios

**Cascading Failure: Circuit Breaker and Thundering Herd（级联故障防护）**
- Root cause of cascading failures: synchronous blocking calls let one slow node exhaust threads, propagating failure down the entire chain
- **Circuit Breaker three states**:
  - Closed (normal) → failure rate exceeds threshold → Open (tripped, fail fast directly)
  - After a period → Half-Open (let a small number of requests through to probe)
  - Probe succeeds → Closed; probe fails → back to Open
- **Thundering Herd**: when a service recovers, massive queued requests simultaneously surge — may crash it again; Half-Open rate limiting is the key protection (same idea as Cache Stampede Single Flight — "control traffic and let the system recover gradually")

## Key Questions

**Q: Why does HTTPS use both asymmetric and symmetric encryption?**
Answer framework: Asymmetric encryption (RSA) is secure but hundreds of times slower than symmetric; it's only used to exchange the session key once; then symmetric encryption (AES) is used for actual data (fast); combines the best of both: security from asymmetric, performance from symmetric; CA trust chain ensures the public key cannot be replaced by a man-in-the-middle.
> 中文提示：非对称只用一次（交换密钥），对称加密实际数据（快）；CA 信任链防止中间人替换公钥

**Q: What is the difference between WebSocket and SSE? What are they each suited for?**
Answer framework: SSE is unidirectional (server → client), persistent HTTP connection, simple to implement — suited for push-only scenarios (stocks, notifications); WebSocket is full-duplex, requires HTTP Upgrade (101) — suited for bidirectional real-time (chat, gaming); when choosing SSE: if the client doesn't need to send messages, SSE is much simpler than WebSocket.
> 中文提示：SSE 单向推送（简单，基于 HTTP）；WebSocket 双向（复杂，需全链路支持）；能用 SSE 就不用 WebSocket

**Q: 1 billion users concurrently on WebSocket — how do you solve cross-server message routing?**
Answer framework: Users A and B are on different WS servers; two approaches: Redis pub/sub (publish to a channel, all subscribed nodes receive — lightweight, efficient, suits most scenarios) vs Zookeeper (strongly consistent service registry, suited when you need to know precisely which server a user is on); proactively state both approaches and when each applies — don't wait to be asked.
> 中文提示：Redis pub/sub（轻量适合大多数场景）vs Zookeeper（强一致，知道用户在哪台服务器）；主动说出两种方案

**Q: How does Circuit Breaker prevent cascading failures? How do the three states transition?**
Answer framework: Closed → Open (failure rate exceeds threshold, fail fast — don't call downstream) → Half-Open (after a period, let a small amount of traffic probe) → success returns to Closed, failure returns to Open; Half-Open rate limiting prevents Thundering Herd (massive queued requests simultaneously surging after recovery would crash it again); same idea as Cache Stampede Single Flight: "control traffic and let the system recover gradually."
> 中文提示：三态转换；Half-Open 限流防雷群（与 Cache Stampede Single Flight 思想一致）

**Q: Is CDN useful for dynamic content?**
Answer framework: More than just caching. CDN caches static content (images, video) directly; dynamic content (API responses) is not cached by CDN, but still valuable: low-latency TCP from user → CDN (nearby connection establishment), CDN → origin via optimized private network (faster than public internet); Cloudflare's Argo Smart Routing is this principle.
> 中文提示：CDN 对动态内容的价值不是缓存，而是就近建 TCP 连接 + CDN 到源站走优化专线

**Q: How do you choose between TCP and UDP? When would you consider UDP?**
Answer framework: Default TCP (reliable ordered, covers the vast majority of scenarios); UDP use conditions: low latency is more important than reliability + app layer can handle packet loss (video can drop frames, games can drop state packets) + browser support not needed; mention QUIC (HTTP/3 is TCP-like reliability over UDP) as a bonus point; modern apps mix: TCP for control plane, UDP for data plane (WebRTC).
> 中文提示：默认 TCP；UDP 适合低延迟+可接受丢包（音视频/游戏）；QUIC 是面试加分项

**Q: What is the difference between L4 and L7 load balancers? Which does WebSocket use?**
Answer framework: L4 = transport-layer routing (IP+Port), transparently passes TCP connections, doesn't parse application layer, suited for WebSocket persistent connections (sticky routing); L7 = application-layer routing, terminates TCP, parses HTTP, supports URL/Header routing, SSL offloading, suited for HTTP traffic; most scenarios use L7; WebSocket uses L4 (avoids L7 re-establishing connections and breaking persistent connections); mention health checks (TCP connection check vs HTTP status code check).
> 中文提示：L4 透传 TCP（WebSocket 用 L4）；L7 终止 TCP 解析 HTTP（大多数 HTTP 流量用 L7）

**Q: When you mention retry in an interview and the interviewer asks "how do you prevent retry from causing an avalanche?"**
Answer framework: Three-layer protection: ① Exponential Backoff (wait time grows exponentially, reduces total request volume); ② Jitter (random offset breaks synchronized retry "pulses" from multiple clients); ③ Circuit Breaker (failure rate exceeds threshold → fail fast, stop retrying); all three combined: Jitter prevents pulses, Backoff reduces frequency, Circuit Breaker protects recovering services; "retry with exponential backoff and jitter" is the interview keyword.
> 中文提示：三层：Backoff 降频率 + Jitter 打散脉冲 + Circuit Breaker 保护恢复中的服务；必须三者结合

**Q: How do you handle cross-region latency for a global service?**
Answer framework: Speed-of-light physical limit (NY→London RTT minimum 56ms) cannot be eliminated, only unnecessary cross-region hops can be reduced; two main strategies: ① CDN (static resources cached nearby); ② Regional Partitioning (stateful data partitioned by region, local requests hit local DB); Uber partitions by city (driver and rider data only in local city DB); global user data (accounts, payments) still needs cross-region access — handle with async + eventual consistency.
> 中文提示：光速限制不可消除；CDN 缓存静态资源 + Regional Partitioning 本地化有状态数据；全局账户数据需异步+最终一致

## Summary

Network fundamentals are most commonly tested in system design interviews across three dimensions: ① protocol understanding (TCP handshake / HTTPS encryption); ② real-time communication selection (polling/SSE/WebSocket); ③ system reliability (CDN distribution / Circuit Breaker protection). All three dimensions share the same engineering mindset: **finding balance under constraints** (performance vs security, real-time vs complexity, availability vs consistency).

Circuit Breaker is the core pattern for distributed systems protecting themselves, sharing the same fundamental idea as Cache Stampede's Single Flight, Kafka's ISR Quorum (preventing slow nodes from dragging down performance): **control traffic and give the system a chance to recover, rather than letting all traffic through and causing a second crash**. Understanding this unified pattern helps proactively consider failure recovery paths when designing any distributed system.

From an AI Infra perspective, high-speed networking fundamentals (RDMA/InfiniBand) are a specialized extension of this TCP/HTTPS knowledge base — distributed training's latency sensitivity is orders of magnitude higher than web systems, requiring bypassing the traditional TCP/IP stack and using RDMA for direct memory access. This networking foundation is the prerequisite for understanding InfiniBand and NCCL communication optimization.

> 面试重点：TLS 握手（非对称换密钥+对称加密数据）→ SSE vs WebSocket 选型 → L4 vs L7 负载均衡 → retry + exponential backoff + jitter 三层 → Circuit Breaker 三态 → CDN 对动态内容的价值

## Raw Material
- [[raw_material/tech/system-design/sd-network]]
- [[raw_material/tech/system-design/network-essential]]
