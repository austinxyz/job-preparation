---
title: GPU Fleet Cost Optimization
category: tech/ai-infra
tags: [cost-optimization, gpu-utilization, spot-instances, scheduling, chargeback, compute-governance, finops]
status: draft
priority: medium
last_updated: 2026-04-09
created_from_jd: [[positions/Sample AI Infra Manager - Test Co]]
---

# GPU Fleet Cost Optimization

## Knowledge Map
- Prerequisites（前置知识）：[[GPU Cluster Management]], [[Kubernetes GPU Scheduling]], [[AI-Native Infrastructure]]
- Related Topics（延伸话题）：[[Spot Instances]], [[Cluster Autoscaling]], [[Chargeback Models]], [[LLM Inference Optimization]]
- Management（管理关联）：[[Capacity Planning]], [[Technical Roadmap]]

## Core Concepts

- **Consequence-first design principle**: AI infra costs must be governed starting from resource/cost/risk outcomes ("consequences"), not layered on top of API/agent capabilities ("intent") — post-hoc governance is the failure mode that leads to cost runaway at scale
- **Four compute governance objects**: (1) Token Economics — request-level token consumption maps directly to cost/latency; must be attributed per call; (2) Accelerator Time — GPU utilization measured by MFU (Model FLOP Utilization) and throughput-per-dollar; (3) Interconnect and Storage — network/storage pressure from distributed training and KV cache sharing; (4) Organizational Budget & Risk — multi-tenant isolation, fairness enforcement, audit trails, compliance controls
- **Long-tail cost distribution**: AI request costs do not follow normal distributions — agentic branching, context inflation, and tool-call amplification create fat-tail token consumption; P99/P999 cost dominates economics, not averages; "average GPU utilization" is a misleading metric for AI workloads
- **MCP cost amplification**: Anthropic's own docs note tool calls increase cost because tool definitions + intermediate results consume context window; multi-step agent workflows create exponential cost volatility without governance constraints; MCP cannot self-govern — governance must be enforced at the infrastructure layer
- **Five governance standards**: Admission Control (reject oversized requests; encode budget/priority/compliance at ingress) → Intent Translation (cap steps/tools/tokens per plan) → Metering (end-to-end attribution by tenant/project/model/use-case; tail overhead as separate cost center) → Enforcement (budget triggers rate-limit/degradation/preemption; risk triggers isolation) → Feedback Loop (SLO → cost → policy correction cycle)
- **Simultaneous sharing + isolation**: GPU governance must achieve both utilization (sharing mechanisms: MIG, MPS, time-slicing) AND risk reduction (isolation: dedicated pools, namespace separation) — optimizing for only one creates either waste or noisy-neighbor contention
- **Context/KV cache as cost asset**: KV cache reuse directly determines inference unit cost; failing to assetize context as infrastructure (metered, allocated, governable) prevents reuse and inflates per-request costs; treating it as a temporary variable is a common anti-pattern
- **Cost attribution as scaling prerequisite**: "If you cannot attribute the primary consumption of each agent/job to team/project/model/use-case, you haven't reached the 'scale' starting line" — chargeback/showback is not just accounting but an incentive alignment mechanism
- **FinOps as architecture, not reconciliation**: FinOps must be incorporated into platform architecture and team contracts upfront; bolt-on cost reconciliation after the fact creates friction without corrective behavior change
- **Anti-patterns to avoid**: treating GPUs as ordinary cloud resources (no isolation → contention), procuring GPUs without orchestration/sharing mechanisms, ignoring network topology (amplifies tail latency), building APIs/agents without cost ledgers (runaway at scale)

## Key Questions

**Q: How do you govern and control AI infrastructure costs at scale?**
Answer framework: Five-component minimal implementation — admission + budget policies per workload type, end-to-end metering with attribution dimensions (team/project/model/use-case), simultaneous sharing + isolation strategies, topology/network as first-class variables, context/state as governed assets. The key insight: governance must be front-loaded into architecture, not retrofitted. Cite the "functional but unsustainable" failure mode for API-first approaches.

**Q: What metrics do you track for GPU fleet cost efficiency?**
Answer framework: Token economics (cost per token/task by tenant), GPU MFU (Model FLOP Utilization — measures how much of theoretical peak compute is used), throughput per dollar, tail latency (P99/P999 — dominates agent workloads), cost attribution coverage (% of consumption with clear owner). Distinguish from cloud-native metrics: average utilization is misleading for long-tail AI workloads.

