---
title: GPU Cluster Management
category: tech/ai-infra
tags: [gpu, cluster, nvidia, cuda, distributed-training]
status: in-progress
priority: high
last_updated: 2026-04-08
created_from_jd:
---

# GPU Cluster Management

## Knowledge Map
- Prerequisites（前置知识）：[[Linux Basics]], [[Networking Fundamentals]]
- Related Topics（延伸话题）：[[NCCL Collective Communication]], [[RDMA and InfiniBand]], [[Kubernetes GPU Scheduling]], [[Slurm Workload Manager]], [[MIG Multi-Instance GPU]], [[DCGM GPU Monitoring]], [[Infrastructure as Code]], [[Clos Network Topology]], [[BMC and Redfish API]]
- Management（管理关联）：[[Capacity Planning]]

## Core Concepts

- **What it is**: Orchestrating, monitoring, and optimizing distributed GPU resources for AI training, inference, and HPC — covering provisioning, job scheduling, utilization, and failure recovery.
- **Resource scheduling**: Slurm (traditional HPC) and Kubernetes (cloud-native) are the two dominant workload managers; they handle job queuing, resource allocation, and priority/preemption.
- **Monitoring stack**: NVIDIA DCGM (Data Center GPU Manager) tracks SM utilization, memory bandwidth, temperature, and power; often paired with Prometheus + Grafana for dashboards.
- **MIG (Multi-Instance GPU)**: Partitions a single physical GPU (e.g., A100) into up to 7 isolated slices, each with dedicated compute and memory — maximizes utilization for smaller inference workloads.
- **Interconnects matter**: Intra-node uses NVLink (high-bandwidth GPU-to-GPU); inter-node uses InfiniBand (low-latency RDMA) or high-speed Ethernet — the choice directly impacts all-reduce collective performance.
- **Multi-node training init**: Three common methods to bootstrap NCCL across nodes — (1) OpenMPI rank exchange, (2) shared filesystem rendezvous, (3) TCP socket handshake. Slurm-based clusters often use FS or TCP when PMIx is unavailable.
- **Utilization target vs reality**: Well-managed clusters run at 85–95% GPU utilization; poorly managed clusters waste 40–60% of resources due to idle queuing, resource fragmentation, and bad job packing.
- **Job lifecycle management**: Automated checkpointing, preemption, and failure recovery are essential — training jobs run for hours to weeks and must survive node failures without restarting from scratch.
- **Common platforms**: NVIDIA Base Command Manager (end-to-end HPC cluster mgmt), Kubernetes + DCGM-Exporter (cloud-native), Slurm (traditional HPC), GPUStack (open-source inference-focused).
- **Build considerations**: GPU selection (H100 for training, L4 for inference), NVMe SSDs for high-throughput data loading, network bandwidth (≥25GbE per node minimum, InfiniBand preferred for large-scale training).

**10K+ GPU scale — qualitative shifts:**
- **Scale threshold**: At ~10K GPUs, management becomes "industrial manufacturing" — 1% efficiency gain saves millions, 5 min downtime > many companies' annual revenue. Manual processes become impossible (30 min/GPU manual deploy = 5,000 person-hours for 10K GPUs).
- **NVIDIA NGC monitoring platform**: New cluster-level software aggregates telemetry from open-source client agents deployed by customers to a unified dashboard on NGC. Monitors power (including transient spikes), SM utilization, memory bandwidth, interconnect health, and thermal conditions. Positioned as observation-only — no remote kill switch. Complements DCGM (node-level raw data) + Base Command (workflow orchestration) to form a three-tier management stack.
- **NVIDIA tool stack layers**: DCGM = node-level health probing (raw, operator assembles own dashboards); Base Command = job/dataset/workflow orchestration; NGC Cluster Monitor = cluster-level geographic visualization integrating the other two.
- **Power law failure distribution**: Google found 1% of GPUs cause 50% of job failures — at scale, targeted predictive maintenance outperforms blanket redundancy. Track per-GPU error history (50 attributes per GPU, refreshed every 30 sec).
- **Firmware management risk**: NVIDIA releases monthly GPU firmware updates; version mismatch between GPUs on the same job causes mysterious failures. Requires staged rollout with version control and automated drift detection. Anthropic enforces strict firmware version pinning.
- **Monitoring data volume at scale**: Each GPU generates 10,000+ metrics/sec → 10K GPUs = 100M metrics/sec = 8.6T data points/day. Traditional tools (Nagios, Zabbix) collapse; require time-series DBs (Prometheus, InfluxDB) with hierarchical aggregation (rack → row → cluster). ML-based anomaly detection (e.g., Amazon Random Cut Forest) required — target <0.01% false positive rate to avoid alert fatigue.
- **Cascade refresh strategy**: Use new-generation GPUs (H100/B200) for training workloads, prior-gen for inference — maximizes TCO while keeping training on latest hardware. H100 unit cost $25K–$40K; 3–4 year optimal TCO window unless 3x+ gen-over-gen improvement justifies early refresh.
- **Network at 10K scale**: 10K × 400 Gbps = 4 Pb/s total bandwidth. Use Clos topology (fat-tree) for consistent any-to-any latency; Dragonfly for ultra-large scale. InfiniBand costs 2x vs Ethernet but provides lower latency and better all-reduce performance; RoCE bridges gap but requires careful flow configuration. Hyperscaler rule of thumb: IB for training clusters, Ethernet for inference.
- **Deployment automation**: IaC is mandatory (not optional) — Meta manages GPU infra with 2M lines of Terraform. Zero-touch provisioning via BMC automation + Redfish API; Amazon GPU trays arrive and auto-provision without human touch. Immutable image-based deployment eliminates configuration drift.

