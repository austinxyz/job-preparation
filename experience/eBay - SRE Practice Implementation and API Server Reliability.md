---
title: eBay - SRE Practice Implementation and API Server Reliability
type: Additional
signal_areas: [Ownership, Growth, Leadership, Scope]
skills: [sre, slo-engineering, incident-management, on-call-design, blameless-postmortem, toil-reduction, observability, ai-augmented-ops, kubernetes, apf]
company: eBay
date: 2023-09
impact: high
growing_link:
---

# eBay - SRE Practice Implementation and API Server Reliability

## Context

eBay's Kubernetes API servers — the control plane for 200+ clusters — had severe reliability problems. The most extreme case: a Dev API Server stayed down for two full days, blocking developer work across dozens of engineering teams. The Production Federated API Server, the primary entry point for all platform clients, was operating below 90% availability. Root causes were compounding: APF (API Priority and Fairness) was misconfigured and allowed client bursts to starve critical traffic; etcd had no governance and was growing unbounded; alert coverage was patchy; and there was no structured incident process — every outage was handled ad hoc by whoever happened to be available.

The team had not adopted SRE practices yet — no SLOs, no error budget, no runbooks, no on-call rotation in place. eBay's central SRE team had an established framework covering SLO/SLI structure, error budget policy, incident templates, and on-call design. The gap wasn't the framework — it was that this team hadn't implemented it, and nobody had made the specific decisions about what targets made sense for the API server context. Fixing the technical problems in isolation wasn't enough — we needed to implement the operational model properly and make it stick.

## Actions

**SLO and Error Budget Implementation:**
- Following eBay's SRE framework, I worked with the team to select availability and latency as the primary SLIs for the API server — for a control plane consumed by platform clients, request success rate and response time are what clients actually experience, so that's where measurement belonged.
- I deliberately set the initial SLO at 99% rather than 99.9% for the Federated API Server. Starting aggressive from a broken baseline would have burned error budget immediately and taught the team to ignore the signal. 99% gave meaningful headroom to improve while making progress measurable. I graduated the target to 99.9% as infrastructure stabilized and the team developed confidence in the measurement methodology.
- I used Kubernetes built-in Prometheus metrics as the SLI signal source to minimize instrumentation overhead — the metrics already existed, so we could start measuring immediately without a parallel instrumentation project.
- I established an error budget burn rate policy with a deliberately conservative 95% threshold to trigger action — starting conservative to build baseline understanding before tightening. I set up a regular team cadence to review incidents, alerts, and burn rate; when burn rate spiked, triage focused on the root cause (release? configuration change? specific client APF?), and the burn rate signal determined mitigation priority.

**Incident Management Process:**
- I built a multi-level alert hierarchy: primary SLO/SLI alerts as the pager trigger; secondary alerts on API server instance health, etcd size, etcd compaction failures, and APF queue depth — each added after a real incident exposed the gap.
- I established a runbook standard for every alert: triage steps, mitigation actions, escalation criteria — the team wrote them, I reviewed. The goal was that on-call engineers had a defined SOP for common failure modes rather than debugging from first principles at 2am.
- I established 24/7 PagerDuty coverage with an explicit escalation path: on-call engineer → tech lead → engineering manager.

**Blameless Postmortem Culture:**
- I introduced a standardized RCA template focused on: timeline, MTTD, MTTR, root cause (technical, not personal), why the issue wasn't caught earlier, and prevention steps.
- I tracked follow-up action items in the sprint backlog alongside feature work — not a separate postmortem board that would decay — so RCA outputs had the same accountability as any other committed work.
- I explicitly framed postmortems as learning exercises and recognized engineers who wrote thorough RCAs, not just engineers who fixed the immediate issue.

**On-Call Rotation Design:**
- Initial design: follow-the-sun with US and China teams covering ~12 hours each, providing near-24/7 coverage without requiring night shifts — designed with the team and agreed collectively.
- When the China team lost production environment access due to a compliance constraint, I drove a redesign of the rotation: US team as primary, India/Europe team as secondary — covering the gap while the India/Europe team ramped toward production readiness. The long-term plan was to evolve back to follow-the-sun as the new teams gained production access.

**AI-Augmented Triage:**
- The dominant toil category was triage of bad-instance and release-induced API server degradation — recurring, time-consuming, requiring engineers to manually correlate signals across API server metrics, etcd metrics, and error logs.
- I led the team to build an AI triage agent using MCP servers to automatically collect cross-system signals on incident trigger and produce a structured triage summary: likely root cause, affected clients, recommended mitigation steps.
- Human approval was required for all mitigation actions — the agent handled information gathering and synthesis, not execution.

## Results

- Federated API Server availability improved from below 90% to a 30-day rolling average of 99%+ in dev environments; Production sustained 99.9%.
- Dev API Server sustained outages (the 2-day incident) eliminated — runbooks and alerts caught degradation before it escalated to full unavailability.
- MTTD reduced to ~20 minutes; MTTR reduced from 24+ hours (worst case) to under 1 hour for defined incident classes.
- Incident frequency dropped from multiple per week to rare occurrences as postmortem action items closed the recurring failure patterns.
- On-call cognitive burden reduced: AI triage cut time-to-diagnosis from 30–60 minutes to under 10 minutes for common incident classes.
- On-call rotation survived a compliance-driven team change (China team losing prod access) without service disruption.

## Learnings

