---
title: Cloud Computing Fundamentals
category: tech/infra
tags: [cloud, iaas, paas, saas, vm, auto-scaling, availability-zone, storage, cdn, elasticity]
status: draft
priority: medium
last_updated: 2026-04-07
created_from_jd:
---

# Cloud Computing Fundamentals

## Knowledge Map
- Prerequisites（前置知识）：[[Networking Fundamentals]], [[Linux Namespaces]]
- Related Topics（延伸话题）：[[Kubernetes]], [[Container Basics]], [[Hybrid Cloud Deployment]], [[Distributed Systems]]
- Management（管理关联）：[[Technical Roadmap]]

## Core Concepts

**Service Models**
- **IaaS** (Infrastructure as a Service): raw compute, storage, network; you manage OS upward (AWS EC2, Azure VMs); maximum control, maximum responsibility
- **PaaS** (Platform as a Service): deploy apps without managing OS/runtime (Heroku, Google App Engine); you manage app code only
- **SaaS** (Software as a Service): fully managed applications (Gmail, Salesforce); you manage data and access only
- More managed = less control, less operational burden; choose based on how much differentiation you get from managing lower layers

**Regions and Availability Zones**
- **Region**: geographic area (us-east-1, eu-west-1); data residency and latency-based selection
- **Availability Zone (AZ)**: isolated datacenter within a region with independent power, cooling, and networking
- Deploy across AZs for HA: one AZ failure doesn't take down the service; most managed services replicate across AZs automatically
- Multi-region: disaster recovery or global latency optimization; significantly increases operational complexity

**Compute**
- **Virtual Machine (VM)**: software-based computer on physical hardware via hypervisor; multiple VMs share one physical server; isolation at OS level
  - Type 1 (bare-metal hypervisor): runs directly on hardware — KVM, VMware ESXi, Xen; better performance; production use
  - Type 2 (hosted hypervisor): runs on host OS — VirtualBox, VMware Workstation; easier setup; dev/test use
- **Instance types**: General purpose (balanced CPU/memory — web servers), Compute optimized (high CPU — batch), Memory optimized (high RAM — in-memory DB), Storage optimized (high IOPS — data warehouses); profile workload bottleneck before choosing
- **CPU pinning & NUMA**: bind vCPUs to physical cores (reduce migration cost); allocate memory from same NUMA node as CPU (reduce remote memory access latency); for latency-sensitive workloads (databases, HPC)

**Auto-scaling and Elasticity**
- **Elasticity**: automatic scale up/down based on real-time demand (traffic spike → add instances, quiet → remove); reduces over-provisioning cost
- **Scalability**: ability to grow by adding resources (planned, manual, or automated)
- Elasticity implies scalability; scalability doesn't require elasticity
- Implementation: auto-scaling groups (AWS ASG), HPA in K8s; trigger on CPU, memory, or custom metrics

**Load Balancing**
- Distributes traffic across multiple backend instances; prevents single-server overload; provides failover when instances are unhealthy
- **L4 (TCP/UDP)**: routes based on IP and port; faster, less CPU overhead; used for raw throughput
- **L7 (HTTP/HTTPS)**: routes based on URL path, headers, cookies; supports content-based routing and TLS termination; more flexible
- Health checks remove unhealthy backends from rotation automatically

**Content Delivery Network (CDN)**
- Geographically distributed edge servers cache content closer to users → lower latency, reduced origin load, bandwidth savings
- **Edge caching**: static content (images, CSS, JS) cached at PoP (Point of Presence); TTL-based invalidation or purge API
- Dynamic content: CDN routes via optimized paths even when caching doesn't apply
- Use CloudFront / Cloudflare / Akamai for global user bases

**Storage Types**
| Type | Examples | Use Case | Access |
|---|---|---|---|
| Block | EBS, Persistent Disk | Databases, VMs | Single attachment, low latency |
| File | EFS, NFS | Shared filesystems, home dirs | Multi-attach, POSIX API |
| Object | S3, GCS Blob | Backups, static content, data lakes | HTTP API, unlimited scale |

- **Persistent vs Ephemeral**: persistent storage survives VM stop/restart (EBS); ephemeral tied to VM lifecycle, deleted on termination (instance store) — use for caches/temp files only
- **IOPS vs Throughput**: IOPS = small random I/O ops/sec (databases, transactional); Throughput = MB/s sequential (backups, streaming); storage tier choice depends on workload pattern
- **SSD vs HDD**: SSD (flash) faster random I/O; NVMe SSD (PCIe) lower latency than SATA SSD; HDD cheaper for cold/archival
- **Storage tiering**: hot (S3 Standard) → warm (S3 IA) → cold (Glacier) → archive (Deep Archive); lifecycle policies automate transitions

