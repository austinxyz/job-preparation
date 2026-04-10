---
title: Observability and Incident Management
category: tech/infra
tags: [observability, monitoring, sre, incident-response, alerting, debugging, slo, sli, on-call]
status: in-progress
priority: high
last_updated: 2026-04-10
created_from_jd:
---

# Observability and Incident Management

## Knowledge Map
- Prerequisites（前置知识）：[[Kubernetes]], [[Distributed Systems]]
- Related Topics（延伸话题）：[[Service Mesh and Istio]], [[Cloud Computing Fundamentals]], [[K8s Control Plane]]
- Management（管理关联）：[[Engineering Team Management]], [[Technical Roadmap]]

## Core Concepts

**The Three Pillars of Observability**
- **Metrics**: numeric time-series data (CPU, latency, error rate, saturation); Prometheus is the standard for cloud-native
- **Logs**: discrete events with context (structured JSON preferred over plaintext); Fluentd/Vector → Elasticsearch (Loki) aggregation
- **Traces**: distributed request traces across services; OpenTelemetry is the standard instrumentation API; Jaeger/Tempo for storage
- Golden signals (Google SRE): **Latency**, **Traffic**, **Errors**, **Saturation** — instrument these four for any new service

**SLI / SLO / SLA / Error Budget**
- **SLI** (Service Level Indicator): the metric you measure (e.g., 99th percentile latency, availability %)
- **SLO** (Service Level Objective): the target for that metric (e.g., 99.9% of requests succeed)
- **SLA** (Service Level Agreement): the contractual commitment to customers; usually less strict than internal SLO
- **Error Budget**: 100% minus SLO; the allowed "failure budget" per period; if burned, freeze features, invest in reliability
- Error budget policy turns reliability vs. velocity into a data-driven conversation, not an opinion fight

**Instrumentation in Kubernetes**
- Metrics: Prometheus client libraries (expose /metrics endpoint); `kube-state-metrics` (K8s object state), `cAdvisor` (per-container resource usage), `node-exporter` (host metrics)
- Logs: Fluent Bit (lightweight) or Fluentd as DaemonSet → aggregator → Elasticsearch/Loki; structured JSON for queryability
- Traces: OpenTelemetry SDK + collector; export to Jaeger/Tempo/OTLP-compatible backend
- K8s events: `kubectl get events` for cluster-level operational events (pod evictions, scheduling failures)

**Alerting Best Practices**
- Alert on symptoms (user-visible impact) not causes; cause-based alerts create noise without actionability
- SLO-based alerting: alert when error budget burn rate is too high (e.g., 5% of budget burned in 1 hour)
- Alert fatigue: too many alerts → engineers stop responding; regular alert audit/tuning, only actionable alerts
- Runbooks: every alert must have a documented remediation path; otherwise it shouldn't alert

**Debugging Kubernetes**

Structured debugging flow:
1. `kubectl get pods -n <namespace>` → identify problematic pod
2. `kubectl describe pod <pod>` → read Events section (OOMKilled, ImagePullBackOff, probe failures, scheduling issues)
3. `kubectl logs <pod> --previous` → crashed container logs
4. Check resource limits (OOM → increase memory limit or fix memory leak)
5. Check liveness/readiness probe configs (false kills → adjust `initialDelaySeconds`, `timeoutSeconds`)
6. Check node status: `kubectl describe node <node>` → disk/memory pressure, taints

**Debugging Network Issues in Kubernetes**
- Tools: `kubectl exec` → `ping`, `curl`, `nslookup`, `dig` for DNS; `tcpdump` inside pod for packet capture
- Check NetworkPolicy: is traffic being blocked by a policy rule?
- Check Service endpoints: `kubectl get endpoints <service>` → empty = no matching pods (label selector mismatch)
- CNI plugin issues: check CNI pod logs (Calico, Cilium node pods)
- DNS latency: check CoreDNS pod logs and resource limits; `ndots` configuration in pod spec

