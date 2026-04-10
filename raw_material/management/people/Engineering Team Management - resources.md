---
title: Engineering Team Management - resources
source: (multiple)
date_saved: 2026-04-07
processed: true
skill_note: "[[skills/management/people/Engineering Team Management]]"
---

# Engineering Team Management — Suggested Resources

## Reading List

- Will Larson — *An Elegant Puzzle: Systems of Engineering Management* (recommended chapters: 2 "Organizations", 4 "Approaches")
- Camille Fournier — *The Manager's Path*, Chapter 5 (Managing a Team) & Chapter 6 (Managing Multiple Teams)

---

## Notes: Will Larson — An Elegant Puzzle

### Chapter 2 — Organizations

**Team sizing**
- Optimal team size: **6–8 engineers per manager**. Below 4 = manager is under-leveraged and team lacks critical mass for real systems work. Above 10 = manager can't give adequate individual support.
- Teams below ~4 feel perpetually short-staffed and can't handle member churn (one person leaving is catastrophic). Teams above ~10 lose individual ownership — contributions get diffused.
- Rule: a manager managing 2 teams should aim for those teams to each have 4+ engineers, not split 8 people 4/4.

**Team lifecycle**
- Teams move through stages: **bootstrapping → growing → sizing → consolidating → sunsetting**. Each stage requires different management energy.
- Bootstrapping: heavy hiring + culture-setting. Growing: onboarding + process-building. Sizing: right-sizing headcount to workload. Consolidating: merging overlapping teams. Sunsetting: winding down with care.
- Don't apply "growing" tactics to a "consolidating" situation — you'll over-hire into a shrinking mandate.

**Slack as a strategic resource**
- Teams without slack (buffer capacity) can only do reactive work. Proactive improvement, technical debt, and experimentation require ~20% protected slack.
- When stakeholders request 100% utilization, the team loses the ability to do anything unplanned — this is how tech debt compounds and morale deteriorates.
- Protect slack explicitly; don't let it get quietly poached by ad-hoc requests.

**Migrations and ownership transitions**
- When moving ownership between teams, use **time-boxed migration plans** with explicit done criteria. Open-ended migrations drift indefinitely.
- Never migrate something to a team that can't own it (lacking context, capacity, or expertise). The migrating team must either transfer knowledge or retain shared ownership with a clear sunset date.
- Migration debt: when ownership is ambiguous, bugs get dropped, features are built twice, and neither team feels responsible.

**Organizational design traps**
- **Conway's Law**: systems tend to mirror the org structure of the teams that build them. If two teams can't collaborate, their systems will have a poorly-designed boundary.
- **Matrix hell**: engineers reporting to multiple managers (tech lead + functional manager + product manager) lose clarity on priorities and accountability.
- **Too many tiger teams**: spinning up special task forces fragments attention without adding sustained capacity. Tiger teams should be temporary and have explicit disbandment criteria.
- **Senior manager with too few reports**: a VP managing 3 engineers is a sign of structural misalignment; the abstraction layer adds overhead without value.

**Succession planning**
- Every key role (manager, tech lead, staff engineer) should have an identified internal candidate. If someone leaves and there's no successor, the role becomes a crisis.
- Building succession candidates is a manager's job, not HR's. Give potential candidates stretch opportunities — leading projects, standing in at leadership meetings — before they're in the role.

---

### Chapter 4 — Approaches

**System thinking for organizational problems**
- Most "people problems" are actually system problems. An engineer who "doesn't communicate well" may be in a role with unclear interfaces, no documentation culture, or a team that punishes question-asking.
- **Work the policy, not the person**: if the same problem recurs with different people, the system is at fault. Fix the system (process, expectation, interface) rather than coaching individual after individual.
- Exception: if only one person has the problem across many contexts, it's an individual issue. Use the counterfactual: "would someone else in this role have this problem?"

