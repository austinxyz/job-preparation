---
title: Multi-Cluster GitOps and Fleet Management
category: tech/infra
tags: [argocd, ocm, kubernetes, multi-cluster, gitops, fleet-management, applicationset, helm, kustomize, argo-rollouts, blue-green, canary, federated-deployment, thanos, observability]
status: in-progress
priority: high
last_updated: 2026-04-26
created_from_jd: "[[jobs/Manager, DevOps, SRE & AI Infrastructure - AppZen]]"
---

# Multi-Cluster GitOps and Fleet Management

## Knowledge Map
- 前置知识：[[CI-CD Pipeline Engineering]], [[Kubernetes]], [[ArgoCD basics]], [[Helm]]
- 延伸话题：[[SRE Practices and SLO Engineering]], [[Observability and Incident Management]], [[DevOps Principles and Culture]]
- 管理关联：platform engineering at scale, developer productivity, incident management, change management

## Core Concepts

### The Multi-Cluster Problem

Single-cluster GitOps is straightforward: one ArgoCD Application pointing at a Git repo, reconciling one cluster. At scale — 30, 50, 200+ clusters — three problems compound:

1. **Configuration drift**: How do you ensure every cluster runs the right version of every app?
2. **Safe progressive rollout**: How do you deploy to a canary cluster first, validate, then roll out without a manual process per cluster?
3. **Fleet observability**: How do you know the deployment state across all clusters at a glance?

The answer is a layered architecture where each layer has a clear responsibility.

### Architecture: OCM + ArgoCD + CI Pipeline

```
OCM Hub (cluster registry)
  └─ ManagedCluster CR — one per cluster, with ring/env labels
  └─ Placement — dynamic cluster selection by label or resource capacity

ArgoCD (GitOps execution layer)
  └─ ApplicationSet — generator reads OCM cluster list → creates one Application per cluster
  └─ Application — manages all workloads in one cluster

CI Pipeline (cross-cluster orchestration)
  └─ Decides rollout order, triggers ArgoCD sync, validates, promotes/rolls back

Argo Rollouts (within-cluster progressive delivery)
  └─ canary / blue-green within a single cluster
```

**Layer responsibilities — the key mental model:**
- **OCM** — "which clusters exist and what are their properties"
- **ArgoCD** — "what is deployed on each cluster" (GitOps reconcile)
- **CI Pipeline** — "in what order to push, what to validate before continuing" (cross-cluster decisions)
- **Argo Rollouts** — "how traffic is split within a cluster"

### OCM (Open Cluster Management)

CNCF project providing a hub-spoke architecture for multi-cluster management.

**Hub-Spoke model:**
```
Hub cluster:
  - Stores ManagedCluster CRs
  - Runs Placement and Policy controllers
  - Receives status from spoke agents

Spoke clusters:
  - Run klusterlet agent (self-registers to hub)
  - Execute ManifestWork delivered from hub
```

**Three core primitives:**

| Primitive | Purpose |
|---|---|
| `ManagedCluster` | Represents a registered cluster; carries labels (ring, region, env) |
| `Placement` | Selects clusters dynamically by label or real-time resource capacity |
| `ManifestWork` | Delivers K8s resources to a specific spoke cluster |

**OCM vs. plain ArgoCD cluster management:**

| Capability | OCM | ArgoCD only |
|---|---|---|
| Cluster registration | Automatic (klusterlet self-registers) | Manual (`argocd cluster add`) |
| Dynamic cluster selection | Placement API (label + capacity) | Static label generator |
| Cross-cluster policy enforcement | Policy Add-on | Not supported |
| Cluster lifecycle management | Full (register, taint, deregister) | Limited |

**When to add OCM:** 50+ clusters, need dynamic Placement, already using Red Hat ACM, or need policy enforcement across the fleet. For fewer clusters with simple label-based selection, ArgoCD's native cluster generator is sufficient.

### ArgoCD ApplicationSet for Fleet Management

ApplicationSet is the factory pattern for multi-cluster: one template generates N Applications, one per cluster.