**Incident Response Process**
1. **Detect**: alert fires or customer report; assign SEV (1 = revenue impact/complete outage, 2 = degraded, 3 = minor)
2. **Triage**: is it still happening? What's the blast radius? Who is impacted?
3. **Mitigate first**: rollback, feature flag toggle, traffic shift — stop the bleeding before diagnosing the root cause
4. **Communicate**: internal status page, stakeholder Slack channel, customer status page (for external incidents)
5. **Resolve**: identify and fix underlying cause (may be separate from mitigation)
6. **Postmortem**: blameless — focus on system, process, tooling failures, not individual error; action items with owners/deadlines; share learnings broadly

**On-call Health**
- Rotation: distribute on-call load; avoid single-hero patterns; provide context documents (runbooks, architecture diagrams)
- Alert tuning: quarterly audit of firing alerts; suppress or delete alerts without runbooks; set proper thresholds with real data
- Toil reduction: automate repetitive on-call tasks; track toil as a metric and set reduction targets

**Multi-tier alert hierarchy — SLO-first design**
- Tier 1 (page on-call): SLO burn rate alert — user-visible impact, the thing that matters most. Fires when error budget is being consumed faster than the SLO allows.
- Tier 2 (warning/ticket): Component health indicators — API server instance health, etcd latency/growth, memory pressure. These are leading indicators that may precede an SLO breach.
- Tier 3 (informational): Capacity and trend signals — gradual resource growth, slow error rate creep. Don't page, but should appear on dashboards for weekly review.
- Design principle: Tier 1 alerts are always accompanied by a runbook with a triage path and rollback procedure. An alert without a runbook is a placeholder, not a real alert.
- **eBay practice**: APF (API Priority and Fairness) misconfigurations and etcd unbounded growth each caused major incidents → both got dedicated Tier 2 alerts and SOPs *after* the first incident. "Every incident should make the next one cheaper to handle."

**K8s Control Plane observability specifics**
- API Server key metrics: `apiserver_request_total` (by verb, resource, code), `apiserver_request_duration_seconds` (latency by verb), `apiserver_current_inflight_requests` (APF queue depth), `etcd_request_duration_seconds`.
- etcd metrics: `etcd_db_total_size_in_bytes` (DB size — if unconstrained, can OOM etcd), `etcd_disk_wal_fsync_duration_seconds` (disk latency; spikes indicate storage pressure), `etcd_server_proposals_failed_total` (Raft consensus failures).
- APF (API Priority and Fairness): K8s 1.20+ flow control mechanism that queues/prioritizes API requests by PriorityLevelConfiguration. Without proper APF settings, a chatty controller can exhaust the API Server queue and starve other clients. Monitor `apiserver_flowcontrol_rejected_requests_total` and `apiserver_flowcontrol_current_executing_requests`.
- **eBay incident pattern**: poorly configured APF for network controllers and app release pipelines caused API Server throughput collapse under bursty load → fix: instrument APF per-flow metrics, tune PriorityLevelConfigurations per client type, alert on rejection spikes.
- etcd governance: without explicit compaction and defragmentation schedules, etcd DB grows unboundedly → triggers OOM or fills disk → API Server becomes unavailable. Automate `etcdctl compact` + `etcdctl defrag` on schedule; alert on DB size thresholds.

**Error budget burn rate alerting — the mechanics**
- Burn rate = how fast you're consuming the error budget relative to the SLO window. A burn rate of 1 = exactly on track (budget used at the rate that would exactly exhaust it at window end). A burn rate of 2 = consuming 2× faster than sustainable.
- Alert thresholds (Google SRE recommendation for 30-day window):
  - Burn rate > 14 (1 hour window) → page immediately (2% budget gone in 1 hour)
  - Burn rate > 6 (6 hour window) → page (5% budget gone in 6 hours)
  - Burn rate > 3 (1 day window) → ticket
  - Burn rate > 1 (3 day window) → informational
- Why burn rate over raw thresholds: self-calibrating (10 errors/min is catastrophic on a lightly-loaded service, fine on one handling 10k req/min), and tied directly to business impact (SLO).

