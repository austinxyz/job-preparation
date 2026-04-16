---
title: eBay - Automated Cluster Management Overhaul
type: Additional
signal_areas: [Ownership, Perseverance, Leadership, Scope]
skills: [cluster-automation, infrastructure-lifecycle, cross-team-coordination, decommission, roadmap-execution, stakeholder-management]
company: eBay
date: 2024-06
impact: high
growing_link:
---

# eBay - Automated Cluster Management Overhaul

## Context

eBay's cloud fleet team was responsible for building and retiring 20+ clusters annually — cloud control planes, Hadoop systems, API gateways, and more — driven largely by annual tech refresh cycles that required decommissioning old clusters and building replacements. The existing process was a patchwork of manual steps and scripts that took weeks to over a month per cluster. New hardware sat idle while build work progressed; aging hardware couldn't be decommissioned quickly enough, creating ongoing finance losses from unused hardware and missed discount windows. The complexity was compounded by the diversity of cluster types and the need to maintain business continuity during peak periods.

The structural problem was that no shared automation contract existed across the many component teams involved in each cluster's lifecycle — network, security, app lifecycle, Hadoop each had their own manual process with no common interface. Without that, automation had to be rebuilt from scratch for every cluster type.

## Actions

- I shared the automation vision with the capacity team — our primary customer — negotiated a transition timeline, and set explicit expectations that short-term progress on manual cluster delivery might slow while we invested in automation. Getting their agreement upfront prevented the initiative from being killed by near-term delivery pressure.
- I sequenced the roadmap into three phases — decommission first, then cluster build, then tech refresh — based on where the ROI was clearest and the cross-team dependencies fewest. Decommission had the most direct hardware cost impact and the simplest automation surface; starting there made progress visible and fundable before we tackled the harder phases.
- I identified the highest-impact clusters and ring-fenced their manual delivery during the transition period — ensuring we didn't drop finance commitments while the automation work was in flight.
- I directed our tech lead to work with each component team to define common automation contracts — a shared interface each team could implement independently. Using the app lifecycle team's implementation as a concrete reference reduced ambiguity for the others. I led the team to build a proof-of-concept automated decommission pipeline with the app lifecycle team to demonstrate feasibility and onboard the remaining component teams.
- I presented progress and complexity to leadership to secure additional engineering resources for the cluster build and tech refresh phases — framing the ask as a de-risking investment backed by the delivered decommission ROI, not a continuation of an unvalidated initiative.

## Results

- Cluster decommission reduced from several weeks to a few days; the capacity team gained self-service control over the decommission flow.
- Automated decommission applied successfully to 5+ clusters to start; the capacity team has since continued applying it independently through the self-service flow.
- Cluster build automation completed for the API gateway cluster, hitting the one-week target timeline.
- Leadership validated the roadmap and endorsed continued investment in full lifecycle automation.
- Established the foundation for immutable infrastructure capabilities, reducing future incident risk and improving resource utilization.

## Learnings

- Sequencing by ROI clarity, not technical complexity, was the right call. Decommission wasn't the hardest problem — it was the most defensible first step. Getting that win on the board gave me the credibility and the resource case to push into the harder phases.
- Getting the capacity team's explicit agreement to the transition timeline before starting was load-bearing. Without that pre-commitment, every slow manual delivery during the transition period would have been cited as evidence the automation investment wasn't working.
- The shared automation contract approach was slower upfront but the only approach that scales to 20+ heterogeneous clusters per year. A single team's end-to-end solution for one cluster type would have solved the immediate problem and created a new maintenance silo.

## Signal Areas

**Primary:** Ownership (identified the systemic problem, designed the phased roadmap, drove cross-team alignment and leadership buy-in — no one asked for this to be built), Perseverance (sustained execution across multiple phases and component teams over many months with no shared mandate)

**Secondary:** Leadership (built alignment across network, security, app lifecycle, and Hadoop teams through shared contracts and a reference implementation rather than top-down mandate), Scope (20+ heterogeneous clusters annually, multiple component teams, finance impact at the hardware level)

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
Talking points: Establish a shared automation contract — a common interface each team can implement independently — rather than trying to build one team's end-to-end solution. Reduce coordination overhead with a reference implementation. Use early wins (self-service decomm) to build credibility and unlock resources for harder phases.

**Q: How do you balance building new capabilities with keeping existing operations running?**
Talking points: Identify the finite set of must-deliver clusters (protecting finance commitments); ring-fence those in the roadmap explicitly; communicate the tradeoff to the customer team before starting so they can plan accordingly — not as a surprise mid-execution.

**Q: Tell me about a time you secured leadership buy-in for a long-horizon initiative.**
Talking points: Show incremental, measurable progress first (self-service decomm in days, hardware cost reduction). Quantify the ROI. Frame the ask for more resources as a de-risking investment validated by the first phase, not a sunk-cost continuation. Leadership responds to "we proved it works, here's what it takes to scale it" better than "trust us, it'll be worth it."

**Q: How do you get multiple engineering teams to align on a common technical contract?**
Talking points: Define the contract based on the desired automation workflow, not on what any one team already has. Build one working implementation as a proof point — it removes ambiguity more effectively than a spec document. Let teams self-implement with clear success criteria rather than dictating implementation detail.

## Summary

eBay's cluster lifecycle process — 20+ clusters per year across heterogeneous types — was a manual bottleneck that was costing real money in idle hardware and missed discount windows. The core problem was structural: no shared automation contract existed across the component teams involved in each cluster's lifecycle, so every cluster type required its own manual process with no reuse.

I sequenced the roadmap to start with cluster decommission — the phase with the clearest ROI and fewest cross-team dependencies — and used the first successful delivery to prove feasibility, earn team confidence, and negotiate leadership resources for the harder phases. The result was a self-service decommission capability the capacity team could operate independently, a cluster build pipeline that hit the one-week target, and a foundation for immutable infrastructure. The key judgment call was insisting on shared contracts across teams rather than a single team's end-to-end solution — slower to establish but the only architecture that scales to the full heterogeneous fleet.

## Raw Material
- [[raw_material/experience/Automated Cluster Management Overhaul]]
