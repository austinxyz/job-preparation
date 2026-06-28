---
title: Core Interview Stories — spoken-delivery practice scripts
date: 2026-06-25
source: Austin_Xu_Story_Revisions.docx (Regan / Weekly Commit)
purpose: Say-aloud versions of core stories, usable across all interviews. Rewritten to grade 4–7, ~9–11 words/sentence, every metric intact.
how_to_use: Read each aloud once, then deliver once WITHOUT looking. Pause between paragraphs. Signpost ("I did three things"). End with "anything you'd like me to expand on?"
---

# Regan's Rewritten Stories — Practice Sheet

Why these were rewritten: Austin is fluent but not native; under pressure long sentences are where you lose breath + the thread. Originals were grade 6–9 / 12–16 words per sentence → rewrites are grade 4–7 / ~9–11 words, **same numbers kept**.

## ⚠️ Two flags before practicing
1. **Q6 (grow a member) and Q7 (failure) are the SAME situation** — the troubled fleet team, manager gone 6 months, lead engineer just left. **Do NOT tell both in one loop.** Pick one per interview; if both, frame explicitly: Q6 = developing the engineer, Q7 = your own early mistake.
2. **Metric fix:** it's **p95** of deployments → say **"95% of deployments finished in under an hour"** (not "95% of deployment duration").

---

## Q1 — Tell me about yourself  *(target ~90s, 4 clean beats)*

> I'm Austin. I've worked in cloud and infrastructure for over 20 years.
>
> Most recently, I led a platform team at eBay. We ran eBay's Kubernetes fleet, about 5,000 apps across 200 clusters. My team handled everything from the clusters themselves to reliability and developer tooling.
>
> What I'm most excited about right now is AI. I'm one of the top Claude Code users at eBay. I built AI workflows for hiring. I led my team to build an MCP server and triage agents, so developers could solve their own infra problems. And I moved the whole team to spec-driven development.
>
> eBay had a layoff in March, and my role was part of it. For me, the timing worked out. I was already looking for a faster-moving, AI-first company.
>
> What draws me is the point where infrastructure meets AI — building the platforms that make AI development possible. That's exactly where I want to be.

**Delivery:** pause after each paragraph (4 beats). Land hard + slow on the 3 AI items (hiring, MCP/agents, spec-driven) — the differentiator. Layoff line short + matter-of-fact → move straight to "the timing worked out."

---

## Q4 — AI strategic experience  *(his signature story)*

> At eBay, more and more teams were starting to use AI tools. But they used them ad hoc — one person here, one tool there. I saw a bigger opportunity. I thought we should adopt AI in a systematic way, across the whole team.
>
> I started with my own management work. I built Claude skills to create an AI workflow, then used it to speed up my hiring.
>
> Next, I moved the team to spec-driven development. We write a clear spec first, then let AI help build to it. This roughly doubled our PR throughput.
>
> Then I led the team to build a support agent. It now handles about 70% of our customer support questions on its own.
>
> The results were strong. Production incidents dropped by half. Support effort went way down. And the team's work-life balance got much better.
>
> My biggest lesson: using AI on demand only helps a little. But using it systematically, across many areas, lets each area learn from the others. The gains compound.
>
> One thing I'd do differently. I'd measure a clear baseline before and after. That would have shown us exactly where AI helped most.

**Delivery:** four moves build on each other (management → spec-driven → support agent → results) — count on fingers for pacing. State each number plainly and stop ("doubled our PR throughput"). Closing reflection = maturity; say it calmly, not apologetically.

---

## Q3 — Deliver under a hard deadline / high uncertainty (DOJ)

> I want to share a project with a hard compliance deadline and a lot of unknowns. We figured it out and delivered on time.
>
> Last year, the US Department of Justice introduced a new policy. Under it, developers in certain countries could no longer access the personal data of US citizens. Some of our developers in China were affected.
>
> So eBay launched a project to build an isolated environment for those developers. My team owned the infrastructure piece. We had to build isolated clusters in the cloud, and move thousands of applications to US developers.
>
> For problems like this, my team follows a simple order: technology first, then process, then people.
>
> First, we try to solve it with technology, for example building automation into our platform. If that's not enough, we adjust the process to separate the work. And only as a last resort, we move people.
>
> There were still many unknowns. So we ran rehearsals. The real environment wasn't ready, so we used a mock setup. It still helped us find problems fast. We also held a daily sync with every dependent team to clear blockers right away.
>
> In the end, we built the isolated environment in three months. We hit the deadline and moved thousands of application ownerships to US developers.

