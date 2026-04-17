---
title: CI/CD Pipeline Engineering
category: tech/infra
tags: [ci-cd, jenkins, tekton, prow, argocd, argo-rollouts, flux, github-actions, helm, kustomize, kyverno, cosign, sbom, slsa, pipeline, build-automation, devops, gitops, kaniko, dora]
status: in-progress
priority: high
last_updated: 2026-04-16
created_from_jd: "[[positions/Manager, DevOps Engineering - NVIDIA]]"
---

# CI/CD Pipeline Engineering

## Knowledge Map
- 前置知识：build systems, version control (Git), containerization, Kubernetes
- 延伸话题：[[DORA Metrics]], [[Deployment Strategies (canary, blue-green)]], [[GitOps]], [[Kubernetes]], [[SRE Practices and SLO Engineering]]
- 管理关联：developer productivity, engineering velocity, platform reliability, developer experience (DevEx)

## Core Concepts

- **Two-tier CI/CD architecture at scale**: Separate CI platform (CIaaS/Jenkins) for application builds and a dedicated CD platform (ECD/Tekton) for deployment — decoupling build from release allows each to scale and be governed independently.
- **Jenkins Master/Slave on Kubernetes**: Slave pods are created on-demand per build job (via CRD/operator), mount a shared volume for artifact persistence, and are destroyed after the build. This elastic model avoids idle capacity while maintaining build isolation.
- **Kaniko for rootless container builds**: Builds container images inside Kubernetes pods without requiring privileged Docker daemon — essential for secure multi-tenant CI environments.
- **Two pipeline types — Staging vs. PR pipeline**:
  - *Staging pipeline*: deploys a feature branch image to a dynamically provisioned feature pool; runs SAST and integration tests.
  - *PR pipeline*: triggered on merge; promotes through feature → staging → prod with mandatory checkpoints (test coverage gate, security scan badge, multi-reviewer approval, blue-green/canary rollout).
- **Policy-as-badges enforcement**: Each pipeline stage issues a "badge" (test coverage passed, security scan clean, ≥2 PR reviews, staging deploy complete). Downstream steps require specific badges before proceeding — decentralized yet auditable governance.
- **Prow + Releaser for platform/cloud components**: Prow (Kubernetes-native CI) validates PRs with e2e tests before merge; Releaser (homegrown GitOps CD) stores YAML specs per cluster/environment in Git, applies them, and provides a UI with rollout progress, health monitoring, and logs.
- **Federated Deployment Controller for multi-cluster CD**: A custom controller orchestrates rolling updates across multiple clusters — progressively shifting traffic to the new version, reading health signals from an AI-based health detector, and triggering automatic rollback on degradation.
- **Artifact promotion with ECR + image scanning**: Images tagged by commit SHA. Promotion dev → staging → prod requires passing test coverage gate and image scan (Anchors-based tool). Kyverno pod policies prevent unsigned/unscanned images from deploying.
- **Supply chain security**: Tekton pipeline enhanced to sign images (similar to cosign); Kyverno verifies the signature at admission time before pods can run.
- **DORA metrics as the velocity north star**: Lead time, deployment frequency, rollout duration, rollback duration, and success rate are the primary health indicators for the CI/CD platform — not just pipeline pass rate.
- **CI/CD reliability as a platform concern**: Excessive pipeline load caused K8s API server pressure → solved with API Priority and Fairness (APF) + a gateway layer that queues jobs and monitors total in-flight pipeline count. CI/CD node pools are isolated to prevent capacity contention with workloads.
- **Selective test execution**: Commercial tooling (integrated into CIaaS) analyzes code change impact and runs only affected test cases — directly reduces pipeline duration without dropping coverage signal.

### Industry-Standard Tooling Landscape

