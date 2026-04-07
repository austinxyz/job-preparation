---
title: Database Indexing
category: tech/system-design
tags: [database, indexing, b-plus-tree, composite-index, clustered-index, covering-index, mysql, postgresql, query-optimization]
status: draft
priority: medium
last_updated: 2026-04-06
created_from_jd:
---

# Database Indexing

## Knowledge Map
- Prerequisites（前置知识）：[[Distributed Systems]], [[Cache and Consistency]]
- Related Topics（延伸话题）：[[NoSQL Databases]], [[Sharding and Scalability]]
- Management（管理关联）：[[Technical Roadmap]]

## Core Concepts

**The Essence of Indexing: Reducing Disk IO（减少磁盘 IO）**
- No index → **full table scan**: reads pages from disk into memory one by one; the bottleneck is disk IO, not CPU computation
- Index internals: **B+ tree** (not B-tree): leaf nodes store `index_value + pointer to data row`, sorted by index value, leaves connected by a linked list
- Tree height of 3–4 levels can index billions of records; IO count = tree height; B+ tree nodes can have hundreds of children vs binary trees needing 30+ levels

**Why B+ Trees Support Range Queries（范围查询）**
- Sorted leaf nodes + linked list → find the range start, then traverse the linked list — natively supports `BETWEEN`, `>`, `<`
- vs B-tree (no leaf linked list): must repeatedly return to the root for range traversal, poor range query efficiency

**Composite Index and the Leftmost Prefix Rule（复合索引与最左前缀）**
- With a `(city, age)` composite index: `WHERE city='Beijing'` ✅; `WHERE city='Beijing' AND age=25` ✅; `WHERE age=25` ❌ (skips the leftmost field)
- **Equality fields first, range fields last** (fields after a range field lose index effectiveness) （等值在前，范围在后）
- Having a `(city, age)` composite index means you don't need a separate `city` index (redundant waste)
- Each index is an independent B+ tree; **every write (INSERT/UPDATE/DELETE) updates all indexes** — more indexes = slower writes

**Clustered vs Non-Clustered Index（聚簇索引 vs 非聚簇索引）**
- **Clustered Index**: leaf nodes store the full data row — one IO retrieves the data; only one per table (data has only one physical ordering); MySQL InnoDB uses the primary key as the clustered index by default
- **Non-Clustered Index**: leaf nodes store `index_value + primary key`; retrieving data requires a **table lookup** (回表) back to the clustered index — 2 IOs total
- **Covering Index**: includes all fields the query needs in the index — eliminates the table lookup entirely; e.g., `SELECT name, city WHERE city='Beijing'` with index `(city, name)` — `name` is already in the index

**Index Invalidation Scenarios — Must Know（索引失效场景）**
1. Skipping the leftmost field (violates leftmost prefix rule)
2. Fields after a range field lose effectiveness
3. Applying a function to the field (`WHERE YEAR(created_at) = 2024`) — breaks B+ tree ordering
4. LIKE with a leading wildcard (`WHERE name LIKE '%Zhang%'`) — cannot locate from the root
5. Type mismatch (`WHERE age = '25'` when age is INT) — implicit conversion acts like a function
6. OR with a non-indexed field — one side has no index → full table scan

**Index Design in Practice（索引设计实战）**
- Optimal index design order: **equality fields (high cardinality first) → equality fields (low cardinality) → range fields → covering index append fields**
- Example: `WHERE city='Beijing' AND age BETWEEN 18-25 AND register_date > 30 days ago, SELECT user_id, name`
  → Optimal index: `(city, age, register_date, user_id, name)` (register_date is a range field, placed last; user_id/name added to achieve covering index)

## Key Questions

**Q: What is a B+ tree? Why do databases use B+ trees rather than binary trees or hash indexes?**
Answer framework: B+ tree is short and wide (tree height 3–4 vs binary tree's 30+ levels), fewer IO operations; leaf linked list supports range queries (hash doesn't); disk IO is the bottleneck and tree height directly determines IO count; B+ tree is optimized for disk IO; B-tree is B+ tree's predecessor (no leaf linked list, poor range queries).
> 中文提示：树高 = IO 次数；叶子链表支持范围查询；磁盘 IO 是瓶颈，不是 CPU

**Q: What is the difference between a clustered and non-clustered index? What is a table lookup (回表)?**
Answer framework: Clustered index stores the full data row in the leaf — one IO; non-clustered stores the primary key — data retrieval requires a table lookup back to the clustered index (2 IOs total); one table can only have one clustered index (one physical ordering); covering index eliminates table lookups (includes all returned fields in the index).
> 中文提示：聚簇 = 叶子存完整行，1 次 IO；非聚簇 = 叶子存主键，需回表共 2 次 IO；覆盖索引消除回表

**Q: What are the rules for field ordering in a composite index? Why must range fields be placed last?**
Answer framework: Leftmost prefix rule (must match from the leftmost field); equality first, range last (fields after range lose effectiveness, because B+ tree cannot continue precise navigation after a range scan); state the common intuition error: many people put range fields first (wrong) — equality fields narrow the search space, then the range scan.
> 中文提示：最左前缀；等值在前、范围在后；范围字段后的字段索引失效，根本原因是 B+树无法继续精确定位

**Q: Are more indexes always better? What is the cost of having many indexes?**
Answer framework: No. Each index is an independent B+ tree; every write updates all related indexes; more indexes → slower writes, more storage; build indexes based on actual query needs; read-heavy systems can afford more indexes; write-heavy systems (e.g., log tables) must be cautious; use EXPLAIN regularly to analyze slow queries, don't add indexes blindly.
> 中文提示：索引越多写入越慢；每次写入更新所有相关 B+树；按实际查询需求建索引，用 EXPLAIN 指导

**Q: In what situations does an index become ineffective? What is the root cause?**
Answer framework: 6 invalidation scenarios (see above); root cause: **all of them break the B+ tree's ordering, preventing the database from locating contiguous data starting from the root**; proactively mention function application and type mismatch (often overlooked); fix: rewrite queries to avoid functions (e.g., `created_at >= '2024-01-01'` instead of `YEAR(created_at) = 2024`).
> 中文提示：根本原因都是破坏了 B+树有序性；函数操作和类型不匹配是最容易被忽视的两个

## Summary

Database indexing is fundamentally a trade of space (extra B+ trees) for time (fewer disk IOs). The B+ tree's short-wide structure (3–4 levels for billions of records) and leaf node linked list (native range query support) are the core reasons it is the standard choice for database indexes. Understanding "tree height = IO count" is the foundation for understanding every index design decision.

Three key rules for composite indexes: ① Leftmost prefix (must match from the leftmost field); ② Equality before range (range field and beyond lose effectiveness); ③ Covering index (add returned fields to the index to eliminate table lookups). All three rules stem from the same underlying principle — how the B+ tree navigates — so once you understand the structure, memorization is unnecessary.

Index design engineering advice: start with the slow query log (find full table scans), analyze execution plans with EXPLAIN, and design indexes for actual query patterns rather than intuition. Write-heavy tables (e.g., log tables) require extreme caution with index count; read-heavy tables (e.g., user tables, product tables) can accommodate more indexes.

> 面试重点：B+树为什么矮胖（树高=IO次数）→ 聚簇 vs 非聚簇（回表）→ 复合索引三规则（最左/等值在前/覆盖索引）→ 索引失效根本原因

## Raw Material
- [[raw_material/tech/system-design/sd-db-index]]
