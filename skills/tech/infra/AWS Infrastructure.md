---
title: AWS Infrastructure
category: tech/infra
tags: [aws, eks, vpc, iam, s3, rds, aurora, dynamodb, ec2, cloud, infrastructure-as-code, gcp, gke, private-cloud, multi-cloud]
status: in-progress
priority: high
last_updated: 2026-04-12
created_from_jd: "[[positions/Manager, DevOps, SRE & AI Infrastructure - AppZen]]"
---

# AWS Infrastructure

## Knowledge Map
- 前置知识：cloud fundamentals (VPC, IAM, compute, storage), Linux networking, Kubernetes, Terraform
- 延伸话题：[[EKS]] vs GKE vs self-managed K8s, GCP TPU ecosystem (TPU v4/v5, JAX), AWS networking (Transit Gateway, PrivateLink, Direct Connect), [[Karpenter]] for GPU node provisioning, FSx for Lustre vs GCS FUSE vs Ceph, hybrid cloud scheduling (Volcano, Armada), SageMaker vs Vertex AI vs self-managed
- 管理关联：cloud cost management, CapEx vs OpEx tradeoffs, vendor lock-in decisions, FinOps culture, Spot/Preemptible strategy for ML training, hybrid cloud architecture, private cloud build-vs-buy

## Core Concepts

### Compute
- **EC2 instance families for AI**: P4d (A100 8x, 400Gbps EFA), P3 (V100), G5 (A10G inference), Trn1 (Trainium), Inf2 (Inferentia2) — choose by workload: training vs inference, memory bandwidth, NVLink topology
- **Spot Instances**: up to 90% discount; ideal for fault-tolerant ML training; use Spot interruption handlers + checkpoint-resume to survive 2-min warnings; mix with On-Demand for critical jobs
- **Savings Plans / Reserved Instances**: Compute Savings Plans cover EC2+Fargate+Lambda across families; 1yr no-upfront ≈ 30%, 3yr all-upfront ≈ 60%; use for baseline On-Demand capacity, Spot for burst
- **EKS Managed Node Groups vs Karpenter**: Node Groups = static pools, simple but slow to scale; Karpenter = just-in-time provisioning, bin-packs pods onto cheapest fitting instance, preferred for GPU clusters

### Networking
- **VPC design**: CIDR planning matters — use /16 per VPC, /24 per subnet; private subnets for workloads, public subnets only for NAT GW / load balancers; avoid 10.0.0.0/8 conflicts with on-prem if using Direct Connect
- **Availability Zones**: spread critical workloads across ≥3 AZs; AZ-affinity matters for latency-sensitive multi-GPU training (inter-AZ traffic adds latency and cost)
- **EFA (Elastic Fabric Adapter)**: required for multi-node GPU training (NCCL over EFA); enables OS-bypass RDMA-like communication; cluster placement groups keep nodes physically close for EFA performance
- **PrivateLink / VPC Endpoints**: keep S3, ECR, DynamoDB traffic off public internet; Gateway Endpoints (S3, DynamoDB) are free; Interface Endpoints (ECR, SSM) cost per-hour + per-GB
- **Transit Gateway**: hub-and-spoke for multi-VPC / multi-account; scales to thousands of VPCs; replace VPC peering mesh above ~5 VPCs; supports inter-region peering
- **Security Groups vs NACLs**: SGs are stateful (return traffic auto-allowed), NACLs are stateless; use SGs as primary firewall, NACLs for subnet-level deny rules

### IAM & Security
- **Least privilege principle**: start with deny-all, grant only required actions on specific resources; use IAM Access Analyzer to find overly permissive policies
- **IRSA (IAM Roles for Service Accounts)**: EKS pods assume IAM roles via OIDC federation; eliminates need for node-level IAM roles or long-lived credentials in pods; standard pattern for S3/DynamoDB access from training jobs
- **KMS**: encrypt S3 buckets (SSE-KMS), EBS volumes, RDS at rest; control key access via key policy + IAM; use CMKs for audit trail and rotation control
- **AWS Organizations + SCPs**: Service Control Policies enforce guardrails across all accounts (e.g., block regions, prevent disabling CloudTrail); use with multi-account strategy (prod/staging/dev/security accounts)
- **Multi-account strategy**: separate blast radius; prod workloads in dedicated account; shared services (VPN, DNS, ECR) in shared-services account; billing consolidated under management account

