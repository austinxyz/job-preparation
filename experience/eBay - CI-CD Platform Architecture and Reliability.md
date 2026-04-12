---
title: eBay - CI/CD Platform Architecture and Reliability
type: experience
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

## Situation

eBay operated two CI/CD systems with distinct ownership: the ECD platform (CIaaS/Jenkins + Tekton) was owned by a dedicated platform team and served hundreds of application teams; the Cloud Control Plane CI/CD pipeline (Prow + Releaser) was owned by my team and handled deployment of Kubernetes control plane components across 200+ clusters. My team's relationship with ECD was as an infrastructure partner — we provided the Kubernetes infrastructure layer ECD ran on, contributed K8s enhancements (such as the Federated Deployment Controller), and collaborated on reliability issues when pipeline load impacted API server health.

Both systems faced compounding reliability problems: pipeline traffic caused cascading pressure on the Kubernetes API server, CI worker node pools were exhausted by excessive pod creation, and a bad base image had once propagated through all downstream application image scan gates simultaneously. On the Cloud Control Plane side, our Prow + Releaser pipeline lacked a structured multi-cluster progressive rollout mechanism and automated rollback capability.

## Task

As the Cloud Application Lifecycle Management team manager, I owned two distinct scopes: (1) **direct ownership** of the Cloud Control Plane CI/CD pipeline — designing and operating Prow + Releaser, ensuring safe multi-cluster deployments with automated health checks and rollback; (2) **infrastructure partnership** with the ECD platform team — providing reliable K8s infrastructure for their pipeline workloads, building shared K8s enhancements like Federated Deployment Controller, and jointly resolving infrastructure-layer reliability incidents that affected both systems. I also drove DORA metrics adoption as the shared measurement framework across both platforms, and initiated ArgoCD evaluation as a long-term replacement for Releaser.

## Action

**Cloud Control Plane CI/CD Pipeline (direct ownership):**
- Established Prow as the CI layer: Kubernetes-native, GitHub PR-integrated, ran e2e tests as a mandatory merge gate (≥2 reviews + e2e pass required before merge).
- Designed Releaser (homegrown GitOps CD) to manage YAML specs per environment/cluster in a directory-structured Git repo; Releaser applied specs, monitored rollout health, and provided a UI for progress tracking and log triage.
- Initiated ArgoCD evaluation to replace Releaser — addressing multi-cluster fleet management at greater scale with a community-supported tool.

**Federated Deployment Controller (K8s enhancement, contributed to ECD):**
- Built a custom K8s controller that orchestrated progressive rollouts across multiple clusters: progressively shifting pods to the new version cluster by cluster, querying an AI-based health detector for automated go/no-go signals, and triggering automatic rollback on degradation.
- This controller was integrated into ECD's deployment pipeline as the multi-cluster CD mechanism — my team owned the controller, ECD team consumed it.

**Infrastructure Support for ECD Platform:**
- Provided and maintained the Kubernetes infrastructure layer ECD ran on: Jenkins Master/Slave node pools, Tekton worker pools, image registry (ECR) access, and network connectivity.
- Collaborated with ECD team on supply chain security enhancements at the infrastructure layer: Kyverno admission policies to enforce image signing at deploy time, ensuring pipeline-level security controls had a runtime enforcement backstop regardless of which pipeline produced the image.
- Worked with the Global Information Security team on integrating their Anchors-based image scanner as a shared infrastructure service available to both ECD and Cloud Control Plane pipelines.

**Reliability Incident Resolution (infrastructure layer, joint with ECD team):**
- *API server overload*: Pipeline traffic from both Tekton and Jenkins slave pod lifecycle calls spiked K8s API server load during peak build windows. My team applied API Priority and Fairness (APF) to rate-limit CI/CD traffic classes; worked with ECD team to add a gateway layer that queued pipeline job submissions and monitored total in-flight job count.
- *Node pool exhaustion*: Concurrent slave pod creation (Jenkins) and Tekton pipeline pods competed for shared node capacity, causing scheduling delays and evictions. My team provisioned dedicated CI/CD node pools with taints to isolate pipeline workloads, and improved observability on pod lifecycle metrics.
- *Bad base image propagation*: A base image with a CVE reached the shared registry and caused all downstream application image scans to fail. My team worked with GIS and ECD to enforce a stricter multi-stage validation gate on base image releases (security scan + sign + approval required before any team could reference the image).

**DORA Metrics Adoption:**
- Drove adoption of DORA metrics (lead time, deployment frequency, rollout duration, rollback duration, success rate) as the shared measurement framework for both platforms — giving engineering leadership a unified view of CI/CD health across the org.

