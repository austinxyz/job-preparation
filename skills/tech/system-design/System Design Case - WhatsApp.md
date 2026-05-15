---
title: System Design Case - WhatsApp
category: tech/system-design
tags: [system-design-case, websocket, messaging, zookeeper, consistent-hashing, dynamodb, offline-delivery, multi-device]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# System Design Case - WhatsApp

## Knowledge Map
- 前置知识：WebSocket, consistent hashing, ZooKeeper, DynamoDB (partition key + GSI), S3 pre-signed URLs, offline message delivery patterns
- 延伸话题：[[System Design Case - Google Doc]] (WebSocket colocation pattern), [[System Design Case - Robinhood]] (SSE vs WebSocket)
- 管理关联：

## Core Concepts

- **WebSocket colocation for chat rooms**: All participants in one chat must be on the same Chat Server to deliver messages over live WebSocket connections. This mirrors the Google Doc OT constraint — state must be colocated for real-time delivery without coordination overhead.
- **ZooKeeper + consistent hashing for routing**: Chat Service maintains `chatId → Chat Server` mapping via consistent hashing, stored in ZooKeeper. Any client connecting to any Chat Server gets redirected to the correct one.
- **Inbox table as the offline delivery mechanism**: Rather than a push queue, the design uses a pull-based inbox: each participant has an `Inbox` record tracking `lastMessageId` per chat. Offline users reconnect, fetch all messages after `lastMessageId`, and ACK to advance the cursor. Simple and resilient.
- **DynamoDB for message storage**: Messages stored with `chatId` as partition key and `createTime` as sort key. This enables efficient range queries ("give me all messages in chat X after time T"). DynamoDB's horizontal scaling handles billions of messages without schema migrations.
- **S3 pre-signed URLs for media**: The Chat Server never handles media bytes — it only orchestrates. It requests a pre-signed URL from S3, sends it to the client, the client uploads directly, and the URL is stored as the message body. This keeps Chat Server bandwidth purely for signaling.
- **ACK-based delivery guarantee**: The Chat Server only acknowledges to the client after the message is delivered to all online recipients' WebSocket connections. Unacknowledged messages are redelivered on recovery. This prevents message loss during server crashes.
- **Per-client inbox for multi-device support**: Each device has its own clientId and a separate `Inbox` record. A message is sent to all active clients for a user simultaneously. Each device independently tracks `lastMessageId`, so switching devices gives correct catch-up behavior.

## Key Questions

**Q: Why must all participants of a chat be on the same Chat Server?**
Answer framework: WebSocket connections are stateful and bound to a specific server. To deliver a message to a participant over their live WebSocket, the delivering code must run on the server holding that connection. Co-locating all participants of a chat on one server means a single in-memory `chatId → participants` map handles delivery without inter-server message passing.

**Q: How does the system ensure no messages are lost when a Chat Server crashes?**
Answer framework: Two guarantees: (1) all messages are persisted to the Chat DB before delivery, and (2) the ACK mechanism ensures the client only marks a message sent after all online recipients receive it. On Chat Server crash, the chat is reassigned via ZooKeeper rebalancing. Offline participants catch up via the Inbox pull mechanism; online participants reconnect and also use Inbox pull for any messages missed during the crash window.

**Q: How do offline users receive messages they missed while disconnected?**
Answer framework: The Inbox table stores `(participant, chatId, lastMessageId)`. On reconnect, the Chat Server fetches all Chat DB records with `createTime > lastMessageId` for each of the user's chats. The client receives these messages, then sends ACK per message, advancing `lastMessageId` in the Inbox. No push queue needed — the inbox is a persistent cursor.

**Q: What happens when two Chat Servers need to communicate (e.g., after a rebalance)?**
Answer framework: The design avoids inter-server messaging by making Chat Service the coordinator. On rebalance, ZooKeeper mapping is updated, clients reconnect to the new server, and catch up via Inbox pull. There's no direct Chat Server to Chat Server communication required.

**Q: How does the media upload flow prevent the Chat Server from becoming a bandwidth bottleneck?**
Answer framework: The Chat Server only handles the pre-signed URL request (a small metadata call to S3) and the message record storage. The actual media bytes are uploaded directly from client to S3 using the pre-signed URL. The Chat Server then broadcasts the URL (not the media) to all participants, who download directly from S3 or CDN. Chat Server bandwidth stays proportional to message metadata, not media size.

**Q: How does multi-device support change the Inbox design?**
Answer framework: Instead of one Inbox record per user per chat, the design uses one Inbox record per client per chat. Each device has a unique `clientId`. When a message arrives, the Chat Server looks up all `clientIds` for the recipient `userId` and sends to all active ones. Each device tracks its own `lastMessageId`, so a phone and laptop can be at different positions in the message history and each catches up independently.

**Q: How would you handle very large group chats (e.g., 1000+ participants)?**
Answer framework: The colocation constraint means all 1000+ participants must be on one Chat Server — this becomes a bottleneck. Solutions: (1) increase server capacity for large groups; (2) use a fan-out approach where the Chat Server publishes to Redis Pub/Sub channels and multiple servers subscribe for their local participants; (3) accept eventual delivery for large groups. The design should acknowledge this as a scaling boundary and discuss trade-offs explicitly.

## Summary

WhatsApp combines real-time messaging with reliable offline delivery at billion-user scale. The real-time path relies on WebSocket colocation (all chat participants on same server), while the offline path relies on a simple pull-based Inbox cursor. The two paths are complementary — the Inbox also serves as the recovery mechanism when real-time delivery fails.

The non-obvious design decisions are: (1) using a pull-based inbox instead of a push queue for offline delivery — simpler, more resilient, and avoids separate queue infrastructure; (2) S3 pre-signed URL pattern for media — keeps Chat Server stateless relative to media and lets S3 handle large-scale binary storage; (3) per-client (not per-user) inbox for multi-device — a subtlety that most candidates miss.

What interviewers are testing: understanding of stateful WebSocket routing, the trade-off between push and pull for offline delivery, and how to model multi-device support without duplicating message storage.

## Key Terms

**Technologies**
- `WebSocket` · `ZooKeeper` · `DynamoDB` · `S3 pre-signed URLs` · `Redis` · `APN`

**Patterns**
- `colocation constraint` · `consistent hashing routing` · `inbox cursor (pull-based offline delivery)` · `ACK-based delivery guarantee` · `per-client inbox for multi-device`

**Decision Points**
- `WebSocket vs SSE vs polling` · `pull-based inbox vs push queue` · `per-user vs per-client inbox` · `server-side vs client-side media upload`

## Raw Material
- [[raw_material/tech/system-design/hello-interview/case-whatsapp.md]]
