---
title: eBay - Cloud Migration to Kubernetes
type: Additional
signal_areas: [Scope, Ownership, Leadership]
skills: [cloud-migration, kubernetes, ci-cd, cross-team-collaboration, distributed-systems, engineering-management]
company: eBay
date: 2025-01
impact: high
growing_link:
---

# eBay - Cloud Migration to Kubernetes

## Context

eBay's cloud platform was built on VMs with a home-grown CI/CD system that was showing its age: performance bottlenecks and slow recovery times were degrading developer productivity and site reliability. The platform team committed to migrating all 5,000 applications to a container/Kubernetes-based cloud-native architecture — a two-phase migration (assimilation then cloud-native) spanning Java services, Node.js frontends, messaging systems, and batch jobs across multiple traffic topologies (private, public L4, public L7, and POP). The migration had to complete within one year without service disruptions and without requiring new hardware that only the cloud-native stack supported.

## Actions

- I proposed the ownership split between the US and China teams — US team owned orchestration (the "Application Instance Migration" workflow); China team owned hardware LB-to-software LB configuration conversion — and got buy-in from the China team on the structure. A minimal interface contract between the two let both move in parallel without constant coordination overhead.
- I worked with the PM and tech lead to translate requirements into designs, scope features into delivery phases, and secure the resources needed to staff both teams for the full program duration.
- I directed the team to build a unified migration blueprint documenting the five-phase migration flow per application — preparation, workload creation, traffic switching, baking period, and decommission — with rollback capability built into each phase gate, not just at the end.
- The batching strategy — pilot applications first, then scale by application type and topology — was driven by the team and PM; I aligned on the approach and ensured it was reflected in the overall sequencing plan.
- I set up multi-channel coordination across the global team: regular US–China sync meetings for alignment, on-demand Slack channels for unblocking, and formal design review processes for architectural decisions — matching the communication channel to the decision latency required.
- The team implemented comprehensive end-to-end test cases covering all application types and traffic topologies, and built a migration dashboard tracking per-application progress across all 5,000 applications — both of which I directed and reviewed.

## Results

- All 5,000 applications migrated to cloud-native Kubernetes within the one-year timeline, with no major service disruptions.
- Deployment duration reduced by 75% — large application pools dropped from 4 hours to under 60 minutes.
- Site reliability improved materially: container remediation and auto-scaling reduced critical incidents.
- Application teams reported strong productivity improvements; eBay's framework team credited the cloud-native feature enablement.
- The migration approach became eBay's reference model for large-scale platform transitions.

## Learnings

- The US/China ownership split worked because it was defined at the interface level, not the component level. Both teams had a clear, bounded scope with a minimal contract between them — that's what allowed parallel execution without constant coordination overhead. Vague ownership across global teams generates hand-off failures; explicit interface contracts generate independence.
- Building rollback into each of the five phase gates, rather than only at the end, was what made the migration low-risk despite the scale. Each gate was a real decision point, not a formality — application teams trusted the process because the exit was always available.
- The batching strategy (pilot first, then scale by type) front-loaded the validation cost. The pilot applications found the issues; the scaled rollout was fast because the tooling had already been stress-tested. It's tempting to go faster earlier — I'd resist that next time too.

## Signal Areas

**Primary:** Scope (5,000 applications, 10+ engineers across US and China, one-year hard deadline, multiple application stacks and traffic topologies, full end-to-end delivery accountability), Ownership (accountable for team structure, technical blueprint, delivery sequencing, and outcomes — not just the engineering work but the program-level result)

**Secondary:** Leadership (US/China ownership design, multi-channel coordination model, cross-functional alignment with platform, network, and security teams throughout a year-long program)

## Related Skills
- [[skills/tech/infra/Kubernetes]]
- [[skills/tech/infra/Container Basics]]
- [[skills/management/people/Engineering Team Management]]
- [[skills/management/project/Technical Roadmap]]
- [[skills/tech/system-design/Distributed Systems]]

## Interview Usage
- 适用 BQ：Tell me about a large-scale technical migration you led — how did you manage risk?
- 适用 BQ：How do you coordinate global teams (US + China) on a shared technical deliverable?
- 适用 BQ：Give an example of a project you delivered on time under significant complexity and scope
- 适用 BQ：Describe a time when communication and collaboration were pivotal to achieving a team goal
- 适用 JD 关键词：cloud migration, Kubernetes, CI/CD, cross-functional leadership, global teams, risk mitigation, rollback strategy, developer productivity, site reliability

## Key Questions

**Q: How do you manage a one-year, 5,000-application migration without disrupting production?**
Talking points: Phase by risk — pilot first, then scale by application type and topology. Build rollback into each phase gate, not just at the end; every gate is a real decision point. Build a visibility layer (dashboard) early so the team and stakeholders can track at a glance. Use automated E2E tests to validate each feature release before widening rollout.

**Q: How did you coordinate two geographically distributed engineering teams on a complex shared deliverable?**
Talking points: Define ownership at the interface level, not the component level. Minimal, explicit contract between the two teams — US owns orchestration, China owns LB configuration conversion. Match communication channels to decision latency: sync meetings for alignment, Slack for unblocking, formal design reviews for architectural decisions. Keep the migration blueprint as the single source of truth everyone works from.

**Q: How do you de-risk a migration that must complete with zero downtime across thousands of applications?**
Talking points: Five-phase migration with rollback at each gate. Don't switch traffic before a baking period. Pilot on a controlled set first; broaden only after validation. Separate the orchestration concern from the configuration conversion concern to contain blast radius if something goes wrong in one layer.

**Q: How do you maintain alignment across PM, tech lead, and engineers through a year-long program?**
Talking points: Translate requirements into concrete designs early so the team isn't guessing. Maintain a single migration blueprint everyone works from. Build multiple communication channels for different latency needs. Make phase sequencing explicit — everyone should know what's in scope now and what's deferred to which phase.

## Summary

Migrating eBay's 5,000 applications from a VM-based CI/CD stack to cloud-native Kubernetes was one of the highest-scope infrastructure programs I led. The technical challenge was real — multiple application stacks, traffic topologies, a hard one-year deadline — but the organizational challenge was equally complex: a 10+ person team across US and China, plus coordination with platform, network, and security teams, while keeping every application team's operations uninterrupted throughout.

The decision that made the migration tractable was defining the ownership split at the interface level (US team: orchestration; China team: LB configuration conversion) with a minimal contract between them, and building a five-phase workflow with rollback built into each gate. This let both teams move in parallel, made the risk profile predictable, and gave application teams a credible safety mechanism. The result — 5,000 applications migrated on time with no major service disruptions, 75% reduction in deployment duration, measurable reliability improvements — validated both the technical design and the organizational approach, and became eBay's reference model for large-scale platform transitions.

## Raw Material
- [[raw_material/experience/Cloud Migration Success]]