**Delivery:** "technology first, then process, then people" is the anchor — say it slowly, let it sit. Keep the DOJ setup factual/neutral (routine compliance, not sensitive).

---

## Q5 — Biggest project (Engineering Velocity / DORA)

> eBay ran a company-wide program called Engineering Velocity. The goal was to get 60% of our applications to the DORA elite level.
>
> At the time, most teams took about a week to deploy. And rolling back was hard and risky. The program spanned many teams. My team owned the Kubernetes clusters and the API servers, so I was the main contact on the infra side. Every cloud bottleneck came to me.
>
> I did three things.
>
> First, I led my team to build a Federated Deployment Controller. It supported canary and blue-green rollouts, with an AI-based detector in the canary step. This cut deployment time sharply.
>
> Second, I fixed an API server problem. During peak hours, traffic was overwhelming the servers. I applied API Priority and Fairness to slow down development traffic, so production traffic stayed protected.
>
> Third, I broke a deadlock. The CD team and the security team were stuck on a policy. I pulled the data and found that only 5% of apps had complex policies. So I proposed a phased plan: move the other 95% first, and give security time to build a better solution. Both teams agreed.
>
> The results were strong. 65% of applications hit DORA elite. 95% of deployments finished in under an hour. And we rolled the DORA metrics out to more than 200 teams.
>
> My takeaway: align across teams instead of only optimizing your own. And data is the fastest way to break a deadlock.

**Delivery:** "I did three things" → clear pause. Slow down on "only 5% of apps had complex policies" (the resolving insight). Final numbers = three separate sentences, beat between each.

---

## Q6 — Grow a team member  *(SAME setup as Q7 — pick one per loop)*

> I want to share how I helped grow one of my engineers.
>
> Three years ago, I took over the fleet management team at eBay. The team was in trouble. The manager had left six months earlier, the lead engineer had just left, and morale was low. There were four engineers left.
>
> One of them caught my attention. She'd only been on the team a year, but she took initiative on her own. I saw real potential. So I thought about how to set her up to succeed.
>
> I did three things. First, I gave her the goal and let her own the plan, including the technical details. I trusted her to make the calls.
>
> Second, I set realistic expectations with our customers. I asked what mattered most to them, and we agreed to give the team some time to recover.
>
> Third, I gave her regular feedback — what she did well, and where she could improve. When she made progress, I recognized it, both inside and outside the team.
>
> It worked. In three months, the project turned around. The service used to crash often. Now it was stable.
>
> What I learned: when someone shows potential, trust them and give them room. Set honest expectations with customers. And give steady feedback so people can grow.

**Delivery:** keep focus on HER, not the team's troubles (setup = one breath). If also using Q7, change this opening so it doesn't sound like the same story restarting.

---

## Q7 — Failure story  *(SAME setup as Q6 — pick one per loop)*

> This is a story about a time I started in the wrong direction, then corrected course.
>
> Two years ago, I became the leader of the fleet management team at eBay. The situation was rough. The manager had left six months earlier, and the lead engineer had just left. The system was unreliable, and customers were complaining a lot.
>
> Because it felt urgent, I jumped straight into fixing the technical problems myself. I worked hard for a few weeks. But the results still weren't good.
>
> So I stopped and rethought it. This area was new to me, so technology wasn't my strength here. I realized the real priority wasn't a quick technical fix. It was customer satisfaction, and building trust with the team.
>
> So I changed my approach. First, I listed every issue and ranked them by priority. Then I started talking, with customers and with my team. I managed customer expectations, and I found a new lead engineer. Together, we built a new plan. I focused on the customers and on supporting the team.
>
> After two months, things turned around. Incidents dropped. Availability went from 90% to 99%. Customers were happier. One even sent me a thank-you email.
>
> What I learned: understand the whole problem before jumping to a technical fix. Customer satisfaction helps you prioritize. And trust matters most when you're leading a team that's struggling.

