---
title: eBay Cloud vs AWS - Observations
type: Reflection
topic: [cloud-platform-reflection, private-vs-public-cloud, aws-mapping]
company: eBay
date: 2026-04-21
related_skill: "[[skills/tech/infra/AWS Infrastructure]]"
---

# eBay Cloud vs AWS - Observations

## What This Note Is

This is a reflection, not a STAR story. It maps the six dimensions of [[skills/tech/infra/AWS Infrastructure]] onto the actual work I've been doing as an engineering manager on eBay's Fleet Management / Cloud Platform team. Two cross-references in each section:

- **Observations about eBay** → linked out to specific experience notes for depth
- **Specific experiences** → contrasted against the AWS equivalent to show where they map

The core insight in one sentence: **AWS users think about "how do I use it well and spend less"; an internal cloud platform team thinks about "how do I build it and keep it running."** Consumer vs producer — different KPIs, different skill stacks, different optimization targets.

---

## 1. Compute

**The AWS approach.**
Deep instance family selection (CPU / GPU / Inferentia), multiple pricing models (On-Demand / Savings Plans / Spot), and Karpenter doing just-in-time node provisioning. The user picks instance type and capacity type; compliance (OS hardening, CVE patching) and full node lifecycle (create / maintain / upgrade / decomm) are absorbed by AWS. The user's optimization focus is **cost efficiency** — pick the right instance, use Spot well, let Karpenter bin-pack.

**The eBay approach.**
Fleet Management — the team I run — is exactly the layer AWS handles invisibly for its customers:
- Node compliance and annual tech refresh
- Cluster lifecycle end-to-end (create / maintain / upgrade / decomm)
- A capacity team that carves out dedicated node pools for large internal customers (Search, Hadoop, Data, AI Platform, and general applications)
- Node provisioning exists but is **less flexible than Karpenter** — no autoscaling, and **no multi-SKU in a single node pool**
- Hardware adaptation work so compute SKUs match eBay application profiles
- **GPU integration via the NVIDIA Device Plugin** to expose GPUs as K8s schedulable resources
- **Node-level observability tooling built on eBPF** (typical use case: diagnosing the root cause of disk-full conditions)
- Utilization telemetry (CPU / memory) recently started, with memory as a current focus given pricing pressure — but no ML-driven rightsizing like AWS Compute Optimizer yet

**Links to experiences.**
- The operational pressure of 200+ clusters × two K8s upgrades per year × monthly OS patching × 33% YoY growth is what drove the shift documented in [[experience/eBay - Platform Engineering at Scale]]. The AWS equivalent is EKS managed node groups + Karpenter + a well-maintained base AMI (Bottlerocket or AL2023) — most of this work is simply abstracted away for AWS customers.
- Moving cluster build/decommission from manual multi-week flows to a shared cross-component automation contract is [[experience/eBay - Automated Cluster Management Overhaul]]. The AWS equivalent is the EKS cluster API + CloudFormation StackSets: the cluster itself is just an API object.
- **Workload disruption handling:** AWS users running on Spot instances must design applications to tolerate interruption. Internal-cloud users face the same tolerance requirement during OS upgrades and node remediation — just with different triggers and frequency. The application-level resilience bar is the same.

---

## 2. Network

**The AWS approach.**
Users focus on VPC architecture (CIDR planning, multi-AZ and multi-region topology), subnet segmentation (public / private / isolated), and inter-AZ / inter-region data transfer costs. The building blocks (VPC, routing, NACLs, Gateways, PrivateLink, Transit Gateway) come out of the box; no one is building a network fabric from scratch.

**The eBay approach.**
eBay has a dedicated network team that builds the fabric itself:
- The service mesh migration was targeting istio, but **Envoy sidecar CPU/memory overhead and istiod control plane scalability** together drove an effort toward an **in-house service mesh data plane** (replacing Envoy)
- A **custom network daemon** at the CNI / network runtime layer
- Custom IPAM and load balancer implementations
- L7-specific capabilities have to be built internally — [[experience/eBay - Resolving L7 Traffic Gap]] describes how I worked with the network team to integrate their L7 ramp-up tooling to close a gap in our AZ rebalance workflow. The AWS equivalent is a combination of ALB + Global Accelerator + AWS Shield + Route53 health checks — a few clicks rather than a cross-team integration project.

**Summary:** eBay's network team is doing roughly what AWS's own networking engineers do internally. AWS customers never touch this layer.

---

## 3. Storage & Database

**The AWS approach.**
S3 (object) / FSx for Lustre (training-grade parallel filesystem) / EBS (block) / EFS (shared file), plus Aurora / DynamoDB / ElastiCache. For customers this is a **selection problem**, not a construction problem.

**The eBay approach.**
Cloud Team (us) provides compute; Data Platform Team builds storage and database services on top. That split creates one load-bearing constraint: **these services are all stateful, so the hard requirement on Cloud Team is "no data loss."**

