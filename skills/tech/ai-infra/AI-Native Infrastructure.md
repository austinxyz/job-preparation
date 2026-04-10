---
title: AI-Native Infrastructure
category: tech/ai-infra
tags: [ai-native, governance, compute-scarcity, uncertainty, agent-infrastructure, closed-loop]
status: draft
priority: high
last_updated: 2026-04-09
created_from_jd:
---

# AI-Native Infrastructure

## Knowledge Map
- Prerequisites（前置知识）：[[GPU Cluster Management]], [[Kubernetes GPU Scheduling]], [[LLM Inference Optimization]]
- Related Topics（延伸话题）：[[GPU Fleet Cost Optimization]], [[AI Agents Architecture]], [[Context Engineering and Tool Interfaces]], [[Distributed Training Frameworks]]
- Management（管理关联）：[[Technical Roadmap]], [[Engineering Team Management]]

## Core Concepts

- **Three Constitutional Premises**: (1) Model-as-Actor — models/agents are execution subjects with side effects, not passive services; (2) Compute-as-Scarcity — GPUs/interconnects/power are hard-constrained, not elastic; (3) Uncertainty-by-Default — behavior and resource consumption are highly unpredictable, especially in agentic scenarios
- **Three-Plane Architecture**: Intent Plane (APIs, agent workflows, policy expressions — "what I want") → Execution Plane (training, inference, serving, tool calls, KV cache/state management) → Governance Plane (GPU orchestration, isolation, quotas, SLOs, risk policies); the Governance Plane binds the system together
- **The Closed Loop — Four Steps**: Admission (bind intent with policy at ingress; reject oversized/unauthorized requests) → Translation (convert to governable plans with caps on steps/tools/tokens) → Metering (end-to-end attribution by tenant/project/model/use-case) → Enforcement (budget triggers degradation/preemption; risk triggers isolation; SLO triggers scaling)
- **AI-Native vs. Cloud-Native dividing line**: cloud-native solves service delivery for deterministic systems; AI-native solves non-deterministic systems where the execution unit shifts from request/response → agent actions with side effects, and reliability means behavior + cost + risk governance (not just uptime/latency)
- **Context/KV Cache as Infrastructure**: when a state asset becomes a determinant variable of system cost and throughput, it rises from application detail to infrastructure layer — KV cache is now a first-class scheduled resource, not an optimization
- **MCP placement**: MCP belongs to the intent plane (orchestration layer), NOT the control/governance plane — it expresses capability boundaries but cannot constrain resource consequences on its own; governance must be enforced at the governance plane
- **Tail behavior dominates economics**: four uncertainty sources (behavior variability, demand bursts, state/context migration, network congestion) create an amplification path: agent branch explosion → context inflation → resource contention distortion; average performance metrics are misleading — P99/P999 drives economics
- **Governance readiness test** — an org that cannot answer these lacks AI-native infra: "What is the worst-case resource consumption for this agent, and where are the upper bounds?" and "How do we degrade or rollback when budget/risk thresholds are triggered?"
- **AI-grafted vs. AI-native**: AI-grafted = traditional infra with AI bolt-ons, reactive governance; AI-native = governance-first, closed loop operational, FinOps embedded in architecture; "functional but unsustainable" is the AI-grafted failure mode
- **The determinant**: "True AI-native infrastructure isn't measured by component count but by the existence of an executable governance closed loop that constrains intent to controllable resource consequences and economic/risk outcomes"

## Key Questions

**Q: What is AI-native infrastructure, and how does it differ from cloud-native?**
Answer framework: Define via three premises (model-as-actor, compute-as-scarcity, uncertainty-by-default). Then contrast dimensions: execution unit (request/response → agent actions with side effects), resource model (elastic → hard-constrained), reliability (uptime/latency → behavior + cost + risk governance), state model (stateless → KV cache as critical asset). The key shift: cloud-native solves deterministic service delivery; AI-native solves governance of non-deterministic systems.

**Q: Explain the three-plane architecture for AI infrastructure.**
Answer framework: Intent Plane (expresses "what I want" via APIs/MCP/agent workflows + policy-as-intent), Execution Plane (implements training/inference/serving, manages context/state assets), Governance Plane (enforces quotas/budgets/isolation/risk controls). The closed loop connecting them is what makes it AI-native — without the loop, you have components but not governance.

