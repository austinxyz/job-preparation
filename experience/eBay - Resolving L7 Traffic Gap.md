---
title: eBay - Resolving L7 Traffic Gap
type: experience
skills: [az-rebalance, cross-team-collaboration, technical-disagreement, site-reliability, capacity-management, sop-design]
company: eBay
date: 2024-06
impact: high
growing_link:
---

# eBay - Resolving L7 Traffic Gap

## Situation

At eBay, my team had built APIs enabling the capacity team to automatically rebalance resources across Availability Zones for most applications. However, a small subset of applications handling public Layer 7 traffic remained unsupported — these were core to eBay's business and at risk of latency or revenue impact during traffic spikes. My manager and I had conflicting views on how to address the gap: he wanted to extend the existing solution with minimal changes, prioritizing resource efficiency; my team and I believed these applications required specialized handling.

## Task

As tech lead, I was accountable for resolving the technical disagreement and delivering a solution that covered public L7 traffic applications without sacrificing the AZ resource efficiency goals already committed to. I needed to find a path that satisfied both the reliability requirement and my manager's constraint.

## Action

- Acknowledged my manager's resource efficiency goal as valid, rather than treating the disagreement as a binary conflict
- Reached out to the network team, who had domain expertise in L7 traffic patterns, to understand what tooling existed
- Discovered they had already built a specialized tool for managing L7 traffic ramp-ups — an existing capability I could leverage rather than build from scratch
- Designed a two-phase workflow: use the existing AZ rebalance system for normal operations, then trigger the network team's L7 tool during high-traffic periods
- Wrote a detailed SOP documenting the workflow, trigger conditions, and handoff points between the two systems, enabling the team to execute consistently without full automation in the short term

## Result

- Implemented the two-phase workflow within 1 month; validated through try-run and pilot on a subset of applications
- Reduced AZ ramp-up time for public L7 applications to within 1 day (previously unsupported entirely)
- Maintained AZ resource utilization at 40–80%, meeting the manager's efficiency targets
- Team completed the full auto-rebalance solution for private traffic and public L4 applications within 3 months
- Delivered end-to-end AZ workload management coverage across all application types

## Related Skills

- [[skills/tech/system-design/Distributed Systems]]
- [[skills/tech/infra/Kubernetes]]
- [[skills/management/behavior/STAR Method]]
- [[skills/management/project/Technical Roadmap]]

## Interview Usage
- 适用 BQ：Tell me about a time you disagreed with your manager
- 适用 BQ：Describe a situation where you had to influence without authority
- 适用 BQ：Tell me about a time you found a creative solution to a technical constraint
- 适用 BQ：Tell me about a time you drove cross-team collaboration to solve a problem
- 适用 JD 关键词：site reliability, capacity management, AZ rebalancing, cross-functional collaboration, technical leadership, SOP design, traffic management, conflict resolution

## Key Questions

**Q: How did you handle a technical disagreement with your manager?**
Talking points: Validate their goal first (efficiency), reframe the disagreement as a tradeoff rather than a binary; bring data or external input (network team discovery) to reopen the solution space; propose a path that satisfies both constraints.

**Q: Walk me through a time you resolved a gap in a system you owned.**
Talking points: Define the gap's business risk clearly (L7 traffic → revenue exposure); explain why existing solutions didn't fit; describe the investigation that uncovered the two-phase approach; quantify the outcome (1-day ramp-up, 40–80% utilization maintained).

**Q: How do you build cross-team buy-in for a solution?**
Talking points: Start by understanding the other team's existing work (avoid duplicate effort); co-design rather than dictate; formalize the handoff with an SOP so both teams can operate it reliably.

**Q: How do you balance reliability and efficiency when they conflict?**
Talking points: Treat them as constraints, not a zero-sum choice; identify where the real tradeoff boundary is (small set of L7 apps, not all traffic); find a phased or tiered approach that honors both within acceptable ranges.

## Summary

At eBay, I owned the AZ rebalance system that allowed the capacity team to dynamically shift workload across Availability Zones. The system worked well for most applications, but a gap remained: public L7 traffic applications — high-stakes, revenue-critical — were unsupported. My manager favored deferring support to keep the team focused on efficiency goals; I believed the reliability risk was too high to leave unaddressed.

Rather than escalating the disagreement, I investigated the problem laterally and discovered the network team had already built an L7 traffic ramp-up tool. This unlocked a two-phase workflow that covered the gap without requiring a full rebuild or significant diversion of team effort. The solution delivered complete AZ coverage within a month, maintained resource utilization in the target range, and demonstrated how reframing a conflict as a constraint problem — and doing the legwork to find hidden existing capabilities — can resolve seemingly deadlocked disagreements.

## Raw Material
- [[raw_material/experience/Resolving L7 Traffic Gap]]
