---
title: K8s Istio / Service Mesh 复习
source: internal
date_saved: 2026-04-06
processed: true
skill_note: "[[skills/tech/infra/Service Mesh and Istio]]"
---

# K8s Istio / Service Mesh 复习

> 覆盖主题：为什么需要 Istio → Sidecar 注入机制（Mutation Webhook / iptables / Envoy）→ Istiod 架构（Control Plane / Data Plane）→ 核心对象（VirtualService / DestinationRule / Gateway）→ mTLS 安全 → 可观测性（Trace ID / Span ID）→ 性能开销 → Ambient Mesh（ztunnel / Waypoint）

---

## 一、为什么需要 Istio

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 1 | 有了 Kubernetes Service，为什么还需要 Istio？ | Service 只能做基本负载均衡和服务发现；Istio 提供**精细化流量控制**：A/B 测试、按比例分流、故障注入、请求验证等 Service 做不到的能力 | Service = 基础路由；Istio = 精细流量控制 |
| 2 | Istio 解决的核心痛点是什么？ | 几十个微服务互相调用时，**没有 Istio**：无法灰度发布、无法限流熔断、服务间通信无加密、排查故障靠猜；**有了 Istio**：流量可观测、可控制、可加密 | 可观测 + 可控制 + 可加密 |

---

## 二、Sidecar 注入机制

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 3 | Istio 是怎么"插入"到服务通信链路中的？ | 利用 Pod **多容器共享网络**的特性，向每个 Pod 注入一个 **Sidecar 容器（Envoy Proxy）**，所有进出流量先经过 Envoy，业务容器完全无感知 | Sidecar = 共享网络命名空间的代理容器 |
| 4 | Sidecar 是怎么自动注入到 Pod 里的？ | 通过 **Mutation Webhook**：Istio 注册 Webhook，Pod 创建时自动往 spec 里插入 Envoy Sidecar 容器，无需手动修改每个 Deployment yaml | Mutation Webhook = 自动注入 Sidecar |
| 5 | Sidecar 是怎么拦截流量的？业务容器自己的端口不会冲突吗？ | 通过 **iptables 规则**强制把所有进出流量重定向到 Envoy 监听的端口；业务容器完全不知情，流量已在到达业务容器前被劫持 | iptables = 流量劫持底层机制 |

---

## 三、Istiod 架构（Control Plane / Data Plane）

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 6 | Envoy 的行为是它自己决定的，还是有人在指挥？ | 有 **Istiod** 统一指挥：开发者写 Istio spec → Istiod（Control Plane）读取并下发配置 → 每个 Pod 里的 Envoy（Data Plane）执行 | Istiod = Control Plane；Envoy = Data Plane |
| 7 | Istiod 是怎么把配置推送给 Envoy 的？ | **Istiod 主动推送**给每个 Envoy，不是 Envoy 轮询；使用 xDS 协议（gRPC 长连接）实时下发路由、监听器、端点配置 | Istiod 推送，非 Envoy 轮询 |

---

## 四、核心配置对象

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 8 | Istio 的三个核心 spec 对象分别是什么？ | **Gateway**：管理进入集群的流量入口；**VirtualService**：定义流量路由规则（如 90/10 分流）；**DestinationRule**：定义目标服务策略（如故障注入、熔断、超时） | Gateway / VirtualService / DestinationRule |
| 9 | A/B 测试（90% v1，10% v2）用哪个对象？ | **VirtualService**：定义流量比例；配合 **DestinationRule** 的 subset（通过 Pod Label 如 `version: v1` / `version: v2` 区分实例） | VirtualService = 分流规则；Label = subset 依据 |
| 10 | 故障注入（模拟服务随机 500 错误）用哪个对象？ | **DestinationRule**（或 VirtualService 的 fault 字段）：配置 abort / delay，模拟服务异常来测试系统韧性 | DestinationRule fault = 故障注入 |
| 11 | Istio Gateway 和 Kubernetes Ingress 是什么关系？ | 互补而非替代：**Ingress** 管集群**外部进来**的流量（North-South）；**Istio Gateway** 管集群**内部服务间**的流量（East-West） | Ingress = 南北流量；Gateway = 东西流量 |

---

## 五、mTLS 安全

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 12 | mTLS 是什么？和普通 TLS 有什么区别？ | **mTLS（双向 TLS）**：普通 TLS 只有客户端验证服务端；mTLS 双方都要验证对方身份，加密通信 + 双向认证 | 双向 = 两边都验证身份 |
| 13 | mTLS 需要开发者自己管理证书吗？ | 不需要，**Istiod 统一签发和管理证书**：自动分发、到期前自动续期，业务代码零感知 | Istiod = 统一证书颁发机构（CA） |
| 14 | 服务 A 如何确认它在和真正的服务 B 通信，而不是冒充者？ | Istiod 签发的证书中包含了 **Service Account + Pod 信息**，且**过期时间很短**（分钟级）；证书由 Istiod 背书，无法伪造，泄露后窗口期极小 | 证书 = 身份 + 短期有效 = 无法冒充 |

---