| Layer | Common Tools | When to Choose |
|---|---|---|
| CI (hosted) | GitHub Actions, GitLab CI, CircleCI, Buildkite | SaaS convenience, tight SCM integration |
| CI (self-hosted) | Jenkins, Tekton, Prow, Drone, Concourse | Control, on-prem, K8s-native |
| CD / GitOps | **ArgoCD**, Flux, Jenkins X | Declarative, drift detection, multi-cluster |
| Progressive delivery | **Argo Rollouts**, Flagger, Spinnaker | Automated canary with metric-based promotion |
| Build (app) | Bazel, Gradle, Maven, Turborepo, Nx | Monorepo caching, language-specific |
| Container build | Kaniko, BuildKit, ko, Buildpacks | Rootless, cache-efficient, K8s-native |
| Image registry | ECR, GCR, Harbor, Artifactory, Docker Hub | Cloud-native vs. self-hosted governance |
| Manifest packaging | Helm, Kustomize, Timoni, cdk8s | Templating vs. overlay vs. typed config |
| Secret injection | HashiCorp Vault, AWS Secrets Manager, External Secrets Operator, Sealed Secrets | Centralized rotation vs. K8s-native sync |
| Policy enforcement | Kyverno, OPA/Gatekeeper, jsPolicy | Admission control for image/config compliance |
| Scanning | Trivy, Grype, Snyk, Anchore, Dependency-Track | SAST/SCA/image CVE scanning |
| Supply chain | Sigstore/cosign, SLSA, in-toto, Syft (SBOM) | Signed artifacts, provenance, SBOM generation |
| Feature flags | LaunchDarkly, Unleash, Flagsmith, Split.io | Decouple deploy from release |
| Artifact promotion | Argo Workflows, Tekton Chains, GitHub Environments | Environment gates, approval flows |

### Industry-Standard Tooling — Common Usage Patterns

Deep-dives on the tools most commonly asked about in DevOps / AI Infra manager interviews. Each follows: *Purpose → Core Usage → Key Primitives → Gotchas → When to Pick*.

#### ArgoCD (GitOps CD — the de facto standard)

- **Purpose:** Declarative GitOps continuous delivery for Kubernetes — Git is the single source of truth for cluster state; ArgoCD reconciles the live cluster to match.
- **Core usage pattern:**
  1. App team commits Helm/Kustomize/plain YAML manifests to a Git repo.
  2. An `Application` CR in ArgoCD points at `{repo, path, targetRevision}` and a destination cluster/namespace.
  3. ArgoCD polls (or receives webhook), renders manifests, diffs against live state, and syncs.
  4. UI shows per-resource sync + health status; automated or manual sync.
- **Key primitives:**
  - `Application` — a single app's deployment definition. Mostly a pointer: source (Git) + destination (cluster/ns) + sync policy.
  - `ApplicationSet` — generator-based factory that templates many `Application` CRs from one definition. Common generators: `list`, `cluster`, `git`, `matrix`, `pull-request` — the industry answer for multi-cluster fleet management.
  - `Project` — RBAC boundary: which repos/clusters/namespaces a set of Applications may touch.
  - `Sync waves` — ordering hint (annotation `argocd.argoproj.io/sync-wave: "N"`) to deploy CRDs before CRs, namespaces before workloads, etc.
  - `Hooks` — `PreSync` / `Sync` / `PostSync` / `SyncFail` for DB migrations, smoke tests, cleanup.
  - Sync policies: `automated` (self-heal + prune), `manual`; `syncOptions` like `CreateNamespace=true`, `ServerSideApply=true`.
- **Common patterns:**
  - **App-of-apps / ApplicationSet fleet** — one parent Application generates many child Applications across a fleet of clusters.
  - **Directory-per-environment** Git layout: `envs/dev/`, `envs/staging/`, `envs/prod/` with Kustomize overlays.
  - **PR preview envs** — `pull-request` generator creates ephemeral Application per open PR; teardown on merge/close.
  - **Progressive rollout with Argo Rollouts** — ArgoCD syncs the `Rollout` CR; Argo Rollouts handles the actual canary/blue-green.
- **Gotchas:**
  - Drift from hand-edits: without `selfHeal: true`, `kubectl edit` changes persist silently. Auto self-heal reverts them and can surprise operators.
  - Sync waves are hints, not guarantees — don't encode business logic in them.
  - Repo size + refresh interval can overload the repo-server; shard large repos or use multiple repo-servers.
  - Live manifests that mutate (e.g., HPA adjusting `spec.replicas`) trigger endless diff — use `ignoreDifferences` or tell ArgoCD the field is server-owned.
- **When to pick:** Default choice for K8s-native GitOps. Pick **Flux** instead when you want a more Kubernetes-controller-idiomatic architecture (GitRepository/Kustomization CRs as the surface) or stricter OCI/notation-based source control. Pick **Jenkins X** when tightly integrated CI+CD+preview envs are wanted out-of-the-box.

#### Argo Rollouts (progressive delivery)