**AI-assisted triage — reducing toil at the detection layer**
- Pattern: monitoring system (Prometheus/Sherlock) fires an alert → MCP server collects the relevant metrics, logs, and event stream for the affected component → AI agent synthesizes a diagnosis and suggests the most likely root cause and next investigation step.
- Value: reduces MTTD for known failure patterns from ~20-30 min (engineer wakes up, orients, reads dashboards) to near-instant. Enables junior on-call engineers to handle incidents that previously required senior escalation.
- **eBay implementation**: MCP server pulls K8s API Server metrics (APF queue depth, etcd latency, error rate) + relevant logs (apiserver, etcd, controller logs) → AI agent classifies the incident type (APF saturation / etcd issue / client misbehavior / network) and surfaces the matching SOP.
- Limitation: AI triage handles *known* failure patterns well; novel/complex incidents still require senior engineer judgment. AI reduces the first-response burden, not the deep diagnosis burden.
- Organizational benefit beyond speed: reduces on-call burnout by removing the cognitive load of "what do I even look at first?" at 3am.

**Centralized RCA management — making institutional knowledge compound**
- Every RCA lives in one searchable place (Confluence, Notion, internal wiki). Structure: timeline, root cause, contributing factors, detection gap (why MTTD was high), mitigation steps, follow-up actions with owners and due dates.
- Action items are tracked separately with a completion rate metric. An RCA that produces 3 unresolved action items for 3 months is worse than no RCA — it creates false confidence.
- New on-call engineers should be able to study the RCA repository before going on-call live. This is the fastest onboarding path for incident response quality.
- Pattern-based learning: if the same root cause recurs in multiple RCAs (etcd growth, APF misconfiguration, cert expiry), it signals a systemic gap — a platform feature or automation investment is overdue, not another SOP.

**On-call rotation models and evolution**
- **Follow-the-sun**: each regional team covers a business-hours shift (e.g., US covers 8am–8pm PST, China covers the other 12h). No one wakes up for incidents. Requires meaningful timezone coverage (>= 2 regions, ~12h apart).
- **Primary/Secondary**: 24h primary who handles all alerts; secondary escalation for incidents the primary can't resolve within N minutes. Simpler to staff; primary does sometimes wake up.
- **eBay evolution**: started follow-the-sun (US + China). When China team lost production access, pivoted to primary/secondary with India/Europe as secondary, while building those teams toward follow-the-sun capability. The lesson: on-call model must adapt to org structure realities; don't force a model that requires access/coverage you don't have.
- Burnout prevention: enforce < 25% on-call time per engineer; mandatory off-call recovery after high-incident periods; track pager volume per rotation slot and flag outliers.

## Key Questions

**Q: How would you instrument an application in Kubernetes for observability?**
Answer framework: Metrics — embed Prometheus client, expose /metrics, add kube-state-metrics and node-exporter for cluster/node visibility; Logs — structured JSON, Fluent Bit DaemonSet → centralized storage; Traces — OpenTelemetry SDK for distributed tracing; instrument the four golden signals (latency, traffic, errors, saturation) for every new service.
> 中文提示：三大支柱：指标（Prometheus）+ 日志（结构化 JSON + Fluent Bit）+ 追踪（OpenTelemetry）；四个黄金信号优先

**Q: What metrics and logs would you collect to monitor Kubernetes node and workload health?**
Answer framework: Node-level — CPU/memory/disk/network usage (node-exporter), kubelet metrics; Pod-level — resource usage (cAdvisor), restart count, readiness/liveness probe failures; Cluster-level — kube-state-metrics (pod states, deployment status); Application — custom /metrics endpoint; Logs from containers + K8s events.
> 中文提示：node-exporter 节点指标，cAdvisor Pod 指标，kube-state-metrics K8s 对象状态；三层都要覆盖

