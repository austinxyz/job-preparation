---
title: PostgreSQL
category: tech/system-design
tags: [postgresql, database, sql, acid, indexes, replication, partitioning, sharding, b-tree, jsonb]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# PostgreSQL

## Knowledge Map
- 前置知识：Relational databases, SQL fundamentals, ACID properties, B-Tree data structure
- 延伸话题：WAL internals, MVCC (Multi-Version Concurrency Control), connection pooling (PgBouncer), Citus for sharding, PostGIS for geospatial, EXPLAIN ANALYZE, vacuum/autovacuum, pg_stat_statements
- 管理关联：database capacity planning, RTO/RPO requirements for HA, when to migrate off Postgres (scale inflection points), DBA function vs app team ownership

## Core Concepts

- **Write path (WAL-first)**: every write goes to the Write-Ahead Log (WAL) on disk first → Buffer Cache update in memory → Background Writer async flush to disk → Index update (also WAL-logged); WAL ensures durability — a crash can replay the log to recover committed transactions
- **B-Tree indexes**: the default index type; supports exact match, range queries, and sorting; trade-off: slower writes (index must be updated) and more disk space; multiple columns → composite index (column order matters for query matching)
- **Full-text search via GIN indexes**: word stemming, relevance ranking, AND/OR/NOT queries, multiple languages; sufficient for many use cases; ElasticSearch is more powerful but Postgres often avoids adding another system
- **JSONB + GIN**: stores semi-structured JSON as binary; GIN index enables efficient queries on JSON fields — key-value lookups, array containment, path queries; good for schema-flexible data without a separate document store
- **PostGIS extension**: geospatial search — points, polygons, lines; Euclidean and driving distance; uses GIST indexes (R-tree); enables geo-queries (`ST_DWithin`, `ST_Contains`) without adding a dedicated geo service
- **Covering indexes**: include all needed columns in the index (`INCLUDE` clause) so the query can be satisfied entirely from the index without touching the heap table (index-only scan); faster reads at cost of index size and write overhead
- **Partial indexes**: index only rows matching a WHERE condition → smaller index, faster scans for targeted queries (e.g., index only `WHERE status = 'active'`)
- **Performance numbers to know**: simple indexed lookups ~tens of thousands/sec/core; complex joins ~thousands/sec; tables become unwieldy past 100M rows; performance degrades when working set exceeds available RAM (**memory is king**); write throughput per core: simple inserts ~5,000/sec, updates with index modifications ~1,000–2,000/sec
- **Scaling strategies in order**: ① Batch processing (reduce transaction overhead); ② Vertical scaling (larger instance); ③ Write offloading via message queue; ④ Table partitioning by date range (`PARTITION BY RANGE`); ⑤ Sharding via Citus extension (not built-in)
- **Replication**: read replicas scale read traffic; primary handles all writes; synchronous replication to a small number of replicas for strong consistency + additional async replicas for read scaling; HA setup promotes a replica on primary failure

## Core Concepts (continued)

**ACID and Concurrency**

- **Transactions + row-level locking**: `SELECT FOR UPDATE` acquires a pessimistic row lock; safe for auction bidding, inventory deduction where you know exactly which rows to lock
- **Isolation levels**: Read Committed (default — allows non-repeatable reads); Repeatable Read (prevents non-repeatable reads + phantom reads); Serializable (strongest — detects conflicts and retries; lower concurrency, more overhead)

| | Serializable Isolation | Row-Level Locking |
|---|---|---|
| Concurrency | Lower (retries on conflict) | Higher (only conflicts on same row) |
| Performance | More overhead | Less overhead |
| Use case | Complex transactions where you can't predict which rows conflict | When you know exactly which rows to lock |
| Error handling | Handle serialization failures + retry logic | Handle deadlock scenarios |
| Example | Complex financial calculations | Auction bidding, inventory updates |

## Key Questions

**Q: How does PostgreSQL's WAL ensure durability? What happens during a crash?**
Answer framework: Every committed transaction is first written to the WAL on disk before acknowledging success. On crash recovery, Postgres replays WAL records from the last checkpoint forward, re-applying any changes that didn't make it to the main data files. The Buffer Cache (in-memory) can be lost; the WAL is the source of truth. This is why `fsync=on` must not be disabled in production — it ensures WAL writes reach durable storage before the transaction commits.

**Q: PostgreSQL tables become unwieldy past 100M rows. What are your scaling options in order?**
Answer framework: (1) Ensure correct indexes (B-Tree for range/sort, covering indexes to eliminate heap access); (2) Vertical scale — more RAM so working set fits in memory; (3) Table partitioning by date range — queries that filter by date only scan the relevant partition, enabling partition pruning; (4) Archive old partitions to cold storage (detach + compress); (5) Sharding via Citus when write throughput exceeds a single primary's capacity. Don't jump to sharding prematurely — partitioning solves most cases and is operationally simpler.

**Q: When would you use Serializable isolation vs row-level locking (`SELECT FOR UPDATE`)? What are the failure modes?**
Answer framework: Use `SELECT FOR UPDATE` when you know exactly which rows to lock (e.g., `UPDATE inventory WHERE product_id = X`) — it's efficient and only conflicts when two transactions touch the same row. Use Serializable when transaction logic is complex and you can't enumerate all rows upfront (e.g., complex financial calculations involving derived aggregates). Serializable failure mode: transactions abort with serialization failure and must retry — requires retry logic in application code. Row-level locking failure mode: deadlocks — Postgres detects and aborts one party; application must handle and retry.

