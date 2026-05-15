---
title: System Design Case - Google Doc
category: tech/system-design
tags: [system-design-case, collaborative-editing, operational-transform, websocket, zookeeper, consistent-hashing, real-time]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# System Design Case - Google Doc

## Knowledge Map
- 前置知识：Operational Transform (OT), WebSocket, ZooKeeper, consistent hashing, document compaction, log-structured storage
- 延伸话题：[[System Design Case - WhatsApp]] (WebSocket colocation pattern), CRDTs as an alternative to OT
- 管理关联：

## Core Concepts

- **OT requires colocation — this is the central constraint**: Operational Transform only produces correct results when all concurrent operations for the same document are transformed by the same server in the same order. This forces all users editing the same document to be on the same Document Service instance — not a typical stateless service.
- **ZooKeeper as the routing layer**: ZooKeeper stores `docId → Document Service instance` and `docId → user list` mappings. Every user connection queries ZooKeeper first and is redirected to the correct instance. This makes ZooKeeper the coordination backbone of the entire real-time system.
- **Consistent hashing for docId assignment**: A Service Manager uses consistent hashing to map docIds to Document Service instances, balancing load while minimizing remapping when instances are added or removed.
- **Service Manager for rebalancing**: The Service Manager monitors CPU, memory, and connection count per instance. On detecting a hotspot (too many concurrent editors on one instance), it moves some docIds to less-loaded instances and updates ZooKeeper mappings. Heartbeat failure triggers rebalance.
- **Compaction to control operation log growth**: Every edit is stored as an operation record. Over time, a document's history can become thousands of individual operations. The Doc Ops Cleanup Processor merges consecutive operations into a single snapshot, but only runs on idle documents (no active connections or below an edit frequency threshold) with a lock to prevent concurrent editing.
- **Cold document offload to S3**: Documents with no recent activity have their operation logs archived to S3. On reconnection, they're loaded back into the operations DB and served. This tiers hot/warm/cold storage without architectural complexity.
- **Cursor presence as a separate lightweight path**: Cursor updates are ephemeral state (not persisted). They flow through the same WebSocket connection but are tracked in-memory per Document Service instance. Heartbeat timeout removes stale cursor state.

## Key Questions

**Q: Why must all users editing the same document be on the same server instance?**
Answer framework: OT transforms operations relative to each other's position in the document. If user A's insert at position 5 and user B's delete at position 3 are processed on different servers, neither server has the information needed to transform them correctly against each other. Colocation ensures one server sees all concurrent operations and applies transforms in a consistent order.

**Q: What happens when the Document Service instance serving a document crashes?**
Answer framework: Service Manager detects missing heartbeat → marks that instance as down → triggers rebalance. ZooKeeper mappings are updated to assign affected docIds to other instances. Users reconnect, are redirected to the new instance, and their clients re-fetch the document state from the Document Operations DB (persisted, not lost).

**Q: How does compaction work without corrupting document state?**
Answer framework: The compaction process (Doc Ops Cleanup Processor) only runs on idle documents. It acquires a lock on the document (setting it read-only), merges operations into a single consolidated state, saves a snapshot (preserving version history), and releases the lock. Running on idle documents eliminates the risk of a concurrent edit racing with compaction.

**Q: How does a new user joining an existing document catch up to the current state?**
Answer framework: On connection, the Document Service loads all operations from the Document Operations DB for that docId (in order) and sends them to the client. The client replays these operations to reconstruct current document state. After replay, subsequent real-time operations arrive via WebSocket.

**Q: How does the system scale to support millions of concurrent documents?**
Answer framework: Thousands of Document Service instances, each hosting a subset of active docIds via consistent hashing. ZooKeeper provides the routing directory. Service Manager handles load rebalancing. Idle documents are evicted from memory (operations stay in DB). Cold documents archive to S3. Total capacity scales horizontally by adding more Document Service instances.

**Q: What is the trade-off between OT and CRDTs for collaborative editing?**
Answer framework: OT requires server-side centralized transform ordering (hence colocation constraint). CRDTs (Conflict-free Replicated Data Types) allow fully decentralized editing with eventual consistency — no server coordination needed — but the data structures are more complex (e.g., Logoot, WOOT). Google Docs uses OT; Figma and some newer systems use CRDTs. For an interview, either is valid; the key is articulating the colocation constraint that OT imposes.

**Q: Why use ZooKeeper specifically rather than a simpler key-value store like Redis?**
Answer framework: ZooKeeper provides distributed coordination primitives — watches (notifications on key change), ephemeral nodes (auto-deleted on session expiry), and sequential nodes — that are critical for detecting service crashes and triggering rebalance. Redis could store the mapping, but doesn't natively provide the coordination semantics needed for reliable distributed locking and failure detection.

## Summary

Google Doc is a real-time collaborative editor, and the defining constraint is that Operational Transform requires all concurrent editors of a document to be colocated on the same server. This single requirement drives the entire architecture: ZooKeeper as a routing directory, consistent hashing for initial assignment, and a Service Manager for rebalancing on load changes or failures.

The non-obvious design decisions are in the storage and cleanup layers. Rather than storing full document snapshots on every save, the system stores individual operations (an append-only log). This enables efficient real-time sync but requires compaction to prevent unbounded log growth. Compaction is tricky because it must not interfere with live editing — the design solves this by locking documents during cleanup and only running on idle documents.

What interviewers are really testing: (1) whether the candidate understands why stateless horizontal scaling doesn't work for OT, and (2) how to design a coordination layer (ZooKeeper) that handles routing, failure detection, and rebalancing in a single coherent system.

## Key Terms

**Technologies**
- `OT (Operational Transform)` · `WebSocket` · `ZooKeeper` · `S3` · `Document Operations DB`

**Patterns**
- `colocation constraint` · `consistent hashing for routing` · `heartbeat-based failure detection` · `operation log + compaction` · `cold storage tiering`

**Decision Points**
- `OT vs CRDT` · `ZooKeeper vs Redis for coordination` · `operation log vs snapshot storage` · `in-memory vs DB for cursor presence`

## Raw Material
- [[raw_material/tech/system-design/hello-interview/case-google-doc.md]]
