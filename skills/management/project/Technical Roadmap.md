---
title: Technical Roadmap
category: management/project
tags: [roadmap, planning, prioritization, stakeholders, project-management]
status: in-progress
priority: medium
last_updated: 2026-04-13
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

**Roadmap Layering & Horizon**
- North Star roadmap: org/domain long-term direction — a plan, not a commitment; sets strategic intent (3-year horizon)
- Yearly/quarterly roadmap: more commitment-oriented; primary communication tool for stakeholders and teams
- Relationship to OKRs: roadmap typically precedes OKR setting (Key Results tie to deliverables); OKRs in turn inform the next roadmap cycle — bidirectional influence
- Common formats: **Now / Next / Later** (honest about uncertainty; avoids false commitment in "Later"); **OKR-linked** (each KR maps to specific roadmap items); **Themes-based** (org-level; shows strategic why, not feature list)
- Committed vs. stretch split: mark items explicitly — prevents over-commitment and manages stakeholder expectations

**Prioritization Frameworks for Infrastructure**
- **RICE**: Reach × Impact × Confidence ÷ Effort — quantified scoring; useful for feature roadmaps where many items compete
- **MoSCoW**: Must / Should / Could / Won't — fast layering; good for scope-cut conversations
- **Impact vs. Effort 2×2**: intuitive quadrant; high-impact + low-effort = do now; high-impact + high-effort = plan; low-impact = challenge the assumption
- **Jobs to be Done**: prioritize by user scenario, not by feature — prevents shipping features that don't solve actual problems
- Infrastructure-specific weighting:

| Work Type | Priority Driver | Common Trap |
|---|---|---|
| Reliability/SRE | Error budget burn rate, SLO breach frequency | Fix the incident but not the root cause |
| Tech debt | Lead time growth, onboarding time | Invisible debt always gets squeezed by features |
| Security/compliance | Regulatory deadline or CVE severity | Reactive; no proactive roadmap |
| Platform new capabilities | User demand signals, strategy alignment | Built but unadopted (missing golden path + adoption plan) |
| Migration/upgrade | Risk window (EOL, version support) | Underestimate migration complexity; no phased rollback |

- Set a fixed budget ratio for tech debt (e.g., 20–30% of capacity) to make it visible and defended
- Top-down + bottom-up blending: org-level roadmap + team members' input (TOIL → platform feature, tech debt items) → score by impact/effort

**Stakeholder Management & Buy-in**
- **RACI/RASCI**: explicitly assign Responsible, Accountable, (Support), Consulted, Informed per item — prevents diffuse ownership
- **Dependency map**: surface all cross-team dependencies explicitly in the roadmap; set up early warning signals instead of discovering slips at deadline
- **Pre-wiring (预热对齐)**: socialize important decisions in 1:1s before group forums — avoids public disagreement
- **"Not in scope" list**: proactively maintain and publish what is NOT planned this cycle — manages scope creep and sets clear expectations
- **Reporting to leadership**: use business language (risk, cost, velocity impact), not technical terms; communicate one quarter ahead; front-load risk transparency ("here are the risks and my mitigation") rather than waiting to be discovered; use data (DORA, SLO, customer feedback) to justify prioritization
- **Weekly status updates**: Delivery / Commitment / Blocker format for VP/Director — especially Blocker, where you actively seek leadership support

**Roadmap Execution Challenges**
- **Mid-execution scope change**: "adding one thing means pushing one thing" — make the trade-off explicit to stakeholders; don't silently absorb scope
- **Dependency slip**: early dependency exposure; phased agreements (immediate improvement now + roadmap commitment for harder cases later); always have a Plan B
- **Completion rate**: track via OKRs (complete vs. partial); review risks in sprint retros; DX Core 4 "stable priorities" is a predictor of high-performing teams
- **Graduated approach**: when starting from a poor baseline (e.g., reliability < 90%), set achievable intermediate targets rather than aspirational goals — builds team confidence and avoids immediate budget burn

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

