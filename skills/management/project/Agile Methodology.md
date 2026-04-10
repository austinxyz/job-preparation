---
title: Agile Methodology
category: management/project
tags: [agile, scrum, kanban, sprint, retrospective, velocity, backlog, tdd, ai-development, iteration]
status: in-progress
priority: medium
last_updated: 2026-04-09
created_from_jd: "[[positions/Manager, DevOps Engineering - NVIDIA]]"
---

# Agile Methodology

## Knowledge Map
- 前置知识：software development lifecycle, project management basics
- 延伸话题：SAFe (Scaled Agile), Scrum@Scale, OKR integration with Agile, TDD, CI/CD Pipeline Engineering
- 管理关联：sprint planning, team cadence, stakeholder communication, roadmap alignment, Developer Productivity and DORA Metrics

## Core Concepts

**The Agile Manifesto — 4 values**
- **Individuals and interactions** over processes and tools
- **Working software** over comprehensive documentation
- **Customer collaboration** over contract negotiation
- **Responding to change** over following a plan
- The right side has value; the left side is valued *more*. Understanding the nuance (when to apply each) separates experienced practitioners from rule-followers.

**The 12 Agile Principles** *(agilemanifesto.org — verbatim)*
1. Satisfy the customer through **early and continuous delivery** of valuable software.
2. **Welcome changing requirements, even late** in development — harness change for customer's competitive advantage.
3. **Deliver working software frequently**, preference for shorter timescales (weeks, not months).
4. **Business and developers work together daily** throughout the project.
5. Build projects around **motivated individuals** — give them environment, support, and trust.
6. **Face-to-face conversation** is the most efficient communication method.
7. **Working software is the primary measure of progress**.
8. Agile promotes **sustainable development** — sponsors, developers, users maintain a constant pace indefinitely.
9. **Continuous attention to technical excellence** and good design enhances agility.
10. **Simplicity** — the art of maximizing the amount of work not done — is essential.
11. The best architectures, requirements, and designs emerge from **self-organizing teams**.
12. At regular intervals, the team **reflects on how to become more effective**, then tunes and adjusts.

Interview relevance: principles 2 (change welcome), 7 (working software), 9 (technical excellence), 10 (simplicity), 12 (retrospection) come up most often. Know the tension between them: principle 9 (technical excellence) directly conflicts with teams that skip refactoring for speed.

**Scrum framework**
- Work organized in **sprints** (1–4 weeks, fixed length). Within a sprint: planning → daily standups → review → retrospective.
- Three roles: **Product Owner** (prioritizes backlog, owns "what"), **Scrum Master** (removes impediments, owns "how the process runs"), **Dev Team** (owns "how to build").
- Key artifacts: **product backlog** (all work, prioritized), **sprint backlog** (committed work this sprint), **increment** (potentially shippable product at sprint end).
- Velocity = story points completed per sprint; use as a forecasting tool, not a performance metric. Gaming velocity destroys its predictive value.

**Scrum ceremonies in detail**
- **Sprint Planning**: team pulls from prioritized backlog; commits to a sprint goal; breaks stories into tasks. Output: sprint backlog with a clear goal.
- **Daily Standup** (15 min): each person answers "what did I do yesterday, what am I doing today, any blockers?" Anti-pattern: status report to the manager. Purpose: team self-coordination and blocker surfacing — not status reporting upward.
- **Sprint Review**: demonstrate working software to stakeholders; get feedback that feeds next sprint's backlog. Not a rubber-stamp; actual product decisions should come out of it.
- **Sprint Retrospective**: process improvement (not product). What went well, what didn't, what to try. Output: 1–3 actionable items with owners. Anti-pattern: observations without action items.
- **Backlog Refinement** (ongoing): break large epics into stories; add acceptance criteria; estimate; deprioritize stale items. Teams that skip refinement arrive at sprint planning unprepared.

**Definition of Done vs. Definition of Ready**
- **Definition of Done (DoD)**: shared team agreement on what "done" means for any story — e.g., code written + reviewed + tested + deployed to staging + monitoring in place + runbook updated. Without a DoD, "done" means different things to different people → rework at demos.
- **Definition of Ready (DoR)**: criteria a story must meet before being pulled into a sprint — e.g., acceptance criteria written, design reviewed, dependencies identified. Prevents mid-sprint blocking.
- For infra/platform teams: DoD should always include operational readiness (monitoring, alerting, runbook) — not just code merged.

