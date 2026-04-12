---
title: eBay - SRE Practice Implementation and API Server Reliability
type: experience
skills: [sre, slo-engineering, incident-management, on-call-design, blameless-postmortem, toil-reduction, observability, ai-augmented-ops, kubernetes, apf]
company: eBay
date: 2023-09
impact: high
growing_link:
---

# eBay - SRE Practice Implementation and API Server Reliability

## Situation

eBay's Kubernetes API servers — serving as the control plane for 200+ clusters across multiple environments — had severe reliability problems. The most extreme case: a Dev API Server stayed down for two full days, blocking developer work across dozens of engineering teams. Production Federated API Server (the primary entry point for all platform clients) was operating well below 90% availability. The root causes were compounding: APF (API Priority and Fairness) was misconfigured, allowing client bursts to starve critical traffic; etcd governance was absent, allowing unbounded growth; alert coverage was patchy; and there was no structured incident process — every outage was handled ad hoc by whoever happened to be available. The team had no SLO/SLI framework, no error budget policy, no runbooks, and no on-call rotation.

## Task

Design and implement SRE practices from scratch for the Kubernetes API server fleet: define SLI/SLO targets that were technically grounded and stakeholder-aligned, establish an error budget policy to govern reliability vs. velocity tradeoffs, build an incident management process with proper runbooks and escalation paths, stand up a 24/7 on-call rotation, and systematically reduce toil through AI-augmented triage tooling.

## Action

**SLI/SLO Design:**
- Chose availability and latency as the primary SLIs — API server is a control plane consumed by platform clients, so request success rate and response time are what clients actually care about.
- Deliberately set the initial SLO at 99% (not 99.9%) for the Federated API Server: starting aggressive from a broken baseline would have burned error budget immediately and demoralized the team; 99% gave room to improve infrastructure while tracking meaningful progress.
- Prioritized Federated API Server first (highest blast radius), then progressively added cluster-level and environment-specific SLOs for Dev, Staging, and Production.
- Leveraged Kubernetes built-in Prometheus metrics as the SLI signal source — minimal instrumentation overhead since the metrics already existed.

**Error Budget Policy:**
- Started with a 95% target threshold before error budget exhaustion triggered action — again, deliberately conservative at first to gather baseline data without constant false alarms.
- Ran daily error budget reviews during the first months: when burn rate spiked, triage focused on whether the cause was a release, a configuration change, or a specific client's APF configuration.
- Used burn rate signal to drive prioritization: high burn from a specific client → escalate APF tuning for that client; high burn from a release → require staging validation before next prod push.
- Graduated the SLO target from 99% → 99.9% for production as infrastructure stabilized and the team developed confidence in the measurement methodology.

**Incident Management Process:**
- Built a multi-level alert hierarchy: primary SLO/SLI alerts (availability drop, latency spike) as the pager trigger; secondary alerts on API server instance health, etcd size, etcd compaction failures, and APF queue depth.
- Wrote runbooks for every alert: triage steps, mitigation actions, escalation criteria — engineers on call had a defined SOP for the most common failure modes rather than debugging from first principles.
- Established 24/7 PagerDuty on-call coverage with explicit escalation path: on-call engineer → tech lead → engineering manager.
- Specific incidents that drove alert additions: APF misconfiguration allowing one client to starve others (→ per-client APF alert), etcd unbounded growth causing compaction delays (→ etcd size alert with automated compaction trigger).

**Blameless Postmortem Culture:**
- Introduced a standardized RCA template focused on: timeline of events, MTTD, MTTR, root cause (technical, not personal), why the issue wasn't caught earlier, how to prevent recurrence.
- Centralized all RCAs in a shared knowledge base — searchable by incident type, enabling pattern detection across incidents over time.
- Every RCA produced follow-up action items with named owners and due dates; tracked in sprint backlog alongside feature work, not a separate "postmortem board" that never got reviewed.
- Explicitly framed postmortems as learning exercises, not accountability hearings; recognized engineers who wrote thorough RCAs, not just engineers who fixed the immediate issue.

**On-Call Rotation Design:**
- Initial design: follow-the-sun with US team covering US business hours and China team covering China/Asia hours (~12h each), providing near-24/7 coverage without requiring night shifts.
- When China team lost production environment access (compliance constraint), redesigned rotation: US team as primary, India/Europe team as secondary — covering the gap while the India/Europe team ramped up to production access.
- Long-term plan: evolve back toward follow-the-sun as India/Europe team gained production readiness.
- Escalation path kept consistent regardless of rotation: on-call → tech lead → EM.

**AI-Augmented Toil Reduction:**
- Identified the dominant toil category: triage of bad instance and release-induced API server degradation — recurring, time-consuming, required reading metrics and logs across multiple systems simultaneously.
- Built an AI triage agent using MCP (Model Context Protocol) servers to collect API server metrics, etcd metrics, and error logs automatically on incident trigger.
- AI agent synthesized cross-system signals and produced a structured triage summary: likely root cause, affected clients, recommended mitigation steps — reducing the on-call engineer's triage time from 30–60 minutes to under 10 minutes for common incident classes.
- Maintained human approval for all mitigation actions; AI handled information gathering and synthesis, not execution.

## Result

