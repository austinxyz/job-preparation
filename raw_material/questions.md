# Infrastructure Engineering Question Library

**Authors:** [Kire Filipovski](mailto:kfilipov@ebay.com), [Sharad Murthy](mailto:shmurthy@ebay.com), [Austin Xu](mailto:yanzxu@ebay.com)
**Last Updated:** January 11, 2026

---

## Overview

This library provides a comprehensive collection of interview questions organized by focus area for Infrastructure Engineering roles. Questions are categorized by career level (Early, Mid, Peak) and include expected answer traits to help interviewers assess candidates consistently.

**For interview process and stage guidance, see:** [Infrastructure Engineering Interview Process](./Infrastructure-Engineering-Interview-Process.md)

---

## How to Use This Library

### Question Selection
- Select 2-3 questions per focus area based on your assigned interview stage
- Match question career level to candidate's experience level
- Avoid duplicating questions across panel members

### Evaluation
- Use "Expected Answer" as guidance, not a strict rubric
- Probe for depth with follow-up questions
- Note specific examples and demonstrations
- Look for STAR method (Situation, Task, Action, Result) in behavioral answers

### Career Level Guidelines
- **Early** (0-3 years): Foundational knowledge, willingness to learn
- **Mid** (3-7 years): Hands-on experience, problem-solving, some leadership
- **Peak** (7+ years): Deep expertise, system-level thinking, thought leadership

---

## Table of Contents

