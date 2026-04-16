---
title: eBay - Resolving L7 Traffic Gap
type: Additional
signal_areas: [Conflict Resolution, Ownership]
skills: [az-rebalance, cross-team-collaboration, technical-disagreement, site-reliability, capacity-management, sop-design]
company: eBay
date: 2024-06
impact: high
growing_link:
---

# eBay - Resolving L7 Traffic Gap

## Context

My team had built APIs enabling the capacity team to automatically rebalance resources across Availability Zones for most applications. A gap remained: a small subset of applications handling public Layer 7 traffic were unsupported — core to eBay's business and at risk of latency or revenue impact during traffic spikes. My manager and I had conflicting views on how to address it. He wanted to extend the existing solution with minimal changes, prioritizing resource efficiency; my team and I believed these applications required specialized handling given their traffic patterns.

The disagreement wasn't about whether the gap mattered — it was about how to close it without compromising the resource efficiency targets already committed to.

## Actions

- I acknowledged my manager's resource efficiency goal as a legitimate constraint, not an obstacle to overcome. Reframing the disagreement as "how do we satisfy both constraints" rather than "who is right" changed how we could talk about it.
- My tech lead and I met with the network team, who had domain expertise in L7 traffic patterns, to understand what tooling already existed — specifically to avoid building something from scratch if the capability was already there.
- We discovered they had already built a specialized tool for managing L7 traffic ramp-ups. This was the unlock: an existing capability we could integrate rather than build.
- My tech lead and I collaborated with the network team to design a two-phase workflow: use the existing AZ rebalance system for normal operations, then trigger the network team's L7 tool during high-traffic ramp-up periods. This satisfied both the reliability requirement for L7 applications and my manager's efficiency constraint — neither system needed to be replaced.
- I directed the team to write a detailed SOP documenting the workflow, trigger conditions, and handoff points between the two systems, so the team could execute consistently without waiting for full automation.

## Results

- Two-phase workflow implemented within 1 month, validated through a trial run and pilot on a subset of applications.
- AZ ramp-up time for public L7 applications reduced to within 1 day — previously unsupported entirely.
- AZ resource utilization maintained at 40–80%, meeting the manager's efficiency targets.
- Team completed the full auto-rebalance solution for private traffic and public L4 applications within 3 months.
- End-to-end AZ workload management coverage delivered across all application types.

## Learnings

- Treating my manager's constraint as valid from the start — rather than as resistance to overcome — was what made the conversation productive. Once the goal was "satisfy both constraints" instead of "win the disagreement," the solution space opened up.
- The network team meeting was the turning point, and we would have missed it if we'd started from "what do we build" rather than "what already exists." Going to domain experts before committing to a build should be the default, especially under time pressure.
- The SOP was the right short-term move. Full automation would have taken weeks longer; a well-documented manual workflow covered the reliability gap immediately and gave the team time to automate the right way.

## Signal Areas

**Primary:** Conflict Resolution (genuine technical disagreement with my manager; resolved by reframing as a constraint problem, doing lateral investigation to find a third path, and proposing a solution that satisfied both positions)

**Secondary:** Ownership (identified and closed a gap in a system my team owned; took initiative to investigate and deliver rather than waiting for the disagreement to be resolved top-down)

## Related Skills
- [[skills/tech/system-design/Distributed Systems]]
- [[skills/tech/infra/Kubernetes]]
- [[skills/management/project/Technical Roadmap]]

## Interview Usage
- 适用 BQ：Tell me about a time you disagreed with your manager
- 适用 BQ：Describe a situation where you had to influence without authority
- 适用 BQ：Tell me about a time you found a creative solution to a technical constraint
- 适用 BQ：Tell me about a time you drove cross-team collaboration to solve a problem
- 适用 JD 关键词：site reliability, capacity management, AZ rebalancing, cross-functional collaboration, technical leadership, SOP design, traffic management, conflict resolution

## Key Questions

**Q: How did you handle a technical disagreement with your manager?**
Talking points: Validate their goal first (efficiency is a real constraint, not an excuse). Reframe the disagreement as a tradeoff problem rather than a binary win/lose. Bring in external input — meeting with the network team reopened the solution space in a way that internal debate couldn't. Propose a path that satisfies both constraints, not a compromise that partially satisfies neither.

**Q: Walk me through a time you resolved a gap in a system you owned.**
Talking points: Define the gap's business risk clearly (L7 traffic → revenue exposure during spikes). Explain why extending the existing solution didn't fit the L7 traffic pattern. Describe the lateral investigation that found the existing network team tool. Quantify the outcome: 1-day ramp-up, 40–80% utilization maintained, full coverage within 3 months.

**Q: How do you build cross-team buy-in for a solution?**
Talking points: Start by understanding what the other team has already built — avoid duplicate effort and create an incentive for them to participate. Co-design the integration rather than dictating requirements. Formalize the handoff with an SOP so both teams can operate the workflow reliably without full automation on day one.

**Q: How do you balance reliability and efficiency when they appear to conflict?**
Talking points: Treat them as constraints, not a zero-sum choice. Identify where the real tradeoff boundary is — in this case, a small set of L7 apps, not all traffic. Find a tiered approach that honors both within acceptable ranges. The disagreement often dissolves once you've scoped the actual problem correctly.

## Summary

At eBay, my team owned the AZ rebalance system that allowed the capacity team to dynamically shift workloads across Availability Zones. The system covered most applications, but a gap remained for public L7 traffic — revenue-critical applications that were entirely unsupported. My manager favored minimal extension to protect resource efficiency goals; I believed the reliability risk was too high to defer.

Rather than escalating the disagreement, my tech lead and I met with the network team and discovered they had already built an L7 traffic ramp-up tool. We collaborated with them to design a two-phase workflow that closed the gap without a rebuild or significant diversion of team effort — and satisfied both my manager's efficiency constraint and the reliability requirement for L7 applications. The solution delivered complete AZ coverage within a month. The more general lesson: reframing a conflict as a constraint problem and doing the legwork to find existing capabilities can resolve what looks like a deadlocked disagreement.

## Raw Material
- [[raw_material/experience/Resolving L7 Traffic Gap]]
