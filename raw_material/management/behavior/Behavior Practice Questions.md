---
title: Behavior Practice Questions
source:
date_saved: 2026-04-19
processed: false
skill_note:
---

# Behavior Practice Questions

---

## Practice Script #1

**Tell me about yourself.**
→ Use prepared TMAY from `experience/big3question.md`. 60–90 sec. Personal summary → 3 accomplishments → forward-looking.

---

**Tell me about the largest scoped project you've ever built.**
Story: **Cloud Migration to Kubernetes**

- S: 5,000+ eBay apps on legacy VM CI/CD; deployment bottlenecks degrading productivity and reliability at scale.
- A: Proposed US/China ownership split at interface level (not component) to enable parallel execution. 5-phase blueprint with rollback gates at every phase. Batched apps by complexity type.
- R: All 5,000 apps migrated on time. Deployment duration reduced 75%. Zero major service disruptions.

---

**Tell me about a time when you had to solve a complex technical problem.**
Story: **CI/CD Platform Architecture and Reliability**

- S: ECD infrastructure causing K8s API server overload and node exhaustion during deployments. Cloud Control Plane lacked progressive rollout — any bad change propagated instantly across the fleet.
- A: Built Federated Deployment Controller with progressive rollout and AI health-gated rollback. Applied APF tuning and dedicated CI/CD node pools to isolate ECD load from production traffic.
- R: Controller adopted by ECD org-wide. CI/CD-induced API server incidents eliminated. DORA metrics established as org-wide framework.

---

**Tell me about a time you did something impactful that was not assigned to you.**
Story: **AI Innovation**

- S: Across eBay, AI tools were used individually and ad hoc. Nobody asked me to change this on my team.
- A: Identified highest-leverage pain points (hiring pipeline slow, development quality/speed tension, operations toil). Ran pilots myself — hiring skills, spec-driven dev, MCP server + triage agents — on real work before proposing anything. Structurally embedded tools so adoption wasn't optional.
- R: PR volume doubled. Monthly incidents dropped 50%+. 70% of customer support cases autonomous. Spec-driven adopted across 50+ projects.
- Close: "Leading by example on real work first — team moved when they saw me using tools daily, not on a demo."

---

**Share an example of when you had to adapt to a requirement that changed quickly.**
Story: **DoJ and Jade Programs**

- S: DoJ compliance program had hard deadline (3 months). Definition of "covered person access" kept shifting; each scope change had large architectural implications. Requirements were not stable when design decisions had to be made.
- A: Three principles simultaneously: (1) document assumptions explicitly rather than waiting for certainty, (2) design environments to be adjustable as scope shifted, (3) use rehearsal rounds as forcing function — each rehearsal required legal/compliance to commit to specific definitions in order to proceed.
- R: All Cloud Fleet workstreams on schedule. Zero critical incidents in the 2-week execution window. Automated namespace transfer adopted as model by other teams.
- Key line: "Ambiguity with a hard deadline means you can't wait for clarity — you move with documented assumptions and create forcing functions that accelerate the decision."

---

**Tell me a time when you disagreed with your manager or another leader.**
→ Use prepared **L7 Traffic Gap** story from `experience/big3question.md`.

---

**Tell me about a time when you failed.**
Story: **Engineering Velocity Program — the bilateral mistake**

- S: CD and security teams were at an impasse. I owned cross-team coordination.
- Failure: Spent several weeks trying to resolve it through bilateral 1:1s — separate conversations with each team. Slow, no movement.
- What changed: Brought phased proposal + quantified data (5% vs 95%) to the full working group. Resolved in one session.
- Learning: For cross-team disagreements, the group forum is nearly always more productive than bilateral mediation. The dynamic that makes 1:1s comfortable (no audience) is also what lets parties dig in. Now the group forum is my default for any cross-team conflict that can't resolve in two bilateral conversations.

---

**Tell me about when you went above and beyond the requirements.**
Story: **Engineering Velocity Program (cross-team accountability)**

