---
title: Sample AI Infra Manager - Test Co
company: Test Co
date_added: 2026-04-06
status: ready
growing_link:
---

# Sample AI Infra Manager - Test Co

## Raw JD
We are looking for an AI Infrastructure Manager to lead our GPU cluster operations team.

Requirements:
- 5+ years managing large-scale GPU clusters (A100/H100)
- Deep knowledge of NCCL and distributed training frameworks (PyTorch, DeepSpeed)
- Experience with Kubernetes for ML workloads
- Strong understanding of InfiniBand and high-speed networking
- Experience managing a team of 8-15 infrastructure engineers
- Proven ability to drive cross-functional technical projects

Nice to have:
- Experience with model serving and inference optimization
- Knowledge of cost optimization for GPU fleets
- Experience with on-premise to cloud hybrid deployments

## Key Requirements

**Required Technical Skills:**
- GPU cluster management at scale (A100/H100)
- NCCL and distributed training frameworks (PyTorch, DeepSpeed)
- Kubernetes for ML workloads
- InfiniBand and high-speed networking

**Required Leadership / Management:**
- 5+ years experience
- Managing a team of 8–15 infrastructure engineers
- Proven cross-functional technical project leadership

**Nice-to-have:**
- Model serving and inference optimization
- Cost optimization for GPU fleets
- On-premise to cloud hybrid deployments

**Domain Signals:**
- GPU cluster operations team — this is a hands-on infra management role, not pure people management
- AI/ML workloads focus (training + serving)
- Scale: A100/H100 clusters implies large-scale production AI infra

## Skill Gap Analysis

| Skill | Status | Priority |
|-------|--------|----------|
| GPU Cluster Management | stub | high |
| NCCL and Collective Communication | stub | high |
| Distributed Training Frameworks (PyTorch, DeepSpeed) | stub | high |
| Kubernetes | stub | high |
| InfiniBand and High-Speed Networking | stub | high |
| Engineering Team Management | stub | high |
| Technical Roadmap (cross-functional projects) | stub | high |
| LLM Inference Optimization | stub | medium |
| GPU Fleet Cost Optimization | stub | medium |
| Hybrid Cloud Deployment | stub | medium |

## Prep Checklist

**Tech — 需要学习（stub，最优先）**
- [ ] **[high]** Learn GPU Cluster Management (A100/H100 architecture, CUDA, NVLink) → [[skills/tech/ai-infra/GPU Cluster Management]]
- [ ] **[high]** Learn NCCL and Collective Communication (AllReduce, ring-allreduce, bandwidth) → [[skills/tech/ai-infra/NCCL and Collective Communication]]
- [ ] **[high]** Learn Distributed Training Frameworks (PyTorch DDP, DeepSpeed ZeRO, Megatron) → [[skills/tech/ai-infra/Distributed Training Frameworks]]
- [ ] **[high]** Deepen Kubernetes for ML workloads (GPU scheduling, device plugins, MIG partitioning) → [[skills/tech/infra/Kubernetes]]
- [ ] **[high]** Learn InfiniBand and High-Speed Networking (RDMA, RoCE, fat-tree topology) → [[skills/tech/infra/InfiniBand and High-Speed Networking]]
- [ ] **[medium]** Learn LLM Inference Optimization (vLLM, TensorRT-LLM, KV cache, continuous batching) → [[skills/tech/ai-infra/LLM Inference Optimization]]
- [ ] **[medium]** Learn GPU Fleet Cost Optimization (utilization, chargeback, spot instances) → [[skills/tech/ai-infra/GPU Fleet Cost Optimization]]
- [ ] **[medium]** Learn Hybrid Cloud Deployment patterns → [[skills/tech/infra/Hybrid Cloud Deployment]]

