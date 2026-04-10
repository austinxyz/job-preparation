---
title: SRE Practices and SLO Engineering
category: tech/infra
tags: [sre, slo, sli, error-budget, incident-management, blameless-postmortem, reliability, toil]
status: draft
priority: high
last_updated: 2026-04-10
created_from_jd: "[[positions/Manager, DevOps, SRE & AI Infrastructure - AppZen]]"
---

# SRE Practices and SLO Engineering

## Knowledge Map
- 前置知识：observability (metrics/logs/traces), incident management, service architecture
- 延伸话题：error budget policies, toil elimination, chaos engineering, SLO-based alerting, Google SRE book
- 管理关联：reliability culture, blameless post-mortems, on-call design, SRE team charter

## Core Concepts

**SLI / SLO / SLA — the reliability contract stack**
- **SLI** (Service Level Indicator): a quantitative measure of service behavior — e.g., request success rate, p99 latency, availability. Must be measurable from the user's perspective.
- **SLO** (Service Level Objective): the target value for an SLI — e.g., "99% availability over a 30-day rolling window." Owned by the engineering team; defines what "reliable enough" means.
- **SLA** (Service Level Agreement): a contractual commitment with consequences for breach, usually set *below* the SLO to create a safety margin.
- Rule of thumb: SLA < SLO < 100%. The gap between SLO and SLA is the safety margin for remediation before business consequences kick in.
- **eBay context**: K8s API Server SLIs focused on availability and latency. API Server is Control Plane — primarily consumed by the Platform team, not end-users directly — so 99% was the right starting SLO, not 99.9%. Different SLO targets for different tiers: Federated API Server (highest impact, addressed first) vs. Cluster API Server vs. Dev environments.

**Setting SLOs: start feasible, not aggressive**
- Starting with an overly ambitious SLO (99.9% before reliability baseline is known) causes immediate error budget exhaustion, alert fatigue, and demoralization.
- **eBay approach**: started at 99% when the system had frequent incidents; used real data to understand baseline before committing to higher targets. Daily error budget reviews early on to track consumption and identify root causes.
- K8s provides built-in metrics, making SLI instrumentation straightforward for API Server (API request success rate, etcd latency, etc.).
- Complexity driver at eBay: Federated API Server aggregates many clusters; large total call volume; clients without proper APF (API Priority and Fairness) settings can starve each other, causing cascading reliability degradation.

**Error budget — the reliability budget mechanism**
- Error budget = 1 − SLO. A 99% SLO gives 1% budget = 432 minutes/month. Every minute of downtime or SLI breach burns budget.
- When budget is being consumed: trigger root cause investigation. Key question: was it caused by a release/change event, or by a specific client with misconfigured APF?
- Error budget policy: when budget runs low, trigger reliability freeze (no new deployments until budget recovers); when budget is healthy, team has room to take risks and ship features.
- **eBay approach**: early data was noisy, so started with a generous budget threshold (95%), then gradually tightened. Policy reviews triggered by daily dashboards showing consumption rate.

**Alert design: SLO-first, symptom-second**
- Primary alerts should fire on SLI/SLO violations (user-facing symptoms), not on internal metrics. This reduces false positive alert fatigue and ensures on-call focuses on real user impact.
- Secondary alerts fire on leading indicators: API server instance health, etcd health/growth rate — these catch problems *before* SLO is breached.
- Multi-tier alert structure at eBay: (1) SLO burn rate alert → page on-call; (2) API server instance alerts; (3) etcd governance alerts (e.g., etcd unbounded growth was a recurring root cause — required dedicated alerting and SOP).
- Every alert must have a corresponding runbook and SOP. Alerts without runbooks train engineers to ignore them.

**Incident management — structure reduces MTTR**
- Key metrics: **MTTD** (Mean Time to Detect) and **MTTR** (Mean Time to Recover). Both should be minimized; MTTD is often underinvested.
- Escalation path: on-call engineer → tech lead → engineering manager. Clear levels prevent ambiguity about when to escalate.
- 24/7 pager with complete runbook coverage: every known failure mode has a documented triage path, recovery procedure, and rollback plan.
- At eBay, specific incident patterns (APF misconfiguration, etcd governance failures) were root-caused, documented in SOPs, and had dedicated alerts added post-incident. Each RCA made the next incident of the same type faster to resolve.