**Q: Walk me through how you build a technical roadmap for your team. What's your process from start to finish?**
Answer framework: Start with inputs — align to org OKRs and leadership strategy, gather customer/user feedback, audit tech health (debt, SLO, lead time trends) and team member input (TOIL, blockers). Score items using Impact vs. Effort (or RICE for feature-heavy backlogs). Format as Now/Next/Later or OKR-linked; commit vs. stretch split for realistic delivery. Communicate through dependency maps, "not in scope" list, and pre-wiring key stakeholders before group sessions. Track via OKR completion rate and sprint retros.
> 可结合 Engineering Velocity Program（metrics-first: identify bottleneck before planning）或 Platform Engineering at Scale（ops → platform mental model shift first）

**Q: How do you balance short-term reliability/maintenance work against long-term feature investments?**
Answer framework: Reserve an explicit budget ratio for reliability/SRE (e.g., 20–30%) so it doesn't disappear under feature pressure. Use error budget burn rate as the objective signal — when burn rate exceeds threshold, reliability pre-empts feature work (not as a judgment call but as a pre-committed policy). For tech debt, quantify the drag in business terms (lead time increase, incident rate) to make it visible. Use a graduated SLO approach: set achievable initial targets (e.g., 99% not 99.9%), stabilize, then raise the bar.
> 可结合 SRE reliability roadmap — reliability from < 90% → 99% → 99.9% in 6 months using graduated targets and error budget policy

**Q: Describe a time you had to significantly change course on a roadmap mid-execution.**
Answer framework: Establish the context (external or internal trigger?), explain how you assessed impact to existing commitments, describe how you made the trade-off explicit to stakeholders ("adding DoJ means pushing X"), and outline how you re-sequenced (mitigation first in current sprint, root-fix converted to a future planned item). Show that the change was managed, not absorbed.
> 可结合 DoJ/Jade program — hard legal deadline mid-year; required de-prioritizing planned items (e.g., ECR upgrade); triple-track (Technical/Process/People) with rehearsals to manage unknown risk

**Q: How do you get stakeholder buy-in for a roadmap that includes significant infrastructure investment with no visible user-facing features?**
Answer framework: Translate infrastructure value into business language — risk reduction, cost avoidance, developer velocity (DORA metrics), reliability (SLO/SLI). Show graduated early wins to build credibility before asking for the bigger investment. Use data: "we had X incidents/week before, Y after Phase 1." Frame the investment as making future feature delivery faster and safer, not as pure maintenance.
> 可结合 Platform Engineering at Scale — leadership alignment came naturally because compliance + reliability pressures made the "ops → platform" case obvious; harder sell was team confidence (selected high-potential team member, phased delivery to prove the model)

