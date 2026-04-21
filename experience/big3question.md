---
title: Big Three Questions — My Prepared Answers
type: Core
skills: [tmay, favorite-project, conflict-resolution, behavioral-interview, ai-infra-manager]
company: eBay
date: 2026-04-16
impact: high
growing_link:
---

# Big Three Questions — My Prepared Answers

> Prepared answers for the three behavioral questions that drive most hiring decisions:
> 1. **Tell Me About Yourself (TMAY)**
> 2. **Tell Me About Your Favorite Project** — *Engineering Velocity Program (CI/CD + cross-team)*
> 3. **Tell Me About a Time You Resolved a Conflict** — *Resolving L7 Traffic Gap (disagreement with manager)*
>
> Guidance source: [[raw_material/management/behavior/The Big Three Questions]]
> Resume source: [[_meta/resume-base]]

---

## 1. Tell Me About Yourself (TMAY)

**Target length:** 60–90 seconds. Structure: Personal Summary → 2–3 Accomplishments → Forward-Looking Statement.

### Delivery Script

> I'm an engineering manager with 20+ years in platform engineering, currently leading eBay's Cloud Fleet Management, Core Services, and App Lifecycle teams. My focus has been building and operating large-scale cloud and CI/CD platforms — Kubernetes, SRE, and developer velocity, Proven ability to set technical direction, drive automation culture, and grow global high-performing teams — and I'm a hands-on AI practitioner bringing Claude-powered agents, MCP servers, and spec-driven development into the SDLC.
>
> At eBay over the last couple of years, I led the cloud-native migration of 5,000+ applications onto Kubernetes across 100+ clusters and 2M+ pods, and served as the infrastructure lead on a company-wide engineering velocity program — coordinating cloud-infra changes across multiple teams that helped cut 95th-percentile deployment time by 20% for the initial application population. More recently, I personally built a suite of Claude-based skills for end-to-end hiring, and led my team to a customer-support agent that automated 70% of support cases, and a Cloud Platform MCP server for issue triage. I've published some of this work externally.
>
> What I'm looking for next is an AI infrastructure leadership role — a place where I can combine the platform, SRE, and CI/CD foundations I've built at scale with the AI-native engineering practices I've been pioneering. That intersection — AI infra plus AI-augmented engineering — is what I want to lead.

### Structure Breakdown

| Part | Content | Hooks Created |
|------|---------|---------------|
| **Personal Summary** | EM, 20+ years, platform engineering → K8s/SRE/CI-CD + AI practitioner | Platform depth, AI credibility |
| **Accomplishment 1** | 5,000-app K8s migration, 100+ clusters, 2M+ pods | Scope signal, scale |
| **Accomplishment 2** | Infra lead on velocity program; coordinated cloud-infra changes → 20% deployment-time reduction | Favorite-Project hook — natural pivot if asked next |
| **Accomplishment 3** | Personal: Claude hiring skills. Team-led: PR-review agent (2x PR output), customer-support agent (70% automation), Cloud Platform MCP server (issue triage) | AI-infra credibility, current relevance |
| **Forward-Looking** | AI infrastructure leadership at the platform/AI-native intersection | Ties past → target role |

### Tailoring Notes

- **For an AI Infra Manager JD:** Emphasize accomplishment 3 (AI/MCP work) and frame accomplishment 1 around GPU/training-cluster analogs if applicable.
- **For a pure platform/SRE JD:** Swap accomplishment 3 with SRE outcomes (API server 99% → 99.9%, MTTR under 1 hour).
- **For a hiring manager who has read the resume:** Shorten accomplishments to one clause each — they don't need the full scope repeated.

### What to Avoid

- ❌ Chronological walkthrough ("I started at Mainet in 2000, then eBay China in 2007, then San Jose in 2017…") — History Lesson anti-pattern.
- ❌ Childhood origin story — irrelevant unless explicitly asked.
- ❌ Negative framing of previous work — even subtly.
- ❌ "Less is more" minimalism — interviewers need the hooks.

---

## 2. Tell Me About Your Favorite Project — Engineering Velocity Program