### Storage
- **S3**: durable (11 9s), scalable object store; use for ML datasets, model artifacts, checkpoints; S3 Intelligent-Tiering auto-moves objects between frequent/infrequent/archive tiers; prefix partitioning for high-throughput (avoid sequential prefixes that hit same shard)
- **FSx for Lustre**: high-throughput parallel filesystem (up to 1 TB/s); ideal for training data that must be local-speed; can be backed by S3 (lazy-load on first access); use Scratch (cheaper, no replication) for ephemeral training, Persistent for shared datasets
- **EBS**: block storage attached to EC2; GP3 (cheaper baseline IOPS, configurable up to 16K IOPS), io2 Block Express (high IOPS, SAN-level durability) for databases; not shared — one EC2 at a time
- **EFS**: managed NFS, shared across multiple EC2/EKS pods; lower throughput than FSx Lustre but simpler ops; good for config sharing, small shared datasets

### Databases
- **RDS Aurora**: MySQL/Postgres compatible; cluster with 1 writer + up to 15 read replicas; Aurora Serverless v2 auto-scales in fine-grained ACUs (good for variable workload); storage auto-grows
- **DynamoDB**: serverless key-value/document; single-digit ms latency at any scale; on-demand capacity avoids over-provisioning; DynamoDB Streams for event-driven workflows; good for metadata stores in ML pipelines (job status, artifact registry)
- **ElastiCache (Redis)**: in-memory caching; use for feature caching, session state, rate limiting; cluster mode for horizontal scaling

### Observability & Cost
- **CloudWatch**: default metrics, logs, alarms; custom metrics via PutMetricData; Container Insights for EKS pod/node metrics; Log Insights for ad-hoc queries
- **AWS Cost Explorer + Budgets**: tag-based cost allocation (team, env, project tags mandatory); anomaly detection for surprise spend; Budgets can trigger SNS/Lambda actions
- **Trusted Advisor / Compute Optimizer**: right-sizing recommendations for EC2, EBS, Lambda; Compute Optimizer uses ML on CloudWatch metrics to suggest cheaper instance types

### Infrastructure as Code
- **CloudFormation**: AWS-native IaC; strong resource coverage; drift detection; StackSets for multi-account/region deployment; slower than Terraform for iterative dev
- **CDK (Cloud Development Kit)**: imperative IaC in TypeScript/Python/Go; generates CloudFormation; preferred for complex logic (loops, conditionals); good for teams already writing code
- **Terraform**: multi-cloud, large community; state management (remote state in S3+DynamoDB lock); workspaces for environments; preferred when org uses GCP/Azure too

### AWS vs GCP vs Private Cloud (K8s)

#### Managed Kubernetes: EKS vs GKE vs Self-managed
| Dimension | EKS (AWS) | GKE (GCP) | Self-managed K8s (Private Cloud) |
|-----------|-----------|-----------|----------------------------------|
| Control plane ops | AWS-managed (you pay per cluster/hr) | Google-managed, more opinionated | You own etcd, API server, upgrades |
| Autoscaling | Karpenter (best-in-class, just-in-time) | GKE Autopilot (fully managed nodes) or Node Auto Provisioner | Cluster Autoscaler; slower, less flexible |
| GPU support | EFA for multi-node RDMA, P4d/P3/G5 | GPUDirect RDMA on A3 (H100), A100 | Depends on HW vendor; RDMA config is DIY |
| Networking | VPC-native pods (aws-vpc-cni), ENI-based | VPC-native (alias IPs), cleaner IP management | Calico/Cilium/Flannel; you pick and maintain |
| IAM integration | IRSA (OIDC → IAM roles per service account) | Workload Identity (OIDC → GCP Service Account) | Vault, cert-manager, or cloud IAM if hybrid |
| Upgrade experience | Manual node group rolling upgrades; Karpenter helps | GKE handles node upgrades more automatically | Fully manual; kubeadm/Rancher/OpenShift tooling |
| Cost model | Per cluster ($0.10/hr) + EC2 nodes | GKE Standard: per node; Autopilot: per pod resource | CapEx (servers) + OpEx (ops team); no per-API cost |

