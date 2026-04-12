---
title: Kubernetes
category: tech/infra
tags: [k8s, container-orchestration, scheduling, pods, deployments, statefulset, rbac, hpa, pv, pvc]
status: in-progress
priority: high
last_updated: 2026-04-10
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

**Control Plane Architecture**
- **API Server**: the single entry point for all cluster operations — validates/persists objects to etcd, enforces authN/authZ/admission. Stateless and horizontally scalable; multiple replicas behind a load balancer for HA.
- **Controller Manager**: runs reconciliation loops (Deployment Controller, ReplicaSet Controller, Node Controller, etc.). Each controller watches the API Server for object changes and drives actual state toward desired state.
- **Scheduler**: watches for unscheduled Pods → runs Filter + Score → writes `spec.nodeName` back to the API Server. Pluggable; custom schedulers possible for specialized workloads (e.g., gang scheduling for ML training jobs).
- **etcd**: the only stateful component of the control plane. All cluster state lives here. HA requires 3 or 5 nodes (Raft quorum = majority). Losing quorum = read-only degraded mode. etcd should run on dedicated nodes, separate from worker nodes.
- **kubelet**: agent on each worker node. Watches API Server for Pods assigned to its node, drives container runtime (containerd/CRI-O) to start/stop containers, reports node/pod status back.
- **kube-proxy**: runs on every node, programs network rules (iptables or ipvs) for Service VIP → Pod IP translation. IPVS mode is preferred at scale (O(1) rule lookup vs O(n) iptables traversal).

**APF — API Priority and Fairness (K8s 1.20+)**
- Problem: in a large cluster, a chatty controller (e.g., release pipeline making thousands of LIST calls) can exhaust API Server concurrency and starve other clients — cascading to cluster instability.
- APF introduces **PriorityLevelConfigurations** (each with a concurrency quota) and **FlowSchemas** (match rules → priority level). Every API request is classified into a flow and queued/executed within its level's concurrency budget.
- Key metrics: `apiserver_flowcontrol_rejected_requests_total` (requests dropped because queue was full), `apiserver_flowcontrol_current_executing_requests` (in-flight per level).
- Tuning: create separate FlowSchemas for known high-volume clients (monitoring scrapers, CI pipelines, user traffic) and assign them appropriate priority levels and concurrency. Don't leave all clients on the default level.
- **eBay lesson**: APF misconfiguration (app release controllers on the same priority level as platform tooling) caused multiple API Server saturation incidents. Fix: model each client type explicitly in FlowSchemas.

**Resource Requests, Limits, and QoS Classes**
- **Request**: the amount of CPU/memory the scheduler uses for placement decisions. A node won't be selected unless it has enough unallocated resources to satisfy all requests.
- **Limit**: the hard cap at runtime. Exceeding CPU limit → throttling. Exceeding memory limit → OOMKill.
- **QoS Classes** (assigned automatically):
  - **Guaranteed**: `requests == limits` for all containers. Never evicted under resource pressure (except for critical node pressure). Highest scheduling priority. Use for latency-sensitive workloads.
  - **Burstable**: `requests < limits` or only some containers have both. Evicted after BestEffort under pressure. Middle tier.
  - **BestEffort**: no requests or limits set. First to be evicted. For fault-tolerant batch jobs only.
- Best practice: always set requests (for accurate scheduling); set limits for memory (to bound OOM impact); consider leaving CPU limits unset for latency-sensitive workloads (CPU throttling at limit causes unexpected latency spikes even when the node has idle CPU).
- **LimitRange**: sets default and max requests/limits per namespace. Prevents Pods from launching without resource specs.
- **ResourceQuota**: caps total resource consumption per namespace. Essential for multi-tenant clusters.

**DaemonSet**
- Ensures exactly one Pod runs on every node (or a subset matching a NodeSelector/Toleration). Used for: log collectors (Fluent Bit), monitoring agents (node-exporter, cAdvisor), CNI plugins, security scanners.
- Pods are created/deleted automatically as nodes join/leave the cluster.
- Tolerates node taints by default for system-level DaemonSets (`node.kubernetes.io/not-ready`, etc.) — otherwise monitoring would fail on problem nodes, exactly when you need it most.
- Rolling update supported (`RollingUpdate` strategy); `maxUnavailable` controls pace.

