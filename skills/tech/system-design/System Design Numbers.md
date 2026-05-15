---
title: System Design Numbers
category: tech/system-design
tags: [capacity-planning, back-of-envelope, numbers, throughput, latency, scaling-triggers, caching, database, app-server, message-queue, benchmarks]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# System Design Numbers

## Knowledge Map
- 前置知识：[[Distributed Systems]], [[Sharding and Scalability]], [[Database Indexing]]
- 延伸话题：[[Cache and Consistency]], [[Message Queue]], [[Sharding and Scalability]]
- 管理关联：

## Core Concepts

- **Capacity Reference Table** — memorize these to anchor every design decision:

  | Component | Key Metrics | Scale Triggers |
  |-----------|-------------|----------------|
  | **Cache (Redis)** | ~1ms latency; 100K+ ops/sec; memory-bound up to 1TB | Hit rate <80%; latency >1ms; memory usage >80%; cache thrashing |
  | **Database (Postgres)** | Up to 50K TPS; sub-5ms read latency (cached); 64 TiB+ storage | Writes >10K TPS; read latency >5ms uncached; geographic distribution needed |
  | **App Servers** | 100K+ concurrent connections; 8–64 cores @ 2–4 GHz; 64–512 GB RAM (up to 2TB) | CPU >70%; response latency >SLA; connections near 100K/instance; memory >80% |
  | **Message Queue (Kafka)** | Up to 1M msgs/sec per broker; sub-5ms end-to-end latency; up to 50TB storage | Throughput near 800K msgs/sec; partition count ~200K per cluster; growing consumer lag |

- **Latency hierarchy (for back-of-envelope reasoning)**:
  - Memory access: ~1 ns
  - SSD random read: ~100 μs (0.1 ms)
  - Redis (in-memory cache): ~1 ms
  - Database read (cached): sub-5 ms
  - Database read (uncached, SSD): ~10 ms — not 100ms (common overestimate)
  - Same-datacenter network round trip: 1–10 ms
  - Cross-continent (NY → London): ~56 ms minimum (speed of light)

- **TPS estimation formula**:
  - Average TPS = DAU ÷ 100,000 seconds (86,400 seconds in a day, round up)
  - Peak TPS = average × 3–10× (use 3× for stable products, 10× for flash-sale style traffic)
  - Example: 100M DAU → ~1,000 avg TPS → ~3,000–10,000 peak TPS

- **Common interview mistake — premature sharding**: most products at normal scale don't need it.
  - Yelp, LeetCode leaderboard: single Postgres handles terabytes of data without sharding.
  - A single Postgres instance handles ~50K TPS and 64 TiB+ storage — don't shard until you have math proving you've exceeded this.

- **Common interview mistake — overestimating SSD latency**: SSD is ~10 ms (not 100 ms). Saying "100 ms" in an interview signals calibration is off.

- **Common interview mistake — premature message queue introduction**: a message queue is for async decoupling and burst absorption, not just throughput.
  - At 5K writes/sec, Postgres handles it natively (handles 20K+ writes/sec).
  - Before introducing a queue: consider batch writes, schema/index optimization, connection pooling, async commits for non-critical data.

- **Single-node is more powerful than most engineers assume**:
  - Single databases can handle **terabytes** of data
  - Caches can hold **entire datasets in memory** — a 1 TB Redis instance can hold a lot
  - Message queues are fast enough for **synchronous flows** (sub-5ms) as long as no backlog builds
  - App servers have enough memory for **significant local state and caching**

- **Scaling decision framework (in order)**:
  1. Start with a simple single-node or single-DB solution
  2. Add replicas for read scaling (read-write separation)
  3. Add caching when DB read latency becomes the bottleneck
  4. Add sharding/partitioning when write throughput exceeds single-node capacity
  5. Add message queues when you need async decoupling, not just raw throughput

- **"Show your math" rule**: every architecture proposal should be backed by numbers. Don't say "we need to shard" — say "at 50M DAU with a 10:1 read/write ratio, peak writes hit ~50K TPS, which exceeds single-Postgres capacity, so we shard."

## Key Questions

**Q: What are the throughput limits of a single database, cache, and message queue broker?**
Answer framework: Postgres ~50K TPS; Redis ~100K ops/sec; Kafka ~1M msgs/sec per broker. These are the anchors. Scale trigger for DB: writes >10K TPS or storage hitting TBs. Scale trigger for cache: hit rate <80% or latency >1ms. Scale trigger for Kafka: throughput approaching 800K msgs/sec or consumer lag growing. Most interview systems don't exceed these limits — state single-node first, then justify scaling with math.

