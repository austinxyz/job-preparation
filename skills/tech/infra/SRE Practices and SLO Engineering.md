---
title: SRE Practices and SLO Engineering
category: tech/infra
tags: [sre, slo, sli, error-budget, burn-rate, golden-signals, red-method, use-method, incident-command, prr, chaos-engineering, rto-rpo, slo-as-code, pyrra, sloth, incident-management, blameless-postmortem, reliability, toil]
status: in-progress
priority: high
last_updated: 2026-04-17
created_from_jd: "[[positions/Manager, DevOps, SRE & AI Infrastructure - AppZen]]"
---

# SRE Practices and SLO Engineering

## Knowledge Map
- 前置知识：observability (metrics/logs/traces), incident management, service architecture, statistics basics (percentiles, rates)
- 延伸话题：error budget policies, toil elimination, **multi-burn-rate alerting**, **Golden Signals / RED / USE methods**, **SLO-as-code (Sloth, Pyrra, Nobl9, OpenSLO)**, **chaos engineering (Chaos Monkey, Gremlin, LitmusChaos, AWS FIS)**, **Production Readiness Review (PRR)**, **Incident Command System (IC / Comms / Scribe)**, **DR / RTO / RPO**, **AWS Well-Architected Reliability Pillar**, **K8s reliability primitives** (probes, PDB, topology spread), [[Observability and Incident Management]], [[LLMOps and AI Pipeline Engineering]] (quality SLOs for AI systems), Google SRE book, SRE Workbook, Hidalgo "Implementing SLOs"
- 管理关联：reliability culture, blameless post-mortems, on-call design, SRE team charter, PRR governance, incident command drills, SOC2/ISO-27001 reliability controls

## Industry Foundations (textbook baseline)

> This section is the industry-standard SRE baseline — terminology, frameworks, and tools commonly referenced in interviews — kept separate from the eBay-experience content in Core Concepts so both are easy to scan.

### The SLI Menu & Specification Frameworks

- **SLI menu (choose from this list):** Availability · Latency · Freshness · Correctness · Quality · Throughput · Coverage · Durability. For stateful services add Durability + Consistency; for batch add Freshness + Coverage.
- **Golden Signals (Google SRE Book):** Latency · Traffic · Errors · Saturation. Start here for any request-driven service.
- **RED method (Tom Wilkie):** Rate · Errors · Duration. Simplified Golden Signals for microservices — the most-used variant in practice.
- **USE method (Brendan Gregg):** Utilization · Saturation · Errors. Applied to *resources* (CPU, disk, network), not requests — complements RED.
- **VALET (Google, less common externally):** Volume · Availability · Latency · Errors · Tickets. "Tickets" means human intervention count — useful for ops-heavy services.

### SLI specification — where and how to measure

- **Measurement location matters:** server-side (what the service sees), load-balancer / API-gateway (what clients see — usually the right layer), synthetic probes (what a virtual user sees from outside), client-side real-user monitoring (RUM) for web/mobile. SLIs measured from the server underestimate real user impact because they miss network, TLS, and DNS failures.
- **Sampling + aggregation:** high-cardinality labels can blow up metrics cost; sample traces at 1–5%; aggregate over a rolling window (28–30 days standard).
- **Exclusions:** planned maintenance can be excluded from SLI if communicated in advance; external-dependency failures often *not* excluded (your users still see them).

### Event-based vs Window-based SLOs

- **Event-based (request-count):** "99% of HTTP requests succeed." Good SLI is clear per-request; bad: quiet services (low traffic) have noisy SLI.
- **Window-based (time-slice):** "99% of 1-minute windows have ≥99% success rate." Better for low-traffic or batch services; smoother but slower to react.
- **User-journey SLOs:** compose multiple service SLOs that touch a critical path (login → browse → checkout). Each step has its own SLI; journey SLO = intersection.

### Availability math (memorize these)

| SLO | Downtime / year | Downtime / month | Downtime / week |
|---|---|---|---|
| 99% | 3.65 days | 7.2 h | 1.68 h |
| 99.5% | 1.83 days | 3.6 h | 50.4 min |
| 99.9% | 8.76 h | 43.8 min | 10.1 min |
| 99.95% | 4.38 h | 21.9 min | 5.04 min |
| 99.99% | 52.6 min | 4.38 min | 1.01 min |
| 99.999% | 5.26 min | 26.3 s | 6.05 s |

