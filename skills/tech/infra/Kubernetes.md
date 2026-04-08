---
title: Kubernetes
category: tech/infra
tags: [k8s, container-orchestration, scheduling, pods, deployments, statefulset, rbac, hpa, pv, pvc]
status: draft
priority: high
last_updated: 2026-04-06
created_from_jd:
---

# Kubernetes

## Knowledge Map
- Prerequisites（前置知识）：[[Container Basics]], [[Linux Namespaces]], [[Networking Fundamentals]]
- Related Topics（延伸话题）：[[Kubernetes GPU Scheduling]], [[Karpenter]], [[Service Mesh]], [[etcd]], [[Admission Webhooks]], [[Custom Resource Definitions]]
- Management（管理关联）：[[Platform Team Management]]

## Core Concepts

**Pod**
- The smallest deployable unit in K8s （最小部署单元）; multiple containers share a Network Namespace (localhost reachable) and storage volumes; containers within the same Pod cannot use the same port
- Pod IPs are ephemeral; a **Service** provides a stable virtual IP and DNS name via Label/Selector （标签选择器）

**Scheduling（调度）**
- The Scheduler operates in two phases: **Filter** (eliminate Nodes that don't meet requirements) → **Score** (rank candidates and select the best) （过滤→打分）
- **Taint/Toleration**: a Node carries a "repelling mark" (Taint); a Pod must declare a matching Toleration to be scheduled there — this is the core mechanism for GPU Node isolation （GPU 节点隔离的核心机制）
- **NodeSelector**: Pods proactively target Nodes by Label; combined with Taint/Toleration for precise placement

**Probes（探针）**
- **Liveness Probe**: failure → restart the Pod (detects if the process is alive) （检测是否存活）
- **Readiness Probe**: failure → remove Pod from the Service endpoint without restarting (detects if it can accept traffic) （检测是否可接流量）
- `initialDelaySeconds`: gives slow-starting apps (e.g., JVM) time to initialize before probes begin, preventing false kills

**Deployment / HPA / Rolling Updates（滚动发布）**
- Deployment = ReplicaSet (maintains replica count) + rolling update + rollback support
- `maxSurge`: max extra new Pods created during rollout; `maxUnavailable`: max Pods allowed to be unavailable (hard guarantee) （硬性保证）
- If new Pods never reach Ready before timeout → automatic rollback; also supports `kubectl rollout undo`
- **HPA**: auto-scales horizontally based on CPU/memory/custom metrics （水平自动扩缩容）

**StatefulSet (stateful applications — 有状态应用)**
- Each Pod has a fixed identity (pod-0, pod-1) and ordered startup (0→1→2) （有序启动）
- Data persists in PVs; Pods re-attach to the same PV after rescheduling, no data loss
- Migration is complex: delete Pods from highest index down, relying on network storage that can be re-mounted
- Split-brain issues are not handled by K8s; the application layer must resolve them (e.g., MySQL Group Replication) （脑裂问题需应用层解决）

**PV / PVC / StorageClass（持久卷）**
- **PV** (PersistentVolume): actual storage resource — must be network storage so it can be mounted across Nodes
- **PVC** (PersistentVolumeClaim): a Pod's storage request; K8s binds the smallest satisfying PV automatically （最小满足原则）
- **StorageClass**: dynamically provisions PVs on demand; without a matching PV, Pods remain in Pending state

**ConfigMap & Secret**
- ConfigMap: non-sensitive configuration （非敏感配置）; Secret: sensitive data (Base64 + etcd AES encryption + RBAC is the real security stack) （Base64 只是编码不是加密）

**RBAC（权限控制）**
- **Role** (namespace-scoped) / **ClusterRole** (cluster-scoped): define permissions
- **RoleBinding** / **ClusterRoleBinding**: bind permissions to a User/Group/ServiceAccount
- **ServiceAccount**: a Pod's identity for calling the K8s API; the default SA has no extra permissions （Pod 的身份证）

**Cluster Stability（集群稳定性）**
- kubelet sends periodic Heartbeats; `pod-eviction-timeout` controls when to evict Pods after a Node goes silent — too short causes false-positive migration storms on network blips; too long means prolonged unavailability
- If etcd goes down → cluster enters **read-only degraded mode**: existing Pods keep running, but no new resources can be created or modified （只读降级）

## Key Questions

**Q: What is the difference between a Pod and a container? Why does K8s schedule Pods rather than containers directly?**
Answer framework: A Pod is a group of containers sharing a Network Namespace and storage — K8s's smallest scheduling unit. Explain the sidecar pattern (logging/monitoring containers co-located with the main container needing shared networking); clarify why the Pod abstraction is necessary.
> 中文提示：Pod = 共享网络/存储命名空间的容器组；sidecar 模式需要共享网络是 Pod 抽象存在的核心原因

**Q: How does a Service know which Pods to forward traffic to? What happens when a Pod crashes?**
Answer framework: Label/Selector mechanism; a failing Readiness Probe removes the Pod from the Endpoint list automatically; extend to why Probe configuration directly impacts service stability.
> 中文提示：Label/Selector 路由；Readiness Probe 失败自动从 Endpoint 摘除，不重启

**Q: How do you ensure GPU workloads are only scheduled onto GPU Nodes?**
Answer framework: Three-layer mechanism — Taint GPU Nodes (repel ordinary Pods) + Pod declares Toleration (allowed to enter) + NodeSelector/NodeAffinity (target specific GPU model); mention the K8s device plugin that exposes GPU resources.
> 中文提示：Taint + Toleration + NodeAffinity 三层结合；device plugin 暴露 GPU 资源

**Q: How do you guarantee zero downtime during a Deployment rolling update? How do you handle a buggy new version?**
Answer framework: `maxSurge`/`maxUnavailable` control rollout pace; Readiness Probe ensures new Pods are ready before receiving traffic; automatic rollback on timeout + manual `kubectl rollout undo`.
> 中文提示：maxSurge/maxUnavailable 控节奏；Readiness Probe 是安全阀；超时自动回滚

**Q: What is the core difference between StatefulSet and Deployment? When do you use StatefulSet?**
Answer framework: Fixed Pod identity + ordered startup + PV binding; examples: MySQL primary/replica (pod-0 = primary, pod-1 = replica with fixed roles), Kafka (fixed Broker IDs); note PV mount failures and split-brain as common pitfalls.
> 中文提示：固定 Pod ID + 有序启动 + PV 绑定；MySQL 主从、Kafka Broker 是典型场景

**Q: How secure is a Secret? Is Base64 enough?**
Answer framework: Base64 is encoding, not encryption; real security requires etcd AES encryption (at-rest) + RBAC to control access + external Secret management (Vault/KMS) — three layers total.
> 中文提示：三层才真安全：etcd AES 加密 + RBAC + 外部 Secret 管理（Vault/KMS）

**Q: What happens if etcd goes down? How do you ensure etcd high availability?**
Answer framework: Read-only degraded mode (existing Pods keep running; cannot create/modify resources); odd-node count (3/5) with Raft consensus, quorum = majority; explain etcd backup strategy.
> 中文提示：只读降级而非集群崩溃；奇数节点 Raft；备份必须存储在 etcd 节点之外

**Q: A Node suddenly goes silent — how does K8s respond? How do you tune `pod-eviction-timeout`?**
Answer framework: kubelet Heartbeat → Node Controller detects → waits for eviction-timeout → evicts Pods for rescheduling; too short causes migration storms on network blips; too long increases unavailability window; calibrate based on business SLA.
> 中文提示：太短触发迁移风暴（网络抖动误判），太长服务不可用；结合业务 SLA 取值

**Q: Describe the networking model in Kubernetes. How do Pods communicate with each other?**
Answer framework: Flat network model — every Pod gets a unique cluster-wide IP, no NAT between Pods; CNI plugins (Calico, Cilium, Flannel) implement the model; Services provide stable VIPs; CoreDNS for in-cluster DNS resolution; NetworkPolicy restricts Pod-to-Pod traffic.
> 中文提示：每个 Pod 唯一 IP，无 NAT；CNI 插件实现；Service 提供稳定 VIP；NetworkPolicy 限流量

**Q: What is the difference between a Kubernetes Ingress and a Service? When would you use each?**
Answer framework: Service = internal/external L4 load balancing (ClusterIP, NodePort, LoadBalancer types); Ingress = HTTP(S) L7 routing with host/path rules, TLS termination, single entry point for multiple services; use Ingress to avoid provisioning one LoadBalancer per service.
> 中文提示：Service 是 L4，Ingress 是 L7 HTTP 路由；Ingress 节省 LoadBalancer 数量

**Q: How does Kubernetes handle horizontal and vertical scaling?**
Answer framework: Horizontal Pod Autoscaler (HPA) watches CPU/memory/custom metrics, adjusts replica count; Vertical Pod Autoscaler (VPA) adjusts resource requests/limits per container; Cluster Autoscaler adds/removes Nodes based on pending Pods; note HPA and VPA conflict on CPU-based metrics.
> 中文提示：HPA 调副本数，VPA 调 resource request，CA 调节点数；HPA+VPA 同时用要避免 CPU 指标冲突

**Q: How do you secure a Kubernetes cluster? What measures protect both control plane and workloads?**
Answer framework: Control plane — API server authN/authZ (RBAC), TLS everywhere, etcd encryption at rest, audit logging; Workloads — Network Policies (east-west traffic), PodSecurityStandards (privileged container prevention), admission controllers (OPA/Gatekeeper), ServiceAccount least privilege; image scanning in CI/CD pipeline.
> 中文提示：控制面用 RBAC + TLS + etcd 加密；工作负载用 NetworkPolicy + PodSecurityStandards + admission controller

**Q: A pod is stuck in CrashLoopBackOff. Walk through your debugging approach.**
Answer framework: `kubectl logs <pod> --previous` (crashed container logs); `kubectl describe pod` (Events — OOMKilled, image pull errors, failed probes); check resource limits (OOM); inspect liveness/readiness probe config; check init container logs; look at recent Deployment changes (`kubectl rollout history`).
> 中文提示：先看 --previous 日志，再看 describe Events；OOMKilled 调 limits，探针误杀调 initialDelaySeconds

**Q: Design a system to patch the Linux kernel or container runtime across 10,000 nodes in 5 regions with zero downtime.**
Answer framework: Phased rollout (canary per region → staging → prod); zone-aware sequencing (one AZ at a time per region); node drain/cordon + PodDisruptionBudgets to protect workloads during upgrade; automated health checks and rollback gates per phase; GitOps (ArgoCD/Flux) for version tracking; blast radius control by region; maintenance window alignment across time zones.
> 中文提示：分阶段（canary→staging→prod），逐 AZ 操作，PDB 保护工作负载，GitOps 追踪版本，每阶段健康门控

**Q: Design a system to detect noisy-neighbor disk I/O abuse in a multi-tenant Kubernetes cluster and rebalance automatically.**
Answer framework: Real-time per-pod disk I/O metrics (cAdvisor + Prometheus); anomaly detection with threshold triggers; automatic Pod eviction (PriorityClass + preemption) or resource quota enforcement (cgroup limits); QoS class consideration (BestEffort evicted first); avoid thundering herd during rebalancing; notify tenant and log audit trail.
> 中文提示：cAdvisor 采集 per-pod I/O，阈值触发驱逐，按 QoS class 排优先级，避免踩踏

## Summary

Kubernetes is the industry standard for container orchestration, and its core value is **declarative infrastructure**: you describe the desired state, K8s converges to it and maintains it continuously. The key to understanding K8s is the **control loop** (observe → diff → act) — this pattern runs through the Scheduler, kubelet, Deployment Controller, HPA, and every other core component.

From a scheduling perspective, K8s uses Taint/Toleration + NodeSelector to isolate workloads (the foundation of GPU cluster management), HPA for elastic scaling, and `maxSurge`/`maxUnavailable` for zero-downtime deployments. **Readiness Probe** is the safety valve throughout — only truly ready Pods receive traffic, whether during normal operation or a rolling update.

From a storage perspective, PV/PVC decouples storage resources from Pod lifecycle; StatefulSet builds on this to provide fixed identities for stateful applications, at the cost of more complex migration and higher operational overhead. etcd is the single source of truth for the cluster; its high-availability and encryption configuration directly caps the cluster's reliability and security ceiling. For AI Infra scenarios, K8s GPU device plugin, MIG partitioning, and GPU topology-aware scheduling are the specialized directions to master beyond these core concepts.

> 面试重点：控制循环思想（observe → diff → act）贯穿所有组件；Readiness Probe 是零停机发布的安全阀；etcd 高可用是集群可靠性上限

## Raw Material
- [[raw_material/tech/infra/k8s-core]]
