---
title: eBay - Embracing a New Leadership Challenge
type: Additional
signal_areas: [Growth, Leadership, Ownership]
skills: [growth-mindset, engineering-management, sre-practices, incident-management, people-development, zone-of-discomfort]
company: eBay
date: 2023-09
impact: high
growing_link:
---

# eBay - Embracing a New Leadership Challenge

## Context

After 15+ years at eBay — 10 in cloud infrastructure — I had built a successful Application Lifecycle Management team and was operating in a domain I knew deeply. When my manager asked me to take over the cloud fleet and core services team, it was a genuine stretch: a different technical domain, higher criticality (the team's API server was relied on by every eBay developer), and a team that had been without a manager for six months. System reliability had dropped below 90%, critical incidents were happening multiple times per week, and customer complaints were escalating.

I could have stayed in my established domain. I chose not to. The discomfort was the point — this was the kind of assignment that would either expose gaps in my leadership model or prove it worked beyond the domain I'd built it in.

## Actions

- I accepted the assignment intentionally, framing the unfamiliarity as the learning mechanism rather than a risk to manage around. That framing mattered because it changed how I approached the first weeks — not trying to project confidence I didn't have, but being explicit that I was learning.
- I started from the outside in: I engaged key customers — eBay developers who depended on the API server — to understand their pain points before forming any internal opinions about what to fix. This gave the team an external anchor instead of internal debate about priorities.
- I borrowed expertise deliberately rather than faking it. I partnered with the Cloud SRE team to import SRE best practices — SLOs, error budgets, runbooks, incident process — rather than trying to reinvent reliability engineering in a domain I was still learning.
- I anchored the team's work in customer-defined SLOs, translating vague complaints into specific, observable targets that gave engineers clarity on what success looked like.
- I formed a dedicated reliability sub-team (1 lead + 2 members) to concentrate focus on the highest-leverage work and give it structural protection from the ongoing firefighting.
- I introduced post-incident retrospectives as a standing practice, explicitly reframing mistakes as learning inputs — modeling the behavior I needed the team to adopt before asking them to adopt it.
- I recognized and celebrated small wins both internally and externally with customers; visible external validation rebuilt team confidence faster than any technical fix.

## Results

- Service reliability improved from below 90% to stable 99%+ within 2–3 months.
- Major incidents eliminated; incident recovery time reduced from multiple days to under one hour.
- Team shifted from reactive firefighting to proactive risk identification — retrospectives moved from blame to learning.
- Customers sent positive feedback and thank-you emails within 2 months — external validation of the turnaround.
- Durable foundations established (SLOs, runbooks, alert coverage) that reduced ongoing firefighting load after the initial recovery.

## Learnings

- Not having domain expertise forced me to use the right leadership levers — customer conversations, borrowed SRE expertise, structured frameworks — rather than substituting technical opinions for management judgment. In retrospect, the unfamiliarity made me a better manager of this team than I might have been if I'd started with deep technical confidence.
- Being explicit about what I didn't know built more trust with the team than projecting false confidence would have. Engineers in crisis mode don't need a manager who knows the answers — they need one who asks the right questions and creates the conditions to find them.
- The retrospective culture shift was slower than the reliability improvement and more durable. Technical fixes revert when the conditions that caused them return; a team that treats incidents as learning inputs doesn't revert.

## Signal Areas

**Primary:** Growth (deliberate choice to take on a technically unfamiliar domain in crisis; treated discomfort as the learning mechanism rather than the risk; applied leadership model beyond its original context and validated it)

**Secondary:** Leadership (rebuilt a demoralized team without domain expertise by starting from customers, borrowing SRE frameworks, and giving engineers ownership of solutions), Ownership (accepted accountability for a team in crisis with no context handover; drove the full arc from crisis to stable operations)

## Related Skills
- [[skills/management/people/Engineering Team Management]]
- [[skills/management/project/Technical Roadmap]]
- [[skills/tech/infra/Kubernetes]]

## Interview Usage
- 适用 BQ：Tell me about a time you voluntarily stepped outside your comfort zone
- 适用 BQ：How do you become effective quickly when leading a team in an unfamiliar technical domain?
- 适用 BQ：Describe a time you took on a high-risk assignment and delivered despite personal uncertainty
- 适用 BQ：Tell me about a time you had to grow as a leader, not just execute
- 适用 JD 关键词：growth mindset, adaptability, engineering management, SRE, incident management, SLO, people development, customer orientation

## Key Questions

**Q: Tell me about a time you took on something well outside your comfort zone.**
Talking points: Name the specific stretch — new technical domain, leaderless team in crisis, six months of deferred problems, higher criticality than my previous scope. Explain why I said yes: belief the leadership skills transferred, and recognition that staying in the comfortable domain would cap my growth. Describe how I navigated unfamiliarity (customer-first, borrowed SRE expertise). Outcome: reliability recovered to 99%+ in 3 months, team culture shifted from firefighting to learning.

**Q: How do you lead effectively when you don't have deep domain expertise?**
Talking points: Start from customer needs, not technical assumptions. Identify who does have the expertise and partner explicitly — I used the SRE team, not my own knowledge. Ask questions before prescribing solutions. Use structured frameworks (SLOs, runbooks) to establish rigor without relying on tribal knowledge. Being explicit about what you're learning builds more trust than projecting false confidence.

**Q: How do you rebuild a demoralized team quickly?**
Talking points: Psychological safety first — celebrate wins, reframe mistakes as learning inputs, model the behavior before asking for it. Give engineers ownership of real solutions. Make progress visible externally — customer recognition matters more than manager praise. Retrospectives convert firefighting culture into learning culture, but they require consistent reinforcement to take hold.

**Q: What does growth mindset look like in a senior leader?**
Talking points: Choosing hard problems over comfortable ones when the growth matters more than execution certainty. Using unfamiliarity as a discovery mechanism rather than hiding it. Modeling risk-taking explicitly — the team watches what you do more than what you say. Treating the stretch assignment as evidence of where the growth is, not exposure to be minimized.

## Summary

After 10 years in cloud infrastructure at eBay, I was asked to lead a team outside my established domain — one in crisis after six months without a manager. Accepting that assignment was a deliberate choice, not obligation. The discomfort was the point: this was the kind of problem that would either expose limits in my leadership model or validate that it worked beyond the domain I'd built it in.

The key judgment call was recognizing what I didn't know and borrowing expertise rather than faking confidence — partnering with the SRE team, anchoring everything in customer-defined SLOs, and giving engineers ownership of the solutions. Reliability recovered from below 90% to above 99% within three months. More durably, the team shifted from reactive firefighting to proactive ownership — which meant the results held. The more lasting lesson was that not having domain expertise forced me to use the right leadership levers rather than substituting technical opinions for management judgment. The unfamiliarity made me a better manager of this team.

## Raw Material
- [[raw_material/experience/Experience STAR summary]]
