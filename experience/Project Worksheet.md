---
title: Project Worksheet - Experience Stories
type: index
---

# Project Worksheet

Based on the thebehavioral.tech framework. Ratings: **Size** = S / M / L / XL. **Signals** = ✓ present / — absent.

> Tip: In Obsidian, enable "Readable line length" off and use horizontal scroll to view the full table.

## Axes Legend

| Axis | Meaning |
|------|---------|
| Impact | Business / org impact of the outcome |
| Scope | Breadth of the project (# teams, # systems, org level) |
| Personal Contribution | How much of the work was directly yours vs. delegated |
| Tech Complexity | Depth of technical challenge |
| Org Complexity | Political / cross-team coordination difficulty |

---

## Signal Areas Table

| Project | Impact | Scope | My Contribution | Tech | Org | Initiative | Ambiguity | Perseverance | Conflict | Growth | Communication | Leadership | Compassion | Mentoring |
|---------|--------|-------|----------------|------|-----|-----------|-----------|-------------|---------|--------|--------------|-----------|-----------|---------|
| [DoJ & Jade Programs](eBay%20-%20DoJ%20and%20Jade%20Programs.md) | XL | XL | L | L | XL | — | ✓ | ✓ | — | — | ✓ | ✓ | — | — |
| [Global Team Expansion](eBay%20-%20Global%20Team%20Expansion.md) | L | XL | L | M | L | ✓ | — | ✓ | — | ✓ | ✓ | ✓ | — | ✓ |
| [AI Innovation](eBay%20-%20AI%20Innovation.md) | L | L | L | L | M | ✓ | — | — | — | ✓ | ✓ | ✓ | — | — |
| [Platform Engineering at Scale](eBay%20-%20Platform%20Engineering%20at%20Scale.md) | XL | XL | L | XL | L | ✓ | — | ✓ | — | ✓ | — | ✓ | — | — |
| [Cloud Infra Team Turnaround](eBay%20-%20Cloud%20Infrastructure%20Team%20Turnaround.md) | L | L | L | M | M | — | — | ✓ | — | — | ✓ | ✓ | ✓ | — |
| [SRE Practice Implementation](eBay%20-%20SRE%20Practice%20Implementation%20and%20API%20Server%20Reliability.md) | L | L | L | L | M | — | — | ✓ | — | ✓ | — | ✓ | — | — |
| [Automated Cluster Mgmt Overhaul](eBay%20-%20Automated%20Cluster%20Management%20Overhaul.md) | L | L | L | L | L | ✓ | — | ✓ | — | — | ✓ | ✓ | — | — |
| [CI/CD Platform Architecture](eBay%20-%20CI-CD%20Platform%20Architecture%20and%20Reliability.md) | L | XL | L | XL | L | — | — | — | — | — | — | ✓ | — | — |
| [Engineering Velocity Program](eBay%20-%20Engineering%20Velocity%20Program.md) | L | XL | M | M | XL | — | — | — | ✓ | — | ✓ | ✓ | — | — |
| [Cloud Migration to Kubernetes](eBay%20-%20Cloud%20Migration%20to%20Kubernetes.md) | XL | XL | L | XL | L | — | — | ✓ | — | — | ✓ | ✓ | — | — |
| [Resolving L7 Traffic Gap](eBay%20-%20Resolving%20L7%20Traffic%20Gap.md) | M | M | M | M | M | — | — | — | ✓ | — | — | — | — | — |
| [Growing & Managing Talent](eBay%20-%20Growing%20and%20Managing%20Engineering%20Talent.md) | L | M | L | L | M | — | — | ✓ | — | ✓ | — | ✓ | ✓ | ✓ |
| [Embracing New Leadership Challenge](eBay%20-%20Embracing%20a%20New%20Leadership%20Challenge.md) | L | L | L | M | M | — | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ | — |
| [AI-Augmented EM Workflow](eBay%20-%20AI-Augmented%20Engineering%20Management.md) | M | M | L | M | S | ✓ | — | — | — | ✓ | — | — | — | — |

---

## Full Story Details

| Project | Context (1-line) | Key Action | Key Result | Key Learning |
|---------|-----------------|-----------|-----------|-------------|
| [DoJ & Jade Programs](eBay%20-%20DoJ%20and%20Jade%20Programs.md) | DoJ compliance mandate required covered persons removed from all eBay infra within 3 months | Structured 3 parallel tracks (Technical/Process/People), drove automation for bulk namespace transfer, participated in program war room | Zero slip on all Cloud Fleet workstreams; automated ownership transfer adopted as model by other teams | Rehearsal rounds are the highest-ROI forcing function for resolving scope ambiguity — not just execution dry-runs |
| [Global Team Expansion](eBay%20-%20Global%20Team%20Expansion.md) | US team was sole 24/7 on-call after China lost prod access; needed Europe + India teams in 3 months | Built AI-assisted hiring workflow, documentation site, and ramp-up structure; set explicit 3-month production-readiness bar | 8+ engineers hired across 2 regions; Europe team independently on-call; hiring workflow adopted org-wide | Documentation site was the highest-leverage investment — forced implicit knowledge to become explicit |
| [AI Innovation](eBay%20-%20AI%20Innovation.md) | Teams used AI tools ad hoc; I saw opportunity to systematically embed AI across hiring, dev, and ops | Built Claude hiring skills, piloted spec-driven development, led MCP server + triage agent construction | PR volume doubled; incidents 50%+ reduction; 70% support cases autonomous; spec-driven adopted across 50+ projects | Adoption stuck because tools were structurally integrated, not optional — and I led by example on real work first |
| [Platform Engineering at Scale](eBay%20-%20Platform%20Engineering%20at%20Scale.md) | 200+ clusters, manual ops model had become a ceiling at 50K nodes / 2M instances | Shifted team to declarative CRD/controller model, admission webhooks, self-service validation platform | K8s upgrades and monthly patching became routine; hundreds of apps onboarded per year via self-service | Shift from ops thinking to platform thinking was primarily a cultural change, not a technical one |
| [Cloud Infra Team Turnaround](eBay%20-%20Cloud%20Infrastructure%20Team%20Turnaround.md) | Inherited 7-person leaderless team in crisis: 24hr outage, reliability <90%, multiple incidents/week | Started with customer SLO conversations, narrowed to 2 initiatives, phased API server upgrade, coached rather than directed | Reliability 90%→99%+ in 3 months; MTTR 24hr→<1hr; team shifted from firefighting to proactive ownership | Coaching builds durable improvement; engineers who own solutions also own the monitoring and follow-up |
| [SRE Practice Implementation](eBay%20-%20SRE%20Practice%20Implementation%20and%20API%20Server%20Reliability.md) | K8s API servers had no SLOs, no runbooks, no on-call — Dev server had a 2-day outage | Implemented SLOs (99%→99.9% graduated), error budget policy, runbooks, PagerDuty, blameless postmortems, AI triage agent | Availability 90%→99.9%; MTTD ~20min; MTTR <1hr; on-call survived compliance-driven team change without disruption | Starting SLO targets conservatively is counterintuitive but right — an unsustainable SLO teaches engineers to ignore the signal |
| [Automated Cluster Mgmt Overhaul](eBay%20-%20Automated%20Cluster%20Management%20Overhaul.md) | 20+ clusters/year built/retired manually in weeks; no shared automation contract across component teams | Sequenced roadmap (decommission first), negotiated timeline with capacity team, directed tech lead to define cross-team automation contracts | Decommission reduced weeks→days; capacity team self-service; cluster build hit 1-week target; roadmap endorsed by leadership | Sequence by ROI clarity, not technical complexity; early wins fund credibility for harder phases |
| [CI/CD Platform Architecture](eBay%20-%20CI-CD%20Platform%20Architecture%20and%20Reliability.md) | Cloud Control Plane pipeline lacked progressive rollout; ECD infra caused API server overload + node exhaustion | Built Federated Deployment Controller (progressive rollout + AI health-gated rollback); applied APF, dedicated CI/CD node pools | Controller adopted by ECD org-wide; CI/CD-induced API server incidents eliminated; DORA metrics established | Boundary clarity was operationally load-bearing — knowing exactly which layer you own prevents both scope creep and gaps |
| [Engineering Velocity Program](eBay%20-%20Engineering%20Velocity%20Program.md) | Pipelines taking up to 1 week; CD team and security team at impasse blocking broader DORA targets | Analyzed deployment data; built phased proposal (3 app buckets by policy complexity); facilitated stakeholder consensus | 20% reduction in p95 deployment duration; teams saw immediate improvement; security team's roadmap preserved | Quantifying the scope of the blocker (only 5% have complex policies) reframed the debate from opinion to obvious math |
| [Cloud Migration to Kubernetes](eBay%20-%20Cloud%20Migration%20to%20Kubernetes.md) | 5,000 apps on legacy VM CI/CD; bottlenecks degrading dev productivity and site reliability | Proposed US/China ownership split at interface level; 5-phase migration blueprint with rollback at every gate; batching by app type | All 5,000 apps migrated on time; deployment duration reduced 75%; zero major service disruptions | Defining ownership at the interface level (not component level) allowed parallel execution without constant coordination |
| [Resolving L7 Traffic Gap](eBay%20-%20Resolving%20L7%20Traffic%20Gap.md) | Manager and I disagreed on how to handle L7 traffic gap in AZ rebalance system | Met with network team, found their existing L7 tool; co-designed 2-phase workflow; wrote detailed SOP | L7 AZ ramp-up delivered in 1 day; utilization 40–80% maintained; full AZ coverage within 3 months | Reframing conflict as "satisfy both constraints" instead of "who is right" opens the solution space |
| [Growing & Managing Talent](eBay%20-%20Growing%20and%20Managing%20Engineering%20Talent.md) | Three simultaneous people challenges on a high-stakes K8s upgrade program (high-potential, low-performer, open headcount) | Gave Yiran full ownership + structural support; ran genuine PIP for low performer; standardized structured hiring process | Yiran promoted to Staff in 3 quarters; K8s upgrade playbook cut cycle 9mo→4-5mo; LNP managed out cleanly; critical hire filled | Career development only works anchored to specific observable criteria — vague standards produce nothing |
| [Embracing New Leadership Challenge](eBay%20-%20Embracing%20a%20New%20Leadership%20Challenge.md) | Asked to take over leaderless crisis team in unfamiliar technical domain after 10 years in my own area | Started customer-first (SLOs), borrowed SRE expertise, formed reliability sub-team, modeled blameless retros | Reliability <90%→99%+ in 3 months; team shifted to proactive ownership; customers sent thank-you emails | Unfamiliarity forced me to use the right leadership levers instead of substituting technical opinions for management judgment |
| [AI-Augmented EM Workflow](eBay%20-%20AI-Augmented%20Engineering%20Management.md) | Admin layer of EM work consuming disproportionate time across 6 areas (reviews, hiring, planning, reporting) | Built AI workflows for executive summaries, performance reviews (NotebookLM), hiring skills, OKR docs, onboarding agents | Admin time reduced ~2/3; hiring cycle 3mo→4-6wk; OKR completion 50%→80%; new-hire ramp 3mo→6wk | Form your own opinion before consulting AI — the failure mode is outsourcing decisions and losing the ability to evaluate output |

---

## Signal Coverage Summary

| Signal Area | Stories Covering It |
|-------------|-------------------|
| **Initiative** | AI Innovation, Platform Eng at Scale, Global Team Expansion, Automated Cluster Overhaul, AI-Augmented EM |
| **Ambiguity** | DoJ & Jade Programs, Embracing New Leadership |
| **Perseverance** | DoJ & Jade, Global Team Expansion, Platform Eng at Scale, Cloud Infra Turnaround, SRE Implementation, Automated Cluster Overhaul, Cloud Migration, Growing Talent, Embracing New Leadership |
| **Conflict Resolution** | Resolving L7 Traffic Gap, Engineering Velocity Program |
| **Growth** | Global Team Expansion, AI Innovation, Platform Eng at Scale, SRE Implementation, Growing Talent, Embracing New Leadership, AI-Augmented EM |
| **Communication** | DoJ & Jade, Global Team Expansion, AI Innovation, Cloud Infra Turnaround, Automated Cluster Overhaul, Engineering Velocity, Cloud Migration, Embracing New Leadership |
| **Leadership** | DoJ & Jade, Global Team Expansion, AI Innovation, Platform Eng at Scale, Cloud Infra Turnaround, SRE Implementation, Automated Cluster Overhaul, CI/CD Platform, Engineering Velocity, Cloud Migration, Growing Talent, Embracing New Leadership |
| **Compassion** | Cloud Infra Turnaround, Growing Talent, Embracing New Leadership |
| **Mentoring** | Global Team Expansion, Growing Talent |