**Engineering metrics and technical debt as organizational signals**
- Cycle time (time from start to ship) and lead time (time from request to ship) are org health signals, not just engineering metrics. Long lead times often reveal unclear requirements or approval bottlenecks, not slow engineers.
- DORA metrics (deployment frequency, lead time for changes, MTTR, change failure rate) are a proxy for delivery health. Low deployment frequency often signals manual processes, fear of breaking prod, or insufficient test coverage — systemic issues.
- Technical debt accumulation is also **organizational debt**: teams carrying heavy tech debt can't execute new features, which manifests as "this team is slow." The root cause is prior underinvestment, not current laziness.

**Process debt**
- Just as tech debt accumulates, so does process debt. Under-defined processes create chaos; over-defined processes create bureaucracy that slows execution.
- Signs of process debt: engineers don't know how to get a decision made; the same question gets answered differently by different people; nothing ships without the manager's involvement.
- Fix: document the decision-making process, not just the decision. Make processes "self-service" wherever possible.

**Career development as continuous practice**
- "Career ladder" is a shared vocabulary, not a bureaucratic exercise. Without it, engineers don't know what growth looks like and managers can't give actionable feedback.
- Don't wait for annual reviews. Continuous growth conversations ("here's what I see you doing well, here's the next level behavior I'd want to see") compound. Surprise reviews damage trust.
- The "pillar vs. keystone" distinction: some engineers are **pillars** (high individual output, independent), others are **keystones** (high structural value — connectors, reviewers, mentors — with lower individual output). Both matter. Optimizing only for individual output undervalues structural contributors and causes collaboration to collapse.

**Incident culture**
- Incidents are system failures, not people failures. **Blameless post-mortems** focus on: what in the system allowed this to happen? What change prevents recurrence?
- Blameful cultures produce cover-ups and under-reporting. Blameless cultures produce faster learning and lower MTTR over time.
- "Five whys" is a root-cause tool, not an interrogation. Stop at the system-level intervention, not the person-level one.

---

## Notes: Camille Fournier — The Manager's Path

### Chapter 5 — Managing a Team

**The "shit umbrella" responsibility**
- A manager's job includes shielding the team from organizational noise: leadership anxiety, shifting priorities, political churn that doesn't affect the team's actual work. Don't forward every fire downward.
- But also: don't over-protect. Engineers who never see the reality of the business become disconnected and make poor prioritization decisions. Give context without creating anxiety.
- The balance: share the "why" and the strategic picture; filter out the "what if" speculation and the organizational drama.

**Debugging dysfunctional teams**
- **Not shipping**: usually unclear goals, too much WIP, or blocked dependencies — not individual laziness. Fix: narrow WIP to 1-2 active projects per engineer; clarify done criteria.
- **Low morale / unhappy team**: start by listening (1:1s, skip-levels), not fixing. You don't know the root cause yet. Common causes: perceived lack of impact, leadership vacuum, unclear growth path, over-work.
- **Product-engineering tension**: usually a goals misalignment. Fix: joint roadmap session where both functions are co-authors, not presenters to each other.
- **Constant fires**: technical debt + lack of monitoring + no on-call rotation design. Fix the system, not the on-call roster.

**Managing low performers**
- The "two-strike clarity test": (1) Have you told them clearly and specifically what the gap is? (2) Have you given them adequate time and support to close it?
- Most low performance is a **role-person mismatch**, not bad intent: wrong level, wrong domain, unclear expectations. Rule out the mismatch before concluding it's a performance problem.
- PIPs are documentation, not a surprise — they should describe exactly what was already communicated verbally. If the engineer is surprised by a PIP, the manager failed earlier.
- The humane exit: when it's not working, be honest, specific, and kind. Help the person understand where they might succeed. Long, drawn-out ambiguous situations hurt everyone.