- **Serial composition (dependencies in a chain):** `A × B × C`. Three 99.9% deps → max 99.7%. If your SLO > deps' product, you must build redundancy.
- **Parallel composition (redundancy):** `1 − (1 − A)(1 − B)`. Two 99% replicas in parallel → 99.99%.
- **Rule of thumb:** your SLO ≤ (weakest dep's SLO × number of hops). Don't promise users 99.99% when S3 promises you 99.9%.

### Multi-window, multi-burn-rate alerting (Google SRE Workbook, Ch. 5)

- **Burn rate** = rate at which error budget is being consumed. A burn rate of 1× means the budget will last exactly the SLO window; 10× means it'll be fully consumed in 1/10 of the window.
- **Canonical thresholds** (for a 30-day SLO window):

  | Severity | Burn rate | Short window | Long window | Budget consumed to fire |
  |---|---|---|---|---|
  | Page | 14.4× | 5 min | 1 h | 2% in 1h |
  | Page | 6× | 30 min | 6 h | 5% in 6h |
  | Ticket | 3× | 2 h | 24 h | 10% in 1d |
  | Ticket | 1× | 3 h | 72 h | 10% in 3d |

- **Two-window rule:** alert fires only if *both* a short window AND a long window exceed the burn-rate threshold — the short window prevents slow-to-react alerts, the long window prevents flapping.
- **Implementation:** Prometheus recording rules pre-compute burn rate at multiple horizons (`rate(errors[5m])` / `rate(requests[5m])`); alerts reference the recorded metric.
- **Why this beats simple threshold alerts:** catches both fast catastrophic burn (page immediately) and slow quality decay (ticket for investigation) without tuning per service.

### Error budget policies — what actually changes behavior

- **Soft freeze:** budget < 20% remaining → any new deploy requires senior engineer approval.
- **Hard freeze:** budget exhausted → stop feature deploys; reliability work only until budget recovers.
- **Reliability tax:** recurring budget exhaustion → dedicate X% of next quarter's capacity to reliability work proportional to overspend.
- Without a policy, the error budget is a decoration. The *policy* — pre-agreed consequences — is what changes engineering behavior.

### SLO-as-code ecosystem

- **Sloth** (OSS, Prometheus-native): YAML SLO spec → generates recording rules + alert rules. Most popular OSS choice.
- **Pyrra** (OSS, K8s-native CRDs): `ServiceLevelObjective` CRD, controller-driven, UI included.
- **OpenSLO** (spec, not a tool): vendor-neutral YAML SLO specification; tools implement it.
- **Nobl9** (SaaS): commercial SLO platform; unifies metrics sources (Prometheus, Datadog, CloudWatch, etc.).
- **Grafana SLO** (Grafana Cloud feature): SLO objects with burn-rate dashboards + alert generation.
- **Datadog SLO** / **Dynatrace SLO** (SaaS built-ins): works if you're already on-platform.

### Production Readiness Review (PRR) — Google's launch gate

- A formal checklist a service must pass before production traffic. Not a one-time event — reviewed annually for existing services.
- **Categories:** capacity (load tested for 2× peak) · reliability (SLOs defined, error budget policy documented) · observability (metrics + logs + traces + dashboards + alerts) · on-call (rotation, runbooks, escalation) · security (auth, secrets, audit logs) · deployment (rollback plan, canary gates) · dependencies (SLOs of deps, fallback behavior) · data (backup, retention, DR).
- **Exit criteria:** all blocker items closed; non-blocker items tracked with owners and deadlines.
- Adjacent: **launch review** (go/no-go decision), **hardening sprint** (pre-launch reliability investment).

### Incident Command System (ICS) — structured response protocol

- Adapted from FEMA emergency-response for software incidents (popularized by PagerDuty).
- **Roles (per major incident):**
  - **Incident Commander (IC):** owns the incident end-to-end; makes binding decisions; does NOT debug.
  - **Comms Lead:** handles stakeholder updates (status page, Slack, customer-facing), freeing IC to coordinate response.
  - **Scribe:** timeline recorder for postmortem; captures decisions and actions in real-time.
  - **Subject Matter Experts (SMEs):** the engineers doing the debug/fix work, directed by IC.
- **Severity levels (common taxonomy):** SEV1 (complete outage), SEV2 (major degradation), SEV3 (minor), SEV4 (internal-only).
- **Ceremonies:** regular sitrep (situation report) every 15–30 min; handoff protocol when IC or responders change; post-incident review scheduled within 48h.

### Chaos engineering — proactive reliability testing

- **Principles (Netflix / Principles of Chaos Engineering):** build hypotheses about steady-state behavior; vary real-world events in a controlled environment; run experiments in production when possible; minimize blast radius; automate experiments.
- **Tools:** Chaos Monkey (Netflix, kills instances) · Gremlin (SaaS) · LitmusChaos (K8s-native) · Chaos Mesh (K8s-native, CNCF) · AWS Fault Injection Simulator (AWS-native) · Toxiproxy (network fault injection).
- **GameDays:** scheduled team-wide chaos drills; often include a simulated SEV1 to test IC/runbook/comms.
- **Failure modes commonly injected:** instance termination, network latency, packet loss, DNS failure, dependency unavailability, disk fill, CPU starvation, clock skew.

### DR vocabulary — Disaster Recovery targets

- **RTO (Recovery Time Objective):** how long until the service is restored after a disaster. "RTO = 1 hour" means we must be back within an hour.
- **RPO (Recovery Point Objective):** how much data can be lost. "RPO = 5 minutes" means last 5 minutes of writes can be lost in the worst case.
- **DR strategies (increasing cost):** backup-and-restore (cheap, RPO/RTO in hours) → pilot light (minimal standby, minutes) → warm standby (scaled-down live, near-zero) → active-active multi-region (zero RTO/RPO, most expensive).
- **Compliance tie-in:** SOC2 CC9.1 (recovery procedures); ISO 27001 A.17 (business continuity); regular DR drills (quarterly/annual) are audit artifacts.

### Capacity planning & load testing

- **Headroom rule:** maintain 2–3× peak capacity as headroom; alert on sustained >70% utilization.
- **Load testing tools:** k6 (modern, JS-based) · Locust (Python) · JMeter (legacy, Java) · Gatling (Scala) · Vegeta (Go, CLI).
- **K8s autoscaling:** HPA (horizontal pod autoscaling on metrics) · VPA (vertical — adjusts requests/limits) · KEDA (event-driven autoscaling on queue depth, Kafka lag, etc.) · Cluster Autoscaler / Karpenter (node provisioning).
- **Capacity as reliability investment:** unused capacity *is* the budget for handling unexpected load; under-provisioning is a reliability choice, not a cost saving.

### K8s reliability primitives (practical SRE knowledge)

- **Probes:** `readinessProbe` (remove from service rotation when unhealthy) · `livenessProbe` (restart when hung) · `startupProbe` (ignore other probes during slow startup). Misconfigured liveness probe is a common cause of cascading restarts.
- **PodDisruptionBudget (PDB):** `maxUnavailable` / `minAvailable` — ensures voluntary evictions (drain, upgrade) don't take down too many pods at once.
- **Topology Spread Constraints:** spread pods across AZs / nodes for failure isolation. Replaced anti-affinity for most use cases.
- **PriorityClass + PreemptionPolicy:** critical workloads preempt lower-priority ones under capacity pressure.
- **Graceful shutdown:** `terminationGracePeriodSeconds` + PreStop hook; readiness probe should fail *before* SIGTERM so traffic drains first.
- **Resource requests/limits:** QoS classes (Guaranteed / Burstable / BestEffort) drive eviction order when nodes are pressured.

### AWS Well-Architected — Reliability Pillar (4 design principles)

1. **Automatically recover from failure** — health checks + automatic replacement (Auto Scaling, EKS node groups, RDS Multi-AZ failover).
2. **Test recovery procedures** — GameDays, chaos experiments, DR drills. Most orgs fail here.
3. **Scale horizontally to increase aggregate availability** — many small instances beat few large ones for failure tolerance.
4. **Stop guessing capacity** — use AWS auto-scaling + CloudWatch metrics to provision based on demand, not guesses.
- Specific AWS services to name-drop: CloudWatch Metrics + Alarms, CloudWatch Synthetics (external probes), X-Ray (tracing), AWS Health Dashboard, AWS Fault Injection Simulator, Route 53 health checks + failover routing, Multi-Region replication (DynamoDB Global Tables, S3 CRR, Aurora Global).

### SRE for AI/LLM systems — the emerging frontier

- **Availability + latency SLOs transfer directly** to LLM gateways and inference endpoints; the math is the same.
- **New dimension: quality SLOs.** Define semantic thresholds measured via continuous LLM-as-Judge sampling — e.g., "faithfulness ≥ 0.9" or "hallucination rate ≤ 2%." Quality SLO violations burn error budget the same way availability violations do.
- **Observability 2.0 for LLMs:** three-pillar model (Computational / Semantic / Agentic) — see [[LLMOps and AI Pipeline Engineering]].
- **Canary on quality, not just latency:** Argo Rollouts analysis templates can query LLM-as-Judge scores as the gate signal.

### SRE anti-patterns

- **100% SLO** — "downtime is unacceptable." Promises a target you can't meet; removes the ability to ship features. Choose a number with real headroom instead.
- **Vanity SLOs** — measure what's easy (CPU, uptime) not what users experience (successful completion of critical journey). SLI menu exists to fight this.
- **SLOs without an error budget policy** — budget is a number nobody does anything with. No behavior change = no reliability improvement.
- **Alert on causes, not symptoms** — "disk > 80%" alerts train the team to treat symptoms; SLO burn-rate alerts focus on user impact. Still monitor causes as leading indicators, just don't page on them.
- **Runbook-less alerts** — every page without a runbook trains engineers to ignore alerts. Alert hygiene = runbook hygiene.
- **"Hero" incident response** — one senior engineer always firefighting. Scales poorly, creates single-point-of-failure, burns out the hero. Structure via IC + rotation instead.
- **Blameless in name only** — postmortem says "no blame" but the engineer involved is quietly shuffled. Actual blameless culture requires org-level consistency.
- **Toil treated as career-limiting** — if engineers who automate themselves out of a job are less promoted than those who "heroically" carry toil, the incentive is backwards.

### Canonical references

- **Google SRE Book** (free at [sre.google/books](https://sre.google/books/)): foundational; chapters on embracing risk, SLOs, eliminating toil, monitoring, being on-call, postmortem culture, release engineering, load balancing, handling overload, cascading failures, critical state, product launches.
- **Google SRE Workbook** (free): practical companion — Ch. 5 "Alerting on SLOs" is the canonical source for multi-window multi-burn-rate alerting.
- **"Implementing Service Level Objectives"** (Alex Hidalgo, O'Reilly): practitioner-focused SLO guide.
- **"Seeking SRE"** (David Blank-Edelman, O'Reilly): essay collection; diverse perspectives beyond Google's model.
- **John Allspaw** (blog, adaptivecapacitylabs.com): "How Complex Systems Fail" (Cook), Learning-from-Incidents movement, resilience engineering vocabulary.
- **Laura Maguire / Learning From Incidents (LFI)**: modern post-incident cognitive-science framing.
- **PagerDuty Incident Response docs** (response.pagerduty.com): canonical Incident Command protocol for software teams.
- **AWS Well-Architected Framework — Reliability Pillar**: AWS-native reliability design patterns.

## Core Concepts

**SLI / SLO / SLA — the reliability contract stack**
- **SLI** (Service Level Indicator): a quantitative measure of service behavior — e.g., request success rate, p99 latency, availability. Must be measurable from the user's perspective.
- **SLO** (Service Level Objective): the target value for an SLI — e.g., "99% availability over a 30-day rolling window." Owned by the engineering team; defines what "reliable enough" means.
- **SLA** (Service Level Agreement): a contractual commitment with consequences for breach, usually set *below* the SLO to create a safety margin.
- Rule of thumb: SLA < SLO < 100%. The gap between SLO and SLA is the safety margin for remediation before business consequences kick in.
- **eBay context**: K8s API Server SLIs focused on availability and latency. API Server is Control Plane — primarily consumed by the Platform team, not end-users directly — so 99% was the right starting SLO, not 99.9%. Different SLO targets for different tiers: Federated API Server (highest impact, addressed first) vs. Cluster API Server vs. Dev environments.

**Setting SLOs: start feasible, not aggressive**
- Starting with an overly ambitious SLO (99.9% before reliability baseline is known) causes immediate error budget exhaustion, alert fatigue, and demoralization.
- **eBay approach**: started at 99% when the system had frequent incidents; used real data to understand baseline before committing to higher targets. Daily error budget reviews early on to track consumption and identify root causes.
- K8s provides built-in metrics, making SLI instrumentation straightforward for API Server (API request success rate, etcd latency, etc.).
- Complexity driver at eBay: Federated API Server aggregates many clusters; large total call volume; clients without proper APF (API Priority and Fairness) settings can starve each other, causing cascading reliability degradation.

**Error budget — the reliability budget mechanism**
- Error budget = 1 − SLO. A 99% SLO gives 1% budget = 432 minutes/month. Every minute of downtime or SLI breach burns budget.
- When budget is being consumed: trigger root cause investigation. Key question: was it caused by a release/change event, or by a specific client with misconfigured APF?
- Error budget policy: when budget runs low, trigger reliability freeze (no new deployments until budget recovers); when budget is healthy, team has room to take risks and ship features.
- **eBay approach**: early data was noisy, so started with a generous budget threshold (95%), then gradually tightened. Policy reviews triggered by daily dashboards showing consumption rate.

**Alert design: SLO-first, symptom-second**
- Primary alerts should fire on SLI/SLO violations (user-facing symptoms), not on internal metrics. This reduces false positive alert fatigue and ensures on-call focuses on real user impact.
- Secondary alerts fire on leading indicators: API server instance health, etcd health/growth rate — these catch problems *before* SLO is breached.
- Multi-tier alert structure at eBay: (1) SLO burn rate alert → page on-call; (2) API server instance alerts; (3) etcd governance alerts (e.g., etcd unbounded growth was a recurring root cause — required dedicated alerting and SOP).
- Every alert must have a corresponding runbook and SOP. Alerts without runbooks train engineers to ignore them.

**Incident management — structure reduces MTTR**
- Key metrics: **MTTD** (Mean Time to Detect) and **MTTR** (Mean Time to Recover). Both should be minimized; MTTD is often underinvested.
- Escalation path: on-call engineer → tech lead → engineering manager. Clear levels prevent ambiguity about when to escalate.
- 24/7 pager with complete runbook coverage: every known failure mode has a documented triage path, recovery procedure, and rollback plan.
- At eBay, specific incident patterns (APF misconfiguration, etcd governance failures) were root-caused, documented in SOPs, and had dedicated alerts added post-incident. Each RCA made the next incident of the same type faster to resolve.

**Blameless post-mortems — making RCA compound**
- RCA template focus: what in the *system* allowed this to happen? Why was MTTD/MTTR high? What changes prevent recurrence? Avoid "who made the mistake."
- Centralized RCA repository: all past incidents in one place, searchable. New on-call engineers can understand failure patterns before experiencing them live.
- Every RCA produces follow-up action items with named owners and deadlines. Actions without owners are observations, not improvements. Track action completion rate as a team health metric.
- **eBay practice**: recognized team effort publicly when reliability milestones were hit. Blameless culture only works if the organization also celebrates progress — not just investigates failures.

**Toil reduction — eliminating repetitive operational work**
- Google SRE definition of toil: manual, repetitive, automatable work that grows linearly with service scale and provides no lasting value.
- Operational threshold: if toil exceeds ~50% of on-call time, it crowds out reliability engineering work and causes burnout.
- **eBay classification**: work that consumes on-call time, has no SOP, and recurs regularly = toil. Primary K8s API Server toil: triage for degraded/bad instances and release-caused reliability events.
- **AI-powered triage at eBay**: MCP server collects metrics and logs; AI agent performs combined diagnosis. Reduces the time from alert to root-cause hypothesis from 20–30 min to near-instant for known failure patterns. Allows junior on-call engineers to handle incidents that previously required senior escalation.
- Platform investment to eliminate toil permanently: build automation and tooling so that the next occurrence of a known failure is resolved without human triage.

**On-call design — coverage without burnout**
- On-call models: **follow-the-sun** (regional handoff every 12h, no one wakes up) vs. **primary/secondary** (24h primary who pages secondary when needed). Follow-the-sun is better for engineer wellbeing; requires coverage in enough timezones.
- **eBay evolution**: started with US/China follow-the-sun (12h each). After China lost production access, shifted to primary/secondary with India/Europe as secondary while gradually building their capability toward follow-the-sun again.
- Escalation design should be explicit, not assumed. On-call person should know exactly when to escalate and to whom within minutes of an unresolved page.
- Work-life balance principle: no engineer should be on-call more than 25% of their time. Sustained over-on-call drives attrition on the best engineers (those most able to find new roles).

**SRE team model — embedded vs. centralized**
- **Centralized SRE**: dedicated SRE team owns reliability across services. Risk: SRE becomes an ops dumping ground; dev teams offload reliability work.
- **Embedded SRE**: SREs join product/infra teams directly. Risk: SRE practices fragment across teams; no shared tooling.
- **Hybrid (eBay model)**: embedded SREs with *rotation* (team members take on SRE responsibilities on rotation); centralized SRE team provides tooling, best practices, and standards. Rotation builds reliability ownership across the broader team rather than concentrating it in specialists.
- Reliability tickets belong in the sprint backlog, not a separate track. Team OKRs included toil reduction, MTTD/MTTR improvement, and SLO attainment. This makes reliability work visible and comparable to feature work.

**Reliability culture — shifting ownership left**
- Key principle: every engineer on-calls for the systems their team builds. Rotating on-call builds empathy and ownership; dedicated ops teams create a "throw it over the wall" dynamic.
- Encourage feature work that permanently resolves reliability problems, not just patches that defer the issue. "Fix the system, not the symptom."
- Data-driven prioritization: identify top 3 reliability drivers, fix those first. Don't spread effort across 10 issues simultaneously.

## Key Questions

**Q: How do you define SLOs for a service, and how do you pick the right target?**
Answer framework: Start with SLI selection — what metrics matter to users (availability, latency p99, error rate). Set the SLO based on the service's role and user impact: Control Plane / platform services can tolerate 99%; user-facing critical services might need 99.9%. At eBay, the K8s Federated API Server started at 99% because the primary consumers were platform engineers, not end-users, and the initial baseline was unknown. Starting conservative (then raising) beats starting aggressive (and immediately exhausting budget). Distinguish SLO (engineering target) from SLA (business contract with a safety margin below the SLO).

**Q: What is an error budget, and how does it influence team behavior?**
Answer framework: Error budget = 1 − SLO. It gives the team a quantified "risk allowance" — while budget is healthy, the team can ship aggressively; when budget runs low, trigger reliability freeze and root-cause investigation. The policy shifts behavior: instead of debating "is this deployment too risky?", the question becomes "how much budget do we have?". At eBay, daily budget reviews early in the reliability journey helped identify whether consumption was coming from release events or from client-side APF misconfigurations — two very different interventions.

**Q: How did you structure incident management at eBay? What reduced MTTR most?**
Answer framework: Multi-tier alerts (SLO burn rate as primary, component health as secondary); runbooks for every known failure mode; 24/7 pager with explicit escalation path (on-call → tech lead → EM). The biggest MTTR reduction came from (1) investing in runbook quality after each incident so the next occurrence was faster, and (2) AI-assisted triage (MCP server + AI agent analyzing metrics and logs) for known failure patterns, reducing time-to-diagnosis from ~30 minutes to near-instant. Track MTTD separately from MTTR — many teams optimize recovery but not detection.

**Q: How do you run blameless post-mortems? What makes them effective?**
Answer framework: Template focuses on system failure (not individual error): what allowed this to happen, why was MTTD/MTTR high, what changes prevent recurrence. Centralize all RCAs so institutional knowledge compounds. Every RCA must produce named-owner action items with deadlines — observations without owners are not improvements. Track action completion rate. At eBay, the centralized RCA repository meant new on-call engineers could study past failure patterns before encountering them live, significantly reducing escalation rate.

**Q: What counts as toil and how do you reduce it?**
Answer framework: Toil = repetitive, manual, automatable work that grows linearly with scale and provides no durable value. At eBay, the primary K8s API Server toil was incident triage — diagnosing bad instances and release-caused degradation without a documented SOP. Eliminated it in two ways: (1) built SOPs and runbooks that made triage deterministic; (2) built AI-assisted triage using MCP server + AI agent to collect metrics/logs and diagnose known patterns automatically. Measure toil as % of on-call time; if > 50%, it's crowding out reliability engineering. Fix by building platform automation, not by adding on-call headcount.

**Q: How do you design on-call to prevent burnout while maintaining coverage?**
Answer framework: Preferred model is follow-the-sun (no one wakes up for incidents outside their timezone) but requires geographic distribution. At eBay, pivoted from US/China follow-the-sun to primary/secondary when China lost production access, with India/Europe as secondary while building their capability. Two hard rules: no engineer on-call > 25% of their time, and every page must have a runbook — undocumented pages train engineers to ignore alerts. Escalation path (on-call → tech lead → EM) must be explicit and time-boxed.

**Q: How do you build a reliability culture without a dedicated SRE team?**
Answer framework: Rotate on-call across all team members — this builds ownership and empathy faster than any process. Put reliability tickets in the sprint backlog alongside feature work — if it's not in the sprint, it doesn't get done. Use team OKRs to make reliability improvements measurable: reduce toil X%, improve MTTD from Y to Z min, hit SLO target. At eBay, the combination of rotation + OKRs + centralized tooling from the SRE platform team created a culture where engineers saw reliability work as core to their role, not as ops overhead. Blameless culture requires publicly recognizing reliability wins, not just investigating incidents.

### Industry-Baseline Questions (textbook)

**Q: Walk me through how you'd pick SLIs for a new service.**
Answer framework: Start from the SLI menu — Availability, Latency, Freshness, Correctness, Quality, Throughput, Coverage, Durability — and select based on what users experience. For a request-driven API, Golden Signals (Latency/Traffic/Errors/Saturation) or RED (Rate/Errors/Duration) is the default; for a batch pipeline, Freshness + Correctness + Coverage; for storage, Availability + Durability. Measure at the point the user experiences the service (load-balancer / API-gateway), not server-side (which hides network/TLS/DNS failures). Avoid vanity SLIs that are easy to measure but don't reflect user impact.

**Q: How do multi-window multi-burn-rate alerts work, and why are they better than simple thresholds?**
Answer framework: Burn rate = rate of error-budget consumption; 1× means the budget lasts exactly the SLO window, 10× means it'll be exhausted in 1/10 of the window. Canonical thresholds (Google SRE Workbook): 14.4× for 5-min-and-1-hour (page), 6× for 30-min-and-6-hour (page), 3× for 2-hour-and-1-day (ticket), 1× for 3-hour-and-3-day (ticket). The two-window rule (short AND long must both exceed) prevents flapping and slow-to-react alerts. Implemented as Prometheus recording rules that pre-compute burn rate at multiple horizons. Better than simple thresholds because it catches both fast catastrophic burn and slow quality decay without per-service tuning.

**Q: If your service depends on 3 downstream services each at 99.9%, what's the best SLO you can commit to?**
Answer framework: Serial composition — multiply the dependency SLOs. `0.999 × 0.999 × 0.999 ≈ 0.997` = 99.7%. If you promise users 99.9%, you *cannot* meet it without adding redundancy. Options: (1) add parallel redundancy (`1 − (1−A)(1−B)` gets 99.9999% from two 99.9% replicas), (2) add caching/fallback to tolerate dep outages, (3) renegotiate the user-facing SLO to be realistic. The anti-pattern is committing to 99.9% and hoping — that's an error-budget trap.

**Q: Walk me through Incident Command during a SEV1.**
Answer framework: Three roles, one person each — **Incident Commander** owns coordination and decisions (does NOT debug), **Comms Lead** handles stakeholder updates (status page, customer-facing Slack, execs), **Scribe** captures timeline + decisions for the postmortem. Subject Matter Experts do the actual debug/fix work directed by IC. Ceremonies: regular sitrep every 15–30 min, explicit handoff protocol when roles change, postmortem scheduled within 48h. This structure scales beyond the "one hero debugs while three people ask them questions" anti-pattern.

**Q: What is a Production Readiness Review, and what would be on your checklist?**
Answer framework: A formal launch gate — categories typically cover: capacity (load-tested for 2× peak), reliability (SLOs defined + error budget policy), observability (metrics + logs + traces + dashboards + alerts + runbooks), on-call (rotation, escalation path), security (auth, secrets, audit logs), deployment (canary + rollback plan), dependencies (dep SLOs known + fallback behavior), and data (backup + retention + DR). Exit = all blockers closed; non-blockers tracked with owners. At Google the PRR is reviewed annually even for existing services — it's not a one-time gate.

**Q: What's the difference between RTO and RPO? How do they drive DR strategy?**
Answer framework: RTO = recovery time (how long until service is restored). RPO = recovery point (how much data can be lost). Tighter targets cost more: backup-and-restore (RTO/RPO in hours, cheap) → pilot light (minutes) → warm standby (near-zero) → active-active multi-region (zero, most expensive). Choose based on business impact, not engineering preference. Tie-in: SOC2 CC9.1 requires documented recovery procedures; regular DR drills (quarterly/annual) are the audit artifact that proves the procedure works.

**Q: How do you monitor and alert on LLM-based services? How does SRE apply to AI systems?**
Answer framework: Availability and latency SLOs transfer directly to the LLM gateway and inference endpoints — same SLI/SLO/error-budget math. The new dimension is *quality SLOs*: define semantic thresholds (faithfulness ≥ 0.9, hallucination rate ≤ 2%) measured via continuous LLM-as-Judge sampling of production traces. Quality SLO violations burn error budget the same way availability does. Observability follows the three-pillar model (Computational, Semantic, Agentic) — traditional APM only covers the first. Canary rollouts gate on quality scores, not just error rate (Argo Rollouts AnalysisTemplate querying a quality metric). This is where SRE bridges into LLMOps — see [[LLMOps and AI Pipeline Engineering]].

**Q: What are the most common SRE anti-patterns you've seen?**
Answer framework: **100% SLO** (removes the ability to ship), **vanity SLOs** (measuring what's easy not what users experience), **SLOs without an error-budget policy** (no behavior change = no improvement), **alerting on causes instead of symptoms** (train the team to firefight CPU alerts instead of user-impact alerts), **runbook-less alerts** (train engineers to ignore pages), **hero-mode incident response** (single point of failure, burns out the hero), **blameless in name only** (postmortem says no blame but the engineer is quietly shuffled). For each, the fix is structural not cultural — the anti-pattern persists until the mechanism is replaced.

## Summary

SRE practices provide a systematic framework for managing reliability as an engineering problem rather than an ops firefighting exercise. The SLI/SLO/error budget stack is the foundation: SLIs measure service behavior from a user perspective, SLOs set the target, and error budgets convert reliability into a quantified risk allowance that directly governs deployment velocity. The key insight is that reliability and feature velocity are in tension — error budgets make that tension explicit and data-driven rather than political. At eBay, the K8s API Server reliability turnaround applied this framework to a complex control-plane service: starting with a feasible 99% SLO (not aggressive), identifying the top root causes (APF misconfigurations, etcd governance failures), building SOPs for each, and gradually tightening targets as baseline improved from frequent incidents to 99%/99.9% (Dev/Production) on a 30-day rolling window.

The operational practices that have the most leverage are: (1) alert design — primary alerts on SLO burn rate (user-visible symptoms), secondary on component health (leading indicators); (2) runbook discipline — every alert must have a corresponding SOP or it becomes noise; (3) blameless RCAs with centralized tracking and named-owner action items — this is how institutional reliability knowledge compounds rather than repeating. Toil reduction is a force multiplier: eliminating repetitive manual work (through SOPs, automation, and AI-assisted triage) frees on-call capacity for reliability engineering rather than firefighting. At eBay, MCP-powered AI triage reduced diagnosis time for known failure patterns from ~30 minutes to near-instant, enabling junior engineers to handle incidents that previously required senior escalation.

Building reliability culture requires structural investment, not just tooling: rotating all engineers through on-call builds ownership; reliability OKRs make improvement measurable; centralized RCA repositories make learning compound across the team. The SRE team model that works at scale is hybrid — embedded rotation builds ownership in each team, while a centralized SRE platform team provides tooling and standards. The anti-pattern to avoid is dedicated SRE specialists who absorb all on-call load: this creates a "throw it over the wall" dynamic where dev teams stop owning reliability outcomes.

## Key Terms

**Reliability contract**
- `SLI` · `SLO` · `SLA` · `error budget` · `burn rate` · `error-budget policy` · `soft freeze` · `hard freeze` · `reliability tax`

**SLI specification frameworks**
- `SLI menu` (Availability · Latency · Freshness · Correctness · Quality · Throughput · Coverage · Durability) · `Golden Signals` · `RED method` · `USE method` · `VALET`

**SLO types & composition**
- `event-based SLO` · `window-based SLO` · `user-journey SLO` · `critical-path SLO` · `serial composition` · `parallel composition` · `dependency SLO` · `the 9s` (99.9 / 99.99 / 99.999)

**Burn-rate alerting**
- `multi-window multi-burn-rate` · `14.4× / 6× / 3× / 1×` · `two-window rule` · `page vs ticket severity` · `Prometheus recording rule` · `exemplars`

**SLO-as-code**
- `Sloth` · `Pyrra` · `OpenSLO` · `Nobl9` · `Grafana SLO` · `Datadog SLO` · `Dynatrace SLO`

**Measurement & observability**
- `server-side vs LB-side vs synthetic vs RUM` · `sampling` · `high-cardinality` · `histogram` · `percentile` · `rate/increase` · `Prometheus` · `OpenTelemetry` · `CloudWatch` · `X-Ray`

**Incident Command System**
- `Incident Commander (IC)` · `Comms Lead` · `Scribe` · `SME` · `sitrep` · `handoff protocol` · `SEV1 / SEV2 / SEV3 / SEV4` · `48h postmortem window`

**Incident metrics**
- `MTTD` · `MTTR` · `MTBF` · `RCA` · `follow-up action item` · `blameless postmortem` · `centralized RCA repo`

**Production Readiness**
- `PRR (Production Readiness Review)` · `launch review` · `hardening sprint` · `blocker vs non-blocker` · `annual re-review`

**Chaos engineering**
- `Principles of Chaos` · `blast radius` · `steady-state hypothesis` · `Chaos Monkey` · `Gremlin` · `LitmusChaos` · `Chaos Mesh` · `AWS FIS` · `Toxiproxy` · `GameDay`

**Disaster Recovery**
- `RTO` · `RPO` · `backup-and-restore` · `pilot light` · `warm standby` · `active-active` · `multi-region` · `region failover` · `SOC2 CC9.1` · `ISO 27001 A.17`

**Capacity & load**
- `headroom` · `70% utilization rule` · `k6` · `Locust` · `JMeter` · `Gatling` · `Vegeta` · `soak test` · `spike test`

**K8s reliability primitives**
- `readinessProbe` · `livenessProbe` · `startupProbe` · `PodDisruptionBudget (PDB)` · `topology spread constraints` · `PriorityClass` · `preemption` · `terminationGracePeriodSeconds` · `PreStop hook` · `QoS class` (Guaranteed / Burstable / BestEffort) · `HPA` · `VPA` · `KEDA` · `Cluster Autoscaler` · `Karpenter`

**AWS reliability**
- `Well-Architected Reliability Pillar` · `Auto Scaling Group` · `Multi-AZ RDS` · `DynamoDB Global Tables` · `S3 CRR` · `Aurora Global` · `Route 53 health checks` · `CloudWatch Synthetics` · `AWS Health Dashboard` · `AWS FIS`

**SRE team models**
- `centralized SRE` · `embedded SRE` · `hybrid / rotation` · `on-call rotation` · `follow-the-sun` · `primary/secondary` · `25% on-call cap` · `toil` · `50% toil ceiling` · `sprint-backlog reliability work`

**AI/LLM SRE**
- `quality SLO` · `LLM-as-Judge SLI` · `faithfulness threshold` · `three-pillar observability` · `canary on quality score`

**Anti-patterns**
- `100% SLO` · `vanity SLO` · `alert on causes (not symptoms)` · `runbook-less alert` · `hero-mode response` · `blameless in name only` · `toil as career-limiting` · `SLOs without policy`

**Key references**
- `Google SRE Book` · `SRE Workbook Ch. 5` · `Hidalgo — Implementing SLOs` · `Seeking SRE` · `Allspaw / How Complex Systems Fail (Cook)` · `Learning From Incidents (LFI)` · `PagerDuty Incident Response` · `AWS Well-Architected`

## Raw Material
- [[raw_material/tech/infra/SRE Practices and SLO Engineering - personal]]