- Starting SLO targets conservatively was the right call and counterintuitive to explain to leadership. An SLO you can't sustain teaches engineers to ignore the signal — which is worse than no SLO. The graduated approach (99% → 99.9%) gave the team a target they could actually hit, which built the reliability discipline before we tightened the standard.
- Tracking postmortem action items in the sprint backlog was critical to closing the loop. Teams that put RCA items on a separate tracking board have RCAs that generate learning but don't generate fixes. Mainlining the actions into sprint planning made follow-through the default, not the exception.
- The AI triage tool was most valuable not because it was fast, but because it was consistent. An on-call engineer at 2am is tired and under pressure — they miss signals. The agent gathered the same signals every time, in the same order, with no gaps. That consistency was what reduced MTTD.

## Signal Areas

**Primary:** Ownership (designed and delivered the entire SRE system from zero — SLOs, error budget, runbooks, on-call, postmortems, AI triage — accountable for the full outcome), Growth (built a reliability discipline that didn't exist; graduated the team from ad hoc firefighting to systematic, measurable incident management)

**Secondary:** Leadership (blameless culture required explicit framing and recognition patterns to take hold; on-call redesign navigated a compliance-driven constraint without service disruption), Scope (control plane reliability for 200+ clusters and all platform clients across eBay)

## Related Skills
- [[skills/tech/infra/SRE Practices and SLO Engineering]]
- [[skills/tech/infra/Observability and Incident Management]]
- [[skills/tech/infra/Kubernetes]]
- [[skills/management/people/Engineering Team Management]]

## Interview Usage
- 适用 BQ：Tell me about a time you implemented SRE practices on a team that had none
- 适用 BQ：How do you design SLOs when the baseline reliability is very poor?
- 适用 BQ：Describe a time you built a blameless culture around incidents
- 适用 BQ：Tell me about a time you reduced on-call toil using tooling or automation
- 适用 Technical：How would you define SLIs/SLOs for a Kubernetes API server?
- 适用 Technical：How do you use AI to augment incident response without introducing risk?
- 适用 JD 关键词：SRE, SLO, SLI, error budget, incident management, on-call, blameless postmortem, toil reduction, observability, reliability engineering

## Key Questions

**Q: How do you set SLO targets when your baseline reliability is already very poor?**
Talking points: Don't set an aspirational target — set one that's above current performance but achievable within months. The goal is to make progress measurable, not to declare a false standard. Starting at 99% from <90% gave meaningful headroom without burning error budget immediately. An SLO you can't sustain is worse than no SLO — it teaches engineers to ignore the signal. Graduated: 99% → 99.9% as infrastructure stabilized.

**Q: Walk me through how you designed the error budget policy. How did you use it operationally?**
Talking points: Error budget converts a reliability debate into a math problem. Daily burn rate reviews in early months to calibrate. Burn rate spike → root cause triage (release? client? infra?). Burn rate determined mitigation priority: high burn from a specific client → escalate APF tuning; high burn from a release → require staging gate. Started at 95% threshold to avoid constant false-exhaustion signals; tightened as the team learned the system.

**Q: How do you build a blameless postmortem culture when engineers are used to being blamed?**
Talking points: Template the process so it's structured, not a freeform interrogation. Centralize RCAs so the org learns across incidents. Track follow-up actions in the sprint backlog — not a separate queue that decays. Explicitly recognize engineers who write thorough RCAs. Culture shifts when engineers see that postmortems produce improvements, not punishments.

**Q: How do you design on-call rotations for a global team with uneven production access?**
Talking points: Start with the constraint (compliance mandate removed China team's prod access). Follow-the-sun was the ideal; primary/secondary was the pragmatic bridge. India/Europe as secondary during ramp-up gives real incident exposure without sole responsibility. Plan the transition explicitly — what milestones enable them to go primary? Don't leave the interim state permanent by default.

**Q: How did you use AI in incident response without introducing new risk?**
Talking points: AI handled information gathering and synthesis — pulling metrics, logs, cross-system correlation — the tasks where speed matters and human bottleneck is worst. Human approval gate on all mitigation actions; AI never executed changes autonomously. On-call engineer gets a structured triage summary in under 10 minutes instead of manually querying 4–5 systems. Design principle: AI augments decision-making speed, doesn't replace judgment.

## Summary

Implementing SRE practices for eBay's Kubernetes API server fleet meant adopting eBay's existing SRE framework — SLO/SLI structure, error budget policy, incident templates, on-call design — while simultaneously dealing with an active reliability crisis. The framework existed; the work was making the specific decisions for this context and making them stick. The most consequential choices were deliberately conservative: starting the SLO at 99% rather than 99.9% gave the team room to improve without constant error budget exhaustion, and the graduated approach (99% → 99.9% as infrastructure stabilized) built reliability discipline before tightening the standard. An SLO you can't sustain teaches engineers to ignore the signal — which is worse than no SLO.

The incident management work had two components that compounded each other: the process (runbooks, PagerDuty hierarchy, blameless postmortems, centralized RCA knowledge base tracked in sprint backlog) reduced the organizational cost per incident; and the AI-augmented triage agent reduced time-to-diagnosis from 30–60 minutes to under 10 for common failure classes. Together these brought MTTD to ~20 minutes and MTTR under 1 hour. The cumulative effect of closed postmortem action items eliminated entire incident categories over time — which is the goal of SRE practice, not just faster response.

## Raw Material
- [[raw_material/tech/infra/SRE Practices and SLO Engineering - personal]]