**PodDisruptionBudget (PDB)**
- Limits the number of Pods that can be voluntarily disrupted simultaneously — during node drains, cluster upgrades, or evictions.
- `minAvailable: 2` → at least 2 Pods must stay up during disruption. `maxUnavailable: 1` → at most 1 Pod can be unavailable at a time.
- PDB blocks `kubectl drain` if draining a node would violate the budget. This is the mechanism that makes large-scale node upgrades safe without manual coordination.
- Required for any production workload. Without PDB, rolling a 10k-node cluster can accidentally take down an entire service if the upgrade evicts Pods faster than they reschedule.

**Admission Controllers and Webhooks**
- Admission controllers intercept API Server requests *after* authN/authZ, *before* persistence to etcd. Two phases: **Mutating** (modify the object, e.g., inject sidecar, set default resource limits) → **Validating** (accept or reject).
- Built-in controllers: `LimitRanger` (enforce LimitRange), `ResourceQuota`, `PodSecurity` (enforce PodSecurityStandards), `DefaultStorageClass`.
- **MutatingAdmissionWebhook / ValidatingAdmissionWebhook**: call external HTTPS endpoints for custom logic. Power tools like Istio sidecar injection, OPA/Gatekeeper policy enforcement, and image signature verification.
- The webhook call is on the critical path — a slow or unavailable webhook can block all Pod creation. Always set `failurePolicy: Fail` for security-critical webhooks but `Ignore` for non-critical ones; always run webhooks with high availability (≥ 2 replicas).

**CRDs and the Operator Pattern**
- **CRD (Custom Resource Definition)**: extends the K8s API with custom object types. After registering a CRD, you can `kubectl get myresource` just like Pods or Deployments.
- **Operator pattern**: CRD (defines the custom object) + custom Controller (reconciles desired state → actual state). This is how Prometheus Operator, cert-manager, Kafka on K8s, and GPU operator work.
- Why it matters for platform engineering: complex stateful systems (databases, ML training jobs, GPU allocation) need domain-specific reconciliation logic that generic K8s controllers don't provide. Operators encode that operational knowledge into code, making it repeatable and version-controlled.
- Operator development frameworks: Kubebuilder (Go, official), Operator SDK (Go/Ansible/Helm).

**Multi-Tenancy Patterns**
- **Namespace-level**: namespaces provide soft isolation (separate RBAC, ResourceQuota, NetworkPolicy). Simple to operate; workloads still share the same node kernel. Sufficient for most internal multi-team scenarios.
- **Node-level**: dedicated node pools per tenant (Taint + Toleration + NodeSelector). Hard isolation; workloads don't share nodes. More expensive but required for regulatory/security separation.
- **Cluster-level**: separate clusters per tenant. Maximum isolation; highest operational overhead. Typical for multi-org or prod/staging separation.
- Control plane isolation: without APF, a noisy tenant's workload can degrade the API Server for all tenants. APF FlowSchemas per namespace/tenant are the mitigation.
- NetworkPolicy is mandatory for namespace-level multi-tenancy: without it, Pods in one namespace can reach Pods in any other by default.

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

**Q: Walk through the K8s control plane components. What happens from the moment you run `kubectl apply` to a Pod running?**
Answer framework: `kubectl apply` → API Server (authN/authZ/admission/persist to etcd) → Controller Manager detects new ReplicaSet → creates Pod objects (unscheduled) → Scheduler picks up unscheduled Pods, runs Filter+Score, writes nodeName → kubelet on that node watches for its assigned Pods → calls container runtime to pull image and start containers → kubelet reports status back to API Server. Emphasize each component's role and that the API Server is the only component that talks to etcd directly.

**Q: What are K8s QoS classes and how do they affect scheduling and eviction?**
Answer framework: Three classes assigned automatically: Guaranteed (requests==limits, never evicted except critical pressure), Burstable (requests < limits, middle priority), BestEffort (no resources set, first evicted). Practical guidance: always set memory limits to bound OOM blast radius; consider leaving CPU limits unset for latency-sensitive services because throttling at limit causes latency spikes even when the node has spare CPU. LimitRange enforces defaults; ResourceQuota caps namespace totals.

