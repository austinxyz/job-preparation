---
title: eBay - Cloud Infrastructure Team Turnaround
type: experience
skills: [engineering-management, team-turnaround, sre-practices, reliability, incident-management, people-leadership]
company: eBay
date: 2023-09
impact: high
growing_link:
---

# eBay - Cloud Infrastructure Team Turnaround

## Situation

I stepped in to manage a cloud infrastructure team of 7 engineers that had been without a manager for several months. The situation was in crisis: a 24-hour API server outage had just occurred, system reliability had dropped below 90%, and critical incidents were happening multiple times per week. The team was demoralized — constant firefighting, a backlog of customer complaints, and no sense of progress. Senior leadership expected me to stop the bleeding and restore customer confidence quickly.

## Task

My task was to execute a full turnaround: restore system reliability to above 99%, reduce incident recovery time from 24+ hours to under 1 hour, and rebuild team confidence and engagement — all within a few months. I needed to identify and execute the highest-leverage technical fixes while simultaneously stabilizing team dynamics and rebuilding customer trust.

## Action

- Started with in-depth conversations with key customers to understand their pain points and establish clear service level objectives (SLOs) as the shared success criteria
- Focused the team on two initiatives: an API server infrastructure upgrade and onboarding SRE best practices — chosen because they addressed both the root cause of instability and the team's lack of structured incident management
- Phased the API server upgrade version by version (not a big-bang upgrade), starting in testing/staging to contain risk; this addressed the team's concern that an upgrade would create more instability
- For SRE adoption, started with the most important non-functional requirements the customer cared about (per SLO conversations), so early wins were immediately visible to customers
- Coached engineers by asking probing questions rather than prescribing solutions; when an engineer proposed a caching solution for API endpoints, I helped them refine it through technical dialogue and gave them ownership of the implementation
- Ran regular retrospectives to convert incidents into learning; celebrated wins explicitly — internally with the team and externally with customers — to rebuild confidence and shift from reactive firefighting to proactive ownership

## Result

- System reliability improved from below 90% to consistently above 99% within 3 months
- Incident recovery time dropped from 24+ hours to under 1 hour
- Critical incidents decreased from multiple per week to rare occurrences
- Customers noticed the improvement within 2 months; one specifically commended our transparent communication during the transformation
- Team shifted from reactive firefighting to proactive issue identification — measurable change in team posture and engagement
- Established durable foundations: automated testing, comprehensive monitoring, and incident response protocols

## Related Skills

- [[skills/management/people/Engineering Team Management]]
- [[skills/management/behavior/STAR Method]]
- [[skills/management/project/Technical Roadmap]]
- [[skills/tech/infra/Kubernetes]]

## Interview Usage

- 适用 BQ：Tell me about a time your adaptability was crucial in navigating a difficult situation
- 适用 BQ：Describe a time you took over a struggling team and turned it around
- 适用 BQ：How do you rebuild team morale and confidence after a period of sustained failure?
- 适用 BQ：Give an example of how you balanced short-term stabilization with long-term structural improvement
- 适用 JD 关键词：team leadership, reliability, SRE, incident management, SLO, stakeholder communication, coaching, turnaround

## Key Questions

**Q: How do you stabilize a team that is in crisis when you're new to the team?**
Talking points: Start with customer conversations (external grounding, not internal politics); identify two high-leverage focus areas rather than trying to fix everything; make immediate small progress visible to rebuild team confidence; protect the team from new work while they execute.

**Q: How do you coach engineers who lack confidence without undermining their ownership?**
Talking points: Ask questions rather than giving answers — guide them toward a robust solution, but let them lead; explicitly give them ownership of the implementation; recognize their wins publicly to reinforce that their judgment is valued.

**Q: How do you manage the tension between doing an upgrade safely vs. quickly when reliability is already poor?**
Talking points: Phased approach by version, not a big-bang; start in staging/testing to isolate risk; communicate the phasing plan to the team so they understand why it's safer; each minor version is a decision point, not a commitment to the full upgrade path.

**Q: How do you rebuild customer trust after a major reliability failure?**
Talking points: Establish SLOs co-defined with the customer (shared accountability); provide transparent progress updates at regular intervals; celebrate milestones (first month at 99.9%) with the customer, not just internally.

## Summary

When I took over this cloud infrastructure team, the immediate crisis was technical — a major API server outage and reliability below 90% — but the deeper problem was organizational: no clear ownership of reliability standards, no structured incident learning, and a team so burned by firefighting that they'd lost confidence in their own ability to fix things.

My first move was external: talking to customers to anchor the team's work in concrete SLOs rather than internal opinions about what mattered. From there, I narrowed the focus ruthlessly to two initiatives — an API server upgrade and SRE onboarding — and phased both conservatively to protect a team that couldn't absorb more instability. The recovery was faster than expected: 99%+ reliability within 3 months, sub-hour incident recovery, and a team that was proactively identifying issues instead of reacting to them. The most important judgment call was choosing to coach rather than direct — giving engineers ownership of the solutions built their confidence at the same time as it fixed the systems, making the improvement sustainable rather than dependent on me.

## Raw Material
- [[raw_material/experience/Cloud Infrastructure Team Turnaround]]
