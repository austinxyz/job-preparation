---
title: eBay Work Highlights
type: experience
skills: [kubernetes, k8s, cross-functional-leadership, team-management, hiring, people-management, ai-tools, sre, incident-management, platform-engineering, cloud-infrastructure, devops]
company: eBay
date: 2023-09
impact: high
growing_link:
---

# eBay Work Highlights

> Core achievements, project experiences, and technical contributions from eBay — for writing, LinkedIn updates, and interview preparation.

---

## Project Highlights

<!-- Format: Project | Background | My Role | Key Actions | Quantified Results -->

### DoJ & Jade Programs

**Situation:** eBay was required to prevent covered persons from accessing PII data in staging and production environments to comply with a DoJ policy. Non-compliance carried significant legal and financial risk.

**Task:** As the Cloud Fleet team lead, I was responsible for three critical workstreams:
- Build two new cloud environments from scratch: SDDZ (isolated dev environment for covered persons) and DCPX (a transition layer for data sanitization between the isolated and production environments)
- Transfer ownership of thousands of cloud namespaces and apps away from covered persons
- Maintain business continuity for existing infrastructure functions — including host runtime, OS patching, cloud console, and namespace/app RBAC management

**Action:**
- Coordinated a cross-team war room with daily syncs; created a comprehensive runbook covering all steps, owners, and dependency graphs
- Ran multiple rehearsal rounds to de-risk the final cutover
- Drove a three-track execution across Technical, Process, and People dimensions:
  - *Technical:* Automated AZ/cluster provisioning and ownership transfer at scale; used data-driven analysis to prioritize efforts across knowledge transfer, incident handling, and end-to-end deployment; leveraged AI to rapidly build dashboards and visualize progress reports
  - *Process:* Streamlined on-call workflows to reduce pager volume
  - *People:* Traveled on-site for knowledge transfer; drove targeted hiring to backfill covered-person capacity

**Result:**
- Stood up SDDZ and DCPX AZ/clusters within 2 weeks
- Automatically transferred thousands of cloud namespaces and apps with zero customer intervention
- Completed cutover on schedule; US team absorbed additional infrastructure components with no critical incidents

---

### Global Team Expansion

**Situation:** After China-based engineers were designated as covered persons and lost access to PII data, staging, and production environments, the US team was left bearing sole 24/7 on-call responsibility. To restore a sustainable follow-the-sun support model, the company decided to expand the Cloud team into Europe and India.

**Task:**
- Stand up Fleet & Apps teams in Europe and India, each within a 3-month hiring window.
- Transfer domain knowledge from the China team and ramp up new regional members.
- Enable new hires to independently handle production incidents within 3 months of joining.

**Action:**
- Leveraged AI agents to standardize the end-to-end hiring workflow — including JD creation, resume screening, interview question libraries, feedback templates, and debrief/offer packet templates; documented best practices and trained interviewers.
- Built a team documentation site covering day-by-day ramp-up plans, key component/product architecture, development processes, and operationalization principles (SRE).
- Established smooth collaboration processes with local hiring teams and tech managers to accelerate recruiting and onboarding.

**Result:**
- Europe: completed hiring in 3 months, ramped up over the following 3 months, and now independently supports production.
- India: completed hiring in 3 months (started later); engineers recently onboarded and actively ramping up.
- Hired 8+ engineers across seniority levels (senior, mid-level, new grad) across both regions.
- Standardized hiring and ramp-up agents were adopted by other teams across the org.

---

### AI Innovation

**Situation:** As eBay broadly adopted AI tools (ChatGPT, Gemini, Claude Code, Cline, Cursor), the Cloud Platform team faced a practical challenge: how to systematically embed AI into engineering workflows — not just as individual tools, but as a team-wide capability across hiring, development, and operations.

**Task:**
- Automate and improve the end-to-end hiring process using AI agents
- Introduce spec-driven development to improve SDLC quality and team productivity
- Build AI-powered tooling (MCP server, triage agents) to reduce operational toil and improve customer support

