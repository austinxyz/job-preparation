---
title: eBay - CI/CD Platform Architecture and Reliability
type: Additional
signal_areas: [Scope, Ownership, Leadership]
skills:
  - ci-cd
  - jenkins
  - tekton
  - prow
  - gitops
  - kaniko
  - kyverno
  - platform-engineering
  - supply-chain-security
  - dora-metrics
  - incident-management
company: eBay
date: 2024-06
impact: high
growing_link:
---

# eBay - CI/CD Platform Architecture and Reliability

## Context

My team's CI/CD responsibility at eBay had a clear boundary — important to name explicitly because the two systems involved are often confused.

**Direct ownership:** The Cloud Control Plane CI/CD pipeline (Prow + Releaser), which handled deployments of Kubernetes control plane components across 200+ clusters. My team designed, operated, and was accountable for this pipeline end-to-end.

**Infrastructure partnership:** The ECD platform (CIaaS/Jenkins + Tekton), owned by a dedicated platform team and serving hundreds of application teams. My team provided the Kubernetes infrastructure layer ECD ran on, contributed K8s enhancements, and jointly resolved infrastructure-layer reliability incidents.

Both systems were experiencing compounding reliability problems: pipeline traffic caused cascading pressure on the Kubernetes API server; CI worker node pools were exhausted by concurrent pod creation from Jenkins and Tekton workloads; and a bad base image had once propagated through all downstream application image scan gates simultaneously. On the Cloud Control Plane side specifically, our Prow + Releaser pipeline lacked structured progressive rollout and automated rollback capability.

## Actions

**Cloud Control Plane CI/CD Pipeline (direct ownership):**
- My team established Prow as the CI layer — an existing open-source solution, Kubernetes-native and GitHub PR-integrated, with e2e tests as a mandatory merge gate (≥2 reviews + e2e pass required before merge).
- Releaser was a pre-existing homegrown GitOps CD tool managing YAML specs per environment/cluster; I contributed enhancement suggestions to improve its rollout health monitoring and triage capabilities.
- ArgoCD adoption as a future replacement for Releaser was an org-wide direction; I had my team move on it proactively as the community-supported path to multi-cluster fleet management at greater scale.

**Federated Deployment Controller (K8s enhancement, contributed to ECD):**
- I led the team to build a custom K8s controller that orchestrated progressive rollouts across multiple clusters — progressively shifting workloads cluster by cluster, querying a third-party AI-based health detector service for automated go/no-go signals, and triggering automatic rollback on degradation.
- This controller was built for our own Cloud Control Plane deployments. The ECD team adopted it as their standard multi-cluster CD mechanism — my team owned the controller, ECD team consumed it at platform scale.

**Infrastructure Support for ECD:**
- My team provided and maintained the Kubernetes infrastructure layer ECD ran on: Jenkins Master/Slave node pools, Tekton worker pools, image registry (ECR) access, and network connectivity.
- On supply chain security, I participated in discussions with the ECD team at the infrastructure layer; our tech lead provided the solution — Kyverno admission policies to enforce image signing at deploy time, so that even if pipeline-level checks were bypassed, the cluster itself would reject unsigned images.
- My team integrated the Global Information Security team's Anchors-based image scanner as a shared infrastructure service available to both ECD and Cloud Control Plane pipelines.

**Reliability Incidents (infrastructure layer, joint resolution with ECD):**
- *API server overload:* Pipeline traffic from Tekton and Jenkins pod lifecycle calls spiked API server load during peak build windows. My team applied APF to rate-limit CI/CD traffic; I worked with the ECD team to add a gateway layer that queued pipeline job submissions and monitored total in-flight job count.
- *Node pool exhaustion:* Concurrent Jenkins slave pod creation and Tekton pipeline pods competed for shared node capacity, causing scheduling delays and evictions. My team provisioned dedicated CI/CD node pools with taints to isolate pipeline workloads and improved observability on pod lifecycle metrics.
- *Bad base image propagation:* A base image with a CVE reached the shared registry and caused all downstream application image scans to fail simultaneously. My team worked with GIS and ECD to enforce a stricter multi-stage validation gate on base image releases: security scan + sign + approval required before any team could reference a new base image version.

**DORA Metrics:**
- DORA metrics adoption was an org-wide initiative; my team implemented it proactively, giving engineering leadership a unified view of CI/CD health (lead time, deployment frequency, rollout duration, rollback duration, success rate) across both platforms.

## Results

- Cloud Control Plane pipeline: multi-cluster progressive rollout with automated rollback established; Prow + Releaser reduced manual deployment intervention and provided structured rollout visibility across 200+ clusters.
- Federated Deployment Controller adopted by ECD as the standard multi-cluster CD mechanism — a capability built for our own use that scaled to platform-wide adoption.
- CI/CD-induced API server incidents eliminated after APF + gateway layer implementation.
- Node pool exhaustion incidents eliminated; dedicated CI/CD pools isolated pipeline workloads from production scheduling.
- Bad base image propagation risk addressed; the multi-stage validation gate prevented recurrence.
- DORA metrics gave engineering leadership a unified, quantitative view of CI/CD health across both platforms.

## Learnings

