---
title: "Hello Interview — Core Concept: Networking 101"
source: "https://www.notion.so/1f5afa27ec7280f6a22fd72e2ebff7b5"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/Networking Fundamentals]]"
---

# Core Concept: Networking 101

## Network Layers (OSI)

Application Layer — DNS, HTTP, WebSockets, WebRTC
Transport Layer — TCP / QUIC / UDP
Network Layer — IP (DHCP server, routable addresses)
Data Link + Physical Layer

## Transport Protocols

**UDP**: connectionless, no delivery/ordering guarantee, lower latency
- Use when: speed > reliability (live video streaming, online gaming, VoIP, DNS lookups)

**TCP**: connection-oriented, reliable delivery + ordering, flow control, congestion control
- Use when: data integrity is critical

**Default rule**: TCP unless low-latency real-time system where some data loss is acceptable (video streaming, high-volume telemetry). UDP also for non-browser environments.

## Application Layer Protocols

**HTTP/HTTPS**: request/response, stateless, on TCP
- Methods: GET/POST/PUT/PATCH/DELETE
- Status codes: 2xx (200 OK, 201 Created), 3xx (301 Permanent, 302 Temporary), 4xx (401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Too Many Requests), 5xx (500 Server Error, 502 Bad Gateway)

**REST**: resource-based, nouns in URLs, standard HTTP methods
**GraphQL**: client specifies exactly what data it needs; flexible query patterns
**gRPC**: high performance RPC (Google), HTTP/2 + Protocol Buffers (binary), internal microservices

### Push Protocols

**SSE (Server-Sent Events)**: server pushes multiple messages over single HTTP connection; one-way (server → client); EventSource auto-reconnects; good for notifications, live feeds

**WebSockets**: bidirectional persistent connection; client initiates HTTP upgrade → WebSocket protocol; both sides send binary messages; good for games, chat, real-time bidirectional (stateful, more overhead)

**WebRTC**: peer-to-peer (video/audio); UDP-based
- **STUN**: discover public IP/port via NAT traversal ("hole punching")
- **TURN**: relay server when direct P2P fails
- Steps: clients → signaling server → STUN for public addresses → exchange via signaling → direct P2P connection

## Load Balancing

**Client-Side**: client maintains server list from registry; decides which server to call
- Redis Cluster: MOVED response with hash slot
- DNS: returns rotated IP list (slow updates)

**Dedicated Load Balancers**:
- **L4 (TCP/UDP)**: routes by IP+port without inspecting content; maintains persistent connections; fast; good for WebSockets
- **L7 (HTTP)**: terminates connections, inspects content, routes by URL/headers/cookies; more CPU-intensive; supports content-based routing

**Algorithms**: Round Robin (stateless), Random, Least Connections (SSE/WebSocket), Least Response Time, IP Hash

**Products**: Hardware (F5, NetScaler), Software (HAProxy, Nginx, Envoy), Cloud (AWS ELB/ALB/NLB)

## Regionalization & Latency

- Speed of light in fiber: ~200,000 km/s; NY → London ≈ 56ms
- CDNs with edge locations serve cached content from nearest node
- Regional partitioning: route users to nearest region (e.g., Uber geo-partitioned ride queues)

## Handling Failures

**Timeouts + Retries with Exponential Backoff**: idempotent APIs required (calling multiple times = same result); use idempotency key for writes

**Circuit Breakers** (prevent cascading failures):
1. Monitor failures to external service
2. When failures exceed threshold → circuit trips OPEN (fail fast, no actual calls)
3. After timeout → HALF-OPEN (allow test request)
4. Test success → close circuit; test failure → stay open

Benefits: fail fast, reduce load on struggling services, self-healing, system stability
