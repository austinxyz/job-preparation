---
title: AI Native Infrastructure — Part I: Definition
source: https://jimmysong.io/book/ai-native-infra/definition/
date_saved: 2026-04-09
processed: true
skill_note: "[[skills/tech/ai-infra/AI-Native Infrastructure]]"
book: "AI Native Infrastructure — Systems Designed for Uncertainty"
book_url: https://jimmysong.io/book/ai-native-infra/
chapters_included:
  - "Definition"
  - "One-Page Reference Architecture"
---

# Part I: Definition

## What Is AI-Native Infrastructure

AI-native infrastructure is an operating system designed for environments where:
1. **Models become actors** — models/agents are execution subjects with side effects, not passive services
2. **Compute becomes scarce** — GPUs, interconnects, power, bandwidth are hard-constrained assets, not elastic
3. **Uncertainty is the default** — behavior and resource consumption are highly unpredictable, especially in agentic scenarios

The goal: make these three properties governable through a closed loop connecting **intent → execution → resource consumption → economic/risk outcomes**.

## The Three-Plane Architecture

```
Intent Plane      — APIs, agent workflows, policy expressions ("what I want")
Execution Plane   — Training, inference, serving, tool calls, state/context management
Governance Plane  — GPU orchestration, isolation, quotas, SLOs, risk policies
                         ↑_______________The Loop____________________________↑
```

### Intent Plane
- Expresses intent via inference/training APIs, MCP/tool calling protocols, agent/workflow definitions
- Policy as intent: priorities, budgets, quotas, compliance constraints embedded at entry
- Critical: intent must translate into **executable, governable plans**

### Execution Plane
- Training, fine-tuning, inference serving, batch processing, agentic runtime
- State and context services: KV cache, vector DBs, context memory
- Full-chain observability: token metering, GPU time, memory, network, storage I/O

### Governance Plane
- Transforms resource scarcity into controllable systems via budget/quota management
- Implements isolation strategies, topology-aware scheduling, risk/compliance controls
- Integrates FinOps + SRE + SecOps mechanisms

## The Closed Loop (Four Steps)

1. **Admission** — bind intent with policy at entry point; reject oversized/unauthorized requests
2. **Translation** — convert intent into executable plans with caps on steps, tools, tokens
3. **Metering** — end-to-end attribution by tenant/project/model/use-case; isolate tail overhead
4. **Enforcement** — budget triggers degradation/rate-limiting/preemption; risk triggers isolation; SLO triggers scaling

> "The determinant of true AI-native infrastructure isn't component count but the existence of an executable governance closed loop that constrains intent to controllable resource consequences and economic/risk outcomes."

## AI-Native vs. Cloud-Native

| Dimension | Cloud-Native | AI-Native |
|-----------|-------------|-----------|
| Execution unit | request/response | agent actions/decisions with side effects |
| Resource constraints | elastic CPU/memory | hard GPU/token limits |
| System behavior | deterministic | controllable non-deterministic |
| Reliability model | uptime/latency | behavior + cost + risk governance |
| State model | stateless preferred | context/KV cache are critical infra assets |

## Core Engineering Capabilities Required

- **Resource Model**: GPU, context windows, tokens as first-class schedulable resources
- **Budgets & Policies**: infra enforces org rules via automatic rate-limiting, degradation, risk-based capability gates
- **Observability**: behavior signals (tool calls, reads/writes), cost signals (tokens, GPU time), quality/safety signals
- **Risk Governance**: tiered assessment frameworks for high-capability thresholds, not single-point controls

## AI-Native Readiness Checklist

- [ ] Models treated as autonomous agents (not simple APIs)
- [ ] Budget/compute integrated into business SLAs
- [ ] Uncertainty treated as operational default
- [ ] Model behavior has audit and accountability
- [ ] Cross-team governance mechanisms (not siloed engineering optimization)
- [ ] Defined operating, cost, and risk boundaries

## Interview Relevance

- **"What is AI-native infrastructure?"** — The three premises + three-plane + closed loop is a complete 2-minute answer
- **"How is AI infra different from cloud infra?"** — Use the dimensions table above
- **"What does a platform team own in AI infra?"** — Governance plane + closed loop; workload teams own intent plane
- **MCP placement question**: MCP belongs to the orchestration layer (intent plane), NOT the control plane — cannot constrain consequences alone
- **Context as infrastructure**: "When a state asset becomes a determinant of system cost and throughput, it rises from application detail to infrastructure layer" — KV cache and long-context management are core infra concerns