#### GPU Compute: AWS vs GCP for AI Training
| Dimension | AWS | GCP |
|-----------|-----|-----|
| H100 clusters | P5 (H100 SXM5, 8x, 3200Gbps EFA) | A3 Mega (H100, 8x, GPUDirect RDMA over RoCEv2) |
| A100 clusters | P4d (A100 SXM4, 8x, 400Gbps EFA) | A2 Ultra (A100, 8x) |
| Custom silicon | Trainium (training), Inferentia (inference) | TPU v4/v5 (training), TPU v5e (inference) — mature, unique to GCP |
| Multi-node networking | EFA (proprietary, AWS-only) | GPUDirect RDMA, also RoCEv2; more open-standards based |
| Spot equivalent | EC2 Spot (2-min warning, standard K8s eviction) | Spot VMs (30-sec warning — harder to handle) + Preemptible VMs |
| GPU availability | Historically broader, more regions | TPU availability unique; GPU availability more limited outside US |

**Key insight**: GCP's TPU ecosystem is unmatched for large-scale training if your framework supports it (JAX first-class, PyTorch/XLA); AWS has the broadest GPU variety and deepest Spot infrastructure. Most companies follow the model: train on AWS (GPU depth + Spot maturity) or GCP (TPU for specific workloads), serve on whichever has better inference cost.

#### Storage: AWS vs GCP vs Private
| Dimension | AWS | GCP | Private Cloud |
|-----------|-----|-----|---------------|
| Object store | S3 (11 9s, strong consistency since 2020) | GCS (strong consistency, similar durability) | Ceph/MinIO (S3-compatible; you manage replication) |
| Parallel FS for training | FSx for Lustre (up to 1 TB/s, S3-backed) | Filestore (NFS, lower throughput); GCS FUSE (fuse-mounted, not fast) | GPFS / Lustre on-prem; high-performance but CapEx-heavy |
| Block storage | EBS GP3/io2 | Persistent Disk (pd-ssd, pd-extreme) | Ceph RBD, iSCSI, NVMe-oF |
| GCP advantage | — | GCS → BigQuery integration is seamless for ML analytics | Latency: local NVMe is unbeatable for hot data |

#### Identity & Access: AWS vs GCP vs Private
- **AWS IAM**: policy documents (JSON), resource-based + identity-based; IRSA for K8s; complex but very powerful; steep learning curve
- **GCP IAM**: role bindings on resources; simpler mental model (who gets what role on what resource); Workload Identity for GKE; audit logs in Cloud Audit Logs
- **Private cloud**: typically Vault (secret management + dynamic credentials), cert-manager (mTLS), LDAP/Active Directory for human access; no managed IAM — higher ops burden but full control
- **OIDC federation** is the common bridge: both EKS (IRSA) and GKE (Workload Identity) use OIDC to federate K8s service accounts to cloud IAM; same pattern extends to private cloud using Vault's JWT auth

#### Networking: AWS vs GCP vs Private
- **AWS VPC**: subnet-based, SG + NACL, ENI-per-pod (aws-vpc-cni); each pod gets a routable VPC IP; scales well but ENI limits per instance constrain pod density
- **GCP VPC**: global (spans regions natively, unlike AWS which is regional); alias IP ranges for pods; simpler peering model; Cloud Interconnect for on-prem
- **Private K8s**: Calico (BGP-native, good for bare-metal), Cilium (eBPF, best observability + performance), or Flannel (simple overlay, lower performance); RDMA networking requires SR-IOV and manual configuration
- **Multi-cluster networking**: AWS uses Transit Gateway + EKS; GCP uses Anthos (multi-cluster mesh); private cloud uses Cilium Cluster Mesh or Submariner