**Q: How do you estimate the TPS requirement for a system with 100M DAU?**
Answer framework: 100M DAU ÷ 100K seconds/day ≈ 1,000 avg TPS. Peak is 3–10× average: 3,000–10,000 peak TPS. Read/write ratio shapes the architecture: 100:1 read/write at 10K peak TPS → ~100 peak write TPS (trivially handled by a single DB) + ~9,900 peak read TPS (add read replicas + cache). Numbers drive architecture; architecture without numbers is guessing.

**Q: A candidate proposes sharding for a system with 10M users. How do you evaluate whether that's correct?**
Answer framework: Check the math. 10M users × 5 KB/user = 50 GB — tiny, fits on one DB node easily. Peak writes: 10M DAU ÷ 100K × write ratio — probably under 1K TPS, well within single-Postgres capacity. Sharding at this scale adds operational complexity with no benefit. Correct answer: start single-node, add read replicas if needed, add caching for hot reads. Propose sharding only when storage or write throughput numbers actually demand it.

**Q: When does a message queue become necessary vs when is it premature optimization?**
Answer framework: Necessary when: (1) you need to decouple producer and consumer so either can fail independently; (2) you need to absorb burst traffic the consumer can't process synchronously; (3) you need guaranteed at-least-once delivery with retry. Premature when: write throughput is under ~5–10K/sec (Postgres handles it directly); synchronous confirmation is required (payment, inventory deduction); you're adding queue complexity just for throughput. Before adding a queue: try batch writes, connection pooling, and async commits for non-critical paths.

**Q: An interviewer challenges you: "SSD reads are slow, that's why we need caching." How do you respond?**
Answer framework: Calibrate the numbers. SSD random read latency is ~100 μs (0.1 ms), not 100 ms — a common misconception. A Postgres read of a cached page (OS page cache) is sub-5ms. Caching is still valuable for hot data to reduce DB load and push read latency to ~1ms, but the justification is "reduce DB load and improve P99 latency" not "SSD is too slow to use."

**Q: Walk through the decision process for when to escalate from single-node to distributed architecture.**
Answer framework: Use the five-step escalation ladder: (1) single-node DB → measure; (2) read replicas for read-heavy loads; (3) Redis caching for hot data (hit rate >80% → latency drops from 5ms to 1ms); (4) sharding when writes exceed ~10K TPS sustained; (5) message queue for async decoupling, not just throughput. Each step requires a triggering metric — don't add a layer without demonstrating the previous layer is the bottleneck.

## Summary

System design numbers are the difference between architectural intuition and architectural judgment. The four benchmark numbers every engineer should internalize: Redis ~100K ops/sec at ~1ms; Postgres ~50K TPS on terabytes; App servers ~100K concurrent connections; Kafka ~1M msgs/sec per broker. These are not ceilings to apologize for — they are powerful baselines that eliminate most "we need distributed everything" reflexes.

The most common anti-pattern in system design interviews is proposing distributed complexity before justifying it with math. A system with 10M users and a 10:1 read/write ratio typically generates well under 1,000 peak write TPS — a single well-indexed Postgres handles this trivially. Sharding, message queues, and distributed caches should be introduced only when back-of-envelope calculation shows the simpler layer is the bottleneck. The canonical formula: DAU ÷ 100,000 = average TPS; multiply by 3–10× for peak; apply read/write ratio to determine the exact architecture need.

From an AI Infra perspective, these numbers translate directly to infrastructure sizing: GPU cluster throughput, training job queue depth, model serving latency SLOs. The same "start simple, scale with evidence" principle applies: don't run every training job on a 1,000-GPU cluster when a single A100 suffices. Karpenter-style dynamic node provisioning is the infrastructure equivalent of "add replicas for read scaling" — provision capacity to match actual demand, not anticipated demand.

## Key Terms

**Capacity Benchmarks**
- `Redis ~100K ops/sec` · `Postgres ~50K TPS` · `Kafka ~1M msgs/sec per broker` · `App server ~100K connections`

**Latency Constants**
- `memory ~1ns` · `SSD ~100μs` · `Redis ~1ms` · `DB cached <5ms` · `DB uncached ~10ms` · `NY→London ~56ms`

**Estimation Formulas**
- `avg TPS = DAU ÷ 100K` · `peak TPS = avg × 3–10×` · `read/write ratio → architecture direction`

**Scaling Ladder**
- `single-node → read replicas → caching → sharding → message queue`

**Anti-Patterns**
- `premature sharding` · `premature message queue` · `overestimating SSD latency` · `architecture without math`

## Raw Material
- [[raw_material/tech/system-design/hello-interview/concept-numbers.md]]
