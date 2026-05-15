---
title: ZooKeeper
category: tech/system-design
tags: [distributed-systems, coordination, consensus, leader-election, service-discovery]
status: in-progress
priority: medium
last_updated: 2026-05-14
created_from_jd:
---

# ZooKeeper

## Knowledge Map
- 前置知识：[[Distributed Systems]], [[Apache Kafka]], [[Redis]]
- 延伸话题：etcd, Consul, Raft consensus, ZAB protocol, [[Message Queue]]
- 管理关联：

## Core Concepts

- **What it is**: ZooKeeper is a distributed coordination service providing a consistent, hierarchical key-value store (like a synchronized metadata filesystem). Every connected node sees the same view.
- **ZNodes**: The data model consists of a tree of ZNodes (like filesystem paths). Three types:
  - *Persistent*: exist until explicitly deleted — used for config data
  - *Ephemeral*: auto-deleted when the client session ends — used for liveness/presence tracking
  - *Sequential*: auto-appended monotonically increasing counter — used for leader election and distributed locks
- **Data constraints**: ZNodes are for coordination metadata, not bulk data. Each node stores <1MB; dataset must fit in memory. Thousands of ZNodes is typical, not millions.
- **Ensemble**: ZooKeeper runs as a cluster (ensemble) of 3, 5, or 7 servers (odd numbers for quorum). One server is elected **Leader** (handles all writes); the rest are **Followers** (serve reads, replicate writes).
- **Quorum**: A write succeeds only when a majority of servers persist it. A 3-node ensemble tolerates 1 failure; a 5-node ensemble tolerates 2.
- **Watch mechanism**: Clients register one-time callbacks (watches) on ZNodes. When the node changes, ZooKeeper pushes a notification — enabling reactive, cache-based designs without polling or n² broadcast connections.
- **Sessions & ephemeral nodes**: Clients maintain sessions via heartbeats (timeout typically 10–30s). If a session expires, all ephemeral nodes created by that client are automatically deleted — the core failure-detection primitive.
- **ZAB protocol** (ZooKeeper Atomic Broadcast): The internal consensus protocol. Two phases:
  1. *Leader Election*: server with most up-to-date transaction history wins; tie-break by highest server ID.
  2. *Atomic Broadcast*: all writes go to leader → leader proposes to followers → commit on quorum ACK. Similar in spirit to Raft/Paxos.
- **Consistency guarantees**: Sequential consistency (client updates applied in order), Atomicity (no partial updates), Single System Image (consistent view across servers after sync), Durability (write-ahead transaction log + periodic snapshots), Timeliness (bounded staleness).
- **Read vs write**: Reads served locally by any follower (high throughput, possibly slightly stale). Writes must go through leader (expensive). Optimized for ~10:1 read/write ratio. Use `sync()` before reads requiring strongest consistency.
- **Four primary use cases**:
  1. *Configuration Management*: store dynamic config, watches propagate changes to all services in real time without restarts.
  2. *Service Discovery*: ephemeral nodes register service instances; auto-deregister on crash.
  3. *Leader Election*: sequential ephemeral nodes under a path; lowest seq# wins; each server watches the node just below its own.
  4. *Distributed Locks*: same sequential ephemeral pattern; holder is lowest seq#; on release/crash next holder is notified.
- **ZooKeeper vs Redis locks**: Redis locks favor performance and simplicity. Prefer ZooKeeper when you need stronger consistency for critical operations (financial transactions), long-lived locks (hours), or hierarchical lock structures with deadlock prevention.
- **Limitations**:
  - *Hot spotting*: popular ZNodes (e.g., all clients watching a single leader node) create notification storms at scale.
  - *Performance ceiling*: writes are serialized through leader; in-memory storage caps dataset size.
  - *Operational complexity*: JVM tuning, disk layout, session timeout calibration — "simple to use, complex to operate."