**Q: What does the governance closed loop consist of?**
Answer framework: Four steps — Admission (ingress binding of intent to policy, reject oversized requests), Translation (convert to executable plan with explicit caps), Metering (end-to-end attribution by tenant/project/model/use-case; tail overhead isolated), Enforcement (budget triggers degradation/rate-limit/preemption; risk triggers isolation). The loop closes when enforcement feeds back into policy iteration.

**Q: Where does MCP fit in an AI-native architecture? Can it replace governance?**
Answer framework: MCP is an intent-plane component — it standardizes how tools are declared and accessed but cannot constrain resource consequences on its own. Anthropic's own docs note that tool calls increase cost due to context window consumption. Governance (quotas, budgets, metering) must be enforced at the governance plane below MCP. MCP without governance = capability without cost control.

**Q: How do you assess whether an organization's AI infrastructure is mature?**
Answer framework: Use the 10-question executive checklist across three domains: Strategy (unit cost defined, budget controls at runtime, trade-offs explicit), Governance (uncertainty handling, resource mapping, utilization strategy), Execution (end-to-end observability, hardware evolution path), Organization (team alignment with accountability, architecture documented). Scoring: 0–3 = AI-grafted; 4–6 = transitioning; 7–9 = AI-native; 10 = institutionalized. The fastest signal questions are: unit cost attribution, runtime budget enforcement, and FinOps team accountability.

**Q: What makes AI infrastructure costs so hard to predict and control?**
Answer framework: Four uncertainty sources create an amplification cascade — behavior variability (agent branching, tool selection, retry loops), demand variability (concurrency bursts, multi-tenant interference), state/context variability (KV cache migration, context reuse), infrastructure variability (network congestion → tail latency). Together they make average-based capacity planning invalid; tail behavior at P99/P999 dominates economics. Solution: treat each uncertainty source as a governance object with explicit admission, metering, and enforcement.

**Q: What is the "AI Landing Zone" concept?**
Answer framework: The AI Landing Zone = compute governance loop + context tier architecture + organizational contracts. All agents, APIs, and runtimes operate within this bounded zone. It is both a technical and organizational artifact — it carries the responsibility boundary definitions (platform team vs. workload team, SLOs, budget ownership) that make scaling sustainable.

## Summary

AI-native infrastructure is an operating model designed for environments where three properties are structural: models act as autonomous agents with side effects, compute (GPUs, interconnects, power) is a hard-constrained scarce resource rather than elastic capacity, and uncertainty is the system default rather than an exception. This is a fundamental departure from cloud-native assumptions — not a migration of technology but a transformation of how organizations govern complex, non-deterministic systems. The three-plane architecture (Intent → Execution → Governance) provides a shared language for cross-team alignment, and the closed loop (Admission → Translation → Metering → Enforcement) is the operational mechanism that separates AI-native from AI-grafted systems.

The core engineering insight is "consequence-first design": infrastructure must be built starting from resource/cost/risk outcomes rather than stacking capabilities from the intent layer downward. This is counterintuitive for engineering teams who think API-first and treat governance as post-optimization. The failure mode — "functional but unsustainable" — emerges when MCP/agent capabilities are layered onto systems without cost attribution or enforcement, causing cost and risk runaway at scale. Context and KV cache state must be elevated from application details to first-class infrastructure assets: metered, allocated, and governable.

For managers and platform leaders, the practical implication is that FinOps cannot be a reconciliation exercise — it must be embedded in architecture and team contracts from day one. The AI SRE / ModelOps / FinOps triangle must operate with explicit accountability boundaries, not informal coordination. An organization that cannot answer "what is the worst-case consumption of this agent, and how do we degrade when thresholds are triggered?" has not yet built AI-native infrastructure, regardless of how sophisticated its models or APIs are.

> 面试重点：三个前提 + 三平面架构 + 四步闭环是核心框架；MCP 属于 intent plane 不能替代 governance；tail latency 主导经济而非平均值；AI-native 的判断标准是闭环是否存在，不是组件数量

## Raw Material
- [[raw_material/books/ai-native-infra/part1-definition]]
- [[raw_material/books/ai-native-infra/appendix]]
