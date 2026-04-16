---
title: eBay - Growing and Managing Engineering Talent
type: Additional
signal_areas: [Leadership, Growth, Ownership]
skills: [people-management, talent-development, performance-management, hiring, engineering-leadership, kubernetes]
company: eBay
date: 2023-09
impact: high
growing_link:
---

# eBay - Growing and Managing Engineering Talent

## Context

After expanding my management scope to include a new team, I inherited a situation with three distinct people challenges running simultaneously. The team was responsible for eBay's Kubernetes cluster upgrade program — 100+ clusters, 10K+ nodes, thousands of applications across multiple environments — and a key senior engineer had just left, creating a leadership vacuum on the project.

The three challenges: a senior engineer with staff potential (Yiran) who could fill that vacuum if developed deliberately; a different senior engineer who had been stalled at the same level for five years and was now blocking a critical workstream; and an open headcount for a customer-facing role where vacancy was degrading customer satisfaction.

## Actions

**Growing high-potential talent:**

- I shared the full scope, urgency, and technical complexity of the K8s upgrade project with the senior engineer (Yiran) and asked her to own the planning rather than prescribing it. She independently decomposed the project into phases and introduced ideas around patch management and multi-environment verification sequencing that hadn't been in the original plan.
- I assembled a supporting team for her, handled stakeholder communication and cross-team dependencies on her behalf so she could focus on execution, and shielded her from blame during incidents — framing retrospectives around resolution rather than attribution.
- I explicitly broadcast her wins to customers and senior leadership to build her credibility externally, not just internally.
- I delegated full technical decision-making to her: execution plan, task breakdown, weekly meeting facilitation, cross-team dependency management.
- I linked the project scope explicitly to Staff Engineer criteria at eBay — strategic thinking, technical influence across teams — and discussed her specific development gaps (cross-team communication, delegating to peers) against those criteria, so she was developing toward a real bar, not a vague standard.
- Yiran proactively sought out communication training on her own initiative. I nominated her for the architecture committee to build her cross-team visibility. I also managed out the low-performing team member (described below) whose execution drag had been directly impacting her project.

**Managing out a low performer:**

- I inherited a senior engineer with five years at eBay, stuck at the same level. He owned the load/performance testing workstream under the new Kubernetes version — a prerequisite for the upgrade to proceed — and was showing slow progress and inability to root-cause metrics drift.
- I established a weekly 1:1 cadence, delivered clear and written feedback on the gap between his output and senior engineer expectations (end-to-end ownership, problem-solving depth, self-directed learning), and gave a formal 2-month improvement window with structured support: a dedicated tech buddy, additional training resources, and a commitment to remove external blockers.
- After several weeks, the pattern was clear: low motivation to learn Kubernetes internals, over-reliance on the buddy without self-effort, and a stated preference for ops-style work over the engineering depth the role required. After the improvement period, I delivered the decision clearly and professionally. He transitioned out within 3 months.

**Hiring:**

- I identified the real need: not a headcount fill, but a customer-focused engineer with end-to-end problem-solving skills, strong coordination instincts, quick learning capacity, and eBay-specific Kubernetes knowledge.
- I targeted sourcing at peer companies (Google, Amazon, Microsoft, VMware, Red Hat) and supplemented with internal referrals. I sold the role on eBay's cloud scale, the growth trajectory, and competitive compensation — and sought VP-level support on comp packages for the right candidate.
- I standardized a structured interview process: behavioral, cloud knowledge, system design, and coding rounds with a panel and group decision-making to reduce individual bias.

## Results

- **Yiran:** In 3 quarters, led the team to successfully upgrade all eBay Kubernetes clusters (100+ clusters, multiple environments, 10K+ nodes). She produced a mature upgrade playbook that reduced future upgrade cycles from 9+ months to 4–5 months. She was promoted to Staff Engineer as a direct result of this project.
- **Low performer:** Managed out professionally; the LNP workstream was reassigned and unblocked. Team morale improved as the persistent performance drag was resolved.
- **Hiring:** Filled the role with a candidate who met all criteria; customer satisfaction stabilized under consistent, high-quality support.

## Learnings

