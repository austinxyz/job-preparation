---
title: eBay - Global Team Expansion
type: Core
signal_areas: [Scope, Leadership, Ownership, Communication, Growth]
skills: [team-management, hiring, people-management, cross-functional-leadership, onboarding, sre, documentation]
company: eBay
date: 2025-04
impact: high
growing_link:
---

# eBay - Global Team Expansion

## Context

After eBay's China-based engineers were designated as covered persons under the DoJ compliance program and lost access to PII data, staging, and production environments, the US team was left as the sole owner of 24/7 on-call for Cloud Platform. That wasn't sustainable — Cloud Platform is a critical shared service and a single-region on-call model created both reliability and burnout risk. The company's answer was to expand into Europe and India. I was given a 3-month hiring window per region and was accountable for the full arc: hire the teams, transfer the domain knowledge, and get new engineers to independently handle production incidents within 3 months of joining.

## Actions

- I treated hiring as a systems problem, not a talent acquisition problem. I built a standardized end-to-end AI-assisted hiring workflow covering JD refinement, resume-to-JD matching, interview question libraries, structured feedback templates, feedback summarization, and offer packet generation — so the process could run consistently at speed across 10+ open roles without varying by interviewer.
- I established collaboration cadences with local hiring managers and tech leads in each region, defining clear hand-off points between my team's technical evaluation and local HR/recruiting operations.
- I built a team documentation site from scratch covering day-by-day ramp-up plans, key component and product architecture, development processes, and SRE operationalization principles — so new hires had a structured path to production readiness that didn't depend on tribal knowledge or US team availability.
- I set an explicit success criterion for ramping: independently handle production incidents within 3 months of joining. I used this to anchor the documentation content — every runbook, architecture doc, and process guide was written to the standard of "could a new hire follow this alone at 2am?"
- I established a pairing arrangement where our US team lead worked directly with the Europe team through their first production incidents — using real incidents as ramp validation rather than a separate formal assessment.

## Results

- Europe team: hired within 3 months, fully ramped over the following 3 months, now independently handles production on-call.
- India team: hired within 3 months (started later than Europe); engineers actively ramping up toward production readiness.
- Hired 8+ engineers across seniority levels (senior, mid-level, new grad) across both regions.
- The AI-assisted hiring workflow and ramp-up documentation were adopted by other Cloud teams across the org — they became reusable infrastructure, not one-off artifacts from this program.

## Learnings

- The documentation site was the highest-leverage investment — not just for the new hires but for forcing the existing US team to make implicit knowledge explicit. The process of writing it exposed gaps we didn't know we had.
- I should have started building the documentation site 2–3 months before the hiring window opened, not concurrently with it. By the time the first hires arrived, documentation was still catching up. Earlier preparation would have made the ramp faster.
- The AI hiring workflow was adopted by other teams because it was built as a repeatable system, not customized for one hiring cycle. That generality was intentional but I hadn't predicted the adoption. In the future, I'd architect these internal tools for reuse from day one and share them earlier.

## Signal Areas

**Primary:** Scope (two global regions, 8+ engineers, 3-month windows, full arc from hiring to production readiness), Leadership (built and ramped teams from zero under urgency, created knowledge infrastructure that outlasted the immediate need), Ownership (accountable for the full outcome — not just hiring headcount but production on-call independence)

**Secondary:** Communication (documentation site as scalable knowledge transfer; hiring workflow as coordination infrastructure across regions and interviewers), Growth (designed a system that made the org better beyond my team — hiring workflow and ramp docs adopted org-wide)

## Related Skills
- [[skills/management/people/Engineering Team Management]]
- [[skills/management/project/Technical Roadmap]]
- [[skills/management/behavior/STAR Method]]

## Interview Usage
- 适用 BQ：Tell me about a time you built and scaled an engineering team under time pressure
- 适用 BQ：Tell me about a time you had to manage a team across multiple geographies
- 适用 BQ：Tell me about a time you improved a hiring or onboarding process
- 适用 BQ：Tell me about a time you built something that had impact beyond your immediate team
- 适用 JD 关键词：team building, hiring, people management, global team, onboarding, knowledge transfer, production readiness

## Key Questions

**Q: Tell me about a time you built a team from scratch under significant time pressure.**
Talking points: Name the urgency driver (US team sole on-call after China team lost access — not sustainable). Describe how I treated hiring as a systems problem: built the AI-assisted workflow so the process could scale across 10+ roles without varying by interviewer. Result: 8+ engineers across two regions hired within 3 months each.

**Q: How do you ensure new hires in remote locations become independently effective quickly?**
Talking points: Set an explicit, measurable criterion upfront (independently handle production incidents within 3 months). Built documentation to that standard — every doc written to "could a new hire follow this alone at 2am?" Used first real incidents as ramp validation, not a separate test. Europe team met the 3-month target.

**Q: How do you scale a hiring process across multiple roles and interviewers without losing consistency?**
Talking points: Standardize the artifacts that vary most — JD templates, question banks, feedback forms, debrief structure. Use AI to reduce per-interview overhead so interviewers focus on evaluation, not preparation. Document and train so the process outlives any single hiring cycle. The workflow was later adopted by other teams because it was built as a system, not a one-off.

**Q: Tell me about a time you had impact beyond your immediate team.**
Talking points: The hiring workflow and ramp-up documentation were designed to solve Cloud Fleet's problem but built to be reusable. Other Cloud teams adopted them without being asked. The lesson: internal tools built for scale rather than customized for the immediate need naturally become org-wide infrastructure.

## Summary

When eBay's China engineers lost production access under the DoJ compliance mandate, the US team became the sole 24/7 on-call owner for Cloud Platform — an unsustainable position for a team that needed global coverage to be reliable. The company's answer was expansion into Europe and India, with a 3-month hiring window per region and a clear bar: new hires independently handling production incidents within 3 months of joining.

I treated this as a systems design problem. The hiring workflow, documentation site, and ramp-up structure were all built as repeatable infrastructure rather than one-off solutions — both because the scale (8+ roles across two regions) demanded it, and because I knew the knowledge transfer problem would recur. Both teams were hired on schedule; Europe is now independently on-call. The hiring framework and ramp-up agents were adopted by other teams in the org, which validated the approach: building for reuse rather than the immediate deadline creates compounding value.

## Raw Material
<!-- No raw_material/ source file — story reconstructed from direct experience -->
