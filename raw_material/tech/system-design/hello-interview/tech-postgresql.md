---
title: Hello Interview — Key Technology: PostgreSQL
source: "https://www.notion.so/200afa27ec7280e69231f70120ab6387"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/PostgreSQL]]"
---

# Key Technology: PostgreSQL

**Used by**: Reddit, Instagram

## Core Capabilities

### Read Performance

- **B-Tree indexes**: exact match, range queries, sorting; trade-off: slower writes, more disk space
- **Full-text search via GIN indexes**: word stemming, relevance ranking, multiple languages, AND/OR/NOT queries (ElasticSearch is more powerful but Postgres is often sufficient)
- **JSONB + GIN**: efficient queries on JSON data
- **PostGIS**: geospatial search (points, lines, polygons; Euclidean/driving distance; GIST using R-tree indexing)
- **Covering indexes**: include all needed columns → return from index without table access (slower writes)
- **Partial indexes**: WHERE condition → smaller index for specific subsets

### Write Performance

Write path: WAL (write-ahead log to disk) → Buffer Cache update (memory) → Background writer (async flush to disk) → Index update (also through WAL)

**Throughput limits (per core)**:
- Simple inserts: ~5,000/sec
- Updates with index modifications: ~1,000-2,000/sec
- Complex transactions: hundreds/sec
- Bulk operations: tens of thousands rows/sec

**Factors affecting limits**: disk I/O for WAL, number of indexes, synchronous replication lag, transaction complexity

### Performance Numbers

- Simple indexed lookups: tens of thousands/sec/core
- Complex joins: thousands/sec
- Tables become unwieldy past 100M rows
- Performance drops when working set exceeds available RAM (**memory is king**)

## Scaling Strategies

1. **Batch Processing**: reduce transaction overhead
2. **Vertical Scaling**: larger instances
3. **Write Offloading**: message queue for non-critical writes
4. **Table Partitioning**: partition by date range (e.g., monthly partitions)

```sql
CREATE TABLE posts (...) PARTITION BY RANGE (created_at);
CREATE TABLE posts_2024_01 PARTITION OF posts FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

5. **Sharding**: not built-in; use manually or via **Citus** (managed sharding extension)

## Replication

- **Read replicas**: scale reads; write to primary, read from replicas
- **High availability**: detect primary failure, promote replica
- **Synchronous vs. async**: small number of synchronous replicas for stronger consistency + additional async replicas for read scaling

## Data Consistency: ACID

- **Transactions** with row-level locking (`SELECT FOR UPDATE`)
- **Isolation levels**:
  - Read committed: allows non-repeatable reads
  - Repeatable read: prevents non-repeatable reads + phantom reads
  - Serializable: strongest isolation

| | Serializable Isolation | Row-Level Locking |
|-|----------------------|-------------------|
| Concurrency | Lower (retries on conflict) | Higher (conflicts only on same row) |
| Performance | More overhead | Less overhead |
| Use case | Complex transactions (hard to know what to lock) | When you know exactly which rows to lock |
| Error handling | Handle serialization failures + retry logic | Handle deadlock scenarios |
| Example | Complex financial calculations | Auction bidding, inventory updates |

## When to Use PostgreSQL

1. Strong ACID requirements
2. Both structured + unstructured data (JSONB)
3. Full-text search and geospatial queries (without adding ElasticSearch/PostGIS)
4. Scale reads effectively via replication
5. Rich tooling/ecosystem

## Alternatives

- **Extreme write throughput**: Cassandra or Redis
- **Global multi-region**: Cassandra or DynamoDB
- **Simple key-value access patterns**: DynamoDB or Redis
