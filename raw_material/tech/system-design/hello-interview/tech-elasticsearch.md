---
title: "Hello Interview — Key Technology: ElasticSearch"
source: "https://www.notion.so/1fbafa27ec728057a0f0f8c1d380908b"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/ElasticSearch]]"
---

# Key Technology: ElasticSearch

## Basic Concepts

- **Document**: individual unit of data (e.g., a book)
- **Index**: collection of documents (e.g., bookstore)
- **Mapping**: schema of an index
- **Fields**: `keyword` type (whole value, hash table) vs. `text` type (inverted index, full-text search)

## REST API

```
PUT /books                          # Create index
PUT /books/_mapping                 # Set mapping
POST /books/_doc                    # Add document (returns _id, _version)
PUT /books/_doc/<docId>?version=?   # Update (full)
PUT /books/_update/<docId>          # Update (partial fields)
GET /books/_search                  # Search with query DSL
```

**Relevance sorting**: `_score` based on TF-IDF (term frequency - inverse document frequency)

**Pagination**: `from`/`size` (page-based) or `search_after` + `size` (cursor-based)

## Cluster Architecture

### Node Types

- **Master Node**: coordinates cluster (add/remove nodes, create/delete indices)
- **Data Node**: stores data; hot/warm/cold/frozen tiers
- **Coordinating Node**: routes search requests to appropriate data nodes; maintains query statistics
- **Ingest Node**: data transformation/preparation before indexing

### Data Node Storage (LSM-like)

- **Shard**: unit of data partitioning; each shard = one Lucene index
- **Replicas**: copies of shards for HA + read throughput
- **Segment**: immutable containers of indexed data

**Write flow**: batch documents → construct segment → flush to disk

**Segment immutability benefits**:
1. Safe caching (data won't change mid-query)
2. Simplified concurrency (no lock needed for reads)
3. Easier crash recovery
4. Better compression
5. Optimized data structures for searching

**Deletes**: soft-delete markers; physical cleanup during segment merges (compaction)

## Using ElasticSearch Correctly

1. **Not a primary database** — use as secondary search index alongside authoritative store (Postgres/DynamoDB)
2. Designed for **read-heavy workloads**
3. **Eventual consistency** model — slight lag from CDC sync is acceptable
4. Not relational — no joins; pre-transform data for search patterns
5. **Change Data Capture (CDC)** keeps ES in sync with authoritative DB

## Key Lessons from ES Design

1. **Immutability** → enables caching, compression, no synchronization issues
2. **Separation of query execution** (coordinating nodes) and **data storage** (data nodes)
3. **Indexing strategy** dramatically impacts performance: inverted index (full-text), doc values (sorting/aggregations)
4. Scalability + fault tolerance at cost of complexity (CAP tradeoffs)
5. Efficient data structures: skip lists, inverted index
