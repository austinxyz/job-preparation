---
title: eBay - Cloud Infrastructure Team Turnaround
type: Additional
signal_areas: [Leadership, Ownership, Perseverance, Communication, Scope]
skills: [engineering-management, team-turnaround, sre-practices, reliability, incident-management, people-leadership]
company: eBay
date: 2023-09
impact: high
growing_link:
---

# eBay - Cloud Infrastructure Team Turnaround

## Context

I stepped in to manage a cloud infrastructure team of 7 engineers that had been without a manager for several months — absorbing them while continuing to run my existing team of 6. The situation was in crisis: a 24-hour API server outage had recently occurred, system reliability had dropped below 90%, and critical incidents were happening multiple times per week. The team was demoralized — constant firefighting, a growing backlog of customer complaints, and no sense that anything they did was making it better. Senior leadership expected a fast turnaround.

The deeper problem wasn't technical. There were no shared reliability standards, no structured process for learning from incidents, and a team so burned by reactive firefighting that they'd lost confidence in their own judgment. Fixing the systems required fixing both layers simultaneously.

## Actions

- I started with in-depth conversations with key customers rather than an internal audit — to anchor the team's work in concrete SLOs and give us a shared definition of success that wasn't just "fewer pages." This also gave us a credibility signal to customers that we were treating this seriously.
- I narrowed the team's focus to two initiatives: an API server infrastructure upgrade and onboarding SRE best practices. Both addressed root causes — the upgrade tackled the instability source; SRE practices built the structured incident management the team was missing. I protected the team from new work intake while they executed.
- I phased the API server upgrade version by version rather than big-bang, starting in test/staging environments. The team was worried a disruptive upgrade would make things worse before they got better — the phased approach let each version be a discrete decision point and kept risk contained while still moving forward.
- For SRE adoption, I sequenced work starting from the non-functional requirements customers had flagged as most important in the SLO conversations — so the first wins were immediately visible externally, not just internally.
- I coached engineers by asking probing questions rather than prescribing solutions. When an engineer proposed a caching approach for API endpoints, I worked through the design with them technically and then gave them full ownership of the implementation. My goal was that each solved problem built their confidence, not their dependence on me.
- I ran regular retrospectives to convert incidents into documented learning and explicitly celebrated wins — internally with the team and with customers — to mark the transition from reactive firefighting to proactive ownership.

## Results

- System reliability improved from below 90% to consistently above 99% within 3 months.
- Incident recovery time dropped from 24+ hours to under 1 hour.
- Critical incidents decreased from multiple per week to rare occurrences.
- Customers noticed the improvement within 2 months; one specifically commended the team's transparent communication during the transformation.
- The team shifted from reactive firefighting to proactive issue identification — a measurable change in posture, not just metrics.
- Durable foundations established: automated testing, comprehensive monitoring, and incident response protocols that persisted beyond the immediate turnaround.

## Learnings

- Starting with customer conversations rather than an internal audit was the right call — it gave the team a concrete external anchor rather than internal politics about what mattered most. I'd do this in any future turnaround situation.
- The phased upgrade approach resolved a team confidence problem as much as a technical risk problem. Engineers who were afraid of making things worse needed to see that each step was safe before they could commit to the next. The sequencing was a trust-building mechanism, not just risk management.
- Coaching rather than directing was slower in the short term but produced faster recovery overall — because engineers who own their solutions also own the monitoring, the follow-up, and the learning. A solution I'd prescribed would have fixed one problem; a solution they owned fixed a class of problems.

## Signal Areas

**Primary:** Leadership (took over a team in crisis with no prior context; rebuilt confidence, posture, and capability — not just fixed the immediate technical problem), Ownership (accountable for the full turnaround arc: customer trust, technical reliability, and team health)

**Secondary:** Scope (absorbed a 7-person team in crisis while continuing to run an existing 6-person team — 13 engineers total during the turnaround), Perseverance (sustained execution through continued incidents and team demoralization over several months), Communication (SLO co-definition with customers, transparent progress updates, explicit win celebrations to shift team narrative)

## Related Skills
- [[skills/management/people/Engineering Team Management]]
- [[skills/management/project/Technical Roadmap]]
- [[skills/tech/infra/Kubernetes]]

## Interview Usage
- 适用 BQ：Tell me about a time you took over a struggling team and turned it around
- 适用 BQ：How do you rebuild team morale and confidence after a period of sustained failure?
- 适用 BQ：Give an example of how you balanced short-term stabilization with long-term structural improvement
- 适用 BQ：Tell me about a time you coached someone without prescribing the answer
- 适用 JD 关键词：team leadership, reliability, SRE, incident management, SLO, stakeholder communication, coaching, turnaround

## Key Questions

**Q: How do you stabilize a team that is in crisis when you're new to it?**
Talking points: Start with customer conversations to establish external grounding (shared SLOs) rather than internal debate about what's broken. Narrow focus ruthlessly — two high-leverage initiatives, not ten. Protect the team from new work while they execute. Make progress visible early, externally as well as internally.

**Q: How do you coach engineers who have lost confidence without undermining their ownership?**
Talking points: Ask questions rather than giving answers — guide them toward a robust solution but let them lead. Explicitly hand them ownership of the implementation after the coaching conversation. Recognize wins publicly to reinforce that their judgment is valued. The goal is that each problem they solve builds confidence, not dependence.

**Q: How do you manage the tension between doing an upgrade safely vs. quickly when reliability is already poor?**
Talking points: Phased approach by version, not big-bang. Start in staging to isolate risk. Communicate the phasing plan so the team understands why it's safer — this addresses both technical risk and team confidence. Each version is a decision point, not a commitment to the full upgrade path.

**Q: How do you rebuild customer trust after a major reliability failure?**
Talking points: Co-define SLOs with the customer so success is a shared commitment, not a unilateral promise. Provide transparent progress updates — don't go quiet and hope things improve. Celebrate milestones explicitly with the customer, not just internally.

## Summary

When I took over this cloud infrastructure team, the immediate crisis was technical — a major API server outage and reliability below 90% — but the deeper problem was structural: no shared reliability standards, no incident learning process, and a team so burned by firefighting that they'd stopped trusting their own judgment.

My first move was external: talking to customers to anchor the work in concrete SLOs rather than internal opinions about priorities. From there I narrowed the focus to two initiatives — an API server upgrade and SRE practices — and phased both conservatively to protect a team that couldn't absorb more disruption. The recovery was faster than expected: above 99% reliability within 3 months, sub-hour incident recovery, and a team that was proactively identifying issues rather than reacting to them. The most important judgment call was coaching rather than directing — engineers who owned their solutions also owned the monitoring and the follow-up, making the improvement durable rather than dependent on my continued involvement.

## Raw Material
- [[raw_material/experience/Cloud Infrastructure Team Turnaround]]