**Delivery:** own the mistake plainly in paragraph 3 — don't rush past it; the honesty is what lands. End on the three lessons and stop. **Do NOT** add the old "I can manage any team anywhere" line.

---

## Q8 — Develop a team member (coaching save)  *(the builder story — use when asked how you grow people)*

> I want to share a time I helped an engineer grow from senior to staff level.
>
> Two years ago, I expanded my scope and took over a new team. Their main project was a large Kubernetes upgrade — over 100 clusters, thousands of nodes, multiple environments. A key senior engineer had just left. The project had no clear owner.
>
> One of the remaining engineers, Yiran, was a strong senior with real potential. I believed she could step up and own this project. So I made a deliberate bet on her.
>
> I did three things.
>
> First, I gave her full ownership. She owned the planning, the technical decisions, and the weekly cross-team meetings. I didn't prescribe anything. She broke the project into phases herself. She introduced ideas around patch management that hadn't been in the original plan.
>
> Second, I provided structural support underneath her. I assembled her team, handled stakeholder communication for her, and shielded her from blame during incidents. This let her focus on execution, not politics.
>
> Third, I linked the project to Staff Engineer criteria explicitly. I named her specific gaps — cross-team influence and delegating to peers. She knew exactly what bar she was developing toward. She took initiative and sought out communication training on her own. I nominated her for the architecture committee to build her cross-team visibility.
>
> The results were strong. In three quarters, the team upgraded all 100-plus clusters. Yiran built a reusable playbook that cut future upgrade cycles from nine months down to four. She was promoted to Staff Engineer.
>
> What I learned: high-potential engineers grow faster under real ownership than under managed exposure. The key is structural support underneath — not protection from the complexity on top. And career development only works when it's anchored to explicit, observable criteria.

**Delivery:** "I did three things" → clear pause, count on fingers. Slow down on the three numbers: 100+ clusters, 9 months → 4, Staff promotion. These are your anchors. Opening 45–60s, then three tight 30s moves. End with the learning — it's what makes you sound like a builder, not just an executor.

**⚠️ Use this when asked:** "develop a team member," "grow someone," "coaching success," "how do you build people." This is your **coaching save** — the story Regan said was missing. It balances the kernel-engineer (managed out) story. Don't pair them in one answer; they cover opposite ends of the people-management spectrum.

---

## Q2 — Why this company  *(can't pre-write — reusable structure)*

Three concrete, **researched** reasons, each tied back to your own experience. Generic praise ("I admire your culture") is the failure mode.
- **Reason 1** — a specific phrase from the JD that matches how you already work.
- **Reason 2** — a real product/launch from the company that proves they do the work you want to build for.
- **Reason 3** — the scope of the role, mapped to something you've already done at scale.

**Worked example (Tapestry pattern):**
> A few specific things drew me to this role. First, the JD literally says "Design as Code" and "AI-augmented engineering" — the exact language I use for how my team works; rare to see it written into a JD, not just a slide. Second, I saw the HyperQ launch — agentic AI automating interconnection site validation for PJM — a real deployment on a hard problem, not a demo; that's the kind of infra I want to build. Third, the role is about helping multi-disciplinary teams — ML, power systems, software — go from idea to production without friction; that's exactly what I did at eBay across 200+ teams. Different domain, same model.

**For TikTok/Yemao:** build 3 reasons from the JD + TikTok e-commerce/SRE + the team scope (Algorithms/Architecture/SRE/QA). Tie each back to your eBay work.

---

## Delivery coaching (apply to ALL)
- **One idea per sentence.** Two ideas → split. Short sentences buy thinking time, never strand you mid-clause.
- **Pause on purpose.** After a number or key line, stop a beat. Silence = confidence; rushing = nerves.
- **Signpost.** "I did three things" → first / second / third.
- **Lead with the result, then explain.** "We cut incidents in half. Here's how."
- **Trim filler.** Drop "last but not least" / "as quickly as possible" → "third" / "right away."
- **Practice numbers out loud** — crisp, not hesitant. They're your strongest asset.
- **Close every story:** "That's the high-level overview — anything you'd like me to expand on?" → hands the turn back, makes it 50-50.