**Q: How do you scale PostgreSQL reads? What are the trade-offs of read replicas vs caching?**
Answer framework: Read replicas accept SELECT queries — distribute read traffic by pointing read-heavy services to replicas. Trade-off: async replication means replicas lag primary by milliseconds to seconds; reads may see stale data (replication lag). For time-sensitive reads (e.g., "did my payment just go through?"), route to primary. For stale-tolerant reads (dashboards, search autocomplete), replicas are fine. Caching (Redis) eliminates DB load entirely but requires cache invalidation — adds consistency complexity. Typical pattern: read replicas for DB-level read scaling, cache for hot data with known TTL.

**Q: When should you use PostgreSQL vs Cassandra vs DynamoDB? What are the inflection points?**
Answer framework: Use Postgres when: strong ACID needed (financial transactions, user accounts), data is relational or mixed structured/JSON, team wants a single system for most use cases. Switch to Cassandra/DynamoDB when: write throughput exceeds a single primary (~1,000–5,000 writes/sec/core), need multi-region active-active writes, or access pattern is simple key-value (no complex queries). DynamoDB for serverless/operational simplicity + AWS ecosystem; Cassandra for self-hosted multi-region. The mistake is sharding Postgres when the access pattern doesn't need relational — you pay all the complexity of distributed systems without the benefits.

**Q: What is a GIN index and when would you choose it over a B-Tree?**
Answer framework: GIN (Generalized Inverted Index) indexes multiple keys within a single value — used for full-text search (document → token list), JSONB (document → key-path list), and arrays (row → element list). B-Tree indexes one value per row. Choose GIN when querying inside a composite value: `WHERE body @@ to_tsquery('search')` or `WHERE json_col @> '{"status":"active"}'`. GIN is slower to update (more write overhead) and larger than B-Tree, but enables queries that B-Tree cannot serve at all.

**Q: How does table partitioning work in PostgreSQL? What does the query planner do differently?**
Answer framework: Declarative partitioning (`PARTITION BY RANGE/LIST/HASH`) splits a logical table into physical child tables. Each partition holds a subset of rows. On query execution, the planner performs **partition pruning** — if the WHERE clause includes the partition key (e.g., `WHERE created_at > '2024-01-01'`), it only scans the matching partitions and skips the rest. Benefits: faster queries on recent data, easier archival (detach a partition → move to cold storage), smaller per-partition indexes. Limitation: partition key must appear in most queries; cross-partition queries that can't prune lose the benefit.

## Summary

PostgreSQL is the default relational database for modern systems — ACID-compliant, richly featured (full-text search, JSONB, geospatial via PostGIS), and used by Reddit, Instagram, and most web-scale companies before they hit true scale limits. Its WAL-first write path ensures durability; B-Tree and GIN indexes cover the majority of read patterns from simple lookups to full-text search to JSON queries.

The key benchmark to internalize: tables become unwieldy past 100M rows; writes are bounded at ~1,000–5,000/sec per core depending on transaction complexity; and **memory is king** — performance degrades sharply when the working set exceeds RAM. Scaling in order: correct indexes → vertical scale → partitioning → read replicas → Citus sharding. Sharding is the last resort because it sacrifices joins and distributed transactions.

For AI Infra, Postgres is commonly used for experiment metadata (runs, hyperparameters, metrics), model registry (version, artifacts, lineage), job scheduling state, and feature store metadata. The JSONB capability handles schema-flexible ML metadata well. When interview questions involve "store experiment results" or "track model lineage," Postgres + JSONB is the pragmatic answer before reaching for a purpose-built system.

## Key Terms

**인덱스 유형**
- `B-Tree` · `GIN` · `GIST` · `covering index` · `partial index` · `composite index`
- `index-only scan` · `heap access` · partition pruning

**쓰기 경로**
- `WAL` (Write-Ahead Log) · `Buffer Cache` · `Background Writer` · `checkpoint` · `fsync`
- `durability` · crash recovery · `MVCC`

**트랜잭션 / 동시성**
- `ACID` · `isolation level` · `Read Committed` · `Repeatable Read` · `Serializable`
- `SELECT FOR UPDATE` · row-level locking · deadlock · serialization failure · `BEGIN` / `COMMIT` / `ROLLBACK`

**성능 / 스케일링**
- `working set` · `vertical scaling` · `table partitioning` · `PARTITION BY RANGE`
- `read replica` · `replication lag` · `Citus` · sharding · `connection pooling` · PgBouncer

**확장 기능**
- `JSONB` · `PostGIS` · `GIN index` · `to_tsquery` · `ST_DWithin` · `R-tree`

**벤치마크**
- ~5,000 simple inserts/sec/core · ~1,000–2,000 updates/sec/core · 100M row inflection point

**대안 비교**
- Postgres vs `Cassandra` (write throughput, multi-region) · vs `DynamoDB` (serverless, key-value) · vs `Redis` (in-memory, cache)

## Raw Material
- [[raw_material/tech/system-design/hello-interview/tech-postgresql.md]]
