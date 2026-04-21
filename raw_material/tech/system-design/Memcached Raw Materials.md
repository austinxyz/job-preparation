---
title: Memcached Raw Materials
source: multiple (see sections)
date_saved: 2026-04-21
processed: true
skill_note: "[[skills/tech/system-design/Memcached]]"
---

# Memcached Raw Materials

Compiled raw material for the Memcached skill note. Four sources covering: Facebook scaling paper (architecture at extreme scale), Memcached internals (slab + LRU), AWS engine comparison (selection criteria), and Pinterest production deployment (modern real-world usage).

---

## Source 1 — Scaling Memcache at Facebook (NSDI 2013)

**Source:** Micah Lerner summary — https://www.micahlerner.com/2021/05/31/scaling-memcache-at-facebook.html
**Original paper:** Nishtala et al., USENIX NSDI 2013
**Why it matters:** The canonical reference for running Memcached at extreme scale. Every mechanism here — leases, gutter pool, regional replication, mcrouter — is a likely interview question for infra manager roles.

### Overview

Facebook built a distributed key-value caching system on memcached to serve millions of requests per second. The system scaled from single clusters to multi-regional deployments. Primary concerns: latency, load on backing datastores, and eventual consistency across regions. Paper handles billions of requests per second and holds trillions of items.

### 1. Lease Mechanism

**Purpose:** Addresses two critical problems:
- **Stale Sets:** Prevent old data from overwriting newer values
- **Thundering Herds:** Handle scenarios where many clients request the same uncached key

**Implementation:**
- Backend servers track the most recent lease issued per key
- Writes from older leases are blocked
- Leases distributed at constant rate to prevent cache miss storms
- When multiple clients request same key: first lease holder fetches from database, others retry and succeed from cache

### 2. Gutter Pool for Node Failure

**Mechanism:** Automatic failure recovery system that activates when memcache clients cannot reach a server.

**Key Details:**
- Gutter = ~1% of memcached servers in a cluster, dedicated as fallback
- When a client gets no response: retry to Gutter pool
- If second request misses: client inserts key-value pair into Gutter machine after querying DB
- Explicitly avoids redistributing keys to healthy servers (risk of overload cascade)
- Prevents failure cascade in large clusters with frequent hardware failures

### 3. Memcache Pools Separation

**Motivation:** Different datasets have varying churn rates; high-churn items evict long-lived keys via LRU.

**Solution:**
- Separate pools for datasets with different update frequencies (e.g., wildcard pool vs specialized pools)
- Infrastructure sized appropriately per pool type
- Reduces unnecessary evictions of stable data

### 4. Regional Replication Architecture

**Master-Slave Model:**
- One region designated as master, others as slaves
- System accepts eventual consistency
- MySQL replication keeps databases synchronized across regions

**Cache Invalidation Timing:**
- Cache invalidations generated from MySQL commit log in master region only
- Invalidations appear in slave regions only after replication lag
- Prevents invalidations arriving before database acknowledges changes

**Stale Read Mitigation — Remote Marker Mechanism:**
- Web servers set markers on keys requiring consistency guarantees
- Marker contains target region identifier
- Deletes value from local region cache
- Future reads redirected to marked region
- Reduces but doesn't eliminate stale reads in eventually-consistent system

### 5. Cold Cluster Warmup

**Problem:** Newly initialized clusters have empty caches, causing database load spikes.

**Solution:** Cold clusters forward requests to warm clusters with established hit rates until achieving acceptable cache saturation levels.

### 6. Mcrouter / Routing Layer

**Function:** Proxy between web servers and memcache servers.

**Features:**
- Exposes same interface as memcache server
- Maintains TCP connections with web server threads
- Routes and distributes load across servers
- Enables connection coalescing

**Protocol Selection:**
- **TCP:** Used for state-mutating requests (set, delete) for reliability
- **UDP:** Used for read requests (get) to avoid connection overhead
- Rationale: Maintaining TCP connections from all web server threads to all memcache servers incurs prohibitive cost

### 7. Connection Coalescing

Through mcrouter, multiple client connections consolidated into fewer server connections, reducing resource overhead and improving efficiency.

### 8. Sliding Window Protocol for Incast Congestion Control

