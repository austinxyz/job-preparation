---
title: eBay - Automated Cluster Management Overhaul
type: experience
skills: [cluster-automation, infrastructure-lifecycle, cross-team-coordination, decommission, roadmap-execution, stakeholder-management]
company: eBay
date: 2024-06
impact: high
growing_link:
---

# eBay - Automated Cluster Management Overhaul

## Situation

At eBay, our cloud fleet team was responsible for building and retiring 20+ clusters annually — cloud control planes, Hadoop systems, API gateways, and more. The existing process was a patchwork of manual steps and scripts that took 2 weeks to a month per cluster. New hardware sat idle while build work progressed, and aging hardware couldn't be decommissioned quickly enough, creating ongoing finance losses from unused and over-discounted hardware. The complexity was compounded by the diversity of cluster types and the need to maintain business continuity during peak holiday periods.

## Task

As lead engineer, I was accountable for designing and driving an automated cluster lifecycle system — covering build, tech refresh, and decommission — targeting a one-week end-to-end timeline. I needed to coordinate across multiple component teams (network, security, app lifecycle, Hadoop), define common automation contracts, and balance the team's development capacity against ongoing operational demands without dropping delivery commitments on key clusters.

## Action

- Shared the automation vision with the capacity team (our primary customer), negotiated a transition timeline, and set expectations that short-term progress on manual clusters might slow while we invested in automation
- Identified the highest-impact clusters and prioritized their decommission/build delivery to prevent finance impact during the transition period
- Split the roadmap into three sequential phases — decommission first (clearest ROI, reduced hardware discount costs), then cluster build, then tech refresh — to make progress visible and fundable
- Worked with each component team (app lifecycle, network, security) to define common automation contracts; used the app lifecycle team's implementation as a concrete reference for others
- Built a proof-of-concept automated decommission pipeline with the app lifecycle team to demonstrate feasibility and onboard other component teams
- Presented progress and complexity to leadership to secure additional engineering resources for the cluster build and tech refresh phases

## Result

- Cluster decommission reduced from several weeks to a few days; capacity team gained self-service control over the decomm flow
- Applied the automated decommission to 5+ clusters successfully
- Completed cluster build automation for the API gateway cluster, hitting the one-week target timeline
- Leadership validated the roadmap and endorsed continued investment in full lifecycle automation
- Established foundation for immutable infrastructure capabilities, enabling future incident reduction and improved resource utilization

## Related Skills

- [[skills/tech/infra/Kubernetes]]
- [[skills/management/project/Technical Roadmap]]
- [[skills/management/people/Engineering Team Management]]
- [[skills/tech/system-design/Distributed Systems]]

## Interview Usage

- 适用 BQ：Tell me about a time your perseverance drove a long-term initiative to success
- 适用 BQ：Describe a time you had to coordinate across many teams to deliver a complex project
- 适用 BQ：Tell me about a time you balanced operational demands with strategic investment
- 适用 BQ：Give an example of building a roadmap and sequencing work under resource constraints
- 适用 JD 关键词：cluster lifecycle management, infrastructure automation, cross-team coordination, roadmap sequencing, stakeholder management, self-service platform, decommissioning, immutable infrastructure

## Key Questions

**Q: How do you drive a complex multi-team automation initiative when there is no shared mandate?**
Talking points: Establish a shared contract/interface that each team can implement independently; reduce coordination overhead with a reference implementation; use early wins (cluster decomm) to build credibility and unlock resources for harder phases.

**Q: How do you balance building new capabilities with keeping existing operations running?**
Talking points: Identify the finite set of must-deliver clusters (to protect finance commitments); explicitly ring-fence those in the roadmap; communicate the tradeoff to the customer team early so they can plan accordingly.

**Q: Tell me about a time you secured leadership buy-in for a long-horizon initiative.**
Talking points: Show incremental, measurable progress first (self-service decomm in a few days); quantify the ROI (hardware cost, incident risk); frame the ask for more resources as a de-risking investment, not a sunk-cost continuation.

**Q: How do you get multiple engineering teams to align on a common technical contract?**
Talking points: Define the contract top-down based on the desired automation workflow; build one working implementation as a proof point; let teams self-implement with clear success criteria rather than dictating the implementation detail.

## Summary

When I joined eBay's cloud fleet team, the cluster lifecycle process was a bottleneck that was costing the company real money — idle new hardware and overdue decommissions drove compounding financial losses. I saw that the core problem was the absence of a shared automation contract across the many component teams involved in each cluster's lifecycle, and that fixing it required both a clear technical design and sustained organizational coordination over many months.

I sequenced the roadmap to start with cluster decommission — the phase with the clearest ROI and the fewest dependencies — and used the first successful delivery to prove feasibility, earn team confidence, and negotiate leadership support for the harder phases. The result was a self-service decomm capability the capacity team could operate independently, a cluster build pipeline that hit our one-week target, and a foundation for immutable infrastructure that leadership had been waiting for. The key judgment call was choosing to invest in shared contracts across teams rather than building one team's end-to-end solution — slower upfront, but the only approach that scales to 20+ heterogeneous clusters per year.

## Raw Material
- [[raw_material/experience/Automated Cluster Management Overhaul]]
