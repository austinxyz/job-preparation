---
title: Karpenter
category: tech/infra
tags: [karpenter, autoscaling, node-provisioning, kubernetes, gpu-scaling, spot-instance, nodepool, ec2nodeclass, just-in-time]
status: draft
priority: high
last_updated: 2026-04-06
created_from_jd:
---

# Karpenter

## Knowledge Map
- Prerequisites（前置知识）：[[Kubernetes]], [[K8s Control Plane]], [[Kubernetes GPU Scheduling]]
- Related Topics（延伸话题）：[[GPU Fleet Cost Optimization]], [[Hybrid Cloud Deployment]]
- Management（管理关联）：[[Platform Team Management]]

## Core Concepts

**What Karpenter Is — The Problem It Solves（节点自动供给器）**
- Karpenter = K8s **Node Autoprovisioner** — open-sourced by AWS, now a CNCF project
- Core capability: watches Pending Pods → computes the required node spec → directly calls cloud APIs to create nodes (bypasses Node Groups) → Pods are scheduled once the node is ready
- vs **Cluster Autoscaler (CA)** (the traditional approach): CA scales by adjusting the replica count of predefined Node Groups (limited to existing Node Group types); Karpenter calls EC2 API directly, can select **any instance type** — one order of magnitude more flexible

**Karpenter vs Cluster Autoscaler（对比）**

| Dimension | Cluster Autoscaler | Karpenter |
|-----------|-------------------|-----------|
| Scale-out speed | Slow (poll-based detection + Node Group scaling) | Fast (Watch Pending Pods, call API directly) |
| Instance types | Limited to preconfigured Node Groups | Any instance type, dynamically selects optimal |
| Scale-in | By Node Group | Smart consolidation (bin-packing), actively migrates Pods before deleting idle nodes |
| GPU support | Requires a Node Group per GPU type | Single NodePool config, selects GPU model on demand |
| Complexity | Complex configuration (multiple Node Groups to manage separately) | Simple configuration (NodePool + NodeClass) |

**Core Concepts: NodePool + EC2NodeClass（核心配置对象）**
- **NodePool**: defines node constraints (allowed instance type range, CPU/GPU model, AZ, Spot vs On-demand ratio, TTL, etc.)
- **EC2NodeClass** (on AWS): defines AWS-specific configuration (AMI, subnets, security groups, IAM role, user data script)
- Within the NodePool's allowed range, Karpenter selects the **optimal instance type** for the Pending Pod's needs (smallest spec that satisfies requirements, minimizing cost) （成本最优）

**Just-in-Time Provisioning Flow（即时供给流程）**
1. Pod becomes Pending due to insufficient resources
2. Karpenter watches the Pending Pod, analyzes its `resources.requests`, `nodeSelector`, `tolerations`
3. Selects the best instance type within the NodePool's allowed types (satisfies requirements + cost-optimal)
4. Calls EC2 API to create the node; node joins the cluster
5. Karpenter directly binds the Pod to the new node (no need to wait for the Scheduler to reschedule)

**Consolidation — Smart Scale-In（智能整合缩容）**
- Karpenter continuously evaluates cluster node utilization: detects Pods on some nodes that could be migrated to other nodes → triggers **Consolidation**
- Evicts Pods from underutilized nodes → Pods reschedule to other nodes → delete empty nodes
- Cost savings: avoids many underutilized nodes running indefinitely （避免半满节点长期运行）
- `consolidationPolicy: WhenEmptyOrUnderutilized` controls the consolidation policy; `disruptionBudget` controls max simultaneous evictions

**Karpenter Practices for GPU Clusters（GPU 集群实践）**
- Single NodePool configuring multiple GPU types (A100, H100, V100); Karpenter selects the most suitable on demand
- **Spot instances**: Karpenter supports configuring Spot/On-demand ratios; GPU Spot instances can save 60–70% cost (trade-off: can be preempted) （节省 60-70% 成本）
- Training jobs + Spot: requires checkpoint mechanism (save training state when node is preempted; new node resumes training)
- `karpenter.sh/do-not-disrupt: "true"` annotation: prevents Karpenter from evicting a Pod mid-training (Consolidation protection) （防训练中断）
- **Expiry (TTL)**: set maximum node lifetime (e.g., 24 hours) to force node rotation and prevent configuration drift

## Key Questions

