---
title: K8s Control Plane 复习
source: internal
date_saved: 2026-04-06
processed: true
skill_note: "[[skills/tech/infra/K8s Control Plane]]"
---

# K8s Control Plane 复习

> 覆盖主题：请求链路（kubectl apply → etcd → Controller Manager → Scheduler → kubelet）→ Webhook（Mutation / Validation）→ Container Runtime（CRI / containerd / namespace / cgroup）→ Resources（requests / limits / LimitRange）→ Control Plane 高可用（API Server 多实例 / Leader Election / etcd Raft Quorum）

---

## 一、请求链路

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 1 | `kubectl apply -f deployment.yaml` 请求首先由谁接收？ | **API Server**，做验证后再写入 etcd | API Server = Control Plane 统一入口 |
| 2 | API Server 主要验证哪些内容？ | **身份验证**（认证/授权/RBAC）+ **内容验证**（YAML 格式是否合法） | 认证 + 授权 + Schema 验证 |
| 3 | Deployment 写入 etcd 后，谁负责真正去创建 Pod？ | **Controller Manager** 下的 Deployment Controller 和 Pod Controller，通过 watch 机制比较 spec 和实际状态，发现差异则写入待调度 Pod | watch 机制 = 期望状态 vs 实际状态 |
| 4 | Deployment Controller 和 Pod Controller 是独立进程吗？ | 不是，都由 **Controller Manager** 统一管理 | Controller Manager = 所有 Controller 的容器 |
| 5 | Pod Controller 决定创建 Pod 后，它直接去 Node 上创建吗？ | 不是，只写入"待调度 Pod"到 etcd，由 **Scheduler** 决定放到哪个 Node | 解耦：Controller 写意图，Scheduler 做决策 |
| 6 | Scheduler 完成调度后，kubelet 如何得知需要创建 Pod？ | **API Server 主动推送**给 kubelet，不是 kubelet 轮询 | API Server 推送，非 kubelet 轮询 |
| 7 | 完整的请求链条是什么？ | `kubectl apply` → API Server → Mutation Webhook → Validation Webhook → etcd → Controller Manager → Scheduler → kubelet → Container Runtime → cgroup | 9 个环节，每组件只做一件事，通过 etcd 解耦 |

---

## 二、Webhook

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 8 | Mutation Webhook 和 Validation Webhook 的区别？ | **Mutation** = 修改请求（补默认值）；**Validation** = 验证请求（不符合则拒绝） | Mutation = 改；Validation = 审 |
| 9 | 两种 Webhook 在请求链条中的顺序？ | API Server 基本验证 → **Mutation Webhook（改）** → **Validation Webhook（验）** → 写入 etcd | 先改后验证，最终写入内容符合规范 |
| 10 | Validation Webhook 验证的是改之前还是改之后的内容？ | **改之后**（先 Mutation 再 Validation） | 保证 etcd 里存的是经过修改且验证通过的内容 |

---

## 三、Container Runtime

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 11 | kubelet 是直接调用 Docker 创建容器吗？ | 不是，通过 **CRI（Container Runtime Interface）** 接口调用 Container Runtime | CRI = K8s 与容器技术之间的抽象层 |
| 12 | 常见的 Container Runtime 有哪些？ | **containerd**、**CRI-O** | containerd 最主流；CRI-O 更轻量 |
| 13 | containerd 和 Docker 的关系？ | containerd 是从 Docker 剥离出来、捐赠给 CNCF 的，只专注**容器生命周期管理**；Docker 是包含构建、分发、运行的**全家桶方案** | containerd ⊂ Docker（功能子集） |
| 14 | K8s "弃用 Docker" 弃的是什么？ | 弃用的是 **dockershim**（Docker 整体方案作为 runtime），不是弃用镜像格式，开发者仍可用 Docker 构建镜像 | 弃 dockershim，不弃镜像格式 |
| 15 | 容器底层依赖 Linux 的什么机制？ | **namespace**（隔离网络、存储、进程等资源）+ **cgroup**（限制 CPU、内存等计算资源） | namespace = 隔离；cgroup = 限制 |
| 16 | 容器和虚拟机隔离的本质区别？ | 虚拟机是**操作系统级隔离**（更强）；容器是**线程级隔离**，共用宿主机操作系统（更轻但隔离性弱） | VM = OS 级隔离；容器 = 进程级隔离 |

---

