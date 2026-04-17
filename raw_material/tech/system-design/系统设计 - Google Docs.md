---
title: 系统设计 - Google Docs
source: https://www.hellointerview.com/learn/system-design/problem-breakdowns/google-docs
date_saved: 2026-04-15
processed: false
skill_note:
---

# 系统设计 - Google Docs

Requirement
- Create new doc
- Edit - Multiple users
- view changes in real-time
- see cursor position

NFR
- availability
- latency
- scalability
- < 100 concurrent editors
- durable and available - server restarted

Entity
- User
- Document
- Edit
- Cursor

Deep dive
- OT Operation Transforms - central server to provide final order of operations, small number of collaborators.
- CRDTs - Conflict-free Replicated Data Types, positions using unique identifiers that can be infinitely subdivided, tombstones for deleted text - large number of collaborators
- Document Service - save OTs to DB. init read all OPs. send to client (websocket), client perform OTs.
- cursor position - ephemeral, keep in memory of Document Service
- multiple document service - zookeeper. same document id to keep all clients in one server, consistent hash.
- Document service do compaction
![[raw_material/tech/system-design/images/googledocs.png]]