**Implementation:** Memcache clients restricted from issuing unbounded requests.

**Details:**
- Configurable limit (n) on concurrent in-flight requests per client
- Requests exceeding limit placed in queue
- Reduces network contention and associated latency
- Production data showed effectiveness without impacting normally-operating clients

### 9. Key Design Decisions and Tradeoffs

| Decision | Rationale |
|----------|-----------|
| Simplicity over advanced features | Enables tailoring to use case; advanced functionality added as needed |
| UDP for reads, TCP for writes | Balances reliability with connection overhead |
| Eventual consistency across regions | Acceptable given data volume and geographic distribution |
| Lease-based thundering herd mitigation | Prevents stampedes on cache misses |
| Regional pools | Reduces data duplication and inter-cluster replication traffic |
| MySQL commit log as invalidation source | Guarantees invalidations follow database changes; enables batching |

**Design Philosophy:** Maintain simplicity while making data-driven tradeoffs based on production system behavior.

### Scaling Hierarchy

```
Single Cluster → Multi-cluster Region → Multi-region Deployment
     ↓                  ↓                        ↓
Latency/Load      Replication                Consistency
  Reduction         Management               & Availability
```

---

## Source 2 — Memcached Internals (Slab Allocator + LRU)

**Source:** Memcached GitHub Wiki — https://github.com/memcached/memcached/wiki/UserInternals
**Why it matters:** The slab allocator is the **fundamental architectural difference from Redis** and drives all the operational quirks (memory efficiency, eviction behavior, page assignment lock-in).

### Slab Allocator Architecture

**Memory Division Strategy:**
Memory allocated via the `-m` command-line parameter is reserved for item storage and organized into **1 megabyte pages by default**. Pages are assigned to slab classes as needed and subdivided into fixed-size chunks appropriate for each class.

**Slab Classes:**
Each slab class maintains its own chunk size, item capacity, and independent LRU. Once a page is assigned to a class, it cannot be reassigned — creating a segmented caching model where memcached functions as "many smaller individual caches."

**Size Progression:**
Classes increase in chunk size progressively:
- Class 1: 80 bytes (13,107 chunks per page)
- Class 2: 104 bytes (10,082 chunks per page)
- Class 3: 136 bytes (7,710 chunks per page)
- Higher classes continue to 1 megabyte

Items are stored in the nearest-fit class; a 50-byte item uses class 1 with 30-byte overhead, while a 90-byte item uses class 2 with 14-byte overhead.

### Item Storage and Retrieval

**Item Structure Overhead:**
- **32-bit systems:** 32 bytes per item (without CAS), 40 bytes (with CAS)
- **64-bit systems:** Larger pointers increase overhead but enable greater memory capacity

**Memory Composition:**
Total memory usage includes:
- Item key length
- Internal item data structure
- Item value length
- Hash table overhead for lookups
- Per-connection buffers (minor additional overhead, typically <5%)

### LRU Eviction Mechanism

**Per-Class LRU Management:**
Each slab class maintains its own Least Recently Used queue. Items are evicted at the tail when the slab class exhausts free chunks and no free pages remain.

**Eviction Logic:**
The system searches the LRU tail for expired items first before evicting unexpired data. This approach maximizes reuse of naturally-expired items before forcing premature eviction.

**Eviction Triggers:**
Items are evicted when:
1. Slab class has zero free chunks
2. No free pages exist to assign to the class
3. Item has not expired (expired items are reclaimed first)

### Item Expiration

**Active Expiration (v1.5.0+):**
Modern versions implement active expiration through a periodic crawler that scans the cache and frees expired objects.

**Passive Expiration:**
Fetching an expired item triggers immediate recognition and memory reclamation. Normal cache churn typically reuses its own memory through this mechanism.

**Reclamation Strategy:**
Memory is reclaimed through three pathways:
- Natural expiration discovery during access
- Active crawler scans (modern versions)
- Eviction to accommodate new items

### Threading and Scalability

**Event-Driven Architecture:**
Memcached leverages **libevent for scalable socket handling**, enabling management of tens of thousands of concurrent connections. Each worker thread operates its own independent event loop.