**Management — 经验 notes 已写，练习讲述即可**
- [x] **[high]** Engineering Team Management stories — ✅ [[experience/eBay - Global Team Expansion]], [[experience/eBay - AI-Augmented Engineering Management]]
- [x] **[high]** Cross-functional project leadership stories — ✅ [[experience/eBay - DoJ and Jade Programs]], [[experience/eBay - Platform Engineering at Scale]]

## Experience Match

**强相关（直接回答 JD 要求）**

- [[experience/eBay - Platform Engineering at Scale]] — Kubernetes at scale (200+ clusters, 2M instances), CRDs/admission webhooks, 2-engineer team maintaining entire fleet with zero incidents; directly addresses "Kubernetes for ML workloads" and "cross-functional technical projects"
- [[experience/eBay - Global Team Expansion]] — built and managed 8+ engineers across Europe & India within 3 months; directly addresses "managing a team of 8–15 infrastructure engineers"
- [[experience/eBay - DoJ and Jade Programs]] — high-stakes cross-functional war room, zero-downtime infra cutover, Kubernetes cluster provisioning at scale; directly addresses "cross-functional technical projects" and K8s ops

**补充相关（展示管理深度）**

- [[experience/eBay - AI-Augmented Engineering Management]] — people management systems (hiring, performance, onboarding), OKR 50%→80%, hiring cycle 3月→4–6周; relevant for "managing a team" and operational excellence
- [[experience/eBay - AI Innovation]] — SRE metrics (incidents 50%↓, MTTD/MTTR), triage automation 70%; relevant for operational excellence and infra reliability culture

## Resume Tailoring

### 关键词匹配

| JD 关键词 | 建议加入 resume 的表述 |
|----------|----------------------|
| GPU clusters (A100/H100) | 当前简历无 GPU 经验 — 如有任何 GPU 基础设施接触，补充进 eBay 最近一段经历 |
| NCCL / distributed training | 当前简历无 — 学习后可在 Summary 加 "experience supporting distributed AI training infrastructure" |
| Kubernetes for ML workloads | 当前：「migrate 5,000+ eBay applications to Kubernetes」→ 改为「Kubernetes platform supporting ML training and serving workloads」突出 AI 角度 |
| Managing team of 8–15 engineers | 当前：「hired 8+ engineers」→ 改为「built and managed a team of 10+ infrastructure engineers across 3 regions」更贴近 JD 表述 |
| Cross-functional technical projects | 当前：「coordinating across multiple cloud teams」→ 改为「led cross-functional initiatives across Cloud, AI, and SRE teams」 |
| InfiniBand / high-speed networking | 当前简历无 — 学习后可在 Skills 加「InfiniBand, RDMA, high-speed networking」|
| Model serving / inference optimization | 当前简历无 — 学习后可酌情加入 |
| Cost optimization for GPU fleets | 当前有「auto-scaling and traffic rebalancing to improve efficiency」→ 可扩展为「capacity and cost optimization for large-scale compute fleets」|

### 建议强调的 Experience

1. **eBay Cloud Platform (Sept 2023–Present)** — 最相关，强调 K8s 规模（100+ clusters, 2M+ pods）、SRE、cross-functional leadership、team building（8+ engineers hired）
2. **eBay Cloud App Lifecycle (Feb 2017–Aug 2023)** — 补充体现 infra 技术深度：custom controllers, multi-cluster deployment, CI/CD platform
3. **eBay CCOE Cloud (Feb 2012–Feb 2017)** — 体现从 V1→V3 三代平台建设经验，展示 infra 架构广度

### 建议弱化的内容

- **DevEx Tools (2007–2012)**: IDE 工具、前端框架开发与 AI Infra Manager 职位相关性低，可简化为 1 行
- **Mainet (2000–2007)**: ERP 产品、RAD 工具与目标职位无关，建议精简为 2 行或移至附录
- **技能列表中**: Java/J2EE、Spring/SpringBoot、前端框架（React/Vue/jQuery）权重降低，GPU/NCCL/InfiniBand 学习后补充进来
