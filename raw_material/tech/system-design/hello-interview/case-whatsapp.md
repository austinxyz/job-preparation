---
title: "Hello Interview — Case: WhatsApp (Messaging)"
source: "https://www.notion.so/1f2afa27ec72808fb5fbd7a61b87d97f"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/System Design Case - WhatsApp]]"
---

# Case: WhatsApp (Messaging)

## Key Design Questions & Answers

### Create Chats + Add Participants

1. `POST /chat` → Chat Service creates chat in Chat DB + calls Chat Server to setup WebSocket with client
2. Chat Server notifies participants; new participants receive notification, connect, and get WebSocket setup
3. DynamoDB: Chat table (chatId, name) + Participants table (chatId → participant mapping with GSI for reverse lookup)

### Send and Receive Messages

1. Client sends message via WebSocket → Chat Server
2. Message stored in Chat DB
3. Chat Server maintains `chatId → participants list` map → sends message over WebSocket to each participant

### Offline Message Delivery

1. All messages stored in Chat DB (chatId + createTime as sort key)
2. **Inbox table**: stores `participant, chatId, lastMessageId`
3. Offline user reconnects → Chat Server fetches all messages in Chat DB after `lastMessageId` → sends via WebSocket
4. Client reads message → ACKs → updates `lastMessageId` in Inbox

### Media Attachments

1. Chat Server calls blob storage (S3) to generate a pre-signed URL
2. Pre-signed URL sent to client → client uploads media directly to S3 (bypasses Chat Server)
3. Chat Server stores pre-signed URL in message DB
4. Chat Server sends message (including media reference) to all participant clients → clients download from S3

### Scale to Billions of Users

**ZooKeeper + Consistent Hashing + Redis Pub/Sub**:
1. Hundreds/thousands of Chat Servers
2. Chat Service manages `chatId → Chat Server` mapping via **consistent hashing**; stored in **ZooKeeper**
3. All participants in one chat colocated on same Chat Server (ensuring WebSocket delivery)
4. Chat Service monitors load (CPU, memory, connection count); high load → rebalance, move chats to new server, update ZooKeeper
5. Chat Server sends heartbeat; no heartbeat → Chat Service detects crash, triggers rebalance
6. No message loss: client sends message to message queue; Chat Server only ACKs after delivering to clients; unACKed messages redelivered on recovery
7. DynamoDB for messages (chatId as partition key, GSI for createdTime); easy billion-user scale
8. Redis cache for hot chats + messages
9. **Multi-device support**: separate Inbox per clientId; on new message → send to all active clients

### Multiple Clients Per User

1. Clients table: `userId → [clientIds]`
2. Inbox table updated to be per-client (not per-user)
3. Message sent to all active clients for a user simultaneously
4. Latest active device determined by `latestSentMessage` timestamp
5. Switch devices: load from device-specific `lastMessageId` or use youngest across all clients
