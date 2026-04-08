---
title: Kubernetes GPU 调度手册 — 第一部分：基础认知与问题定义
source: https://jimmysong.io/zh/book/gpu-infra/fundamentals/
date_saved: 2026-04-08
processed: true
skill_note: "[[skills/tech/ai-infra/Kubernetes GPU Scheduling]]"
book: "Kubernetes 中的 GPU 调度与虚拟化手册"
book_url: https://jimmysong.io/zh/book/gpu-infra/
chapters_included:
  - "GPU 基础认知 — 从硬件到 Kubernetes"
  - "GPU 异构生态导引"
  - "GPU 资源治理为什么难"
  - "GPU 资源控制面地图"
  - "GPU 平台能力模型"
  - "K8s 设备资源模型"
  - "GPU 评估决策轴"
---

# 第一部分：基础认知与问题定义

## GPU 基础认知 — 从硬件到 Kubernetes

核心命题：GPU 不是"更快的 CPU"，而是面向吞吐量计算的工程范式转变。

**五类硬件组件**决定基础设施约束：
- 计算单元（SM / Tensor Core）
- 显存（HBM / GDDR）
- 片上缓存（L2 / Shared Memory）
- 互联（PCIe / NVLink / NVSwitch）
- 驱动与固件

**显存 vs 算力的关键区别**：
- 显存：硬约束，存在碎片化，需要连续分配，绑定进程生命周期
- 算力：软约束，可时间片共享，主要影响速度而不是可执行性
- → "Compute is soft constraint, memory is hard constraint"

**Kubernetes 边界**：K8s 仅管理节点级 Pod 放置，GPU 内部资源治理（显存分配、算力公平、干扰管理）需要额外插件、运行时机制或数据平面方案。

## GPU 异构生态导引

国内 GPU 厂商分层：
- **一线**：华为昇腾（910, CANN）、寒武纪 MLU、沐曦"曦云"C500/C550（声称 A100 级别）、天数智芯"大岛"
- **二线**：摩尔线程、壁仞科技、燧原科技、百度昆仑
- 国际：NVIDIA（CUDA 事实标准）、AMD（ROCm）、Intel（oneAPI）
- 专用：Groq（亚毫秒推理）、Cerebras（晶圆级）、Graphcore（IPU）

Kubernetes 集成成熟度：只有一线厂商达到生产级 K8s 成熟度，其他依赖 HAMi 等社区方案。

## GPU 资源治理为什么难

GPU 资源的三个根本属性使治理困难：
1. **强状态性**（Stateful）
2. **紧耦合性**（多维度资源必须同时满足）
3. **多维性**（显存 + 算力 + 拓扑同时约束）

**不可能三角**：利用率 / 隔离保障 / 性能可预测性，三者不可兼得。

K8s Device Plugin 假设"离散可分配资源"，但 GPU 分配需要连续变量优化——调度器无法感知"剩余显存"或"带宽争用"，产生根本的语义鸿沟。

**典型失效模式**：
- 平均指标良好但 P99 崩溃
- 显存看似充足但 OOM（碎片化）
- 相同配额产生截然不同的性能
- 调度成功但吞吐不可接受

## GPU 资源控制面地图

**正交分工**（核心认知）：
- **控制面**：治理层——谁能用、何时能用、能用多少、什么优先级（Kueue、Volcano）
- **数据平面**：资源兑现层——GPU 如何被暴露、切分、隔离、计量（MIG、HAMi、Device Plugin）

五层控制面架构：
- Layer 0：工作负载单元（粒度与原子性）
- Layer 1：入口治理（配额与准入）→ Kueue
- Layer 2：全局调度策略 → Volcano
- Layer 3：K8s 编排闭环（Pod 生命周期）
- Layer 4：节点分配与设备交付（控制面↔数据平面接口）

三种典型架构范式：
- 范式 A（原生 K8s）：最小化，适合小规模单团队
- 范式 B（Volcano）：作业级策略 + Gang 调度，适合训练/批处理
- 范式 C（Kueue）：显式化等待/准入/抢占，适合多租户

## GPU 平台能力模型（四层）

- **L0 Primitives**：可观测的资源单元（显存、算力、带宽、健康指标）
- **L1 Foundations**：配额、准入、抢占、隔离剖面、性能层级
- **L2 Capabilities**：面向业务的交付单元（GPU 超卖、优先级抢占、弹性伸缩、Turbo 模式、资源配额、显存分析、可观测性）
- **L3 Solutions**：多能力组合（云租赁、潮汐推理、共享资源池）

能力成熟度三阶段：demo-ready → acceptance-ready（有可验收指标）→ production-ready（有运营防护）

## K8s 设备资源模型

K8s 使用 **Extended Resources** 作为标量整数计数器（`nvidia.com/gpu: 1`），调度器仅做整数匹配，对 MIG 剖面、时间片策略、具体 GPU 身份一无所知。

Device Plugin 三阶段：
1. **Advertise**：插件上报可用设备为 Extended Resource
2. **Bind**：调度器将 Pod 分配到节点
3. **Allocate**：kubelet 从插件获取具体设备 ID，准备挂载/环境变量

三大原生局限：
1. 连续资源维度（显存、带宽、拓扑）无法用单一整数表达
2. 共享不是一等公民——K8s 交付离散设备，多租户 GPU 需要数据平面 workaround
3. 节点本地复杂性（驱动兼容、MIG 重配、CUDA 运行时差异）在分配时暴露，而非调度时

**演进路径**：Device Manager → **DRA（Dynamic Resource Allocation）**：将设备选择从 kubelet 的不透明 Allocate 阶段迁移到调度器可见的声明式 ResourceClaim 对象，支持参数化请求。

## GPU 评估决策轴（十维框架）

| 维度 | 关注点 |
|------|-------|
| 资源单位 | 整卡/MIG 实例/时间片副本/vGPU/Claims 的粒度 |
| 隔离强度 | 故障、显存、性能边界 |
| 尾延迟风险 | 共享场景下 P99 可预测性 |
| 性能开销 | 上下文切换、虚拟化、框架成本 |
| 控制面治理 | 准入、配额、公平性、抢占能力 |
| 兼容性 | Pod spec 稳定性、厂商锁定、侵入性 |
| 运维成本 | 重配置负担与变更窗口 |
| 可观测性与计量 | 设备遥测与工作负载归因 |
| 失效模式 | 可调试性与根因清晰度 |
| 演进路径 | 多厂商支持与参数化请求 |

先用门槛维度（P99、可观测性、可扩展性）排除不适选项，再按工作负载模式（推理 vs 训练）加权评分。
