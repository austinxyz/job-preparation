---
title: Kubernetes GPU Scheduling and Virtualization
category: tech/ai-infra
tags: [gpu, kubernetes, scheduling, mig, hami, volcano, kueue, vllm, distributed-training]
status: in-progress
priority: high
last_updated: 2026-04-08
created_from_jd: false
---

# Kubernetes GPU Scheduling and Virtualization

> Source: Jimmy Song — *Kubernetes 中的 GPU 调度与虚拟化手册*
> https://jimmysong.io/zh/book/gpu-infra/

## Knowledge Map

- Prerequisites（前置知识）：[[Kubernetes]], [[GPU Cluster Management]], [[NCCL Collective Communication]]
- Related Topics（延伸话题）：[[MIG Multi-Instance GPU]], [[DCGM GPU Monitoring]], [[Distributed Training Frameworks]], [[Slurm Workload Manager]]
- Tools covered：[[Volcano]], [[Kueue]], [[HAMi]], [[vLLM]], [[DRA Dynamic Resource Allocation]]

---

## Core Concepts

### 基础认知

- **GPU ≠ 更快的 CPU**：GPU 是面向吞吐量计算的范式转变，牺牲控制流灵活性换取极端吞吐密度。五类硬件组件决定基础设施约束：SM/Tensor Core、HBM/GDDR（显存）、L2/Shared Memory、PCIe/NVLink/NVSwitch（互联）、驱动与固件。
- **显存 vs 算力的核心区别**：显存是硬约束（存在碎片化，需要连续分配，绑定进程生命周期）；算力是软约束（可时间片共享，影响速度不影响可执行性）。**"Compute is soft constraint, memory is hard constraint."**
- **K8s 原生边界**：K8s 仅管理节点级 Pod 放置，GPU 内部资源治理（显存分配、算力公平、干扰管理）需要额外插件或数据平面方案。
- **GPU 治理不可能三角**：利用率 / 隔离保障 / 性能可预测性，三者不可兼得——这是所有设计决策的根本张力。
- **典型失效模式**：平均指标良好但 P99 崩溃；显存看似充足但 OOM（碎片化）；相同配额产生截然不同的性能；调度成功但吞吐不可接受。

### K8s 设备资源模型

- **Extended Resources**：标量整数计数器（`nvidia.com/gpu: 1`），调度器做整数匹配——对 MIG 剖面、时间片策略、具体 GPU 身份一无所知。
- **Device Plugin 三阶段**：Advertise（上报设备）→ Bind（调度器分配节点）→ Allocate（kubelet 获取具体设备 ID，准备挂载/环境变量）。
- **三大原生局限**：(1) 连续资源维度（显存、带宽、拓扑）无法用单一整数表达；(2) 共享非一等公民；(3) 节点本地复杂性在分配时暴露，而非调度时。
- **演进路径 DRA**：Dynamic Resource Allocation 将设备选择迁移到调度器可见的声明式 ResourceClaim 对象，支持参数化请求——取代 kubelet 的不透明 Allocate。
- **责任分工**：控制面（调度器）决定"Pod 放哪"；数据平面（kubelet + Device Manager + Device Plugin）决定"哪个具体设备、如何交付"。

### 控制面 vs 数据平面（最重要的认知分层）

- **控制面**：治理层——谁能用、何时能用、能用多少、什么优先级（Kueue、Volcano）
- **数据平面**：资源兑现层——GPU 如何被暴露、切分、隔离、计量（MIG、HAMi、Device Plugin）
- 两层**正交**，可独立替换，可组合——先定位层级再评估方案，避免跨层比较。

### 数据平面技术谱系

- **五种共享机制**（强隔离 → 软约束）：独占直通 → MIG（硬分区）→ vGPU（中介虚拟化）→ 时间切片 → MPS（并发优化）
- **MIG**：硬件级隔离（独立显存系统路径 + L2 缓存组隔离），资源单位离散（预定义剖面）。两大代价：资源碎片化（内部碎片 + 组合碎片 + 集群级倾斜）+ 重配置开销（需零工作负载，往往要 cordon/drain）。**推荐策略**：将 MIG 几何形状作为节点池属性固化，用亲和性路由匹配，而非动态重配置。
- **HAMi**：声明式 GPU 共享数据平面。四层分配链：设备发现上报 → 调度扩展 → 容器级算力/显存配额执行 → Prometheus 可观测性。提供"比整卡分配更好的治理"（策略层），而非"MIG 级硬件分区"（硬隔离层）。
- **时间切片**：超卖灵活，但引入调度干扰和尾延迟风险，不适合有 SLO 要求的推理。