**Q: How is GPU cost governance different from traditional cloud resource governance?**
Answer framework: Three key differences — (1) Hard scarcity: GPU/interconnect/power cannot be elastically scaled like CPU/memory; procurement cycles are long; (2) Non-linear cost: AI request costs follow long-tail distributions (not Gaussian) due to agentic branching and context inflation; (3) State cost: KV cache and inference state are cost-determining assets that must be governed, unlike stateless cloud workloads. Governance mechanisms must address all three.

**Q: How do you implement chargeback/showback for a multi-team GPU platform?**
Answer framework: Attribution dimensions first (team, project, model, use-case, priority tier) — must be captured at request ingress, not derived post-hoc. Metering stack: token counters + GPU time + network I/O, aggregated per billing period. Showback before chargeback to align on attribution accuracy. Governance contracts: each team has budget, quota, and escalation path defined before resource allocation. Incentive design: chargeback rates that reward efficient models and batching.

**Q: How do you handle agent cost runaway — an agent that consumes far more resources than expected?**
Answer framework: Prevention (admission control with budget binding at ingress; per-agent step/tool/token caps), Detection (real-time cost telemetry with anomaly alerting; cost-per-task vs. baseline), Response (automatic degradation: reduce parallelism, cap context window; preemption: pause low-priority jobs; circuit breaker: suspend the agent), Recovery (postmortem: identify which uncertainty source caused the amplification — behavior, demand, state, or network). The feedback loop then updates admission policies.

**Q: Explain GPU sharing strategies — MIG, MPS, time-slicing. When do you use each?**
Answer framework: MIG (Multi-Instance GPU) — hardware partitioning at silicon level; full isolation of memory and compute; best for mixed workloads with hard isolation requirements (different tenants, different SLOs); overhead: underutilizes if workloads don't fill their slice. MPS (Multi-Process Service) — software sharing with memory isolation; multiple processes share SM time; better utilization for latency-tolerant inference; risk: fault propagation between processes. Time-slicing — round-robin scheduling; maximum flexibility; no memory isolation; best for dev/test or burst workloads. Choose based on: isolation requirement (MIG > MPS > time-slice) vs. utilization target (time-slice > MPS > MIG).

## Summary

GPU fleet cost optimization in AI-native infrastructure is fundamentally different from cloud cost optimization — it requires governance-first design rather than post-hoc FinOps. The root cause of AI cost unpredictability is the long-tail distribution of request costs: agentic branching, context inflation, and tool-call amplification create fat-tail token consumption where P99 costs can be 10–100x the median. Average utilization metrics and monthly billing reconciliation are insufficient controls for this regime. Effective cost governance requires treating token economics, accelerator time, interconnect, and organizational budget as four distinct governance objects, each with admission controls, real-time metering, and enforcement mechanisms.

The five governance standards — Admission Control, Intent Translation, Metering, Enforcement, and Feedback Loop — form a closed operational cycle. The most commonly skipped step in practice is the feedback loop: organizations implement metering and even enforcement but fail to close the cycle back to policy update and cost correction. Without the feedback loop, governance is reactive rather than adaptive. A related anti-pattern is treating GPU governance as separate from FinOps: chargeback/showback is not an accounting exercise but an incentive alignment mechanism that drives teams toward efficient model selection, batching, and context management.

Context and KV cache management are the hidden cost levers. Treating inference state as a temporary variable (stateless cloud-native pattern) prevents KV cache reuse and inflates per-request costs unnecessarily. Elevating context to a metered, allocated, governable infrastructure asset — with explicit cache hit rates, reuse ratios, and cost attribution — is one of the highest-leverage optimizations available to AI infra teams. Combined with GPU sharing strategies (MIG for isolation, MPS for throughput, time-slicing for flexibility) tuned to workload mix, these mechanisms can dramatically improve cost-per-task while maintaining SLO compliance.

> 面试重点：五步治理标准（Admission → Translation → Metering → Enforcement → Feedback）；长尾分布是核心问题，平均利用率是误导指标；KV Cache 是成本杠杆；FinOps 必须前置而非事后对账

## Raw Material
- [[raw_material/books/ai-native-infra/part2-principles]]
