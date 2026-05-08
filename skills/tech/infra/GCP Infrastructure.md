---
title: GCP Infrastructure
category: tech/infra
tags: [gcp, gke, vpc, iam, gcs, bigtable, tpu, compute-engine, cloud, infrastructure-as-code, vertex-ai, anthos, multi-cloud]
status: in-progress
priority: high
last_updated: 2026-05-07
created_from_jd: ""
---

# GCP Infrastructure

## Knowledge Map
- 前置知识：cloud fundamentals (VPC, IAM, compute, storage), Linux networking, Kubernetes, Terraform
- 延伸话题：[[GKE]] vs EKS vs self-managed K8s, TPU v4/v5/v5e ecosystem (JAX, PyTorch/XLA), GPUDirect RDMA on A3/A3 Mega, Vertex AI vs SageMaker vs self-managed MLOps, GCS FUSE vs Filestore vs Lustre on-prem, Anthos/Google Distributed Cloud for hybrid, BigQuery ML analytics pipeline
- 管理关联：cloud cost management (committed use discounts vs Spot VMs), CapEx vs OpEx tradeoffs, vendor lock-in decisions, TPU pod capacity planning, hybrid cloud architecture with GCP as burst layer

## Core Concepts

### Compute

#### Compute Engine (GCE) Instance Families for AI
- **A3 Mega (H100 SXM5, 8x per node)**: GCP's top GPU SKU; GPUDirect RDMA over RoCEv2 (3200 Gbps); ideal for large-scale LLM training; pairs with GKE + DWS (Dynamic Workload Scheduler) for reservation management
- **A3 (H100 80GB, 8x per node)**: predecessor to A3 Mega; RDMA networking; still widely used for training and inference
- **A2 Ultra (A100 80GB, 8x)**: mature, broadly available; NVLink within node; 200Gbps inter-node; good for mid-scale training and inference
- **A2 (A100 40GB, 8x or 16x)**: most available A100 SKU; use A2 Ultra for large model training requiring 80GB VRAM
- **G2 (L4 GPU)**: inference-optimized; transformer engine acceleration; cost-effective for serving medium-sized models
- **N2/C2/C2D**: CPU-focused; high-memory variants (N2-highmem) good for feature engineering / preprocessing
- **TPU VMs**: access TPU pods via TPU nodes in GKE or standalone TPU VMs; v4/v5/v5e have different ICI (Inter-Chip Interconnect) bandwidth and pod sizes

#### Spot VMs and Preemptible VMs
- **Spot VMs**: GCP's equivalent of AWS Spot; up to 91% discount; **30-second warning** before eviction (vs AWS 2-min) — requires faster checkpoint cadence
- **Preemptible VMs**: legacy flavor; max 24-hr runtime; always preempted after 24hr; use Spot VMs instead for flexibility
- **Spot interruption handling**: shorter eviction notice demands NCCL job checkpoint intervals of <30s or use of async checkpoint libraries (e.g., Orbax for JAX, Torch Distributed Checkpoint for PyTorch); GKE node pool taints help avoid scheduling non-tolerant workloads on Spot nodes
- **Committed Use Discounts (CUDs)**: 1yr = ~37% discount, 3yr = ~55% discount; resource-based (specific instance type + region) or spend-based (more flexible); use for steady-state inference fleet; combine with Spot for training burst

#### GKE (Google Kubernetes Engine)
- **Standard mode**: you manage node pools; pay per node; full control over node config; use for GPU/TPU clusters where you need fine-grained control
- **Autopilot mode**: Google manages nodes; you pay per Pod resource request (CPU, memory, GPU); automatic scaling; less control but lower ops overhead; suited for mixed workloads where GPU jobs are not dominant
- **Node Auto Provisioner (NAP)**: GKE's equivalent of Karpenter — creates and deletes node pools on demand based on pending Pods; less feature-rich than Karpenter but integrated natively
- **DWS (Dynamic Workload Scheduler)**: schedules large GPU/TPU reservations using a "queued resource" model; essential for A3 Mega clusters where capacity must be reserved in advance; works with GKE and Batch
- **GKE multi-cluster**: Anthos Fleet for multi-cluster management, config sync across clusters, Gateway API for multi-cluster ingress

### Networking