- **Modern landscape**: ZooKeeper is still central to the Apache ecosystem (HBase, Hadoop, Solr, Pulsar, ClickHouse). Kafka moved away from it via KRaft (Raft-based). Common alternatives: **etcd** (Kubernetes, cloud-native), **Consul** (service mesh + health checking), and cloud-managed services (AWS Parameter Store, AWS CloudMap, Azure App Configuration).
- **When to reach for it in interviews**: Deep infra design problems (distributed message queue, distributed task scheduler), smart routing/colocation for websocket servers, durable hierarchical distributed locks. NOT the default choice for general system design.

**Hello Interview: Smart Routing Pattern（面试场景：智能路由）**
- **Chat apps / Live comments**: each WebSocket server registers an ephemeral ZNode with its capacity + the list of rooms/videos it handles; API Gateway queries ZooKeeper to find the right server for a new user's room/chat; when a server reaches capacity, ZooKeeper coordinates expansion and re-routing — eliminates the need for a separate service registry
- **ZAB vs Paxos/Raft**: ZAB (ZooKeeper Atomic Broadcast) serves the same role as Paxos/Raft — leader election + atomic broadcast for consensus; key difference is ZAB's two-phase design (leader election phase → then steady-state broadcast phase)
- **Distributed lock: ZooKeeper vs Redis decision rule**: ZooKeeper for strong consistency + long-lived locks + hierarchical lock structures (file systems); Redis for simple, short-lived locks where performance matters more than theoretical correctness guarantees

## Key Questions

**Q: What are the three types of ZNodes and when do you use each?**
Answer framework: Persistent (config/metadata that outlives sessions), Ephemeral (liveness — auto-deletes on session expiry, key for failure detection), Sequential (ordering — for leader election and locks via monotonic counter). Give a concrete example for each.

**Q: How does ZooKeeper implement leader election?**
Answer framework: Each candidate creates a sequential ephemeral node under a common path. The node with the lowest sequence number is the leader. Non-leaders watch the node just below theirs (not the leader directly — avoids "herd effect"). On leader failure, its node disappears; the next server is notified via its watch and steps up. Mention this is application-level election, distinct from ZAB's internal leader election.

**Q: How does ZooKeeper handle server failures internally?**
Answer framework: ZAB protocol — if a follower fails, the leader continues as long as quorum remains. If the leader fails, ZAB triggers a new leader election (highest transaction history + highest ID). The ensemble requires a majority to serve writes; during split-brain/partition with no majority, writes are blocked (no "split-brain" divergence). Client ephemeral nodes are cleaned up after session timeout.

**Q: ZooKeeper vs etcd — when do you choose each?**
Answer framework: Both provide distributed coordination with strong consistency. ZooKeeper is battle-tested in the Apache ecosystem (Kafka historically, HBase, Hadoop), uses the ZAB protocol, and supports watches natively. etcd uses Raft, is the default for Kubernetes, has a modern gRPC/HTTP API, and is generally simpler to operate. Choose etcd for cloud-native/Kubernetes-adjacent work; ZooKeeper when integrating with the Apache stack or needing its specific primitives.

**Q: Why are ZooKeeper reads potentially stale, and how do you fix it?**
Answer framework: Reads are served locally by any follower from its in-memory copy without consulting the leader, so a follower lagging in replication may return slightly stale data. To get up-to-date data, clients can call `sync()` before a read, which forces the follower to sync with the leader first. This is a consistency/performance trade-off by design — ZooKeeper is optimized for read-heavy workloads.

**Q: What are ZooKeeper's scalability limitations and when would you choose an alternative?**
Answer framework: Three main limitations — hot spotting (millions of clients watching one node overwhelms notification traffic), write throughput (all writes serialized through leader, no horizontal scale), and in-memory dataset size (<1MB per node, total fits in RAM). Alternatives: etcd for cloud-native, Consul for service mesh, Redis for high-frequency locking, cloud-managed config stores for operational simplicity.

**Q: Explain the watch mechanism and how it enables efficient distributed coordination.**
Answer framework: Watches are one-shot callbacks registered on a ZNode (data change, children change, node deletion). When the event fires, ZooKeeper pushes a notification to the client. This eliminates polling and n² broadcast connections — clients keep a local cache updated via watches rather than querying ZooKeeper on every read. Important to note: watches are one-time; the client must re-register after receiving a notification.