- **Purpose:** Replaces the built-in Deployment controller with a `Rollout` CR that supports canary, blue-green, and experiment strategies, plus automated analysis gates.
- **Core usage pattern:** Define a `Rollout` instead of a `Deployment`. Define an `AnalysisTemplate` that queries Prometheus/Datadog/New Relic. Canary steps alternate between traffic shifts (`setWeight: 25`) and pauses (for manual approval or automated analysis).
- **Key primitives:**
  - `Rollout` — drop-in for Deployment. Supports `strategy.canary.steps[]` or `strategy.blueGreen`.
  - `AnalysisTemplate` / `AnalysisRun` — queries a metrics provider; passes/fails based on a success condition (`result[0] >= 0.95`).
  - Traffic-management integrations: Istio, Linkerd, NGINX, AWS ALB, SMI, Gateway API — Argo Rollouts updates the traffic split mechanism declaratively.
  - Experiment CR — short-lived A/B against baseline for fixed duration.
- **Common patterns:**
  - Canary: 5% → analysis → 25% → analysis → 50% → 100%. Automatic rollback on analysis failure.
  - Blue-green with `autoPromotionEnabled: false` gate for manual approval.
  - Post-rollout analysis (background) that watches for 30 min after 100% and triggers rollback on regression.
- **Gotchas:**
  - Analysis queries must be *derivative* (rate over window), not cumulative — cumulative counters never trigger failure.
  - Traffic-routing needs an actual service mesh or ingress that supports weights; without one, canary degrades to pod-count-based splitting (`setWeight` by replica ratio, not actual traffic).
  - Metric windows must be large enough that low-traffic services produce statistically valid signals — otherwise you get flappy analysis.
- **When to pick:** Anywhere canary or blue-green is needed with automated quality gates. **Flagger** is the Flux equivalent — pick it if you're already on Flux. **Spinnaker** is the legacy alternative for multi-cloud, non-K8s pipelines.

#### GitHub Actions (hosted CI, ubiquitous)

- **Purpose:** YAML-defined workflows co-located with code; free for OSS, widely adopted.
- **Core usage pattern:** `.github/workflows/*.yml` defines jobs triggered on `push`, `pull_request`, `schedule`, `workflow_dispatch`. Each job runs on a runner (hosted or self-hosted).
- **Key primitives:**
  - `job` → `steps` (each step is a shell command or an `action`).
  - `uses: owner/action@sha` — pinned by SHA for security (tags are mutable!).
  - `matrix` — fan out across dimensions (OS × language version).
  - Reusable workflows (`workflow_call`) and composite actions — share logic across repos.
  - `permissions:` block — least-privilege the `GITHUB_TOKEN`; default write-all is a supply-chain risk.
  - OIDC federation to AWS/GCP/Azure — short-lived credentials, no long-lived cloud keys in secrets.
- **Common patterns:**
  - **Build-test-publish** on push to `main`; build+test only on PRs.
  - **Release-please or semantic-release** to auto-cut versions from conventional commits.
  - **Self-hosted runners in K8s** via Actions Runner Controller (ARC) for private network access or GPU builds.
  - **Reusable workflow** in a central repo; app repos `uses: org/ci-central/.github/workflows/build.yml@main`.
- **Gotchas:**
  - Tag-pinned actions are a supply-chain hole — pin to SHA, review on upgrade.
  - `pull_request_target` runs with write tokens on fork PRs — common misconfig causing RCE.
  - Matrix builds can multiply cost unexpectedly; add `fail-fast: false` cautiously.
- **When to pick:** Default for GitHub-hosted code. Move to **GitLab CI** if on GitLab (tighter parity), **Buildkite** for enterprise-scale with BYO compute, **Jenkins** for complex legacy pipelines.

#### Tekton (K8s-native CI/pipeline engine)

- **Purpose:** Kubernetes-native, pipeline-as-code via CRDs. Vendor-neutral, designed as a building block (Cloud Native Computing Foundation graduated).
- **Core usage pattern:** Define reusable `Task` CRs (each a containerized step); compose them into a `Pipeline`; execute via `PipelineRun`. Triggers via Tekton Triggers (webhooks → EventListener → TriggerBinding → PipelineRun).
- **Key primitives:**
  - `Task` / `ClusterTask` — a containerized step with params, workspaces, results.
  - `Pipeline` — DAG of Tasks; `runAfter:` or implicit via param dependencies.
  - `Workspace` — shared volume between steps (ephemeral or backed by PVC).
  - `Results` — typed outputs from one task consumed by another.
  - `Tekton Chains` — signs task outputs (images, attestations) via Sigstore; core to supply-chain security.