**Thread Model:**
- Individual threads handle their own client connections
- Centralized locks protect shared cache access
- Protocol processing is distributed across threads
- Scales effectively at typical operational loads

### Notable Limitations and Considerations

**Static Slab Assignment:**
The most significant constraint is that page-to-class assignments are permanent. Poor access pattern distribution (e.g., 80% of pages in one class) reduces available capacity for other classes.

**Fragmentation:**
Users can adjust slab classes using the `-f` parameter to optimize for specific workload distributions, though this requires tuning for particular use cases.

**Configuration Optimization:**
The `-vv` verbose flag displays complete slab topology, enabling administrators to verify class distributions match expected access patterns.

---

## Source 3 — AWS ElastiCache: Redis OSS vs. Memcached

**Source:** AWS Official — https://aws.amazon.com/elasticache/redis-vs-memcached/
**Why it matters:** The canonical "which one do I choose" reference. Interviewers ask this constantly.

### Licensing

- **Memcached:** BSD licensed (fully open source)
- **Redis OSS 7.2:** Last fully open source version
- **Redis 8.0+ (Community Edition):** Licensed under AGPLv3 with copyleft provisions

### Feature Comparison

#### Data Structures
- **Redis OSS/CE:** Strings, lists, sets, sorted sets, hashes, bit arrays, and hyperloglogs. Enables advanced use cases like "game leaderboards that keep a list of players sorted by their rank"
- **Memcached:** Basic key-value caching only

#### Persistence & Recovery
- **Redis OSS/CE:** Point-in-time snapshots for archiving and recovery; data retention on disk
- **Memcached:** No built-in persistence

#### Replication & High Availability
- **Redis OSS/CE:** Multiple replicas of a primary node; enables read scaling and highly available clusters
- **Memcached:** No native replication

#### Clustering & Sharding
- **Both:** Data partitioning across multiple nodes for horizontal scaling

#### Multithreading
- **Redis OSS/CE:** Single-threaded architecture
- **Memcached:** Multithreaded; leverages multiple processing cores for higher throughput

#### Pub/Sub Messaging
- **Redis OSS/CE:** Pattern-matching pub/sub for "chat rooms, real-time comment streams, social media feeds, and server intercommunication"
- **Memcached:** Not supported

#### Transactions
- **Redis OSS/CE:** Atomic command grouping via transactions
- **Memcached:** Not supported

#### Lua Scripting
- **Redis OSS/CE:** Transactional Lua script execution
- **Memcached:** Not supported

#### Geospatial Support
- **Redis OSS/CE:** Purpose-built commands for real-time geospatial operations
- **Memcached:** Not supported

### Optimal Use Cases

**Choose Memcached When:**
- Operating the "simplest model" with minimal features
- Running large nodes requiring multiple cores
- Needing dynamic scaling (add/remove nodes by workload)
- Caching objects without advanced features

**Choose Redis OSS When:**
- Advanced data structures are required
- Persistence, replication, or transactions are needed
- Real-time messaging or pub/sub functionality desired
- Complex application scenarios benefit from scripting