- S: Formal scope was Cloud Application Lifecycle Management — my team's infrastructure changes.
- Beyond: Ran the deployment-metrics analysis that identified actual bottlenecks. Built the phased proposal that broke the CD/security impasse. Served as cross-team accountability point across 15+ teams. None of that was in my job description.
- R: 20% reduction in 95th-percentile deployment time. Leadership recognized the cross-team coordination explicitly.

---

**What questions do you have for me?**
→ Use prepared questions from `experience/big3question.md`, matched to interviewer type.

---

## Practice Script #2

**Tell me about yourself.**
→ TMAY (as prepared).

---

**Why are you interested in this role?**

> "I've spent 20+ years building platform infrastructure at scale — Kubernetes, SRE, CI/CD — and the last two years actively building AI-native engineering practices into how my team operates. The intersection of AI infrastructure and AI-augmented engineering is where I want to spend the next decade, and this role sits directly at that intersection. [Add one specific thing from the JD or company context.]"

Always close with something specific to the company — shows preparation.

---

**Tell me about the project you're most proud of.**
→ Use prepared **Engineering Velocity Program** story from `experience/big3question.md`. Use the four-theme signpost structure.

---

**Share an example of when you saw an opportunity that others missed and took action on it.**
Story: **AI Innovation** — add the "others missed it" frame explicitly:

> "Most teams were using AI tools individually, ad hoc. I saw that the real opportunity wasn't any individual tool — it was systematically rebuilding team workflows across hiring, development, and operations. Nobody asked me to do this…"

Results: PR volume doubled, incidents 50%+, 70% support automation, spec-driven adopted across 50+ projects.

---

**Tell me about a time when you had to get something from someone who didn't want to give it to you.**
Story: **Resolving L7 Traffic Gap** (frame as persuasion, not conflict)

- What I needed: Manager's buy-in to build a specialized L7 solution rather than extend the existing AZ rebalance system.
- Why he resisted: He had committed efficiency targets upstream — additional build scope was a real constraint, not obstruction.
- How I got it: Reframed from "who is right" to "how do we satisfy both constraints." Met with network team; found their existing L7 tool. Brought back a two-phase design that honored his efficiency constraint and addressed the L7 gap. He agreed because his constraint was central to the solution.
- R: Two-phase workflow in 1 month. L7 AZ ramp-up reduced to 1 day. Utilization held at 40–80%.

---

**Tell me about a time when you were faced with a problem with many possible solutions. How did you approach it?**
Story: **Cloud Migration to Kubernetes**

- Problem: 5,000 apps to migrate. Multiple approaches: big-bang, team-by-team, region-first, complexity-first.
- Approach: Started with bottleneck analysis. Chose interface-level ownership splits (not component-level) to avoid constant coordination. Built 5-phase blueprint with rollback gates so program could stop safely at any point. Batched by app complexity so learning from each batch informed the next.
- R: All 5,000 migrated on time, 75% deployment duration reduction, zero major disruptions.
- Key line: "The goal was to make the most common paths fast, rollback paths safe, and ownership boundaries clear — all three had to be true for parallel teams to move without constant coordination."

---

**Tell me about a time when you were misunderstood.**
Story: **Embracing a New Leadership Challenge**

- S: When I took over the cloud fleet team after 10 years in a different domain, engineers initially assumed I'd pretend to know their systems and give confident-sounding bad advice.
- How it showed: Engineers were guarded in technical discussions, hedging answers, not pushing back.
- What I did: Was explicit about what I didn't know. Asked questions rather than asserting answers. Started from customer SLOs rather than my own technical assumptions. Dynamic shifted once it was clear I wasn't competing with them technically.
- R: Team shifted from guarded to engaged. Reliability <90% → 99%+ in 3 months. Customer thank-you emails within 2 months.
- Key line: "The misunderstanding was that 'manager' meant 'technical authority.' Once I made it clear I was there to create conditions, not supply the answers, the team's own expertise came forward."

---

