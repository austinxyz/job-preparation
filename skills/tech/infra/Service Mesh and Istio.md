---
title: Service Mesh and Istio
category: tech/infra
tags: [istio, service-mesh, envoy, sidecar, mtls, traffic-management, observability, ambient-mesh, distributed-tracing]
status: draft
priority: medium
last_updated: 2026-04-06
created_from_jd:
---

# Service Mesh and Istio

## Knowledge Map
- Prerequisites（前置知识）：[[Kubernetes]], [[K8s Control Plane]], [[Networking Fundamentals]]
- Related Topics（延伸话题）：[[Distributed Tracing]], [[Zero Trust Security]]
- Management（管理关联）：[[Platform Team Management]]

## Core Concepts

**Why Istio Exists（解决的痛点）**
- K8s Service only provides basic L4 load balancing and service discovery; with dozens of microservices, without Istio: no canary releases, no rate limiting or circuit breaking, no encrypted service-to-service communication, troubleshooting relies on guesswork
- Istio delivers three capabilities: **Observability** + **Traffic Control** + **mTLS encryption** （可观测 + 可控制 + 可加密）

**Sidecar Injection Mechanism（注入机制）**
- Leverages the fact that containers within a Pod share a Network Namespace: injects an **Envoy Sidecar container** into every Pod so all inbound/outbound traffic passes through Envoy — the business container is completely unaware （业务容器无感知）
- Injection method: **Mutation Webhook** — at Pod creation time, Envoy is automatically inserted into the spec; no changes to Deployment YAML needed
- Traffic interception: **iptables rules** forcibly redirect all traffic to Envoy's listening port (the underlying traffic hijacking mechanism) （流量劫持底层机制）

**Istiod Architecture — Control Plane vs Data Plane（控制面与数据面）**
- **Istiod** = Control Plane: reads user-written Istio specs → actively pushes config to every Envoy (xDS protocol over gRPC long-lived connections) （主动推送，非 Envoy 轮询）
- **Envoy** = Data Plane: executes traffic control, collects traces, handles mTLS encryption/decryption; behavior is orchestrated by Istiod, not self-determined

**Core Config Objects（核心配置对象）**
- **Gateway**: manages East-West (intra-cluster) traffic ingress (vs Kubernetes Ingress which manages North-South / external traffic) （东西流量入口）
- **VirtualService**: defines routing rules (90/10 traffic split, timeouts, retries) （路由规则）
- **DestinationRule**: defines destination policies (subset definition, circuit breaking, fault injection); subsets are distinguished by Pod Labels (e.g., `version: v1`)
- A/B testing: VirtualService defines traffic ratios + DestinationRule defines subsets; fault injection: DestinationRule fault field (abort/delay)

**mTLS Security（双向 TLS）**
- **mTLS (Mutual TLS)**: standard TLS has only the client verifying the server; mTLS adds server-verifying-client — both encryption and mutual authentication （双向验证）
- Istiod centrally issues and manages certificates, auto-distributes, and auto-renews before expiry — business code is completely unaware
- Certificates contain ServiceAccount + Pod identity and have extremely short TTLs (minute-level), minimizing the window of exposure if leaked

**Observability — Distributed Tracing（分布式追踪）**
- Envoy natively collects latency, error rate, and traffic volume for all flows — no business code changes required
- **Trace ID** (unique per full request chain) propagates via HTTP Header at every hop; **Span ID** (unique per hop) records that segment's latency and status （全链路唯一标识）
- Envoy auto-forwards Trace IDs; creates a new one if none exists; protocol misconfiguration (e.g., gRPC configured as HTTP) breaks the Trace ID chain

**Performance Cost and Ambient Mesh（性能开销与新架构）**
- Sidecar adds 2 extra Envoy hops per request (egress + ingress), adding ~10+ ms latency; Envoy is single-threaded by default, causing CPU spikes under high concurrency
- **Ambient Mesh**: eliminates per-Pod Sidecar, replaced by two layers:
  - **ztunnel** (Node-level, one per Node): handles L4 (mTLS, basic encryption) （每节点一个）
  - **Waypoint** (Namespace-level, on-demand): handles L7 (advanced traffic control)
  - ztunnel count scales with Node count (not Pod count), dramatically reducing resource consumption; no Waypoint = no L7 features

