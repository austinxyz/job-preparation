---
title: etcd
category: tech/infra
tags: [etcd, raft, consensus, distributed-kv, kubernetes, leader-election, watch, quorum]
status: draft
priority: medium
last_updated: 2026-04-06
created_from_jd:
---

# etcd

## Knowledge Map
- Prerequisites（前置知识）：[[Distributed Systems]]
- Related Topics（延伸话题）：[[Kubernetes]], [[K8s Control Plane]]
- Management（管理关联）：

## Core Concepts

**What etcd Is（强一致分布式键值存储）**
- etcd = a strongly consistent **distributed key-value store** (Distributed KV Store), used to store critical cluster configuration and state data
- In K8s, etcd is the **sole state store**: all K8s resource desired and actual states (Pod, Deployment, Service, etc.) are stored in etcd
- All components access etcd through the **API Server** — no component connects to etcd directly; the API Server is etcd's only client

**Raft Consensus Algorithm（Raft 共识算法）**
- etcd uses **Raft** to guarantee strong data consistency across multiple nodes (CP system)
- Core mechanism: **Leader receives all write requests** → replicates log entries to Followers → **Quorum (n/2+1) nodes confirm** → write is considered committed （多数派确认才算 committed）
- Quorum guarantee: even with partial node failures, the cluster remains readable/writable as long as a majority survives; prevents split-brain (only one Leader at any time)
- Leader election: Follower times out without a Leader heartbeat → triggers election → candidate with majority votes becomes the new Leader

**Node Count Selection（节点数量选择）**
- Odd node counts recommended (3, 5, 7):
  - 3 nodes: tolerates 1 failure (Quorum=2)
  - 5 nodes: tolerates 2 failures (Quorum=3)
  - 7 nodes: tolerates 3 failures (Quorum=4, but write latency increases noticeably)
- Even node counts (4, 6): same fault tolerance as the next lower odd count, cost one more node, and theoretically risk a 2+2 split-brain → **not recommended** （不推荐偶数）
- Production recommendation: 3 nodes (small clusters) or 5 nodes (large clusters / high-availability requirements); beyond 7 nodes, Raft write latency degrades significantly

**etcd Failure Impact on K8s（故障影响）**
- etcd fully unavailable → **cluster read-only degraded mode**:
  - Existing Pods keep running (kubelet uses local state, doesn't depend on real-time etcd access) （已有 Pod 继续运行）
  - **Cannot create, modify, or delete any K8s resources** (all API Server write operations fail)
  - Scheduler and Controller Manager stop working (cannot read new state)
- Partial etcd node failure (quorum still holds): cluster operates normally; failed nodes auto-sync on recovery

**Watch Mechanism（Watch 推送机制）**
- etcd supports a **Watch API**: clients watch a key or key prefix; etcd actively pushes events when changes occur
- All K8s components (Controller Manager, Scheduler, kubelet) use the Watch mechanism to detect state changes — no polling
- This is the underlying driver of the K8s control loop (observe → diff → act) （控制循环的底层驱动）

**Data Security（数据安全）**
- etcd stores K8s Secrets (certificates, passwords, tokens) → **at-rest encryption** (AES) must be enabled
- Access control: only API Server is permitted to connect to etcd; mTLS between etcd and API Server
- **Backup strategy**: periodic `etcdctl snapshot save`; production environments should back up at least hourly; backups stored outside etcd nodes

## Key Questions

**Q: What is etcd's role in K8s? What happens to the cluster if it goes down?**
Answer framework: etcd = K8s's single source of truth, all resource state stored there; on failure: read-only degraded mode (existing Pods keep running; cannot create/modify resources; Scheduler/Controller Manager stop working); emphasize "read-only degraded" not "cluster crash" — running workloads are unaffected.
> 中文提示：只读降级而非集群崩溃；已运行的 Pod 不受影响；API Server 写操作全部失败

**Q: Why does etcd recommend odd node counts? How do you choose between 3 and 5 nodes?**
Answer framework: Quorum = n/2+1; even counts have the same fault tolerance as the next lower odd count — pay for one extra node and risk theoretical split-brain; 3 nodes tolerates 1 failure, good for small clusters; 5 nodes tolerates 2 failures, good for production high availability; beyond 7 nodes, Raft write latency degrades significantly.
> 中文提示：偶数节点容错能力 = 少 1 个奇数，多付成本且有脑裂风险；生产用 3 或 5

**Q: How does etcd's Watch mechanism work? Why does K8s use Watch rather than polling?**
Answer framework: Client watches a key prefix; etcd pushes events when changes occur (client does not poll); all K8s controllers are Watch-driven (Controller Manager, Scheduler); Watch advantages: low latency (immediate notification on change), low overhead (no polling), precise (only receive changes to watched keys).
> 中文提示：etcd 主动推送而非客户端轮询；这是 K8s 控制循环低延迟响应的底层原因

**Q: How is etcd's data security guaranteed?**
Answer framework: Three layers: ① at-rest encryption (AES encrypts etcd storage — protects against disk theft); ② mTLS (encrypted communication + mutual authentication between API Server and etcd); ③ RBAC (only API Server can access etcd, other components cannot connect directly); plus periodic backups (etcdctl snapshot, stored externally).
> 中文提示：三层：at-rest AES 加密 + mTLS 传输加密 + RBAC 访问控制；加上定期备份存外部

## Summary

etcd is K8s cluster's "database" — but not a general-purpose database. It is a distributed system specifically optimized for **strongly consistent configuration storage**, with Raft consensus at its core to guarantee multi-replica data consistency. K8s's entire control loop (observe → diff → act) depends on etcd's Watch mechanism: Controller Manager watches Pod state changes, Scheduler watches pending-schedule Pods, kubelet watches Pods assigned to its Node.

etcd's importance to K8s means its high-availability configuration is the highest priority in cluster design: odd node count, cross-availability-zone deployment (3 nodes across 3 AZs), at-rest encryption, and regular backups are the standard production configuration. etcd's "read-only degraded" failure behavior is a common interview topic — running workloads are unaffected, but no new resources can be created; this is key to understanding K8s's fault tolerance model.

From an AI Infra perspective, etcd stability directly affects GPU training cluster operations: etcd jitter (increased write latency) causes Pod scheduling delays, impacting training job startup times; etcd data corruption (without backup) can cause GPU resource allocation state inconsistency. Large-scale GPU clusters (1000+ GPUs) face real operational challenges with etcd performance tuning (write QPS, Watch connection count).

> 面试重点：etcd = K8s 唯一状态存储 → Raft Quorum（奇数节点原因）→ 故障只读降级（已有 Pod 继续运行）→ Watch 机制（控制循环驱动）→ 三层安全（加密+mTLS+RBAC）

## Raw Material