**Action:**
- **Hiring automation**: Built 6+ Claude-based hiring skills covering the full recruitment lifecycle — JD refinement, resume-to-JD matching, interview question generation, interview feedback structuring, feedback summarization, and offer packet generation; dramatically improved both efficiency and consistency across 10+ open roles
- **Spec-driven development**: Piloted spec-driven development with Claude Code on the hiring automation project, then scaled it to a security project automating changes across 50+ Cloud systems (SSO access patterns and configurations); entire team of 5–6 engineers adopted the workflow
- **MCP server & triage agents**: Led the team to build an MCP server for eBay Cloud developers, enabling them to call Cloud APIs directly and automate incident triage; deployed triage agents in Customer Support workflows
- **Documentation**: Stood up a Cloud Platform documentation site to capture architecture, runbooks, and AI best practices for the team

**Result:**
- PR volume doubled across the team following AI tooling adoption
- Monthly incidents reduced from 3–4 to 1–2 (50%+ reduction); MTTD ~20 min, MTTR ~1–2 hours
- 70% of customer support cases now handled by triage agents autonomously
- Disk issue (top RTB) triaged via MCP server, saving ~80% of RTB effort
- Release failure triage time reduced from 1–2 hours to ~5 minutes using local skills
- Hiring skills applied across 10+ roles and a 200–300 candidate pipeline; successfully hired 8+ engineers in Europe and India within 3 months

---

## Technical Contributions

- **AI Agent Reliability**: Pioneered practices for reducing hallucination and improving determinism in Claude-based agents; published findings: [Taming AI Agent Uncertainty](https://austinxyz.github.io/blogs/blog/2025/12/25/taming-ai-agent-uncertainty)
- **Spec-Driven Development**: Established and documented a spec-driven AI coding methodology using Claude Code; published as team reference and external blog: [Claude Code Spec-Driven Development](https://austinxyz.github.io/blogs/blog/2026/03/06/claude-code-spec-driven-development)
- **Agile + AI Coding**: Synthesized how Agile principles apply in AI-assisted development workflows; published: [Agile Development in AI Coding](https://austinxyz.github.io/blogs/blog/2026/03/09/agile-development-in-ai-coding)
- **MCP Server**: Designed and led delivery of a Cloud Platform MCP server enabling API-driven triage and RTB automation for Cloud developers

---

## Team / Leadership

- Led by example: personally adopted and iterated on AI tools before rolling out to the team, building credibility and practical know-how
- Shared learnings proactively — ran internal discussions on how to use AI effectively in day-to-day engineering work
- Actively sourced best practices from peer teams and helped the Cloud team adopt them systematically
- Created a culture of experimentation: encouraged team members to try AI tools on real work, not just demos

---

## Quantified Impact

| Metric | Result |
|--------|--------|
| Hiring pipeline | 10+ roles, 200–300 candidate pipeline, 8+ engineers hired |
| PR output | Team PR volume **doubled** |
| Monthly incidents | Reduced from 3–4 to **1–2** (50%+ reduction) |
| MTTD | ~20 minutes |
| MTTR | ~1–2 hours |
| Customer support automation | **70%** of support cases handled autonomously by agents |
| Disk issue RTB savings | **80%** effort reduction via MCP server triage |
| Release triage time | Reduced from 1–2 hours to **~5 minutes** |
| Spec-driven coverage | **50+ projects**, full Cloud team (5–6 engineers) adopted |

---

## Potential Article Topics

- [x] Controlling uncertainty in AI agents (published)
- [x] Spec-driven development in practice (published)
- [x] Agile methodology in AI-assisted coding (published)
- [ ] MCP server for enterprise Cloud operations: a practical guide
- [ ] Reimagining hiring with AI: end-to-end automation from JD to offer

---

## To Verify / Fill In

- [ ] Security automation project details: exact number of systems changed, scope of SSO migrations
- [ ] More precise MTTD/MTTR baseline figures for historical comparison
