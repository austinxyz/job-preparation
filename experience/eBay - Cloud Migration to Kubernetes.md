---
title: eBay - Cloud Migration to Kubernetes
type: experience
skills: [cloud-migration, kubernetes, ci-cd, cross-team-collaboration, distributed-systems, engineering-management]
company: eBay
date: 2025-01
impact: high
growing_link:
---

# eBay - Cloud Migration to Kubernetes

## Situation

eBay's cloud platform was built on VMs with a home-grown CI/CD system that was showing its age: performance bottlenecks and slow recovery times were degrading developer productivity and site reliability. The platform team had committed to migrating all 5,000 applications to a container/Kubernetes-based cloud-native architecture — a two-phase migration (assimilation then cloud-native) spanning Java services, Node.js frontends, messaging systems, and batch jobs. Applications supported multiple traffic topologies: private, public L4, public L7, and POP. The migration had to complete within one year without service disruptions and without requiring new hardware that only the cloud-native stack supported.

## Task

As engineering manager, I led a cross-functional team of 10+ engineers across US and China offices to deliver the migration tooling and execute the rollout. My responsibilities included defining ownership between global teams, building automated tooling for each application type and traffic topology, coordinating with platform, network, and security teams, and ensuring the one-year timeline held without incidents.

## Action

- Defined clear ownership split between teams: US team owned orchestration (the "Application Instance Migration" workflow); China team owned hardware LB-to-software LB configuration conversion, with a minimal interface contract between the two
- Created a unified migration blueprint documenting the five-phase migration flow per application — preparation, workload creation, traffic switching, baking period, and decommission — with rollback capability at each phase
- Implemented comprehensive end-to-end test cases covering all application types and topologies; used automated test execution to validate each new feature release before rollout
- Built a migration dashboard tracking per-application progress across all 5,000 applications; designed batching strategy — pilot applications first, then scaling by application type and topology
- Set up multi-channel coordination: regular US–China sync meetings, on-demand Slack channels, and formal design review processes for architectural decisions
- Worked with PM and tech lead to translate requirements into designs, scope features into phases, and secure resources

## Result

- Migrated all 5,000 applications to cloud-native Kubernetes within the one-year timeline, with no service disruptions
- Deployment duration reduced by 75% — large application pools dropped from 4 hours to under 60 minutes
- Site reliability improved significantly: container remediation and auto-scaling reduced critical incidents
- Application teams reported strong productivity improvement; eBay framework team praised the cloud-native feature enablement
- Project became a blueprint for large-scale infrastructure migration at eBay

## Related Skills

- [[skills/tech/infra/Kubernetes]]
- [[skills/tech/infra/Container Basics]]
- [[skills/management/people/Engineering Team Management]]
- [[skills/management/project/Technical Roadmap]]
- [[skills/tech/system-design/Distributed Systems]]

## Interview Usage

- 适用 BQ：Describe a time when communication and collaboration were pivotal to achieving a team goal
- 适用 BQ：Tell me about a large-scale technical migration you led — how did you manage risk?
- 适用 BQ：How do you coordinate global teams (US + China) on a shared technical deliverable?
- 适用 BQ：Give an example of a project you delivered on time under significant complexity and scope
- 适用 JD 关键词：cloud migration, Kubernetes, CI/CD, cross-functional leadership, global teams, risk mitigation, rollback strategy, developer productivity, site reliability

## Key Questions

**Q: How do you manage a one-year, 5,000-application migration without disrupting production?**
Talking points: Phase by risk (pilot first, then scale by type); build rollback into each phase, not just at the end; build a visibility layer (dashboard) early so the team and stakeholders can track at a glance; use automated E2E tests to validate every feature release before widening rollout.

**Q: How did you coordinate two geographically distributed engineering teams on a complex shared deliverable?**
Talking points: Define ownership at the interface level (not the component level); design a minimal, explicit contract between the two teams; establish regular structured touchpoints AND ad-hoc channels for unblocking; keep the design doc (BP) as the single source of truth.

**Q: How do you de-risk a migration that must complete with zero downtime across thousands of applications?**
Talking points: Five-phase migration with rollback at each gate; don't switch traffic before a baking period; pilot on low-criticality applications and broaden only after validation; separate the orchestration concern from the configuration conversion concern to contain blast radius.

**Q: How do you maintain team alignment across PM, tech lead, and engineers through a year-long program?**
Talking points: Translate requirements into concrete designs early; maintain a migration blueprint everyone works from; build multiple communication channels for different latency needs (sync meetings for alignment, Slack for unblocking, design reviews for decisions).

## Summary

Migrating eBay's 5,000 applications from a VM-based home-grown CI/CD stack to cloud-native Kubernetes was one of the highest-impact infrastructure programs I led. The technical challenge was significant — multiple application stacks, traffic topologies, and a hard one-year deadline — but the organizational challenge was equally complex: coordinating a 10+ person team across US and China, plus handoffs with platform, network, and security teams, while keeping every application team's operations uninterrupted.

The key architectural decision that made the migration tractable was defining a strict five-phase workflow per application with rollback built into each gate, and separating the orchestration concern (US team) from the LB configuration conversion concern (China team) with a minimal interface contract. This division let both teams move in parallel without constant coordination overhead. The result — 5,000 applications migrated on time, 75% reduction in deployment duration, and measurable reliability improvements — validated both the technical design and the organizational approach, and became a reference model for how eBay approaches large-scale platform transitions.

## Raw Material
- [[raw_material/experience/Cloud Migration Success]]