**Matrix generator pattern (cluster × git config):**
```yaml
generators:
  - matrix:
      generators:
        - clusters:
            selector:
              matchLabels:
                managed-by: ocm        # only OCM-registered clusters
        - git:
            files:
              - path: "values/{{metadata.labels.ring}}/{{name}}.yaml"
template:
  metadata:
    name: 'myapp-{{name}}'
  spec:
    source:
      repoURL: https://github.com/org/manifests
      path: charts/myapp
      helm:
        valueFiles:
          - ../../../values/{{metadata.labels.ring}}/{{name}}.yaml
    destination:
      server: '{{server}}'             # injected by cluster generator
      namespace: myapp
    syncPolicy:
      automated:
        selfHeal: true
        prune: true
```

**Key variables from generators:**
- `{{name}}` — cluster name from ManagedCluster CR
- `{{server}}` — cluster API server URL
- `{{metadata.labels.ring}}` — ring label (canary / staging / prod)

**Critical gotcha — `preserveResourcesOnDeletion: true`:**
If a cluster entry is removed from the generator, ArgoCD deletes all resources on that cluster by default. Set `preserveResourcesOnDeletion: true` to prevent accidental mass deletion.

### Multi-Cluster Pipeline Design

Two approaches for per-cluster configuration, depending on manifest tooling:

#### Kustomize approach

```
manifests/
├── base/                    # CI writes image tag here after build
│   └── kustomization.yaml
└── overlays/
    ├── canary/cluster-canary-us/   # Ring 0
    ├── staging/cluster-stg-us/    # Ring 1
    └── prod/
        ├── cluster-prod-us-1/     # Ring 2 (batched)
        └── cluster-prod-eu-1/
```

**Why split base/ and overlay:** CI updates `base/` with the new image tag (no cluster sync triggered). Pipeline then updates each cluster's overlay sequentially — ArgoCD only syncs when the overlay changes. Git history precisely reflects when each cluster was deployed.

#### Helm approach

```
manifests/
├── charts/myapp/            # Helm chart (shared across all clusters)
│   ├── Chart.yaml
│   ├── templates/
│   └── values.yaml          # defaults
└── values/
    ├── canary/cluster-canary-us.yaml
    ├── staging/cluster-stg-us.yaml
    └── prod/cluster-prod-us-1.yaml
```

CI does **not** update the repo at build time. Pipeline writes to each cluster's values file sequentially during rollout.

**Important:** `helm rollback` is ineffective — ArgoCD uses `helm template` internally, not `helm install`. Rollback means reverting the values file in Git → commit → push → ArgoCD reconciles.

**Kustomize vs. Helm selection:**

| Factor | Kustomize | Helm |
|---|---|---|
| Manifest origin | Own YAML | Upstream open-source charts |
| Inter-cluster variation | Small (replicas, image) | Large (complex values, conditionals) |
| Build/deploy decoupling | Easy (base/ updated first) | Requires discipline: no repo writes at build time |
| Template capability | None (overlay patches only) | Full Go template + conditionals |

### Cross-Cluster Progressive Rollout

**Standard rollout flow:**

```
Build phase (CI):
  └─ Build image, push, sign → image tag: v1.2.3
     Kustomize: update base/ image tag
     Helm: do NOT write to GitOps repo yet

Orchestration phase (CI Pipeline + OCM):
  Query OCM Placement → ordered cluster list by ring

  Ring 0 (canary, 1 cluster):
    Update overlay/values for this cluster → commit → push
    ArgoCD detects change → syncs cluster
    Wait: ArgoCD health == Healthy (timeout 10min → rollback)
    Wait: Argo Rollouts completes canary steps
    Validate: error rate < 1%, p99 latency < 200ms (15min window)
    Pass → Ring 1 | Fail → rollback this cluster, stop pipeline

  Ring 1 (staging, N clusters, one at a time):
    Same pattern per cluster

  Ring 2 (prod, M clusters, 25% batches):
    Per batch: update → sync → health → metrics → next batch
    Batch failure: rollback that batch only; prior batches keep new version

Completion:
  DORA metrics update (lead time covers full rollout duration)
```

### Multi-Cluster Blue/Green

**Model: build all green at once, switch traffic cluster by cluster**

- **Resources:** 2x — both old (blue) and new (green) deployments exist simultaneously across all clusters
- **Traffic:** switched one cluster at a time, not all at once

