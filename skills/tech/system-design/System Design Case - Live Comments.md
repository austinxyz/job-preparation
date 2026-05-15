---
title: System Design Case - Live Comments
category: tech/system-design
tags: [system-design-case, sse, websocket, real-time, consistent-hashing, kafka, dynamodb, pub-sub]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# System Design Case - Live Comments

## Knowledge Map
- 前置知识：SSE vs. WebSocket, DynamoDB partition/sort keys, consistent hashing, Kafka consumer groups, ZooKeeper, Redis pub/sub
- 延伸话题：live chat moderation, comment spam detection, reaction systems, video sync (comments timed to video position), WebRTC
- 管理关联：

## Core Concepts

- **SSE for Real-Time Comment Delivery**: SSE (Server-Sent Events) is a one-way server-push connection over HTTP. Ideal for live comments: the server pushes new comments to viewers, viewers POST new comments via regular HTTP. Lower overhead than WebSocket for this asymmetric pattern (many readers, fewer writers).
- **DynamoDB Schema for Comment Pagination**: `videoId` as partition key (all comments for a video on the same shard), `createdTime` as sort key (enables efficient range queries for pagination). On join, fetch latest N comments using `createdTime` as cursor. "Load more" uses cursor-based pagination.
- **Redis Live User List**: Tracks active viewers per video (userId + clientIP/sessionId). Used by the Live Comment Service to know which SSE connections to push to. Heartbeat from client keeps the record alive; expiry removes disconnected users without explicit cleanup.
- **Coordinator + Consistent Hashing for Scale**: Multiple Live Comment Service servers form a pool. A coordinator assigns each videoId to a specific server via consistent hashing. That server consumes the Kafka topic for its assigned videos and maintains SSE connections for those viewers. Consistent hashing minimizes reassignment when servers are added/removed.
- **Kafka Topic Per Video**: Each video gets its own Kafka topic (or partition). When a comment is posted, it's published to the video's topic. Live Comment Service instances subscribe only to their assigned video topics. Consumer group ensures each message is processed once.
- **Spike Handling for Viral Videos**: A single video going viral can overload one Live Comment Service server. Use `videoId + seq` (e.g., `videoId:0`, `videoId:1`) as hash keys to spread the video across multiple servers. Each server handles a subset of viewers for that video.
- **ZooKeeper-Based Dispatch Alternative**: Alternative architecture: a Dispatch Service (backed by ZooKeeper) records `videoId → list of Live Comment Service instances`. New comments are routed by the Dispatch Service to all relevant instances, which push to their client lists. ZooKeeper provides distributed coordination for instance assignment.

## Key Questions

**Q: A viewer joins a live stream mid-way. How do they see recent comments they missed?**
Answer framework: On join, the Comment Service fetches the latest N comments (e.g., N=50) from DynamoDB using the current timestamp as cursor (query all records with createdTime ≤ now, sorted desc, limit 50). The client shows "load more" for older comments, which fetches the next page using the oldest comment's timestamp as the next cursor.

**Q: A viewer's browser tab goes to the background. How does the system detect their disconnection?**
Answer framework: The client sends periodic heartbeats (e.g., every 30s) to the Video Service, which updates a `lastSeen` timestamp in the Redis live user list. If no heartbeat arrives within the TTL, the Redis record expires and the user is considered offline. The Live Comment Service stops pushing to that SSE connection (which would error on the next attempt anyway).

**Q: How do you scale live comment delivery to millions of concurrent viewers on one video?**
Answer framework: Multiple Live Comment Service instances in a pool. Coordinator assigns viewers to instances (consistent hashing). For a single viral video, use `videoId + seq` as hash keys to spread the video across multiple instances. Each instance maintains SSE connections for its subset of viewers and consumes from the video's Kafka partition. Kafka partitions can be split further for high-throughput videos.

**Q: Why SSE instead of WebSocket for this use case?**
Answer framework: Comments are asymmetric: many readers, fewer writers. WebSocket is full-duplex — overhead of bidirectional connection is wasted here. SSE is a unidirectional server-push over standard HTTP — simpler to scale, passes through HTTP proxies/load balancers more easily, and auto-reconnects natively. Writers (commenters) use regular POST requests. SSE is the right fit when the server pushes significantly more than the client sends.

**Q: A Live Comment Service instance goes down. How are its viewers affected?**
Answer framework: The coordinator detects the instance's missing heartbeat. It uses consistent hashing to reassign the dead instance's videoIds to surviving instances. Clients with broken SSE connections auto-reconnect (SSE has built-in reconnect with `Last-Event-ID` header). Clients can include their last received comment timestamp in the reconnect request so the server can replay any missed comments.

**Q: Walk through the data flow when a viewer posts a comment.**
Answer framework: (1) Viewer POSTs comment to Comment Service. (2) Comment stored in DynamoDB (videoId partition key, timestamp sort key). (3) Comment published to Kafka topic for that video. (4) Live Comment Service instances subscribed to that video consume the message. (5) Each instance fetches live user list from Redis for its assigned viewers. (6) Comment pushed via SSE to all connected viewers. Total end-to-end: sub-second.

## Summary

Live Comments must deliver newly posted comments to potentially millions of concurrent viewers of the same video in near-real-time, while also supporting pagination for viewers joining mid-stream. Functional requirements: post comment, view recent comments with pagination, real-time delivery to live viewers.

The core delivery mechanism is SSE: a server-pushed, unidirectional HTTP connection. This asymmetric choice (server → many clients) is more efficient than WebSocket for a read-heavy workload. Comments are stored in DynamoDB with videoId as partition key and timestamp as sort key — this schema directly enables the two access patterns: paginated history (range scan on sort key) and live delivery to all viewers of a video.

The scaling challenge is the hot-video problem: a single viral video's viewers might overwhelm one Live Comment Service instance. The solution combines consistent hashing (coordinator assigns videoIds to instances) with sharding (splitting one video's viewers across multiple instances via `videoId + seq` keys). This pattern of coordinator-managed consistent hashing for stateful streaming connections recurs in distributed systems and is what the interview is really testing.

## Key Terms

**Technologies**
- `SSE (Server-Sent Events)` · `DynamoDB` · `Kafka` · `Redis` · `ZooKeeper` · `Consistent Hashing`

**Patterns**
- `Coordinator + Consistent Hashing` · `Topic Per Video` · `Cursor-Based Pagination` · `Heartbeat-Based Presence`

**Decision Points**
- `SSE vs. WebSocket` · `per-video topic vs. shared topic with filtering` · `consistent hashing vs. broadcast` · `viral video sharding via videoId+seq`

## Raw Material
- [[raw_material/tech/system-design/hello-interview/case-live-comments.md]]