- **Common patterns:**
  - Catalog-first design: consume standard tasks from `tektoncd/catalog` (git-clone, buildah, kaniko, helm-upgrade) before writing custom ones.
  - Pair with ArgoCD: Tekton builds image + updates manifest Git repo; ArgoCD picks up the commit and deploys.
  - Tekton Chains + cosign in-pipeline → SLSA-level-3 provenance out of the box.
- **Gotchas:**
  - Pod-per-task model means many short pods — requires fast image pull + K8s API server headroom (this is what hit our API server at eBay).
  - YAML verbosity is real; lean on catalog Tasks to keep it manageable.
  - Debugging failed runs requires understanding `TaskRun` logs (per-step containers) — more indirection than Jenkins console output.
- **When to pick:** K8s-native orgs wanting pipeline-as-code with full primitives control; base for building *a CI platform* rather than using one. **Prow** on top of Tekton is the classic pattern for K8s-project CI (merge gating, lgtm, test-retry).

#### Jenkins (still dominant in enterprise)

- **Purpose:** Extensible, plugin-rich CI server. The workhorse that most large orgs still run — Jenkinsfile (Groovy DSL) for pipeline-as-code.
- **Core usage pattern:** Declarative Jenkinsfile in repo; Shared Libraries for reusable steps; agents run on K8s via `kubernetes` plugin (pod-per-build model, like Tekton's TaskRun).
- **Key primitives:**
  - `pipeline { agent; stages; post }` declarative DSL; `node {}` scripted DSL (legacy).
  - Shared Libraries — versioned Groovy code loaded via `@Library('libname')`.
  - Multibranch / Organization folders — auto-discover repos/branches and run their Jenkinsfile.
  - Credentials Provider — centralized secret injection; avoid plaintext in Jenkinsfile.
- **Common patterns:**
  - Master + ephemeral K8s agents (Jenkins `kubernetes-plugin`) — elastic, the eBay CIaaS model.
  - Pipeline-as-platform: platform team owns Shared Libraries; app teams call `@Library('ci-v3') _; buildJava()`.
- **Gotchas:**
  - Plugin version drift and Groovy sandbox issues — plugin hell is the #1 Jenkins operational cost.
  - Master scaling ceiling — eventually requires shard federations or migration to distributed controllers (CloudBees CI).
  - Groovy pipeline memory leaks; master needs periodic restarts.
- **When to pick:** Existing Jenkins footprint + enterprise plugin needs + large shared library investment. New green-field K8s-native orgs should prefer Tekton or GitHub Actions + ARC.

#### Flux (GitOps alternative to ArgoCD)

- **Purpose:** CNCF GitOps toolkit; more controller-idiomatic Kubernetes feel than ArgoCD. Each concern is a separate CRD/controller.
- **Key primitives:** `GitRepository`, `OCIRepository`, `HelmRepository` as source CRs → `Kustomization`, `HelmRelease` as deploy CRs → notifications via `Alert` + `Provider`.
- **Differences vs ArgoCD:**
  - No built-in UI (you build one via Weave GitOps or similar); ArgoCD's UI is a strong reason teams prefer it.
  - Flux embraces OCI-as-Git-substitute earlier — `OCIRepository` + `cosign` verification natively.
  - More modular architecture (source-controller, kustomize-controller, helm-controller) — easier to reason about as individual controllers.
- **When to pick:** Platforms already standardized on OCI-distributed manifests, or teams preferring pure-controller patterns. ArgoCD wins on UI/UX; Flux wins on controller architecture purity.

#### Helm vs Kustomize (manifest packaging)

- **Helm:** Go-template-based package manager. Charts are versioned, published to repos (HTTP or OCI), released to clusters. Hooks, tests, dependencies, rollback built-in.
- **Kustomize:** Overlay-based — `kustomization.yaml` composes base YAML + patches. Built into `kubectl`. No templating (deliberate).
- **Common combinations:**
  - Helm + values-per-env → complex chart, many environments.
  - Kustomize overlays → simpler YAML, environment-specific patches, no templating hell.
  - Helm chart *as base* + Kustomize overlays — `helm template` output piped through kustomize; used when upstream chart isn't flexible enough.
- **When to pick:**
  - **Helm:** redistributable packaging (like charts for Prometheus, Istio), complex templating needs, lifecycle hooks.
  - **Kustomize:** app-team-owned deployment config, few environment knobs, preference for "just YAML."
  - **Timoni / cdk8s:** when Go-template-driven YAML becomes unmaintainable — typed config (CUE/TypeScript) replaces templating.

#### Harbor (container registry with governance)

- **Purpose:** Self-hosted OCI registry with CVE scanning (Trivy), image signing (Notary/cosign), replication, RBAC, and retention policies.
- **Common usage patterns:**
  - Per-team projects with quota + retention rules (auto-prune untagged images older than N days).
  - Automatic Trivy scan on push; policy blocks pulls of images with critical CVEs.
  - Cross-region replication for multi-region clusters.
  - Proxy cache for upstream registries (Docker Hub rate-limit mitigation).
- **When to pick:** On-prem or regulated environments needing full registry control. **ECR/GCR/ACR** for cloud-native; **Artifactory** when multi-artifact-type (Maven, npm, Docker) governance matters.

#### Policy: Kyverno vs OPA/Gatekeeper

- **Kyverno:** K8s-native policies written in YAML (no Rego). Validate/mutate/generate. Popular for "require image signatures," "enforce resource limits," "block `latest` tag."
- **OPA/Gatekeeper:** Policies in Rego (more expressive, steeper learning curve). Popular in orgs with a broader OPA footprint (API authz, Terraform policies).
- **Common patterns:**
  - Admission control blocking unsigned images (cosign verification policy).
  - Enforce required labels (owner, cost-center) at namespace creation.
  - Mutate defaults (inject sidecars, add default requests/limits).
- **When to pick:**
  - **Kyverno** for K8s-only policy with a short learning curve.
  - **OPA** when you want one policy language across K8s, CI, and API gateways.

#### Secrets Management

- **Vault** — central secret store with dynamic secrets, leasing, rotation. K8s integration via Vault Agent Injector or CSI driver.
- **External Secrets Operator (ESO)** — reconciles a `SecretStore` (Vault, AWS Secrets Manager, GCP SM, Azure KV) into native K8s `Secret` objects. Most common pattern in 2026.
- **Sealed Secrets** — encrypt secret-as-YAML that can be checked into Git; only the cluster's controller can decrypt. Good for pure-GitOps workflows.
- **Cloud-provider native** — AWS Secrets Manager / GCP Secret Manager / Azure Key Vault with CSI drivers mounting secrets as files.
- **Anti-pattern:** secrets committed to Git plaintext, even in private repos. Sealed Secrets or ESO solves this cleanly.

#### Supply Chain Security — Sigstore, SLSA, SBOM

- **cosign** — signs and verifies container images, signatures stored in OCI registry next to images.
- **SLSA levels 1–4** — build provenance maturity model; Level 3 requires hermetic, signed builds; Tekton Chains or GitHub Actions provenance can achieve SLSA-3.
- **Syft / Trivy SBOM** — generate Software Bill of Materials (SPDX or CycloneDX format) at build time; scan SBOMs later for newly-disclosed CVEs without rebuilding.
- **Common pattern:**
  1. Build image in CI.
  2. Generate SBOM (Syft) → attach as OCI artifact via cosign.
  3. Sign image (cosign) with OIDC-federated keyless signing.
  4. Kyverno policy verifies signature at admission time.
  5. Trivy continuously scans SBOMs in registry for newly disclosed CVEs.

### Canonical End-to-End Pipeline (2026 reference stack)

A reference pipeline wiring up the industry-standard tools — useful as a whiteboard answer:

```
Developer pushes code
  ↓
GitHub Actions (or Tekton)
  ├─ Lint / unit tests (matrix across versions)
  ├─ SAST scan (Trivy / Snyk)
  ├─ Build container (Kaniko or BuildKit)
  ├─ Generate SBOM (Syft)
  ├─ Push to Harbor (or ECR)
  ├─ Sign image (cosign, OIDC keyless)
  └─ Update Kustomize overlay in GitOps repo with new image tag
  ↓
ArgoCD detects Git change
  ├─ Renders manifests (Helm / Kustomize)
  ├─ Syncs to target cluster(s)
  └─ Kyverno admission verifies image signature + policy compliance
  ↓
Argo Rollouts executes canary
  ├─ 5% → AnalysisTemplate queries Prometheus for error rate + latency
  ├─ Pass → 25% → 50% → 100%
  └─ Fail → automatic rollback to prior ReplicaSet
  ↓
Post-rollout observability
  ├─ DORA metrics updated (lead time, deploy freq, change-fail rate)
  └─ Tekton Chains / GitHub Actions provenance published (SLSA-3)
```

**Key design choices in this reference:**
- GitOps repo separate from app repo — enables PR-based deploy approval, auditable history, no write-to-cluster from CI.
- Image signing + admission verification — runtime guarantee that only signed images deploy, even if CI is bypassed.
- Canary gates on derived metrics (error rate, latency) not just HTTP 200 — catches semantic regressions.
- SBOMs stored alongside images in OCI registry — enables post-deploy CVE rescanning without rebuild.

### Trunk-Based Development vs. Feature Branches

- **Trunk-based development (TBD)**: All engineers commit to `main` (or short-lived branches < 2 days). Enables true continuous integration — no long-lived divergence. Requires feature flags to decouple deploy from release.
- **Feature branches**: Easier for teams new to CI, but long-lived branches create merge hell and defeat the purpose of CI (integrating *continuously*).
- **Platform team recommendation**: TBD for mature teams; enforce short branch lifetime (<2 days) as a policy gate for others.

### Feature Flags as a Deployment Decoupler

- Deploy code to production independently of releasing it to users — dark launches, % rollouts, targeted user groups.
- Eliminates the need for long-lived feature branches and big-bang releases.
- Tools: LaunchDarkly, Unleash, Flagsmith, or homegrown via config service.
- Key risk: **flag debt** — flags that are never cleaned up become permanent complexity.

### Pipeline Observability

CI/CD platforms need the same observability discipline as production services:
- **Key metrics**: pipeline success rate, P50/P95 pipeline duration, queue depth, flaky test rate, rollback rate.
- **Dashboards**: per-team breakdown to identify outliers (one team's bad tests shouldn't hide in aggregate).
- **Alerting**: success rate drop, queue backup exceeding SLO, node pool saturation.
- **Correlation with DORA**: if pipeline duration increases, lead time increases — surface this to engineering leadership.

### AI/ML CI/CD Considerations (MLOps Pipeline)

ML model deployment has different gates than application code:

| Stage | App CI/CD | ML CI/CD |
|---|---|---|
| Build | Compile + unit test | Data validation, feature pipeline test |
| Validate | Integration test, coverage gate | Model evaluation (accuracy, bias, drift metrics) |
| Artifact | Container image (immutable tag) | Model artifact + serving container + config |
| Canary gate | Error rate, latency | Prediction quality metrics, A/B test results |
| Rollback signal | HTTP 5xx spike | Model performance degradation (offline or online) |

- **Model registry** (MLflow, W&B, Vertex AI Model Registry): stores versioned model artifacts with evaluation metadata — analogous to image registry + image scan badge.
- **Shadow mode / champion-challenger**: serve new model in shadow alongside production model; compare outputs before promotion.
- **Data pipeline as a first-class CI citizen**: data quality checks must run before model training, not just before deployment.
- **Training pipeline reproducibility**: pin data version + code version + hyperparameters → deterministic retraining is a testability requirement, not a nice-to-have.

### Cost Management for CI/CD at Scale

- **Spot/preemptible instances for CI workers**: build jobs are interruptible; using spot reduces compute cost 60-80%. Requires retry logic for interruptions.
- **Build cache sharing**: persistent layer caching (BuildKit) and dependency caching (Maven/Gradle/npm) reduce redundant work — measure cache hit rate as a KPI.
- **Idle pipeline infrastructure**: Jenkins master, ArgoCD server, image registries have fixed costs — right-size or consolidate across teams.
- **Pipeline run attribution**: tag pipeline runs with team/project to enable chargeback and identify high-cost outliers.

## Key Questions

**Q: Walk me through how you designed or operated a large-scale CI/CD platform. What were the biggest architectural decisions?**
Answer framework: Describe the two-tier separation (CIaaS for build, ECD/Tekton for deploy). Explain the Jenkins Master/Slave on K8s elastic model. Highlight policy-as-badges as the governance mechanism. Tie choices to developer experience (self-service, no platform team bottleneck) and reliability (isolated node pools, gateway layer).

**Q: How did you enforce compliance and security in the pipeline without slowing teams down?**
Answer framework: Mandatory badge system — stages won't proceed without required badges (coverage, scan, review). Security scan in staging pipeline (not blocking PR creation). Image signing + Kyverno admission control as a runtime safety net. Result: teams move fast, but bad images literally cannot deploy.

**Q: How do you handle multi-cluster, multi-environment deployments safely?**
Answer framework: Federated Deployment Controller for progressive cluster-by-cluster rollout. AI-based health detector provides automated go/no-go signal. Automatic rollback on degradation. For cloud components, GitOps with directory-per-cluster structure in Releaser.

**Q: What DORA metrics did you track and how did you improve them?**
Answer framework: Define the five metrics used (lead time, deploy frequency, rollout/rollback duration, success rate). Explain what drove improvements: incremental build, selective tests, parallel validation jobs, removing manual approval gates, blue-green reducing rolling upgrade time. Give specific directional improvements if possible.

**Q: CI/CD infrastructure caused production incidents at your company — how did you handle that?**
Answer framework: Three classes of incidents — (1) API server overload from pipeline traffic (→ APF + gateway queue + monitoring), (2) node capacity exhaustion from excess Tekton/Jenkins slave pods (→ dedicated node pool + observability), (3) bad base image failing all downstream scans (→ stricter base image validation gate). Each resolution follows: detect → contain → fix root cause → add preventive control.

**Q: How do you make CI/CD self-service while maintaining standards?**
Answer framework: CRD-driven app onboarding (operator provisions Jenkins config automatically). Policy-as-badges lets teams customize pipeline steps but cannot skip mandatory gates. Visual pipeline UI lets teams see and modify their pipeline without opening support tickets. Platform team owns the policy definition, not the day-to-day execution.

**Q: How did you handle flaky tests in CI?**
Answer framework: Triage flakiness source — infra vs. app. Infra flakiness: improve platform reliability + automatic retry. App flakiness: AI-powered log analysis suggests code fixes. Coverage gate adjusted based on deployment track record (fewer failures → selective test runs allowed).

**Q: How is CI/CD for ML models different from application CI/CD? What challenges does that introduce?**
Answer framework: The validation gate is fundamentally different — instead of test pass/fail, you're evaluating model quality metrics (accuracy, latency, bias). The artifact is richer (model weights + serving config + preprocessing code). Rollback signal is harder to define (model degradation may be subtle and lagged). Shadow mode / champion-challenger testing is essential before full promotion. Data pipeline integrity is a prerequisite — garbage in, garbage out regardless of how good the deployment pipeline is.

**Q: How do you balance trunk-based development vs. feature branches for a large engineering org?**
Answer framework: TBD is the goal state for fast-moving platform teams — it eliminates merge debt and forces feature flags as a release mechanism. For teams not ready, enforce a branch lifetime gate (PRs open > N days get flagged). Feature flags are the enabling technology — deploy dark, release gradually. Key management concern: flag cleanup process to prevent flag debt accumulation.

**Q: How would you measure and improve developer velocity through CI/CD improvements?**
Answer framework: Start with DORA metrics as baseline. Break down lead time into components: PR review wait, pipeline queue wait, pipeline execution time, deploy wait, monitoring window. Each is a different fix — code review culture vs. infrastructure scaling vs. pipeline optimization vs. self-service. Pick the biggest bottleneck, fix it, re-measure. Show the business value: X% improvement in deploy frequency → Y more features shipped per quarter.

**Q: How do you manage CI/CD costs at scale without sacrificing speed?**
Answer framework: Use spot instances for CI workers (with retry on interruption) — biggest lever. Invest in build caching (layer cache, dependency cache) and measure cache hit rate. Implement selective test execution to avoid running all tests on every commit. Tag pipeline costs by team for visibility and accountability. Right-size persistent infra (Jenkins master, ArgoCD). The framing: cost optimization and speed are aligned — faster pipelines cost less because they consume resources for less time.

## Summary

CI/CD pipeline engineering at eBay operated at two levels: a centralized CIaaS platform (Jenkins on Kubernetes) serving hundreds of application teams, and a separate platform-component pipeline (Prow + Releaser) for the Cloud Control Plane itself. The application platform used an elastic Jenkins Master/Slave model where slave pods were provisioned on-demand via a K8s operator, with Kaniko handling container image builds in a rootless, multi-tenant-safe way. The CD layer (ECD/Tekton) defined two pipeline archetypes — staging pipelines for feature testing in dynamically provisioned pools, and PR pipelines that enforced a mandatory progression through staging to production with policy gates expressed as "badges." This badge-based governance model let teams customize their pipelines while guaranteeing non-negotiable controls (test coverage, security scan, multi-reviewer approval) could not be bypassed.

For platform/cloud components, Prow provided Kubernetes-native CI tightly integrated with GitHub PR workflows, while Releaser (a homegrown GitOps tool) managed cluster-level deployments by committing YAML specs to a directory-structured Git repo. Multi-cluster progressive rollout was handled by a Federated Deployment Controller that queried an AI-based health detector for automated go/no-go decisions and triggered rollbacks on signal degradation. Security was layered: image scanning (Anchors-based) in staging pipelines, image signing in Tekton, and Kyverno admission policies that rejected unverified images at deploy time — creating defense in depth without manual checkpoints slowing teams down.

The platform was measured against DORA metrics plus rollout/rollback duration and success rate. Key velocity improvements came from incremental builds (Bazel for Go components), selective test execution, parallel validation steps, and elimination of manual approval gates. Major reliability incidents (API server overload from pipeline traffic, node pool exhaustion from too many slave pods) were resolved by adding an API gateway/queue layer, APF configuration, and dedicated CI node pools. The overarching design philosophy: give teams full self-service with visual tooling, enforce standards via automated policy rather than human review, and treat CI/CD infrastructure reliability with the same rigor as production services.

## Key Terms

**CI engines**
- `Jenkins` · `Jenkinsfile` · `Shared Library` · `Multibranch Pipeline` · `kubernetes-plugin` · `GitHub Actions` · `workflow_call` · `matrix` · `OIDC federation` · `ARC (Actions Runner Controller)` · `Tekton` · `Task` · `Pipeline` · `PipelineRun` · `TriggerBinding` · `EventListener` · `Prow` · `GitLab CI` · `Buildkite` · `Drone`

**GitOps CD**
- `ArgoCD` · `Application` · `ApplicationSet` · `AppProject` · `sync wave` · `sync hook` · `selfHeal` · `prune` · `ServerSideApply` · `app-of-apps` · `PR preview env` · `Flux` · `GitRepository` · `OCIRepository` · `Kustomization` · `HelmRelease` · `Weave GitOps` · `Jenkins X`

**Progressive delivery**
- `Argo Rollouts` · `Rollout` · `AnalysisTemplate` · `AnalysisRun` · `Experiment` · `setWeight` · `Flagger` · `Spinnaker` · `canary` · `blue-green` · `shadow` · `champion-challenger`

**Manifest packaging**
- `Helm` · `chart` · `values.yaml` · `Helm hooks` · `OCI chart` · `Kustomize` · `overlay` · `patch` · `Timoni` · `cdk8s` · `CUE`

**Container build**
- `Kaniko` · `BuildKit` · `ko` · `Buildpacks` · `rootless build` · `layer cache` · `multi-stage`

**Registries**
- `Harbor` · `ECR` · `GCR` · `ACR` · `Artifactory` · `OCI artifact` · `replication` · `proxy cache` · `retention policy`

**Policy & admission**
- `Kyverno` · `OPA/Gatekeeper` · `Rego` · `ValidatingAdmissionPolicy` · `mutate` · `validate` · `generate`

**Secrets**
- `HashiCorp Vault` · `Vault Agent Injector` · `External Secrets Operator (ESO)` · `SecretStore` · `Sealed Secrets` · `AWS Secrets Manager` · `GCP Secret Manager` · `CSI driver` · `KMS envelope encryption`

**Supply chain**
- `cosign` · `Sigstore` · `OIDC keyless signing` · `SLSA` · `SLSA-3` · `in-toto attestation` · `Tekton Chains` · `Syft` · `SBOM` · `SPDX` · `CycloneDX` · `provenance`

**Scanning**
- `Trivy` · `Grype` · `Snyk` · `Anchore` · `Dependency-Track` · `SAST` · `SCA` · `CVE` · `license scan`

**Build systems**
- `Bazel` · `Gradle` · `Maven` · `Turborepo` · `Nx` · `remote cache` · `incremental build`

**Feature flags**
- `LaunchDarkly` · `Unleash` · `Flagsmith` · `Split.io` · `dark launch` · `targeted rollout` · `flag debt`

**DORA & velocity**
- `lead time for changes` · `deployment frequency` · `change failure rate` · `MTTR` · `rollback duration` · `elite/high/medium/low tier`

**Platform reliability patterns**
- `API Priority and Fairness (APF)` · `pipeline gateway queue` · `dedicated node pool` · `taints/tolerations` · `selective test execution` · `build cache hit rate` · `spot/preemptible workers` · `flaky test quarantine`

**Trunk vs branch**
- `trunk-based development` · `short-lived branch` · `feature flag` · `release train` · `merge queue`

**ML-specific CD**
- `model registry (MLflow, W&B)` · `shadow mode` · `champion-challenger` · `offline eval` · `online eval` · `data validation gate` · `drift detection`

## Raw Material
- [[raw_material/tech/infra/CI-CD Pipeline Engineering - personal]]