- Boundary clarity was operationally load-bearing. I wasn't the architect of ECD's pipeline design or governance — but I was fully accountable for the infrastructure layer it ran on. Getting that boundary right, and repeating it clearly in cross-team conversations, prevented both scope creep and accountability gaps. When reliability incidents happened, everyone knew which team owned which layer.
- The Federated Deployment Controller's platform-wide adoption happened because we built it to solve a real problem (multi-cluster progressive rollout with health-gated rollback) rather than as a contribution project. Infrastructure teams create leverage when they build something for their own workload that turns out to generalize — not when they build something they think other teams should use.
- Treating pipeline infrastructure as a first-class monitored service (not just a dependency) was what allowed us to catch and resolve the API server overload and node pool exhaustion incidents before they became chronic. Adding queue depth, pod saturation, and APF pressure to our alerting surfaced these patterns early.

## Signal Areas

**Primary:** Scope (direct ownership of 200+ cluster deployment pipeline + infrastructure partnership for hundreds of application teams; both scopes active simultaneously), Ownership (clear accountability boundary across two systems; each incident response, each contribution, scoped to the layer my team actually owned)

**Secondary:** Leadership (Federated Deployment Controller adopted at platform scale by ECD; DORA metrics established as shared measurement framework across both platforms)

## Related Skills
- [[skills/tech/infra/CI-CD Pipeline Engineering]]
- [[skills/tech/infra/Kubernetes]]
- [[skills/tech/infra/SRE Practices and SLO Engineering]]
- [[skills/management/project/Developer Productivity and DORA Metrics]]

## Interview Usage
- 适用 BQ：Tell me about a time you built a platform component that was adopted by another team at scale
- 适用 BQ：How do you work effectively as an infrastructure partner to a platform team you don't own?
- 适用 BQ：Describe a time CI/CD infrastructure caused production incidents — what did you do?
- 适用 BQ：Tell me about a time you improved developer velocity with measurable results
- 适用 Technical：How would you design a multi-cluster progressive deployment system?
- 适用 Technical：How do you secure a CI/CD supply chain at the infrastructure layer?
- 适用 JD 关键词：CI/CD, GitOps, multi-cluster deployment, Kubernetes, DORA metrics, supply chain security, platform engineering, incident management, infrastructure reliability

## Key Questions

**Q: How do you contribute effectively to a platform you don't own?**
Talking points: Clarify the boundary explicitly — own the infrastructure layer, contribute K8s enhancements, but don't make decisions that belong to the platform team. Build shared capabilities (Federated Deployment Controller) that solve a real problem for the platform team, not just for yourself. Establish a joint incident response model for issues that span the boundary. The relationship works when both teams understand what they own and trust the other team's domain expertise.

**Q: How do you design a multi-cluster progressive deployment system with automated rollback?**
Talking points: Federated Deployment Controller as the orchestration layer — cluster-by-cluster progressive rollout, not all-at-once. Health signal from an AI-based health detector provides the go/no-go gate between clusters. Automatic rollback triggered on signal degradation, not on fixed timeout. Directory-per-cluster GitOps structure provides auditability — you can always see which spec version is deployed where.

**Q: How do you design CI/CD infrastructure that doesn't become a reliability liability for production systems?**
Talking points: Isolate CI/CD compute into dedicated node pools (taints/tolerations) so pipeline spikes can't starve production scheduling. Apply APF to rate-limit CI/CD traffic class against the API server — pipeline jobs are lower priority than user-facing workloads. Add a gateway/queue layer to absorb burst job submissions. Treat pipeline infrastructure as a first-class monitored service: success rate, queue depth, node saturation all have alerts.

**Q: Walk me through how you secured the CI/CD supply chain at the infrastructure layer.**
Talking points: My team's responsibility was the runtime enforcement layer, not the pipeline scanning itself. Kyverno admission policies ensured that even if an image bypassed pipeline-level checks, it couldn't deploy — the cluster itself rejected it. Anchors-based image scanner provided shared scanning infrastructure available to both pipelines. Base image validation gate added after the bad image incident: security scan + signing required before any team could reference a new base image version.

**Q: How do you measure CI/CD platform health when you only own part of the stack?**
Talking points: DORA metrics as a shared language — lead time and deployment frequency are outcomes that depend on both the platform team's pipeline and your team's infrastructure. Joint ownership of the metric creates joint accountability. For the Cloud Control Plane pipeline specifically, rollout duration and rollback rate are primary indicators of Prow + Releaser's effectiveness.

## Summary

My team's CI/CD responsibility at eBay had a clear boundary: direct ownership of the Cloud Control Plane pipeline (Prow + Releaser) for 200+ clusters, and infrastructure partnership for the ECD platform serving hundreds of application teams. This distinction mattered in every cross-team conversation — I wasn't the architect of ECD's pipeline design, and my team adopted existing solutions (Prow, Releaser) rather than building from scratch. What I owned was the operational accountability for the infrastructure layer and the judgment calls about what to adopt, enhance, and contribute.

The Federated Deployment Controller was the most impactful cross-team contribution: a custom K8s controller that orchestrated cluster-by-cluster progressive rollouts with AI-based health detection and automatic rollback. My team built it for our own Cloud Control Plane deployments; it solved a real multi-cluster CD problem for ECD as well, which led to platform-scale adoption. This is the pattern that creates infrastructure team leverage — building something for your own workload that generalizes, rather than building something specifically for others to use.

The reliability incidents (API server overload, node pool exhaustion, bad base image propagation) were all joint problems requiring joint resolution. My team's contribution in each case was at the infrastructure layer: APF configuration, dedicated node pools, admission control policies, base image validation gates. The consistent pattern: add a structural control at the layer you own, verify the incident class is eliminated, and transfer day-to-day monitoring responsibility accordingly.

## Raw Material
- [[raw_material/tech/infra/CI-CD Pipeline Engineering - personal]]