### 控制面工具

- **Volcano**：批处理语义 + Gang 调度引擎。核心能力：Gang 调度（全有或全无）、Backfill（小作业填隙）、抢占（优先级驱逐）、DRF 公平份额、拓扑亲和性。**不处理** GPU 虚拟化或隔离。
- **Kueue**：资源治理与准入控制。两阶段调度：先准入（LocalQueue → ClusterQueue 配额检查），再调度。核心组件：LocalQueue（团队入口）、ClusterQueue（全局资源池）、Workload（可管理单元）、ResourceFlavor（差异化资源类型）。
- **Volcano vs Kueue**（正交互补）：Volcano = "如何排座位"（Gang 调度、批处理语义）；Kueue = "谁能进场、能占多少"（准入、配额治理）。生产集群通常两者并用。

### 六种参考架构（从简到复杂）

| 方案 | 数据平面 | 控制面 | 适用 |
|------|----------|--------|------|
| A | 整卡 | 单队列 | 最小可行闭环 |
| B | 整卡 | Kueue 多队列 | 引入公平治理 |
| C | MIG | Kueue | 强隔离 + 细粒度 |
| D | HAMi | Kueue | 高利用率 + 声明共享 |
| E | 整卡/HAMi | Kueue + Volcano | 训练语义增强 |
| F | 双池（在线/离线） | 分域管理 | 在线离线隔离 |

演进建议：Phase 1（A→B 建立秩序）→ Phase 2（→C/D 引入粒度）→ Phase 3（→E/F 平台成熟）

### 工作负载：推理（vLLM）

- **核心张力**：吞吐优化（平均收益）vs 尾延迟（最坏情况），两者非线性对立，根源在 KV cache 显存压力 + 排队方差。
- **Goodput > tokens/s**：SLO 合规的吞吐才是真实容量指标，原始 tokens/s 会误导。
- **验收四维度**（需 P50/P95/P99 分布）：TTFT（首 token 时间，反映队列健康）、TPOT（每输出 token 时间，反映生成稳定性）、Throughput + Goodput、Reliability（拒绝/OOM/重试率）。
- **高风险配置**：显存利用率过高 + 高并发（碎片级联）；混合负载无队列隔离（短请求被长请求阻塞）；无界上下文长度（罕见超长序列破坏全局稳定）。

### 工作负载：训练（PyTorch 分布式）

- **训练资源四大特性**：连续性（跨小时/天）、同步通信（DDP/FSDP 集合操作对拓扑敏感）、刚性资源单位（需特定数量和拓扑）、耦合约束（显存/IO/算力多维权衡）。
- **五种必需调度语义**：Min-Available、Gang 调度、拓扑感知（同节点 > 同机架 > 跨域）、可抢占性分层、Suspend/Resume。
- **抢占真实代价**：重启开销 + 回滚损失（checkpoint 频率决定恢复代价）+ 系统抖动（级联中断降低实际吞吐）。
- **核心洞察**："你优化的不是 GPU 可用性，而是在资源争用下的有效步数产出。"

### 可观测性体系

- **三级实施路径**：Level 0（nvidia-smi，1-2 天）→ Level 1（DCGM + Prometheus + Grafana，1-2 周）→ Level 2（完整可审计，分配/使用对账，1-2 月）。
- **六个核心指标定义**：已分配 vs 已使用 / 利用率 vs 饱和度 / 碎片化（剩余资源不匹配请求形状，而非简单"剩余少"）/ 队列等待时间 / 干扰系数 / 标准化 GPU-小时。
- **平台成熟度标准**：不是功能数量，而是"能解释资源行为、能治理分配决策、能按组织精度结算成本"。

### 评估决策框架

十维评估轴：资源单位粒度、隔离强度、尾延迟风险、性能开销、控制面治理能力、兼容性、运维成本、可观测性与计量、失效模式可调试性、演进路径。

**使用方法**：先用门槛维度（P99、可观测性、可扩展性）排除不适选项，再按工作负载模式（推理 vs 训练）加权评分。

---

## Key Questions

