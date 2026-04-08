---
title: eBay - AI Innovation
type: experience
skills: [ai-tools, platform-engineering, devops, sre, incident-management, automation, cross-functional-leadership, mcp-server]
company: eBay
date: 2025-06
impact: high
growing_link:
---

# eBay - AI Innovation

## Situation

As eBay broadly adopted AI tools (ChatGPT, Gemini, Claude Code, Cline, Cursor), the Cloud Platform team faced a practical challenge: how to systematically embed AI into engineering workflows — not just as individual tools, but as a team-wide capability across hiring, development, and operations.

## Task

- Automate and improve the end-to-end hiring process using AI agents
- Introduce spec-driven development to improve SDLC quality and team productivity
- Build AI-powered tooling (MCP server, triage agents) to reduce operational toil and improve customer support

## Action

- **Hiring automation**: Built 6+ Claude-based hiring skills covering the full recruitment lifecycle — JD refinement, resume-to-JD matching, interview question generation, feedback structuring, feedback summarization, and offer packet generation; improved efficiency and consistency across 10+ open roles
- **Spec-driven development**: Piloted spec-driven development with Claude Code on the hiring project, then scaled to a security project automating changes across 50+ Cloud systems; full team of 5–6 engineers adopted the workflow
- **MCP server & triage agents**: Led the team to build an MCP server for eBay Cloud developers, enabling direct Cloud API calls and automated incident triage; deployed triage agents in Customer Support workflows
- **Documentation**: Stood up a Cloud Platform documentation site to capture architecture, runbooks, and AI best practices

## Result

- PR volume doubled across the team following AI tooling adoption
- Monthly incidents reduced from 3–4 to 1–2 (50%+ reduction); MTTD ~20 min, MTTR ~1–2 hours
- 70% of customer support cases now handled by triage agents autonomously
- Disk issue (top RTB) triaged via MCP server, saving ~80% of RTB effort
- Release failure triage time reduced from 1–2 hours to ~5 minutes using local skills
- Hiring skills applied across 10+ roles and a 200–300 candidate pipeline; hired 8+ engineers in Europe and India within 3 months
- Spec-driven methodology adopted across 50+ projects by the full Cloud team

## Related Skills
- [[skills/management/project/Technical Roadmap]]
- [[skills/management/people/Engineering Team Management]]

## Interview Usage
- 适用 BQ：Tell me about a time you drove innovation on your team
- 适用 BQ：Tell me about a time you improved engineering productivity at scale
- 适用 BQ：Tell me about a time you reduced operational toil
- 适用 JD 关键词：AI tooling, operational excellence, SRE, MTTD/MTTR, automation, platform engineering

## Key Questions

**Q: How did you drive AI adoption across your team without it feeling forced?**
Talking points: Led by example — personally used and iterated tools first; shared concrete productivity gains (not abstract promises); created space for experimentation on real work; documented workflows so adoption was cumulative, not one-off.

**Q: Tell me about a time you reduced operational toil through automation.**
Talking points: Quantify the before state (3–4 incidents/month, 1–2 hours triage); describe the specific system built (MCP server, triage agents); show the outcome (1–2 incidents/month, 5-minute triage, 70% support automation); explain what made the solution durable.

**Q: How do you decide where to invest engineering effort on internal tooling?**
Talking points: Identify highest-frequency pain points (RTB, incident triage, hiring); estimate leverage (80% of support cases → agent handles 70%); pilot on real work before scaling; measure and communicate results to build team confidence.

**Q: Tell me about a time you introduced a new development methodology to your team.**
Talking points: Explain why spec-driven development was chosen (quality, speed, repeatability); describe the pilot scope (hiring project) before scaling; show adoption curve (1 project → full team → 50+ projects); tie to measurable outcome (PR volume doubled).

## Summary

At eBay, I used the broad AI adoption wave as an opportunity to systematically rebuild how my team operated — not just to save time, but to raise the quality ceiling on work that had been rate-limited by manual effort. I introduced spec-driven development, built an MCP server for Cloud API access, deployed triage and customer support agents, and built end-to-end AI hiring skills. Each initiative was piloted on real work before being scaled to the team and eventually the broader org.

The outcomes were compounding: PR volume doubled, monthly incidents dropped by 50%+, 70% of customer support cases were handled autonomously, and the spec-driven methodology was adopted across 50+ projects by the full team. The story demonstrates what's possible when AI adoption is treated as a deliberate engineering investment — not a set of disconnected experiments — and when the manager does the groundwork before asking the team to follow.

## Raw Material
<!-- No raw_material/ source file — story reconstructed from direct experience -->
