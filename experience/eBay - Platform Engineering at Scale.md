---
title: eBay - Platform Engineering at Scale
type: experience
skills: [kubernetes, k8s, platform-engineering, cloud-infrastructure, system-design, devops, sre, abstraction, crd, admission-webhooks]
company: eBay
date: 2020-01
impact: high
growing_link:
source_blog: https://austinxyz.github.io/blogs/blog/2026/03/16/platform-engineer-vs-ops-engineer
---

# eBay - Platform Engineering at Scale

## Situation

eBay's Kubernetes platform had grown to 200+ clusters, 5,000+ applications, 500,000 nodes, and 2M instances. Annual operational demands included two major Kubernetes version upgrades, adding ~33% more clusters each year, onboarding hundreds of new applications, and monthly OS security patching. With this scale, a traditional ops approach — scripting node-by-node upgrades, writing per-customer runbooks, manually coordinating rollouts — was no longer sustainable. Every new requirement meant rewriting automation; every incident meant heroic intervention by a small number of people with irreplaceable context.

## Task

Shift the team's operating model from ops thinking ("fix this problem") to platform thinking ("eliminate this class of problem") — building systems that multiplied engineer leverage rather than requiring constant human heroics. The goal: two engineers should be able to maintain the entire fleet operation with zero incidents.

## Action

- **Declarative upgrade model**: Instead of scripting node-by-node upgrades, modeled OS and K8s upgrades as declarative desired state using Kubernetes CRDs and Controllers — engineers specify requirements, the platform enforces policies automatically
- **Standardized patch specs**: Formalized customer modification requirements into structured specifications, enabling audit trails and AI-assisted generation of upgrade PRs at scale
- **Self-service validation**: Built a validation platform so teams could test their own upgrade compatibility without waiting in a central queue
- **Deployment automation**: Implemented configurable upgrade strategies with staged rollouts and automatic rollback gates — correctness embedded in technical constraints, not runbooks
- **Admission webhooks**: Used admission webhooks and policies-as-code to enforce guardrails that cannot be skipped, replacing human review steps that could
- **Extended Kubernetes**: Built Custom Resource Definitions and custom controllers for eBay-specific lifecycle features: multi-cluster deployment, dependency-aware rolling upgrades, canary releases based on metrics
- **Eliminated heroism**: Systematically identified single points of failure (the engineer called at 2am) and made those capabilities self-service and systematized

## Result

- Two engineers maintained 200+ clusters, 5,000+ applications, 2M instances with zero incidents
- Eliminated the need to rewrite automation for each new upgrade or customer context
- Onboarded hundreds of applications per year through self-service platform, not manual coordination
- Monthly OS patching and bi-annual K8s upgrades became routine, non-incident operations
- Platform model adopted as eBay's standard for cloud lifecycle management

## Related Skills
- [[skills/tech/infra/Kubernetes]]
- [[skills/tech/system-design/Distributed Systems]]
- [[skills/management/project/Technical Roadmap]]

## Interview Usage
- 适用 BQ：Tell me about a time you scaled an infrastructure system beyond what manual processes could handle
- 适用 BQ：Tell me about a time you changed your team's operating model or philosophy
- 适用 BQ：Tell me about a time you reduced operational toil through platform thinking
- 适用 Technical：How would you design an upgrade system for a 200+ cluster Kubernetes fleet?
- 适用 JD 关键词：Kubernetes, platform engineering, CRD, admission webhooks, large-scale infra, SRE, operational excellence, self-service, automation