- **Global VPC**: unlike AWS (regional VPCs), GCP VPCs are global — subnets are regional but the VPC spans regions natively; simplifies multi-region routing without Transit Gateway equivalents
- **Alias IP ranges**: pods in GKE get IP aliases from the node's subnet CIDR; cleaner than AWS ENI-per-pod model; higher pod density per node; avoids the ENI limit bottleneck that AWS has
- **GPUDirect RDMA (A3/A3 Mega)**: A3 nodes use RoCEv2-based RDMA with 8x100G or 8x400G NICs; requires specific GKE node pool configuration; NCCL uses GPU-Direct RDMA path automatically when configured; enables sub-microsecond GPU-to-GPU communication across nodes
- **Cloud Load Balancing**: global (anycast) vs regional; HTTP(S) Load Balancer (global Layer 7, anycast IP), Network Load Balancer (regional Layer 4), Internal Load Balancer (private); GKE integrates via Gateway API and BackendConfig CRDs
- **Cloud CDN**: integrated with HTTP(S) Load Balancer; edge caching for model artifacts, static assets; useful for inference endpoints serving many end users
- **VPC Peering vs Shared VPC**: VPC Peering = private connectivity between two VPCs (non-transitive); Shared VPC = host project owns the network, service projects borrow subnets — preferred for multi-project orgs as it centralizes network management
- **Cloud Interconnect**: dedicated (10/100Gbps) or partner interconnect for on-prem connectivity; lower latency and cost than VPN for sustained high-throughput; use for hybrid cloud data pipelines
- **Cloud Armor**: WAF and DDoS protection attached to HTTP(S) LB; rate limiting, IP allowlisting, OWASP rule sets; important for public-facing AI APIs
- **Private Google Access**: allows VMs in private subnets to reach Google APIs (GCS, BigQuery, Vertex) without public IP; equivalent to AWS VPC Gateway Endpoints for GCS; reduces NAT costs

### IAM & Security

- **GCP IAM model**: simpler mental model than AWS — bind `member` (who) to `role` (what) on `resource` (where); roles are collections of permissions; conditions support attribute-based access (e.g., time of day, resource tag)
- **Service Accounts**: the primary identity for workloads; avoid user-managed keys (long-lived secret); prefer Workload Identity which fedrates short-lived tokens
- **Workload Identity (GKE)**: K8s ServiceAccount → GCP Service Account via OIDC federation; pods get GCP credentials without storing keys anywhere; equivalent to AWS IRSA; enables per-namespace or per-team IAM isolation in GKE
- **Cloud KMS**: managed key management; CMEK (Customer-Managed Encryption Keys) for GCS, BigQuery, Persistent Disk; Cloud HSM for hardware-backed keys; audit via Cloud Audit Logs
- **Secret Manager**: stores secrets (API keys, DB passwords) with versioning, IAM-controlled access, audit logging; equivalent to AWS Secrets Manager; use in conjunction with External Secrets Operator in GKE
- **Identity-Aware Proxy (IAP)**: zero-trust access control for internal apps; protects GCE instances, GKE services, App Engine — no VPN needed; verifies Google identity before proxying; useful for internal ML tooling (Jupyter, monitoring dashboards)
- **VPC Service Controls**: defines security perimeters around GCP resources; prevents data exfiltration even if credentials are compromised; restricts which GCP APIs can be called from within/outside the perimeter; critical for regulated data (HIPAA, FedRAMP)
- **Cloud Audit Logs**: Admin Activity, Data Access, System Event, Policy Denied; use Cloud Logging with log sink to BigQuery for long-term retention and analysis; equivalent to AWS CloudTrail
- **Resource Hierarchy (Org → Folder → Project → Resource)**: IAM policies inherit down the hierarchy; use folders to group projects by team/environment; enforce guardrails at org level via Org Policies (equivalent to AWS SCPs)

### Storage