**Source:** [[experience/eBay - Engineering Velocity Program]]
**Why this story:** Direct infrastructure-accountability role in a company-wide, revenue-impacting velocity program. Combines CI/CD, DORA metrics, cross-team leadership (15+ teams), data-driven prioritization, and a cleanly resolved impasse — all signals an AI Infra Manager interviewer is looking for. Scope is wide, impact is measurable, personal contribution is clear.

### Table of Contents (signpost in delivery)

> "This was a company-wide engineering velocity program at eBay. I'd like to walk you through four themes: **the problem and my role**, **how I unblocked prioritization with data**, **how I resolved a cross-team deadlock**, and **the results plus what I learned**. Stop me if you want me to go deeper on any of them."

### Theme 1 — The Problem and My Role

- eBay launched a company-wide velocity program to fix a systemic developer productivity issue: **CI/CD pipelines taking up to a week**, and **rollbacks that were slow and painful** — directly blocking business growth and lengthening incident recovery.
- Targets were concrete: **95th-percentile deployment under 60 minutes**, **infrastructure reliability > 99%**, **DORA elite-tier for 65% of applications**.
- The program spanned **10+ development domains, 5 cloud infrastructure teams, 3 platform teams**. As the Cloud Application Lifecycle Management manager, I was **the infrastructure accountability point** — responsible for identifying and resolving the cloud-infra bottlenecks blocking velocity, and keeping cross-team delivery on track without direct authority over most of the teams involved.

### Theme 2 — Unblocking Prioritization with Data

- Started with a **thorough deployment-metrics analysis** to find the actual bottlenecks — not what teams *believed* was slow.
- The data surfaced a critical fact: **only ~5% of applications had large, complex security policies**, but they were creating disproportionate noise in the overall velocity conversation.
- Developed a **phased proposal segmenting applications into three buckets**: no security policy, small policy, and large/complex policy — so we could lock in wins for the 95% while still committing to a path for the 5%.

### Theme 3 — Resolving the Cross-Team Deadlock

- The CD pipeline team and the cloud security team were at an **impasse**: CD wanted an immediate fix for security-policy initialization delays during pod startup; Security wanted teams to wait for their next-gen policy solution.
- I brought the phased proposal to the broader working group. Quantifying the scope — "5% vs 95%" — reframed the debate from a **technical argument into an obvious sequencing decision**.
- Stakeholders reached consensus: **immediately optimize the no-policy and small-policy buckets (covering ~95% of apps)**, buy time for the security team to deliver its new solution, then integrate the large-policy applications afterward.
- I then served as the **cross-team accountability point**, coordinating internal infra teams to deliver the agreed enhancements and keeping the program moving between milestones.

### Theme 4 — Results and Learnings

**Results:**
- **20% reduction in 95th-percentile deployment time** (to 75 minutes) for the initial target population.
- Development teams credited the phased approach — they saw **immediate, measurable improvement** while knowing the harder cases were on a **committed roadmap**.
- Leadership recognized the coordination across **15+ teams** and the ability to maintain steady delivery through organizational complexity.
- Large-security-policy integration underway on the agreed sequencing.

**Learnings:**
- **Quantifying the blocker broke the deadlock.** "Security policy is a problem" is debatable; "5% of apps have complex policies" is a fact. The phased approach became obviously correct, not a negotiated compromise.
- **Coordination was the job.** Being accountable for a program this size meant redefining "making progress" as *keeping cross-team agreements intact and unblocking whoever was stuck* — not just shipping my team's slice.
- **Respect each team's core constraint or the agreement slips.** A compromise that forced either team to abandon its central position would have produced nominal agreement and real drift.

### Prepared Follow-Ups

**Q: What were the conflicts you encountered?**
→ The CD team vs security team impasse (covered in Theme 3). Also inside my own team — engineers wanted to focus on the hardest bucket first because that's where the technical challenge was. I had to redirect toward the 95% where we could ship wins.

**Q: What was the hardest part?**
→ Operating without direct authority over most of the teams. The temptation is to escalate to get decisions forced through. That's short-term leverage that destroys long-term trust. Building consensus — especially after the security-team impasse — was slower but made every subsequent cross-team ask easier.

