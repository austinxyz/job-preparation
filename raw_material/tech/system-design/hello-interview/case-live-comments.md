---
title: Hello Interview — Case: Live Comments
source: "https://www.notion.so/1ebafa27ec728024a6b7c8911621bdfe"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/System Design Case - Live Comments]]"
---

# Case: Live Comments

## Key Design Questions & Answers

### Basic Comment Posting

1. Video Service stores live user list (userId + clientIP) in Redis cache
2. Viewer posts comment via Comment Service → stored in Comment DB (DynamoDB, videoId as partition key, timestamp as sort key)
3. Live Comment Service reads latest comment from DB, fetches live user list, sends via SSE

### Viewing Pre-Existing Comments (Pagination)

1. On join: Comment Service fetches latest N comments (N=50) from current timestamp as cursor
2. Client shows "load more" → fetches next N comments (pagination)
3. DynamoDB partition key = videoId (same partition server for all comments), sort key = createdTime
4. Viewer added to live user list with clientIP for SSE delivery

### Real-Time Comment Delivery (Single Video)

**SSE (Server-Sent Events)**:
1. Viewer joins → user info stored in Redis live user list (userId + clientId)
2. Live Comment Service establishes one-way SSE connection with this viewer
3. New comment posted → stored in DB + published to message queue
4. Live Comment Service consumes queue → gets live user list from Redis → sends via SSE
5. Client receives SSE → renders comment (low latency vs. polling)
6. Client sends heartbeat → Video Service updates latestUpdate in live users list
7. Client lost connection → live user record expires/removed → SSE stops

### Scaling to Millions of Concurrent Viewers

**Coordinator + Consistent Hashing** approach:
1. LB + auto-scale for Comment Service, Video Service; DynamoDB scales with partitions
2. Kafka/SQS as message queue; different topic per video
3. Multiple Live Comment Service servers as consumer group
4. Coordinator uses **consistent hashing** to assign videoId → specific Live Comment Service server
5. Each server only consumes comments for its assigned videos + fetches live user list from Redis for those videoIds
6. Live Comment Service sends heartbeat to coordinator; no heartbeat → reassign videoIds (consistent hashing minimizes remapping)
7. Sudden spike for a video: use `videoId+seq` as hash key → spread to multiple servers

**Alternative architecture**: Multiple live comment services handling SSE; Dispatch Service (using ZooKeeper) records videoId → service list; new comments routed by Dispatch Service to corresponding live comment services → pushed to client lists.