### Quick Screening (Phone Screen Only)
- [Quick Screening Questions](#quick-screening-questions)

### Behavioral & Soft Skills
- [Team Fit/Behavioral Questions](#team-fitbehavioral-questions)
- [Collaboration](#collaboration)
- [Communication](#communication)
- [Adaptability](#adaptability)
- [Conflict Resolution](#conflict-resolution)
- [Values Alignment](#values-alignment)
- [Customer Centricity](#customer-centricity)

### Technical Depth
- [Cloud Knowledge Questions](#cloud-knowledge-questions)
- [Linux Kernel & OS Internals](#linux-kernel--os-internals)
- [Kernel Engineering](#kernel-engineering)
- [Containerization & Kubernetes](#containerization--kubernetes)
- [Containerization & Runtimes](#containerization--runtimes)
- [Networking & Security](#networking--security)
- [BPF & Networking](#bpf--networking)

### System Design & Architecture
- [System Design Questions](#system-design-questions)
- [Systems Design & Architecture](#systems-design--architecture)

### Programming & Development
- [Coding Questions](#coding-questions)
- [Programming Proficiency](#programming-proficiency)
- [Programming & Tooling](#programming--tooling)
- [Software Development Questions](#software-development-questions)

### Operations & Reliability
- [Observability & Diagnostics](#observability--diagnostics)
- [Observability](#observability)
- [Debugging & Troubleshooting](#debugging--troubleshooting)
- [Troubleshooting](#troubleshooting)
- [Incident Response](#incident-response)
- [Operational Excellence](#operational-excellence)

### Security & Compliance
- [Security Engineering](#security-engineering)
- [Security & Compliance Awareness](#security--compliance-awareness)

### Other
- [Automation & Tooling](#automation--tooling)
- [Continuous Learning](#continuous-learning)
- [Open Source Contributions](#open-source-contributions)
- [Strategy](#strategy)
- [Vision](#vision)
- [Other](#other)

---

## Quick Screening Questions

**Purpose:** Rapid initial assessment (5 minutes total) at the start of phone screens to validate basic technical competency and communication skills before diving into detailed questions. These are intentionally VERY EASY to quickly identify red flags (resume inflation, communication issues).

**When to Use:** ONLY at the beginning of phone screen interviews (NOT for technical rounds or on-site)

**Format:** Conversational, warm-up tone, NOT interrogative

---

### Current Role Overview

**Q: Walk me through your current role and what you work on day-to-day.**
- **Level:** All Levels
- **Expected Answer:** Clear description of responsibilities, technologies used, team structure, typical tasks. Shows ability to communicate technical work to non-experts.
- **Red Flags:** Cannot articulate basic job responsibilities, vague answers, defensive tone
- **Time:** 2-3 minutes

---

### Technology Familiarity (Resume-Based)

**Select ONE question based on most prominent technology on resume:**

**Q: You mentioned [Kubernetes/Docker/AWS/Python/etc.] on your resume - can you briefly explain what problem it solves and why you use it in your work?**
- **Level:** All Levels
- **Expected Answer:** Simple, clear explanation of the technology's purpose and their use case. Not looking for deep technical details - just validation they actually use it.
- **Example Good Answer (K8s):** "Kubernetes helps us manage containerized applications at scale. We use it to deploy and run our microservices across multiple servers, and it handles things like scaling, health checks, and rolling updates automatically."
- **Example Good Answer (Python):** "I use Python for automation scripts and infrastructure tooling because it's readable, has great libraries for cloud APIs, and our team is familiar with it."
- **Red Flags:** Cannot explain what the technology does, overly complex jargon-heavy answer (trying to compensate), admits they haven't actually used it
- **Time:** 2-3 minutes

---

### Basic Technical Concept (Resume-Based)

**Alternative warm-up question if candidate struggles with technology familiarity:**

**Q: Tell me about the most recent technical problem you solved at work. What was the issue and how did you fix it?**
- **Level:** All Levels
- **Expected Answer:** Concrete recent example with clear problem statement and solution. Shows problem-solving approach and ability to explain technical work.
- **Red Flags:** Cannot recall any recent work, extremely vague ("I fixed some bugs"), over-complicated explanation of trivial issue
- **Time:** 2-3 minutes

---

**Interviewer Note:** If candidate struggles significantly with these basic questions (cannot explain their role, cannot describe technologies they claim expertise in, poor communication), this is a strong signal to either:
1. Keep remaining questions at the easiest difficulty level, OR
2. Conclude the interview early (after 15-20 minutes) to respect everyone's time

---

## Team Fit/Behavioral Questions

### Customer Focus

**Q: Describe a time when you didn't have all the information to understand the exact nature of a user's issue when developing a feature. How did that affect how you developed the feature? What steps (if any) did you take to understand the user's problem better?**
- **Level:** Early to Peak
- **Expected Answer:** Demonstrates fast learning, seeking help/resources, applying knowledge to deliver results.

### Composure

**Q: Tell me about a time when someone pushed you to the limit. What was it about their behavior that pushed you too far? How did you react? What would you have done differently?**
- **Level:** Mid to Peak
- **Expected Answer:** Shows emotional intelligence, self-control, reflection, and constructive conflict resolution.

### Interpersonal Savvy

**Q: Describe a recent unpopular decision you made and what the result was.**
- **Level:** Mid to Peak
- **Expected Answer:** Demonstrates courage, ability to stand by decisions, stakeholder management, and learning from outcomes.

**Q: Describe when you made an extra effort to build strong relationships with others inside or outside the organization. What difficulties did you face and how did you overcome them?**
- **Level:** Mid to Peak
- **Expected Answer:** Shows networking skills, persistence, empathy, and relationship-building strategies.

### Action Oriented

**Q: Sometimes people delay taking action on something. Describe a time when you saw other people in the organization who were not acting and you took it upon yourself to lead the effort.**
- **Level:** Mid to Peak
- **Expected Answer:** Demonstrates initiative, leadership, accountability, and driving outcomes.

### Flexibility (Dealing with Paradox, Adaptability)

**Q: When you have difficulty persuading someone to your point of view, what do you do? Give an example.**
- **Level:** Mid
- **Expected Answer:** Shows adaptability, empathy, multiple persuasion strategies, and willingness to compromise.

**Q: What do you do when you are faced with an obstacle to an important project? Give an example.**
- **Level:** Mid
- **Expected Answer:** Demonstrates problem-solving, creativity, resilience, and finding alternative paths.

### Taking Direction/Mentoring Others

**Q: (Junior Level) Share a time when it was critical that you follow clear instructions, direction, or vision with an individual or group. What was the situation and with whom were you communicating? How did you ensure that you received clear guidance in order to complete your task?**
- **Level:** Early
- **Expected Answer:** Shows ability to seek clarification, active listening, and executing on clear direction.

**Q: (Senior Level) Share a time when it was critical that you provide clear instructions, direction, or vision to an individual or group. What was the situation and to whom were you communicating? How did you ensure that your communications were clear and understood by the individual or group?**
- **Level:** Mid to Peak
- **Expected Answer:** Demonstrates leadership, clear communication, checking for understanding, and ensuring alignment.

### Organizational Savvy

**Q: Tell me about a team or work situation with diverse stakeholders (e.g., across orgs, different roles). How did you navigate through it? What steps did you take to ensure the team was able to act effectively?**
- **Level:** Mid to Peak
- **Expected Answer:** Shows political awareness, stakeholder management, alignment strategies, and effective collaboration.

---

## Collaboration

**Q: Tell me about a time when team priorities conflicted with another team's. How did you resolve it?**
- **Level:** Mid
- **Expected Answer:** Shows empathy, proactive communication, compromise, alignment on goals.

**Q: You're working with a team unfamiliar with Kubernetes. How do you help them adopt best practices?**
- **Level:** Mid
- **Expected Answer:** Mentions mentorship, documentation, pairing sessions, gradual onboarding.

**Q: How do you give and receive feedback in a high-performing team?**
- **Level:** Early to Mid
- **Expected Answer:** Shows openness, tact, specific feedback examples, continuous improvement mindset.

**Q: Tell me about a time when you had to convince another team to adopt a more secure design despite pushback.**
- **Level:** Mid
- **Expected Answer:** Shows influence, empathy, data-driven persuasion, working through priorities, negotiation, and outcome.

**Q: Tell me about a time you collaborated with infra and app teams to roll out a kernel or OS upgrade. What went well or wrong?**
- **Level:** Mid
- **Expected Answer:** Highlights testing rigor, cross-functional alignment, blast radius control, documentation, and customer empathy.

**Q: Describe a time when you had to work with a cross-functional team to achieve a goal. What was your role and the outcome?**
- **Level:** Mid
- **Expected Answer:** Highlights teamwork, adaptability, and the ability to align different perspectives towards a common objective.

**Q: How do you handle conflicts within a team? Provide an example.**
- **Level:** Mid
- **Expected Answer:** Shows conflict resolution skills, active listening, and a focus on team cohesion.

**Q: Tell me about a time when you mentored a colleague. How did you approach it?**
- **Level:** Mid
- **Expected Answer:** Discusses guidance, knowledge sharing, and fostering growth in others.

**Q: How do you ensure your communication is effective when working on deeply technical problems with cross-functional teams?**
- **Level:** Mid
- **Expected Answer:** Discusses use of diagrams, async comms, documenting assumptions, shared terminology.

---

## Communication

**Q: How do you explain the importance of mTLS to a team unfamiliar with security protocols?**
- **Level:** Early to Mid
- **Expected Answer:** Uses simple analogies, explains authentication/authorization concepts clearly.

**Q: A new edge security policy may degrade UX. How do you communicate and gain alignment with stakeholders?**
- **Level:** Mid
- **Expected Answer:** Balances technical and business priorities, gathers feedback, presents clear impact/risk analysis.

**Q: Describe a time you had to convey complex technical tradeoffs to a non-engineering audience.**
- **Level:** Mid
- **Expected Answer:** Describes use of visual aids, clear language, and ability to address concerns.

**Q: How do you explain complex technical concepts to non-technical stakeholders?**
- **Level:** Early to Mid
- **Expected Answer:** Uses analogies, visual aids, and clear language to bridge the technical gap.

**Q: Describe a situation where you had to convey bad news to a team or stakeholder. How did you handle it?**
- **Level:** Mid
- **Expected Answer:** Shows transparency, empathy, and a focus on solutions while maintaining trust.

**Q: Can you provide an example of how you documented a technical process or system?**
- **Level:** Mid
- **Expected Answer:** Emphasizes clarity, structure, and accessibility of documentation for diverse audiences.

---

## Adaptability

**Q: Describe a time when you had to learn a new technology quickly to complete a project.**
- **Level:** Early to Mid
- **Expected Answer:** Demonstrates fast learning, seeking help/resources, applying knowledge to deliver results.

---

## Conflict Resolution

**Q: How do you handle disagreements on technical decisions with team members?**
- **Level:** Mid
- **Expected Answer:** Emphasizes listening, data-driven arguments, and openness to alternate perspectives.

---

## Values Alignment

**Q: Describe a time you stood up for a secure design even when it slowed development.**
- **Level:** Mid
- **Expected Answer:** Demonstrates integrity, advocacy for quality/security, clear reasoning.

**Q: How do you contribute to a culture of inclusion in engineering teams?**
- **Level:** All Levels
- **Expected Answer:** Mentions listening, valuing diverse perspectives, inclusive code reviews, documentation practices.

**Q: Why do you want to work at eBay, and how do you align with our mission and values?**
- **Level:** Early to Peak
- **Expected Answer:** Shows understanding of eBay's mission, demonstrates passion, and aligns personal values with the company's.

**Q: Describe a time when you had to make a decision that aligned with company values over personal convenience.**
- **Level:** Mid to Peak
- **Expected Answer:** Highlights integrity, ethical decision-making, and commitment to organizational principles.

**Q: How do you contribute to fostering an inclusive and diverse work environment?**
- **Level:** Early to Peak
- **Expected Answer:** Discusses actions taken to promote diversity, equity, and inclusion within teams.

**Q: What do you value most in a team culture, and how do you contribute to it?**
- **Level:** Early to Mid
- **Expected Answer:** Mentions psychological safety, collaboration, helping others succeed, open dialogue.

---

## Customer Centricity

**Q: How would you modify an edge service to meet latency SLAs in underserved markets?**
- **Level:** Mid to Peak
- **Expected Answer:** Explores PoP placement, caching, compression, region-specific configs.

**Q: When building a certificate management system, how do you ensure reliability for internal developers?**
- **Level:** Mid
- **Expected Answer:** Discusses intuitive APIs, uptime guarantees, self-service, alerts, and support processes.

**Q: Tell me about a time when you discovered a security fix was impacting end-user experience. What did you do?**
- **Level:** Mid
- **Expected Answer:** Describes mitigation, stakeholder communication, redesign for balance.

**Q: Describe a time when you identified a customer pain point and implemented a solution. What was the impact?**
- **Level:** Mid to Peak
- **Expected Answer:** Shows empathy, problem-solving, and a focus on enhancing customer experience.

**Q: How do you ensure that the systems you build meet the needs of end-users?**
- **Level:** Mid
- **Expected Answer:** Discusses user feedback loops, usability testing, and iterative development.

**Q: Explain how you prioritize customer needs when balancing technical debt and feature development.**
- **Level:** Mid to Peak
- **Expected Answer:** Highlights prioritization frameworks, stakeholder engagement, and long-term value delivery.

---

## Cloud Knowledge Questions

**Q: List K8s key components in master node and worker node, what's the responsibility.**
- **Level:** Mid
- **Expected Answer:** Master: API server (REST endpoint), etcd (cluster data), scheduler (pod placement), controller manager (reconciliation loops). Worker: kubelet (pod lifecycle), kube-proxy (networking), container runtime.

**Q: What Linux kernel features support docker containers?**
- **Level:** Mid
- **Expected Answer:** Namespaces (process isolation), cgroups (resource limits), capabilities (privilege management), seccomp (syscall filtering), AppArmor/SELinux (MAC).

**Q: Compared to pods and containers, why does K8s use containers as base units?**
- **Level:** Mid
- **Expected Answer:** Pods are logical grouping for co-located containers sharing network/storage; containers are execution units for single processes; this enables multi-container patterns (sidecar, ambassador, adapter).

**Q: Kernel - explain the difference between the Linux /proc and /sys filesystems.**
- **Level:** Mid to Peak
- **Expected Answer:** /proc: process information, system stats (read/write tunables); /sys: kernel object hierarchy, device info, driver parameters; /proc is legacy, /sys is structured.

**Q: Kernel - How to do Linux OS troubleshooting, which tools you will use?**
- **Level:** Mid
- **Expected Answer:** dmesg (kernel logs), journalctl (systemd logs), top/htop (process monitoring), strace (syscall tracing), perf (profiling), tcpdump (network), iotop (I/O), sar (historical stats).

**Q: Compared to deployment and replica set.**
- **Level:** Mid
- **Expected Answer:** ReplicaSet ensures N pods running; Deployment adds declarative updates, rollout/rollback, versioning; Deployment manages ReplicaSets for you.

**Q: What's a readiness probe and liveness probe, what's responsible?**
- **Level:** Mid
- **Expected Answer:** Liveness: restart container if unhealthy; Readiness: remove from service endpoints if not ready (no restart); Startup: delay liveness/readiness checks until app initializes.

**Q: What is a service mesh?**
- **Level:** Mid
- **Expected Answer:** Infrastructure layer handling service-to-service communication (traffic management, security, observability) via sidecar proxies (e.g., Istio/Envoy, Linkerd); separates business logic from network concerns.

**Q: What's the relationship between PV and PVC?**
- **Level:** Mid
- **Expected Answer:** PV (Persistent Volume): cluster resource (storage); PVC (Persistent Volume Claim): request for storage by pod; PVC binds to PV based on storage class, access mode, capacity.

### Compute

**Q: What is a virtual machine (VM)? How does it differ from running an application directly on a physical server?**
- **Level:** Early
- **Expected Answer:** VM: software-based computer running inside physical hardware, has own OS, isolated from other VMs; uses hypervisor to share physical resources; allows multiple OS on one server, easier to move/backup. Direct on physical: one OS per server, no virtualization overhead, wastes resources if underutilized. VMs provide isolation, flexibility, and better resource utilization.

**Q: What is cloud computing? Explain the difference between IaaS, PaaS, and SaaS with examples.**
- **Level:** Early
- **Expected Answer:** Cloud: on-demand computing resources over internet, pay-as-you-go. IaaS (Infrastructure): VMs, storage, network (AWS EC2, Azure VMs) - you manage OS/apps; PaaS (Platform): app deployment platform (Heroku, Google App Engine) - you manage apps only; SaaS (Software): ready-to-use apps (Gmail, Salesforce) - you just use it. More managed = less control but easier.

**Q: What does "auto-scaling" mean in cloud? Why is it useful?**
- **Level:** Early
- **Expected Answer:** Auto-scaling: automatically add/remove compute instances based on demand (CPU, memory, traffic); scales up during peak (Black Friday), scales down to save cost when quiet. Useful for handling traffic spikes without over-provisioning, cost optimization, improved availability. Example: website adds servers when traffic increases, removes them at night.

**Q: What is a cloud region and availability zone? Why do we deploy across multiple zones?**
- **Level:** Early
- **Expected Answer:** Region: geographic area (us-east-1, eu-west-1); Availability Zone (AZ): isolated datacenter within region with own power/network. Deploy across AZs for high availability - if one AZ fails (power outage, network issue), other AZs keep running. Most cloud services automatically replicate across AZs.

**Q: What is a load balancer? Why would you use one?**
- **Level:** Early
- **Expected Answer:** Load balancer: distributes traffic across multiple servers; prevents single server overload, improves availability (if one server fails, others handle traffic), enables horizontal scaling. Example: 100 users spread across 5 web servers instead of all hitting one server. Cloud load balancers (ELB, ALB) are managed services with health checks.

**Q: What are the key differences between Type 1 (bare-metal) and Type 2 (hosted) hypervisors? Give examples of each.**
- **Level:** Early to Mid
- **Expected Answer:** Type 1: runs directly on hardware (KVM, VMware ESXi, Xen, Hyper-V), better performance, production use. Type 2: runs on host OS (VirtualBox, VMware Workstation), easier setup, development/testing use. Type 1 has lower overhead and direct hardware access.

**Q: Explain cloud instance types (general purpose, compute optimized, memory optimized, storage optimized). How do you choose the right instance type?**
- **Level:** Mid
- **Expected Answer:** General purpose: balanced CPU/memory (T/M series in AWS), web servers, small databases; Compute optimized: high CPU (C series), batch processing, gaming; Memory optimized: high RAM (R/X series), in-memory databases, big data; Storage optimized: high IOPS (I/D series), data warehouses. Choose based on workload bottleneck (CPU, memory, I/O profiling).

**Q: Explain how CPU pinning and NUMA awareness improve VM performance. When would you use these techniques?**
- **Level:** Mid to Peak
- **Expected Answer:** CPU pinning: bind VM vCPUs to specific physical cores, reduces context switching, prevents CPU migration; NUMA (Non-Uniform Memory Access): allocate memory from same NUMA node as CPU, reduces memory access latency. Use for latency-sensitive workloads (databases, real-time processing), high-performance VMs. Requires understanding of CPU topology.

### Network

**Q: What is an IP address? Explain the difference between IPv4 and IPv6.**
- **Level:** Early
- **Expected Answer:** IP address: unique identifier for devices on network. IPv4: 32-bit, 4 octets (192.168.1.1), ~4.3 billion addresses, running out; IPv6: 128-bit, hexadecimal (2001:0db8::1), virtually unlimited addresses. IPv6 needed due to IPv4 exhaustion, better for IoT and mobile devices.

**Q: What is the difference between a public IP and a private IP address?**
- **Level:** Early
- **Expected Answer:** Public IP: globally routable, unique on internet, assigned by ISP/cloud provider, used for internet-facing services; Private IP: used within internal network only (10.x.x.x, 172.16.x.x, 192.168.x.x), not routable on internet, can be reused in different networks. Use private IPs for internal communication, public IPs for external access.

**Q: What is a subnet? Why do we divide networks into subnets?**
- **Level:** Early
- **Expected Answer:** Subnet: subdivision of IP network (192.168.1.0/24); uses subnet mask to define network size (/24 = 256 IPs). Benefits: organize network logically (web tier, database tier), improve security (isolate sensitive systems), reduce broadcast traffic, more efficient IP allocation. Cloud: public subnets have internet access, private subnets don't.

**Q: What is a firewall? How do security groups work in cloud environments?**
- **Level:** Early
- **Expected Answer:** Firewall: controls network traffic based on rules (allow/deny); checks source/destination IP, port, protocol. Security groups: cloud firewall for VMs, stateful (auto-allow return traffic), define inbound/outbound rules. Example: allow port 443 (HTTPS) from anywhere, allow port 22 (SSH) from office IP only. Default deny-all, explicitly allow needed traffic.

**Q: What is the difference between HTTP and HTTPS? Why is HTTPS important?**
- **Level:** Early
- **Expected Answer:** HTTP: unencrypted web protocol, port 80, data visible in transit; HTTPS: encrypted (TLS/SSL), port 443, protects data from eavesdropping. HTTPS important for: security (passwords, credit cards), privacy, SEO (Google ranking), trust (browser warnings for HTTP). All modern web apps should use HTTPS.

**Q: What is DNS and why is it important? What happens when you type a URL in your browser?**
- **Level:** Early
- **Expected Answer:** DNS: Domain Name System, translates human-readable names (google.com) to IP addresses (142.250.80.46); distributed hierarchical database. Browser lookup: check local cache → query DNS resolver → root servers → TLD servers (.com) → authoritative nameserver → return IP → browser connects. Important: users don't need to remember IPs, can change IPs without changing domain.

**Q: What are the differences between TCP and UDP? Give examples of cloud services that use each and why.**
- **Level:** Early to Mid
- **Expected Answer:** TCP: connection-oriented, reliable delivery, ordering, flow control, higher overhead; UDP: connectionless, best-effort, lower latency, no guarantees. TCP: HTTP/HTTPS (web), databases (MySQL), SSH; UDP: DNS queries, streaming (video), gaming, service mesh health checks (fast failure detection). Choose based on reliability vs latency requirements.

**Q: Explain the difference between a Layer 2 (L2) and Layer 3 (L3) network. When would you use each in cloud infrastructure?**
- **Level:** Mid
- **Expected Answer:** L2: Ethernet switching, same broadcast domain, MAC addressing, VLAN segmentation; L3: IP routing, different subnets, routing protocols (BGP, OSPF), network isolation. Use L2 for same-subnet communication (database clusters), L3 for cross-subnet/inter-datacenter routing, security boundaries.

**Q: Explain VPC (Virtual Private Cloud) peering vs VPN vs Transit Gateway. When would you use each?**
- **Level:** Mid
- **Expected Answer:** VPC peering: direct connection between VPCs, same/cross-region, no bandwidth limits, non-transitive; VPN: encrypted tunnel over internet, site-to-site or client-to-site, lower cost but variable bandwidth; Transit Gateway: hub-and-spoke model, centralized routing, transitive peering, better for multi-VPC. Use peering for simple connectivity, VPN for hybrid cloud, Transit Gateway for complex multi-VPC architectures.

**Q: What is BGP (Border Gateway Protocol) and why is it important in cloud networking?**
- **Level:** Mid to Peak
- **Expected Answer:** BGP: path-vector routing protocol for inter-AS (Autonomous System) routing, internet backbone protocol; cloud uses: multi-cloud connectivity, hybrid cloud (Direct Connect/ExpressRoute), anycast routing, traffic engineering. BGP attributes (AS_PATH, LOCAL_PREF) control route selection. Critical for datacenter peering and internet routing.

### Storage

**Q: What is cloud storage? Name three common cloud storage services and their use cases.**
- **Level:** Early
- **Expected Answer:** Cloud storage: store data on remote servers accessed via internet. S3/Blob Storage: object storage for files, backups, static websites (cheap, unlimited); EBS/Persistent Disks: block storage for VMs, databases (fast, persistent); EFS/File Storage: shared filesystem for multiple servers (NFS-like). Choose based on: access pattern, sharing needs, cost.

**Q: What does it mean for storage to be "persistent" vs "ephemeral"?**
- **Level:** Early
- **Expected Answer:** Persistent: data survives VM stop/restart/reboot, stored separately (EBS, persistent disks), must explicitly delete; Ephemeral: temporary storage tied to VM lifecycle, deleted when VM terminates (instance store, local SSD). Use persistent for databases and important data, ephemeral for caches and temporary files.

**Q: What is data replication and why is it important for cloud storage?**
- **Level:** Early
- **Expected Answer:** Replication: copying data to multiple locations/servers automatically; protects against hardware failure, improves availability. Cloud storage typically replicates 3+ times within region or across regions. Benefits: durability (11 9's for S3), no single point of failure, faster recovery. Example: S3 stores copies in multiple datacenters automatically.

**Q: What is the difference between a backup and a snapshot?**
- **Level:** Early
- **Expected Answer:** Snapshot: point-in-time copy of disk/volume, fast (incremental), used for quick recovery, version control; stored in same cloud. Backup: full copy stored separately (different region/service), slower but more protection, disaster recovery. Best practice: use both - snapshots for quick recovery, backups for long-term retention and DR.

**Q: What is caching? How does it improve application performance?**
- **Level:** Early
- **Expected Answer:** Caching: storing frequently accessed data in fast storage (memory/SSD) to avoid slow operations (database query, API call, disk read). Benefits: lower latency (milliseconds vs seconds), reduced load on backend, cost savings. Common caches: Redis/Memcached (data), CDN (static files), browser cache. Must handle cache invalidation (TTL, manual purge) when data changes.

**Q: Compare block storage, file storage, and object storage. When would you use each?**
- **Level:** Early to Mid
- **Expected Answer:** Block: raw storage volumes (EBS, persistent disks), low-latency, single attachment, databases/VMs; File: shared filesystem (EFS, NFS, SMB), concurrent access, home directories/shared data; Object: S3/Blob, HTTP API, metadata-rich, unlimited scale, backups/static content/data lakes. Choose based on access pattern (direct vs shared), latency requirements, scale.

**Q: What is IOPS and throughput in storage? How do they differ and why are both important?**
- **Level:** Mid
- **Expected Answer:** IOPS: I/O Operations Per Second, measures small random reads/writes (4KB blocks), important for databases, transactional workloads; Throughput: MB/s, measures sequential I/O, important for large files, streaming, backups. Can have high IOPS with low throughput (random small), or low IOPS with high throughput (sequential large). Choose storage tier based on workload pattern.

**Q: Explain the difference between SSD and HDD storage. What are NVMe SSDs and how do they differ from SATA SSDs?**
- **Level:** Mid
- **Expected Answer:** HDD: spinning disks, magnetic, slower, cheaper, sequential I/O OK; SSD: flash memory, faster, more expensive, better random I/O. SATA SSD: SATA interface (6 Gbps limit), legacy protocol; NVMe SSD: PCIe interface (up to 32 Gbps), parallel command queues, much lower latency (<100µs vs ~1ms). Use NVMe for high-performance databases, SATA for general workloads, HDD for cold storage.

**Q: Explain storage tiering and lifecycle policies. How would you optimize storage costs?**
- **Level:** Mid
- **Expected Answer:** Storage tiering: hot (frequent access, expensive), warm (infrequent, cheaper), cold (archival, cheapest); S3 tiers (Standard, IA, Glacier, Deep Archive); lifecycle policies automate transitions based on age/access patterns. Cost optimization: identify access patterns (CloudWatch metrics), move old data to cold tier, delete obsolete data, use compression, right-size volumes. Example: logs to Glacier after 90 days.

### General Cloud Concepts

**Q: What is elasticity in cloud computing? How is it different from scalability?**
- **Level:** Early
- **Expected Answer:** Elasticity: automatic scaling up/down based on real-time demand, dynamic; Scalability: ability to handle growth by adding resources, planned. Elastic: auto-add servers during traffic spike then remove; Scalable: can add capacity when needed. Elasticity implies scalability, but scalability doesn't require automatic elasticity.

**Q: What is the shared responsibility model in cloud security?**
- **Level:** Early
- **Expected Answer:** Cloud provider responsible for: physical security, hardware, network infrastructure, hypervisor; Customer responsible for: OS patching, application security, data encryption, access control, firewall rules. More managed service = more provider responsibility. Example: IaaS (customer manages OS+), PaaS (customer manages app+), SaaS (customer manages data/access only).

**Q: What is high availability (HA)? What techniques achieve high availability in cloud?**
- **Level:** Early
- **Expected Answer:** High availability: system remains operational even during failures, minimal downtime (99.9%+ uptime). Techniques: redundancy (multiple instances), load balancing, health checks, auto-recovery, multi-AZ deployment, automated failover. Example: deploy 3 web servers across 2 AZs behind load balancer - if one fails, others continue serving traffic.

**Q: What is the difference between horizontal and vertical scaling in cloud compute? Provide examples of when you'd use each.**
- **Level:** Early to Mid
- **Expected Answer:** Horizontal: add more instances/nodes (scale out), better for stateless apps, unlimited scaling potential; Vertical: increase resources per instance (scale up), simpler but limited by hardware, better for stateful apps or databases. Use horizontal for web servers, vertical for single-instance databases or legacy apps.

**Q: What is a CDN (Content Delivery Network) and how does it improve performance? How does edge caching work?**
- **Level:** Mid
- **Expected Answer:** CDN: geographically distributed servers caching content closer to users; reduces latency, bandwidth costs, origin load. Edge caching: stores static content (images, CSS, JS) at PoP (Point of Presence) locations; cache invalidation strategies (TTL, purge API); dynamic content acceleration via route optimization. Use CloudFront/CloudFlare/Akamai for global user base.

**Q: Explain distributed storage systems. What is eventual consistency vs strong consistency?**
- **Level:** Mid to Peak
- **Expected Answer:** Distributed storage: data replicated across nodes/regions (S3, Cassandra, Ceph); CAP theorem (Consistency, Availability, Partition tolerance - pick 2). Strong consistency: all replicas agree before read (slower, linearizable, banks), read-your-writes guarantee; Eventual consistency: replicas converge over time (faster, available during partition, DNS, shopping carts). Use strong for financial/inventory, eventual for social feeds/caches.

---

## Linux Kernel & OS Internals

**Q: Explain the process of booting a Linux system from BIOS to running userspace.**
- **Level:** Peak
- **Expected Answer:** BIOS/UEFI → bootloader (GRUB) → kernel loading → init process (systemd/init.d) → mounting filesystems → starting services → login prompt.

**Q: What is the role of the kernel in memory management? How does the Linux kernel handle memory allocation and page faults?**
- **Level:** Mid to Peak
- **Expected Answer:** Manages physical/virtual memory, page tables, MMU; handles page faults (demand paging, copy-on-write), swapping, caching (page cache, buffer cache).

**Q: Describe the role and importance of system calls in Linux. Can you name a few commonly used system calls?**
- **Level:** Early to Mid
- **Expected Answer:** Interface between user space and kernel; examples: read(), write(), fork(), exec(), open(), close(); enables process management, I/O, memory allocation.

**Q: What are cgroups and namespaces, and how do they contribute to containerization in Linux?**
- **Level:** Mid to Peak
- **Expected Answer:** Cgroups: resource limitation (CPU, memory, I/O quotas); Namespaces: process isolation (PID, network, mount, UTS, IPC, user); together enable container isolation.

---

## Kernel Engineering

**Q: Describe your experience customizing and optimizing the Linux kernel. What were the performance gains or tradeoffs?**
- **Level:** Peak
- **Expected Answer:** Shows understanding of kernel config, scheduler tuning, cgroups, memory management; mentions measurable impact and debugging tools (perf, ftrace, trace-cmd).

**Q: How would you implement a controlled and reliable Linux OS upgrade process across thousands of nodes?**
- **Level:** Mid to Peak
- **Expected Answer:** Phased rollouts, canary upgrades, failback strategies, package/image management (apt, yum, OSTree), automation via Ansible/SaltStack, monitoring, blast radius control.

**Q: What kernel subsystems have you contributed to or debugged in-depth? How did you approach a tricky kernel bug?**
- **Level:** Peak
- **Expected Answer:** Shows confidence reading kernel source, using crash dumps, understanding spinlocks/mutexes, tracepoints, bisecting regressions (git bisect), reproducing issues.

---

## Containerization & Kubernetes

**Q: How does Kubernetes manage the lifecycle of containers?**
- **Level:** Mid
- **Expected Answer:** Explains Pods (smallest unit), Deployments (declarative updates), ReplicaSets (desired state), how K8s orchestrates container deployment, scaling, self-healing.

**Q: What are the differences between a Kubernetes Deployment and a StatefulSet, and when would you use each?**
- **Level:** Mid to Peak
- **Expected Answer:** Deployment: stateless apps, random pod names, any-order scaling; StatefulSet: stateful apps, stable network IDs, ordered deployment/scaling, persistent storage per pod.

**Q: Describe the networking model in Kubernetes. How do Pods communicate with each other?**
- **Level:** Mid to Peak
- **Expected Answer:** Flat network model (every pod has unique IP), CNI plugins (Calico, Cilium, Flannel), Services (ClusterIP, NodePort, LoadBalancer), Network Policies, kube-dns/CoreDNS.

**Q: How does Kubernetes handle scaling, both horizontally and vertically?**
- **Level:** Mid
- **Expected Answer:** Horizontal: ReplicaSets, HPA (Horizontal Pod Autoscaler) based on CPU/memory/custom metrics; Vertical: VPA (Vertical Pod Autoscaler) adjusts resource requests/limits; cluster autoscaler adds/removes nodes.

---

## Containerization & Runtimes

**Q: How do container runtimes like runc, containerd, and Kata Containers differ architecturally? When would you use each?**
- **Level:** Mid to Peak
- **Expected Answer:** runc: OCI-compliant low-level runtime (Linux containers); containerd: high-level runtime (image management, container lifecycle); Kata: hardware virtualization for strong isolation; use Kata for untrusted workloads.

**Q: What challenges have you faced managing containers alongside VMs in a mixed runtime environment?**
- **Level:** Mid
- **Expected Answer:** Resource contention, scheduling complexity, CNI/networking plugin implications, security profiles (AppArmor, seccomp), different monitoring/logging approaches.

---

## Networking & Security

**Q: Explain how you would secure a Kubernetes cluster. What measures would you take to protect both the control plane and workloads?**
- **Level:** Peak
- **Expected Answer:** RBAC (role-based access), Network Policies, PodSecurityStandards, API server auth/authz, audit logs, etcd encryption at rest, TLS for all components, admission controllers (OPA/Gatekeeper).

**Q: What are the key differences between Layer 3 and Layer 7 in network security, and how does this relate to Kubernetes?**
- **Level:** Mid
- **Expected Answer:** Layer 3 (IP level): Network Policies for pod-to-pod; Layer 7 (application level): Service mesh (Istio), Ingress controllers for HTTP routing, WAF integration.

**Q: Describe a situation where you had to debug a networking issue in a containerized environment. What tools and techniques did you use?**
- **Level:** Mid
- **Expected Answer:** kubectl logs/describe, nslookup/dig (DNS), ping/traceroute, tcpdump/wireshark (packet capture), eBPF tracing, checking service endpoints, network policy rules.

**Q: What is the difference between a Kubernetes Ingress and a Service, and when would you use each?**
- **Level:** Mid
- **Expected Answer:** Service: internal/external load balancing (ClusterIP, NodePort, LoadBalancer); Ingress: HTTP(S) routing, host/path-based rules, TLS termination, single entry point for multiple services.

---

## BPF & Networking

**Q: How have you used eBPF for observability or network policy enforcement?**
- **Level:** Mid to Peak
- **Expected Answer:** Explains tracing with BCC/bpftrace, XDP usage for packet filtering, Cilium for network policies, low-overhead diagnostics, code samples or OSS contributions.

**Q: What are the performance and security considerations when deploying BPF-based observability tools?**
- **Level:** Peak
- **Expected Answer:** Understands BPF verifier (safety checks), kernel versioning compatibility, tail calls (program chaining), memory safety, impact of probes in critical paths (overhead), BTF (BPF Type Format).

---

## System Design Questions

**Q: How to design a patching system.**
- **Level:** Mid to Peak
- **Expected Answer:** Phased rollout (canary → staging → prod), rollback mechanism, monitoring/alerting, version control, node cordoning/draining, health checks, maintenance windows, automation.

**Q: How to design a distributed cache system.**
- **Level:** Mid to Peak
- **Expected Answer:** Consistent hashing, replication (master-slave, multi-master), eviction policies (LRU, LFU), TTL, cache invalidation strategies, CAP theorem tradeoffs, monitoring (hit rate, latency).

**Q: How to design a ride-sharing system (Uber).**
- **Level:** Mid to Peak
- **Expected Answer:** Geo-hashing/quad-tree for driver matching, WebSocket for real-time updates, ACID for payments, eventual consistency for ride status, load balancing, surge pricing algorithm, scaling strategy.

**Q: Global Patching & Fleet Management - Design an automated system to patch the Linux Kernel or Container Runtime (e.g., moving from Docker to Containerd) across 10,000 nodes in 5 global regions with zero downtime for applications.**
- **Level:** Peak
- **Expected Answer:** Phased rollout strategy (region-by-region, zone-aware), canary testing per region, automated health checks and validation, node draining/cordoning (PodDisruptionBudgets), rollback mechanisms, traffic shifting during patching, monitoring and alerting per region, maintenance windows optimization, blast radius control, automation via GitOps (ArgoCD/Flux), dependency management (kernel compatibility testing), communication strategy across regions.

**Q: Intelligent Workload Rebalancing - Design a system that detects 'noisy neighbor' applications consuming all Disk I/O in a multi-tenant Kubernetes cluster and rebalances the workload without human intervention.**
- **Level:** Mid to Peak
- **Expected Answer:** Real-time metrics collection (Disk I/O per pod/namespace), anomaly detection algorithms, threshold-based triggers, automatic pod eviction/rescheduling, resource quotas and limits enforcement (cgroups tuning), QoS class consideration (BestEffort, Burstable, Guaranteed), pod priority and preemption, node affinity/anti-affinity adjustments, gradual rebalancing (avoiding thundering herd), audit logging and notifications, integration with cluster autoscaler, SLO/SLA preservation for other tenants.

**Q: Global Container Image Registry - Design a global container registry architecture for a company with developers in the US, Europe, and Asia. It must support high-speed pulls during massive scaling events (e.g., 5,000 pods starting at once).**
- **Level:** Mid to Peak
- **Expected Answer:** Multi-region replication (geo-distributed registries), CDN integration for edge caching, layer deduplication and compression, pull-through cache proxies (Harbor, Docker Registry proxy), image pre-warming strategies, horizontal scaling of registry servers, load balancing across regions, image signing and verification (Notary, cosign), garbage collection strategies, storage backend selection (S3, GCS, Azure Blob), bandwidth optimization (delta pulls, lazy pulling), monitoring (pull latency, cache hit rate), disaster recovery and failover.

**Q: Application Migrations (Cloud-to-Cloud / Hybrid) - Design a plan to migrate a mission-critical, stateful PostgreSQL database and 50 microservices from an on-premise Data Center to AWS with a maximum allowable downtime of 60 seconds.**
- **Level:** Peak
- **Expected Answer:** Pre-migration assessment (dependency mapping, data volume analysis), dual-write strategy or database replication (logical replication, AWS DMS), zero-downtime migration approach (blue-green deployment), microservices migration phases (stateless first, then stateful), DNS/traffic cutover strategy (Route53, load balancer switching), database synchronization and validation (checksum validation, lag monitoring), rollback plan (quick failback to on-prem), testing in staging environment (chaos testing, load testing), cutover window planning (low-traffic period), monitoring and alerting during migration, communication plan (stakeholders, teams), post-migration validation (data integrity checks, performance benchmarks).

---

## Systems Design & Architecture

**Q: Design a scalable and fault-tolerant Kubernetes control plane for a multi-region environment.**
- **Level:** Peak
- **Expected Answer:** etcd HA (3/5 nodes, Raft consensus), control plane separation per region, API server scaling (load balancing), multi-region federation, disaster recovery (backup/restore), network segmentation.

**Q: How would you architect a logging and metrics pipeline for thousands of Kubernetes nodes?**
- **Level:** Mid to Peak
- **Expected Answer:** Fluentd/Vector/Fluent Bit (log forwarding), Prometheus (metrics), OpenTelemetry (traces), log aggregation (Elasticsearch/Loki), horizontal scaling, long-term storage (S3/GCS), retention policies.

**Q: How would you scale a PKI infrastructure to serve thousands of internal services with minimal latency?**
- **Level:** Peak
- **Expected Answer:** Balances scalability, security, fault tolerance; discusses CA hierarchy, certificate caching, geo-redundancy, OCSP stapling, automation (cert-manager), monitoring.

**Q: How do you approach designing a Kafka-based event system that must guarantee no message loss and high throughput?**
- **Level:** Mid to Peak
- **Expected Answer:** Partitioning strategy, replication factor (min in-sync replicas), consumer group handling, idempotent producers, exactly-once semantics, monitoring lag, retention policies.

**Q: Design a globally distributed key validation system for client certificates. How do you ensure low latency and high availability?**
- **Level:** Peak
- **Expected Answer:** PoP (Point of Presence) placement, caching validation results, OCSP alternatives (OCSP stapling, CRLite), failover mechanisms, load balancing, key revocation propagation.

**Q: How would you architect a secure multi-tenant edge platform that isolates traffic and data between tenants?**
- **Level:** Mid to Peak
- **Expected Answer:** Namespace separation (K8s), authn/authz layers (OIDC/OAuth), RBAC/ABAC, eBPF for network isolation, resource quotas/limits, logging segmentation, network policies.

**Q: Explain how you would design logging and observability for an edge auth system without leaking PII.**
- **Level:** Mid
- **Expected Answer:** PII redaction/masking, field-level filtering, log sampling, secure transport (TLS), user opt-out mechanisms, alerting without sensitive data, compliance (GDPR/CCPA).

**Q: Design a Linux-based OS image pipeline for Kubernetes nodes that supports secure boot, observability, and rollback.**
- **Level:** Peak
- **Expected Answer:** Reproducible builds (Packer/Nix), secure boot (UEFI Secure Boot, TPM), image signing, CI/CD pipelines, immutable images (OSTree/A/B partitions), containerd/CRI-O integration, monitoring hooks, rollback mechanism.

**Q: How would you design a distributed rate-limiting system that works across multiple data centers?**
- **Level:** Mid to Peak
- **Expected Answer:** Token bucket/leaky bucket algorithms, distributed counters (Redis), consistency across regions (eventual consistency acceptable), network partition handling, failover strategies.

**Q: Design a secure service for handling API keys and secrets. What are your design priorities?**
- **Level:** Mid
- **Expected Answer:** Encryption at rest (AES-256)/in transit (TLS), access controls (RBAC), audit logging, secret rotation, expiration policies, secure storage (Vault/KMS), least privilege.

**Q: How would you implement secure service discovery in a microservices architecture?**
- **Level:** Mid
- **Expected Answer:** Mutual TLS (mTLS) for authentication, identity-based access (SPIFFE/SPIRE), service mesh (Istio/Linkerd), DNS security (DNSSEC), preventing DNS poisoning, encryption in transit.

---

## Coding Questions

**Q: What is the heap data structure and it could be used to resolve what kind of problem? What's the big O complexity?**
- **Level:** Mid
- **Expected Answer:** Min-heap/max-heap (complete binary tree); used for priority queues, top-K problems, median finding; insert/delete: O(log n), peek: O(1), heapify: O(n).

**Q: Give me several sort algorithms and share with me the big O complexity.**
- **Level:** Early to Mid
- **Expected Answer:** Quick sort O(n log n avg, n² worst), Merge sort O(n log n), Heap sort O(n log n), Bubble sort O(n²), Insertion sort O(n²), Radix sort O(nk).

**Q: What's the average or worse big O complexity for quick sort?**
- **Level:** Early to Mid
- **Expected Answer:** Average: O(n log n) with good pivot selection; Worst: O(n²) with bad pivot (already sorted, random pivot mitigation).

**Q: How to implement LRU algorithm.**
- **Level:** Mid
- **Expected Answer:** Doubly linked list + hash map; get/put O(1); move accessed item to front, evict tail when capacity reached.

**Q: What is BFS and DFS? Could you use BFS to find the nearest leaf node in the tree?**
- **Level:** Early to Mid
- **Expected Answer:** BFS (Breadth-First Search): level-order traversal, queue-based; DFS (Depth-First Search): pre/in/post-order, stack-based; BFS finds nearest leaf (level-order guarantees shortest path).

**Q: What is a consistent hash?**
- **Level:** Mid
- **Expected Answer:** Hash ring for distributed systems; minimal key redistribution when nodes added/removed; virtual nodes for load balancing; used in CDNs, distributed caches.

---

## Programming Proficiency

**Q: What are the key differences between Go and Python in terms of concurrency and performance?**
- **Level:** Mid
- **Expected Answer:** Go: goroutines (lightweight threads), channels (CSP model), compiled (fast); Python: threading (GIL limits CPU), multiprocessing (process overhead), interpreted (slower); Go better for concurrent systems.

**Q: Describe a time when you optimized code for performance in a containerized environment. What tools or techniques did you use?**
- **Level:** Early to Mid
- **Expected Answer:** Profiling (pprof for Go, cProfile for Python), flame graphs, reducing CPU/memory overhead, caching, connection pooling, resource limits tuning.

**Q: How would you handle error handling and logging in a high-performance Go application?**
- **Level:** Mid
- **Expected Answer:** Explicit error returns (no exceptions), wrapping errors (fmt.Errorf, errors.Wrap), structured logging (Logrus, Zap), context propagation, log levels, async logging.

**Q: What's your approach to managing dependencies and ensuring reproducibility in a multi-language development environment (Go, Python)?**
- **Level:** Mid
- **Expected Answer:** Go modules (go.mod), Python virtualenv/Poetry/pipenv, Docker for environment consistency, dependency pinning, vendoring, lock files, CI/CD reproducibility.

---

## Programming & Tooling

**Q: Tell me about a Go-based system tool you've built. What made you choose Go and how did you ensure performance?**
- **Level:** Mid to Peak
- **Expected Answer:** Memory handling (pointers, escape analysis), concurrency patterns (worker pools, channels), benchmarks (testing.B), GC tuning, profiling (pprof), metrics (go-metrics/Prometheus).

**Q: Describe a Python-based automation or monitoring tool you created. What was its impact?**
- **Level:** Mid
- **Expected Answer:** Scripting proficiency, API integrations (requests, boto3), real-world improvements (time savings, error reduction), libraries (click for CLI, asyncio for concurrency).

---

## Software Development Questions

**Q: Could you describe the software development process?**
- **Level:** Early to Mid
- **Expected Answer:** Requirements gathering → design → implementation → testing (unit, integration, E2E) → code review → deployment → monitoring → iteration; mentions Agile/Scrum, CI/CD.

**Q: How could you ensure high quality for your software release into production?**
- **Level:** Mid
- **Expected Answer:** Automated testing (unit, integration, E2E), code reviews, static analysis (linters), staging environment, canary deployments, monitoring/alerting, rollback plan, postmortems.

**Q: What are DORA metrics?**
- **Level:** Mid
- **Expected Answer:** DevOps Research and Assessment metrics: Deployment Frequency, Lead Time for Changes, Mean Time to Recovery (MTTR), Change Failure Rate; measures DevOps performance.

**Q: Share with me your checklist to avoid production bugs?**
- **Level:** Mid
- **Expected Answer:** Code review, automated tests, static analysis, integration tests, staging validation, feature flags, canary rollout, monitoring, rollback plan, runbooks.

**Q: Share with me one example of how you deal with product incidents, during and after.**
- **Level:** Mid
- **Expected Answer:** During: triage (SEV assessment), incident commander, communication (status page), mitigation (rollback/hotfix), logging. After: postmortem (blameless), action items, knowledge sharing.

**Q: You lead a project with 2 junior engineers, it has a tight schedule, how do you do?**
- **Level:** Mid to Peak
- **Expected Answer:** Clear scope/goals, task breakdown, mentoring/pairing, code reviews, daily standups, risk identification, timeline buffer, stakeholder communication.

---

## Observability & Diagnostics

**Q: How would you instrument an application running in Kubernetes for better observability?**
- **Level:** Mid
- **Expected Answer:** Metrics (Prometheus client libraries), distributed tracing (OpenTelemetry), centralized logging (Fluentd → Elasticsearch/Loki), golden signals (latency, traffic, errors, saturation).

**Q: What metrics and logs would you collect to monitor the health of Kubernetes nodes and workloads?**
- **Level:** Mid
- **Expected Answer:** Node: CPU/memory/disk/network usage, kubelet metrics; Pod: resource usage, restart count, readiness/liveness probe failures; container logs, events, kube-apiserver audit logs.

**Q: Describe how you would troubleshoot a Kubernetes pod that is continuously restarting.**
- **Level:** Mid
- **Expected Answer:** kubectl logs (current/previous), kubectl describe pod (events), resource limits (OOMKilled), liveness/readiness probes, crash loop backoff, image pull errors, init container failures.

**Q: How would you monitor and troubleshoot high latency in a Kubernetes network?**
- **Level:** Mid
- **Expected Answer:** kubectl exec → ping/curl, tcpdump (packet capture), network policy checks, DNS resolution (nslookup/dig), service endpoint health, CNI plugin issues, node network saturation.

---

## Observability

**Q: How do you ensure observability for a custom OS running Kubernetes? What metrics and tools do you rely on?**
- **Level:** Mid
- **Expected Answer:** Prometheus (node-exporter, kube-state-metrics, cAdvisor), eBPF (low-overhead tracing), journald/systemd logs, alerting strategy (Alertmanager), golden signals, SLIs/SLOs.

---

## Debugging & Troubleshooting

**Q: Walk me through how you diagnosed a kernel panic or node crash in production.**
- **Level:** Peak
- **Expected Answer:** kdump (kernel crash dump), analyzing vmcore with crash utility, dmesg logs, memory dumps, bisecting kernel changes (git bisect), reproducibility testing, hardware checks.

**Q: What steps would you take to troubleshoot intermittent network latency in a containerized app?**
- **Level:** Mid
- **Expected Answer:** tcpdump/wireshark (packet analysis), iperf (bandwidth testing), eBPF tracing (latency breakdown), QoS configs, container-to-host bridge issues, DNS latency, noisy neighbor detection.

---

## Troubleshooting

**Q: A Kubernetes pod is stuck in `CrashLoopBackOff`. Walk through your approach to debugging it.**
- **Level:** Early to Mid
- **Expected Answer:** kubectl logs (check errors), kubectl describe pod (events, resource limits), image pull status, liveness/readiness probe configs, recent changes (deployment history), init container logs.

**Q: High CPU usage is detected in your certificate signing service. How would you proceed?**
- **Level:** Mid
- **Expected Answer:** Profiling (pprof, perf), code efficiency review, GC behavior analysis (for managed languages), misconfigurations (worker pool size), attack vectors (DDoS), rate limiting.

**Q: A bot mitigation service is experiencing false positives. How do you improve its accuracy?**
- **Level:** Mid to Peak
- **Expected Answer:** Better behavioral heuristics (user patterns), data feedback loops (labeled data), A/B testing, rollout controls (feature flags), detailed logging (investigation), ML model tuning.

**Q: Your DNS layer is intermittently resolving slowly. What tools and strategies do you use to investigate?**
- **Level:** Mid
- **Expected Answer:** dig/nslookup (query time), latency metrics (histogram), upstream DNS health, TTL settings, recursive resolution issues, cache hit rate, DNS server load.

**Q: Certificates in one region are not renewing. How do you triage and isolate the issue?**
- **Level:** Mid
- **Expected Answer:** Regional logging analysis (cert-manager logs), service health checks (cert validation endpoint), dependency mapping (ACME server reachability), failover testing, IAM/RBAC permissions.

---

## Incident Response

**Q: Describe how you would handle a zero-day vulnerability in a critical edge component (e.g., OpenSSL or NGINX).**
- **Level:** Mid to Peak
- **Expected Answer:** Identification (CVE scanning), impact analysis (affected services), patch/testing (staging validation), rollout plan (phased deployment), communication strategy (stakeholders, customers), postmortem.

**Q: Have you ever had to rollback a security feature due to production issues? What did you learn?**
- **Level:** Mid
- **Expected Answer:** Maturity in balancing security vs. reliability, rollback planning (feature flags, canary), stakeholder alignment (trade-offs), lessons learned (testing rigor, gradual rollout).

**Q: What metrics would you monitor to detect potential abuse or system compromise in an edge service?**
- **Level:** Mid
- **Expected Answer:** Anomaly detection (spikes), auth failure rate, egress volume (data exfiltration), response latencies, geographic anomalies, 4xx/5xx error ratios, unusual traffic patterns.

---

## Operational Excellence

**Q: What strategies do you use to ensure high availability and minimal downtime in Kubernetes workloads?**
- **Level:** Mid
- **Expected Answer:** Readiness/liveness probes, PodDisruptionBudgets, zone-aware autoscaling (pod topology spread), chaos testing (chaos mesh), multi-region deployments, blue-green/canary rollouts.

**Q: Describe how you handle on-call rotations and reduce alert fatigue.**
- **Level:** Mid
- **Expected Answer:** SLO-based alerting (error budgets), alert tuning (reducing noise), actionable alerts only, incident review processes (postmortems), runbooks (clear remediation steps), escalation policies.

---

## Security Engineering

**Q: How would you prevent and detect SSRF attacks in an edge service handling dynamic routing?**
- **Level:** Mid to Peak
- **Expected Answer:** Input validation (URL allowlisting), egress controls (network policies), logging patterns (suspicious requests), metadata protection (IMDSv2), WAF rules, service mesh policies, sandboxing.

**Q: What are common TLS misconfigurations you've seen, and how would you detect or mitigate them at scale?**
- **Level:** Mid to Peak
- **Expected Answer:** Weak cipher suites, expired certificates, missing OCSP stapling, protocol downgrade (SSLv3/TLS 1.0), automation (cert-manager, monitoring tools like SSL Labs API), configuration audits.

**Q: Describe how you'd build rate-limiting logic that can withstand DDoS attacks without impacting legitimate users.**
- **Level:** Mid to Peak
- **Expected Answer:** IP/user-token limiting, token bucket/leaky bucket algorithms, CAP principles (availability during partition), CDN strategies (Cloudflare), edge filters, behavioral rate limiting (fingerprinting).

**Q: How do you handle secrets management at the edge where latency and availability are critical?**
- **Level:** Mid
- **Expected Answer:** Secure bootstrapping (init containers), caching with rotation (TTL-based), zero-trust design (short-lived credentials), integration with secret managers (Vault, AWS Secrets Manager), HSM for sensitive keys.

**Q: What's your process for reviewing the security posture of a third-party edge SDK or module before integration?**
- **Level:** Mid
- **Expected Answer:** Dependency analysis (npm audit, Snyk), SBOM tools (Software Bill of Materials), vulnerability scanning (Trivy, Grype), static/dynamic testing (SAST/DAST), supply chain hygiene (signed commits, provenance).

---

## Security & Compliance Awareness

**Q: How do you ensure compliance and security for custom OS images across a fleet?**
- **Level:** Mid to Peak
- **Expected Answer:** CIS benchmarks (hardening), image signing (Notary, cosign), secure boot (UEFI Secure Boot), auditing tools (Lynis, OpenSCAP), drift detection, immutable infrastructure.

**Q: What's your approach to managing secrets in a containerized environment?**
- **Level:** Mid
- **Expected Answer:** Kubernetes secrets (encrypted at rest via KMS), Vault integration, key rotation (automated), RBAC (least privilege), secrets in transit (TLS), avoid environment variables.

---

## Automation & Tooling

**Q: What's a CI/CD setup you implemented for OS or Kubernetes deployment? What tools did you use?**
- **Level:** Mid
- **Expected Answer:** Jenkins/GitHub Actions/GitLab CI, ArgoCD (GitOps), image signing (cosign), canary testing (Flagger), automated rollback (health checks), pipeline stages (build/test/deploy).

**Q: Describe a time you automated a repetitive system task. What was the outcome?**
- **Level:** Early to Mid
- **Expected Answer:** Scripting (Bash, Python, Ansible), measurable time savings (hours → minutes), reduced errors (human error elimination), team benefit (knowledge sharing, documentation).

---

## Continuous Learning

**Q: What recent developments in Linux kernel, Kubernetes, or cloud-native observability excite you most?**
- **Level:** Early to Peak
- **Expected Answer:** Curiosity, mentions kernel features (Landlock LSM, io_uring, BPF improvements), Cilium/eBPF networking, Gvisor security, OpenTelemetry, OSS engagement.

---

## Open Source Contributions

**Q: What's a recent open-source contribution you've made? How do you decide what projects to contribute to?**
- **Level:** Mid to Peak
- **Expected Answer:** Code samples (GitHub PRs), communication on issues/MRs, interest in upstream collaboration, ecosystem relevance (tools you use daily), addressing pain points.

---

## Strategy

**Q: How do you balance engineering velocity with long-term security investments in a fast-paced environment?**
- **Level:** Mid
- **Expected Answer:** Phasing security work (incremental), evangelizing value (risk communication), aligning with risk tolerance (business priorities), automation/tooling (shift-left security), tech debt tracking.

---

## Vision

**Q: What recent trends in edge computing or distributed security excite you? How do you stay ahead of the curve?**
- **Level:** Early to Peak
- **Expected Answer:** Curiosity, follows conferences (KubeCon, Black Hat), blogs (Cloudflare, Fastly), awareness of WASM at edge, passkeys (WebAuthn), egress controls, AI+security, remote attestation.

**Q: Where do you think edge security is heading in the next 3-5 years, and how should we prepare for it?**
- **Level:** Mid to Peak
- **Expected Answer:** Shift toward confidential computing (SGX, SEV), decentralized identity (DIDs), automation (AI-driven threat detection), post-quantum crypto, user-centric privacy models (zero-knowledge proofs).

---

## Other

**Q: What security trends are you most excited about right now? How do you stay current?**
- **Level:** Early to Peak
- **Expected Answer:** Curiosity, learning habits (blogs, Twitter, conferences), awareness of trends like passkeys, AI-secured infrastructure, supply chain attack mitigation (SLSA framework), zero-trust.

**Q: What's a recent technical topic you've taught a teammate? How did you approach it?**
- **Level:** Early to Mid
- **Expected Answer:** Clarity in teaching, mentoring approach (documentation, pairing, demos), adaptability to learning styles (visual, hands-on, reading).

**Q: How do you prioritize your tasks when faced with multiple urgent system issues?**
- **Level:** Mid
- **Expected Answer:** Triage (SEV levels), impact analysis (blast radius), alert severity (customer-facing vs. internal), clear communication (status updates), escalation when needed.

**Q: What would you do in your first 90 days if hired into this role?**
- **Level:** Early to Mid
- **Expected Answer:** Planning (learning roadmap), ramp-up goals (onboarding tasks), relationship building (1:1s with team/stakeholders), quick wins focus (low-hanging fruit).

**Q: Tell me about a time you changed your mind after listening to a teammate's perspective.**
- **Level:** Mid
- **Expected Answer:** Openness to feedback, willingness to learn, team-first mindset (ego-free), growth attitude (continuous improvement).

---

## Changelog

### 2026-01-11
- Restructured into consolidated question library organized by focus area
- Added career level indicators (Early/Mid/Peak) for all questions
- Included expected answer traits from CSV source
- Separated from interview process document for clarity
- Added comprehensive table of contents with anchor links

### 2025-03-19
- Initial version created as combined process + questions

---

**For interview process and stage guidance, see:** [Infrastructure Engineering Interview Process](./Infrastructure-Engineering-Interview-Process.md)