**Q: How does ZooKeeper's session management enable automatic failure detection?**
Answer framework: Clients maintain sessions via heartbeats. Session timeout (10–30s typical) is a critical tuning parameter — too short causes false positives on transient network issues; too long delays failure detection. On session expiry, all ephemeral nodes are deleted, which triggers watches on those nodes across all interested clients. This gives the system an automatic self-healing property: crashed servers/clients are detected and cleaned up without manual intervention.

## Summary

ZooKeeper is a battle-tested distributed coordination service built around a synchronized, hierarchical metadata store (ZNode tree). Its three node types — persistent, ephemeral, and sequential — together with the watch notification mechanism, provide the primitives to solve the classic distributed systems hard problems: configuration propagation, service discovery, leader election, and distributed locking. The key insight is that ZooKeeper acts as a single, consistent source of truth that replaces ad-hoc approaches (shared databases, n² peer broadcasts, manual failure detection) with clean, declarative coordination patterns.

Internally, ZooKeeper achieves consistency through the ZAB (ZooKeeper Atomic Broadcast) protocol: all writes funnel through an elected leader and are committed only when a quorum of servers acknowledge. This gives strong ordering and durability guarantees but limits write throughput and makes it unsuitable for high-frequency writes or large datasets (everything must fit in memory). Reads are served locally by any follower for high throughput, with optional `sync()` for strong consistency. The session mechanism — with heartbeats and automatic ephemeral-node cleanup — is the foundation for failure detection across all its use cases.

In the modern landscape, ZooKeeper remains central to the Apache ecosystem (HBase, Hadoop, Solr, ClickHouse, Pulsar) but is less dominant elsewhere. Kafka migrated to its own Raft-based KRaft mode; Kubernetes uses etcd; many teams use Consul or cloud-managed services. For system design interviews, ZooKeeper is most relevant in deep infrastructure problems (designing a distributed message queue or task scheduler), smart websocket routing/colocation scenarios, and hierarchical distributed lock designs. It should not be your first-reach tool — modern load balancers and cloud service discovery often cover simpler coordination needs.

From the Hello Interview perspective, the highest-value ZooKeeper interview use case is smart routing for stateful connections: each WebSocket/chat server registers itself as an ephemeral ZNode with capacity and room metadata; the API Gateway watches ZooKeeper to route users to the right server; failures auto-deregister via ephemeral node deletion. This pattern elegantly replaces a dedicated service registry + health-check system with ZooKeeper primitives. The lock comparison is also interview-critical: ZooKeeper > Redis when locks must be long-lived, hierarchical, or require strong consistency guarantees; Redis > ZooKeeper for short-lived, performance-sensitive locks.

## Key Terms

**ZNode types**
- `persistent` · `ephemeral` · `sequential` · `sequential-ephemeral`

**Coordination use cases**
- `leader election` · `distributed lock` · `service discovery` · `configuration management` · `service registry`

**Consensus & internals**
- `ZAB` · `ZooKeeper Atomic Broadcast` · `quorum` · `ensemble` · `leader` · `follower` · `transaction log` · `snapshot` · `write-ahead log`

**Key mechanisms**
- `watch` · `watcher callback` · `one-shot watch` · `herd effect` · `session timeout` · `heartbeat` · `session expiry` · `sync()`

**Consistency model**
- `sequential consistency` · `atomicity` · `single system image` · `durability` · `timeliness` · `stale reads`

**Alternatives**
- `etcd` · `Consul` · `KRaft` · `Raft` · `Paxos` · `AWS Parameter Store` · `AWS CloudMap` · `Azure App Configuration`

**Failure patterns**
- `split-brain` · `network partition` · `hot spotting` · `herd effect`

## Raw Material
- [[raw_material/tech/system-design/ZooKeeper - Hello Interview]]
- [[raw_material/tech/system-design/hello-interview/tech-zookeeper.md]]