**Kanban**
- Flow-based, no fixed sprint cadence. Work items pulled when capacity exists; no push.
- Core practice: **WIP (Work in Progress) limits** — cap the number of items in each column. Forces finishing work before starting new work; surfaces bottlenecks immediately.
- WIP limit sizing: rule of thumb is **2/3 to 3/4 of team size** per stage. Too high = no constraint benefit; too low = team blocked waiting. Adjust empirically.
- **Little's Law** (foundational): `Lead Time = WIP ÷ Throughput`. Reducing WIP directly reduces lead time — the math is unambiguous. This is why WIP limits work.
- Key metrics: **cycle time** (card start → done), **lead time** (request → done), **throughput** (cards completed per week). Better predictability signals than velocity.
- **Cumulative Flow Diagram (CFD)**: visual representation of how many items are in each stage over time. Widening bands = WIP growing = throughput problem. Flat bands = healthy flow.
- **Classes of service**: not all work is equal. Expedite (production incidents), fixed-date (compliance deadlines), standard (normal work), intangible (tech debt). Explicit classes prevent hidden prioritization and "everything is urgent" syndrome.
- When to use Kanban over Scrum: ops/support teams with unpredictable inflow, continuous deployment workflows, platform teams maintaining running systems (vs. feature delivery teams).

**Agile for infrastructure and platform teams**
- Classic Scrum friction: infrastructure work doesn't decompose cleanly into 2-week user stories. "Upgrade Kubernetes to 1.29" doesn't fit the same backlog model as "add checkout button."
- Adaptations that work: **tech-lead-owned epics** with sub-tasks in sprints; **20% slack sprint capacity** for reactive/unplanned work; **definition of done** that includes runbook, monitoring, and rollback tested — not just "deployed."
- SRE/ops angle: treat incident response as unplanned work in the backlog; track it explicitly. If >20% of sprint capacity is reactive, it's a signal to invest in reliability, not to increase sprint capacity.

**Agile at scale**
- SAFe (Scaled Agile Framework): organize multiple teams into **Agile Release Trains (ARTs)**; synchronize via **PI Planning** (Program Increment, ~10-week cadence). Good for large orgs needing alignment; criticized for heavyweight ceremonies.
- OKR integration: Objectives (quarter-level strategic goals) → Key Results (measurable outcomes) → Epics/features in sprint backlog. OKRs answer "why are we doing this sprint?"; sprints answer "what are we delivering this week?"
- Calibration problem at scale: "done" means different things across teams. Solve with explicit shared definition of done and cross-team retrospectives.

**Scaling framework comparison**

| Framework | Best fit | Scale | Core mechanism | Criticism |
|-----------|----------|-------|----------------|-----------|
| **SAFe** | Large enterprise (50–125+ people), regulated industries, heavy cross-team dependencies | 4–12 teams per ART | PI Planning (~10 weeks), ART synchronization, portfolio Kanban for strategic alignment | Heavyweight ceremonies; can recreate waterfall at the program level; requires a SAFe coach to set up correctly |
| **LeSS** (Large-Scale Scrum) | 2–8 teams, orgs wanting minimalist overhead, product-centric structure | 2–8 teams (LeSS Huge for 8+) | Single product backlog, one Product Owner, teams work from the same backlog, shared sprint review | Requires deep org redesign (eliminate middle management layers); hard to adopt incrementally |
| **Scrum@Scale** | Flexible scaling, orgs already running Scrum who want to coordinate | No prescribed size cap | "Scrum of Scrums" (coordination across teams) + "MetaScrum" (product alignment); nested Scrum cycles | Less prescriptive — teams must design their own scaling topology; can produce inconsistent results |
| **Nexus** | 3–9 teams building a single product | 3–9 teams | Nexus Integration Team owns cross-team dependency resolution; shared sprint; combined increment | Narrows to single-product use; less adopted than SAFe/LeSS |

Interview heuristic: SAFe = top-down alignment at scale with high ceremony cost; LeSS = radical simplification with org redesign cost; Scrum@Scale = flexible but under-specified. No framework is neutral — choice reflects the org's appetite for prescription vs. autonomy.

**Common Agile anti-patterns**
- **Zombie Scrum**: ceremonies are held but produce no value. Stand-ups are status reports; retros produce no action items; sprint reviews are demos nobody acts on. Teams are going through the motions without the Manifesto's spirit.
- **Velocity gaming**: teams inflate story points to appear faster. Velocity becomes a management metric rather than a forecasting tool; teams estimate to the metric, not to the work. Diagnostic: if velocity goes up but delivery doesn't, it's gaming.
- **Mini-waterfall sprints**: sprints nominally exist but work still flows through sequential phases (design → dev → QA → deploy) that span multiple sprints. The integration and feedback loop is just as slow as waterfall. Fix: cross-functional teams where design, dev, and QA work within the same sprint.
- **Sprint 0 forever**: teams use Sprint 0 (setup/architecture sprint) as a delay mechanism, adding stories to it indefinitely. Real work never starts. Fix: time-box Sprint 0 strictly; start delivering thin end-to-end slices in Sprint 1.
- **Dark Scrum**: Scrum used as micromanagement — daily standups become status reports to management; sprint commitments become contracts; estimates become deadlines. Psychological safety collapses; engineers under-estimate to avoid punishment, creating a self-reinforcing dysfunction.
- **Hero culture**: one engineer handles every production issue, unblocking the team — but creating a single point of failure and burning out the hero. Anti-pattern in Agile: the team should own reliability collectively, not delegate it to a hero.
- **Backlog black hole**: items enter the backlog and are never refined, never prioritized, never removed. The backlog grows to hundreds of items; refinement sessions become overwhelming. Fix: explicit pruning policy — items not refined in 60 days are archived; active backlog is capped at ~2 sprints of work.

