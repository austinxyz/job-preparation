---
title: eBay - Platform Engineering at Scale
type: Additional
signal_areas: [Scope, Ownership, Leadership, Growth]
skills: [kubernetes, k8s, platform-engineering, cloud-infrastructure, system-design, devops, sre, abstraction, crd, admission-webhooks]
company: eBay
date: 2025-01
impact: high
growing_link:
source_blog: https://austinxyz.github.io/blogs/blog/2026/03/16/platform-engineer-vs-ops-engineer
---

# eBay - Platform Engineering at Scale

## Context

eBay's Kubernetes platform had grown to 200+ clusters, 5,000+ applications, 50,000 nodes, and 2M instances. Every year the operational demands compounded: two major Kubernetes version upgrades, adding roughly 33% more clusters, onboarding hundreds of new applications, and monthly OS security patching. The team was handling this through a traditional ops model — scripting node-by-node upgrades, writing per-customer runbooks, manually coordinating rollouts. At that scale, the model had become a ceiling: every new requirement meant rewriting automation, every incident meant heroic intervention by a small number of people with irreplaceable context. I recognized that continuing to optimize the existing approach would never get us to sustainability — we needed to change the model entirely.

## Actions

- When I took ownership of the team, the operating philosophy of "eliminate this class of problem rather than fix this problem" was already a shared direction — I made it explicit and used it as the standing filter for every solution proposal: does this fix the incident, or does it make the incident impossible to create? Naming it consistently helped the team apply it independently to new problems.
- I led the team to enhance our existing OS upgrade system by moving to a declarative model using Kubernetes CRDs and controllers — instead of scripting node-by-node upgrades, engineers specify desired state and the platform enforces it automatically. The key shift was building on what existed rather than rewriting from scratch, and extending the model to handle the growing variety of cluster configurations.
- I led the team to formalize customer modification requirements into structured patch specifications, enabling audit trails and AI-assisted generation of upgrade PRs at scale — so the manual work of understanding per-customer requirements was systematized rather than carried in individual engineers' heads.
- One of our team leads identified the need for a self-service validation platform so application teams could test their own upgrade compatibility without queuing on a central team. I supported the initiative, provided the resources to build it, and made sure it was prioritized — removing a bottleneck that had been invisible but was slowing onboarding at scale.
- I pushed the team to implement admission webhooks and policies-as-code to enforce guardrails that cannot be bypassed, replacing human review steps. The key principle: correctness embedded in technical constraints is more reliable than correctness enforced by process.
- I systematically identified single points of failure — specifically, the engineers who got called at 2am because only they knew how a particular system worked — and drove the team to make those capabilities self-service and documented, so no single person's absence created an incident risk.

## Results

- Bi-annual Kubernetes version upgrades completed without incident across 200+ clusters — upgrades that previously required heroic coordination became routine, planned operations.
- Monthly OS patching sustained without disruption across the fleet.
- Hundreds of applications onboarded per year through the self-service validation platform, with no central coordination required.
- The upgrade automation no longer needed to be rewritten for each new cycle or customer configuration — the declarative model handled new contexts automatically.
- The platform model was adopted as eBay's standard for cloud lifecycle management.

## Learnings

- The shift from ops thinking to platform thinking was primarily a cultural change, not a technical one. The CRDs and controllers were the mechanism, but convincing engineers to reframe how they thought about problems was the harder work. I should have been more explicit about this distinction earlier — naming the mental model shift helped the team apply it to new problems without me needing to redirect each one.
- Self-service only works if the experience is genuinely better than asking a human. Every feature of the validation platform needed to clear that bar — if it was faster to Slack someone than to use the tool, nobody would use the tool. I should have been more rigorous about measuring adoption, not just delivery.
- The "eliminate heroism" effort surfaced how much implicit knowledge was concentrated in a small number of people. That concentration was invisible until we looked for it. In future teams I'd run an explicit "bus factor" audit early rather than discovering it through incidents.

## Signal Areas

**Primary:** Scope (org-wide impact, 200+ clusters, 2M instances, multi-year investment), Ownership (identified the problem and drove the model change — not just the technical delivery but the philosophy shift)

**Secondary:** Leadership (changed the team's operating model and mental framework; pattern adopted org-wide), Growth (ops thinking → platform thinking is a fundamental reframe; "eliminate heroism" as a systematic practice rather than a reactive response)

## Related Skills
- [[skills/tech/infra/Kubernetes]]
- [[skills/tech/system-design/Distributed Systems]]
- [[skills/management/project/Technical Roadmap]]

## Interview Usage
- 适用 BQ：Tell me about a time you scaled an infrastructure system beyond what manual processes could handle
- 适用 BQ：Tell me about a time you fundamentally changed your team's operating model
- 适用 BQ：Tell me about a time you reduced operational toil through platform thinking
- 适用 Technical：How would you design an upgrade system for a 200+ cluster Kubernetes fleet?
- 适用 JD 关键词：platform engineering, Kubernetes, CRD, admission webhooks, large-scale infra, SRE, operational excellence, self-service, automation

## Key Questions

**Q: Tell me about a time you fundamentally changed how your team operated at scale.**
Talking points: Name the inflection point — manual ops couldn't keep up with 200+ clusters growing at 33%/year. Articulate the shift in mental model: ops thinking (fix this problem) vs. platform thinking (eliminate this class of problem). Describe the concrete mechanisms — CRDs, controllers, admission webhooks, declarative upgrade model. Show the outcome: K8s upgrades and monthly patching became routine non-incident operations, self-service onboarding without central coordination.

**Q: How do you design systems that eliminate entire classes of operational problems?**
Talking points: Identify the recurring pattern to eliminate (rewriting automation per upgrade, heroic incident response). Encode correctness as technical constraint rather than process discipline — admission webhooks instead of review steps, declarative state instead of scripts. Measure not just incidents but the absence of the pattern — no more rewriting, no more 2am calls to that one engineer.

**Q: How would you approach Kubernetes fleet management at 200+ cluster scale?**
Talking points: Declarative upgrade model with CRDs and controllers so engineers specify requirements, not procedures. Standardized patch specs for customer modifications — structured, auditable, AI-generatable. Self-service validation so teams don't queue on a central team. Staged rollout with automatic rollback gates. Admission webhooks for non-bypassable guardrails.

**Q: Tell me about a time you eliminated single points of failure in your team's operations.**
Talking points: Name the SPOF explicitly — the engineer called at 2am because only they knew how a system worked. Systematize the capability through documentation and self-service tooling. Measure whether the dependency actually went away: can the team operate without that person for a week? The goal isn't documentation for its own sake — it's making the knowledge institutional rather than individual.

## Summary

eBay's Kubernetes platform reached a scale — 200+ clusters, 5,000+ applications, 2M instances — where the traditional ops model had become a hard ceiling. Every new upgrade cycle meant rewriting automation; every incident meant heroic intervention by people with irreplaceable context. The sustainable path wasn't to hire more ops engineers — it was to change the model.

The shift from ops thinking to platform thinking meant reframing the goal: not "fix this upgrade problem" but "make upgrade problems impossible to create." The mechanisms were declarative desired state via CRDs and controllers, self-service validation, and admission webhooks that embedded correctness as technical constraints rather than process discipline. The result was bi-annual Kubernetes upgrades and monthly patching becoming routine non-incident operations, and hundreds of applications onboarding per year through self-service with no central coordination. The more durable outcome was a team that applied the same mental model to new problems independently — which is what made the change sustainable.

## Raw Material
- source_blog: https://austinxyz.github.io/blogs/blog/2026/03/16/platform-engineer-vs-ops-engineer
