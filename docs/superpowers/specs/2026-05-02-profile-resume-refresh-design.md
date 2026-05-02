# Profile & Resume Refresh — Design Spec
**Date:** 2026-05-02  
**Output location:** `jobs/profile/`  
**Deliverables:** `linkedin-profile.md`, `resume.md`

---

## Context & Goal

Regan's coaching feedback: resume and LinkedIn are underselling Austin's value. Two gaps:
1. **Missing impact** — bullets describe what was built, not what it did for eBay's business
2. **Missing people leadership** — hiring, mentoring, performance management absent

Benchmark: Kevin Zhu (Amazon Senior SDM) — every bullet has action + scale + business outcome; people leadership in every role.

**Positioning strategy:** Kevin Zhu's impact-first structure + Platform Legacy narrative (18yr eBay, 3 tech generations) + AI-native signal as differentiator in most recent role. Targets both FAANG Senior EM and growth-stage Director.

---

## Key Business Numbers (verified with Austin)

| Metric | Value |
|--------|-------|
| eBay GMV supported | $74B annual |
| Internal engineering teams served | 200+ |
| API availability SLO | 99.9%+ |
| Kubernetes clusters | 100+ |
| Pods | 2M+ |
| Regions / AZs | 3 regions, 25 AZs |
| Apps migrated to K8s | 5,000+ |
| Deployments/week (2017–2023 era) | 35,000+ across 20,000+ app pools |
| Cluster utilization maintained | 40–80% |
| Cluster provisioning time | 1 month → 1 week (20+ clusters/year) |
| Cluster lifecycle savings | 12+ person-months/year |
| Engineers hired (EU + India) | 8+ across 200–300 candidate pipeline |
| AI: PR output | Doubled |
| AI: Monthly incidents | 3–4 → 1–2 (50%+ reduction) |
| AI: Customer support automation | 70% |
| AI: Release triage time | 1–2 hours → ~5 minutes |
| AI: Disk issue RTB savings | 80% |
| AI: Spec-driven adoption | 50+ projects |
| People: Staff promotion | 1 engineer → Staff in 3 quarters |
| K8s upgrade cycle (post-playbook) | 9+ months → 4–5 months |

---

## LinkedIn Design

### Headline
```
Software Development Manager at eBay | Platform Engineering Leader 
| Cloud-Native Infrastructure at $74B Commerce Scale | AI-Native Operations & Team Building
```

### About Section
Platform engineering leader with 20+ years building and operating eBay's cloud infrastructure at global scale. Currently leading Cloud Fleet & Apps teams managing 100+ Kubernetes clusters, 2M+ pods across 3 regions — the platform powering eBay's $74B annual GMV and serving 200+ internal engineering teams at 99.9%+ API availability.

Built eBay's cloud infrastructure through three technology generations (VMware → OpenStack → Kubernetes), leading each transition with zero downtime at scale. Technical expertise spans Kubernetes infrastructure, DevOps automation, SRE, and AI-native engineering — currently pioneering practices that have doubled team PR output, reduced monthly incidents 50%+, and automated 70%+ of operational support work via Claude-based agents and MCP servers.

Track record: 5,000+ applications migrated to Kubernetes, 8+ engineers hired across Europe and India, senior engineers developed to Staff level, global teams scaled across San Jose, Shanghai, Dublin, and Bangalore.

Passionate about platform thinking, operational excellence, and building teams that outlast their initial projects.

---

### Experience Bullets

#### SDM — Cloud Fleet Management & App Lifecycle (Sep 2023 – Mar 2026) [6 bullets]

1. Led Cloud Platform (Fleet & Apps) teams managing 100+ Kubernetes clusters, 2M+ pods across 3 regions — platform underpinning eBay's $74B annual GMV and serving 200+ internal engineering teams at 99.9%+ API availability; delivered AZ/Region auto-scaling maintaining cluster utilization at 40–80%, preventing resource waste and capacity-driven incidents

2. Pioneered AI-native operations using Claude-based agents and MCP servers; doubled team PR output, reduced monthly incidents 50%+ (3–4 → 1–2), automated 70% of customer support cases, reduced release triage from 1–2 hours to ~5 minutes, and cut disk issue remediation effort 80% via MCP-driven triage; drove spec-driven AI development adoption across 50+ team projects, becoming one of eBay's highest adopters of Claude Code

3. Automated cluster provisioning reducing setup time from 1 month to 1 week for 20+ clusters/year, saving 12+ person-months annually

4. Served as Cloud primary contact for eBay's engineering velocity initiative; platform reliability and automation improvements enabled significantly faster release cadence and reduced deployment cycle times for 200+ internal engineering teams