### Common Ground
Both offer microsecond latency, developer-friendly APIs, data partitioning, and broad programming language support (Java, Python, PHP, C, C++, C#, JavaScript, Node.js, Ruby, Go).

---

## Source 4 — Pinterest's Cache Infrastructure Scaling

**Source:** Pinterest Engineering on Medium — https://medium.com/pinterest-engineering/scaling-cache-infrastructure-at-pinterest-422d6d294ece
**Why it matters:** The target JD (Pinterest Manager II, Engineering - Infra) — this is exactly how the team you're interviewing at runs Memcached in production.

### Cache Architecture & Fleet Size

Pinterest operates a distributed cache layer spanning thousands of EC2 instances, caching hundreds of terabytes of data. The system handles **150+ million requests per second at peak**, absorbing the majority of backend traffic while reducing latency across services and cutting costs for expensive database backends.

### Memcached Selection

Pinterest chose Memcached as their foundational caching solution for several reasons:

- **Efficiency & Scalability:** The asynchronous, event-driven architecture with multithreading enables horizontal scaling. A single **r5.2xlarge instance sustains "in excess of 100K requests per second"** without latency degradation.
- **Storage Efficiency via Extstore:** This secondary NVMe flash tier expands per-instance capacity from **~55 GB (DRAM) to ~1.7 TB**, dramatically improving capacity-bound workloads without sacrificing latency.
- **Simplicity & Flexibility:** The deliberately minimal design provides no built-in clustering knowledge, enabling flexible abstractions on top.
- **Battle-tested Reliability:** Decades of development with active community support; Pinterest contributes patches upstream.
- **Native Security:** TLS termination support with mutual authentication and SPIFFE-based authorization.

### Mcrouter Integration

Mcrouter, a Layer 7 memcached protocol proxy, forms the critical middle layer:

- Deployed as a service-colocated sidecar proxy on each application instance
- Provides a single endpoint abstraction to the entire memcached fleet
- Decouples control plane (topology/pools) from data plane (routing policies)
- Enables features like **zone-affinity routing, cross-zone replication, multi-tier caching, and shadow traffic testing**
- Offers built-in observability including percentile latency, throughput metrics, and per-key-prefix analytics

### Data Sharding Strategy

Pinterest implements **consistent hashing** for load distribution:

- Deterministically routes each request to a specific host based on cache key
- Maintains keyspace stability during scaling events — when capacity changes, "most of a keyspace partition maps to the same server"
- Enables transparent horizontal scaling with localized hit-rate impact
- Client-side routing abstracts multiple consistently-hashed pools with various policies (AZ-affinity, L1/L2 tiering)

### Failure Handling & High Availability

- **Automatic Failover:** Mcrouter automatically redirects requests from degraded/offline servers to a shared fallback cluster with active health checks for recovery
- **Cross-Zone Replication:** Critical use cases replicate across distinct AWS Availability Zones, enabling "total loss of an AZ with zero downtime"
- **Shadow Testing:** Dark traffic and artificial latency/outage injection for resilience exercises without impacting production

### Pain Points & Solutions

**Trade-offs Addressed:**
- Proxy overhead (compute/I/O) accepted due to high-availability and routing flexibility benefits
- Global configuration risk mitigated through careful change management despite fleet-wide deployments
- Multiple cluster sprawl (**~100 distinct clusters**) enables isolation and optimization per use case
- **Hot key imbalance remains unsolved** — abnormal request spikes on specific keys still cause shard overload

### Monitoring & Operations

Rich observability provided by mcrouter includes:
- Percentile request latency tracking
- Throughput sliced by individual client and server dimensions
- Request trends by key prefix and pattern
- Error rates for anomaly detection
- Per-server failure instrumentation enabling rapid remediation

### Key Architectural Features

- **Instance Efficiency:** r5.2xlarge instances handle tens of thousands of concurrent TCP connections
- **Cluster Diversity:** ~100 distinct memcached clusters with varying tenancy, hardware types, and routing policies
- **Protocol Intelligence:** Mcrouter manipulates memcached requests (TTL modification, in-flight compression)

### Future Directions

Pinterest is exploring:
- Embedding memcached directly in application processes for performance-critical cases (eliminating network overhead)
- Multi-region redundancy solutions for enhanced reliability

---

## Cross-Source Synthesis Notes (for processor)

**The "Memcached Story" across all four sources:**

1. **Core design** (Wiki) — Slab allocator + per-class LRU + multithreaded + no persistence. Simple.
2. **Why this simplicity wins** (AWS) — Multithreading for multi-core efficiency, pure cache without DB overhead.
3. **What you must build around it** (Facebook) — Leases, gutter, pools, regional replication, mcrouter. Memcached doesn't give you clustering; you build it.
4. **Modern production reality** (Pinterest) — Extstore for NVMe expansion, mcrouter as sidecar, consistent hashing, ~100 clusters, 150M+ RPS. Hot keys still unsolved.

**Three "must-have" answers for the Pinterest-style interview:**

- **"Why Memcached over Redis?"** → Multi-core throughput, simplicity, extstore for flash-tier expansion, you only need key-value.
- **"How do you run Memcached at scale?"** → Mcrouter for routing/failover, consistent hashing for sharding, gutter-style pool for failure, cross-zone replication for HA.
- **"What's the hardest unsolved problem?"** → Hot key imbalance. Even Pinterest hasn't fully solved it.