**Technical Agile practices**
- **Continuous Integration (CI)**: every developer integrates code to a shared branch at least daily; automated build and tests run on each commit. Prevents "integration hell" at end of sprint. The foundation of short feedback loops.
- **Continuous Delivery (CD)**: software is always in a deployable state. Separates deployment cadence from development cadence — you can deploy whenever product decides, not just at sprint end. Requires feature flags, automated testing, and deployment pipelines.
- **Pair programming**: two developers work on the same code simultaneously — one drives, one reviews in real-time. Benefits: fewer defects, knowledge transfer, continuous code review. Common objection: costs 2 dev-days per feature. Counter: studies show 15% slower writing, but significantly lower rework and defect rate — usually net-positive for complex features.
- **Collective code ownership**: no engineer "owns" a module. Anyone can improve any code. Prevents knowledge silos and bus-factor risk. Requires: shared coding standards, code review culture, and enough test coverage that change is safe.
- **Sustainable pace** (Agile Principle 8): teams that sprint at 100% capacity indefinitely produce technical debt, burnout, and eventually slower delivery. The Agile answer is not "work harder" — it is to scope down, protect the team, and maintain the ~20% slack buffer.

**TDD (Test-Driven Development) as Agile's verification backbone**
- Write failing test → implement to pass → refactor. Ensures working software at every increment; makes "done" unambiguous.
- In AI-augmented development (blog insight): TDD becomes the **closing loop** mechanism. AI can run failing tests and self-correct iteratively. Without tests, reviewing AI-generated code requires slow human reading. With tests, evaluation becomes tractable: "does this pass?"
- At team level: enforce a "no PR without tests" standard; track test coverage as a team metric, not an individual one.

**Small iterations and calibrating granularity**
- Traditional Agile: 2-week sprints. In AI-native development (blog insight): the useful unit shrinks further. Rule of thumb: if a task takes > 5 minutes for AI to complete, it should be broken down.
- Rationale: long AI sessions accumulate drift — context window limitations cause models to forget earlier architectural decisions. Shorter tasks maintain higher coherence and enable faster human review.
- Applies to teams too: large stories that "span the sprint" are a signal of insufficient decomposition. Break until each task has a clear done state achievable in 1–2 days.

**Retrospectives — continuous improvement in practice**
- What went well / what didn't / what to try next. Run every sprint; focus on process, not blame.
- Effective retros produce **1–3 concrete action items** with owners — not just observations. Retros without follow-through erode trust in the process.
- Blameless culture is prerequisite: if engineers fear naming failures, retros produce surface-level observations. Connect to SRE's blameless postmortem culture.
- In AI workflows (blog insight): lessons should be captured in structured files (architecture decision records, project principles) so they compound across sessions rather than repeating.

**The development bottleneck shift — AI era reframing** *(blog insight)*
- Previously: writing code was the bottleneck → Agile managed human execution speed and coordination.
- Now: **"knowing what to build and verifying correctness"** is the bottleneck → Agile manages judgment, coherence, and verification.
- Key implication for managers: don't measure team productivity by code volume generated. Measure by working, verified, maintainable software delivered. The judgment problems (what to build, when to refactor, how to verify) are exactly what good Agile practice develops.
- **Documentation discipline**: AI generates docs prolifically; the risk is documentation inflation — specs and plans that drift from the code. Discipline: documentation should be minimal, structural, and auto-synced where possible. Working software is truth; documentation is scaffolding.

## Key Questions

**Q: How do you implement Agile on a platform or infrastructure team where work doesn't fit the classic user-story model?**
Answer framework: Acknowledge the friction upfront (infra work is less decomposable than feature work). Describe adaptations: tech-lead-owned epics with sprint sub-tasks; explicit 20% unplanned capacity buffer; definition of done that includes operational readiness (runbook, monitoring, rollback). Track reactive work in the backlog — if it exceeds 20% of capacity, that's a reliability investment signal, not a sprint planning problem.