That requirement shapes many design choices:
- Node remediation must be graceful (cordon → drain → eviction), never a hard kill
- Node upgrades and K8s upgrades require compatibility validation with the Data Platform Team
- Stateful clusters cannot be batched with stateless ones during automated lifecycle operations

AWS customers don't reason about any of this — they interact with a managed service endpoint, and the graceful operations happen below the waterline.

---

## 4. IAM

**The AWS approach.**
The IAM policy model — **Effect / Action / Resource / Condition / Principal** (Principal used in resource-based policies) — plus IRSA for Pod-level credentials, Identity Center for unified human access, and a full audit toolkit (Access Analyzer, Access Advisor, policy simulation, CloudTrail). Granular "who can do what on which resource under what conditions," fully auditable and automatable.

**The eBay approach.**
We're building the IAM platform itself, not using someone else's:
- Application ownership expressed via account / group abstractions
- Application-to-application access governed by policy
- **Default service accounts calling services on the K8s apiserver** (the K8s control plane API, not AWS service APIs) — a layer closer to the control plane than AWS IRSA typically operates at
- Backend services like databases treated as "just another application" under the same policy model
- Periodic audit and short-lived credentials for service accounts
- OS / image compliance validation as an additional layer

**Mapping:** internally we're building the equivalent of AWS IAM + Security Hub + Config + Identity Center. AWS customers use the framework; we build the framework.

---

## 5. Observability & Cost

**The AWS approach.**
- **Observability:** a first-party full stack — CloudWatch Metrics, CloudWatch Logs, CloudWatch Alarms, Container Insights (pod/node-level for EKS), and X-Ray for tracing. Capable but **not cheap at scale**.
- **Cost:** Cost Explorer with multi-dimensional breakdowns (service / account / tag / region), Budgets with alerting, Cost Anomaly Detection (ML-based), and rightsizing recommendations from Trusted Advisor / Compute Optimizer. Customer focus is audit, query, and threshold setting.