**Mechanism — `autoPromotionEnabled: false` in Argo Rollouts:**

```yaml
strategy:
  blueGreen:
    activeService: myapp-active       # production traffic → blue
    previewService: myapp-preview     # no production traffic → green
    autoPromotionEnabled: false       # never auto-switch; wait for explicit promote
    scaleDownDelaySeconds: 300        # keep blue 5min after promotion for instant rollback
    postPromotionAnalysis:
      templates:
      - templateName: error-rate
```

**Flow:**
```
Step 1: CI updates image tag for ALL clusters simultaneously
  → ArgoCD syncs all clusters in parallel
  → Argo Rollouts in each cluster: builds green ReplicaSet, holds traffic on blue
  → State: every cluster has blue (production) + green (ready, no traffic)

Step 2: CI Pipeline promotes cluster by cluster
  for each cluster:
    argocd-rollouts promote myapp --context $cluster
    (activeService selector switches to green — instant 100% traffic cut)
    wait for postPromotionAnalysis (15min Prometheus window)
    Pass → next cluster
    Fail → argocd-rollouts undo $cluster (switch back to blue)
           other clusters unaffected, pipeline stops

Step 3: All promoted → blue ReplicaSets scale down after scaleDownDelaySeconds
```

**vs. FDC model:** FDC adjusts traffic ratios gradually (5%→25%→100%) within each cluster before moving to the next. ArgoCD blue/green is binary (0%→100%). For gradual per-cluster traffic ramping, FDC has the advantage.

### Cross-Cluster Observability

**Layer 1 — Which clusters are deployed (ArgoCD):**
```bash
argocd app list | grep myapp
# NAME                     CLUSTER              SYNC    HEALTH
# myapp-cluster-prod-us-1  https://k8s.prod-us  Synced  Healthy
# myapp-cluster-prod-us-2  https://k8s.prod-us  Synced  Degraded  ← problem
```

**Layer 2 — Instance count per cluster (central metrics):**

Each cluster's Prometheus pushes to central storage (Thanos / Victoria Metrics):
```promql
kube_deployment_status_replicas_ready{deployment="myapp"}
# {cluster="prod-us-1"} 10
# {cluster="prod-us-2"} 8   ← 2 missing
```

**Critical distinction:** ArgoCD health = pod ready (K8s level). Service health = user-facing error rate / latency (Prometheus level). Both are needed. ArgoCD alone cannot answer "is the service actually healthy."

| Need | Tool |
|---|---|
| Which clusters are deployed | ArgoCD UI / `argocd app list` |
| Sync and health status | ArgoCD ApplicationSet status |
| Replica count per cluster | Central Prometheus (Thanos / Victoria Metrics) |
| Cross-cluster resource search | OCM Search Add-on / Red Hat ACM UI |
| Alert on replica shortage | Central Prometheus AlertManager |

### Emergency Cluster Traffic Disable

**Principle: traffic control lives at the Global LB / DNS layer, not inside K8s. Stop traffic first, then handle the cluster.**

```
Detect problem
  → Global LB weight → 0 (seconds)
  → Wait for connection draining (30–60s in-flight requests complete)
  → Cluster safe to diagnose / fix
  → Validate fix
  → Re-add to traffic pool
```

**Three-layer tool responsibilities:**

| Goal | Tool | Effect |
|---|---|---|
| Stop new traffic to cluster | Global LB / DNS weight → 0 | New connections no longer routed there |
| Prevent new workload deployment | OCM ManagedCluster taint | Placement excludes cluster from selection |
| Roll back application version | Argo Rollouts undo | Switches back to previous ReplicaSet |

**OCM taint note:** Only affects future Placement decisions — does not stop existing traffic. Use together with Global LB, not as a substitute.

**Terraform is not in the hot path:** LB weight changes call cloud APIs directly (seconds). Terraform (plan/apply) is too slow for emergency operations. Terraform provisions the LB infrastructure; runtime weight changes bypass it.