**Tell me about a time when a project was behind and how you responded.**
Story: **Automated Cluster Management Overhaul**

- S: Cluster build timeline slipping — dependency on capacity team's API contract unresolved, blocking build automation progress.
- Response: Sequenced decommissioning first — clearer ROI, no external dependencies, could ship immediately. Delivered decommission early (weeks → days). Then negotiated capacity team timeline explicitly with the early win as credibility. Cluster build subsequently hit 1-week target.
- R: Decommission reduced weeks → days. Build hit 1-week target. Capacity team self-service achieved. Roadmap endorsed by leadership.
- Key line: "When a hard dependency is blocking you, find what you can ship independently first — early wins buy credibility and time to unblock the dependency properly."

---

**Tell me about a time when you learned something.**
Story: **Embracing a New Leadership Challenge**

- S: Took over a team in crisis in an unfamiliar technical domain.
- Learning: Not having domain expertise forced me to use the right leadership levers — customer conversations, borrowed SRE frameworks, structured SLOs — rather than substituting my own technical opinions for management judgment. The unfamiliarity made me a better manager of this team than deep technical confidence would have.
- Durable lesson: The retrospective culture shift took longer than the reliability improvement and was more durable. Technical fixes revert; a team that treats incidents as learning inputs doesn't.

---

**What questions do you have for me?**
→ Use prepared questions from `experience/big3question.md`, matched to interviewer type.

---

## Practice Script #3

**Tell me about yourself.**
→ TMAY (as prepared).

---

**Tell me about the project where you've had the largest business impact.**
Story: **Cloud Migration to Kubernetes**

- Impact framing: 5,000 apps on time, 75% reduction in deployment duration, zero major disruptions — directly unblocked eBay developer velocity and site reliability at scale.
- Why it was hard: Interface-level vs. component-level ownership split was the critical decision. Getting it wrong would have required constant cross-team coordination and killed parallel execution.

*If JD emphasizes compliance or program management, swap to DoJ — same XL scope, different impact vector.*

---

**Tell me about when you've demonstrated leadership.**
Story: **Global Team Expansion**

- S: US team was sole 24/7 on-call after China lost production access. Needed Europe + India coverage in 3 months. No process, no documentation site, no hiring pipeline.
- A: Built AI-assisted hiring workflow covering full recruitment lifecycle. Stood up documentation site to force implicit knowledge into explicit form. Set explicit 3-month production-readiness criteria so "ramped" had a specific definition.
- R: 8+ engineers hired across 2 regions in 3 months. Europe team independently on-call. Hiring workflow adopted org-wide.
- Key line: "The documentation site was the highest-leverage investment — it forced the team to make implicit knowledge explicit, which is what made a 3-month ramp actually achievable."

---

**Tell me about a time when you were involved in a conflict at work.**
→ Use prepared **L7 Traffic Gap** story from `experience/big3question.md`.

---

**Tell me about how you handled a project that was very ambiguous.**
Story: **DoJ and Jade Programs**

- Ambiguity: "Covered person access" was actively debated throughout. Each definition change had large architectural implications. Requirements were not stable when design decisions had to be made.
- How I handled: (1) Documented assumptions explicitly rather than waiting for clarity. (2) Designed environments to be adjustable. (3) Used rehearsal rounds as forcing function — required compliance/legal to commit to specific definitions in order to proceed.
- R: All workstreams on schedule. Zero critical incidents in 2-week execution window.

---

**Can you describe an instance where you proactively prepared for a potential issue before it became a problem?**
Story: **SRE Practice Implementation and API Server Reliability**

- S: After inheriting the cloud fleet team, the API server had no SLOs, no runbooks, and no structured on-call. Previous 2-day outage had happened with no early-warning system.
- Proactive actions: Implemented graduated SLOs (starting at 99%, escalating toward 99.9%), error budget policy, PagerDuty alerting, and blameless postmortems — before the next major incident, not in response to one.
- The test: When a compliance-driven team change forced a significant on-call rotation shift, the structured SRE infrastructure allowed the new rotation to hold without disruption.
- R: Availability stable at 99.9%. MTTD ~20 minutes. MTTR <1 hour.