## Key Questions

**Q: How would you approach improving GPU utilization from 60% to 85%+ across a training cluster?**
Answer framework: Diagnose root causes first (idle time from small jobs, resource fragmentation, long queues, bad scheduling policy). Then address: (1) bin-packing / gang scheduling to reduce fragmentation, (2) backfill scheduling to fill gaps with smaller jobs, (3) checkpointing + preemption to unblock stalled queues, (4) MIG partitioning for inference workloads that don't need a full GPU. Measure SM utilization and memory bandwidth, not just "GPU allocated" — allocation ≠ utilization.

**Q: Walk me through how multi-node distributed training is set up at the infrastructure level.**
Answer framework: Each node runs the training process; processes discover each other via a rendezvous mechanism (MPI/FS/TCP) to initialize NCCL. NCCL handles collective communication (all-reduce for gradient sync) over InfiniBand or NVLink. Slurm or K8s allocates nodes, sets env vars (RANK, WORLD_SIZE, MASTER_ADDR), and launches the job. Key failure point: any node drop kills the job → need checkpointing every N steps.

**Q: What metrics do you monitor for a GPU cluster in production, and what do they tell you?**
Answer framework: GPU SM utilization (compute efficiency), GPU memory bandwidth (data throughput), temperature + power (thermal throttling risk), job queue depth (scheduling pressure), job failure rate (hardware/software stability), inter-node bandwidth (networking bottleneck). DCGM exposes these; alert on sustained SM util < 70% (wasted capacity) or temps approaching 83°C (throttle risk).

**Q: How does MIG work and when would you use it?**
Answer framework: MIG partitions one physical GPU into isolated instances with dedicated SM partitions and HBM slices — strong isolation, no cross-instance interference. Use when: inference workloads are too small to fill a GPU, you need multi-tenant GPU sharing with SLA isolation, or you want to run multiple model variants in parallel. Trade-off: partitions are static (require reconfiguration to resize), so it's inflexible for mixed training + inference on the same node.

**Q: What are the trade-offs between Slurm and Kubernetes for GPU cluster management?**
Answer framework: Slurm is purpose-built for HPC batch jobs — excellent at gang scheduling, backfill, and tight MPI integration; poor at containerization and cloud-native workflows. Kubernetes is container-first — great for heterogeneous workloads, service-style inference, CI/CD pipelines; adds overhead for pure batch training (scheduler is not HPC-optimized). Many large clusters run both: Slurm for training, K8s for serving.

**Q: How do you handle GPU node failures in a large training run?**
Answer framework: Preventive: checkpoint frequently (every 10-30 min depending on job length), use heartbeat-based health checks to detect hangs vs crashes. Reactive: Slurm/K8s detects node failure, job is requeued or restarted from last checkpoint. At scale: have spare nodes in "warm standby" to replace failed nodes without full job restart. DCGM alerts on hardware errors (ECC errors, Xid codes) before hard failure.

**Q: How do interconnect choices affect training throughput at scale?**
Answer framework: All-reduce communication volume grows with model size and number of nodes. InfiniBand (HDR/NDR, 200-400 Gb/s) with RDMA bypasses CPU, enabling near-wire-speed collective communication — essential for large model training. High-speed Ethernet (RoCE) can approximate IB performance but requires careful ECMP/flow configuration. NVLink (intra-node) is ~10x faster than PCIe — use NVLink-connected GPU topology (NVSwitch in DGX) for tensor parallelism. Rule of thumb: communication should not exceed 10-15% of compute time for good scaling efficiency.

**Q: At 10,000 GPU scale, what breaks that works fine at 100 GPUs?**
Answer framework: Three categories of breakdown: (1) Operational — manual processes become infeasible (5,000+ person-hours just to deploy); IaC and zero-touch provisioning become mandatory, not optional. (2) Monitoring — raw metric volume (100M/sec) exceeds traditional monitoring tools; need time-series DBs, hierarchical aggregation, and ML-based anomaly detection. (3) Failure modes — power-law distribution of failures means 1% of GPUs cause 50% of job failures; firmware version drift across nodes causes cluster-level outages; thermal and network congestion patterns at scale have no analogue at small scale. Tesla's Dojo: 3 months to deploy 10K GPUs, 1 year to run efficiently.

