---
title: Technical Roadmap
category: management/project
tags: [roadmap, planning, prioritization, stakeholders, project-management]
status: in-progress
priority: medium
last_updated: 2026-04-09
created_from_jd:
---

# Technical Roadmap

## Knowledge Map
- Prerequisites（前置知识）：[[Engineering Team Management]]
- Related Topics（延伸话题）：[[OKRs and Goal Setting]], [[Cross-team Collaboration]], [[Risk Management]], [[AI-Native Infrastructure]]
- Management（管理关联）：[[People Management]], [[Engineering Team Management]]

## Core Concepts

**DORA Metrics** (DevOps Research and Assessment — the industry standard for engineering velocity)
- **Deployment Frequency**: how often code is deployed to production (elite: on-demand)
- **Lead Time for Changes**: time from code commit to running in production (elite: < 1 hour)
- **Mean Time to Recovery (MTTR)**: time to recover from a failure in production (elite: < 1 hour)
- **Change Failure Rate**: percentage of deployments causing a production incident (elite: 0–15%)
- Elite performers score well on all four; improving frequency reduces batch size, which reduces risk and MTTR

**Software Development Process**
- Requirements → Design → Implementation → Testing (unit → integration → E2E) → Code Review → Deploy → Monitor → Iterate
- Agile/Scrum: sprint-based iteration, continuous delivery; CI/CD automates build, test, and deploy gates
- Key quality gates: automated testing, static analysis (linters), staging validation, canary rollout, monitoring with rollback plan

**CI/CD Pipeline**
- CI: automated build + test on every commit; catches integration issues early
- CD: automated deployment to staging/prod; canary/blue-green reduces blast radius
- GitOps (ArgoCD, Flux): desired state in Git, controller reconciles cluster to match
- Rollback strategy: feature flags (instant toggle), blue-green swap, image version pin

**Roadmap Planning & Prioritization**
- Align with business goals (OKRs), customer needs, and technical health (debt, reliability)
- Sequencing: tackle foundation work first (enable other items), deliver quick wins for credibility, defer nice-to-haves
- Risk identification: dependency on other teams, technical unknowns, timeline buffers
- Communication: regular stakeholder updates, explicit "not in scope" list, change management for scope additions

**Production Incident Management**
- During: SEV triage → incident commander → mitigation (rollback/hotfix) → status communication → logging
- After: blameless postmortem → action items with owners → knowledge sharing (runbook update, architecture review)
- On-call hygiene: SLO-based alerting (error budgets), reduce alert noise, actionable alerts only, clear escalation policies

**AI Infrastructure Migration Roadmap**

- **Three migration paths to AI-native** based on org maturity: (1) Bypass Pilot — independent GPU pool with basic admission/budget; for early exploration with high org uncertainty; (2) Domain-Isolated Platform — solidified shared governance across teams with formal platform-workload contracts; (3) AI-First Refactor — AI on the critical path; optimize by unit cost and tail latency
- **90-Day AI Infra implementation plan**: Days 0–30 = Visibility Foundation (cost/usage ledger with attribution dimensions, unit cost metrics, basic admission policies — goal: "can we see what is consuming what?"); Days 31–60 = Governance Infrastructure (GPU governance via MIG/MPS/vGPU, AI-ready network baseline, golden paths — goal: "can we isolate and control consumption?"); Days 61–90 = Enforcement and Migration (rate limiting/degradation/preemption policies, pilot migrations, formalize platform-workload contracts — goal: "is the closed loop operational?")
- **AI Landing Zone**: North star concept = compute governance loop + context tier architecture + org contracts; all agents/APIs/runtimes operate within this bounded zone; it is both technical and organizational — carries the responsibility boundary definitions essential for scaling
- **Platform/Workload team split**: Platform Team owns stable landing zones, governance capabilities, golden paths, shared infrastructure; Workload Team owns model selection, prompt logic, tool integration, SLO definitions; failures cascade when inter-team accountability boundaries aren't defined
- **AI SRE + ModelOps + FinOps triangle**: three functions requiring explicit collaboration contracts — AI SRE/Infra (reliability, capacity, governance plane), ModelOps (model lifecycle, inference optimization, deployment), FinOps (cost attribution, budget governance, chargeback/showback); without formal contracts, governance becomes reactive
- **FinOps as architecture, not reconciliation**: must be incorporated upfront as shared operating model; "after-the-fact reconciliation" = chargeback friction without behavior change; front-loaded FinOps = incentive alignment that drives efficient model selection and batching
- **Migration anti-patterns**: building APIs/agents without cost ledgers (runaway expenses), treating GPUs as ordinary cloud resources (contention), ignoring network topology (tail latency amplification), FinOps as reconciliation exercise (no incentive effect)
- **Scale definition for AI infra**: "If you cannot attribute the primary consumption of each agent/job to team/project/model/use-case, you haven't reached the 'scale' starting line" — attribution coverage is a scaling prerequisite, not a nice-to-have

## Key Questions