## 六、可观测性（Distributed Tracing）

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 15 | Istio 是怎么自动收集服务间调用数据的？ | 所有流量都经过 Envoy，**Envoy 天然可以采集**延迟、错误率、流量量等指标，无需业务代码改动 | Envoy = 天然的可观测性采集点 |
| 16 | 分布式追踪（A → B → C）怎么知道是同一个请求链路？ | **Trace ID**（全链路唯一标识）通过 **HTTP Header** 在每一跳中传递；**Span ID**（每一跳的唯一标识）记录该段调用的延迟和状态 | Trace ID = 全链路 ID；Span ID = 单跳 ID |
| 17 | 服务 B 收到请求后调用服务 C，Trace ID 需要业务代码手动传递吗？ | **不需要**，Envoy 自动转发 Trace ID；如果收到的请求没有 Trace ID，Envoy 自动创建新的，保证每个请求都被追踪 | Envoy 自动传递 / 自动创建 Trace ID |
| 18 | 协议配置错误（如 gRPC 服务配成了 HTTP）会怎样？ | **Trace ID 断链**（Header 格式不兼容），追踪链路断裂；L7 流量规则也可能失效。需要 Istiod 正确配置协议类型 | 协议配错 = 追踪断链 + 规则失效 |

---

## 七、性能开销与常见坑

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 19 | Istio 引入后最常见的问题是什么？ | **性能开销**（延迟 + CPU/内存）+ **调试困难**（多了 Envoy 这一层，排查问题链路更长） | 性能开销 + 调试复杂度 |
| 20 | Sidecar 带来的延迟开销有多大？ | 每个请求多经过两跳 Envoy（出口 + 入口），额外延迟约 **十几 ms**；高并发场景下影响更明显 | 每请求 +2 跳 Envoy ≈ 十几 ms |
| 21 | Sidecar 的 CPU / 内存开销如何？ | Envoy **默认单线程**，高并发时 CPU 容易 spike；内存消耗与 Pod 数量成正比，每个 Sidecar 约几十 MB，Pod 多了总量可观 | Envoy 单线程 CPU spike；内存随 Pod 数线性增长 |

---

## 八、Ambient Mesh

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 22 | Ambient Mesh 是什么？为什么要去掉 Sidecar？ | 新模式：把 Sidecar 的职责拆分到两层，**去掉每个 Pod 内置 Sidecar** 的模式，大幅降低资源消耗 | 去 Sidecar 化 = 降低资源消耗 |
| 23 | Ambient Mesh 的两层架构分别是什么？ | **ztunnel**（Node 级别，每 Node 一个）：处理 L4，负责 mTLS 和基本流量加密；**Waypoint**（Namespace 级别，按需部署）：处理 L7，负责高级流量控制 | ztunnel = L4；Waypoint = L7 |
| 24 | Ambient Mesh 如何节省资源？ | ztunnel 数量只跟 **Node 数量**有关（而非 Pod 数量）；Waypoint 按需部署，不是每个服务都必须有 | Node 数 << Pod 数，资源消耗大幅降低 |
| 25 | 没有部署 Waypoint 的服务还能用 A/B 测试等 L7 功能吗？ | **不能**，L7 功能依赖 Waypoint；只有 L4 的 mTLS 和基本加密可用 | 无 Waypoint = 无 L7 功能 |
| 26 | 从 Sidecar 模式迁移到 Ambient Mesh 难吗？ | **基本平滑**，不需要大改配置；但有一定改动，且 Ambient Mesh 要求团队对 Istio 理解更深，L7 高级功能仍在完善中 | 平滑迁移，但需要团队能力支撑 |
| 27 | Sidecar 模式 vs Ambient Mesh 怎么选？ | **Sidecar**：简单、功能完整、开箱即用，适合入门和中等规模；**Ambient Mesh**：资源高效，适合大规模和有深度运维能力的团队，L7 功能仍在完善，建议谨慎观望 | Sidecar = 简单全功能；Ambient = 高效但复杂 |

---

## 九、术语速查

| 术语 | 一句话解释 |
|------|-----------|
| **Istio** | Kubernetes 上的 Service Mesh，提供精细流量控制、安全、可观测性 |
| **Sidecar** | 注入到每个 Pod 的代理容器（Envoy），与业务容器共享网络命名空间 |
| **Envoy** | Sidecar 的具体实现，执行流量控制、追踪采集、mTLS 加解密 |
| **Istiod** | Istio 的 Control Plane，读取用户配置并推送给每个 Envoy |
| **Mutation Webhook** | Istio 用来自动向 Pod 注入 Sidecar 的机制 |
| **iptables** | Sidecar 拦截流量的底层 Linux 机制，强制重定向所有进出流量 |
| **VirtualService** | 定义流量路由规则，如 90/10 分流、超时、重试 |
| **DestinationRule** | 定义目标服务策略，如 subset 划分、熔断、故障注入 |
| **Gateway** | 管理集群内部服务间（East-West）的流量入口 |
| **subset** | DestinationRule 中通过 Pod Label 划分的服务版本分组 |
| **mTLS** | 双向 TLS，服务双方互相验证身份 + 加密通信 |
| **Trace ID** | 分布式追踪中全链路唯一标识，经 HTTP Header 在各服务间传递 |
| **Span ID** | 分布式追踪中单跳调用的唯一标识，记录该段延迟和状态 |
| **Ambient Mesh** | 新模式：去掉 Pod 内 Sidecar，改用 ztunnel（L4）+ Waypoint（L7） |
| **ztunnel** | Ambient Mesh 中 Node 级别的 L4 代理，每个 Node 一个 |
| **Waypoint** | Ambient Mesh 中 Namespace 级别的 L7 代理，按需部署 |
| **North-South 流量** | 集群外部进出的流量，由 Kubernetes Ingress 管理 |
| **East-West 流量** | 集群内部服务间的流量，由 Istio Gateway 管理 |
