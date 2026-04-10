---
title: Cassandra
category: tech/system-design
tags: [cassandra, nosql, wide-column, distributed-database, lsm-tree, consistent-hashing, eventual-consistency, partitioning, replication, gossip]
status: draft
priority: high
last_updated: 2026-04-09
created_from_jd:
---

# Cassandra

## Knowledge Map
- Prerequisites（前置知识）：[[Distributed Systems]], [[NoSQL Databases]], [[Sharding and Scalability]]
- Related Topics（延伸话题）：[[Cache and Consistency]], [[Database Indexing]], [[Redis]]
- Management（管理关联）：

## Core Concepts

**What Cassandra Is（基本定位）**
- Open-source, distributed NoSQL wide-column database; originally built by Facebook for inbox search
- Combines ideas from Amazon Dynamo (consistent hashing, eventual consistency) and Google Bigtable (wide-column storage)
- Core strengths: massive horizontal scalability, high write throughput, tunable consistency, no single point of failure
- Not suitable for: strict consistency, ACID transactions, JOINs, or ad-hoc aggregations

**Data Model（数据模型）**
- **Keyspace** → **Table** → **Row** → **Column** (mirrors database → table → row → column in relational DBs)
- **Wide-column**: each row can have a different set of columns (sparse schema), unlike relational DBs where every row must have every column
- Every column carries a timestamp; conflict resolution is "last write wins" (LWW)
- **Primary Key** = Partition Key (determines node) + optional Clustering Key (determines sort order within partition)
- Composite partition key `(a, b)` spreads load across more partitions; clustering key enables range scans within a partition

**Partitioning via Consistent Hashing（一致性哈希分区）**
- Cassandra hashes partition keys onto a ring; data is assigned to the first node clockwise from the hash value
- Avoids massive re-mapping when nodes join/leave (only adjacent node affected)
- **vnodes (virtual nodes)**: each physical node owns multiple positions on the ring → even load distribution; larger machines can own more vnodes
- Traditional `hash % N` is fragile on topology changes; consistent hashing minimizes data movement

**Replication（复制策略）**
- Replication factor (RF) configured per keyspace; e.g., RF=3 means 3 copies of every partition
- **SimpleStrategy**: scans clockwise from the primary vnode for N-1 additional replica vnodes (dev/test only)
- **NetworkTopologyStrategy**: rack- and datacenter-aware; spreads replicas across DCs to survive datacenter outages (production standard)
- Replicas are placed on distinct physical nodes to avoid correlated failures

**Tunable Consistency（可调一致性）**
- No ACID; atomic + isolated only at single-row, single-partition level
- Consistency level (CL) specifies how many replicas must respond for a read/write to succeed:
  - `ONE`: fastest, weakest consistency
  - `QUORUM`: majority (n/2 + 1); read QUORUM + write QUORUM guarantees no stale reads
  - `ALL`: strongest consistency, lowest availability
- Default behavior is eventual consistency; with enough time all replicas converge
- CAP Theorem: Cassandra skews heavily toward **AP** (Availability + Partition Tolerance)

**Storage Model: LSM Tree（写优化存储）**
- Uses Log-Structured Merge Tree (LSM) instead of B-tree → optimizes for write throughput
- Every write is an append; no in-place updates or deletes (deletes write a "tombstone")
- Write path: `Commit Log` (WAL for durability) → `Memtable` (in-memory sorted structure) → flush to immutable `SSTable` on disk
- Read path: check Memtable first → use **bloom filter** to identify which SSTables may have the key → scan SSTables newest-to-oldest
- **Compaction**: merges SSTables periodically to reclaim space, remove tombstones, and consolidate row versions; efficient because SSTables are already sorted
- **SSTable Indexing**: byte-offset index files for fast on-disk key lookup

**Gossip Protocol（节点发现与状态传播）**
- Peer-to-peer protocol: each node periodically selects random nodes to exchange cluster state (liveness, schema, topology)
- Uses generation (bootstrap timestamp) + version (logical clock) as a vector clock to discard stale state
- **Seed nodes**: designated "choke points" that all nodes gossip with, preventing cluster partitioning into disconnected sub-groups
- Every node knows the full cluster topology → any node can be a query coordinator; no single master

**Fault Tolerance: Phi Accrual + Hinted Handoff（容错机制）**
- **Phi Accrual Failure Detector**: each node independently scores the liveness of peers; "convicts" a node when gossip repeatedly fails; node re-enters cluster automatically when it recovers (not permanently removed unless decommissioned)
- **Hinted Handoff**: when a write's target node is offline, the coordinator stores a "hint"; hint is replayed to the recovered node when it comes back online
- Prevents permanent data loss for short-lived node failures without requiring immediate re-balancing

**Query Routing（查询路由）**
- Any node can be a coordinator for a client query (no master)
- Coordinator computes which nodes hold the data via consistent hashing + replication strategy
- Coordinator fans out to replica nodes and waits for enough responses per the consistency level configured

