---
title: "Hello Interview — Framework & Overview"
source: "https://www.notion.so/1eaafa27ec7280fdad47fff47ea0486f"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/System Design Interview Framework]]"
---

# Hello Interview — Framework & Overview

## Interview Timeline

1. Requirement (Functional/Non-Functional) - 5 min
2. Core Entity - 2 min
3. API/System interface - 5 min
4. Data flow (optional) - for backend system - no API, like crawler. - 5 min
5. High level design - 10-15 min - functional requirement
6. Deep dive - 10 min - non-functional requirement

## Non-Functional Requirements Checklist

- CAP, availability vs. consistency
- Device/Environment limitation
- Latency
- Throughput/Scalability
- Durability - data persistence, data loss
- Security
- Fault tolerant
- Compliance

## Core Concepts

1. **Scaling** — vertical (bigger) and horizontal (load balancer, more) - how to distribute work - Consistent Hashing
2. **Work Distribution** — load balancer, queueing system, keep load as even as possible
3. **Data Distribution** — in-memory, database sharding/partition, fan-out, results are gathered together (traffic increasing, latency). Synchronization challenges, race conditions and consistency challenges - transition, distributed lock
4. **CAP** — Consistency, Availability and Partition Tolerance. Strong consistency: inventory management systems, booking systems, banking systems
5. **Locking** — ensure one client can access a shared resource at a time. Race condition, multiple clients trying to access the same resource at the same time - data corruption, lost update.
   - Granularity of the lock
   - Duration of the lock
   - Whether we can bypass the lock (optimistic update)
6. **Indexing** — read fast, hash map, sorted list
7. **Indexing in DB** — RDBMS, DynamoDB (secondary indexes)
8. **Specialized Indexes** — geospatial indexes (PostGIS extension), vector databases (high-dimensional data), full-text indexes (ElasticSearch). ElasticSearch builds index via CDC (change data capture - adds latency)
9. **Communication Protocols**
   - HTTP(s)/REST — stateless
   - SSE, Server Sent Event — one direction simpler (integrates into load balancer or firewall)
   - WebSockets (bidirectional) — near realtime, but blends simplicity and scalability (stateful), message broker maintains open connections
10. **Security**
    - Authentication/Authorization (API gateway)
    - Encryption - data in transition SSL/TLS, data at rest DB
    - Data Protection - rate limiting and request throttling
11. **Monitoring**
    - Infrastructure monitoring - cpu, memory, disk, network (Datadog, New Relic)
    - Service level monitoring - request latency, error rates, throughput
    - Application level monitoring - number of users, active sessions, key business metrics (Google Analytics or Mixpanel)

## Key Technologies Summary

### Core Database

- Deep dive one SQL and one NoSQL DB - MySQL and Cassandra
- Product design - SQL, infra design - NoSQL
- Don't do explicit comparison SQL vs. NoSQL; focus on how to resolve the problem

### Relational Databases

- ACID
- SQL joins - powerful but performance bottleneck
- Indexes - B-Tree/Hash Table, multiple indexes, multi-column indexes, specialized indexes (geospatial, full-text)
- Transactions - atomic

### NoSQL

- Data Models: Key Value (Fast Access, simple), Document (schema-less, flexible), Column family (high performance for write, scalable), Graph (relationship)
- Benefits - Flexible Data Models, Scalability, Handling Big Data and Real-Time Web apps
- Consistency Models, from strong to eventual consistency
- Scalability - consistent hashing and/or sharding

### Blob Storage

- Large unstructured blobs - image, video
- Amazon S3 or Google Cloud Storage or Azure Blob
- Upload to get back a URL; use URL to download. CDN as cache
- Durability - replication and erasure coding
- Cost - much cheaper than traditional database $0.023/GB vs $1.25/GB
- Chunking - multipart upload API (resuming)

### Search Optimized Database

- Full-text search - indexing, tokenization, stemming - inverted indexes
- Inverted Indexes - map from words to documents
- Fuzzy Search - tolerates slight misspellings
- ElasticSearch, Postgres GIN indexes, Redis full-text search

### Queue

- Buffers for bursty traffic
- Distribute work across a system (photos editing, video encoding, crawler)
- Decouple producer and consumer
- Messaging Ordering, FIFO, priority
- Retry Mechanisms - exponential delay and max retry
- Dead Letter Queue
- Scaling with Partitions - partition key
- Backpressure - slowing down the production of messages
- Kafka, SQS

### Streams/Event Sourcing

- Event sourcing - a sequence of events, can be replayed
- Stream - retain data for configurable period, support multiple consumers (pub-sub)
- Windowing - calculating hourly or daily aggregates
- Kafka, Flink, Kinesis

### Distributed Lock

- ACID uses transaction locks - short-term; long-term - distribution lock
- Redis or Zookeeper
- Locking Mechanisms: Redis - Redlock
- Lock Expiry - TTL
- Locking Granularity
- Deadlocks: Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait

### Distributed Cache

- Save Aggregated Metrics (heavy computing)
- Reduce Number of DB Queries
- Speed up expensive queries
- Eviction Policy - LRU, FIFO, LFU
- Cache Invalidation Strategy
- Cache Write Strategy: Write-Through (dual-write), Write-Around, Write-back
- Redis and Memcached

### CDN

- Serve users globally; cache based on geographic location
- Eviction policies: TTL, cache invalidation
- Cloudflare, Akamai, Amazon CloudFront

## Common Patterns

- **Simple DB-backed CRUD service with caching** (API Gateway, LB)
- **Async job worker pool** - process lots of data (image, video) - queue SQS (at least once, heartbeat) - Kafka supports replay
- **Two stage architecture** - phase one: fast but inaccurate; phase two: slow but precise - recommendation systems, search engines, route planning
- **Event-Driven Architecture** - react to changes in real-time, highly responsive, scalable, loosely coupled
- **Durable Job Processing** - long-running jobs, hours or days - Kafka, Uber's Cadence (Temporal)
- **Proximity-Based Services** - Uber, Gopuff - Geospatial indexes, PostGIS/Redis geospatial
