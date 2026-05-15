---
title: ElasticSearch
category: tech/system-design
tags: [elasticsearch, search, inverted-index, lucene, full-text-search, distributed, CDC, sharding]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# ElasticSearch

## Knowledge Map
- 前置知识：Distributed Systems, Indexing fundamentals, LSM Tree basics
- 延伸话题：Lucene internals, CDC patterns, Kafka + ES integration, vector search (kNN), OpenSearch, Solr comparison, BM25 vs TF-IDF
- 管理关联：search infrastructure as a platform team responsibility, capacity planning for index growth, SLO for search latency

## Core Concepts

- **Document / Index / Mapping**: document = unit of data (e.g., a product); index = collection of documents (like a table); mapping = schema defining field types; a `keyword` field uses a hash table for exact match; a `text` field builds an inverted index for full-text search
- **Inverted index**: maps each token → list of document IDs containing it; enables sub-millisecond keyword lookup across millions of documents; `_score` uses TF-IDF (term frequency × inverse document frequency) for relevance ranking
- **Cluster architecture — 4 node types**: Master Node (cluster coordination: add/remove nodes, index lifecycle); Data Node (stores shards, hot/warm/cold/frozen tiers); Coordinating Node (routes search requests across data nodes, aggregates results); Ingest Node (transforms documents before indexing)
- **Shards and replicas**: a shard = one Lucene index, the unit of partitioning; replicas are copies of shards — they increase both read throughput and fault tolerance; shard count is set at index creation and cannot be changed without reindexing
- **Segment-based storage (LSM-like write path)**: writes batch documents → flush as an immutable segment → background merges compact segments; immutability enables safe caching, no read locks, better compression, easier crash recovery; deletes are soft-delete markers resolved during merge (compaction)
- **Pagination**: `from`/`size` (offset-based, simple but expensive for deep pages — ES must collect and discard all prior hits); `search_after` + `size` (cursor-based, efficient for large result sets; requires sort key)
- **ES is not a primary database**: use alongside an authoritative store (PostgreSQL/DynamoDB); it is eventually consistent — CDC sync lag is acceptable; no joins — pre-transform data at write time to match read patterns
- **Change Data Capture (CDC)**: keeps ES in sync with the source DB; DB change events (insert/update/delete) are replicated to ES asynchronously; tools: Debezium, custom Kafka consumers
- **Read-heavy workload design**: ES excels at full-text search, aggregations, faceted filtering; not suited for transactional writes or relational queries; write amplification is real (each document update writes a new segment)
- **Key lesson — immutability as architecture**: segment immutability → caching, compression, no synchronization; separation of coordinating nodes (query execution) from data nodes (storage) scales each independently

## Key Questions

**Q: When would you add ElasticSearch to a system that already has PostgreSQL? What are the trade-offs?**
Answer framework: Add ES when (a) full-text search requirements exceed Postgres GIN capabilities, (b) search query complexity (multi-field, fuzzy, ranked results) dominates load, or (c) analytics/aggregations need sub-second latency at scale. Trade-offs: ES is eventually consistent (CDC lag) and operationally more complex; Postgres is simpler and ACID but slower for heavy search workloads. Keep Postgres as source of truth; ES as search projection.

**Q: How does ElasticSearch handle writes internally? Why are segments immutable?**
Answer framework: Documents are buffered in memory → flushed to an immutable segment on disk (like an LSM tree flush). Immutability means: (1) segments can be cached safely — data never changes mid-query; (2) no locking needed for concurrent reads; (3) crash recovery is simpler — partially written segments are simply discarded; (4) better compression since the whole segment is known at write time. Deletes are soft markers; physical removal happens during background merge/compaction.

**Q: ES has 4 node types. How would you scale a cluster experiencing high search latency vs high indexing latency?**
Answer framework: High search latency → add Data Nodes or Coordinating Nodes (more parallel query execution); ensure replicas are sized for read throughput. High indexing latency → add Data Nodes (more shard-level write capacity); tune bulk indexing batch size; add Ingest Nodes if transformation is the bottleneck. Master Nodes should be dedicated and odd-numbered (3 or 5) for quorum; they should not double as Data Nodes at scale.