**Data Modeling: Query-Driven Approach（查询驱动建模）**
- Unlike relational DBs (entity-relationship driven + JOINs), Cassandra models data around access patterns
- No JOINs, no referential integrity; data must be denormalized across tables as needed
- Key design decisions: partition key selection (controls co-location), partition size (avoid hotspots and unbounded growth), clustering key (controls sort order for range queries), denormalization (duplicate data to serve each access pattern efficiently)
- **Classic pattern**: avoid scatter-gather by ensuring each query hits a single partition

## Key Questions

**Q: What makes Cassandra a good fit for write-heavy workloads?**
Answer framework: LSM tree storage model — all writes are sequential appends to commit log + Memtable (no random-disk IO); contrast with B-tree databases that require in-place updates; mention that reads are slightly more expensive (must check Memtable + multiple SSTables); conclude with when this trade-off is worth it (high write throughput, time-series, event logs, messaging).

**Q: Explain Cassandra's consistency model and how you'd achieve strong consistency.**
Answer framework: Cassandra is AP by CAP theorem; no ACID; tunable via consistency levels; explain QUORUM math (n/2+1) — read QUORUM + write QUORUM guarantees at least one overlapping node has the latest write; note that ALL gives strongest consistency but hurts availability; in practice most workloads use QUORUM or ONE with eventual consistency.

**Q: How does Cassandra partition data and how does it handle node additions/removals?**
Answer framework: Consistent hashing on partition key → ring → clockwise assignment; vnodes per physical node for even distribution; node add/remove only re-maps adjacent vnodes (minimal data movement); contrast with naive hash-mod which would re-map most data; replication strategy determines which additional nodes get copies.

**Q: Walk me through Cassandra's read and write paths.**
Answer framework: Write: commit log (durability) → Memtable (fast in-memory) → periodic flush to SSTable; Read: Memtable first → bloom filter to identify candidate SSTables → scan SSTables newest-to-oldest; mention compaction as the maintenance process that merges SSTables and removes tombstones; bloom filter prevents unnecessary disk reads.

**Q: How would you model message storage in Cassandra? (Discord-style)**
Answer framework: Identify access pattern (messages per channel, reverse chronological); choose channel_id as partition key; message_id (Snowflake for time-sort + uniqueness) as clustering key with DESC order; address hot partition problem by bucketing (e.g., time-windowed bucket as part of composite partition key to cap partition size and prevent unbounded growth).

**Q: When would you NOT use Cassandra?**
Answer framework: Avoid when: strict consistency is required (financial transactions, inventory); complex query patterns needed (multi-table JOINs, ad-hoc aggregations); ACID transactions needed; data model requires frequent schema changes or relational integrity; small dataset where the operational complexity isn't worth it. Better alternatives: PostgreSQL for relational/ACID, DynamoDB for managed NoSQL, Redis for pure caching.

**Q: How does Cassandra achieve high availability with no single point of failure?**
Answer framework: Gossip makes every node aware of full cluster state → any node can be coordinator; replication (RF≥3) ensures data survives node failures; Phi Accrual Failure Detector for automatic node conviction/recovery; hinted handoff for short outages; NetworkTopologyStrategy for cross-DC fault isolation; no master node eliminates traditional SPOF.

## Summary

Cassandra is a distributed wide-column NoSQL database purpose-built for massive scale and high availability. It inherits consistent hashing and eventual consistency from Amazon Dynamo, and wide-column storage from Google Bigtable. Its most distinguishing feature is its write-optimized LSM tree storage model: all writes are sequential appends (commit log → Memtable → SSTable), yielding extremely high write throughput compared to B-tree databases. Reads are slightly more complex, requiring a Memtable check and potentially multiple SSTable scans, with bloom filters to prune unnecessary disk reads and compaction to keep SSTable count manageable.

Cassandra's distributed design is masterless: consistent hashing distributes data across nodes with vnodes ensuring even load; gossip propagates cluster state to every node so any node can route queries; replication (with NetworkTopologyStrategy) spreads copies across racks and DCs; and Phi Accrual failure detection plus hinted handoffs handle transient node failures gracefully. Consistency is tunable — from ONE (fast, weak) to QUORUM (balanced) to ALL (strong but brittle) — giving operators control over the CAP trade-off. Cassandra strongly favors AP: it will stay available under partitions at the cost of potential stale reads.

The most important skill for using Cassandra effectively is **query-driven data modeling**: there are no JOINs, so access patterns must be defined up front and tables designed around them. Partition key selection determines data co-location and query efficiency; clustering keys control sort order for range scans; and denormalization across multiple tables is normal and expected. Classic pitfalls include unbounded partition growth (fix with time-bucketing composite partition keys, as Discord did) and hot partitions from low-cardinality partition keys. For AI Infra specifically, Cassandra is well-suited for storing large-scale training metadata, experiment logs, inference request traces, and time-series metrics where write throughput and horizontal scalability matter more than strict consistency.

## Raw Material
- [[raw_material/tech/system-design/Cassandra]]