**Q: What are DORA metrics? How do they measure engineering performance?**
Answer framework: Four metrics — Deployment Frequency, Lead Time, MTTR, Change Failure Rate; elite tier benchmarks; explain the virtuous cycle: higher frequency → smaller batches → lower risk → lower CFR → faster recovery. Use to drive conversations about velocity programs.
> 中文提示：四个指标衡量工程效能；高频小批次是降低风险的关键机制，不是高风险

**Q: Describe the software development process. How do you ensure high quality for a release?**
Answer framework: Requirements → Design → Code → Test → Review → Deploy → Monitor; quality gates: automated tests (unit + integration + E2E), code review, static analysis, staging validation, canary rollout, monitoring + rollback plan, postmortem culture.

**Q: How do you handle production incidents — during and after?**
Answer framework: During — SEV triage, assign incident commander, prioritize mitigation over diagnosis (rollback first), communicate status publicly. After — blameless postmortem, identify contributing factors (not root cause), action items with owners and deadlines, update runbook.
> 中文提示：先止血再查因；事后 blameless 复盘是文化建设，不是追责

**Q: You lead a project with 2 junior engineers and a tight schedule. How do you manage it?**
Answer framework: Scope ruthlessly (MVP first), break work into clear tasks per engineer, pair-program on complex parts, daily standups for unblocking, protect them from scope creep, regular check-ins without micromanaging, communicate schedule risk to stakeholders early.

**Q: How do you balance engineering velocity with long-term technical debt and security investments?**
Answer framework: Phased approach — identify quick wins (no-policy or simple-policy apps first), track debt explicitly in roadmap, use error budgets to decide when to invest in reliability vs features, automate security checks (shift-left) to make security low-friction.

**Q: What's your checklist to avoid production bugs?**
Answer framework: Code review → automated unit/integration/E2E tests → static analysis → staging validation → feature flags for rollout control → canary deployment → monitoring/alerting configured before deploy → rollback plan documented → runbook updated.

**Q: What's a CI/CD setup you would implement for infrastructure deployment? What tools would you use?**
Answer framework: GitHub Actions / GitLab CI for build+test → ArgoCD/Flux for GitOps CD → image signing (cosign) for supply chain security → Flagger for canary analysis → automated rollback on health check failure → audit trail in Git history.
> 中文提示：GitOps = Git 是单一事实来源，controller 自动 reconcile；canary 用 Flagger 自动分析

**Q: What would you do in the first 90 days as an AI Infrastructure Manager?**
Answer framework: Three-phase plan — (1) Days 0–30: establish visibility (cost ledger with attribution dimensions, unit cost baselines, basic admission policies); (2) Days 31–60: build governance infrastructure (GPU sharing/isolation, network baseline, golden paths for teams); (3) Days 61–90: operationalize enforcement (rate limiting, degradation triggers, pilot migrations, formalize team contracts). Frame as: see what's happening → control what's happening → operate what's happening.

**Q: How would you migrate a cloud-native engineering organization to AI-native infrastructure?**
Answer framework: Three-path framework — Bypass Pilot (high uncertainty, explore safely), Domain-Isolated Platform (multi-team sharing, solidify contracts), AI-First Refactor (AI on critical path, optimize unit economics). Choice depends on org maturity and risk tolerance. Emphasize: "migration is not rebuilding the platform — it's using governance loops and org contracts to transform uncertainty into controllable engineering capabilities." Key anti-pattern: treating it as a pure technical migration without changing operating model.

**Q: How do you structure a platform team for AI infrastructure?**
Answer framework: Platform/Workload split is the foundational responsibility boundary. Platform team owns governance capabilities and golden paths; workload teams own model selection and business SLOs. Within platform, the AI SRE + ModelOps + FinOps triangle needs explicit collaboration contracts — not informal coordination. The failure mode is each function optimizing locally (SRE for reliability, FinOps for cost, ModelOps for capability) without shared objectives.

## Summary

Technical roadmap and software delivery practices are the operational backbone of engineering management. The DORA metrics give a shared language for measuring and improving delivery performance — the key insight is that high deployment frequency reduces risk (smaller batches, faster feedback) rather than increasing it. For infrastructure teams, the additional challenge is balancing service reliability (SRE error budgets, on-call health) against feature velocity. Effective roadmapping means making the sequencing rationale explicit — stakeholders need to understand not just what is planned but why in that order, especially when saying "not yet" to something.

For AI infrastructure specifically, the roadmap challenge is institutional as much as technical. The transition from cloud-native to AI-native requires changing the operating model — not just deploying new infrastructure components. The 90-day plan framework (Visibility → Governance → Enforcement) provides a structured answer to "what would you do in your first 90 days?" that covers both technical milestones and organizational change. The AI Landing Zone concept ties the technical and organizational elements together: a bounded operating environment where all agents and APIs must run, governed by explicit platform-workload team contracts. This prevents the most common failure mode — "functional but unsustainable" systems where technical capability outpaces governance readiness.

> 面试重点：DORA 四指标 + elite 基准；小批次高频发布是降低风险的反直觉结论；postmortem 文化是可靠性的制度保障；90 天计划（可见性→治理→执行）；Platform/Workload 分工 + AI SRE/ModelOps/FinOps 三角

## Raw Material
- [[raw_material/books/ai-native-infra/part3-org-migration]]
