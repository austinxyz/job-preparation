---
title: eBay - DoJ and Jade Programs
type: experience
skills: [cross-functional-leadership, kubernetes, k8s, cloud-infrastructure, platform-engineering, incident-management, compliance, automation, devops]
company: eBay
date: 2025-06
impact: high
growing_link:
---

# eBay - DoJ and Jade Programs

## Situation

eBay was required to prevent covered persons from accessing PII data in staging and production environments to comply with a DoJ policy. Non-compliance carried significant legal and financial risk.

## Task

As the Cloud Fleet team lead, I was responsible for three critical workstreams:
- Build two new cloud environments from scratch: SDDZ (isolated dev environment for covered persons) and DCPX (a transition layer for data sanitization between the isolated and production environments)
- Transfer ownership of thousands of cloud namespaces and apps away from covered persons
- Maintain business continuity for existing infrastructure functions — including host runtime, OS patching, cloud console, and namespace/app RBAC management

## Action

- Coordinated a cross-team war room with daily syncs; created a comprehensive runbook covering all steps, owners, and dependency graphs
- Ran multiple rehearsal rounds to de-risk the final cutover
- Drove a three-track execution across Technical, Process, and People dimensions:
  - **Technical:** Automated AZ/cluster provisioning and ownership transfer at scale; used data-driven analysis to prioritize efforts; leveraged AI to rapidly build dashboards and visualize progress reports
  - **Process:** Streamlined on-call workflows to reduce pager volume
  - **People:** Traveled on-site for knowledge transfer; drove targeted hiring to backfill covered-person capacity

## Result

- Stood up SDDZ and DCPX AZ/clusters within 2 weeks
- Automatically transferred thousands of cloud namespaces and apps with zero customer intervention
- Completed cutover on schedule; US team absorbed additional infrastructure components with no critical incidents

## Related Skills
- [[skills/tech/infra/Kubernetes]]
- [[skills/management/project/Technical Roadmap]]
- [[skills/management/people/Engineering Team Management]]

## Interview Usage
- 适用 BQ：Tell me about a time you drove a high-stakes, cross-functional technical project under tight deadline
- 适用 BQ：Tell me about a time you had to coordinate multiple teams to deliver a critical initiative
- 适用 JD 关键词：cross-functional leadership, compliance, cloud infrastructure, incident management, Kubernetes

## Key Questions

**Q: How do you manage a critical, externally-imposed deadline with multiple workstreams in flight?**
Talking points: Establish a war room with daily syncs and a single source of truth runbook; decompose into parallel tracks (Technical / Process / People); use rehearsal rounds to surface risk early; own the dependency graph, not just your track.

**Q: Tell me about a time you led a project with significant legal or compliance stakes.**
Talking points: Name the constraint and the business risk (DoJ policy, PII access, legal/financial exposure); describe how you balanced speed with correctness (runbooks, rehearsals, data-driven prioritization); show you delivered on time with zero critical incidents.

**Q: How do you maintain business continuity while executing a large infrastructure migration?**
Talking points: Identify the live surfaces that cannot go down (host runtime, OS patching, RBAC); build parallel execution so migration doesn't block ongoing operations; automate bulk transfers (namespace/app ownership) to avoid human bottlenecks; validate before cutover.

**Q: How do you drive execution across teams you don't directly manage?**
Talking points: Create shared artifacts everyone depends on (runbook, dependency graph); make blockers visible in daily syncs; assign owners per track so no one waits on a single decision-maker; travel on-site for high-complexity knowledge transfer when remote isn't enough.

## Summary

The DoJ and Jade programs were eBay's response to a government compliance mandate requiring covered persons to be fully removed from access to PII data, staging, and production environments. As Cloud Fleet team lead, I was responsible for standing up two new cloud environments from scratch, transferring ownership of thousands of namespaces and apps, and keeping all existing infrastructure functions running without disruption — simultaneously.

The execution challenge was less technical than organizational: multiple workstreams, tight deadlines, and a zero-tolerance outcome (no critical incidents, no schedule slip). I ran it like an incident response at project scale — daily war room, comprehensive runbook with owners and dependency graphs, multiple rehearsal rounds before the live cutover. The result was delivery on schedule with no customer-visible incidents, and the US team successfully absorbed expanded infrastructure scope. This story is strongest for questions about high-stakes delivery, compliance-driven projects, and cross-functional coordination under pressure.

## Raw Material
<!-- No raw_material/ source file — story reconstructed from direct experience -->