#### When to Choose Each
| Scenario | Recommendation |
|----------|----------------|
| Startup, greenfield, ML-heavy | AWS (broadest GPU variety, Spot maturity, EKS + Karpenter ecosystem) |
| JAX/TPU workloads, Google-stack org | GCP (TPU v4/v5, GCS → BigQuery, Vertex AI) |
| Regulated industry (finance/healthcare) with data residency requirements | Private cloud or hybrid (on-prem training data, cloud burst for compute) |
| Multi-cloud to avoid vendor lock-in | Terraform + Kubernetes abstraction layer; accept ops overhead |
| Cost-sensitivity at scale (>1000 GPUs steady state) | Private cloud CapEx often beats cloud at this scale; hybrid = private for baseline + cloud for burst |
| Fast iteration, small team | Managed cloud (EKS or GKE); avoid on-prem K8s ops cost |

#### Private Cloud / On-prem K8s: Key Operational Differences
- **Control plane burden**: etcd backup, API server HA, certificate rotation, upgrades — all on your team; typically use Rancher, OpenShift, or kubeadm+Ansible
- **Node lifecycle**: no auto-replacement of failed nodes; requires runbook + oncall; BMC/IPMI access for hardware failures
- **Storage ops**: Ceph cluster management is a significant operational surface; requires dedicated storage team at scale; MinIO simpler but less feature-rich
- **Networking complexity**: SR-IOV / RDMA configuration for GPU nodes is manual; Calico BGP peering with physical switches requires network team involvement
- **CapEx vs OpEx tradeoff**: at ~1000+ A100s, on-prem CapEx ($10-30k/GPU amortized over 3-4yr) often beats AWS On-Demand ($30+/hr/GPU); but Spot can close this gap significantly; factor in ops team cost
- **Hybrid pattern**: common architecture = on-prem for baseline steady-state training + AWS/GCP Spot burst for peak; requires unified job scheduler (Volcano, Armada) that can span both

## Key Questions

**Q: How would you design VPC architecture for a multi-tenant AI training platform on AWS?**
Answer framework: Start with multi-account strategy (prod/dev/shared-services); use Transit Gateway for connectivity; private subnets for GPU nodes, no public IPs; VPC Endpoints for S3/ECR to avoid NAT costs; EFA + cluster placement groups for multi-node jobs; explain how IRSA controls data access per team/tenant.

**Q: We're spending $2M/month on AWS. How do you drive cost reduction without impacting reliability?**
Answer framework: First instrument (tag everything, Cost Explorer by team/service); identify Spot candidates (fault-tolerant training jobs); right-size with Compute Optimizer; purchase Savings Plans for stable baseline; FSx Lustre Scratch vs Persistent selection; Spot interruption handling maturity; set up Budgets with auto-alerts; cultural change — engineers see their spend.

**Q: A multi-node GPU training job is getting poor network throughput. Walk me through your diagnosis.**
Answer framework: Check if EFA is enabled (aws ec2 describe-instances); verify cluster placement group; check NCCL env vars (NCCL_DEBUG=INFO); look at EFA metrics in CloudWatch; verify instance type supports EFA (p4d, p3dn); check security group allows all traffic within SG; check if cross-AZ (bad — all nodes should be same AZ for EFA).

**Q: How do you handle IAM for a platform where 20 ML teams each need access to their own S3 prefix?**
Answer framework: IRSA with per-team service accounts; IAM policies scoped to s3:prefix via condition keys; no shared credentials; each team's namespace gets its own K8s service account bound to its IAM role; audit via CloudTrail + Access Analyzer; periodic unused-permission review.

