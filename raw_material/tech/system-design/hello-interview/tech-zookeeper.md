---
title: "Hello Interview — Key Technology: ZooKeeper"
source: "https://www.notion.so/1fbafa27ec72809c893ee777b97770cc"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/ZooKeeper]]"
---

# Key Technology: ZooKeeper

## Core Purpose

Distributed coordination service: consensus, leader election, configuration management, service discovery, failure detection. Provides a consistent, reliable source of truth across distributed systems.

## Data Model: ZNodes

Hierarchical namespace like a file system. ZNodes can store data (<1MB).

- **Persistent ZNodes**: survive session ends (configuration data)
- **Ephemeral ZNodes**: auto-deleted when session ends (disconnection/timeout) — service presence tracking
- **Sequential ZNodes**: monotonically increasing counter — distributed locks, leader election

## ZooKeeper Ensemble

- Group of servers: 3, 5, or 7 (odd for majority voting)
- **Leader**: handles update requests; elected via ZAB protocol
- **Followers**: serve read requests
- Provides HA and durability when individual servers fail

## Watch Mechanism

Clients register watches on ZNodes → receive real-time notifications when ZNode changes. Eliminates polling and complex broadcast systems.

## Key Capabilities

### Configuration Management
- Clients watch config ZNode → notified on change
- Enables real-time propagation, versioning, atomic updates

### Leader Election
1. Each server creates sequential ephemeral node under designated path
2. Lowest sequence number → leader
3. Others watch node with next-lower sequence number
4. Leader fails → its node disappears → next server steps up automatically

### Distributed Locks
1. Client creates sequential ephemeral node under lock path
2. Sort nodes; client with lowest sequence number holds lock
3. Each client watches node with next-lower sequence number
4. Client releases lock (or crashes) → ZNode removed → next client notified
5. **vs. Redis**: ZooKeeper better for strong consistency + long-lived locks; Redis better for simple short-lived locks

### Service Discovery
- Services register ephemeral ZNodes on startup
- Clients watch service directory for membership changes

## How ZooKeeper Works

**ZAB (ZooKeeper Atomic Broadcast)**: similar to Paxos/Raft for consensus

**Strong Consistency Guarantees**: Sequential Consistency, Atomicity, Single System Image, Durability, Timeliness

**Read/Write**: 10:1 reads to writes; writes go through leader → broadcast via ZAB

**Sessions**: heartbeat-based; session recovery if connection lost (connects to another server); session expiration removes ephemeral nodes

## When to Use ZooKeeper in Interviews

**Smart Routing (Chat apps, Live comments)**:
- Each server registers in ZooKeeper with capacity + handled rooms/videos
- API Gateway queries ZooKeeper to find appropriate server for a user's room/chat
- Coordinate expansion when servers reach capacity

**Infrastructure Design**:
- Distributed message queues
- Distributed task schedulers  
- Kafka (historically): leader election + topic/partition configuration

**Durable Distributed Locks**:
- File systems (nested lock hierarchy)
- Long-lived locks with strong consistency requirements

## Alternatives

- **etcd** (Kubernetes)
- **Consul** (network infrastructure automation)
- **Cloud Provider**: AWS Parameter Store, Azure App Configuration, Google Cloud Datastore
- **Kafka KRaft**: Kafka replaced ZooKeeper with its own Raft-based metadata management

## Limitations

- Hot spotting issues
- Performance limitations: write expensive; <1M data capacity
- Operational complexity: JVM tuning, disk layout, ongoing timeout/connection monitoring
