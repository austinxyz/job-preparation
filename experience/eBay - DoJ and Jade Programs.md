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