**Blameless post-mortems — making RCA compound**
- RCA template focus: what in the *system* allowed this to happen? Why was MTTD/MTTR high? What changes prevent recurrence? Avoid "who made the mistake."
- Centralized RCA repository: all past incidents in one place, searchable. New on-call engineers can understand failure patterns before experiencing them live.
- Every RCA produces follow-up action items with named owners and deadlines. Actions without owners are observations, not improvements. Track action completion rate as a team health metric.
- **eBay practice**: recognized team effort publicly when reliability milestones were hit. Blameless culture only works if the organization also celebrates progress — not just investigates failures.

**Toil reduction — eliminating repetitive operational work**
- Google SRE definition of toil: manual, repetitive, automatable work that grows linearly with service scale and provides no lasting value.
- Operational threshold: if toil exceeds ~50% of on-call time, it crowds out reliability engineering work and causes burnout.
- **eBay classification**: work that consumes on-call time, has no SOP, and recurs regularly = toil. Primary K8s API Server toil: triage for degraded/bad instances and release-caused reliability events.
- **AI-powered triage at eBay**: MCP server collects metrics and logs; AI agent performs combined diagnosis. Reduces the time from alert to root-cause hypothesis from 20–30 min to near-instant for known failure patterns. Allows junior on-call engineers to handle incidents that previously required senior escalation.
- Platform investment to eliminate toil permanently: build automation and tooling so that the next occurrence of a known failure is resolved without human triage.

**On-call design — coverage without burnout**
- On-call models: **follow-the-sun** (regional handoff every 12h, no one wakes up) vs. **primary/secondary** (24h primary who pages secondary when needed). Follow-the-sun is better for engineer wellbeing; requires coverage in enough timezones.
- **eBay evolution**: started with US/China follow-the-sun (12h each). After China lost production access, shifted to primary/secondary with India/Europe as secondary while gradually building their capability toward follow-the-sun again.
- Escalation design should be explicit, not assumed. On-call person should know exactly when to escalate and to whom within minutes of an unresolved page.
- Work-life balance principle: no engineer should be on-call more than 25% of their time. Sustained over-on-call drives attrition on the best engineers (those most able to find new roles).

**SRE team model — embedded vs. centralized**
- **Centralized SRE**: dedicated SRE team owns reliability across services. Risk: SRE becomes an ops dumping ground; dev teams offload reliability work.
- **Embedded SRE**: SREs join product/infra teams directly. Risk: SRE practices fragment across teams; no shared tooling.
- **Hybrid (eBay model)**: embedded SREs with *rotation* (team members take on SRE responsibilities on rotation); centralized SRE team provides tooling, best practices, and standards. Rotation builds reliability ownership across the broader team rather than concentrating it in specialists.
- Reliability tickets belong in the sprint backlog, not a separate track. Team OKRs included toil reduction, MTTD/MTTR improvement, and SLO attainment. This makes reliability work visible and comparable to feature work.

**Reliability culture — shifting ownership left**
- Key principle: every engineer on-calls for the systems their team builds. Rotating on-call builds empathy and ownership; dedicated ops teams create a "throw it over the wall" dynamic.
- Encourage feature work that permanently resolves reliability problems, not just patches that defer the issue. "Fix the system, not the symptom."
- Data-driven prioritization: identify top 3 reliability drivers, fix those first. Don't spread effort across 10 issues simultaneously.

## Key Questions

**Q: How do you define SLOs for a service, and how do you pick the right target?**
Answer framework: Start with SLI selection — what metrics matter to users (availability, latency p99, error rate). Set the SLO based on the service's role and user impact: Control Plane / platform services can tolerate 99%; user-facing critical services might need 99.9%. At eBay, the K8s Federated API Server started at 99% because the primary consumers were platform engineers, not end-users, and the initial baseline was unknown. Starting conservative (then raising) beats starting aggressive (and immediately exhausting budget). Distinguish SLO (engineering target) from SLA (business contract with a safety margin below the SLO).

**Q: What is an error budget, and how does it influence team behavior?**
Answer framework: Error budget = 1 − SLO. It gives the team a quantified "risk allowance" — while budget is healthy, the team can ship aggressively; when budget runs low, trigger reliability freeze and root-cause investigation. The policy shifts behavior: instead of debating "is this deployment too risky?", the question becomes "how much budget do we have?". At eBay, daily budget reviews early in the reliability journey helped identify whether consumption was coming from release events or from client-side APF misconfigurations — two very different interventions.

**Q: How did you structure incident management at eBay? What reduced MTTR most?**
Answer framework: Multi-tier alerts (SLO burn rate as primary, component health as secondary); runbooks for every known failure mode; 24/7 pager with explicit escalation path (on-call → tech lead → EM). The biggest MTTR reduction came from (1) investing in runbook quality after each incident so the next occurrence was faster, and (2) AI-assisted triage (MCP server + AI agent analyzing metrics and logs) for known failure patterns, reducing time-to-diagnosis from ~30 minutes to near-instant. Track MTTD separately from MTTR — many teams optimize recovery but not detection.