**Q: Kubernetes 的 Device Plugin 模型有什么根本局限？如何用 DRA 改进？**
Answer framework: Device Plugin 将 GPU 暴露为标量整数（`nvidia.com/gpu: 1`），调度器做整数匹配，无法感知显存余量、拓扑关系、MIG 剖面——这是语义鸿沟，不是实现缺陷。三大局限：(1) 连续资源维度（显存、带宽）无法表达；(2) 共享非一等公民，多租户需要数据平面 workaround；(3) 节点本地复杂性（驱动、CUDA 版本差异）在分配时才暴露。DRA 改进：将设备选择迁移到声明式 ResourceClaim，使调度器能感知设备类别和配置参数，实现参数化请求而非裸整数。

**Q: MIG 和 HAMi 各解决什么问题？在哪些场景选择哪个？**
Answer framework: MIG = 硬件级空间分区，提供真正的内存、缓存、SM 隔离，适合多租户推理（有 SLA 要求、需要 P99 保障、工作负载形状稳定）。代价：资源单位离散，重配置需要停工（cordon/drain），不支持动态弹性。HAMi = 软件层声明共享，将 GPU 拆分为可声明的算力分数和显存配额，适合快速提升利用率的共享推理和研究环境。代价：不提供 MIG 级硬隔离，干扰系数更高，SLO 稳定性弱于 MIG。决策轴：SLA 严格且负载稳定 → MIG；利用率优先且可容忍软隔离 → HAMi。

**Q: Volcano 和 Kueue 各自的定位是什么？为什么通常需要两者？**
Answer framework: 两者正交：Volcano 解决"如何排座位"——Gang 调度（全有或全无）、拓扑感知、批处理作业语义、Backfill，针对训练作业的执行编排；Kueue 解决"谁能进场、能占多少"——LocalQueue/ClusterQueue 配额治理、准入控制、ResourceFlavor 差异化、跨团队公平分配，针对多租户资源治理。Kueue 做准入决策在先，Volcano 做执行调度在后。生产集群同时需要两者的典型场景：多团队共享一个训练集群，既需要 Kueue 的配额公平（避免某团队独占），又需要 Volcano 的 Gang 调度（避免分布式训练部分启动）。

**Q: 如何评估一个 GPU 共享方案是否适合生产？**
Answer framework: 用十维评估轴，先用门槛维度排除。三个门槛维度：(1) P99 尾延迟 — 在共享场景下是否有明确的 P99 保障机制？(2) 可观测性 — 能否追溯"谁在用哪块 GPU、为什么性能下降"？(3) 可扩展性 — 节点数增加时操作复杂度如何变化？排除后，按工作负载模式加权：推理权重高于训练时，隔离强度和尾延迟风险权重大；训练权重高时，Gang 调度语义和拓扑感知权重大。最终需要实验验证：隔离基线 vs 非托管共享 vs 托管共享三组数据。

**Q: 推理平台的 SLO 如何定义和验收？光看 tokens/s 为什么不够？**
Answer framework: tokens/s 是吞吐的平均值，在高负载下会掩盖尾延迟崩溃。吞吐优化和尾延迟保障是对立的：continuous batching 提升平均吞吐，但短请求被长请求推迟，P99 TTFT 劣化。正确的 SLO 框架需要四维度：TTFT（P99 反映队列健康）、TPOT（P99 反映生成稳定性）、Goodput（SLO 合规的 tokens/s，不满足 SLO 的吞吐不计入）、Reliability（OOM/重试率是前置预警）。实际操作：在验收测试中，用三种并发级别（50%/80%/100% 目标负载）跑 P50/P95/P99 分布，设定明确阈值。

**Q: 分布式训练中的抢占代价是什么？如何设计抢占策略？**
Answer framework: 抢占代价分三层：(1) 重启开销——容器重启、权重下载（百 GB 级别）、NCCL 通信组重新初始化；(2) 回滚损失——从最近 checkpoint 重跑，checkpoint 频率决定损失窗口大小；(3) 系统抖动——频繁抢占触发级联中断，GPU 利用率显示很高但有效步数产出极低。设计原则：(a) 按类分层——关键训练（C 类，不可抢占）/ 重要训练（B 类，有 checkpoint 才可抢占）/ 实验训练（A 类，随时可抢占）；(b) Suspend/Resume 优于 Kill/Restart，保存训练状态比硬终止损失小；(c) 设置冷却期，避免触发器在无冷却机制下造成队列振荡；(d) checkpoint 频率与作业重要性挂钩，不能靠平台强制，需要作业配合。