## Key Questions

**Q: K8s already has Service — why do you need Istio?**
Answer framework: Service only does L4 basic routing; Istio provides L7 fine-grained traffic control (A/B testing, Header-based routing, fault injection) + mTLS zero-trust + distributed tracing; three pain points at microservice scale — no canary, no encryption, debugging by guesswork — Istio solves all three.
> 中文提示：Service = L4 基础路由；Istio = L7 精细控制 + mTLS 零信任 + 分布式追踪，三大痛点一套解决

**Q: How is a Sidecar inserted into a Pod? Does the business container notice?**
Answer framework: Mutation Webhook auto-injects the Envoy container (modifies Pod spec at creation time); iptables rules hijack all traffic; the business container is completely unaware; same Webhook mechanism as K8s Control Plane — this is how Istio integrates deeply with the K8s ecosystem.
> 中文提示：Mutation Webhook 注入 + iptables 劫持流量；业务容器完全无感知

**Q: What is the difference between Istio Gateway and K8s Ingress?**
Answer framework: Ingress = North-South traffic (external requests entering the cluster); Gateway = East-West traffic (internal service-to-service); complementary, not mutually exclusive; large microservice architectures use both — Ingress for external, Istio Gateway + VirtualService for internal routing.
> 中文提示：Ingress 管南北流量（外部进入），Gateway 管东西流量（内部互通）；两者互补

**Q: Does mTLS require the business code to manage certificates? How is security guaranteed?**
Answer framework: No — Istiod fully manages (issuance, distribution, renewal); security comes from: ① Istiod-signed certificates cannot be forged; ② certificates contain ServiceAccount (proof of identity); ③ short-lived (minute-level TTL), small exposure window if leaked; four lines of YAML enable Strict mTLS mode.
> 中文提示：Istiod 全托管；安全性三层：不可伪造 + 身份证明 + 短期有效；业务代码零改动

**Q: Sidecar mode vs Ambient Mesh — how do you choose?**
Answer framework: Sidecar = simple, full-featured, works out of the box — good for getting started and mid-scale; Ambient = resource-efficient (ztunnel count = Node count, vs Sidecar count = Pod count) — suited for large-scale teams with deep operational expertise; Ambient's L7 features require Waypoint and are still maturing — evaluate carefully before adopting.
> 中文提示：Sidecar 开箱即用；Ambient 大规模资源高效但 L7 功能仍在完善；按团队规模和运维能力选择

**Q: How does distributed tracing correlate the same request across multiple services?**
Answer framework: Trace ID propagates via HTTP Header at each hop; Envoy auto-handles (forwards existing or creates new); Span ID records per-hop latency; protocol misconfiguration (gRPC vs HTTP) causes Header format incompatibility and breaks the Trace chain — this is a common Istio production debugging pitfall.
> 中文提示：Trace ID 通过 HTTP Header 传递；协议配错（gRPC vs HTTP）导致 Header 不兼容，Trace 断链是生产常见坑

## Summary

Istio's core value is extracting cross-cutting concerns of microservice governance (security, observability, traffic control) from business code and pushing them down into the infrastructure layer. The Sidecar pattern leverages K8s's multi-container shared Network Namespace, combined with Mutation Webhook auto-injection, achieving zero business code changes. Istiod centrally manages config distribution and certificate lifecycle for all Envoy instances — it is the central nervous system of the entire setup.

From an AI Infra perspective, Istio's primary value scenarios are: multi-model service traffic management (A/B testing different model versions), mTLS protecting model API service-to-service communication, and request-level observability for GPU workloads via Envoy metrics collection. For AI inference clusters, the Sidecar-introduced latency (~10+ ms) must be weighed against observability benefits; latency-sensitive paths may bypass Istio or adopt Ambient Mesh to reduce overhead.

> 面试重点：Sidecar 注入机制（Webhook + iptables）→ Istiod 控制面架构 → mTLS 零信任 → Sidecar vs Ambient 选型 trade-off

## Raw Material
- [[raw_material/tech/infra/k8s-istio-table]]
