---
title: Observability and Incident Management
category: tech/infra
tags: [observability, monitoring, sre, incident-response, alerting, debugging, slo, sli, on-call]
status: draft
priority: high
last_updated: 2026-04-07
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

## Summary

Observability is what enables you to understand a system's behavior without being in the room when it breaks. For infrastructure teams, the three pillars (metrics, logs, traces) plus SLO/error-budget thinking form the operational foundation. The critical shift is from reactive firefighting (alert on causes, respond to noise) to proactive reliability management (alert on user-visible symptoms, use error budgets to govern the reliability vs. velocity tradeoff). For Kubernetes specifically, the debugging workflow — describe/logs/events → resource limits → probe configs → networking — is a repeatable procedure that resolves 80% of pod issues. For incidents, the discipline of "mitigate first, diagnose second" prevents prolonged outages caused by teams investigating while users suffer.

> 面试重点：SLO/error budget 是现代 SRE 的核心框架；先止血再查因是事故处理原则；告警必须可操作，否则删除

## Raw Material
- [[raw_material/questions.md]]
