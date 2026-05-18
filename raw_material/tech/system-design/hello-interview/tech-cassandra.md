---
title: "Hello Interview — Key Technology: Cassandra"
source: "https://www.notion.so/1ffafa27ec7280bbb071cb097e15cb94"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/Cassandra]]"
---

# Key Technology: Cassandra

**Used by**: Facebook, Discord, Netflix, Apple, Bloomberg

Distributed NoSQL database; partitioned wide-column storage; eventual consistency semantics.

## Data Model

- **Keyspace**: like a database; contains tables + configuration
- **Table**: contains rows; has configuration
- **Row**: contains data; primary key + columns; columns can vary per row (wide-column)
- **Column**: name + type + value + **timestamp** (last-write-wins for conflict resolution)
- Types support: user-defined types, JSON values → flexible flat/nested data

## Primary Key

```sql
-- Composite partition key (a+b), clustering key c
CREATE TABLE t (a text, b text, c text, d text, PRIMARY KEY ((a, b), c));

-- Partition key a, clustering keys b+c
CREATE TABLE t (a text, b text, c text, d text, PRIMARY KEY ((a), b, c));
```

- **Partition Key**: determines which node stores the data (via consistent hashing)
- **Clustering Key**: determines sort order of rows within a partition

## Core Architecture

### Partitioning
- Consistent hashing distributes data across nodes
- Virtual nodes (vnodes) for even load distribution
- Keys remapped minimally when nodes added/removed

### Replication
- 3 replicas per data item (configurable)
- NetworkTopologyStrategy for multi-DC/rack awareness
- SimpleStrategy for single DC

### Consistency Levels (per operation)
- ONE to ALL; QUORUM (majority = n/2+1) → writes visible to reads
- Not full ACID; only atomic + isolated at row level

### Query Routing
- Any node can be coordinator; gossip protocol for node awareness
- Coordinator calculates hash → routes to correct node(s) based on replication strategy

## Storage: LSM Tree

Optimizes for **write throughput** (vs. B-Tree which optimizes reads):
1. **Commit Log**: write-ahead log for durability
2. **Memtable**: in-memory sorted structure by primary key
3. **SSTable**: sorted string table; flushed from memtable to disk (immutable)

**Read path**: check Memtable → bloom filter determines which SSTable → read from newest to oldest SSTables
**Compaction**: merges SSTables, cleans up deleted (tombstone) rows

## Gossip Protocol
- Nodes exchange state via gossip to detect failures
- Seed nodes guarantee network connectivity
- Phi Accrual Failure Detector for node conviction

## Fault Tolerance
- **Hinted Handoffs**: coordinator stores write hints for offline nodes; delivers when they come back online

## Data Modeling Rules

**Query-driven** (not entity-relationship driven):
- Design tables around query patterns
- No JOINs → denormalize data
- Key considerations: Partition Key, Partition Size, Clustering Key, Data Denormalization

### Discord Example
- `channel_id` as partition key; `message_id` as clustering key
- Hot channel fix: bucket by 10-day period → `PRIMARY KEY (channel_id, bucket)`

### TicketMaster (Taylor Swift Problem)
- `tickets`: partition key = `(event_id, section_id)`
- `event_sections`: partition key = `event_id`

## When to Use Cassandra in Interviews

**Good fit**: availability > consistency; high scalability; fast writes; flexible schemas

**Limitations**: not for strict consistency; complex queries (no joins); advanced query patterns require careful data modeling