**Q: What is the difference between Karpenter and Cluster Autoscaler? Why use Karpenter?**
Answer framework: CA depends on preconfigured Node Groups, can only scale within existing types, high config maintenance cost (each GPU model needs its own Node Group); Karpenter directly calls EC2 API, any instance type created on demand, fast response (Watch Pending Pods rather than polling), smart scale-in (Consolidation actively consolidates underutilized nodes); Karpenter's advantage is even more pronounced for GPU clusters (many GPU models, manual Node Group maintenance cost is extremely high).
> 中文提示：CA 依赖预配置 Node Group；Karpenter 直调 EC2 API 任意实例类型；GPU 集群多型号场景 Karpenter 优势更明显

**Q: How does Karpenter prevent evicting a Pod mid-training (Consolidation protection)?**
Answer framework: `karpenter.sh/do-not-disrupt: "true"` annotation (at Pod or Node level); Karpenter Consolidation skips nodes with this annotation; training job Pods auto-get this annotation (via Mutation Webhook or Training Operator config); `disruptionBudget` controls max nodes evicted simultaneously; for Spot instance preemption (cloud provider actively reclaims), must rely on checkpoint mechanism rather than Karpenter protection.
> 中文提示：do-not-disrupt 注解防 Consolidation 驱逐；Spot 抢占是云厂商强制回收，无法靠注解保护，需 checkpoint 机制

**Q: How do you manage Spot instances in a GPU cluster with Karpenter? What are the risks for training jobs + Spot?**
Answer framework: NodePool configures `capacityType: [spot, on-demand]` mixed by ratio; Spot saves 60–70% cost; risk: Spot preempted (2-minute notice before node reclaim) → training job interrupted; mitigations: ① short training jobs (<1 hour) can be all-Spot (loss is small even if interrupted); ② long training jobs increase checkpoint frequency (save every N steps); ③ critical training jobs use On-demand, non-critical eval/data processing uses Spot.
> 中文提示：Spot 节省 60-70%；短任务全 Spot 可接受；长任务频繁 checkpoint；关键任务用 On-demand

**Q: How does Karpenter Consolidation work? How do you prevent frequent evictions from impacting business?**
Answer framework: Karpenter continuously evaluates node utilization; triggers Eviction + rescheduling + node deletion when Pods can be consolidated; preventing frequent evictions: ① `do-not-disrupt` annotation for critical Pods; ② `disruptionBudget` limits simultaneous eviction count; ③ `consolidationPolicy: WhenEmpty` (only delete empty nodes, no Pod migration) vs `WhenEmptyOrUnderutilized` (aggressive consolidation); ④ PodDisruptionBudget (K8s native, limits max evicted proportion per workload).
> 中文提示：四种保护机制：do-not-disrupt + disruptionBudget + consolidationPolicy + PDB；按场景组合使用

**Q: How do you manage multiple GPU models (A100, H100, V100) with NodePool?**
Answer framework: Single NodePool with `requirements` listing multiple instance types (`p4d.24xlarge`/`p4de.24xlarge`/`p3.16xlarge`); use `nodeSelector` or `NodeAffinity` to declare the required GPU model (`accelerator: a100`); Karpenter selects the most cost-optimal among instance types satisfying Pod constraints; different priority tasks can use different NodePools (high priority = On-demand A100, low priority = Spot V100).
> 中文提示：单一 NodePool 配多种实例类型；Pod 用 nodeSelector 声明 GPU 型号；不同优先级任务用不同 NodePool

## Summary

Karpenter's core value is transforming K8s cluster node management from "pre-planning Node Groups" to "dynamic just-in-time provisioning" — highly aligned with K8s's declarative API philosophy: you describe what a Pod needs, Karpenter ensures the right node exists. This Just-in-Time provisioning mode is especially well-suited for AI training workloads — GPU training jobs tend to be short-burst peaks that don't require continuously provisioned GPU nodes.

Consolidation is Karpenter's killer feature that differentiates it from other solutions: it doesn't just scale out, it also actively consolidates underutilized nodes to avoid large numbers of "half-full nodes" in GPU clusters (each node using only some GPUs, with the remaining GPUs unusable by other jobs). For GPU Fleet cost optimization, the Karpenter + Spot + Consolidation combination can reduce GPU cluster costs by 30–50%.

As an AI Infra Manager, Karpenter configuration strategy is a key decision directly impacting team GPU availability and cost: NodePool instance type range determines the elasticity ceiling, Spot ratio determines the cost-stability trade-off, and `do-not-disrupt` strategy determines training job protection level. These configurations need to be differentiated based on different teams' workload characteristics (long training vs short inference vs data processing).

> 面试重点：Karpenter vs CA（直调 API vs Node Group）→ Just-in-Time 供给流程 → Consolidation 智能整合 → do-not-disrupt 保护训练任务 → Spot + checkpoint 组合降低成本

## Raw Material