**High Availability (HA)**
- System remains operational during failures; target: 99.9%+ uptime
- Techniques: redundancy (multiple instances), load balancing + health checks, multi-AZ deployment, automated failover, auto-recovery
- HA ≠ disaster recovery (DR); HA handles component failures, DR handles regional failures

**Cloud Security Shared Responsibility Model**
- **Provider responsible**: physical security, hardware, network infrastructure, hypervisor
- **Customer responsible**: OS patching, application security, data encryption, access control, firewall rules
- More managed service = more provider responsibility; SaaS customer only manages data and user access

## Key Questions

**Q: Explain the difference between IaaS, PaaS, and SaaS. When would you choose each?**
Answer framework: IaaS for maximum control (custom OS, networking) — use when the infrastructure IS your product; PaaS for app deployment without infra management — use when infra is commodity; SaaS for fully managed tools. Key question: does managing the lower layers give you competitive advantage?
> 中文提示：越托管越少控制；基础设施是产品本身时选 IaaS，否则往上选

**Q: What is an Availability Zone? Why do we deploy across multiple AZs?**
Answer framework: AZ = isolated datacenter with independent power/network within a region; deploy across AZs so a single AZ failure (power, network, hardware) doesn't take down the service; most cloud managed services handle cross-AZ replication automatically; cost: cross-AZ data transfer fees.
> 中文提示：AZ 故障隔离是 HA 的基础；跨 AZ 数据传输有费用

**Q: What does auto-scaling mean? How is elasticity different from scalability?**
Answer framework: Auto-scaling automatically adjusts instance count based on real-time metrics (CPU, traffic); elasticity is the dynamic automatic version of scalability — scales both up AND down to minimize cost; static scalability just means you can add capacity when needed. Cloud value prop: pay for what you use.
> 中文提示：弹性 = 自动双向伸缩（既能扩也能缩）；可扩展性只是能扩不一定自动

**Q: Compare block storage, file storage, and object storage. When would you use each?**
Answer framework: Block = raw volume, single attachment, low latency for databases/VMs (EBS); File = shared POSIX filesystem, concurrent access, home directories (EFS/NFS); Object = HTTP API, unlimited scale, metadata-rich, for backups/static content/data lakes (S3). Choice driven by: latency requirements, sharing needs, scale.
> 中文提示：块存储给数据库（低延迟）；文件系统给共享目录；对象存储给海量数据（S3 语义）

**Q: What is the shared responsibility model in cloud security?**
Answer framework: Provider owns physical infrastructure up to the hypervisor; customer owns everything above — OS patching, app security, network config (security groups), access control, data encryption. More managed service = more provider responsibility. Common mistake: assuming the cloud provider handles data encryption automatically.
> 中文提示：IaaS 客户管 OS 以上；SaaS 客户只管数据和访问；数据加密默认不是 provider 的责任

**Q: What is a CDN and how does edge caching work?**
Answer framework: CDN distributes content to PoPs globally; static assets cached at edge with TTL; cache miss → fetches from origin, caches the response; cache invalidation via TTL expiry or manual purge API; dynamic content routed via optimized network paths without caching. Reduces latency (user hits nearest PoP), origin load, and bandwidth costs.
> 中文提示：静态资源在 edge 缓存；TTL 到期或手动 purge 失效；动态内容靠路由优化不靠缓存

**Q: What is the difference between horizontal and vertical scaling? When do you use each?**
Answer framework: Horizontal (scale out): add more instances — better for stateless apps, theoretically unlimited; Vertical (scale up): bigger instance — simpler but hardware limited, better for stateful apps or monoliths that can't be sharded. Modern cloud-native apps design for horizontal; legacy apps often require vertical.
> 中文提示：无状态应用水平扩展；有状态或单体应用垂直扩展；K8s HPA 是水平，VPA 是垂直

## Summary

Cloud computing fundamentals underpin every infrastructure engineering conversation. The three core mental models: (1) **Shared responsibility** — know exactly where the cloud provider's responsibility ends and yours begins; (2) **AZ-based HA** — deploy across AZs by default, not as an afterthought; (3) **Right storage for the job** — block for databases, object for scale, file for sharing. Elasticity (automatic bidirectional scaling) is the core economic value proposition of cloud — it enables paying for actual usage rather than peak provisioning. CDNs extend the same principle to content delivery: push compute (caching) to where users are rather than routing all requests to a single origin.

> 面试重点：shared responsibility 模型高频考；AZ 是 HA 的基本单元；存储三类型及选择标准；弹性 vs 可扩展性的区别

## Raw Material
- [[raw_material/questions.md]]