**Q: 如何判断 GPU 集群的碎片化问题并解决？**
Answer framework: 碎片化的正确定义：剩余资源无法匹配典型请求形状，不只是"剩余显存少"。三种碎片类型：内部碎片（MIG 剖面大于实际需求）、组合碎片（剩余剖面组合无法满足新请求）、集群级碎片（不同节点的异构 MIG 几何形状导致调度器找不到合适节点）。诊断方法：观察调度成功率 vs 资源已分配率的比值；分析 Pending 队列里的请求形状分布；看 DCGM SM 利用率——分配高但利用低说明碎片严重。解决路径：(a) 对 MIG：固化节点池几何形状（同池同剖面）并用亲和性路由；(b) 对 HAMi 共享：调整粒度配置匹配主流请求形状；(c) 通用：引入 Backfill 调度 + 降级请求形状（请求多但接受少）。

**Q: 如何搭建 GPU 平台的可观测性体系？从零开始的优先级是什么？**
Answer framework: 三级路径，每级有明确验收标准。Level 0（1-2 天）：nvidia-smi 能回答"谁在用 GPU、利用率多少"——先把这两个问题答好，用于快速发现空闲 GPU 和确认作业运行；Level 1（1-2 周）：DCGM Exporter + Prometheus + Grafana——回答"为什么利用率低（碎片/排队/负载限制）、是否达到 SLO、邻居干扰从哪来"；Level 2（1-2 月）：分配/使用对账、标准化 GPU-小时计费、团队级成本报告——回答"如何按项目结算、容量缺口在哪"。最优先建立的指标：GPU UUID 到 Pod 的可追溯性（没有这个，所有其他分析都无从归因）。

---

## Summary

Kubernetes 上的 GPU 资源管理面临的根本挑战，不是 GPU 算力不够，而是 GPU 资源的多维度特性（显存硬约束 + 算力软约束 + 拓扑依赖）与 K8s 标量整数设备模型之间的语义鸿沟。原生 K8s 只能做节点级 Pod 放置，GPU 内部的共享、隔离、计量全部需要生态扩展。理解这个边界，是所有平台设计决策的起点。

最核心的架构认知是控制面与数据平面的正交分层。控制面（Kueue、Volcano）负责治理——谁能用、何时用、优先级如何；数据平面（MIG、HAMi、时间切片）负责资源兑现——GPU 如何被切分、隔离、计量。两层独立演进、可组合。常见错误是期望 Kueue 解决单节点利用率问题，或把 Volcano 当作虚拟化方案——这是跨层混淆。选型时，先定位目标问题在哪一层，再评估该层的方案。MIG 和 HAMi 不是竞争关系，而是不同强度的隔离选择：MIG 适合有严格 SLA 且负载形状稳定的多租户推理；HAMi 适合快速提升利用率、可接受软隔离的共享场景。

工作负载层面，推理和训练对平台的要求截然不同。推理（vLLM）的核心指标是 Goodput（SLO 合规吞吐）和 P99 尾延迟，而非原始 tokens/s——吞吐优化和尾延迟保障是对立的，平台需要通过资源契约（显存余量保留 + 并发序列上限 + 队列隔离）来守住尾延迟底线。训练（PyTorch 分布式）的核心是有效步数产出：Gang 调度防止部分启动浪费、拓扑感知避免跨域通信瓶颈、checkpoint + Suspend/Resume 降低抢占代价。衡量成功不是"GPU 启动了多少"，而是"在资源争用下产出了多少有效训练步"。可观测性是贯穿所有层的基础能力，没有 GPU UUID 到 Pod 的可追溯性，所有性能归因和成本结算都无从实现。

---

## Raw Material

- [[raw_material/books/gpu-infra/index]]
- [[raw_material/books/gpu-infra/01-fundamentals]]
- [[raw_material/books/gpu-infra/02-dataplane]]
- [[raw_material/books/gpu-infra/03-control-plane]]
- [[raw_material/books/gpu-infra/04-workloads]]
- [[raw_material/books/gpu-infra/05-observability]]
- [[raw_material/books/gpu-infra/06-landscape]]
