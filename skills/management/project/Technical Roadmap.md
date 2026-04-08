---
title: Technical Roadmap
category: management/project
tags: [roadmap, planning, prioritization, stakeholders, project-management]
status: stub
priority: medium
last_updated: 2026-04-06
created_from_jd:
---

# Technical Roadmap

## Knowledge Map
- Prerequisites（前置知识）：[[Engineering Team Management]]
- Related Topics（延伸话题）：[[OKRs and Goal Setting]], [[Cross-team Collaboration]], [[Risk Management]]
- Management（管理关联）：[[People Management]]

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

## Summary

Technical roadmap and software delivery practices are the operational backbone of engineering management. The DORA metrics give a shared language for measuring and improving delivery performance — the key insight is that high deployment frequency reduces risk (smaller batches, faster feedback) rather than increasing it. For infrastructure teams, the additional challenge is balancing service reliability (SRE error budgets, on-call health) against feature velocity. Effective roadmapping means making the sequencing rationale explicit — stakeholders need to understand not just what is planned but why in that order, especially when saying "not yet" to something.

> 面试重点：DORA 四指标 + elite 基准；小批次高频发布是降低风险的反直觉结论；postmortem 文化是可靠性的制度保障

## Raw Material