---

**Tell me about a time when you balanced planning with rapid execution.**
Story: **DoJ and Jade Programs**

- Planning: 3-month program with weekly rehearsal rounds, daily-updated runbooks, three parallel tracks (Technical / Process / People).
- Rapid execution: Actual provisioning and cutover in a 2-week window once hardware was ready. Planning investment meant the team could move fast without improvising.
- The balance: Didn't wait for perfect requirements (would have missed deadline). Didn't execute without preparation (would have failed quality bar). Rehearsal rounds were the bridge — they forced requirement decisions while building execution muscle simultaneously.

---

**How did you communicate something technical to someone non-technical?**
Story: **Engineering Velocity Program**

- Technical problem: Security policy initialization during pod startup causing CD pipeline delays. CD and security teams in a technical argument about whose timeline governed.
- Translation: Reframed it for the working group as one quantified fact: "Only 5% of applications have large or complex security policies. 95% can be optimized immediately." That turned a technical debate into an obvious sequencing decision.
- R: Non-technical stakeholders reached consensus in one session. Phased plan approved without further debate.
- Key line: "The translation wasn't simplifying the engineering — it was finding the number that made the decision obvious regardless of technical background."

---

**Tell me about recent constructive feedback you've been given by your manager.**

Frame as internalized behavioral feedback from the Engineering Velocity learning:

> "The pattern I've been working on is defaulting to bilateral 1:1s when I should bring cross-team issues to a working group faster. In the Engineering Velocity program, I spent several weeks trying to mediate the CD/security impasse through separate conversations with each team. When I brought it to the full working group with the quantified data, it resolved in one session. The feedback — and my own retrospective — was that I'd earned each team's trust individually but held back the forum where that trust could produce a decision. Since then, the working group is my default for any cross-team disagreement that can't resolve in two bilateral conversations."

---

**What questions do you have for me?**
→ Use prepared questions from `experience/big3question.md`, matched to interviewer type.

---

## Quick Reference: Story → Question Mapping

| Question Signal | Primary Story | Backup |
|---|---|---|
| TMAY | big3question.md | — |
| Largest scope | Cloud Migration to K8s | DoJ & Jade |
| Complex technical problem | CI/CD Platform Architecture | Platform Eng at Scale |
| Not assigned / initiative | AI Innovation | AI-Augmented EM |
| Adapting to changing requirements | DoJ & Jade | Cloud Migration |
| Disagreement with manager | L7 Traffic Gap | — |
| Failure | Engineering Velocity (bilateral mistake) | DoJ (manual risk scoring) |
| Above and beyond | Engineering Velocity (cross-team accountability) | AI Innovation |
| Why this role | TMAY forward-looking + JD hook | — |
| Favorite / proudest project | Engineering Velocity | CI/CD Platform |
| Opportunity others missed | AI Innovation | — |
| Getting something from resistant party | L7 Traffic Gap | Engineering Velocity |
| Many possible solutions | Cloud Migration | Automated Cluster Mgmt |
| Misunderstood | Embracing New Leadership | Engineering Velocity |
| Project behind | Automated Cluster Mgmt | DoJ & Jade |
| Learning moment | Embracing New Leadership | AI Innovation |
| Largest business impact | Cloud Migration | DoJ & Jade |
| Leadership demonstration | Global Team Expansion | Growing & Managing Talent |
| Conflict | L7 Traffic Gap | Engineering Velocity |
| Ambiguous project | DoJ & Jade | Embracing New Leadership |
| Proactive preparation | SRE Practice Implementation | CI/CD Platform |
| Planning vs rapid execution | DoJ & Jade | Cloud Migration |
| Technical to non-technical | Engineering Velocity | Cloud Infra Turnaround |
| Constructive feedback | Engineering Velocity learning | AI Innovation baseline |