- The right development move for Yiran was to increase her ownership and accountability, not protect her from the project's complexity. High-potential engineers grow faster under real stakes than under managed exposure. The risk I took was calibrated — I provided structural support underneath while giving her full decision authority on top.
- With the low performer, the improvement period was genuinely intended, not a formality before a predetermined outcome. The support was real (tech buddy, training, blocker removal). What became clear was a motivation-fit mismatch, not a skill gap — he preferred ops work over engineering depth, and that preference wasn't going to change with more support. Diagnosing the root cause correctly was what made the decision defensible.
- Career development conversations only work when they're anchored to specific, observable criteria. Telling someone they need to "show more leadership" without connecting it to what Staff Engineer means at eBay produced nothing. Naming the exact gaps against explicit criteria gave Yiran something concrete to develop toward.

## Signal Areas

**Primary:** Leadership (managed the full people spectrum simultaneously — developed a senior engineer to Staff, managed out a chronic low performer, hired for a critical gap — under a high-stakes project with no slack)

**Secondary:** Growth (Yiran's growth from senior to Staff in 3 quarters; the playbook she built reduced future upgrade cycles by half and outlasted the project), Ownership (inherited three distinct people problems and drove each to a clear outcome without deferring or waiting for the situation to resolve itself)

## Related Skills
- [[skills/management/people/Engineering Team Management]]
- [[skills/management/behavior/Coaching and Developing Engineers]]
- [[skills/tech/infra/Kubernetes]]
- [[skills/management/project/Agile and Project Execution]]

## Interview Usage
- 适用 BQ：Tell me about a time you developed a senior engineer into a staff-level role
- 适用 BQ：Describe a situation where you had to manage out a low performer
- 适用 BQ：How do you differentiate your management approach for high-potential vs struggling engineers?
- 适用 BQ：Tell me about a time you had to make a hard people decision
- 适用 BQ：Give me an example of how you've built or hired a high-performing team
- 适用 JD 关键词：people management, talent development, performance management, hiring, coaching, team building, high-potential, staff-level growth

## Key Questions

**Q: Tell me about a time you developed a senior engineer into a staff-level role.**
Talking points: Yiran was a senior engineer with staff potential; a key senior had left and created a vacuum on a high-stakes K8s upgrade project. I gave her full ownership (planning, decisions, meetings, cross-team dependencies), structural support underneath (team, stakeholder cover, no blame on incidents), and explicit career linkage (staff criteria, specific gaps). She proactively sought communication training; I nominated her for the architecture committee to build cross-team visibility. Result: promoted to Staff in 3 quarters, 100+ clusters upgraded, upgrade cycle reduced by half through her playbook.

**Q: Describe how you handle a low performer who isn't improving.**
Talking points: Inherited a 5-year senior stuck at the same level. Set clear written expectations, ran a genuine 2-month improvement window with real support (tech buddy, training, blocker removal). Diagnosed the root cause — motivation-fit mismatch, not skill gap; he preferred ops work, the role required engineering depth. Decisive outcome after the pattern was clear. Emphasize: transparency, support first, decisiveness when support fails and root cause is a fit issue not a skill issue.

**Q: How do you tailor your management approach for different engineers?**
Talking points: High-potential junior required trust + empowerment + career linkage to explicit criteria; low performer required structure + accountability + clear bar + genuine support. Common thread: honest, regular feedback grounded in observable behavior and specific role criteria — the mechanism is the same, the dosage and emphasis differ.

**Q: How do you approach hiring for a technical role?**
Talking points: Define the real need (end-to-end problem-solving, domain knowledge, coordination instincts — not just a headcount fill). Target sourcing at peer companies where those skills already exist. Sell the role authentically. Standardize the interview process with a panel to reduce bias. Seek executive support for competitive comp on the right candidate.

## Summary

This experience spans the full spectrum of people leadership — growing high-potential talent, managing out a chronic low performer, and hiring for a critical gap — all simultaneously under a high-stakes Kubernetes platform project with no slack for mistakes.

The core leadership judgment with Yiran was that her growth required more ownership and accountability, not protection from complexity. I provided structural support underneath (team, stakeholder cover, career linkage to explicit criteria) while giving her full decision authority on top. The result — Staff Engineer promotion in 3 quarters, a reusable upgrade playbook that cut future cycle time in half — validated that approach. The parallel low-performer case required the complementary discipline: clear expectations, genuine support, and decisive action once the pattern was clear and the root cause was a fit issue rather than a skill gap. Both outcomes rested on the same foundation: honest, regular feedback anchored to observable behavior and explicit role criteria.

## Raw Material
- [[raw_material/experience/People Management]]