**Q: Describe how you would troubleshoot a Kubernetes pod that is continuously restarting.**
Answer framework: `kubectl logs --previous` for the crash log; `kubectl describe pod` Events section (OOMKilled, probe failure, image issue); check resource limits if OOMKilled; check liveness probe `initialDelaySeconds` if probes fire too early; check init container logs; look at recent deployment changes with `kubectl rollout history`.
> 中文提示：--previous 看崩溃日志；describe 看 Events；OOMKilled 调内存 limit；probe 太早杀调 initialDelaySeconds

**Q: How would you troubleshoot intermittent network latency in a containerized application?**
Answer framework: `kubectl exec` → `tcpdump`/`curl` latency measurement; check DNS resolution time (CoreDNS pressure?); use eBPF tools (bpftrace, Cilium Hubble) for per-flow latency breakdown; check NetworkPolicy for unintended traffic patterns; look for noisy neighbor resource contention on the node; check CNI plugin metrics.

**Q: How would you handle a zero-day vulnerability in a critical edge component (e.g., OpenSSL)?**
Answer framework: Detect (CVE scanner alert or security advisory); assess blast radius (which services use this version?); patch in staging first with regression tests; phased rollout (canary → staging → prod per region); communicate timeline to stakeholders; update runbook; post-migration: add CVE scanning to CI/CD pipeline to catch future issues earlier.
> 中文提示：先评估影响范围（哪些服务受影响），staging 验证后分阶段推，同步更新 CI/CD 扫描流水线

**Q: What strategies ensure high availability and minimal downtime in Kubernetes workloads?**
Answer framework: Readiness/Liveness probes (only route traffic to healthy pods); PodDisruptionBudgets (limit voluntary disruption during node upgrades); pod topology spread (zone-aware scheduling); HPA for load-driven scaling; multi-AZ deployment; canary/blue-green rollouts; chaos testing (Chaos Mesh) to validate failure handling.
> 中文提示：PDB 保护计划内中断（节点升级）；topology spread 保证跨 AZ 分布；chaos testing 主动验证

**Q: How do you handle on-call rotations and reduce alert fatigue?**
Answer framework: SLO-based alerting (alert on burn rate, not raw error count — self-calibrating); regular alert audits (delete alerts without runbooks); only actionable alerts page (if you can't do anything at 3am, don't alert); clear escalation policy; postmortem for every SEV1/2 with alert review; measure on-call toil as a KPI.
> 中文提示：基于错误预算消耗速率告警（burn rate），不基于阈值；没有 runbook 的告警不应该 page

**Q: Describe how you would design a logging and metrics pipeline for thousands of Kubernetes nodes.**
Answer framework: Per-node — Fluent Bit (lightweight DaemonSet) for log forwarding, node-exporter for host metrics; Cluster-level — Prometheus (or VictoriaMetrics for scale) with remote write to long-term storage (Thanos, Cortex); Log aggregation — Elasticsearch or Loki; Tiered retention — hot (7 days), warm (30 days), cold (S3 Glacier); alert via Alertmanager → PagerDuty/Slack.
> 中文提示：Fluent Bit DaemonSet 轻量采集日志；Prometheus + Thanos/Cortex 解决长期存储；分层存储控成本

**Q: How would you monitor K8s API Server health and prevent it from becoming a reliability bottleneck?**
Answer framework: Instrument the four golden signals on the API server (request rate, error rate, latency by verb, saturation via APF queue depth). Add etcd-specific metrics (DB size, disk fsync latency, proposal failures). Set up APF monitoring per flow/priority level to detect client starvation — `apiserver_flowcontrol_rejected_requests_total` is the canary. Establish etcd compaction/defrag on schedule and alert on DB size. Tier alerts: SLO burn rate pages on-call; APF rejection spikes and etcd size thresholds create tickets. Close with: "at eBay, every major API Server incident we had became a new tier-2 alert and SOP — the goal is to make each incident the last time it surprises anyone."

**Q: How have you used AI to improve incident response? What are the limits?**
Answer framework: Describe the MCP + AI agent pattern: monitoring fires → MCP server collects metrics/logs for affected component → AI agent classifies incident type and surfaces the matching SOP. Quantify: MTTD for known patterns reduced from ~30 min to near-instant; junior engineers can handle incidents that previously required senior escalation. Limits: works well for known patterns, not novel failures; AI diagnosis must be validated against real data before acting; doesn't replace senior judgment on complex incidents. Close with: "the goal is to remove the cognitive overhead of 'what do I look at first?' at 3am — not to automate the decision-making."