**The eBay approach.**
- **Observability:** metrics and logs are comprehensive, but primarily serve **our own SRE work to keep the cloud service reliable**, not application team consumption. My deepest work here is documented in [[experience/eBay - SRE Practice Implementation and API Server Reliability]] — multi-tier alerting, burn rate diagnosis across APF / etcd / release signals, and AI-assisted triage using MCP to pull cross-system signals. The AWS equivalent is customers building their own stack on CloudWatch + Prometheus + custom dashboards; at eBay the platform team builds it for itself.
- **Cost:** there is no systematic cost governance layer. A static "account resource quota" concept exists (where "account" is eBay's application-tenant abstraction), but it only limits maximum consumption — it doesn't assess whether consumption is efficient.
- **Gap:** this is one of the most visible deltas against AWS. The AWS combination of tag policy + Cost Explorer + Compute Optimizer + Anomaly Detection has no real internal counterpart. Recent memory pricing has prompted targeted optimization, but no standing program.

---

## 6. Infrastructure as Code

**The AWS approach.**
CloudFormation / CDK / Terraform. Core value: resource provisioning becomes versioned, reviewable, and rollback-capable; the heavy operational work underneath is handled by AWS. IaC is **declarative resource configuration** that **integrates naturally with a DevOps workflow** — CI/CD, version control, change management.

**The eBay approach.**
Our provisioning must first keep the **cloud platform itself running**, so IaC alone is insufficient. The platform requires extensive extensions on top of K8s: operators, controllers, admission webhooks, custom CRDs. The most consequential shift I drove in [[experience/eBay - Platform Engineering at Scale]] was moving **from script-based operations to a declarative CRD + controller model** for cluster lifecycle — users declare desired state, the platform reconciles toward it. The AWS equivalent is exactly what CloudFormation does; AWS just exposes CFN templates to customers rather than CRDs.

So eBay's IaC story is really two layers:
- **Internal layer:** CRDs and controllers managing the platform itself (invisible to application users)
- **User-facing layer:** a Terraform-equivalent IaC abstraction for application teams could be built on top of the CRD layer — **but we haven't built it yet**. This is a well-defined capability gap.

---

## Synthesis

**The role definitions differ at the foundation.**
AWS customer = cloud consumer, optimizing for efficiency and cost. Internal cloud team = cloud producer, optimizing for reliability, operability, and compliance. Different KPIs, different skills, different decision frameworks.

**What we do ≈ a scoped version of AWS's own platform work.**
Compute lifecycle, IAM platform, network fabric, observability stack — all the layers AWS absorbs on behalf of customers. We are effectively running a "mini AWS" internally, narrower in scope (eBay-only) and less mature in tooling, but the same category of work.

**Using cloud well still requires understanding it deeply.**
Even if an organization moves entirely to AWS, extracting maximum value still requires understanding the internals and cloud-native application design. The producer experience is **the depth half of a T-shaped profile** — it makes the person a stronger consumer, not a redundant one.

---

## Where eBay Cloud Could Get Stronger

**Offer more AWS-like higher-level services.** Today we provide compute + K8s; users still have to assemble observability, cost management, and service abstractions themselves.

**Absorb more of the operational work AWS hides from users.** Application teams should declare desired state and deploy; provisioning, remediation, and upgrades should be platform responsibilities. This is the natural extension of the ops-to-platform shift from [[experience/eBay - Platform Engineering at Scale]].

**Optimize for the application PDLC.** Developer productivity — build, test, deploy, observe, rollback — should feel as smooth as using AWS, without requiring application teams to understand K8s internals.

**Close the user-facing IaC and cost governance gaps.** These are the two clearest deltas against AWS:
- Build a Terraform-equivalent user-facing IaC layer on top of internal CRDs (unlocks self-service)
- Introduce tag policy, per-tenant cost attribution, and rightsizing recommendations (direct financial return)

---

## Related

**Skill:** [[skills/tech/infra/AWS Infrastructure]]

**Experiences referenced:**
- [[experience/eBay - Platform Engineering at Scale]] — CRD + controller, self-service platform; AWS equivalent: CloudFormation + EKS
- [[experience/eBay - Automated Cluster Management Overhaul]] — cluster lifecycle automation; AWS equivalent: EKS cluster API + StackSets
- [[experience/eBay - SRE Practice Implementation and API Server Reliability]] — observability + AI triage; AWS equivalent: CloudWatch + X-Ray + custom analytics
- [[experience/eBay - Resolving L7 Traffic Gap]] — L7 capability integration; AWS equivalent: ALB + Global Accelerator
- [[experience/eBay - Cloud Migration to Kubernetes]] — 5,000-application migration; AWS equivalent: EKS migration at scale

---

## How to Use This Note

This reflection supports several interview scenarios:

**Behavioral:**
- Tell me about a time you evaluated your team's work against an industry benchmark and identified gaps.
- How do you think about the difference between running a private cloud and using a public cloud?
- What would you bring from your private-cloud experience to an AWS-native team?

**Technical:**
- If your company migrated from private cloud to AWS tomorrow, which parts of your current work would become obsolete, and which would become more valuable?
- Where does your private cloud come up short compared to AWS, and what would you invest in first?

**JD keyword coverage:** hybrid cloud, cloud platform engineering, cost optimization, platform vs consumer perspective, cloud-native, private cloud, AWS, Kubernetes lifecycle, IAM platform.

---

## Key Questions (Likely Follow-Ups)

**Q: You've run a private cloud. If you joined an AWS-native team tomorrow, what would you lean on from that experience?**
Talking points: Deep understanding of the layers AWS hides — node lifecycle, IAM platform, network fabric, observability stack — makes you a **sharper AWS consumer**, not a slower one. Specifically: (1) knowing what to measure (per-team reliability + cost, not just uptime), (2) knowing where cloud abstractions leak (OS patching, tech refresh, stateful workload handoffs all still exist, just in different shapes), (3) knowing the thin layer of extension an AWS-native team still has to build (IaC modules, cost guardrails, service abstractions). Private-cloud background means you understand *why* each AWS feature exists rather than treating it as magic.

**Q: Where does eBay's private cloud fall short compared to AWS, and what would you invest in first?**
Talking points: Three concrete gaps. (1) **User-facing IaC**: internal CRDs exist but no Terraform-equivalent for users. (2) **Cost governance**: tag policy, per-team cost attribution, and rightsizing recommendations are largely absent. (3) **Higher-level service abstractions**: we provide compute + K8s; AWS provides managed databases, queues, caches, and observability as composable services. Sequencing by ROI: user-facing IaC first (unlocks self-service), cost governance second (direct financial return), service abstractions as a longer-horizon investment requiring co-build with framework teams.

**Q: What's the fundamental difference between your eBay role and an AWS customer's role?**
Talking points: Producer vs consumer. AWS customers optimize for cost and velocity; we optimize for the platform's own reliability, compliance, and operability. Different KPIs, different skills, different decision frameworks — but the line is blurring. At sufficient scale, AWS customers also need to understand cloud internals (EFA, Spot, Karpenter, IAM depth). A T-shaped engineer who has been a producer tends to become a stronger consumer.

**Q: How would you bring cost discipline to an organization that has none?**
Talking points: Tagging is foundational — without tags, cost is invisible; enforce via policy (AWS Tag Policy or admission webhook), not process discipline. Then build per-team / per-project attribution dashboards so engineers see their own spend. Then automate rightsizing (Compute Optimizer style). Then optimize procurement with Spot / Savings Plans / Reserved Instances. Culturally: make spend a first-class metric reviewed in team ops meetings alongside reliability, not hidden in finance reports. Static quotas limit the downside but don't create accountability — moving from quota to accountability is where real savings come from.

---

## Closing

The value of this note isn't to argue against the work being done today — it's to place "what I'm doing" inside a larger coordinate system. That view makes it clearer **which experience transfers directly, which is producer-specific, which is consumer-specific, and where the next investment should go.**

One sentence: **private cloud and public cloud aren't replacements for each other; they are producer perspective vs consumer perspective. Someone who has been a producer is stronger on either side.** That's the durable value of this experience.