**Pipeline automation:**
```bash
if ! check_metrics cluster-prod-us-2 15m; then
  disable_cluster_traffic cluster-prod-us-2        # Global LB weight → 0
  kubectl taint managedcluster cluster-prod-us-2 incident=true:NoSchedule
  argocd-rollouts undo myapp --context cluster-prod-us-2
  alert_oncall "cluster-prod-us-2 disabled and rolled back"
  exit 1   # other clusters unaffected, pipeline stops
fi

# Recovery:
kubectl taint managedcluster cluster-prod-us-2 incident=true:NoSchedule-
enable_cluster_traffic cluster-prod-us-2
```

### OCM + ArgoCD + Pipeline vs. eBay FDC — Scenario Comparison

eBay's Federated Deployment Controller (FDC) is a custom K8s Controller that manages multi-cluster deployment as a first-class concern: declarative desired state in a CR, continuous reconcile, AI-based health detection, automatic rollback.

| Scenario | OCM + ArgoCD + Pipeline | eBay FDC |
|---|---|---|
| **Progressive rollout** | Pipeline loops clusters per OCM Placement; custom validation (Prometheus, smoke test, human gate) | Controller state machine; AI health detector; fully automatic |
| **Blue/Green** | `autoPromotionEnabled: false`; CI promotes cluster by cluster; binary traffic switch | All-at-once green build; gradient traffic ratios (5%→25%→100%) per cluster before next |
| **Emergency traffic disable** | Global LB API call (manual / semi-automated runbook) | FDC auto-stops on health anomaly; no on-call action needed |
| **Observability** | ArgoCD UI for sync/health; Thanos for replicas; rollout progress in CI logs | FDC CR status as single source of truth; real-time controller updates |
| **Mid-flight failure recovery** | Pipeline runner crash requires manual state assessment to resume | Controller restarts and resumes from K8s CR state automatically |
| **Scale (100+ clusters, hours)** | Pipeline runner timeout risk; needs lock for concurrency | Controller runs indefinitely; naturally serialized |
| **Per-cluster rollback** | `argocd-rollouts undo` (manual / scripted) | FDC auto-rollback on metric failure; no human action |

**Selection guide:**

| Situation | Recommendation |
|---|---|
| < 50 clusters, < 1h rollout, custom validation | **OCM + ArgoCD + Pipeline** |
| 100+ clusters, hours-long rollout, full automation needed | **FDC-style custom Controller** |
| Existing ArgoCD ecosystem, no custom Controller capacity | **OCM + ArgoCD + Pipeline** |
| Need gradient traffic ratios (not binary blue/green) | **FDC-style Controller** |
| Team has Controller development capability | **FDC-style Controller** |

**One-line summary:**
> OCM + ArgoCD + Pipeline is the standard open-source stack — off-the-shelf, flexible validation, good for most production environments. FDC-style Controllers are for large-scale fleets where declarative state management and automatic mid-flight recovery are non-negotiable.

### ArgoCD Reconcile vs. K8s Controller — The Fundamental Distinction

ArgoCD and Kubernetes controllers both reconcile, but at different layers:

```
Git desired state
    ↓
ArgoCD reconcile (manifest layer) — Git ↔ K8s object spec
    ↓
K8s API Server (Deployment spec)
    ↓
Deployment Controller reconcile (runtime layer) — spec ↔ actual Pods
    ↓
Running Pods
```

**ArgoCD** ensures "the K8s object spec matches Git." It does not manage pods.
**Deployment Controller** ensures "the running pods match the spec." It does not read Git.

| Scenario | Handler |
|---|---|
| New image tag in Git → deploy new version | ArgoCD detects → applies new spec → Deployment Controller rolls out |
| Pod crashes, needs restart | **Deployment Controller** (ArgoCD uninvolved) |
| Someone runs `kubectl scale --replicas=5` (was 10) | **ArgoCD** (selfHeal: true → detects drift → re-applies spec) |
| HPA adjusts replicas automatically | ⚠️ ArgoCD sees drift — use `ignoreDifferences` to tell ArgoCD this field is server-managed |
| ConfigMap updated in Git | ArgoCD applies new ConfigMap; pods do NOT auto-restart (need Reloader or `rollout restart`) |

This pattern is consistent across the K8s ecosystem:

```
ArgoCD          Git spec       →  K8s object spec
Deployment Ctrl  replicas: 10   →  10 running pods
Argo Rollouts    Rollout spec   →  canary traffic split
HPA              target CPU     →  replica count
```