**Q: How do you manage a roadmap when there are multiple stakeholders with competing priorities?**
Answer framework: Use RASCI to make ownership and consultation rights explicit — prevents every stakeholder from feeling entitled to veto. Maintain a published "not in scope" list to pre-empt requests. For direct conflicts, surface the trade-off with data and let leadership make the call (don't absorb the conflict silently). Phased agreements — give the lower-priority stakeholder a roadmap commitment for their item with a specific timeline — manage the loss of the immediate battle while preserving the relationship.
> 可结合 Engineering Velocity Program — security team's policy performance optimization low-priority for them, blocking blue/green adoption; resolved by triaging into tiers (complex pools vs. standard apps) and negotiating a phased fix for standard apps

**Q: How do you plan and manage a multi-year technical transformation (e.g., large-scale platform migration)?**
Answer framework: Phase by risk — start where failure is cheapest and deliver early value to build credibility and team confidence. Define clear "done criteria" per phase (not vague milestones). Make rollback strategy explicit per phase. Manage stakeholder patience with early wins (e.g., decommission automation before cluster build). Scope will expand as you succeed — document that explicitly and get new resourcing conversations started early.
> 可结合 Automated Cluster Management — 1.5 year roadmap; 40/60 new feature/ops balance; decommission first (lowest risk, early win), cluster build second; scope expanded organically after each success

## Summary

Technical roadmap and software delivery practices are the operational backbone of engineering management. The DORA metrics give a shared language for measuring and improving delivery performance — the key insight is that high deployment frequency reduces risk (smaller batches, faster feedback) rather than increasing it. For infrastructure teams, the additional challenge is balancing service reliability (SRE error budgets, on-call health) against feature velocity. Effective roadmapping means making the sequencing rationale explicit — stakeholders need to understand not just what is planned but why in that order, especially when saying "not yet" to something.

For AI infrastructure specifically, the roadmap challenge is institutional as much as technical. The transition from cloud-native to AI-native requires changing the operating model — not just deploying new infrastructure components. The 90-day plan framework (Visibility → Governance → Enforcement) provides a structured answer to "what would you do in your first 90 days?" that covers both technical milestones and organizational change. The AI Landing Zone concept ties the technical and organizational elements together: a bounded operating environment where all agents and APIs must run, governed by explicit platform-workload team contracts. This prevents the most common failure mode — "functional but unsustainable" systems where technical capability outpaces governance readiness.

> 面试重点：DORA 四指标 + elite 基准；小批次高频发布是降低风险的反直觉结论；postmortem 文化是可靠性的制度保障；90 天计划（可见性→治理→执行）；Platform/Workload 分工 + AI SRE/ModelOps/FinOps 三角

In practice, roadmap management involves constant prioritization trade-offs between feature work, reliability, tech debt, and compliance obligations. The most defensible prioritization process combines top-down strategy alignment with bottom-up team input, uses data (DORA, SLO burn rate, lead time) to make trade-offs visible, and maintains a fixed budget allocation for reliability and tech debt so they aren't perpetually squeezed. The "Now / Next / Later" format is more honest and reduces stakeholder misalignment than feature lists with false quarterly precision. Managing execution means treating scope changes as explicit trade-offs (not silent additions), surfacing cross-team dependencies early, and having phased agreements ready for lower-priority stakeholders so relationships survive priority conflicts. Graduated approaches — setting intermediate targets rather than aspirational ones — are especially powerful for reliability turnarounds, where the first goal is team confidence and system stability, not maximum SLO.

> 补充面试要点：Now/Next/Later 格式诚实表达不确定性；RASCI + "not in scope" list 防止 scope creep；依赖管理要有 early warning + Plan B；graduated SLO 方法从低目标开始建立团队信心；infra roadmap 要用业务语言（风险、成本、速度）而非技术语言向 leadership 汇报

## Key Terms

**Prioritization Frameworks**
- `RICE` · `MoSCoW` · `Impact vs. Effort 2×2` · `Jobs to be Done` · `committed vs. stretch`

**Roadmap Formats & Horizons**
- `Now / Next / Later` · `OKR-linked roadmap` · `Themes-based roadmap` · `North Star roadmap` · `quarterly roadmap` · `rolling horizon`

**Stakeholder Management**
- `RACI` · `RASCI` · `pre-wiring` · `"not in scope" list` · `dependency map` · `phased agreement` · `scope creep`

**Execution & Tracking**
- `error budget` · `error budget policy` · `burn rate` · `graduated approach` · `completion rate` · `milestone` · `phased rollback` · `fast win` · `early warning system`

**Tools & Processes**
- `Airtable` · `JIRA` · `OKR` · `DORA dashboard` · `scrum of scrum` · `sprint retro`

**Infrastructure-specific**
- `golden path` · `adoption plan` · `self-service capability` · `tech refresh` · `EOL window` · `compliance-driven roadmap`

## Raw Material
- [[raw_material/books/ai-native-infra/part3-org-migration]]
- [[raw_material/management/project/Technical Roadmap - personal]]
