---
title: Hello Interview — Case: Distributed Cache
source: "https://www.notion.so/1ecafa27ec728011ad85c3e6490c65bd"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/System Design Case - Distributed Cache]]"
---

# Case: Distributed Cache

## Key Design Questions & Answers

### Basic Single-Node Cache (Get/Set/Delete)

- Core: hash map for O(1) lookups and inserts
- Set: `key → (value, ttl + currentTimestamp)`; check if key exists → update or insert
- Mutex/read-write locks for concurrent access
- Get: check key exists, return value
- Delete: check key exists, remove from map

### TTL (Time-to-Live) Implementation

1. Store tuples: `(value, expiration_timestamp)`
2. Get: check if `ttl > currentTime`; if expired → delete entry and return null
3. Background janitor process runs every minute: scans all key/values, removes expired entries
4. On-demand TTL check at Get time improves accuracy between janitor runs

### LRU Eviction Policy

**Doubly Linked List + HashMap**:
- Node: `key, value, ttl`; HashMap: `key → node`
- Set (existing key): update node value/ttl, move node to head
- Set (new key): if full → remove tail node from both map and list; add new node at head
- Get: move accessed node to head (most recently used at front, LRU at tail)
- Delete: move node to tail
- All operations O(1)

### High Availability and Fault Tolerance

**Replication**:
1. Multiple replicas per cache node
2. Primary-replica model: client writes to primary, primary replicates to replicas asynchronously (eventual consistency)
3. Reads from replicas (may read slightly stale data due to async lag)
4. When TTL expires, Janitor removes from all replicas
5. Primary failure → leader election to promote new primary
6. Heartbeat monitors replica health; if replica down → use CDC to recover data on new replica
7. Network partition handling: quorum-based writes, split-brain detection

### Dynamic Scaling to 1TB

**Consistent Hashing**:
1. ~50 nodes needed (32GB RAM per instance, ~24GB usable = ~50 nodes for 1TB)
2. Monitor memory usage → auto-scale when usage >80%
3. Consistent hashing: keys mapped to nodes via circular hash ring; adding/removing nodes → minimal key remapping
4. Virtual nodes for better load balancing
5. On new node insertion: migrate relevant keys from neighboring node
6. Each node maintains primary/replica structure for HA
7. During rebalancing: background data migration with read-from-source fallback to minimize disruption
