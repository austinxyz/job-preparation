---
title: "Hello Interview — Core Concept: Numbers Every Engineer Should Know"
source: "https://www.notion.so/1f9afa27ec728020b81ace09c0033aa1"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/System Design Numbers]]"
---

# Core Concept: Numbers Every Engineer Should Know

## Capacity Reference Table

| Component | Key Metrics | Scale Triggers |
|-----------|-------------|----------------|
| **Caching** | ~1ms latency; 100K+ ops/sec; memory-bound (up to 1TB) | Hit rate <80%; latency >1ms; memory usage >80%; cache thrashing |
| **Databases** | Up to 50K TPS; sub-5ms read latency (cached); 64 TiB+ storage | Write throughput >10K TPS; read latency >5ms uncached; geographic distribution needs |
| **App Servers** | 100K+ concurrent connections; 8-64 cores @ 2-4 GHz; 64-512 GB RAM (up to 2TB) | CPU >70%; response latency >SLA; connections near 100K/instance; memory >80% |
| **Message Queues** | Up to 1M msgs/sec per broker; sub-5ms end-to-end latency; up to 50TB storage | Throughput near 800K msgs/sec; partition count ~200K per cluster; growing consumer lag |

## Common Interview Mistakes

- **Premature sharding**: Yelp, LeetCode leaderboard don't need sharding at normal scale. Single Postgres handles terabytes.
- **Overestimating latency**: SSD is ~10ms, not 100ms
- **Over-engineering write throughput**: 5K writes/sec → no need for message queue; Postgres handles 20K+ writes/sec
  - Before message queue: consider batch writes, schema/index optimization, connection pooling, async commits for non-critical writes

## Key Takeaways

- **Single databases can handle terabytes** of data
- **Caches can hold entire datasets in memory** — don't rush to add complexity
- **Message queues are fast enough for synchronous flows** (as long as no backlog)
- **App servers have enough memory** for significant local optimization

## Decision Framework

1. Start with simple single-node or single-DB solution
2. Add replicas for read scaling
3. Add caching when DB read latency becomes a bottleneck
4. Add sharding/partitioning when write throughput exceeds single-node capacity
5. Add message queues when you need async decoupling, not just throughput