- **Google Cloud Storage (GCS)**: durable (11 9s), strongly consistent object store; storage classes — Standard (hot), Nearline (≥1 access/month), Coldline (≥1/quarter), Archive (≤1/year); use Lifecycle policies to auto-transition; GCS is the primary data lake for ML datasets, model artifacts, checkpoints
- **GCS FUSE**: mount GCS buckets as a POSIX filesystem on GCE/GKE; convenient but not high-performance — read throughput limited compared to local NVMe or Filestore; use for small random reads, not for high-throughput training data loading
- **Filestore**: managed NFS; Basic (SSD/HDD), Enterprise tier with multi-zone HA; max throughput ~16 GB/s (Enterprise HPC tier); simpler to use than FSx Lustre but lower throughput ceiling; good for shared datasets in moderate-scale training
- **Persistent Disk (pd-ssd, pd-extreme, pd-balanced)**: block storage; pd-extreme for high IOPS databases; multi-writer PD is limited (no concurrent writes unlike EFS); pd-ssd good for OS disks and single-writer workloads; Google's SSD latency is competitive with AWS gp3
- **Hyperdisk**: next-gen block storage; Hyperdisk Extreme for IOPS-intensive DBs; Hyperdisk Throughput for high-seq-throughput workloads (e.g., data preprocessing pipelines); decouples throughput/IOPS from capacity
- **GCS → BigQuery integration**: first-class; external tables in BigQuery point directly to GCS; BigQuery ML reads GCS data natively; this tight coupling is a key GCP advantage for ML analytics pipelines (no ETL needed for analytics on training data)
- **GCS Transfer Service**: scheduled, managed transfers from S3/Azure Blob/on-prem to GCS; useful when migrating datasets from AWS to GCP

### Databases

- **Cloud SQL**: managed PostgreSQL/MySQL/SQL Server; HA with regional replicas; point-in-time recovery; suitable for ML pipeline metadata stores, experiment tracking backends; Cloud SQL Auth Proxy for secure connection from GKE
- **Cloud Spanner**: globally distributed relational DB; strong consistency across regions; near-limitless scale; expensive but unique for truly global ML platforms that need SQL at massive scale; typical use: global feature store metadata, multi-region serving catalog
- **Bigtable**: wide-column NoSQL; sub-10ms latency at petabyte scale; ideal for high-throughput feature serving (online feature store), time-series data, recommendation system user profiles; HBase-compatible API
- **Firestore**: serverless document DB; strong consistency; good for small/medium metadata stores, user config, experiment metadata in ML platforms
- **Memorystore (Redis/Valkey/Memcached)**: managed in-memory cache; Redis Cluster mode for horizontal scale; use for feature caching, rate limiting, session state in inference serving

### TPU Ecosystem (GCP-Unique)

- **TPU generations**:
  - TPU v4: 275 TFLOPS (bf16), 32GB HBM per chip; pod sizes up to 4096 chips; ICI bandwidth 1.2 Tb/s; dominant for large-scale LLM pre-training in JAX
  - TPU v5p: ~460 TFLOPS (bf16), 95GB HBM per chip; higher ICI bandwidth; designed for largest frontier models
  - TPU v5e: ~197 TFLOPS (bf16), 16GB HBM per chip; inference and fine-tuning optimized; lower cost per chip; dense packing for serving