**Q: What is the difference between `keyword` and `text` field types? Why does it matter?**
Answer framework: `keyword` stores the raw value and builds a hash table for exact match, sorting, and aggregations — fast O(1) lookups, no tokenization. `text` applies an analyzer (tokenization, lowercasing, stemming) and builds an inverted index — enables full-text search but cannot be used for exact sort/aggregation. Common pattern: map the same field as both `keyword` (for filtering) and `text` (for search) via a `fields` multi-mapping. Getting mapping wrong at index creation requires full reindex.

**Q: How do you keep ElasticSearch in sync with your primary database? What are the failure modes of CDC?**
Answer framework: Standard pattern is CDC via Debezium reading PostgreSQL WAL → Kafka → ES consumer. Failure modes: (1) consumer lag → search results temporarily stale; (2) schema mismatch between DB and ES mapping → indexing failures; (3) reordered events for the same document → use document versioning (`_version`) to reject stale updates; (4) consumer crash → at-least-once delivery may re-index documents (idempotent since ES upsert is safe). For critical data, monitor consumer lag as an SLO.

**Q: When should you use `search_after` vs `from`/`size` for pagination? What breaks with `from`/`size` at scale?**
Answer framework: `from`/`size` requires ES to collect and rank all results up to `from + size` across all shards, then discard the first `from`; at deep pages (e.g., `from=10000`) this becomes expensive and ES limits it to 10,000 by default. `search_after` uses a sort key (e.g., `_id` or timestamp) as a cursor — each page only retrieves `size` results starting after the last seen key, efficient regardless of depth. Use `from`/`size` for shallow pages with user-visible page numbers; `search_after` for infinite scroll, export jobs, or deep pagination.

**Q: How does ElasticSearch achieve fault tolerance? What happens when a data node fails?**
Answer framework: Replicas — each primary shard has one or more replica shards on different nodes. When a data node fails: Master Node detects failure (via heartbeat), promotes a replica to primary for the lost shards, then re-replicates to restore the target replica count. During this window the cluster is yellow (replica count degraded) but still fully operational (all primaries available). Coordinating nodes automatically avoid the failed node's shards. Recovery time depends on shard size and network bandwidth — large shards (>50GB) slow recovery.

## Summary

ElasticSearch is a distributed search and analytics engine built on Apache Lucene, designed for sub-second full-text search, faceted filtering, and aggregations at scale. It is the industry-standard choice for adding powerful search to systems that use PostgreSQL or another ACID database as their source of truth, with CDC keeping ES as an eventually consistent search projection.

Internally, ES stores data in immutable segments (similar to an LSM tree). Immutability is the central design insight: it enables safe caching, lock-free concurrent reads, better compression, and simplified crash recovery. The 4-node architecture cleanly separates concerns: Master (cluster coordination), Data (storage, hot/warm/cold tiering), Coordinating (query fan-out and aggregation), and Ingest (transformation). Shards partition data horizontally; replicas multiply read throughput and provide redundancy.

For AI Infra and platform system design, ES appears in: model artifact search, experiment metadata search, log/event search pipelines, and increasingly vector similarity search (kNN). The operational lesson most applicable to interviews is the secondary-index pattern — ES is never the authoritative store, always a derived read model kept in sync via CDC. This pattern (CQRS-adjacent) recurs across distributed system design questions.

## Key Terms

**핵심 구성요소**
- `document` · `index` · `mapping` · `field` · `shard` · `replica` · `segment`

**노드 유형**
- `Master Node` · `Data Node` · `Coordinating Node` · `Ingest Node`

**검색 / 인덱싱**
- `inverted index` · `TF-IDF` · `BM25` · `_score` · `keyword field` · `text field` · `analyzer` · `tokenizer`
- `full-text search` · `faceted search` · `aggregation` · `doc values`

**스토리지 내부**
- `Lucene` · `segment` · `segment merge` · `compaction` · `soft delete` · `immutability`
- `LSM tree` (analogous) · `flush` · `translog`

**클러스터 / 운영**
- `hot/warm/cold/frozen tiers` · `shard allocation` · `rebalancing` · `yellow/green/red cluster status`

**동기화**
- `CDC` (Change Data Capture) · `Debezium` · `WAL` · `eventual consistency` · consumer lag

**페이지네이션**
- `from`/`size` · `search_after` · deep pagination limit (10,000 default)

**반패턴**
- ES as primary database · joins in ES · mutable segments · ignoring mapping at design time

## Raw Material
- [[raw_material/tech/system-design/hello-interview/tech-elasticsearch.md]]