**Q: What's the difference between Scrum velocity and Kanban cycle time, and when do you use each?**
Answer framework: Velocity = story points per sprint (Scrum); useful for sprint forecasting but easy to game and meaningless across teams. Cycle time = card start to done (Kanban); harder to game, more useful for predictability and SLA discussions. Use Scrum/velocity for feature delivery teams with regular cadence; Kanban/cycle time for ops/platform teams with variable inflow. State which you use and why — don't just define them.

**Q: How do you run retrospectives that actually produce change?**
Answer framework: Describe what makes retros fail (no psychological safety → surface observations; no follow-through → engineers stop caring). State your format and its purpose. Emphasize the 1–3 actionable items with owners rule. Connect retrospection to OKR cycles: quarter-level retrospectives should feed into next-quarter priorities. Give a concrete example of a retro that changed a team behavior.

**Q: How do you integrate OKRs with sprint planning?**
Answer framework: OKRs define the "why" (what matters this quarter at the strategic level); sprint backlog defines the "what this week." The connection: every sprint should have a clear line from the work to at least one Key Result. When sprint work can't connect to any OKR, it's either (1) unplanned reactive work (track it separately) or (2) work that shouldn't be in the sprint at all. Use PI Planning or quarterly planning to set OKRs before the sprint cadence begins; review OKR progress in sprint reviews.

**Q: How has Agile changed with AI-augmented development?**
Answer framework: Lead with the bottleneck reframing — writing code is no longer the constraint; knowing what to build and verifying correctness is. Describe how specific Agile practices evolved: TDD becomes the AI self-correction mechanism (tests are what AI runs against, not what humans review); iterations shrink further (context drift in long AI sessions makes short tasks essential); retrospection becomes file-based (architecture decisions captured in CLAUDE.md compound across sessions). Close with what doesn't change: Agile was built to manage complexity and uncertainty — AI amplifies both, making Agile more critical, not less.

**Q: What's the risk of applying Agile too rigidly, and how do you avoid it?**
Answer framework: Over-formalized Agile replaces collaboration with ceremony. Symptoms: stand-ups become status reports, retros produce complaints not actions, sprint reviews are demos nobody acts on, pair programming becomes document exchange. The Manifesto's "individuals and interactions over processes and tools" is the antidote — the ceremonies exist to facilitate the interactions, not replace them. In AI pair programming specifically: stay in conversation longer than formal frameworks prescribe; resist early handoff to structured approval workflows.

**Q: How do you scale Agile across multiple teams without losing autonomy?**
Answer framework: The goal is alignment without uniformity. Teams need autonomy over their sprint cadence and internal processes; alignment is needed on interface contracts, release cadence, and shared definition of done. PI Planning (SAFe) is useful for cross-team dependency discovery — even if you don't adopt full SAFe. OKRs provide strategic alignment without dictating implementation. Calibration sessions ensure "done" means the same thing across teams. Antipattern: forcing all teams onto the same Jira workflow or ceremony schedule — this creates the appearance of process uniformity with none of the actual coordination.

## Summary

Agile methodology is the dominant framework for managing uncertainty and complexity in software delivery — 20+ years after the Manifesto, its core principles hold. The four Manifesto values resolve a recurring tension: formal processes and documentation create predictability but calcify; individual judgment and working software create agility but can lack coordination. Scrum and Kanban operationalize Agile differently — Scrum for time-boxed feature delivery with regular cadence and velocity tracking; Kanban for flow-based work (ops, platform, support) with WIP limits and cycle time measurement. For infrastructure and platform teams, the adaptations matter: explicit unplanned work capacity, operational readiness in the definition of done, and treating reactive work as a reliability signal rather than a planning problem.

The more interesting evolution is Agile in AI-augmented development. The development bottleneck has shifted: writing code is no longer the constraint — knowing what to build and verifying correctness is. This makes Agile's judgment-developing practices *more* critical, not less. TDD becomes the AI self-correction mechanism (tests give AI an unambiguous target to run against, removing the need for slow human code review of every output). Iterations shrink further because long AI sessions accumulate context drift. Retrospection becomes file-based to compound learning across sessions. The dangerous trap is documentation inflation: AI generates specs and plans prolifically, creating the illusion of progress. Discipline: working software is truth; documentation is scaffolding; the two must stay in sync.

For engineering manager interviews, the differentiating signal is not knowing Scrum ceremony names — it's understanding *when Agile creates value and when it creates overhead*. The best managers adapt Agile principles to their context (infra vs. feature teams, small vs. scaled orgs, traditional vs. AI-augmented workflows) rather than applying templates. The retro question is a reliable proxy: managers who run retros that produce real change have internalized Agile's core feedback loop.

## Raw Material
- [[raw_material/management/project/Agile in AI-Augmented Development - blog]]