- Federated API Server availability improved from below 90% to a 30-day rolling average of 99% (Dev environments); Production reached 99.9% sustained.
- Dev API Server sustained outages (the 2-day incident) eliminated — runbooks and alerts caught degradation before it escalated to full unavailability.
- MTTD reduced significantly: multi-level alerts and AI triage cut detection-to-triage time from hours to ~20 minutes.
- MTTR reduced: structured runbooks and AI-assisted triage cut mitigation time from 24+ hours (worst case) to under 1 hour for defined incident classes.
- Blameless postmortem process produced a growing knowledge base of RCAs with closed follow-up actions — team shifted from ad hoc firefighting to systematic pattern elimination.
- On-call burnout risk reduced: follow-the-sun design distributed load geographically; runbooks and AI triage reduced cognitive burden per incident.
- Incident frequency dropped from multiple per week to rare occurrences as preventive controls from RCA action items were implemented.

## Related Skills

- [[skills/tech/infra/SRE Practices and SLO Engineering]]
- [[skills/tech/infra/Observability and Incident Management]]
- [[skills/tech/infra/Kubernetes]]
- [[skills/management/people/Engineering Team Management]]

## Interview Usage

- 适用 BQ：Tell me about a time you built SRE/reliability practices from scratch
- 适用 BQ：How do you design SLOs when the baseline reliability is very poor?
- 适用 BQ：Describe a time you built a blameless culture around incidents
- 适用 BQ：Tell me about a time you reduced on-call toil using tooling or automation
- 适用 Technical：How would you define SLIs/SLOs for a Kubernetes API server?
- 适用 Technical：How do you use AI to augment incident response without introducing risk?
- 适用 JD 关键词：SRE, SLO, SLI, error budget, incident management, on-call, blameless postmortem, toil reduction, observability, reliability engineering

## Key Questions

**Q: How do you set SLO targets when your baseline reliability is already very poor?**
Talking points: Don't set an aspirational target — set a target that's above current performance but achievable within months; the goal is to make progress measurable, not to declare a false standard. For API server at <90%, starting at 99% gave a meaningful gap to close without burning error budget immediately. Graduated: 99% → 99.9% as infrastructure stabilized. Explain why 99.9% from day one would have been counterproductive.

**Q: Walk me through how you designed the error budget policy. How did you use it operationally?**
Talking points: Error budget is a shared contract — it converts a reliability debate into a math problem. Daily burn rate review in early months to calibrate; burn rate spike → root cause analysis (release? client? infra?); burn rate determined the mitigation priority (APF tuning for a bad client, staging gate for a release). Started conservative (95% threshold) to avoid constant false exhaustion signals; tightened as the team learned the system's behavior.

**Q: How do you build a blameless postmortem culture when engineers are used to being blamed for incidents?**
Talking points: Template the process (timeline, MTTD, MTTR, root cause, prevention) so it's structured, not a freeform interrogation. Centralize RCAs so the organization learns across incidents — the knowledge base becomes visible value. Track follow-up actions in the sprint backlog alongside feature work, not a separate queue that decays. Explicitly recognize thorough RCA authors. Over time, the culture shifts when engineers see that postmortems produce improvements, not punishments.

**Q: How do you design on-call rotations for a global team with uneven production access?**
Talking points: Start with the constraint (China team lost prod access — compliance, not performance). Follow-the-sun was the ideal state; primary/secondary was the pragmatic bridge. India/Europe as secondary during ramp-up gives them real incident exposure without sole responsibility. Plan the transition explicitly — what milestones enable India/Europe to go primary? Don't leave the interim state permanent by default.

**Q: How did you use AI in incident response without introducing new risk?**
Talking points: AI handled information gathering and synthesis (pulling metrics, logs, cross-system correlation) — the tasks where speed matters and human bottleneck is worst. Human approval gate on all mitigation actions — AI never executed changes autonomously. Result: on-call engineer gets a structured triage summary in <10 minutes instead of manually querying 4-5 systems. The design principle: AI augments the engineer's decision-making speed, doesn't replace their judgment.

## Summary

Building SRE practices for eBay's Kubernetes API server fleet meant starting from near-zero — no SLOs, no runbooks, no on-call rotation, no postmortem process — while simultaneously dealing with an active reliability crisis. The most consequential design choices were deliberately conservative: starting the SLO at 99% rather than 99.9% gave the team room to improve without constant error budget exhaustion, and starting the error budget threshold at 95% gave time to understand the system's behavior before tightening the policy. This graduated approach is counterintuitive when leadership wants to show ambition, but it's technically grounded — an SLO you can't sustain is worse than no SLO, because it teaches engineers to ignore the signal.

The incident management work had two components that compounded each other: the process (runbooks, PagerDuty hierarchy, blameless postmortems, centralized RCA knowledge base) reduced the cognitive and organizational cost per incident; and the AI-augmented triage agent (MCP servers collecting metrics and logs, AI synthesizing triage summaries) reduced the time-to-diagnosis for common failure classes from 30-60 minutes to under 10. Together these brought MTTD to ~20 minutes and MTTR to under 1 hour for defined incident classes, and the cumulative effect of postmortem follow-up actions eliminated entire incident categories over time. The on-call rotation evolved from follow-the-sun to primary/secondary when a compliance constraint removed China team's production access — a reminder that on-call design is never purely technical; organizational and regulatory constraints shape what's actually feasible.

## Raw Material
- [[raw_material/tech/infra/SRE Practices and SLO Engineering - personal]]