**Q: What is API Priority and Fairness (APF) and when do you need to tune it?**
Answer framework: APF classifies API requests into flows via FlowSchemas, queues them per PriorityLevelConfiguration, and enforces per-level concurrency budgets. Without it, one chatty client (CI pipeline, misconfigured controller) can exhaust API Server concurrency and starve platform tooling. Tune it when: a cluster has heterogeneous clients with very different call patterns; a noisy-neighbor incident has occurred (monitor `apiserver_flowcontrol_rejected_requests_total`). Fix: create explicit FlowSchemas per client type with appropriate priority levels. Close with the eBay experience: APF misconfiguration caused multiple API Server saturation incidents before flow schemas were properly modeled per client.

**Q: How do you safely upgrade Kubernetes nodes at scale? What mechanisms protect workloads?**
Answer framework: Three safety mechanisms working together: (1) PodDisruptionBudget blocks drain if eviction would violate `minAvailable`; (2) node cordon prevents new scheduling while drain completes; (3) Readiness Probes ensure rescheduled Pods are ready before receiving traffic. Rollout strategy: canary → AZ-by-AZ within a region → region-by-region. Automated health gates between phases; pre-provision surge capacity so evicted Pods reschedule immediately. For 10k nodes: GitOps tracks target version, cluster autoscaler pre-scales if needed, automation handles drain/replace in parallel per AZ with PDB as the governor.

**Q: Explain the Operator pattern. Why would you build one instead of using plain Deployments?**
Answer framework: An Operator = CRD (custom object type) + custom Controller (reconciliation loop). Use when the workload needs domain-specific operational logic that generic K8s controllers don't provide: complex stateful systems (databases need coordinated failover, not just restart), batch ML training jobs (need gang scheduling awareness), GPU allocation policies. Examples: Prometheus Operator manages scrape configs as K8s objects; cert-manager automates certificate rotation; GPU Operator configures drivers and device plugins on GPU nodes. Trade-off: more development and maintenance overhead vs. encoding tribal operational knowledge into version-controlled, auditable code.

**Q: How would you design multi-tenancy for a shared Kubernetes cluster serving 20 engineering teams?**
Answer framework: Namespace per team as the baseline (RBAC, ResourceQuota, LimitRange, NetworkPolicy per namespace). APF FlowSchemas per namespace to prevent any team's workload from starving the API Server. NetworkPolicy default-deny within and between namespaces, with explicit allow rules for shared services. For teams with strict isolation requirements (different compliance posture): dedicated node pools via Taint/Toleration. Centralized admission webhooks (OPA/Gatekeeper) enforce org-wide policies (image registry allowlist, required labels, security contexts). Escalation path: namespace-level for most teams, node-level for regulated teams, separate cluster only for highest-sensitivity workloads.

## Summary

Kubernetes is the industry standard for container orchestration, and its core value is **declarative infrastructure**: you describe the desired state, K8s converges to it and maintains it continuously. The key to understanding K8s is the **control loop** (observe → diff → act) — this pattern runs through the Scheduler, kubelet, Deployment Controller, HPA, and every other core component.

From a scheduling perspective, K8s uses Taint/Toleration + NodeSelector to isolate workloads (the foundation of GPU cluster management), HPA for elastic scaling, and `maxSurge`/`maxUnavailable` for zero-downtime deployments. **Readiness Probe** is the safety valve throughout — only truly ready Pods receive traffic, whether during normal operation or a rolling update.

From a storage perspective, PV/PVC decouples storage resources from Pod lifecycle; StatefulSet builds on this to provide fixed identities for stateful applications, at the cost of more complex migration and higher operational overhead. etcd is the single source of truth for the cluster; its high-availability and encryption configuration directly caps the cluster's reliability and security ceiling. For AI Infra scenarios, K8s GPU device plugin, MIG partitioning, and GPU topology-aware scheduling are the specialized directions to master beyond these core concepts.

> 面试重点：控制循环思想（observe → diff → act）贯穿所有组件；Readiness Probe 是零停机发布的安全阀；etcd 高可用是集群可靠性上限

## Raw Material
- [[raw_material/tech/infra/k8s-core]]