**Q: What would you do differently?**
→ Establish the phased segmentation *and* the working-group decision cadence earlier. I spent a few weeks trying to resolve the security/CD debate bilaterally before bringing it to the group. The forum was more productive than the 1:1s — once I saw that, I used it as the default for the rest of the program.

**Q: How did you measure success beyond deployment time?**
→ DORA metrics as the shared language: lead time, deployment frequency, change failure rate, rollback duration. My team implemented DORA proactively ahead of the org-wide rollout, which gave leadership a unified, quantitative view across both our Cloud Control Plane pipeline and the ECD platform.

**Q: What part did you personally own vs. the broader team?**
→ Personally: the data analysis that drove the phased proposal, the cross-team negotiation that produced consensus, the program-level accountability. My team: the infrastructure changes (APF tuning, dedicated CI/CD node pools, supply-chain controls) and the Federated Deployment Controller built for our own Cloud Control Plane pipeline that the ECD team later adopted.

---

## 3. Tell Me About a Time You Resolved a Conflict — L7 Traffic Gap

**Source:** [[experience/eBay - Resolving L7 Traffic Gap]]
**Why this story:** High-stakes — revenue-critical L7 traffic for eBay's public surfaces. Deeply involved — disagreement was directly with my manager. I ended up being substantively right without making my manager wrong. Clean resolution that preserved the working relationship and satisfied both constraints. Demonstrates exactly the behaviors tech companies look for: assertiveness, going to the source, emotional control, outcome focus, data-driven compromise, relationship preservation.

### Context (Stakes Established Quickly)

- My team had built APIs that let the capacity team **automatically rebalance workloads across Availability Zones** for most applications. One gap remained: **a small set of applications handling public Layer 7 traffic** — revenue-critical eBay surfaces — was unsupported. During traffic spikes, that meant real **latency and revenue exposure**.
- **My manager and I disagreed on the approach.** He wanted to extend the existing solution with minimal changes, prioritizing the resource-efficiency targets he had already committed to upstream. My team and I believed L7 traffic patterns required specialized handling — extending the existing system wasn't going to cut it.
- The disagreement wasn't about whether the gap mattered. It was about **how to close it without abandoning the efficiency commitments**.

### Actions (Grouped by Behavior Pattern)

**Reframed the disagreement as a constraint problem, not a win/lose:**
- I explicitly **acknowledged my manager's efficiency goal as a legitimate constraint**, not resistance to overcome. Once the question became "how do we satisfy both constraints?" instead of "who is right?", the solution space opened up.

**Went to domain experts before committing to build:**
- My tech lead and I **met with the network team**, who had deep domain expertise in L7 traffic patterns. The goal was to understand what tooling already existed before we architected anything from scratch.
- We discovered they had **already built a specialized tool for L7 traffic ramp-ups**. That was the unlock — an existing capability to integrate, not a new system to build.

**Co-designed a solution that satisfied both positions:**
- Together with the network team, we designed a **two-phase workflow**: use the existing AZ rebalance system for normal operations, then trigger the network team's L7 tool during high-traffic ramp-up. Nothing had to be replaced, and neither constraint had to be abandoned.

**Delivered a durable short-term path without blocking on automation:**
- I directed the team to write a **detailed SOP** — trigger conditions, workflow, handoff points between the two systems — so we could execute consistently without waiting for full automation to be built.

### Results (Including the Relationship)

- **Two-phase workflow implemented within 1 month**, validated via trial run and pilot.
- **AZ ramp-up for public L7 applications reduced to within 1 day** (previously unsupported entirely).
- **AZ resource utilization held at 40–80%**, meeting my manager's efficiency targets.
- Team completed the **full auto-rebalance solution for private traffic and public L4 applications within 3 months** — end-to-end AZ coverage delivered across all application types.
- **Relationship with my manager strengthened.** He explicitly recognized the approach in subsequent 1:1s, and we used the same "constraint-reframing + domain-expert consultation" pattern on later cross-team problems. The network team also became a durable partner for my team on later traffic-management work.

### Why This Story Works