## Rehearsal plan (→ Tue 6/30)
- [ ] Read each script aloud once, then deliver once WITHOUT looking
- [ ] Time each: open 45–60s → 2–3 points × ~30s → result → "expand?" (total ~2–2.5 min)
- [ ] Pick which fleet-team story (Q6 vs Q7) you'll use; don't pair them
- [ ] **Q8 (Yiran) = coaching save — practice this cold; it's the missing story Regan flagged**
- [ ] Vary toolkit: if you used SLO/error budget → next answer use coaching/hiring/prioritization
- [ ] Numbers ready: 100+ clusters, 9mo→4mo, 3 quarters to Staff, 90%→99% availability, pages -40%
- [ ] AI = "leverage/augmentation", never "replacement"
- [ ] Pre-build Q2 (Why TikTok) — 3 researched reasons tied to your work
- [ ] Fri Alan tech mock + Mon 10am Regan delivery drill = practice these live

---

## Additional Stories (2026-06-27 rewrite batch)

> **Overlap flags before using:**
> - Q9 = same situation as Q7 (failure / fleet turnaround). Pick ONE per loop; Q7 is the tighter version. Q9 useful if asked specifically about "early mistake" framing.
> - Q11 = same situation as Q4 (AI adoption) but different emphasis — Q11 focuses on spreading to OTHER teams / org-level influence. Use Q11 when asked about "cross-team influence" or "organization-wide change."
> - Q12 = same situation as Q3 (DOJ) but adds people-adjustment layer (US team traveled to China, hiring backfill). Use Q12 when interviewer probes on people/org aspects of the project.

---

## Q9 — Fleet turnaround (failure → correction)  *(same situation as Q7 — pick one per loop)*

> This is a story about a time I started in the wrong direction, then corrected course.
>
> Two years ago, I took over the fleet management team at eBay. The situation was rough. The manager had left six months earlier. The tech lead had just left. The system was unreliable. Customers were complaining.
>
> Because it felt urgent, I jumped straight into fixing the technical problems myself. I worked hard for several weeks. But things didn't improve.
>
> So I stopped and rethought it. This area was new to me. Technology wasn't my strength here. The real priority wasn't a quick technical fix. It was customer satisfaction — and building trust with the team.
>
> I did three things. First, I listed every issue and ranked them by priority. Second, I found a new tech lead and built a plan together. Third, I focused on managing customer expectations and supporting the team — not the technical work.
>
> After two months, things turned around. Incidents dropped. Availability went from 90% to 99%. One customer sent me a thank-you email.
>
> What I learned: understand the whole problem before jumping to a technical fix. Customer satisfaction helps you prioritize. And trust matters most when a team is struggling.

**Delivery:** own the early mistake plainly — don't rush past it. Three-item close at the end, then stop. Do NOT add "I can manage any team in any area" — that line is cut.

---

## Q10 — Ops → Platform mindset shift  *(new — use for "team transformation" or "strategic thinking" questions)*

> I want to share how I helped my team shift from firefighting to building a platform.
>
> When I took over the fleet management team, the work was almost entirely operational. The team upgraded Kubernetes twice a year and the OS once a month. But each upgrade caused incidents. Schedules kept slipping. The team was stuck in a loop.
>
> I realized we were solving the same problems over and over. We were using people and manual effort where we needed a system.
>
> I did three things.
>
> First, I shared the platform idea with the team. I listened to their concerns — about deadlines, about the transition risk. They bought in, but needed a plan.
>
> Second, we applied SRE best practices. We set up SLO and SLI measurements before changing anything. That way, we could verify reliability through the transition. We brought in an SRE specialist team to help us adopt the method correctly.
>
> Third, we built the automation system in phases — starting with the highest-risk upgrade type first.
>
> After six months, we had a fully automated upgrade system. Monthly OS upgrades ran on schedule. Kubernetes upgrades ran twice a year without slipping. Incidents dropped sharply. Reliability improved to 99.9%.
>
> What I learned: when you're stuck on the same problem, change the model — not just the execution. Proven frameworks like SRE save time. And measure first — you can't know if you're improving without a baseline.