## 四、Resources / cgroup

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 17 | `requests` 和 `limits` 的区别？ | `requests`：**Scheduler 调度依据**，保证 Pod 一定能拿到的资源；`limits`：**cgroup 强制硬上限** | requests = 调度保证；limits = 运行上限 |
| 18 | 超过 `limits` 会怎样？ | **CPU 超限**：限流（throttle）；**内存超限**：OOM，容器被杀 | CPU throttle；内存 OOM Kill |
| 19 | `limits`/`requests` 底层由谁执行？ | **containerd** 把这两个值翻译成 cgroup 配置，为每个 container 建立单独 cgroup 目录 | containerd → cgroup 目录 |
| 20 | Pod 不设置 requests 会怎样？ | Scheduler 无参考依据，可能把过多 Pod 塞到同一 Node；Node 内存不足时**优先杀这类 Pod** | 无 requests = 随意调度 + 优先被驱逐 |
| 21 | Pod 不设置 limits 会怎样？ | Pod 可无限消耗 CPU/内存，有 bug 时可能**打垮整个 Node**，影响所有邻居 Pod | 无 limits = 噪邻居风险 |
| 22 | 如何强制要求 Pod 必须设置 requests/limits？ | **LimitRange** 对象（不符合则拒绝创建） | LimitRange = 强制门槛 |
| 23 | 如何为忘记设置的 Pod 自动补默认值？ | **Mutation Webhook**（自动补默认值，兜底） | Mutation Webhook = 自动兜底 |

---

## 五、Control Plane 高可用

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 24 | API Server 多实例时，一个挂掉集群还能工作吗？ | 能继续工作，但**部分写操作功能可能受影响**；API Server 无状态，多实例天然高可用 | API Server 无状态 = 多实例简单高可用 |
| 25 | Controller Manager 多实例时，如何防止重复操作？ | **Leader Election**：只有 Leader 实例干活，其他实例待命 | Leader Election = 只有一个实例在工作 |
| 26 | Controller Manager Leader Election 用的是什么机制？ | **API Server 的 Lease 锁**（不是 etcd/Raft），Leader 定期续约，挂掉后锁过期，其他节点抢锁成为新 Leader | Lease 锁 = 定期续约，到期自动释放 |
| 27 | etcd 高可用用的是什么算法？ | **Raft 算法**，保证多节点间数据强一致性 | Raft = 分布式共识算法 |
| 28 | Raft 的 Quorum 是多少？作用是什么？ | **n/2 + 1**（多数派），只要 Quorum 节点存活，集群就能正常工作；防止脑裂，保证强一致性 | Quorum = n/2+1 = 多数派原则 |
| 29 | 5 个 etcd 节点，挂掉 2 个能否正常工作？挂掉 3 个呢？ | 挂掉 2 个：**能**，剩余 3 个 ≥ Quorum（3）；挂掉 3 个：**不能**，剩余 2 个 < Quorum（3） | 5 节点容忍 2 个挂掉 |
| 30 | 为什么推荐奇数个节点（3、5），而不是偶数（4、6）？ | 4 个节点容错能力与 3 个相同（都只能容忍 1 个挂掉），且 4 个节点可能出现 **2+2 脑裂**；奇数节点从根本上避免平票，成本更低 | 偶数 = 浪费成本 + 脑裂风险 |

---

## 六、术语速查

| 术语 | 一句话解释 |
|------|-----------|
| **API Server** | Control Plane 统一入口，所有请求必经此处，负责认证/授权/验证 |
| **etcd** | 集群状态唯一存储，所有组件通过 API Server 读写，Raft 保证强一致性 |
| **Controller Manager** | 所有 Controller 的运行容器，通过 watch 机制持续比较期望与实际状态 |
| **Scheduler** | 决定 Pod 调度到哪个 Node，两步走：Filter（过滤）→ Score（打分） |
| **kubelet** | 每台 Node 上的代理，接收 API Server 推送，实际调用 Container Runtime 创建容器 |
| **CRI** | Container Runtime Interface，K8s 与容器实现之间的标准接口 |
| **containerd** | 主流 Container Runtime，从 Docker 剥离，专注容器生命周期 |
| **namespace（Linux）** | 隔离进程的资源视图（网络、存储、PID 等） |
| **cgroup** | 限制进程的计算资源使用量（CPU、内存） |
| **requests** | Pod 对资源的最低保证，Scheduler 调度时的依据 |
| **limits** | Pod 对资源的硬上限，由 cgroup 强制执行 |
| **LimitRange** | 强制要求 namespace 内 Pod 必须设置 requests/limits |
| **Mutation Webhook** | 在写入 etcd 前自动修改请求内容（如补默认值） |
| **Validation Webhook** | 在写入 etcd 前验证请求内容，不合规则拒绝 |
| **Leader Election** | Controller Manager 等多实例组件通过 Lease 锁选出唯一工作实例 |
| **Raft** | etcd 使用的分布式共识算法，保证多节点数据强一致 |
| **Quorum** | Raft 中的多数派，n/2+1，低于此数集群不可写 |