**Q: What's the difference between alerting on error rate vs. SLO burn rate? Which would you implement?**
Answer framework: Error rate threshold (e.g., alert if error rate > 1%) is brittle — doesn't calibrate to traffic volume, fires spuriously on low-traffic periods, doesn't connect to user impact. SLO burn rate alerts on how fast the error budget is being consumed: burn rate 14× for 1 hour = 2% of monthly budget gone, warranting an immediate page. Self-calibrating to traffic, directly tied to business impact, fewer false positives. Implement multi-window burn rate (1h + 6h fast-burn; 1d slow-burn) so you catch both sudden outages and gradual degradation. This is the Google SRE approach.

**Q: Walk me through how you run a post-mortem. What makes one effective vs. ineffective?**
Answer framework: Structure — timeline, root cause, contributing factors, MTTD/MTTR analysis, follow-up actions with named owners and deadlines. What makes it effective: blameless framing (the system allowed this; what did the system lack?); concrete action items that actually ship (track completion rate); centralized repository so new engineers can study failure patterns before encountering them live. What makes it ineffective: observations without owners ("we should improve monitoring" with no assignee); blame that causes engineers to downplay future incidents; no follow-up on previous RCA actions. At eBay, centralized RCAs meant recurring patterns (APF, etcd) eventually triggered platform investments, not just new SOPs.

## Summary

Observability is what enables you to understand a system's behavior without being in the room when it breaks. For infrastructure teams, the three pillars (metrics, logs, traces) plus SLO/error-budget thinking form the operational foundation. The critical shift is from reactive firefighting (alert on causes, respond to noise) to proactive reliability management (alert on user-visible symptoms, use error budgets to govern the reliability vs. velocity tradeoff). SLO burn rate alerting — rather than raw threshold alerting — is self-calibrating to traffic volume and directly tied to business impact: a 14× burn rate over 1 hour means 2% of monthly budget consumed, warranting an immediate page regardless of the absolute error count. For Kubernetes specifically, the debugging workflow — describe/logs/events → resource limits → probe configs → networking — is a repeatable procedure that resolves 80% of pod issues. For incidents, the discipline of "mitigate first, diagnose second" prevents prolonged outages caused by teams investigating while users suffer.

K8s control plane observability adds specific complexity: API Server health requires monitoring APF (API Priority and Fairness) queue depth per flow, not just aggregate error rate, because a single poorly-configured client can starve all others. etcd requires proactive governance — compaction and defragmentation schedules — or DB growth eventually causes OOM/disk failure, taking down the API Server. At eBay, major K8s API Server incidents from APF misconfiguration and etcd growth each became new alerts and SOPs, reflecting the principle: every incident should make the next one cheaper to handle. AI-assisted triage (MCP server collecting metrics/logs → AI agent classifying incident type and surfacing the matching SOP) reduced MTTD for known failure patterns from ~30 minutes to near-instant, enabling junior on-call engineers to handle incidents that previously required senior escalation.

Effective incident management requires structure at three levels: in the moment (multi-tier alert hierarchy, runbooks for every alert, clear escalation path, mitigate before diagnosing), after the fact (blameless RCAs with named-owner action items in a centralized repository), and over time (track action completion rate, identify recurring root causes as signals for platform investment, enforce on-call load limits to prevent burnout). The on-call model must match the org's real timezone coverage — at eBay, loss of China production access forced a pivot from follow-the-sun to primary/secondary, with a deliberate plan to rebuild follow-the-sun as India/Europe coverage matured.

> 面试重点：SLO burn rate 告警（非原始阈值）；控制面 APF 和 etcd 专项 observability；AI 辅助 triage 减少 MTTD；RCA 集中管理 + action 跟踪

## Raw Material
- [[raw_material/questions.md]]
