---
title: Kubernetes GPU Scheduling
category: tech/infra
tags: [kubernetes, gpu, device-plugin, mig, gpu-scheduling, taint-toleration, node-affinity, nvidia, resource-quota, topology-aware]
status: draft
priority: high
last_updated: 2026-04-06
created_from_jd:
---

# Kubernetes GPU Scheduling

## Knowledge Map
- Prerequisites（前置知识）：[[Kubernetes]], [[K8s Control Plane]], [[GPU Cluster Management]]
- Related Topics（延伸话题）：[[Karpenter]], [[NCCL and Collective Communication]], [[Distributed Training Frameworks]]
- Management（管理关联）：[[Platform Team Management]]

## Core Concepts

**GPU Resource Exposure: Device Plugin Mechanism（设备插件机制）**
- K8s natively manages only CPU and memory; GPU is an **Extended Resource**, exposed to K8s through a **Device Plugin**
- NVIDIA Device Plugin (runs as a DaemonSet on every GPU Node): ① registers `nvidia.com/gpu` resource with the API Server; ② allocates the specific GPU device when kubelet requests it
- Pod requests a GPU: `resources.limits["nvidia.com/gpu"]: 1`; the Scheduler is aware of GPU counts and schedules to Nodes with sufficient GPUs
- **GPU cannot be overcommitted**: GPU resources can only be requested as integers, unlike CPU which can be oversubscribed （不可过度分配）

**GPU Node Isolation: Taint + Toleration + NodeSelector（节点隔离三件套）**
- Prevent ordinary workloads from occupying GPU Nodes (wasted resources): apply a **Taint** to GPU Nodes (e.g., `nvidia.com/gpu=present:NoSchedule`)
- GPU training Pods must declare the corresponding **Toleration**, otherwise they cannot be scheduled to GPU Nodes
- Precise targeting: **NodeSelector** or **NodeAffinity** to specify GPU model (e.g., `accelerator: nvidia-a100`) — prevents accidentally scheduling to V100 Nodes
- All three combined: Taint repels ordinary Pods → Toleration allows GPU Pods → NodeAffinity targets specific model

