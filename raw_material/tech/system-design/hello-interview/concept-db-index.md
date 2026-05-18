---
title: "Hello Interview — Core Concept: Database Indexes"
source: "https://www.notion.so/1faafa27ec7280d2b03fd873bb6b0fd7"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/Database Indexing]]"
---

# Core Concept: Database Indexes

## When to Use Indexes

Trade-offs: additional disk space + slower writes. Not suitable for: write-heavy with infrequent reads (logging tables).

**Index = table of contents**: jumps to relevant pages without full scan. Random access is still significantly slower than sequential scan.

## Types of Indexes

### B-Tree Indexes (Default)

- Balanced tree with multiple children per node (hundreds); leaf nodes at same depth
- Each node: m/2 → m keys, sized to fit in one disk page (8KB)
- Supports: exact match, range queries, sorting
- **PostgreSQL**: primary keys, unique constraints, most regular indexes → B-trees
- **DynamoDB**: B-tree for sort keys
- **MongoDB**: B+ trees (all data in leaf nodes)

### Hash Indexes

- HashMap: indexed values → row locations; O(1) exact-match queries
- Hash collisions → chaining; useless for range queries or sorting
- **Redis**: hash table as primary data structure
- **MySQL**: memory storage engine used hash indexes by default
- Rule: solves a problem we rarely have in practice

### Geospatial Indexes

**Use cases**: Uber, Yelp, Find My Friends

- **Geohash**: converts 2D location to 1D string (base-32 encoding); can use regular B-tree index on strings; find nearby by matching prefixes. Limitation: nearby locations may not share similar prefixes (edge cases at grid boundaries)
  - Used in: Redis `GEOADD`, `GEORADIUS`
- **Quadtrees**: recursively subdivide space into four quadrants; adaptive resolution (dense areas more finely subdivided); complex specialized tree structure
- **R-trees**: default spatial index in PostgreSQL (PostGIS), MySQL; groups nearby objects into overlapping bounding boxes; hierarchy of bounding boxes; handles spatial relationships well

> Traditional B-trees don't work for spatial data because they treat lat/lon as independent dimensions. Geospatial indexes understand spatial relationships.

### Inverted Indexes

Processing steps:
1. Tokenize text (words/subwords)
2. Lowercase
3. Remove stop words ("the", "and")
4. Stem words (finding/find/finds → find)

**Elasticsearch/Lucene**: frequency, relevance scoring, fuzzy matching, phrase queries
**Use cases**: search GitHub repos, Slack, documentation

## Index Optimization Patterns

**Composite Indexes**: multi-column index transforms 2D query into 1D scan
- Order matters: put most selective column first

**Covering Indexes**: include all needed columns in the index → query returns directly from index without touching table rows (faster reads; slower writes)

**Partial Indexes**: index only rows matching a WHERE condition → smaller index, faster queries for specific subsets (e.g., active records only)
