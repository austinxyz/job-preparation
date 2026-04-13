---
title: eBay - Growing and Managing Engineering Talent
type: experience
skills: [people-management, talent-development, performance-management, hiring, engineering-leadership, kubernetes]
company: eBay
date: 2023-09
impact: high
growing_link:
---

# eBay - Growing and Managing Engineering Talent

## Situation

After expanding my management scope to include a new team, I inherited an engineering team with mixed performance: one high-potential junior engineer, one underperforming senior engineer, and an open headcount for a critical customer-facing role. The team was responsible for eBay's Kubernetes cluster upgrade program — a complex, high-stakes project affecting 100+ clusters, 10K+ nodes, and thousands of applications across multiple environments. A key senior engineer had recently left, creating a leadership vacuum on the project.

## Task

I was accountable for three distinct people challenges simultaneously:
1. Identify and grow a junior engineer into a technical lead role for the K8s upgrade project
2. Manage a senior engineer who had stalled on performance for years and was now blocking a critical workstream
3. Hire a Solutions/Customer Support Engineer to stabilize customer satisfaction, which had degraded under an inconsistent rotation model

## Action

**Growing high-potential talent (Yiran):**

- **Trust**: Shared the full scope, urgency, and technical complexity of the K8s upgrade project with Yiran. Instead of prescribing a plan, asked her to own the planning — she independently decomposed it into phases and introduced new ideas around patch management and multi-environment verification sequencing.
- **Supportive**: Assembled a supporting team of developers for her; handled communication with stakeholders and dependent teams on her behalf. During incidents, shielded her from blame and focused the team on resolution first, retrospective second. Broadcast her wins explicitly to customers and senior leadership to build her credibility.
- **Empower**: Delegated full technical decision-making authority to her — execution plan, task breakdown, weekly meeting facilitation, and cross-team dependency management.
- **Strategic thinking**: Encouraged her to think beyond the current upgrade cycle — to frame the project as a platform product with a repeatable upgrade playbook, not a one-time migration.
- **Career development**: Explicitly linked the project scope to staff engineer criteria at eBay (strategic thinking, technical influence across teams) and discussed her specific gaps (cross-team communication, delegation to peers) so she could develop against real criteria.
- Provided communication training, sponsored her to join the architecture committee, and replaced a low-performing team member who was creating execution drag.

**Managing out a low performer:**

- Inherited a senior engineer with 5 years at eBay, stuck at the same level. He was responsible for LNP (load/performance) testing under the new K8s version — a prerequisite for the upgrade to proceed — but showed slow progress and could not identify root causes of metrics drift.
- Set up weekly 1:1 cadence, delivered clear and written feedback on the gap between his output and senior engineer expectations (end-to-end ownership, problem-solving depth, self-directed learning).
- Gave a formal 2-month improvement window with structured support: a dedicated tech buddy, additional training resources, and a promise to remove external blockers.
- After several weeks, the pattern was clear: low motivation to learn new K8s internals, over-reliance on the buddy without sufficient self-effort, and a stated preference for ops-style work over the engineering depth the role required.
- After the performance improvement period, delivered the decision clearly and professionally. He transitioned out of eBay within 3 months.

**Hiring (Senthil case):**

- Identified the real need: not just a headcount fill, but a customer-focused engineer with end-to-end problem-solving skills, strong coordination instincts, quick learning capacity, and eBay-specific K8s knowledge.
- Targeted sourcing at peer companies (Google, Amazon, Microsoft, VMware, Red Hat) and supplemented with internal referrals.
- Sold the role on eBay's cloud scale/maturity, the position's growth trajectory, and competitive compensation — sought VP-level support on comp packages for the right candidate.
- Standardized a structured interview process: behavioral, cloud knowledge, system design, and coding (data structures and algorithms), with an interview panel and group decision-making to reduce bias.

## Result

- **Yiran**: In 3 quarters, led the team to successfully upgrade all eBay Kubernetes clusters (100+ clusters, multiple environments, 10K+ nodes) to a new version. Her technical and leadership skills advanced substantially. She produced a mature, productized upgrade playbook that reduced future upgrade cycles from 9+ months to 4–5 months. She was promoted to Staff Engineer as a direct result of this project.
- **Low performer**: Managed out professionally; project was unblocked by reassigning the LNP workstream. Team morale improved as the persistent performance drag was resolved.
- **Hiring (Senthil)**: Filled the open role with a candidate who met all criteria; customer satisfaction stabilized under consistent, high-quality support.

## Related Skills

- [[skills/management/people/Engineering Team Management]]
- [[skills/management/behavior/Coaching and Developing Engineers]]
- [[skills/tech/infra/Kubernetes]]
- [[skills/management/project/Agile and Project Execution]]

## Interview Usage

- **适用 BQ：**
  - "Tell me about a time you developed a junior engineer into a senior or lead role"
  - "Describe a situation where you had to manage out a low performer"
  - "How do you differentiate your management approach for high-potential vs struggling engineers?"
  - "Tell me about a time you had to make a hard people decision"
  - "Give me an example of how you've built or hired a high-performing team"

- **适用 JD 关键词：**
  - people management, talent development, motivate and retain, grow engineering talent, performance management, hiring, manager of managers, coaching, team building, high-potential, staff-level growth

## Key Questions

**Q: Tell me about a time you developed a junior engineer into a lead role.**
Talking points: Context — key person left, Yiran was junior but high-potential, project was high-stakes K8s upgrade. What I did: gave her full ownership (plan, decisions, meetings), structured support (team, stakeholder cover, no blame on incidents), career linkage (staff criteria). Result: promoted to Staff in 3 quarters, 100+ clusters upgraded, created reusable playbook.

**Q: Describe how you handle a low performer who isn't improving.**
Talking points: Inherit situation (5-year senior stuck at level), set clear expectations in writing, 2-month formal improvement window with real support (buddy, training, blocker removal), diagnosed root cause (ops orientation, low motivation to learn), decisive outcome after pattern was clear. Emphasize: transparency, support first, decisiveness when support fails.

**Q: How do you tailor your management style to different engineers?**
Talking points: Case-by-case — Yiran (high-potential junior) required trust + empowerment + career linkage; low performer required structure + accountability + clear bar. Common thread: clear expectations, regular 1:1 feedback, and matching support to the actual gap.

**Q: How do you approach hiring for a technical role?**
Talking points: Start with real needs (not just headcount), skills gap analysis, targeted sourcing at peer companies, structured interview process with panel, sell the role authentically (scale, growth, comp), seek executive support for competitive packages.

**Q: Tell me about a time you had to make a hard decision about someone on your team.**
Talking points: Low performer case — chose to manage out after transparent improvement period. Why hard: 5-year tenure, genuine support provided. Why right: pattern was clear (motivation-fit mismatch), team impact of continued underperformance, project risk. Outcome: professional transition, team unblocked.

## Summary

This experience demonstrates managing the full spectrum of people leadership: growing high-potential talent, managing out a chronic low performer, and hiring for a critical gap — all simultaneously on a high-stakes K8s platform project.

The core leadership judgment was recognizing that Yiran had the potential to grow into a tech lead role precisely because of the project's complexity, not despite it. Rather than protecting her from risk, I increased her ownership and accountability while providing structured support underneath. The result — Staff Engineer promotion and a reusable upgrade platform — validated the bet. The parallel low-performer case illustrates the complementary discipline: clear expectations, genuine support, and decisive action when the pattern is clear. Both outcomes required the same foundational practice: honest, regular feedback grounded in observable behavior and explicit role criteria.

## Raw Material

- [[raw_material/experience/People Management]]
