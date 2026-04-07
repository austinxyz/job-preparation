---
title: K8s Control Plane
category: tech/infra
tags: [k8s, kubernetes, control-plane, api-server, etcd, controller-manager, scheduler, kubelet, cri, containerd, webhook, raft, leader-election]
status: draft
priority: high
last_updated: 2026-04-06
created_from_jd:
---

# K8s Control Plane

## Knowledge Map
- Prerequisites（前置知识）：[[Kubernetes]], [[Linux Namespaces]]
- Related Topics（延伸话题）：[[Kubernetes GPU Scheduling]], [[etcd]], [[Admission Webhooks]]
- Management（管理关联）：[[Platform Team Management]]

## Core Concepts

**Request Chain: kubectl apply → etcd → Pod Creation（请求链路）**
- Full chain: `kubectl apply` → API Server → Mutation Webhook → Validation Webhook → etcd → Controller Manager → Scheduler → kubelet → Container Runtime → cgroup
- **API Server**: unified entry point — handles authentication, authorization, and schema validation; all writes pass through Webhooks before reaching etcd （统一入口）
- **Controller Manager**: uses the Watch mechanism to compare desired state vs actual state; writes a pending-schedule Pod when there's a diff; all Controllers run inside Controller Manager — they are not separate processes （非独立进程）
- After Scheduler selects the best Node via Filter → Score, **API Server actively pushes** the assignment to kubelet (kubelet does not poll) （主动推送而非轮询）

**Webhook — Mutation and Validation（准入控制）**
- Mutation Webhook (modify) → Validation Webhook (verify) → write to etcd: modify first, then validate, so etcd always stores valid content
- Typical uses: Mutation auto-injects default requests/limits (fallback safety net); Validation rejects non-compliant resources
- Istio Sidecar injection and Karpenter Node admission both rely on Mutation Webhooks

**Container Runtime — CRI / containerd / Namespace / cgroup**
- kubelet calls the Runtime via **CRI (Container Runtime Interface)**; the mainstream choice is **containerd** (extracted from Docker, donated to CNCF)
- Container fundamentals: **namespace** (isolates Network/Storage/PID resource views) + **cgroup** (enforces CPU/memory usage limits) （隔离视图 + 限制上限）
- VM = OS-level isolation (strong); Container = process-level isolation (lightweight but weaker), sharing the host kernel

**Resources — requests / limits / LimitRange（资源配置）**
- `requests`: the Scheduler's basis for placement — guarantees the Pod can always get this amount （调度保证）
- `limits`: the cgroup hard ceiling enforced at runtime （运行上限）
- CPU exceeds limits → throttled; memory exceeds limits → OOM Kill
- No `requests` → Scheduler places arbitrarily + Pod is evicted first under memory pressure; no `limits` → noisy-neighbor risk can bring down an entire Node
- **LimitRange**: enforces that every Pod in a namespace must set requests/limits; Mutation Webhook can auto-inject defaults for Pods that omit them

**Control Plane High Availability（高可用设计）**
- **API Server**: stateless, multiple instances are natively HA — one failure doesn't stop the cluster
- **Controller Manager** multi-instance: **Leader Election** via Lease lock — the lock holder is the only instance that acts; on crash, the lock expires and another instance claims it （只有 Leader 干活）
- **etcd Raft consensus**: Quorum = n/2+1; 5 nodes tolerate 2 failures; odd node counts recommended (even counts don't improve fault tolerance and introduce split-brain risk) （奇数节点）

## Key Questions

**Q: After `kubectl apply`, which components does a Pod pass through before it runs? What does each do?**
Answer framework: 9-step chain (API Server → Webhook → etcd → Controller Manager → Scheduler → kubelet → CRI → cgroup); emphasize each component does exactly one thing and communicates through etcd; Mutation comes before Validation.
> 中文提示：九环节各司其职，通过 etcd 解耦；Mutation 在 Validation 之前，确保 etcd 存的内容合规

**Q: What is the difference between a Mutation Webhook and a Validation Webhook? When do you use each?**
Answer framework: Mutation = modifies the request (auto-injects values — Sidecar injection, default resources); Validation = verifies the request (rejects non-compliant); order is Mutation → Validation; Validation checks the mutated content; in practice the two are combined for Policy-as-Code.
> 中文提示：先改后验；Mutation 补默认值（Sidecar 注入），Validation 拒绝非法配置

**Q: What is the difference between `requests` and `limits`? What happens if you omit them?**
Answer framework: requests = scheduling guarantee (Scheduler's basis); limits = runtime ceiling (cgroup enforced); no requests → arbitrary placement + first-to-be-evicted; no limits → noisy-neighbor risk; LimitRange + Mutation Webhook is the systematic solution.
> 中文提示：requests 是调度依据，limits 是 cgroup 强制上限；不设的后果各不同，系统性方案是 LimitRange + Webhook

**Q: Why doesn't Controller Manager run multiple instances that cause duplicate operations? How does Leader Election work?**
Answer framework: Lease lock (not etcd/Raft): the Leader renews periodically; on crash, the lock expires; another instance claims it and becomes the new Leader. Keep this distinct from etcd Raft — these are two separate mechanisms.
> 中文提示：Lease 锁 ≠ etcd Raft；Leader Election 用 Lease 续约，挂掉后锁过期触发新 Leader 选举

**Q: etcd 3-node vs 5-node — how do you choose? Why are odd counts recommended?**
Answer framework: 3 nodes tolerate 1 failure; 5 nodes tolerate 2 failures; even counts (4/6) have the same fault tolerance as the next lower odd count but cost one more node and risk a 2+2 split-brain; production typically uses 3 or 5 nodes.
> 中文提示：偶数不增加容错能力但多付成本；推荐奇数；生产通常 3 或 5 节点

**Q: What is the relationship between containerd and Docker? Why did K8s deprecate Docker?**
Answer framework: containerd was extracted from Docker as a standalone container lifecycle management component; what K8s deprecated was dockershim (the entire Docker stack as a CRI implementation), not the image format; developers still use `docker build`; containerd runs those images just fine.
> 中文提示：弃用的是 dockershim（整套 Docker 作为 Runtime），不是 OCI 镜像格式；开发者无感知

## Summary

The core design philosophy of the K8s Control Plane is **single responsibility + decoupling through etcd**: API Server handles validation and routing, Controller Manager handles state convergence, Scheduler handles scheduling decisions, kubelet handles execution — each component does exactly one thing and collaborates by watching etcd rather than calling each other directly. This design allows each component to scale independently and lets the cluster partially work even when some components fail.

Webhooks are the extension points of the Control Plane, and the injection mechanism for Istio, Karpenter, and OPA. Understanding the Mutation (modify) → Validation (verify) → etcd sequence is critical for debugging strategy: when a Pod creation fails, check Webhook logs first, then Controller Manager, then kubelet.

For high availability, three components use three different mechanisms: API Server is stateless multi-instance, Controller Manager uses Lease lock Leader Election, etcd uses Raft Quorum. Distinguishing these three mechanisms is a common interview depth probe — especially that Leader Election uses a Lease lock rather than etcd Raft, which is an easy source of confusion.

> 面试重点：九环节链路必须背下来；Mutation→Validation 顺序；三组件三套 HA 机制（无状态/Lease 锁/Raft）要区分清楚

## Raw Material
- [[raw_material/tech/infra/k8s-controlplane-table]]