Each layer is an independent control loop owning one segment. ArgoCD is the outermost loop, converting Git into K8s desired state. Controllers handle the rest.

## Key Questions

**Q: How do you use ArgoCD to manage deployments across 30+ clusters?**
Answer framework: ApplicationSet as the factory (one template → N Applications, one per cluster). Cluster generator discovers registered clusters (via OCM or `argocd cluster add`); git generator supplies per-cluster configuration. Matrix generator combines both. Per-cluster values in Helm values files or Kustomize overlays referenced via `{{name}}` and `{{metadata.labels.ring}}`. Sync policy: automated for dev/staging, manual or CI-triggered for prod. Critical: `preserveResourcesOnDeletion: true` to prevent accidental mass deletion.

**Q: How do you design a cluster-by-cluster progressive rollout with validation gates?**
Answer framework: CI Pipeline as the orchestrator — OCM Placement provides the ordered cluster list by ring; pipeline updates one cluster's overlay/values file at a time, triggers ArgoCD sync, waits for health, validates Prometheus metrics (not just pod readiness), then proceeds. Failure handling: roll back that cluster via Argo Rollouts undo or values revert; prior successful clusters keep the new version; pipeline stops. Pipeline model is imperative/one-shot — for 100+ clusters and hours-long rollouts, a custom Controller (FDC pattern) is more robust.

**Q: How does multi-cluster blue/green work with ArgoCD and Argo Rollouts?**
Answer framework: `autoPromotionEnabled: false` is the key. CI updates all clusters simultaneously (one push) — ArgoCD syncs all clusters in parallel — Argo Rollouts in each cluster builds green ReplicaSet but holds traffic on blue. CI Pipeline then promotes clusters one by one: `argocd-rollouts promote` → traffic 100% to green → postPromotionAnalysis (15min Prometheus window) → next cluster. Failure: `argocd-rollouts undo` reverts that cluster; others unaffected. `scaleDownDelaySeconds: 300` keeps blue alive post-promotion for instant rollback.

**Q: How do you know which clusters have a specific application deployed and how many instances are running?**
Answer framework: Two layers. ArgoCD for deployment/sync/health status across clusters — `argocd app list | grep myapp` or ApplicationSet status shows all clusters and their health. Central metrics (Thanos / Victoria Metrics aggregating per-cluster Prometheus) for replica counts — `kube_deployment_status_replicas_ready{deployment="myapp"}` with cluster labels. Critical distinction: ArgoCD health = pod ready (K8s signal); service health = user-facing error rate / latency (Prometheus signal). Both needed; ArgoCD alone cannot confirm the service is actually healthy.

**Q: A cluster is having issues — how do you take it out of production traffic without causing an outage?**
Answer framework: Traffic lives at Global LB / DNS layer, not K8s. Never scale down first — remove from LB first, then handle the cluster. Flow: set LB weight to 0 (seconds) → connection draining (30–60s) → diagnose / fix. Add OCM taint to prevent new deployments from targeting that cluster during the incident. Roll back application version via Argo Rollouts undo if needed. Terraform is not in the hot path — call cloud APIs directly for LB changes. Recovery: remove taint, restore LB weight.

**Q: What is ArgoCD's role in reconciliation, and what does the Deployment Controller do?**
Answer framework: They reconcile at different layers. ArgoCD is the manifest-layer control loop: Git desired state → K8s object spec. Deployment Controller is the runtime-layer control loop: K8s spec → actual running pods. Pod crash recovery is entirely the Deployment Controller's domain — ArgoCD does not restart pods and should not. `selfHeal: true` makes ArgoCD re-apply the Git spec when it detects manual drift (e.g., someone kubectl-edited the Deployment). HPA is a common gotcha: it modifies `spec.replicas` at runtime, which ArgoCD sees as drift — use `ignoreDifferences` to tell ArgoCD this field is server-managed.

**Q: How does OCM complement ArgoCD in fleet management?**
Answer framework: Different layers. OCM manages cluster lifecycle — registration (klusterlet self-registers), labels, taints, Placement-based dynamic selection. ArgoCD manages workload delivery — ApplicationSet reads OCM's ManagedCluster inventory as the cluster source. Without OCM: clusters must be manually registered to ArgoCD, Placement is static label-matching, no cluster-level policy enforcement. With OCM: cluster registration is automatic, Placement can use real-time resource capacity (not just labels), ManagedCluster taints provide incident isolation. When to add OCM: 50+ clusters, need dynamic Placement, need cross-cluster policy, or already using Red Hat ACM.

