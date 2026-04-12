---
title: CI/CD Pipeline Engineering
category: tech/infra
tags: [ci-cd, jenkins, tekton, prow, argocd, pipeline, build-automation, devops, gitops, kaniko, dora]
status: in-progress
priority: high
last_updated: 2026-04-11
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
| CI (hosted) | GitHub Actions, GitLab CI, CircleCI | SaaS convenience, tight SCM integration |
| CI (self-hosted) | Jenkins, Tekton, Prow | Control, on-prem, K8s-native |
| CD / GitOps | ArgoCD, Flux | Declarative, drift detection, multi-cluster |
| Progressive delivery | Argo Rollouts, Flagger | Automated canary with metric-based promotion |
| Build | Bazel, Gradle, Maven, Turborepo | Monorepo caching, language-specific |
| Container build | Kaniko, BuildKit, ko | Rootless, cache-efficient, K8s-native |
| Image registry | ECR, GCR, Harbor, Artifactory | Cloud-native vs. self-hosted governance |
| Secret injection | HashiCorp Vault, AWS Secrets Manager, External Secrets Operator | Centralized rotation vs. K8s-native sync |
| Policy enforcement | Kyverno, OPA/Gatekeeper | Admission control for image/config compliance |
| Scanning | Trivy, Grype, Snyk, Anchore | SAST/SCA/image CVE scanning |

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

## Raw Material
- [[raw_material/tech/infra/CI-CD Pipeline Engineering - personal]]
