---
title: AI Native Infrastructure — Part II: Principles
source: https://jimmysong.io/book/ai-native-infra/compute-governance/
date_saved: 2026-04-09
processed: true
skill_note: "[[skills/tech/ai-infra/GPU Fleet Cost Optimization]]"
book: "AI Native Infrastructure — Systems Designed for Uncertainty"
book_url: https://jimmysong.io/book/ai-native-infra/
chapters_included:
  - "Compute Governance"
  - "Metrics and Budget Isolation"
---

# Part II: Principles

## Why Governance Before API Design

The central argument: AI-native infra must start from **consequences** (resource/cost/risk outcomes), not from **intent** (API elegance).

Many teams treat AI adoption as an API morphology change — plug in LLMs, expose via REST. This fails because:
1. **Resource scarcity is different**: GPU/interconnect/power are hard constraints, not elastic
2. **Request costs are unpredictable**: token consumption + GPU time follow long-tail distributions due to agentic branching, context inflation, tool-call amplification
3. **Stateless patterns break down**: KV cache persistence and inference state reuse directly determine unit cost controllability

> "AI-native infrastructure must be designed starting from 'Consequence' rather than stacking capabilities from 'Intent.'"

## Uncertainty as the Operational Default

Four sources of uncertainty that make "average performance" meaningless — **tail behavior dominates economics**:

| Category | Key Manifestation |
|----------|-------------------|
| **Behavior** | Agent decomposition paths, tool selection variability, retry/reflection loops |
| **Demand** | Concurrency bursts, long-tail requests, multi-tenant interference |
| **State/Context** | KV cache migration, context reuse across requests |
| **Infrastructure** | Network sensitivity, congestion → tail latency amplification |

**Uncertainty amplification path**: Agent branch explosion → Context inflation → Resource contention distortion

## Compute Governance: Four Objects to Manage

1. **Token Economics** — request-level consumption maps directly to cost/latency; must be metered and attributed
2. **Accelerator Time** — GPU utilization, MFU (Model FLOP Utilization), throughput per dollar
3. **Interconnect and Storage** — network/storage pressure from distributed training + cache sharing
4. **Organizational Budget & Risk** — multi-tenant isolation, fairness, audit, compliance

## MCP/Agent Amplification Warning

Anthropic's own documentation notes: "Direct tool calls increase cost and latency due to tool definitions and intermediate results consuming context window." Exponential cost volatility emerges without governance constraints.

MCP is an **intent-plane** component — it expresses capability boundaries but **cannot constrain consequences** on its own. Governance must be enforced at the governance plane.

## Five Hard Standards for Governance

1. **Admission Control**: reject oversized requests; encode budget, priority, compliance into intent at ingress
2. **Intent Translation**: convert to governable execution plans with explicit caps on steps, tools, tokens
3. **Metering**: end-to-end attribution by tenant/project/model/use-case; isolate tail overhead as separate cost center
4. **Enforcement**: budget triggers (rate limiting, degradation, preemption); risk isolation mechanisms
5. **Feedback Loop**: policy iteration and cost correction; SLO → cost → policy as a closed feedback cycle

## Five-Layer Architecture Stack

```
Layer 5 — Business Interface (SLAs, product experience)
Layer 4 — Intent/Orchestration (MCP, Agents, workflows)
Layer 3 — Execution Runtime (inference, training, caching)
Layer 2 — Resource Abstraction (GPU pools, scheduling)
Layer 1 — Governance Foundation (quotas, budgets, isolation, metering)
```

Layers 1-2 = Governance Plane (infra team owns)
Layers 3-4 = Execution/Intent Planes (platform team owns)
Layer 5 = Business Interface (app team owns)

**Failures cascade when inter-layer closed loops don't exist.**

## Minimal Implementation: Five Components

1. Admission + Budget policies per workload type
2. End-to-end metering and cost attribution chains
3. Simultaneous sharing (utilization) + isolation (risk reduction) — not one or the other
4. Topology and network as first-class architectural variables
5. Context/state as governed assets, not temporary variables

## Critical Architecture Questions (Governance Readiness Test)

An org that cannot answer these lacks true AI-native infrastructure:
- "What is the worst-case resource consumption for this agent, and where are the upper bounds?"
- "How do we degrade or rollback when budget/risk thresholds are triggered?"
- "Can we attribute the primary consumption of each agent/job to team/project/model/use-case?"

## Anti-Patterns

- Treating governance as post-optimization (bolt-on FinOps after scale problems emerge)
- Viewing MCP/Agent solely as capability accelerators (ignoring cost amplification)
- Procuring GPUs without orchestration/sharing mechanisms
- Ignoring network topology and treating AI workloads as ordinary microservices
- "Functional but unsustainable" — API-first without governance amplifies costs and uncertainty

## Interview Relevance

- **"How do you govern AI infra costs?"** — Five-component minimal implementation + metering attribution hierarchy
- **"What's the difference between GPU governance and cloud resource governance?"** — Hard scarcity, non-elastic, long-tail cost distribution
- **"Where does MCP fit in your architecture?"** — Intent plane orchestration layer, not control plane; cannot replace governance
- **"How do you handle agent cost runaway?"** — Admission control + budget enforcement + feedback loop
- **"What metrics matter for AI infra?"** — Token economics, GPU MFU, tail latency (P99/P999), cost per task by tenant
