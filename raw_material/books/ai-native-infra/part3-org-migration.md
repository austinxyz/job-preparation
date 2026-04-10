---
title: AI Native Infrastructure — Part III: Organization & Migration
source: https://jimmysong.io/book/ai-native-infra/operating-model/
date_saved: 2026-04-09
processed: true
skill_note: "[[skills/management/project/Technical Roadmap]]"
book: "AI Native Infrastructure — Systems Designed for Uncertainty"
book_url: https://jimmysong.io/book/ai-native-infra/
chapters_included:
  - "Organization and Culture"
  - "Migration Roadmap"
---

# Part III: Organization & Migration

## The Operating Model Shift

Cloud-native → AI-native is not just a technical migration; it is an **institutional change** in how organizations govern uncertainty.

**Core responsibility split**:
- **Platform Team**: provides stable landing zones, governance capabilities, golden paths, shared infrastructure
- **Workload Team**: owns model selection, prompt logic, tool integration, SLO definitions

The governance closed loop must span both — failures cascade when inter-team accountability boundaries aren't defined.

## Three Failing Assumptions (API-First Organizations)

1. **Resource scarcity misconception**: assumes engineering efficiency is the constraint; misses that GPU/power/interconnect are physically hard-constrained
2. **Predictable request cost assumption**: ignores that agentic branching + context inflation makes token consumption a random variable
3. **Ephemeral state model**: cloud-native stateless patterns break down; KV cache persistence is now a unit cost determinant

## Organizational Structure: AI SRE + ModelOps + FinOps Triangle

Three functions must collaborate with explicit accountability:
- **AI SRE/Infrastructure**: reliability, capacity, governance plane ownership
- **ModelOps**: model lifecycle, inference optimization, deployment pipelines
- **FinOps**: cost attribution, budget governance, chargeback/showback to teams

Without formal collaboration contracts between these three, governance becomes reactive and post-hoc.

## Migration Philosophy

> "Migration is not 'rebuilding the platform,' but using governance loops and organizational contracts to transform uncertainty into controllable engineering capabilities."

> "FinOps must be incorporated into architecture and organization upfront as a shared operating model, not as an after-the-fact reconciliation exercise."

> "If you cannot attribute the primary consumption of each agent/job to team/project/model/use-case...you haven't reached the 'scale' starting line."

## Three Migration Paths

**Path 1 — Bypass Pilot** (high org uncertainty)
- Independent GPU pool with basic admission/budget controls
- For early exploration; minimal dependencies on existing platform
- Entry criteria: team wants to learn; low risk tolerance for platform breakage

**Path 2 — Domain-Isolated Platform** (multi-team stage)
- Solidified platform capabilities managing shared governance across workload teams
- Formal platform-workload team contracts
- Entry criteria: >2 teams sharing GPU resources; consistent chargeback required

**Path 3 — AI-First Refactor** (core business focus)
- Infrastructure as production pipeline; optimize by unit cost and tail latency
- Core business workflows depend on AI capabilities
- Entry criteria: AI is on the critical path; cost-per-task drives business decisions

## 90-Day Implementation Plan

### Days 0–30: Visibility Foundation
- Establish cost/usage ledgers with attribution dimensions (team, project, model, use-case)
- Define unit cost metrics for each workload type
- Implement basic admission policies at ingress
- Goal: "can we see what is consuming what?"

### Days 31–60: Governance Infrastructure
- Build GPU governance (MIG/MPS/vGPU isolation strategies)
- AI-ready network baseline: lossless strategies, isolation domains, congestion management
- Templated delivery paths (golden paths) for common workload types
- Goal: "can we isolate and control consumption?"

### Days 61–90: Enforcement and Migration
- Execute enforcement policies: rate limiting, degradation, preemption triggers
- Migrate pilot use cases to governed paths
- Formalize platform-workload team contracts (SLOs, budget owners, escalation paths)
- Goal: "is the closed loop operational?"

## North Star: The AI Landing Zone

**AI Landing Zone** = compute governance loop + context tier architecture + organizational contracts

All agents, APIs, and runtimes must operate within this bounded zone. The Landing Zone is both a technical and organizational artifact — it carries the responsibility boundary definitions essential for scaling.

## Critical Anti-Patterns

| Anti-Pattern | Consequence |
|-------------|-------------|
| Building APIs/agents without cost ledgers | Runaway expenses at scale |
| Treating GPUs as ordinary cloud resources | Uncontrolled contention, noisy neighbor effects |
| Ignoring network topology | Tail latency amplification, invalidated capacity planning |
| Failing to assetize context as infrastructure | Prevents KV cache reuse, inflates unit costs |
| Governance as post-optimization | "Functional but unsustainable" systems |
| FinOps as reconciliation (not architecture) | Chargeback friction, no incentive alignment |

## Interview Relevance

- **"How would you migrate a cloud-native team to AI-native?"** — Three-path framework + 90-day plan
- **"How do you structure teams for AI infra?"** — Platform/Workload split + AI SRE/ModelOps/FinOps triangle
- **"What's your approach to AI infrastructure cost governance?"** — Landing Zone + attribution ledger + enforcement policies
- **"What does 'scale' mean for AI infra?"** — Being able to attribute consumption by team/project/model/use-case
- **"What would you do in the first 90 days as AI Infra Manager?"** — This chapter maps directly to that question
- **"How do you handle FinOps for AI?"** — Front-loaded into architecture, not reconciliation; chargeback as incentive alignment
