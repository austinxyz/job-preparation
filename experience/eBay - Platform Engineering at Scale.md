---
title: eBay - Platform Engineering at Scale
type: experience
skills: [kubernetes, k8s, platform-engineering, cloud-infrastructure, system-design, devops, sre, abstraction, crd, admission-webhooks]
company: eBay
date: 2025-01
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

## Key Questions

**Q: Tell me about a time you fundamentally changed how your team operated at scale.**
Talking points: Name the inflection point (manual ops couldn't keep up with 200+ clusters); articulate the shift in mental model (ops thinking vs. platform thinking); describe the concrete mechanisms built (CRDs, controllers, admission webhooks, declarative upgrades); show the outcome (2 engineers, zero incidents, monthly patching as routine).

**Q: How do you design systems that eliminate entire classes of operational problems?**
Talking points: Identify the recurring pattern to eliminate (rewriting automation per upgrade, heroic incident response); encode correctness as technical constraint rather than runbook discipline (admission webhooks, declarative desired state); measure not just incidents but the absence of the pattern — e.g., no more rewriting.

**Q: How would you approach Kubernetes fleet management at 200+ cluster scale?**
Talking points: Declarative upgrade model with CRDs/controllers; standardized patch specs for customer modifications; self-service validation so teams don't queue on a central team; staged rollout with automatic rollback gates; admission webhooks for non-bypassable guardrails.

**Q: Tell me about a time you eliminated single points of failure in your team's operations.**
Talking points: Name the SPOF explicitly (the engineer who gets called at 2am — only they know how); systematize the capability by making it self-service and documented; measure whether the person-dependency actually went away (can the team operate without that person for a week?).

## Summary

eBay's Kubernetes platform reached a scale — 200+ clusters, 5,000+ applications, 2M instances — where the existing ops model was a ceiling, not a floor. Two major K8s upgrades per year, monthly OS patching, hundreds of new app onboardings annually: doing these by hand was creating an exponentially growing maintenance burden and a fragile dependency on a small number of people with irreplaceable tribal knowledge.

The shift from ops thinking to platform thinking meant reframing the goal: not "fix this upgrade problem" but "make upgrade problems impossible to create." The mechanism was declarative desired state — engineers specify what they need, the platform enforces it automatically via CRDs, controllers, and admission webhooks. The result was two engineers maintaining the entire fleet with zero incidents, and monthly patching becoming a non-event. This story is strongest for technical depth questions about Kubernetes at scale, and for leadership questions about changing team operating philosophy rather than just optimizing the existing one.

## Raw Material
- source_blog: https://austinxyz.github.io/blogs/blog/2026/03/16/platform-engineer-vs-ops-engineer