**Delivery:** "stuck in a loop" is the hook — say it slowly. Three things signpost. Land the numbers (99.9%, twice a year, monthly) as separate beats.

---

## Q11 — AI adoption: team + org-wide  *(overlaps Q4 — use when asked about org-level influence, not just team adoption)*

> I want to share how I led my team to adopt AI — and then helped the rest of the organization do the same.
>
> AI tools were everywhere. But adoption was uneven. Some teams tried one tool, didn't get results, and gave up. My team went further.
>
> I did three things.
>
> First, I adopted AI myself across three areas: software development, customer support, and my own management work. I found the best approach for each. Then I shared what worked with my team.
>
> Second, I got the team to buy in. I shared my own journey — what worked, what didn't. I listened to their concerns. They worried AI output might cause a production incident. I told them: start small. Pick one low-risk task. Verify the result. Then expand.
>
> Third, I spread this to other teams. Other managers said they were too busy to change. So I picked one task from their actual backlog and completed it with AI in front of them. The result spoke for itself.
>
> More and more teams adopted spec-driven development. Engineering output roughly doubled. Hiring processes got streamlined. Managers found top candidates faster.
>
> What I learned: lead with your own experience before asking others to follow. Address real concerns with real examples. And small wins build the trust to expand further.

**Delivery:** "too busy to change" → pause. Then "I picked one task from their actual backlog and completed it in front of them" — this is the turn, say it slowly. Numbers: doubled throughput, org-wide spread.

---

## Q12 — DOJ compliance + people adjustments  *(overlaps Q3 — use when interviewer probes on org/people layer of the project)*

> I want to share a project with a hard compliance deadline and many unknowns — and how we delivered on time.
>
> Because of a US government policy change, Chinese developers could no longer access US citizens' personal data. eBay needed an isolated environment for those developers. We had three months to build it.
>
> I did three things.
>
> First, I set up a war room with all dependent teams. We met daily. Every blocker went to leadership immediately. Transparency kept everything moving.
>
> Second, we ran rehearsals with mock components because the real environment wasn't ready yet. Each rehearsal found blockers early. By the time we ran the real setup, the team was confident.
>
> Third, we made people adjustments. US team members traveled to China to work side by side with the Chinese team. We hired to backfill critical positions. We transferred knowledge from Chinese team members to US members before the cutover. All of this required management support — travel budget, new headcount — and I secured it.
>
> We completed the isolated environment in three months. No major incidents. Chinese developers moved to the new environment on schedule.
>
> What I learned: be transparent with leadership — it keeps blockers moving fast. Rehearsals build confidence when you have unknowns. And follow the right sequence: technology first, then process, then people.

**Delivery:** "I secured it" — short, matter-of-fact. Don't undersell the exec sponsorship ask. Three-beat close on lessons. End with "anything you'd like me to expand on?"

---

## Q13 — Cluster lifecycle management system  *(new — use for "complex project delivery," "prioritization," or "build vs buy" questions)*

> I want to share how my team built a complex system by starting small and proving value first.
>
> Cluster management was a big pain. Building a new cluster took months. The process was manual and ticket-based. My team spent most of their time on repetitive work. Decommissioning clusters was even riskier — one mistake could take down production.
>
> We decided to build a cluster lifecycle management system. It would handle creation, upgrade, and decommission. But the team was already overwhelmed with incoming requests. We couldn't pause everything to build it.
>
> I did three things.
>
> First, I picked the highest-value component to start: decommission. It was the most painful and the most impactful. Starting there gave us the most leverage.
>
> Second, we piloted it on development clusters only — lower risk, fully under our control. This let us move fast without threatening production.
>
> Third, once decommission worked, we handed it to the capacity team to test. They liked it. Their endorsement gave us the credibility and support to expand to other components.
>
> The results were clear. The capacity team could decommission clusters in under a week — on their own, without my team. My team was freed to build the next components.
>
> What I learned: break complex projects into components and start with the most valuable one. Get customer feedback early — it builds trust and unlocks support. And each success makes it easier to expand.

**Delivery:** "one mistake could take down production" — pause after that. "Under a week, on their own" = the payoff line, say it slowly. Three-beat lessons close.
