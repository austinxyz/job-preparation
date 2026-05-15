---
title: Hello Interview — Key Technology: Kafka
source: "https://www.notion.so/1feafa27ec7280cab5c5ce6f65f31cde"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/Apache Kafka]]"
---

# Key Technology: Kafka

## Core Concepts

- **Producer** → **Topic** → **Consumer** (consumer group: each message processed by exactly one consumer in group)
- **Broker**: each physical/virtual instance storing data
- **Topic**: logical grouping of partitions; how to organize data
- **Partition**: ordered, immutable sequence of messages; physical unit of scaling; key determines partition
- **Offset**: position in partition; consumers commit offsets back to Kafka

## Message Structure

- Required: value (payload)
- Optional: key (determines partition via hash), timestamp, headers
- Typical size: <1MB; for large data (video) → store in S3, message contains S3 URL

## Partition Determination

1. Key present → hash(key) % numPartitions
2. No key → round-robin (configurable)
3. Broker assignment: cluster metadata maps partition → broker; leader-follower replication

## Storage: Append-Only Log

Each partition = append-only log:
- **Immutability**: new data appended, never modified in-place
- **Efficiency**: sequential disk I/O is fast
- **Scalability**: independent partitions can live on different brokers

## Replication

- **Leader Replica**: handles reads + writes
- **Follower Replicas**: backups; sync from leader
- **Cluster Controller**: monitors broker health; manages leader elections
- `acks=all`: producer waits for all replicas to acknowledge → strongest durability

## Pull-Based Consumption

Consumer polls broker at interval (not server-pushed):
- Consumer controls consumption rate
- Enables efficient batching
- Prevents overwhelming slow consumers
- Better failure handling (consumer can pause without dropping messages)

## When to Add Kafka

- **Async processing**: YouTube video transcoding
- **Ordered processing**: TicketMaster seat booking
- **Decoupling producer/consumer**: scale each independently

**Stream mode** (don't commit offsets):
- Continuous real-time processing: Ads Click aggregation
- Multiple simultaneous consumers: Live Comments

## Scalability

1. Add more brokers → add more partitions (horizontal scaling)
2. **Hot partition mitigation**:
   - Random (no key): loses ordering guarantee
   - Random salting: complicates consumer aggregation
   - Compound key: `adId+regionId` or `adId+userId`
   - Back pressure: slow down producer

## Fault Tolerance

- **Consumer failure**: offset management; Kafka rebalances partitions to remaining consumers
- **When to commit offset**: after successfully processing (not before) to guarantee at-least-once delivery
- **Idempotency**: use unique message IDs to deduplicate re-delivered messages

## Error Handling

- Producer: automatic retries with backoff
- Consumer: Kafka doesn't natively support retries → pattern:
  - Main Topic → Retry Topic → Dead Letter Queue (DLQ)

## Performance Optimizations

- Batch messages in producer
- Compression: GZip, Snappy, LZ4
- Optimal partition strategy for your key distribution

## Retention Policies

- `retention.ms`: time-based (default: 7 days)
- `retention.bytes`: size-based (e.g., 1GB per partition)

## Summary

Always available, sometimes consistent. Purpose-built for high-throughput, durable, distributed event streaming. Suitable for both message queue (ack-based) and stream processing (offset-based replay) patterns.