- **ICI (Inter-Chip Interconnect)**: custom high-speed mesh between TPU chips in a pod; unlike GPU clusters (which need external RDMA networking), TPU chips communicate via ICI which is internal to the pod; enables near-linear scaling within a pod
- **JAX first-class support**: JAX (Google's NumPy-based ML framework) is designed for TPU; XLA compiler optimizes for TPU SIMD; `pjit`/`jit` with device mesh for model and data parallelism; TPU's native sharding (GSPMDshardings) maps naturally to JAX's `jax.sharding`
- **PyTorch/XLA**: PyTorch workloads on TPU via XLA backend; functional but adds overhead and debugging complexity; JAX is strongly preferred for TPU-native work; expect 10-20% performance penalty vs native JAX for same workload
- **TPU vs GPU tradeoffs**:
  - TPU wins: large-scale pre-training on JAX models, batch-processing dominated workloads, when ICI all-reduce outperforms RDMA GPU clusters
  - GPU wins: PyTorch-native models (no XLA friction), inference serving (GPU ecosystem much richer), flexibility (CUDA ecosystem, RDMA works for any framework), varied batch sizes (TPU is static-shape-oriented)
- **Accessing TPUs**: TPU Node (legacy — TPU as a separate VM type in GKE), TPU v5+ via GKE Node Pools with `cloud.google.com/gke-tpu-accelerator` nodeSelector; use `TPUAdmissionWebhook` for automatic topology selection
- **TPU capacity**: TPU pods are reserved in advance via Quota + Cloud reservation; Spot TPUs exist but availability is limited; plan 6-8 weeks ahead for large pod reservations

### AI/ML Platform: Vertex AI

- **Vertex AI Training**: managed training jobs (Custom Training); supports GCE VMs, GKE clusters, or managed TPU/GPU VMs; integrates with Artifact Registry for containers; use for one-off training runs without managing infra
- **Vertex AI Pipelines**: managed KFP (Kubeflow Pipelines) and TFX; DAG-based ML pipeline orchestration; stores artifacts in GCS/Artifact Registry; connects to Vertex Experiments for tracking
- **Vertex AI Workbench**: managed Jupyter notebooks on GCE; can attach GPUs; supports BigQuery and GCS natively; for exploration and prototyping
- **Vertex AI Model Registry + Endpoints**: model artifact tracking + managed inference serving; auto-scaling with Dedicated or Shared Machine Resource endpoints; good for production serving of TensorFlow/scikit-learn/custom container models; can route traffic between model versions (canary deployments)
- **Vertex AI Feature Store**: managed online/offline feature store; online serving via Bigtable backend; offline via BigQuery; solves training-serving skew
- **Decision: Vertex AI vs self-managed**: Vertex reduces ops overhead for small-medium ML teams; self-managed (GKE + Kubeflow/Argo) gives more flexibility and lower cost at scale; many large companies run self-managed on GKE with GCS + BigQuery, using Vertex only for specific services (Feature Store, Model Registry)

### Observability & Cost

- **Cloud Monitoring**: GKE metrics (node, pod, container), custom metrics via Cloud Monitoring API or Prometheus (managed collection via Google Cloud Managed Prometheus — GMP); dashboards + alerting; equivalent to AWS CloudWatch
- **Google Cloud Managed Prometheus (GMP)**: collects Prometheus metrics at scale without managing Prometheus servers; recommended for GKE observability; integrates with Cloud Monitoring for dashboards and alerting; uses PromQL
- **Cloud Logging**: structured logs from GKE, GCE, App Engine; log-based metrics for alerting on error patterns; log sinks to GCS (archival), BigQuery (analytics), Pub/Sub (streaming to SIEM)
- **Cloud Trace**: distributed tracing (compatible with OpenTelemetry); latency breakdown for ML inference APIs; integrates with Cloud Monitoring
- **Cost management tools**:
  - **Billing Export to BigQuery**: stream all spend data to BigQuery; enables custom dashboards (Looker Studio), team-level chargebacks, anomaly detection; far more powerful than AWS Cost Explorer for custom analysis
  - **Cost allocation labels**: GCP equivalent of AWS cost tags; apply at project/resource level; `team`, `env`, `model`, `experiment` — enforce via Org Policy `constraints/gcp.resourceLocations` and label enforcement
  - **Recommender API**: right-sizing recommendations for GCE, GKE, Cloud SQL; uses ML on historical usage; apply Idle VM Recommender + VM Machine Type Recommender routinely
  - **Cloud Budgets + Alerts**: set spend budgets per project/folder/label; trigger Pub/Sub for automated remediation (e.g., auto-disable non-critical Spot VMs on budget breach)

### Infrastructure as Code

- **Terraform**: primary IaC tool for GCP; `google` provider; strong coverage of all GCP services; remote state in GCS + DynamoDB lock (or Terraform Cloud); use for multi-cloud orgs (same tool as AWS)
- **Cloud Deployment Manager**: GCP-native IaC (YAML/Jinja2/Python); less popular than Terraform; limited community; avoid for new projects
- **Pulumi**: imperative IaC (Python/Go/TypeScript); generates GCP resources via Pulumi GCP provider; good for teams that prefer real programming languages over HCL; niche but growing
- **Config Connector (KCC)**: manage GCP resources as Kubernetes CRDs; lets platform teams manage GCP infra via GitOps (ArgoCD/Flux); GCS bucket, IAM binding, etc. declared as K8s objects; powerful for GKE-centric orgs
- **Terraform best practices for GCP**: use Google Cloud Foundation Blueprint (https://cloud.google.com/architecture/security-foundations/blueprints) as baseline for org structure; separate state per environment (dev/staging/prod); use google_project_iam_binding vs google_project_iam_member carefully (binding is authoritative, overwrites)

## Key Questions

**Q: How does GCP VPC differ from AWS VPC, and what does that mean for a multi-region ML platform design?**
Answer framework: GCP VPC is global — one VPC spans all regions; subnets are regional but you don't need Transit Gateway for cross-region routing. For a multi-region ML platform: single VPC can span US, EU, Asia; global HTTP LB with anycast IP routes inference requests to nearest region; training jobs in each region access the same VPC natively. AWS requires Transit Gateway + inter-region peering for similar setup — more hops, higher latency, added cost. GCP's simpler global networking is a real operational advantage for globally distributed serving.

**Q: Explain how Workload Identity works in GKE and why it's important.**
Answer framework: Workload Identity federates K8s ServiceAccounts to GCP Service Accounts via OIDC. Pod running as K8s SA `team-a/trainer` → annotated with IAM SA `trainer@project.iam.gserviceaccount.com` → GKE OIDC provider issues a short-lived token → GCP APIs accept it as the IAM SA identity. No keys stored anywhere. Benefits: least privilege per team/namespace (each team's training pods access only their GCS prefix), automatic token rotation (no key rotation ops), full IAM audit trail in Cloud Audit Logs. Equivalent to IRSA on EKS — both are OIDC-based, same mental model.

**Q: Compare TPU pods vs GPU clusters for large-scale LLM pre-training. When would you choose each?**
Answer framework: TPU pods have ICI (internal high-speed mesh, ~1.2 Tb/s), which eliminates the need for external RDMA networking between chips — the pod is a single tightly-coupled unit. GPU clusters (A3 Mega, H100) use GPUDirect RDMA over RoCEv2 externally. Choose TPU when: workload is JAX-native (TPU is a first-class platform for JAX/XLA), you need to scale beyond a single H100 node (v4 pod = 4096 chips), batch sizes are large and static shapes work. Choose GPU when: PyTorch-native codebase (avoid XLA friction), inference serving (GPU ecosystem — vLLM, TensorRT, CUDA — is far richer), variable batch sizes (GPU handles dynamic shapes naturally), team lacks JAX expertise. Most frontier model labs use both: TPU for JAX-based pre-training, GPU for inference serving.

**Q: How would you design GCS access control for a 20-team ML platform where each team's data must be isolated?**
Answer framework: One GCS bucket per team (`gs://company-ml-team-a-data/`) OR single bucket with prefix isolation + IAM conditions. For true isolation: separate buckets per team, Workload Identity binding so team-a's pods only get `storage.objectAdmin` on `team-a` bucket. For cost/ops simplicity with shared bucket: use IAM conditions with `resource.name.startsWith("projects/_/buckets/ml-data/objects/team-a/")`. Either way: no shared service account keys, all access via Workload Identity, audit via Cloud Audit Logs with log export to BigQuery for per-team access reporting. Add VPC Service Controls perimeter to prevent exfiltration even if IAM is misconfigured.

**Q: A multi-node GPU training job on GKE (A3 Mega) is getting poor NCCL throughput. How do you debug?**
Answer framework: (1) Verify GPUDirect RDMA is enabled: node pool must have `--enable-gvnic` and `--accelerator=type=nvidia-h100-mega-80gb,count=8,gpu-driver-version=latest`; check for `gke-gpu-device-plugin` DaemonSet. (2) Check NCCL env vars: `NCCL_DEBUG=INFO` to see which transport NCCL chose (want `NET/Plugin IB` or `NET/RDMA`, not `P2P/Net`); `NCCL_ALGO`, `NCCL_PROTO` should be left to auto-tune first. (3) Verify all nodes are in the same zone (cross-zone RDMA doesn't work — A3 Mega requires placement in same zone for RoCEv2 fabric). (4) Check GKE node pool has `--placement-type=COMPACT` for A3 Mega (enables compact placement = low latency). (5) Run NCCL tests (`nccl-tests` all_reduce_perf) to baseline; compare to expected 3200 Gbps aggregate for A3 Mega. (6) Check pod network limits — gVNIC must be requested in Pod spec as resource `networking.gke.io/default-interface: eth0`.

**Q: How do you manage GCP costs for an AI team spending $3M/month on GPUs?**
Answer framework: (1) Instrument first — export billing to BigQuery, build Looker Studio dashboard by team/model/experiment label; (2) Committed Use Discounts for stable inference fleet (1yr CUDs for known baseline); (3) Spot VMs for training burst with checkpoint-resume (<30s checkpoint interval for 30s eviction window); (4) DWS (Dynamic Workload Scheduler) for efficient A3 Mega batch scheduling (avoids idle reserved GPUs); (5) Rightsizing — Recommender API for idle VMs, GKE VPA for pod CPU/memory; (6) G2 (L4) for inference where H100 is over-provisioned; (7) Budget alerts with Pub/Sub integration to auto-pause non-urgent jobs on budget breach; (8) FinOps culture — engineers see their team's spend in weekly report from BigQuery.

**Q: Compare GCS vs S3 for ML workloads. What are the key differences?**
Answer framework: Functionally similar — both are durable, strongly consistent object stores. Key GCP advantages: (1) GCS → BigQuery native integration (no ETL for analytics on training data), (2) Multi-regional bucket option (data automatically geo-redundant, single endpoint); (3) GCS signed URLs and IAM Conditions are slightly simpler. Key GCP disadvantages: (1) Parallel filesystem — AWS FSx for Lustre (S3-backed, up to 1 TB/s) has no GCP equivalent; Filestore max throughput is 16 GB/s at Enterprise HPC tier, and GCS FUSE is not high-performance; (2) S3 has broader third-party ecosystem integration. Practical guidance: for ML data access where you need high-throughput random reads, avoid GCS FUSE; use BigQuery-managed storage or copy data to local SSD on training nodes; GCS is best used for checkpoints, artifacts, and dataset staging.

**Q: How does GKE's autoscaling compare to EKS + Karpenter?**
Answer framework: GKE Node Auto Provisioner (NAP) is functionally similar to Karpenter — both create/delete node pools on demand. Karpenter is more mature and configurable: fine-grained bin-packing, rich NodePool API, faster consolidation. NAP is simpler operationally (built-in, no separate deployment). GKE Autopilot charges per-pod-resource (not per-node), which can be cheaper for spiky CPU/memory workloads but doesn't support GPU. For GPU clusters, GKE Standard + NAP is the pattern; combine with DWS for large reserved GPU batches. Key difference: Karpenter can diversify across many instance types simultaneously (better Spot availability); NAP is more constrained to configured node pool templates. Bottom line: EKS + Karpenter has the edge for complex GPU Spot strategies; GKE + NAP is simpler to operate for teams that want less K8s tuning.

**Q: What is VPC Service Controls and when would you use it?**
Answer framework: VPC Service Controls creates a security perimeter around GCP resources (GCS buckets, BigQuery datasets, etc.) that restricts access to only from within the perimeter (specific VPCs, specific service accounts, specific geographic regions). Even if an attacker steals a service account key, they cannot exfiltrate data outside the perimeter. Use cases: (1) Regulated data (HIPAA, FedRAMP, PCI) where data must not leave defined boundaries; (2) Insider threat mitigation — even privileged engineers can't access production data from personal laptops; (3) Multi-tenant ML platforms where team data isolation must be enforced at network layer, not just IAM. Trade-off: adds operational complexity — every service-to-service call must be from within the perimeter; debugging access denials requires reading VPC SC audit logs; initial setup is error-prone. Recommendation: enable for production data and training datasets, not for dev/sandbox environments.

**Q: How do you run a hybrid architecture with GCP as burst layer and on-prem as baseline?**
Answer framework: Common pattern — on-prem GPU cluster handles steady-state training (CapEx amortized); GCP Spot VMs / TPU pods handle burst demand. Components: (1) Unified job scheduler — Volcano or Armada spans both; submits to on-prem K8s or GKE based on queue depth and availability; (2) Data plane — training datasets on on-prem NFS/Lustre; GCS mirrors critical datasets for cloud jobs (reduce egress); (3) Container registry — Artifact Registry in GCP, mirrored to on-prem Harbor; (4) Network connectivity — Cloud Interconnect (dedicated) for sustained high-throughput sync; Cloud VPN for control-plane traffic; (5) Observability — Prometheus federation with GMP as central aggregator; Cloud Monitoring dashboards cover both. Key challenges: data egress from on-prem to GCP can be expensive (budget $0.05-$0.08/GB for Interconnect egress); keep datasets on-prem and only move model checkpoints/artifacts to GCS post-training.

**Q: Explain the GCP resource hierarchy and how it maps to a multi-team AI platform.**
Answer framework: Org → Folder → Project → Resource. For an AI platform: Org root (company.com) → Folders: `ai-platform` (for ML infra) and `product` (for product teams). Under `ai-platform` folder: Project `ml-platform-prod` (shared infra: GKE clusters, shared GCS), `ml-platform-dev`, `ml-data-lake` (BigQuery + GCS for datasets). Per-team sub-folders under `ai-platform` for strong billing isolation. IAM policies at folder level propagate down; Org Policies at org level enforce guardrails (allowed regions, require labels, restrict public IPs). This hierarchy enables: per-project billing isolation, per-team Workload Identity namespacing, Org-level audit via Cloud Audit Logs aggregation, and SCPs-equivalent guardrails via Org Policies.

**Q: How do you choose between Cloud SQL, Spanner, Bigtable, and Firestore for an ML platform?**
Answer framework: Decision tree by access pattern and scale:
- **Cloud SQL (PostgreSQL)**: experiment metadata, pipeline run logs, model registry — relational queries, moderate scale, SQL joins needed
- **Spanner**: global ML serving catalogs, multi-region feature metadata that needs SQL + strong global consistency; expensive, use only when global consistency at SQL scale is truly needed
- **Bigtable**: online feature serving (high-throughput key lookups, sub-10ms), time-series telemetry from models, recommendation serving — massive scale, simple key-value/column-family access
- **Firestore**: lighter metadata (user configs, A/B test assignments, small experiment catalogs) — serverless, simpler ops, real-time listeners; moderate scale
- Typical ML platform: Cloud SQL for experiment tracking + MLflow backend, Bigtable for online feature store, GCS for offline feature store, Firestore for user-facing config

## Summary

GCP is the strongest choice for organizations with JAX-native ML workloads, tight Google ecosystem integration (BigQuery, Looker, Vertex AI), or need for TPU-based large-scale pre-training. GCP's global VPC simplifies multi-region architecture, and the BigQuery → GCS → Vertex AI data pipeline is uniquely seamless for ML analytics. For teams running PyTorch-heavy inference serving, AWS has a richer CUDA ecosystem (vLLM, TensorRT, SageMaker) and more mature Spot infrastructure.

**Key GCP strengths for AI Infra managers**:
1. **TPU ecosystem**: unmatched for JAX-native large-scale pre-training; ICI eliminates external RDMA complexity at pod scale
2. **Global VPC**: simpler multi-region networking vs AWS Transit Gateway model; one VPC spans regions
3. **BigQuery + GCS integration**: ML analytics pipeline (training data → BigQuery analytics → GCS feature storage) is native, no ETL
4. **GKE operational maturity**: GKE Autopilot and managed upgrades reduce K8s ops burden; built-in Prometheus (GMP) for observability
5. **Workload Identity**: same OIDC pattern as IRSA but slightly simpler binding model; Workload Identity Federation extends to non-GKE workloads

**Key GCP weaknesses to know**:
1. **No FSx Lustre equivalent**: GCS FUSE is not high-performance; Filestore maxes at 16 GB/s; for training at scale, must use local NVMe or copy data to boot disk — ops friction
2. **Spot VM 30-second warning**: vs AWS 2-minute Spot warning; much harder to checkpoint gracefully; requires aggressive checkpoint cadence or async checkpointing library
3. **PyTorch/XLA overhead**: running PyTorch on TPU adds compilation overhead and debugging friction; GPU is better for PyTorch-native workloads
4. **TPU capacity planning**: TPU pod reservations require 6-8 weeks lead time; less elastic than GPU Spot; limits agility for unplanned large training runs
5. **Smaller ecosystem**: fewer third-party SaaS integrations native to GCP vs AWS; teams may need extra connectors

**Security posture on GCP**: Workload Identity replaces service account keys for all GKE workloads; VPC Service Controls provides network-layer data perimeter enforcement on top of IAM; Cloud Audit Logs feed into BigQuery for compliance reporting; Org Policies enforce guardrails at org level (equivalent to AWS SCPs). The combination of WI + VPC SC + Cloud Audit Logs is the GCP security baseline for regulated ML platforms.

**Cost management levers**: Billing export → BigQuery is the most powerful cost analysis tool in any cloud — use it to build per-team, per-model, per-experiment cost dashboards. Committed Use Discounts for stable baseline (inference fleet), Spot VMs for training burst with proper checkpointing, DWS for efficient large GPU reservation scheduling, and L4 (G2) for cost-effective inference where H100 capacity is over-provisioned.

## Raw Material
<!-- No raw material — written from direct knowledge and AWS Infrastructure skill cross-reference -->
