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

- [ ] **[high]** Learn GPU Cluster Management (A100/H100 architecture, CUDA, NVLink) — find learning material (`stub`) → [[skills/tech/ai-infra/GPU Cluster Management]]
- [ ] **[high]** Learn NCCL and Collective Communication (AllReduce, ring-allreduce, bandwidth) — find learning material (`stub`) → [[skills/tech/ai-infra/NCCL and Collective Communication]]
- [ ] **[high]** Learn Distributed Training Frameworks (PyTorch DDP, DeepSpeed ZeRO, Megatron) — find learning material (`stub`) → [[skills/tech/ai-infra/Distributed Training Frameworks]]
- [ ] **[high]** Deepen Kubernetes knowledge for ML workloads (GPU scheduling, device plugins, MIG) — find learning material (`stub`) → [[skills/tech/infra/Kubernetes]]
- [ ] **[high]** Learn InfiniBand and High-Speed Networking (RDMA, RoCE, topology) — find learning material (`stub`) → [[skills/tech/infra/InfiniBand and High-Speed Networking]]
- [ ] **[high]** Prepare Engineering Team Management stories (managing 8–15 engineers, hiring, performance) — write STAR experience notes (`stub`) → [[skills/management/people/Engineering Team Management]]
- [ ] **[high]** Prepare cross-functional project leadership stories — write STAR experience notes (`stub`) → [[skills/management/project/Technical Roadmap]]
- [ ] **[medium]** Learn LLM Inference Optimization (vLLM, TensorRT-LLM, KV cache) — find learning material (`stub`) → [[skills/tech/ai-infra/LLM Inference Optimization]]
- [ ] **[medium]** Learn GPU Fleet Cost Optimization (utilization, chargeback, spot) — find learning material (`stub`) → [[skills/tech/ai-infra/GPU Fleet Cost Optimization]]
- [ ] **[medium]** Learn Hybrid Cloud Deployment patterns — find learning material (`stub`) → [[skills/tech/infra/Hybrid Cloud Deployment]]

## Experience Match

No experience notes yet. Suggested experience notes to write based on your resume:

- **eBay K8s Platform Migration** — highly relevant for Kubernetes + cross-functional leadership (5,000+ apps, 100+ clusters, 2M+ pods)
- **Global Team Expansion (Europe & India)** — relevant for "managing 8–15 engineers", hiring, team building
- **DoJ & Jade Programs** — relevant for cross-functional technical project leadership under tight deadline
- **OpenStack → Kubernetes Migration (2017–2023)** — relevant for large-scale infra migration ownership

Write these as STAR notes in `experience/` and link back here.

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
