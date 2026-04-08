---
title: eBay - Engineering Velocity Program
type: experience
skills: [engineering-velocity, ci-cd, cross-team-leadership, dora-metrics, security-policy, stakeholder-alignment, conflict-resolution]
company: eBay
date: 2024-01
impact: high
growing_link:
---

# eBay - Engineering Velocity Program

## Situation

eBay launched a company-wide engineering velocity program to address a serious developer productivity problem: CI/CD pipelines were taking up to a week to complete, and rollbacks were difficult and slow. This directly blocked business growth and increased incident recovery times, creating revenue risk. The program required coordination across 10+ development domains, 5 cloud infrastructure teams, and 3 platform teams. As the Cloud Application Lifecycle Management team manager, I was the infrastructure contact point responsible for identifying and resolving the cloud infrastructure bottlenecks blocking velocity.

## Task

My responsibility was to coordinate internally (cloud app, fleet, network, security teams) and externally (platform teams, CD pipeline teams, application development teams) to deliver specific infrastructure improvements: 95th-percentile deployment duration under 60 minutes for large applications, infrastructure reliability above 99%, DORA elite-tier metrics (deployment within 1 day, on-demand frequency, sub-hour rollback, 95%+ success rate) for 65% of applications. I also needed to resolve technical disagreements between engineering leads across teams to keep delivery moving.

## Action

- Conducted a thorough analysis of deployment metrics to identify the most impactful reliability bottlenecks and performance gaps — driving all prioritization from data, not opinions
- Identified that security policy initialization during pod startup was a major contributor to deployment delays for a subset of applications; led a categorization exercise segmenting applications into three buckets: no security policy, small policy, and large/complex policy
- Mediated a technical standoff between the CD pipeline team and the cloud security team: CD wanted a quick fix for current policy initialization; security wanted teams to wait for their next-generation policy solution. Analyzed the breakdown: only ~5% of applications had large complex policies — the blocker was disproportionate to its scope
- Brokered a phased agreement: immediately optimize applications with no or small security policies (fast wins), buy time for the security team to deliver their new solution, then integrate large-policy applications afterward — satisfying both teams' constraints
- Coordinated with internal infrastructure teams to deliver the agreed enhancements on schedule; served as the accountability point ensuring cross-team progress didn't stall

## Result

- 95th-percentile deployment duration reduced by 20% to 75 minutes (excluding large-security-policy applications)
- Development teams credited the balanced phased approach — they saw immediate improvements while knowing the harder cases were on a clear roadmap
- Leadership recognized the coordination work across 5+ infrastructure and 3+ platform teams and the ability to make steady progress despite complexity
- Large-security-application solution integration underway, following the agreed sequencing

## Related Skills

- [[skills/management/project/Technical Roadmap]]
- [[skills/management/people/Engineering Team Management]]
- [[skills/management/behavior/STAR Method]]
- [[skills/tech/infra/Kubernetes]]
- [[skills/tech/system-design/Distributed Systems]]

## Interview Usage

- 适用 BQ：Tell me about a time you exhibited leadership on a complex, multi-team program
- 适用 BQ：Describe a time you resolved a disagreement between engineering leads with conflicting approaches
- 适用 BQ：Give an example of using data to drive prioritization on a high-visibility program
- 适用 BQ：How do you balance short-term wins with long-term technical investments when under pressure?
- 适用 JD 关键词：engineering velocity, DORA metrics, CI/CD, cross-team leadership, conflict resolution, phased delivery, infrastructure reliability, developer productivity

## Key Questions

**Q: How do you lead a high-visibility program when you don't have direct authority over most of the teams involved?**
Talking points: Establish yourself as the infrastructure accountability point — a coordinator, not a director; use data (metrics) to create shared agreement on what matters most; make cross-team agreements explicit (phased approach, sequencing) so each team has clarity on their slice; show steady progress to leadership to maintain momentum and credibility.

**Q: Walk me through how you resolved a disagreement between two engineering leads with opposing views.**
Talking points: Understand each lead's underlying constraint (CD: speed now; Security: technical debt and migration risk); quantify the problem scope to reveal the actual distribution (only 5% large-policy apps); propose a phased solution that gives each team what they care about in the appropriate timeframe — don't force a single winner.

**Q: How do you approach prioritization when you're responsible for infrastructure improvements across many teams?**
Talking points: Start with a metrics analysis to identify what's actually causing the delay (data-driven, not intuition); segment the problem space to find quick wins that are independent of the hardest cases; sequence phases so early wins build momentum and buy time for the harder work.

**Q: How do you maintain progress on a year-long program when the scope keeps expanding?**
Talking points: Stay anchored to the DORA targets as the program's north star; treat scope additions as changes that require explicit prioritization, not automatic inclusion; regularly communicate what IS in scope and what is sequenced for later to prevent scope creep from stalling delivery.

## Summary

The eBay engineering velocity program was a company-wide initiative to fix a systemic developer productivity problem: pipelines taking a week and rollbacks that were painful, slow, and risky. My role was to represent cloud infrastructure — the layer that most other teams depended on — and drive the improvements that would unblock the broader program's DORA targets.

The key challenge wasn't technical; it was organizational. With 5 infrastructure teams, 3 platform teams, and 10+ application domains involved, progress required constant mediation and explicit sequencing of work across teams that had competing priorities. The most concrete example was the security policy deadlock: a 5% problem that was blocking progress for the other 95%. By quantifying the scope and structuring a phased agreement that respected both the CD team's need for fast wins and the security team's migration timeline, I unlocked forward motion without forcing either team to compromise their technical standards. The result was a 20% reduction in deployment duration for the initial target population, with a clear path for the remaining segment.

## Raw Material
- [[raw_material/experience/Engineering velocity improvement initiative]]