**Q: How do you run blameless post-mortems? What makes them effective?**
Answer framework: Template focuses on system failure (not individual error): what allowed this to happen, why was MTTD/MTTR high, what changes prevent recurrence. Centralize all RCAs so institutional knowledge compounds. Every RCA must produce named-owner action items with deadlines — observations without owners are not improvements. Track action completion rate. At eBay, the centralized RCA repository meant new on-call engineers could study past failure patterns before encountering them live, significantly reducing escalation rate.

**Q: What counts as toil and how do you reduce it?**
Answer framework: Toil = repetitive, manual, automatable work that grows linearly with scale and provides no durable value. At eBay, the primary K8s API Server toil was incident triage — diagnosing bad instances and release-caused degradation without a documented SOP. Eliminated it in two ways: (1) built SOPs and runbooks that made triage deterministic; (2) built AI-assisted triage using MCP server + AI agent to collect metrics/logs and diagnose known patterns automatically. Measure toil as % of on-call time; if > 50%, it's crowding out reliability engineering. Fix by building platform automation, not by adding on-call headcount.

**Q: How do you design on-call to prevent burnout while maintaining coverage?**
Answer framework: Preferred model is follow-the-sun (no one wakes up for incidents outside their timezone) but requires geographic distribution. At eBay, pivoted from US/China follow-the-sun to primary/secondary when China lost production access, with India/Europe as secondary while building their capability. Two hard rules: no engineer on-call > 25% of their time, and every page must have a runbook — undocumented pages train engineers to ignore alerts. Escalation path (on-call → tech lead → EM) must be explicit and time-boxed.

**Q: How do you build a reliability culture without a dedicated SRE team?**
Answer framework: Rotate on-call across all team members — this builds ownership and empathy faster than any process. Put reliability tickets in the sprint backlog alongside feature work — if it's not in the sprint, it doesn't get done. Use team OKRs to make reliability improvements measurable: reduce toil X%, improve MTTD from Y to Z min, hit SLO target. At eBay, the combination of rotation + OKRs + centralized tooling from the SRE platform team created a culture where engineers saw reliability work as core to their role, not as ops overhead. Blameless culture requires publicly recognizing reliability wins, not just investigating incidents.

## Summary

SRE practices provide a systematic framework for managing reliability as an engineering problem rather than an ops firefighting exercise. The SLI/SLO/error budget stack is the foundation: SLIs measure service behavior from a user perspective, SLOs set the target, and error budgets convert reliability into a quantified risk allowance that directly governs deployment velocity. The key insight is that reliability and feature velocity are in tension — error budgets make that tension explicit and data-driven rather than political. At eBay, the K8s API Server reliability turnaround applied this framework to a complex control-plane service: starting with a feasible 99% SLO (not aggressive), identifying the top root causes (APF misconfigurations, etcd governance failures), building SOPs for each, and gradually tightening targets as baseline improved from frequent incidents to 99%/99.9% (Dev/Production) on a 30-day rolling window.

The operational practices that have the most leverage are: (1) alert design — primary alerts on SLO burn rate (user-visible symptoms), secondary on component health (leading indicators); (2) runbook discipline — every alert must have a corresponding SOP or it becomes noise; (3) blameless RCAs with centralized tracking and named-owner action items — this is how institutional reliability knowledge compounds rather than repeating. Toil reduction is a force multiplier: eliminating repetitive manual work (through SOPs, automation, and AI-assisted triage) frees on-call capacity for reliability engineering rather than firefighting. At eBay, MCP-powered AI triage reduced diagnosis time for known failure patterns from ~30 minutes to near-instant, enabling junior engineers to handle incidents that previously required senior escalation.

Building reliability culture requires structural investment, not just tooling: rotating all engineers through on-call builds ownership; reliability OKRs make improvement measurable; centralized RCA repositories make learning compound across the team. The SRE team model that works at scale is hybrid — embedded rotation builds ownership in each team, while a centralized SRE platform team provides tooling and standards. The anti-pattern to avoid is dedicated SRE specialists who absorb all on-call load: this creates a "throw it over the wall" dynamic where dev teams stop owning reliability outcomes.

## Raw Material
- [[raw_material/tech/infra/SRE Practices and SLO Engineering - personal]]

## Raw Material
- [[raw_material/tech/infra/SRE Practices and SLO Engineering - personal]]