**MIG — Multi-Instance GPU Partitioning（多实例 GPU 分区）**
- A100/H100 support **MIG (Multi-Instance GPU)**: hardware-level partition of one GPU into up to 7 independent instances
- Each MIG instance has independent memory, SMs (streaming multiprocessors), and bandwidth — completely isolated (no shared memory controller) （硬件级完全隔离）
- Typical configurations: A100 80GB → 7×10GB or 3×20GB among multiple Profile options
- K8s exposes MIG instances as independent resources via NVIDIA MIG Manager (e.g., `nvidia.com/mig-1g.10gb`)
- **Use cases**: inference services (small models don't need a full GPU), multi-tenant sharing (different users get exclusive MIG instances)

**Topology-Aware Scheduling（拓扑感知调度）**
- Distributed training is extremely sensitive to inter-GPU bandwidth: GPUs within the same NVLink domain have interconnect bandwidth (600 GB/s) far higher than cross-Node InfiniBand (200 GB/s) （带宽差 3 倍）
- **NVIDIA GPU Topology**: within a GPU Node, GPUs interconnect via NVLink (high bandwidth); between Nodes in the same rack via NVLink Switch (NVSwitch); cross-rack via InfiniBand
- K8s native scheduling is not GPU-topology-aware; requires **Topology Manager** (kubelet component) + **CPU Manager** to help allocate GPUs on the same NUMA node
- **Gang Scheduling**: all Worker Pods in distributed training must be **scheduled simultaneously** — otherwise some Pods run waiting for others, wasting GPU resources; native K8s doesn't support this, requires Volcano or Kubeflow Training Operator

**GPU Resource Management Best Practices（资源管理最佳实践）**
- **ResourceQuota**: limits total GPU quota per namespace (prevents a single team from monopolizing all GPUs) （防独占）
- **LimitRange**: limits maximum GPU request per Pod (prevents misconfiguration requesting too many)
- **GPU Timesharing (CUDA MPS / Time-Slicing)**: software-level multi-process GPU sharing, no hardware isolation — suited for low-intensity inference
  - vs MIG: MIG has hardware isolation (secure); Time-Slicing is software sharing (flexible but no isolation)
- **GPU Metrics**: `nvidia-smi` / DCGM (Data Center GPU Manager) collects GPU utilization, memory usage, temperature, power; exposed to Prometheus + Grafana for monitoring

## Key Questions

**Q: Does K8s natively support GPUs? How do you make K8s aware of GPU resources?**
Answer framework: K8s only natively manages CPU/memory; GPU is exposed via the Device Plugin mechanism (NVIDIA Device Plugin as DaemonSet registers `nvidia.com/gpu` resource, kubelet allocates specific devices); Pods request via `resources.limits`; GPUs cannot be overcommitted (integer requests only, no overcommit).
> 中文提示：GPU 通过 Device Plugin 暴露（DaemonSet 注册资源，kubelet 分配设备）；GPU 不可过度分配

**Q: How do you ensure GPU training Pods are only scheduled to GPU Nodes, and ordinary Pods don't occupy GPU Nodes?**
Answer framework: Three-layer mechanism: ① Taint GPU Nodes (repel ordinary Pods); ② training Pods declare Toleration (allowed in); ③ NodeSelector/NodeAffinity (target specific GPU model, precise A100 vs V100 routing); all three are needed — Taint alone without NodeAffinity may schedule to any GPU Node, causing GPU model mismatch with training efficiency differences of several times.
> 中文提示：Taint + Toleration + NodeAffinity 三层缺一不可；只有 Taint 没有 NodeAffinity 可能调到错误 GPU 型号

**Q: What is MIG partitioning? When do you use MIG instead of a full GPU?**
Answer framework: MIG = A100/H100 hardware-level GPU partition (independent memory/SMs/bandwidth, fully isolated); suited for inference services (small models don't need a full GPU) + multi-tenant (different users get exclusive MIG instances, secure isolation); vs Time-Slicing (software-level sharing, no hardware isolation, suited for low-intensity scenarios with low isolation requirements); vs full GPU (large model training needing all memory/compute).
> 中文提示：MIG = 硬件级隔离（适合推理服务和多租户）；Time-Slicing = 软件共享（无隔离，适合低强度）

**Q: Why does distributed training need topology-aware scheduling? What are K8s native scheduling's limitations?**
Answer framework: Same-Node NVLink bandwidth (600 GB/s) vs cross-Node InfiniBand (200 GB/s) — 3x difference; AllReduce communication volume is large, bandwidth difference directly impacts training speed; K8s native Scheduler is not GPU-topology-aware — may schedule 8-GPU training across 2 Nodes (4 GPUs each) when the optimal placement is 8 GPUs on the same Node; requires Topology Manager or dedicated schedulers (Volcano).
> 中文提示：同节点 NVLink（600 GB/s）vs 跨节点 InfiniBand（200 GB/s）差 3 倍；K8s 原生不感知拓扑需要 Volcano

**Q: What is Gang Scheduling? Why does distributed training need it?**
Answer framework: Gang Scheduling = all Worker Pods must be scheduled simultaneously (all-or-nothing); without Gang Scheduling: some Pods scheduled successfully wait — occupying GPU resources without training (waste); other Pods fail to schedule waiting for resources — forming deadlock (mutual waiting); K8s doesn't natively support it, requires Volcano or Kubeflow Training Operator.
> 中文提示：全有或全无；缺 Gang Scheduling：部分 Pod 占 GPU 不训练（浪费），其他 Pod 等资源（死锁）

## Summary

K8s GPU scheduling layers AI workload-specific requirements on top of general container scheduling: GPU resource exposure (Device Plugin), isolation (Taint/MIG), topology awareness (NVLink/InfiniBand bandwidth differences), and training task requirements (Gang Scheduling). Each layer exists because AI training scenarios differ fundamentally from web service scenarios — AI training is tightly coupled multi-GPU collaboration, not stateless request handling.

MIG is the hardware foundation for GPU multi-tenancy: it lets a single A100 simultaneously serve multiple inference requests or small model training tasks, dramatically improving GPU utilization. Understanding MIG Profiles (1g.10gb, 2g.20gb, etc.) and how to expose them in K8s is core knowledge that distinguishes AI Infra engineers from general K8s engineers.

From an AI Infra Manager perspective, GPU scheduling strategy directly impacts cluster utilization and team collaboration efficiency: incorrect Taint/Toleration settings cause GPU Nodes to be occupied by ordinary Pods; improper MIG configuration causes inference resource fragmentation; lack of Gang Scheduling creates "deadlocks" in large-scale training. These are platform-level configuration strategies that need unified planning — not decisions each team makes independently.

> 面试重点：Device Plugin 暴露 GPU 资源 → Taint+Toleration+NodeAffinity 三层隔离 → MIG 分区（推理/多租户）→ 拓扑感知调度（NVLink vs InfiniBand 带宽差）→ Gang Scheduling（全有或全无）

## Raw Material
