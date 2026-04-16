---
title: eBay - AI Innovation
type: Core
signal_areas: [Ownership, Leadership, Growth, Scope]
skills: [ai-tools, platform-engineering, devops, sre, incident-management, automation, cross-functional-leadership, mcp-server]
company: eBay
date: 2025-06
impact: high
growing_link:
---

# eBay - AI Innovation

## Context

As eBay broadly adopted AI tools across the engineering org — ChatGPT, Gemini, Claude Code, Cline, Cursor — most teams were using them individually and ad hoc. The Cloud Platform team had the same access, but I saw a different opportunity: systematically embedding AI into team workflows as a capability, not just a collection of individual tools. Nobody asked me to do this. I chose to invest in it because I believed the leverage was there across three areas where we had real pain: a hiring pipeline that was slow and inconsistent, a development process where quality and speed were in tension, and an operations workload where recurring toil was consuming on-call bandwidth.

## Actions

- **Hiring workflow:** I built 6+ Claude-based hiring skills covering the full recruitment lifecycle — JD refinement, resume-to-JD matching, interview question generation, structured feedback templates, feedback summarization, and offer packet generation. Before rolling these out to the team, I ran them myself across several hiring cycles to find failure modes and tune them. The workflow was used across 10+ open roles and a 200–300 candidate pipeline.
- **Spec-driven development:** Spec-driven development was a methodology developed by another team at eBay. I recognized its potential and brought it to Cloud Platform — piloting it with Claude Code on the hiring skills project before proposing it to the team. Once I'd validated it in our context, I introduced it to the team and we scaled it to a security project that required automated changes across 50+ Cloud systems. The full team of 5–6 engineers adopted the workflow; it's now how we start every significant project.
- **MCP server and triage agents:** I identified that incident triage and customer support ticket handling were the two highest-frequency toil sources for the team. I led the team to design and build an MCP server for eBay Cloud developers that enabled direct Cloud API calls and automated triage workflows. We also deployed triage agents in Customer Support to handle the most common support case patterns autonomously.
- **Documentation site:** I stood up a Cloud Platform documentation site to consolidate architecture docs, runbooks, and AI workflow guides — both to reduce the "ask a human" load and to give new hires a structured starting point.
- Throughout all of this, I held to one principle: form your own opinion before consulting AI. I made sure the team saw me using tools to accelerate judgment, not replace it — because the failure mode I most wanted to avoid was engineers outsourcing decisions to a tool and losing the ability to evaluate the output.

## Results

- PR volume across the team doubled after AI tooling adoption.
- Monthly incidents dropped from 3–4 to 1–2 (50%+ reduction); MTTD ~20 minutes, MTTR ~1–2 hours.
- 70% of customer support cases now handled autonomously by triage agents.
- Disk issue RTB (top recurring toil item) reduced by ~80% effort via MCP server triage.
- Release failure triage time dropped from 1–2 hours to ~5 minutes using local skills.
- Spec-driven methodology adopted across 50+ projects by the full team.
- Hiring skills applied to 10+ roles; hired 8+ engineers in Europe and India within 3 months.

## Learnings

- Adoption required leading by example — the team moved faster when they saw me using tools on real work daily, not on demos. In retrospect, this was the single most important factor in whether adoption stuck or faded.
- The most durable improvements were the ones with structural enforcement: the MCP server runs in the workflow automatically; the spec template is how every project starts. Optional tools get used sometimes; structural tools get used always.
- I should have instrumented baseline metrics earlier. Some of the "before" numbers came from estimates and memory rather than tracked data. Better baseline measurement from day one would have made the case stronger and the learning loop tighter.

## Signal Areas

**Primary:** Ownership (self-initiated — I identified the opportunity and drove it without being asked; piloted before proposing; accountable for outcomes across all three areas), Leadership (team-wide capability uplift; tools and workflows adopted beyond my team), Growth (learned AI tooling deeply before asking anyone else to change their workflow; explicitly modeled "AI as thinking partner, not replacement")

**Secondary:** Scope (impacted hiring, development, and operations simultaneously; results spanned multiple dimensions), Communication (led internal discussions on effective AI use; published external blogs on spec-driven development and AI agent reliability)

## Related Skills
- [[skills/management/project/Technical Roadmap]]
- [[skills/management/people/Engineering Team Management]]

## Interview Usage
- 适用 BQ：Tell me about a time you drove innovation on your team without being asked
- 适用 BQ：Tell me about a time you improved engineering productivity at scale
- 适用 BQ：Tell me about a time you reduced operational toil through automation
- 适用 BQ：Tell me about a time you introduced a new development methodology to your team
- 适用 JD 关键词：AI tooling, operational excellence, automation, platform engineering, developer productivity, MTTD/MTTR, spec-driven development

## Key Questions

**Q: How did you drive AI adoption across your team without it feeling forced?**
Talking points: Led by example — personally used and iterated tools first on real work, not demos. Shared concrete productivity gains (not abstract promises). Built structural tools (MCP server, spec template) that ran in the workflow automatically rather than relying on voluntary adoption. Created space for the team to experiment on real work.

**Q: Tell me about a time you reduced operational toil through automation.**
Talking points: Quantify the before state (3–4 incidents/month, 1–2 hours triage time, 70%+ support volume manual). Describe the specific systems built (MCP server for triage, support agents). Show the outcome (50%+ incident reduction, 5-minute triage, 70% support automation). Explain what made it durable: structural integration, not optional tooling.

**Q: Tell me about a time you introduced a new development methodology to your team.**
Talking points: Spec-driven development was invented by another team — my contribution was recognizing it was applicable to Cloud Platform's work and piloting it myself first (hiring skills project) before proposing it to the team. Scaled to a real high-stakes project (security automation across 50+ systems) so the team experienced it on work that mattered. Outcome: full team adoption, 50+ projects, PR volume doubled. The credibility came from having validated it in our own context before asking others to change how they worked.

**Q: How do you decide where to invest in internal tooling?**
Talking points: Identify the highest-frequency pain points (RTB, incident triage, hiring inefficiency). Estimate the leverage ratio — if 70% of support cases follow known patterns, that's where an agent creates the most value. Pilot on real work before scaling. Measure baseline before building so the outcome is defensible.

## Summary

At eBay, I used the broad AI adoption wave as an opportunity to systematically rebuild how my team operated across three domains: hiring, development, and operations. Nobody asked me to do this — I identified the leverage and ran the pilots myself before proposing anything to the team. The approach was consistent throughout: pilot on real work, validate the outcome, then scale.

The results compounded: PR volume doubled, monthly incidents dropped by 50%+, 70% of customer support cases were handled autonomously, and spec-driven development was adopted across 50+ projects by the full team. The most important judgment call was maintaining the principle that AI accelerates decision-making but doesn't replace it — and demonstrating that personally before asking the team to change how they worked. That's what made the adoption durable rather than a short-lived experiment.

## Raw Material
<!-- No raw_material/ source file — story reconstructed from direct experience -->