- **Stakes were high** — revenue-critical traffic, not a stylistic preference.
- **I was deeply involved** — central to the disagreement, central to the resolution.
- **I ended up substantively right** — the two-phase solution did require specialized L7 handling, which validated the original concern.
- **I did it without making my manager wrong** — his efficiency constraint was honored in the final design.
- **Honest emotional content** — I didn't purge the disagreement. My manager genuinely pushed back, I genuinely pushed back, and the tension was real until the network team meeting opened a third path.
- **Relationship preserved and improved** — explicitly cited as a result.

### Key Behaviors Demonstrated

| Best Practice | How It Shows Up |
|---|---|
| Be assertive | I maintained the position that L7 required specialized handling despite disagreement with my manager |
| Go directly to the source | I engaged my manager directly, and went to the network team in person rather than via tickets |
| Remain emotionally in control | Reframed the debate rather than escalating; stayed professional throughout |
| Stay focused on outcomes | Kept revenue-protection and efficiency both on the table — no personal gain involved |
| Use data/facts | Grounded the need in L7 traffic patterns and eBay revenue exposure |
| Demonstrate empathy | Treated my manager's efficiency constraint as valid from the outset |
| Involve the right people | Network team domain experts at the right moment — not to apply pressure, but to open a solution |
| Don't take too long | Resolution and implementation within 1 month |
| Come to a clear resolution | Explicit two-phase workflow + SOP; everyone knew the path forward |
| Preserve the relationship | Working relationship with both manager and network team strengthened |

---

## Bonus — Questions I'll Ask Back

> "Every single interview ends with 'Do you have any questions for me?' 'No, I think you covered everything' is a massive missed opportunity." — adapted from the source article.

### For the Hiring Manager

- What does success look like for this role in the first 90 days, and what about in the first year?
- What's the most important problem you're hoping this hire will solve that isn't being solved today?
- How is the team currently balancing AI infrastructure build-out with day-to-day platform reliability?

### For Peers / Engineering Leads

- How does the team handle disagreements on technical decisions — can you walk me through a recent example?
- What parts of the platform do engineers find frustrating right now, and what's been hard to fix?
- How do engineers collaborate with the AI/ML research teams on infrastructure requirements?

### For Skip-Level / Senior Leadership

- What's the biggest challenge the organization is facing in the next 12 months, and where does this team fit into addressing it?
- How do you think about the balance between in-house AI infrastructure investment and leveraging external platforms?
- What's the company's philosophy on AI-augmented engineering practices for the engineering organization itself?

### For Cross-Functional Partners (Product / Research)

- What signals does your team use to tell whether an infrastructure team is genuinely helping vs. getting in the way?
- Where has the infrastructure team's roadmap diverged from what you needed in the past, and how was that resolved?

### Questions I Won't Ask

- ❌ Anything easily Googleable — "What does eBay do?" signals lack of preparation.
- ❌ Compensation and benefits — save for the recruiter.
- ❌ "How did I do?" — puts the interviewer in an awkward position; rarely gets a useful answer.

---

## Practice Notes

- [ ] Time the TMAY delivery — target 60–90 seconds. Anything over 2 minutes is too long.
- [ ] Rehearse the Favorite Project with the four-theme signpost — the Table-of-Contents technique keeps the interviewer oriented and invites deeper-dive questions you're prepared for.
- [ ] For the Conflict story, practice the "I acknowledged my manager's efficiency goal as a legitimate constraint" framing — it's the line that signals maturity and emotional control.
- [ ] Before any target interview, re-read the JD and swap accomplishment 3 in TMAY if the role is non-AI-infra (see Tailoring Notes).
- [ ] Prepare 3–5 interviewer-type-specific questions from the Bonus section for each interview slot on the loop.

---

## Related Notes

- [[experience/eBay - Engineering Velocity Program]] — source for Favorite Project
- [[experience/eBay - Resolving L7 Traffic Gap]] — source for Conflict Story
- [[experience/eBay - CI-CD Platform Architecture and Reliability]] — alternate favorite-project candidate if interviewer prefers direct-ownership scope over cross-team velocity angle
- [[experience/eBay - SRE Practice Implementation and API Server Reliability]] — backup favorite-project candidate for reliability-focused JDs
- [[experience/ebay-highlights]] — quantified impact table, useful as TMAY accomplishment source
- [[_meta/resume-base]] — full resume content
- [[raw_material/management/behavior/The Big Three Questions]] — source guidance