**Q: What's your strategy for running ephemeral GPU workloads cost-effectively?**
Answer framework: Karpenter with Spot-first NodePool (fallback to On-Demand); checkpoint-resume in training code; Spot interruption handler (drain node gracefully); diversify instance types to improve Spot availability; use EC2 Fleet with capacity-optimized allocation strategy; measure job completion rate vs cost.

**Q: How do you achieve HA for a critical inference serving API on EKS?**
Answer framework: Multi-AZ node groups; pod anti-affinity to spread across AZs; ALB with cross-zone load balancing; PodDisruptionBudgets; readiness/liveness probes tuned to model load time; HPA on custom metrics (latency p99 or queue depth); blue/green via separate node groups; Route 53 health checks for regional failover.

**Q: Compare RDS Aurora vs DynamoDB for a metadata store in an ML pipeline.**
Answer framework: Depends on access pattern — if queries need SQL joins/aggregations (job history reports, complex filters), Aurora wins; if access is key-based lookups at high scale (artifact registry, feature store index), DynamoDB wins; Aurora Serverless v2 for variable load; DynamoDB for predictable ms latency at any scale; cost model differs (DynamoDB per-request vs Aurora per-ACU-hour).

**Q: How do you enforce governance across 50 AWS accounts?**
Answer framework: AWS Organizations + SCPs (deny non-approved regions, require MFA, block root usage); AWS Config rules for compliance (e.g., all S3 buckets must have encryption); Security Hub aggregates findings; CloudTrail org-wide trail to central S3; Identity Center (SSO) for human access, no long-lived IAM users; tag policies to enforce mandatory tags.

**Q: Your company currently runs all ML training on AWS. The ML team is asking to evaluate GCP for TPU workloads. How do you approach the evaluation?**
Answer framework: Define the workload — JAX-native models benefit most from TPUs; PyTorch models need PyTorch/XLA which adds friction. Benchmark: run same training job on P4d (A100 EFA) vs TPU v4 pod; measure throughput (tokens/sec or samples/sec), cost-per-run, and iteration speed (time from code change to first result). Evaluate ecosystem fit (GCS integration, Vertex AI for experiment tracking). Factor in team expertise cost — switching to TPU requires upskilling. Recommend a contained pilot (1-2 models) before committing; maintain AWS as primary unless TPU shows >30% cost or speed advantage for your specific workloads.

**Q: We're moving from AWS to a private on-prem K8s cluster for cost reasons. What risks would you flag?**
Answer framework: (1) Ops burden increase — control plane, node lifecycle, storage, networking all become your responsibility; need dedicated platform engineering headcount. (2) CapEx commitment — 3-4yr amortization, technology can shift (new GPU architectures). (3) Elasticity loss — no Spot equivalent; must right-size capacity or accept idle GPUs. (4) Slower iteration — no managed services (no Karpenter, no Aurora Serverless, no S3-backed FSx). Mitigation: hybrid architecture (on-prem baseline + cloud burst), strong IaC discipline (Terraform across both), unified job scheduler (Volcano). Only recommend full migration if steady-state GPU count is high enough that CapEx math clearly wins.

**Q: EKS vs GKE — what are the key differences you'd consider when choosing for a new AI platform?**
Answer framework: Autoscaling — Karpenter (EKS) is more flexible and cost-optimized; GKE Autopilot is simpler to operate. Networking — GCP VPC is global (simpler cross-region), AWS VPC is regional. GPU networking — EFA (AWS) vs GPUDirect RDMA (GCP) both support multi-node RDMA; EFA requires specific instance types + placement groups. IAM integration — IRSA (AWS) vs Workload Identity (GCP), both OIDC-based and similar in practice. Managed experience — GKE handles more automatically (node upgrades, scale-to-zero); EKS requires more tuning. Cost: EKS charges per cluster; GKE Standard similar; GKE Autopilot charges per pod resource (can be cheaper for spiky workloads). Bottom line: both are excellent; choose based on existing cloud vendor relationship, GPU needs (H100 availability, TPU access), and team expertise.