**Q: What is NVIDIA's three-tier cluster management stack and where does each tool fit?**
Answer framework: DCGM (Data Center GPU Manager) is the node-level layer — collects raw GPU health metrics (SM utilization, memory bandwidth, temperature, ECC errors), but requires the operator to build dashboards and aggregation pipelines. Base Command Platform is the workflow layer — handles job scheduling, dataset management, and AI development workflows; does not do deep hardware monitoring. NGC Cluster Monitor (new) is the cluster-level visualization layer — aggregates telemetry from an open-source client agent into a unified dashboard, supports geographic fleet view and compliance tracking. The right answer shows understanding of which tool to reach for at which level of the stack.

**Q: How would you approach firmware management across a 10,000-GPU fleet?**
Answer framework: Version mismatch between GPUs on the same job is a silent failure mode — NVIDIA releases monthly updates, and running mixed firmware versions during a training job causes mysterious instability. Good approach: (1) pin firmware versions per cluster tier (training vs inference), (2) stage rollouts with canary nodes before fleet-wide push, (3) automate drift detection to alert when any node deviates from target version, (4) test job reproducibility after each firmware update with a short benchmark run. Enforce via IaC — firmware version is part of the immutable node image.

**Q: Describe the economics of managing an H100 cluster at scale. What drives the ROI?**
Answer framework: H100s cost $25K–$40K each; a 10K-GPU cluster represents $250M–$400M in hardware. At this capital intensity, utilization directly translates to ROI — going from 70% to 85% utilization effectively recovers the equivalent of 1,500 GPUs of capacity. Key drivers: (1) scheduling efficiency (gang scheduling, backfill, bin-packing), (2) reducing job failure rate (each restart wastes GPU-hours), (3) cascade strategy (use new GPUs for training, prior-gen for inference to maximize $/FLOP across the fleet). H100→B200 offers ~3x perf improvement, which can justify early refresh if training bottleneck is compute-bound.

## Summary

GPU cluster management is the operational discipline of maximizing utilization, reliability, and throughput across pools of expensive GPU hardware used for AI training and inference. At its core, it involves three layers: (1) resource scheduling (Slurm, Kubernetes) to allocate GPUs to jobs efficiently, (2) monitoring (DCGM, Prometheus, Grafana) to observe real-time health and utilization, and (3) job lifecycle management (checkpointing, preemption, failure recovery) to keep long-running training jobs alive.

The critical insight separating good from poor cluster management is understanding the difference between GPU *allocation* and GPU *utilization*. A cluster can show 100% allocation while SM utilization sits at 40% — meaning jobs hold GPUs but aren't using them efficiently. Techniques like MIG partitioning, gang scheduling, backfill scheduling, and bin-packing address different root causes of low utilization. Target 85–95% SM utilization as a health benchmark; below 70% sustained warrants investigation.

Networking and storage are often overlooked bottlenecks. For large-scale distributed training, InfiniBand with RDMA is the standard — it enables NCCL's all-reduce collectives to run near wire speed, keeping gradient synchronization from becoming the bottleneck. NVMe SSDs with sufficient read bandwidth prevent data starvation during training. As clusters scale to hundreds or thousands of GPUs (as in frontier model training), the management surface grows dramatically — automated observability, health checking, and fast failure recovery become as important as raw compute.

At 10K+ GPU scale, the nature of the management problem changes qualitatively. Monitoring alone generates 100M+ metrics/second, requiring purpose-built time-series databases and ML-based anomaly detection (traditional threshold alerting creates alert fatigue at this scale). Deployment automation goes from best practice to hard requirement — Meta manages its GPU fleet with 2M lines of Terraform and zero-touch BMC provisioning. NVIDIA's emerging three-tier management stack reflects this complexity: DCGM for node-level probing, Base Command for workflow orchestration, and the new NGC Cluster Monitor for fleet-level geographic visualization. Power-law failure distribution (Google's finding: 1% of GPUs cause 50% of failures) means naive redundancy is wasteful — predictive maintenance driven by per-GPU telemetry history is the correct approach. The economics are similarly stark: H100s cost $25K–$40K each, making utilization optimization the highest-leverage lever — each percentage point of utilization recovered at 10K GPU scale is worth the equivalent of 100 GPUs.

## Raw Material
- [[raw_material/tech/ai-infra/GPU Cluster Management - resources]]
- [[raw_material/tech/ai-infra/英伟达全新AI GPU集群监控软件深度解析]]
