---
title: eBay - Engineering Velocity Program
type: Core
signal_areas:
  - Conflict Resolution
  - Leadership
  - Scope
skills:
  - engineering-velocity
  - ci-cd
  - cross-team-leadership
  - dora-metrics
  - security-policy
  - stakeholder-alignment
  - conflict-resolution
company: eBay
date: 2024-01
impact: high
growing_link:
---

# eBay - Engineering Velocity Program

## Context

eBay launched a company-wide engineering velocity program to fix a serious developer productivity problem: CI/CD pipelines were taking up to a week to complete, and rollbacks were difficult and slow — directly blocking business growth and increasing incident recovery times. The program required coordination across 10+ development domains, 5 cloud infrastructure teams, and 3 platform teams. As the Cloud Application Lifecycle Management team manager, I was the infrastructure contact point responsible for identifying and resolving the cloud infrastructure bottlenecks blocking velocity.

The program's targets were specific: 95th-percentile deployment duration under 60 minutes for large applications, infrastructure reliability above 99%, and DORA elite-tier metrics (deployment within 1 day, on-demand frequency, sub-hour rollback, 95%+ success rate) for 65% of applications.

## Actions

- I directed the team to conduct a thorough analysis of deployment metrics to identify the most impactful bottlenecks — making sure all prioritization decisions were grounded in data rather than team opinions about what was slow.
- Based on that data, I developed a phased proposal that segmented applications into three buckets by security policy complexity: no security policy, small policy, and large/complex policy. The key insight the data revealed: only ~5% of applications had large complex policies, but they were creating disproportionate noise in the overall velocity conversation.
- The CD pipeline team and the cloud security team were at an impasse: CD wanted an immediate fix for security policy initialization delays during pod startup; security wanted teams to wait for their next-generation policy solution. I brought the proposal to the broader working group, and stakeholders across both teams reached consensus on a phased sequencing: immediately optimize the no-policy and small-policy buckets (covering ~95% of apps), buy time for the security team to deliver their new solution, then integrate the large-policy applications afterward.
- I served as the cross-team accountability point, coordinating with internal infrastructure teams to deliver the agreed enhancements on schedule and ensuring cross-team progress didn't stall between milestones.

## Results

- 95th-percentile deployment duration reduced by 20% to 75 minutes for the initial target population (excluding large-security-policy applications).
- Development teams credited the phased approach — they saw immediate, measurable improvement while knowing the harder cases were on a clear, committed roadmap.
- Leadership recognized the coordination work across 5+ infrastructure and 3+ platform teams and the ability to maintain steady progress despite the organizational complexity.
- Large-security-policy application integration underway following the agreed sequencing.

## Learnings

- Quantifying the actual scope of the blocker was the move that broke the deadlock. "Security policy delays are a problem" was a subjective claim both teams could argue. "Only 5% of applications have complex policies" was a fact that reframed the conversation — it made the phased approach obviously correct rather than a compromise.
- Being the infrastructure accountability point in a program this size meant a lot of the work was coordination, not technical execution. That's uncomfortable when you're used to measuring progress by what ships. I had to redefine "making progress" as keeping cross-team agreements intact and unblocking whoever was stuck — not just delivering my team's slice.
- The phased agreement only held because both teams saw their constraint respected in the sequencing. A solution that asked either team to compromise their core position would have generated compliance without commitment — I'd have gotten nominal agreement and then watched it slip.

## Signal Areas

**Primary:** Conflict Resolution (two engineering teams were at an impasse with incompatible short-term positions; I developed a data-grounded phased proposal and brought it to the working group, creating the conditions for consensus that unblocked the broader program), Leadership (coordinated across 15+ teams without direct authority; served as the accountability point keeping cross-team delivery on track)

**Secondary:** Scope (company-wide program; 10+ development domains, 5 infrastructure teams, 3 platform teams; revenue-impacting velocity problem)

## Related Skills
- [[skills/management/project/Technical Roadmap]]
- [[skills/management/people/Engineering Team Management]]
- [[skills/tech/infra/Kubernetes]]
- [[skills/tech/system-design/Distributed Systems]]

## Interview Usage
- 适用 BQ：Tell me about a time you resolved a disagreement between engineering leads with conflicting approaches
- 适用 BQ：Tell me about a time you led a high-visibility program without direct authority
- 适用 BQ：Give an example of using data to drive prioritization on a complex program
- 适用 BQ：How do you balance short-term wins with long-term technical investments under pressure?
- 适用 JD 关键词：engineering velocity, DORA metrics, CI/CD, cross-team leadership, conflict resolution, phased delivery, infrastructure reliability, developer productivity

## Key Questions

**Q: Walk me through how you helped resolve a disagreement between two engineering leads with opposing views.**
Talking points: Understand each side's underlying constraint — CD team needed fast wins; security team needed migration runway. Use data to reframe the debate: only 5% of applications had complex policies, which meant the "wait for the new solution" position was costing the other 95% their velocity improvements. Bring a phased proposal to the working group that gives each team what they care about in the appropriate timeframe — create the conditions for consensus rather than trying to force a winner.

**Q: How do you lead a high-visibility program when you don't have direct authority over most teams involved?**
Talking points: Establish yourself as the infrastructure accountability point — coordinator, not director. Drive all prioritization from data so decisions aren't personality contests. Make cross-team agreements explicit (phased approach, sequencing, milestone ownership) so each team has clarity on their slice. Show steady progress to leadership to maintain momentum and your own credibility as the coordinator.

**Q: How do you approach prioritization when you're responsible for improvements across many teams?**
Talking points: Start with a metrics analysis to identify what's actually causing the delay — not what teams think is causing it. Segment the problem space to find quick wins that are independent of the hardest cases. Sequence phases so early wins build momentum and buy time for the harder work. A 5% edge case shouldn't block 95% of the population.

**Q: How do you maintain progress on a year-long program when scope keeps expanding?**
Talking points: Stay anchored to the DORA targets as the north star. Treat scope additions as changes that require explicit prioritization, not automatic inclusion. Regularly communicate what IS in scope and what is sequenced for later — prevents scope creep from becoming an excuse for stalled delivery.

## Summary

The eBay engineering velocity program was a company-wide initiative to fix a systemic developer productivity problem: pipelines taking up to a week and rollbacks that were painful and slow. My role was to represent cloud infrastructure — the layer most other teams depended on — and drive the improvements that would unblock the broader DORA targets.

The key challenge wasn't technical; it was organizational. With 5 infrastructure teams, 3 platform teams, and 10+ application domains involved, progress required constant mediation and explicit cross-team sequencing. The most concrete example was the security policy deadlock: a 5% problem blocking progress for the other 95%. I developed a phased proposal grounded in the data and brought it to the working group — quantifying the scope changed the conversation from a technical debate into an obvious sequencing decision, and stakeholders reached consensus on the phased approach. The result was a 20% deployment duration reduction for the initial population and a clear committed path for the remaining segment.

## Raw Material
- [[raw_material/experience/Engineering velocity improvement initiative]]
