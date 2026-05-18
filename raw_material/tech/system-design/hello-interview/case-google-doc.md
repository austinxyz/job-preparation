---
title: "Hello Interview — Case: Google Doc (Collaborative Editor)"
source: "https://www.notion.so/1f1afa27ec7280ad8e0cd04bd0e5b444"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/System Design Case - Google Doc]]"
---

# Case: Google Doc (Collaborative Editor)

## Key Design Questions & Answers

### Create Documents

1. `POST /documents` → Document Metadata Service
2. Creates document record in Metadata DB (docId, owner, title)
3. Returns docId to user

### Concurrent Editing (Operational Transform)

1. User opens document → establishes **WebSocket** connection with Document Service
2. Document Service uses **OT (Operational Transform)** to handle concurrent edits
3. All operations stored in Document Operations DB
4. OT ensures operations from concurrent users are transformed and applied in consistent order

### View Each Other's Changes in Real-Time

1. User connects → Document Service loads all operations from Document Operations DB → sends to client
2. Other user's changes saved as operations → broadcast to all connected clients via WebSocket
3. Client applies OT to merge incoming operations with local state
4. All users editing same doc routed to same Document Service instance — use **ZooKeeper** to track `docId → Document Service` mapping

### Cursor Presence

1. Document Service maintains struct per document: connected users + cursor positions
2. On cursor change: client sends cursor update event → Document Service pushes to all connected clients
3. Heartbeat from client; no heartbeat → user marked offline, presence/cursor removed, ZooKeeper updated (delete user from docId's user list)

### Scale to Millions of Connections

**Consistent Hashing with ZooKeeper**:
1. Hundreds/thousands of Document Service instances
2. **Service Manager** uses consistent hashing: `docId → Document Service instance`
3. ZooKeeper stores `docId → user list` and `docId → service instance` mapping
4. New user connects to any Document Service → redirected to correct service via ZooKeeper hash lookup
5. Service Manager monitors load (CPU, memory, connections); on hotspot → rebalance by moving some docIds to new services
6. Document Service sends heartbeat to Service Manager; no heartbeat → rebalance triggered
7. Rebalance updates ZooKeeper mappings

### Document Storage Optimization

1. Evict document from memory when last user disconnects (only keep active documents in memory)
2. **Compaction**: Document Ops Cleanup Processor merges series of edits into single operation
   - Only runs on idle documents (no active connections, or below edit frequency threshold)
   - Adds lock during cleanup → document set readonly → prevents concurrent edits + cleanup race condition
   - Keeps snapshot of old version for version history
3. Cold documents: write operations to S3; on reconnection, load from blob storage → Document Operations DB → serve

## Key Insight

OT requires all users on same document to be on same Document Service instance to maintain transform ordering. ZooKeeper provides the coordination layer for this colocation strategy.