**Q: How does the OCM + ArgoCD approach compare to a custom Federated Deployment Controller?**
Answer framework: Execution model is the key difference. OCM + ArgoCD + Pipeline is imperative and one-shot — if the pipeline runner crashes mid-rollout, you must manually assess state and decide how to resume. FDC (custom K8s Controller) is declarative and continuously reconciling — it reads desired state from a CR, restores from the CR on restart, and proceeds automatically. Pipeline wins on: flexibility of validation logic (any external check), off-the-shelf tooling, lower build investment. FDC wins on: 100+ cluster scale, long rollouts (hours), automatic recovery, no runner timeout concerns. The inflection point is roughly 50 clusters / 1 hour of rollout time.

## Key Terms

**Multi-cluster management**
`OCM` · `Open Cluster Management` · `ManagedCluster` · `Placement` · `ManifestWork` · `klusterlet` · `hub cluster` · `spoke cluster` · `Red Hat ACM` · `ManagedClusterSet` · `ManagedCluster taint`

**ArgoCD fleet**
`ApplicationSet` · `cluster generator` · `git generator` · `matrix generator` · `pull-request generator` · `Application` · `AppProject` · `preserveResourcesOnDeletion` · `selfHeal` · `ignoreDifferences` · `sync wave` · `sync hook`

**Progressive delivery**
`ring-based rollout` · `canary cluster` · `Argo Rollouts` · `autoPromotionEnabled` · `promote` · `argocd-rollouts undo` · `scaleDownDelaySeconds` · `postPromotionAnalysis` · `AnalysisTemplate` · `activeService` · `previewService`

**Observability**
`Thanos` · `Victoria Metrics` · `remote_write` · `cross-cluster Prometheus` · `cluster label` · `kube_deployment_status_replicas_ready` · `ArgoCD health` · `pod ready` · `user-facing health`

**Traffic management**
`Global LB` · `Route53 weighted routing` · `AWS Global Accelerator` · `connection draining` · `LB weight` · `hot path` · `Terraform drift`

**Custom controller pattern**
`Federated Deployment Controller (FDC)` · `DeploymentWave CR` · `AI health detector` · `declarative rollout` · `controller reconcile loop` · `state machine` · `CR status`

## Summary

Multi-cluster GitOps at scale requires separating concerns across layers: OCM for cluster registry and dynamic selection, ArgoCD for GitOps workload delivery per cluster, CI Pipeline for cross-cluster rollout orchestration and validation, and Argo Rollouts for within-cluster progressive traffic management. Each layer owns a specific control loop — conflating them is the most common design mistake.

The core patterns are: ApplicationSet with a matrix generator (cluster × git) to auto-generate per-cluster Applications without manual registration; ring-based pipeline rollout (canary → staging → prod batches) with OCM Placement providing the ordered cluster list; and `autoPromotionEnabled: false` in Argo Rollouts for multi-cluster blue/green where all clusters build green simultaneously but traffic switches one cluster at a time.

Observability requires two distinct signals: ArgoCD for deployment/sync/health status (pod-ready signal), and a central metrics layer (Thanos/Victoria Metrics) for user-facing service health and replica counts across clusters. ArgoCD alone cannot confirm service health. Emergency cluster isolation uses the Global LB layer (not K8s) to stop traffic, OCM taints to prevent new deployments, and Argo Rollouts undo for version rollback — in that order.

The comparison with eBay's Federated Deployment Controller illustrates the fundamental trade-off: OCM + ArgoCD + Pipeline is the off-the-shelf standard, flexible on validation logic but fragile for long-running rollouts (imperative, runner-dependent). FDC-style custom Controllers are declarative and self-recovering, essential for 100+ cluster fleets where rollouts run for hours. The inflection point is roughly 50 clusters / 1 hour of rollout duration.

## Raw Material
- [[Multi-Cluster Deployment - OCM+ArgoCD vs FDC]]
- [[CI-CD Pipeline Engineering - zh]]