**Brilliant jerks**
- The cost of tolerating a "brilliant jerk" = (their output) − (everyone else's reduced output from toxic behavior). The math rarely favors keeping them.
- Address early, specifically, and directly: "When you interrupt engineers in design reviews, it prevents others from contributing — I need that to stop." Not "your attitude is bad."
- If behavior doesn't change after clear, direct feedback with a timeline: escalate or exit. Letting it persist signals to the team that the behavior is acceptable.

**Process as documentation**
- If you have to explain the same thing twice, write it down. Documented processes reduce key-person dependency, onboard faster, and prevent "it depends on who you ask" inconsistency.
- Runbooks, decision logs, onboarding docs: these are multipliers on team capacity. Under-investment in documentation is a choice to remain a bottleneck.

**Meeting cadence**
- Weekly 1:1s (engineer's agenda, career conversations, blockers)
- Weekly team sync (project status, not individual status — that's what tickets are for)
- Bi-weekly retrospective for active project teams
- Monthly skip-levels for the manager's manager to stay connected to team health

---

### Chapter 6 — Managing Multiple Teams

**The "second team" transition**
- Moving from one team to multiple teams is the hardest management transition. You can no longer track individual engineer progress directly — you must **manage through your managers**.
- The failure mode: continuing to manage individual contributors on one team while nominally managing the others. The "special team" gets over-attention; others feel orphaned.
- The shift: your job is now to make your managers successful, not to make your engineers successful directly.

**Delegation to managers (not just tasks)**
- Delegate **authority**, not just work. If you second-guess every decision your managers make, they become coordinators not leaders, and you become the bottleneck.
- "Disagree and commit" applies here: if you wouldn't block a decision but have a concern, say so once, then let the manager proceed. Save escalation for decisions that are genuinely irreversible or high-stakes.
- Your job with managers: set context (what matters and why), set expectations (what good looks like), give feedback regularly, remove blockers they can't remove themselves.

**Management debt**
- Organizational equivalent of technical debt: postponed performance conversations, unresolved team conflicts, role boundaries that were never clarified, two teams with overlapping mandates.
- Management debt compounds: a performance conversation not held in Q1 is a crisis by Q3. Address it early while it's still manageable.

**Staying technical as a manager of managers**
- Attend design reviews selectively (don't dominate, ask questions). Do code reviews for important decisions. Maintain a small personal project to keep your instincts calibrated.
- Without technical credibility, you can't evaluate whether your managers' technical assessments are correct. You become dependent on their judgment in ways that remove your ability to grow them or catch blind spots.
- "Technical" at this level means: can you tell a good architectural decision from a bad one? Can you identify when a tech debt problem is being under-estimated? Do engineers respect your technical opinion?

**Cross-team dependencies: the #1 source of friction**
- Map all cross-team dependencies explicitly. Make them visible in roadmaps and planning. Hidden dependencies are landmines.
- Own the coordination overhead yourself rather than delegating it to ICs — an engineer waiting on another team is expensive; a manager triaging and escalating the dependency is the right model.
- Reduce dependencies wherever possible: APIs, contracts, shared ownership models, co-location of tightly-coupled work.

**Calibration across teams**
- Run cross-manager calibration sessions regularly (quarterly): multiple managers discuss engineer performance together. Goal: prevent grade inflation/deflation, ensure the bar is consistent across teams.
- Without calibration: Team A's "meets expectations" may be Team B's "exceeds expectations." This causes resentment, attrition, and unfair comp outcomes.

**Building a management pipeline**
- Identify future managers early: look for engineers who naturally lead projects, mentor others, and think about systems not just their own work.
- Give "management apprentice" opportunities: lead a team meeting, run a project, present to leadership, do a round of 1:1s with teammates during a manager vacation.
- Don't wait until you have an open manager role to develop candidates. By then, it's too late for a smooth transition.

**The dual pipeline problem**
- Engineers who don't want to manage need a genuine growth path, not a consolation prize. Staff/Principal/Distinguished engineer tracks must be as valued — in comp, visibility, and influence — as the management track.
- If the IC track is a second-class track, your best senior ICs will leave or reluctantly move to management, where they may be less effective.

**Headcount and budget**
- At this level, you own headcount requests. Justify with scope + capacity math: "We have X projects at Y capacity; we can't start Z without 2 engineers."
- Vague headcount requests ("we need more people") get denied. Specific, scope-justified requests get approved.
- Understand the budget cycle of your company and get your asks in early. Headcount approved in Q3 doesn't arrive until Q1 of next year.
