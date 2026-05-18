---
title: "Hello Interview — Key Technology: DynamoDB"
source: "https://www.notion.so/1ffafa27ec7280c793d6d2172b670b12"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/DynamoDB]]"
---

# Key Technology: DynamoDB

Fully-managed AWS service; automatically scales; key-value + document store.

## Data Model

- **Tables**: mandatory primary key; support secondary indexes
- **Items** (rows): primary key + up to 400KB of attributes
- **Attributes**: key-value pairs; scalar types, set types, nested/complex structures
- **Schema-less**: items in same table can have different attributes

## Primary Key Structure

```
Primary Key = {Partition Key} : {Sort Key (optional)}
```

- Partition Key → consistent hashing determines node
- Sort Key → B-tree determines sort order within partition

## Secondary Indexes

| Feature | GSI (Global Secondary Index) | LSI (Local Secondary Index) |
|---------|------------------------------|------------------------------|
| Partition Key | Different from base table | Same as base table |
| Sort Key | Optional, different | Different sort key |
| Consistency | Eventually consistent only | Strongly consistent supported |
| Throughput | Separate RCU/WCU | Shared with base table |
| Size limit | None | 10 GB per partition key |
| Max count | 20 per table | 5 per table |
| Deletion | Safe (independent) | Cannot delete without dropping table |

**Example**: Chat app — `chat_id + message_id` as primary key; `user_id + message_id` as GSI for user's messages

## Consistency Modes

**Eventually consistent (default)**:
- Writes to primary replica → async replication to secondary replicas
- Reads may serve slightly stale data
- 0.5 RCU per 4KB; lower latency

**Strongly consistent**:
- Routes directly to leader node; most up-to-date data
- 1 RCU per 4KB; higher latency

## Scalability

- **Auto-sharding**: automatically distributes data as table grows
- **Global Tables**: cross-region replication for multi-region low latency
- Throughput: single shard supports 4MB reads/sec + 1MB writes/sec

## Advanced Features

### DAX (DynamoDB Accelerator)
- Built-in in-memory cache; no application code changes needed
- Read-through + write-through
- Item cache (GetItem) + query cache (Query/Scan results)

### DynamoDB Streams (CDC)
- Built-in change data capture
- Use cases: sync with Elasticsearch, real-time analytics, change notifications

## Transactions

DynamoDB supports **ACID properties and transactions** (often forgotten in interviews). Multiple item operations across one or more tables in a single atomic operation.

## CAP Position

Primarily **AP** (availability + partition tolerance) by default. Strongly consistent reads provide CP semantics for specific operations.

## Pricing

- On-demand (unpredictable workload)
- Provisioned capacity (predictable workload, billed hourly)

## When to Use

**Good fit**: serverless apps; AWS ecosystem; key-value/document patterns; need sub-millisecond latency at scale; unpredictable traffic (on-demand mode)

**Limitations**:
- Cost at high throughput
- No complex queries (no JOINs)
- Data modeling constraints (don't over-use GSI/LSI)
- Vendor lock-in (AWS only)