## Result

- Cloud Control Plane CI/CD pipeline: multi-cluster progressive rollout with automated rollback established; Prow + Releaser reduced manual deployment intervention and provided structured rollout visibility.
- Federated Deployment Controller adopted by ECD team as the standard multi-cluster CD mechanism — my team's K8s contribution consumed at platform scale.
- CI/CD pipeline-induced API server incidents eliminated after APF + gateway layer; API server availability improved as a direct consequence.
- Node pool exhaustion incidents eliminated; dedicated CI/CD pools isolated pipeline workloads from production scheduling.
- Base image propagation risk addressed; stricter multi-stage validation gate prevented recurrence.
- DORA metrics adoption gave engineering leadership a unified, quantitative view of CI/CD health across both platforms.

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
Talking points: Clarify the boundary clearly — own the infrastructure layer, contribute K8s enhancements, but don't make decisions that belong to the platform team. Build shared capabilities (Federated Deployment Controller) that solve a real problem for the platform team, not just for yourself. Establish a joint incident response model for issues that span the boundary (CI/CD traffic → API server). The relationship works when both teams understand what they own and trust the other team's domain expertise.

**Q: How do you design a multi-cluster progressive deployment system with automated rollback?**
Talking points: Federated Deployment Controller as the orchestration layer — cluster-by-cluster progressive rollout, not all-at-once. Health signal from an AI-based health detector provides the go/no-go gate between clusters. Automatic rollback triggered on signal degradation, not on fixed timeout. Directory-per-cluster GitOps structure in Releaser provides auditability — you can always see which spec version is deployed where.

**Q: How do you design CI/CD infrastructure that doesn't become a reliability liability for production systems?**
Talking points: Isolate CI/CD compute into dedicated node pools (taints/tolerations) so pipeline spikes can't starve production scheduling. Apply APF to rate-limit CI/CD traffic class against the API server — pipeline jobs are lower priority than user-facing workloads. Add a gateway/queue layer to absorb burst job submissions. Treat pipeline infrastructure as a first-class monitored service: success rate, queue depth, node saturation all have alerts.

**Q: Walk me through how you secured the CI/CD supply chain at the infrastructure layer.**
Talking points: My team's responsibility was the runtime enforcement layer, not the pipeline scanning itself. Kyverno admission policies ensured that even if an image bypassed pipeline-level checks, it couldn't deploy — the cluster itself rejected it. Anchors-based image scanner provided shared scanning infrastructure available to both pipelines. Base image validation gate added after the bad image incident: security scan + signing required before any team could reference a new base image version.

**Q: How do you measure CI/CD platform health when you only own part of the stack?**
Talking points: DORA metrics as a shared language — lead time and deployment frequency are outcomes that depend on both the platform team's pipeline and your team's infrastructure. Joint ownership of the metric creates joint accountability. For the Cloud Control Plane pipeline specifically, track rollout duration and rollback rate as primary indicators of the Prow + Releaser system's effectiveness.

## Summary

My team's CI/CD responsibility at eBay had a clear boundary: we directly owned the Cloud Control Plane CI/CD pipeline (Prow + Releaser), and we were the infrastructure partner for the ECD platform that served hundreds of application teams. This distinction mattered operationally — I wasn't the architect of ECD's badge-based governance or Tekton pipeline design, but I was responsible for the Kubernetes infrastructure layer ECD ran on, and for K8s enhancements like the Federated Deployment Controller that ECD consumed.

The Federated Deployment Controller was the most impactful cross-team contribution: a custom K8s controller that orchestrated cluster-by-cluster progressive rollouts with AI-based health detection and automatic rollback. My team built it for our own Cloud Control Plane deployments, but it solved a real multi-cluster CD problem for ECD as well, which led to its adoption at platform scale. This is a concrete example of infrastructure team leverage — building a capability that multiplies its value by being adopted beyond your own team's workloads.

The reliability incidents (API server overload from pipeline traffic, node pool exhaustion, bad base image propagation) were all joint problems requiring joint resolution with ECD and the security team. My team's contribution in each case was at the infrastructure layer: APF configuration, dedicated node pools, admission control policies, base image validation gates. The pattern across all three: add a structural control at the layer you own, verify the incident class is eliminated, and transfer the monitoring responsibility to the team that operates that layer day-to-day.

## Raw Material
- [[raw_material/tech/infra/CI-CD Pipeline Engineering - personal]]