**Q: How would you design a hybrid cloud architecture for a company that trains on private GPU clusters but wants to burst to AWS?**
Answer framework: Unified job scheduler spanning both environments (Volcano or Armada for K8s-native scheduling); consistent container registry (ECR or Harbor with mirroring); data plane — training data in on-prem NFS/Lustre, model artifacts synced to S3 post-training; burst trigger = on-prem queue depth or job urgency threshold; network connectivity = Direct Connect or VPN for secure data transfer; IaC with Terraform managing both; unified observability (Prometheus + Grafana federation, or Datadog). Key challenge: data egress costs from on-prem to cloud; minimize by keeping datasets on-prem and only moving model artifacts to cloud.

**Q: A new engineer asks: "Why don't we just run K8s ourselves instead of paying for EKS?" How do you respond?**
Answer framework: Acknowledge the cost concern is valid — EKS charges $0.10/hr/cluster (~$72/mo). Explain the hidden costs of self-managed: etcd backup/restore, API server HA (3 nodes minimum), certificate rotation, K8s upgrades (2-3x/year, each is a multi-day project), CNI plugin maintenance, cloud provider integration (IAM, load balancers, storage drivers). At small scale, self-managed can make sense; at production scale with SLAs, the platform engineering time cost typically far exceeds EKS fees. EKS also gets first-party integration with Karpenter, IRSA, and ALB ingress controller. Recommend EKS for most cases; self-managed only if strong regulatory requirements or multi-cloud strategy demands it.

## Summary

AWS is the dominant cloud platform for AI Infra, offering the broadest set of managed services and the deepest GPU instance portfolio. For an AI Infra Manager, the highest-leverage areas are compute (GPU instance selection, Spot strategy, EFA for multi-node training), networking (VPC design, EFA placement groups, PrivateLink), and storage (S3 for datasets/artifacts, FSx for Lustre for high-throughput training data access). Understanding the EKS + Karpenter + IRSA + Spot stack is essential — this combination enables cost-efficient, secure, auto-scaling GPU clusters that are the de facto standard at most AI companies.

Cost and governance are the two managerial differentiators. Cloud spend at AI companies is dominated by GPU compute, and the difference between a mature Spot strategy with proper checkpointing vs naive On-Demand usage can be 50-70% savings. Governance at scale requires AWS Organizations with SCPs, tag policies, and centralized observability — without these, spend accountability and security posture degrade as teams proliferate. A good AI Infra Manager ties infrastructure decisions to unit economics (cost per training run, cost per inference request) rather than just uptime.

Security on AWS centers on IAM: IRSA replaces node-level credentials, least-privilege policies prevent blast radius, and KMS ensures data at rest is encrypted with auditable key access. Multi-account isolation (prod/dev/security) provides the strongest blast-radius containment. Infrastructure as Code (Terraform or CDK) is non-negotiable for reproducibility, drift detection, and enabling platform teams to move fast without breaking things.

**AWS vs GCP vs Private Cloud**: The choice is rarely binary. AWS wins on GPU variety, Spot infrastructure maturity, and ecosystem breadth (EKS + Karpenter + FSx Lustre is the gold standard for GPU clusters). GCP wins for JAX/TPU workloads — TPU pods offer unique scale-out for large language model training, and the GCS → BigQuery data pipeline is unmatched for ML analytics. Private cloud (on-prem K8s) wins on unit economics at sustained high GPU utilization (>1000 GPUs steady state), data residency requirements, and eliminating egress costs — but requires significant platform engineering investment to replace what cloud providers give for free. The mature pattern at large AI companies is hybrid: on-prem for baseline steady-state training, cloud burst (AWS Spot or GCP Spot VMs) for peak demand. Kubernetes as the common abstraction layer, with Terraform managing both, makes this achievable — but unified scheduling, observability, and IAM federation across environments add real complexity.

## Raw Material
<!-- No raw material — written from direct knowledge -->