5. Delivered critical infrastructure for eBay's company-wide DoJ & Jade compliance programs — built isolated environments for covered-person PII access control and automated ownership transitions for thousands of cloud namespaces/apps; completed infra cutover within 3 months under legal deadline

6. Established global engineering teams in Europe and India; hired 8+ engineers across a 200–300 candidate pipeline; developed a senior engineer to Staff level in 3 quarters, reducing K8s upgrade cycles from 9+ months to 4–5 months

---

#### SDM — Cloud App Lifecycle Management (Feb 2017 – Sep 2023) [4 bullets]

1. Led global teams (San Jose + Shanghai) to migrate 5,000+ eBay applications and 1M+ instances from OpenStack to Kubernetes, enabling cloud-native architecture transformation at scale

2. Architected end-to-end CI/CD platform powering 35,000+ deployments/week across 20,000+ app pools; delivered multi-cluster deployment, dependency-aware rolling upgrades, and metrics-based canary releases

3. Drove zero-downtime regional data center migration (PHX exit, RENO launch) for mission-critical services; built self-healing remediation system (LOM) reducing manual recovery ops burden

4. Managed cross-site teams (San Jose + Shanghai), mentoring engineers to senior-level growth and driving technical roadmap across 6+ years of platform evolution

---

#### SDM — Cloud, eBay China COE (Feb 2012 – Feb 2017) [4 bullets]

1. Led ~20 engineers to architect eBay's internal cloud platforms across 3 technology generations: V1 (VMware), V2 (OpenStack), V3 (Docker + Kubernetes)

2. Built Zebra — eBay's fully automated provisioning system — reducing developer provisioning time from days to under 10 minutes, serving 2,000+ eBay developers

3. Designed MongoDB-based Configuration Management System, migrating 30+ critical systems; owned NextGen provisioning service during eBay/PayPal unified platform initiative

4. Drove eBay China Innovation Program; incubated open-source projects; teams won multiple Skunkworks innovation awards

---

#### Team Lead — Platform DevEx Tools (Jun 2007 – Feb 2012) [2 bullets]

1. Built eBay Shanghai platform developer experience team from 0 to 8 members in 6 months

2. Delivered Raptor IDE and eBay developer tooling significantly improving productivity for 2,000+ eBay engineers; developed eBay APIs and SDK for third-party developers

---

## Resume Design

### Summary
Platform engineering leader with 20+ years building and operating large-scale cloud infrastructure at eBay. Currently leading Cloud Fleet & Apps teams managing 100+ Kubernetes clusters, 2M+ pods across 3 regions — platform underpinning eBay's $74B annual GMV and serving 200+ internal engineering teams at 99.9%+ API availability. Track record: 5,000+ applications migrated to Kubernetes, global teams built across 4 regions, senior engineers developed to Staff level. Active AI practitioner — pioneered Claude-based agents and MCP servers that doubled team PR output and automated 70%+ of operational support work.

### Experience Bullets
Same as LinkedIn above. Resume version of the most recent role: consolidate bullets 3+4 into one bullet (cluster lifecycle + velocity, separated by semicolon) to keep to 5 bullets per role. All other roles: same bullet count as LinkedIn.

### Early Career (Mainet System, Apr 2000 – Mar 2007)
Include condensed version (2 bullets max): team building (50+ developers, multi-city) + enterprise product delivery (40+ customers, China/Japan/Korea). Signals early leadership and breadth but should not dominate the resume.

### Skills (reordered, trimmed)
```
Cloud & Infrastructure:  Kubernetes, Docker, OpenStack, Service Mesh/Istio/Envoy, GCP/GKE
SRE & Operations:        SLO/SLI, Incident Management, Capacity Planning, Auto-scaling
DevOps & CI/CD:          Tekton, Jenkins CI, Git
AI Tools:                Claude Code, MCP Servers, Spec-Driven Development
Observability:           Prometheus, Grafana, Kibana
Databases:               MySQL, MongoDB, PostgreSQL, Cassandra, Elasticsearch
Programming:             Go, Python, Java, JavaScript
Management:              Agile/Scrum, Hiring & Onboarding, Performance Management
Languages:               English, Mandarin
```

### Removed from skills
Vue.js, Sprint, Memcache, ActiveMQ, JQuery, Tailwind — non-core for Senior EM targeting

### Education (unchanged)
- Zhejiang University — Master's, Automation (1997–2000)
- Zhejiang University — Bachelor's, Automation (1993–1997)

### Certifications (keep, trim)
PMP | Scrum | Kubernetes | Redhat  
(Remove: eBay People Management, OpenStack — internal/dated)

---

## Files to Create

| File | Location |
|------|----------|
| `linkedin-profile.md` | `jobs/profile/linkedin-profile.md` |
| `resume.md` | `jobs/profile/resume.md` |
