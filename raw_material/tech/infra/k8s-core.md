---
title: K8s 核心概念复习
source:
date_saved: 2026-04-06
processed: true
skill_note: [[skills/tech/infra/Kubernetes]]
---

# K8s 核心概念复习

> 覆盖主题：Pod → Service（Label/Selector）→ Probe（Liveness/Readiness）→ 调度（Scheduler/Taint/NodeSelector）→ Deployment / HPA / 滚动发布 → StatefulSet → PV / PVC / StorageClass → ConfigMap / Secret → RBAC / ServiceAccount → 集群稳定性（Node 故障 / etcd 高可用 / 迁移风暴）

---

## 一、Pod 基础

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 1 | 为什么用 Pod 而不直接部署容器？ | Pod 是 K8s 最小部署单位，可包含多个容器，这些容器**共享网络、存储和计算资源**。如 Service 容器 + 日志容器共存。Pod 像一个 OS，容器像其中运行的进程 | Pod = 共享命名空间的容器组 |
| 2 | Pod 内两个容器如何通信？ | 共享同一网络命名空间，通过 **localhost + 不同端口号**互相访问（如 `localhost:8080`），不需要跨 IP | 同一 Pod 内 = 同一个 localhost |
| 3 | Pod 内容器端口有没有冲突风险？如何避免？ | **有冲突风险**。同一 Pod 内的容器共享端口空间，若两个容器都用 8080，后者无法启动。开发者需负责确保端口不重叠 | 端口冲突由开发者自己管理 |

---

## 二、Service 与负载均衡

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 4 | Pod IP 会变，Pod 间如何稳定通信？ | 用 **Service**：Service 提供稳定的虚拟 IP 和 DNS 名，无论 Pod 怎么重建，访问地址不变 | Service = 稳定的访问入口 |
| 5 | Service 怎么知道流量该转发给哪些 Pod？ | 通过 **Label + Selector**：Pod 打 Label（如 `app: web`），Service 的 Selector 匹配对应 Label，自动找到"自己人" | Label/Selector = 松耦合匹配机制 |
| 6 | Service 如何分配流量？挂掉的 Pod 会被转发吗？ | 支持多种规则（默认 Round Robin，也可 Hash 等）；Pod 有 **Readiness Probe**，未通过则自动从 Service 转发列表中摘除，不会转发到不健康的 Pod | Readiness Probe = 流量熔断保护 |

---

## 三、Liveness & Readiness Probe

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 7 | Liveness Probe 和 Readiness Probe 有什么区别？ | **Liveness**：检测 Pod 是否存活，失败则重启 Pod；**Readiness**：检测 Pod 是否准备好接收流量，失败则从 Service 摘除但不重启 | Liveness = 活没活；Readiness = 能不能接活 |
| 8 | Java 应用启动需要 30 秒，如何防止 Probe 误杀？ | 配置 **`initialDelaySeconds`**：让 K8s 在 Pod 启动后等待指定秒数再开始探测，避免 JVM 还没初始化好就被判死 | `initialDelaySeconds` = 启动缓冲期 |
| 9 | Liveness 和 Readiness 可以用不同的检测方式吗？ | 可以。Liveness 可以只 ping 通（TCP/ICMP），Readiness 可以要求某个 HTTP URL 返回 200，二者相互独立配置 | 两种 Probe 可配不同检测端点和条件 |

---

## 四、调度：Scheduler / Taint / Node Selector

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 10 | K8s 如何决定把 Pod 调度到哪台 Node？ | **Scheduler** 两步走：① Filter（过滤不符合条件的 Node）→ ② Score（对候选 Node 打分选最优）| Scheduler = Filter + Score |
| 11 | 如何限制 Pod 只能运行在 GPU Node 上？ | **Taint + Toleration**：给 GPU Node 打 Taint（"闲人免进"），Pod 声明对应 Toleration 才能调度进来；**Node Selector**：Pod 主动声明目标 Node 的 Label | Taint/Toleration = 门卫；NodeSelector = GPS 导航 |
| 12 | Taint 和 Node Selector 的区别？两个配合使用效果如何？ | Taint 是 Node 的**排斥**机制（没 Toleration 进不来）；Node Selector 是 Pod 的**主动选择**。两者组合：没 Toleration 的 Pod 被拦，有 Toleration 但没 Node Selector 的 Pod 只是"可以进"但不一定会进，同时配置才能精准钉死 | Taint ≠ 吸引，只是排斥；要精准定向需两者结合 |

---

## 五、ReplicaSet / Deployment / HPA

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 13 | ReplicaSet 是什么？如何保证多个 Pod 完全一样？ | ReplicaSet 维护指定数量的 Pod 副本，通过 **Pod Template Spec** 定义统一模板，所有 Pod 从同一模子创建 | Template Spec = Pod 克隆模板 |
| 14 | Deployment 和 ReplicaSet 的关系？Deployment 额外解决了什么？ | Deployment 管理 ReplicaSet，在其基础上增加了：**滚动发布**、**暂停/继续发布**、**版本回滚**，以及通过 `maxSurge` / `maxUnavailable` 保证发布期间服务稳定 | Deployment = ReplicaSet + 发布管理 |
| 15 | 如何实现根据流量自动扩缩容？ | 使用 **HPA（Horizontal Pod Autoscaler）**：配置触发扩缩容的 metrics（CPU、内存或自定义指标），K8s 自动调整 replica 数量 | HPA = 自动水平扩缩容 |

---

## 六、滚动发布：maxSurge / maxUnavailable

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 16 | `maxSurge=2, maxUnavailable=1` 时滚动发布的步骤？ | 先新建 2 个新版本 Pod，同时允许杀掉 1 个旧 Pod；等新 Pod 就绪后继续替换，直到全部更新完成 | maxSurge = 最多额外新建数；maxUnavailable = 最多允许不可用数 |
| 17 | 最坏情况下最多几个 Pod 不可用？会超过 `maxUnavailable` 吗？ | **不会超过**，`maxUnavailable` 是硬性保证。如设为 1，整个发布过程中最多同时 1 个 Pod 不可用 | 硬性下限，K8s 保证不突破 |
| 18 | 新版本有 bug，新 Pod 一直起不来，K8s 会自动回滚吗？ | 会。Pod 一直未达到 Ready 状态超过超时时间，Deployment 自动回滚到上一个稳定版本；也可手动触发 `kubectl rollout undo` | 自动回滚 + 手动回滚均支持 |

---

## 七、StatefulSet（有状态应用）

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 19 | StatefulSet 和 Deployment 的核心区别？ | StatefulSet 的每个 Pod 有**固定 ID**（pod-0, pod-1, pod-2）和**固定启动顺序**（按编号 0→1→2 顺序启动）；Deployment 的 Pod ID 随机，无顺序 | 固定身份 + 有序启动 = StatefulSet 核心特征 |
| 20 | StatefulSet 的数据存在哪里？Pod 重启后数据不会丢吗？ | 业务数据存在 **PV（PersistentVolume）** 中；集群状态存在 **etcd** 中。Pod 重启后 pod-0 仍会挂载原来的 PV，数据不丢 | etcd = 集群配置；PV = 业务数据持久化 |
| 21 | StatefulSet 最容易踩的坑是什么？ | **PV 挂载失败**（网络存储不稳定）、**主从脑裂**（K8s 本身无法解决，需应用层处理，如 MySQL Group Replication）、**有序升级/迁移复杂度高** | 实战坑：PV 挂载 + 脑裂 = 应用层自己处理 |

---

## 八、PV / PVC / StorageClass

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 22 | PV 和 PVC 分别是什么？它们如何配合使用？ | **PV**（PersistentVolume）= 实际存储资源；**PVC**（PersistentVolumeClaim）= Pod 对存储的申请单。K8s 自动将 PVC 和符合条件的 PV 绑定 | PV = 存储资源；PVC = 存储申请 |
| 23 | 申请 100GB PVC，集群有 80GB 和 200GB 的 PV，选哪个？ | 选 **200GB** 的 PV（最小满足需求的 PV） | 按最小满足原则匹配 |
| 24 | PV 必须用网络存储，不能用本地磁盘，为什么？ | Pod 可能被调度到任意 Node，本地磁盘无法跟随迁移；**网络存储**（如 NFS、EBS、Ceph）可在任意 Node 上挂载 | PV = 必须网络存储，保证可迁移性 |
| 25 | 没有符合条件的 PV 时 Pod 会怎样？如何自动供给？ | Pod 卡在 Pending 状态等待。配置 **StorageClass** 后可按需自动创建 PV，无需管理员手动准备 | StorageClass = 动态按需供给 PV |

---

## 九、ConfigMap & Secret

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 26 | ConfigMap 和 Secret 的区别？ | **ConfigMap** = 普通配置（无加密）；**Secret** = 敏感配置（Base64 编码存储，支持加密）。Secret 是特殊的 ConfigMap，专门处理密码、Token 等敏感信息 | Secret ≠ 只是 Base64，配合 etcd 加密才真安全 |
| 27 | Secret 的 Base64 只是编码，真正安全靠什么？ | ① **etcd AES 加密**：开启后数据在磁盘上真正加密；② **RBAC 权限控制**：限制哪些用户/服务账号可以读取 Secret | 安全 = etcd 加密 + RBAC 双层保障 |

---

## 十、RBAC 权限控制

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 28 | Role 和 ClusterRole 的区别？ | **Role** = namespace 级别权限，只在某个命名空间内有效；**ClusterRole** = 集群级别权限，跨所有 namespace | namespace 范围 vs 全集群范围 |
| 29 | 如何把权限绑定给用户或 Pod？ | **RoleBinding**：把 Role 绑定到 User/Group/ServiceAccount（namespace 级别）；**ClusterRoleBinding**：把 ClusterRole 全局绑定 | RoleBinding = 权限与身份的"桥梁" |
| 30 | Pod 在运行时需要调用 K8s API，怎么授权？ | 使用 **ServiceAccount**：专门给 Pod 用的身份标识。流程：① 创建 ServiceAccount → ② 创建 ClusterRole（定义权限）→ ③ ClusterRoleBinding 绑定 → ④ Pod 配置中声明使用该 ServiceAccount | ServiceAccount = Pod 的"身份证" |
| 31 | Pod 不配置 ServiceAccount 有默认权限吗？ | Pod 默认使用 namespace 下的 **default ServiceAccount**，默认无任何额外权限，基本调用不了 K8s API | 默认 default SA 无权限，需显式绑定 |

---

## 十一、集群稳定性

| # | 问题 | 核心答案 | 关键词 |
|---|------|----------|--------|
| 32 | K8s 如何检测到 Node 挂掉？ | **kubelet** 定期向 Node Controller 发送 **Heartbeat**；收不到后等待 `pod-eviction-timeout`（可配置）后将 Node 上的 Pod 驱逐并在其他 Node 重建 | Heartbeat + eviction timeout |
| 33 | `pod-eviction-timeout` 设太短或太长各有什么风险？ | **太短**：网络抖动导致误判，触发大规模迁移风暴；**太长**：真正挂掉的 Node 上的 Pod 长时间不可用，影响服务 | 权衡：快速响应 vs 误判风险 |
| 34 | etcd 挂掉，集群会完全瘫痪吗？ | 不会立刻瘫痪。etcd 挂掉后集群进入**只读状态**：已在跑的 Pod 继续提供服务，但无法创建/修改/删除资源 | etcd = 只读降级，而非立刻崩溃 |
| 35 | StatefulSet 的 Pod 和 Deployment 的 Pod 迁移一样吗？ | 不一样。StatefulSet 迁移更复杂：按 ID **从高到低顺序删除**，再到新 Node 按顺序重建，且 PV 必须能在新 Node 成功挂载，失败风险更高 | StatefulSet 迁移 = 有序 + 依赖网络存储 |
| 36 | MySQL 主从脑裂，K8s 能自动解决吗？ | **不能**。脑裂是应用层问题，需要 MySQL 自己的高可用方案解决（如 MySQL Group Replication、Orchestrator） | 脑裂 = 应用层处理，K8s 不介入 |

---

## 十二、综合设计：电商系统 K8s 部署

**需求**：无状态 Web 服务（高可用 + 弹性扩容）+ MySQL（持久化）+ 敏感配置

| 组件 | K8s 机制 | 理由 |
|------|----------|------|
| 无状态 Web 服务 | **Deployment + HPA + Service** | Deployment 保证滚动发布和副本管理；HPA 自动扩缩容；Service 提供稳定访问入口 |
| MySQL 数据库 | **StatefulSet + PVC + StorageClass** | 固定 Pod ID 区分主从；PVC 绑定 PV 持久化数据；StorageClass 自动供给存储 |
| 数据库密码等敏感信息 | **Secret（+ etcd AES 加密）** | Base64 存储 + RBAC 权限控制，开启 etcd 加密后真正安全 |
| 普通配置（端口、环境等）| **ConfigMap** | 非敏感配置，直接注入环境变量或挂载为文件 |

---

## 十三、术语速查

| 术语 | 一句话解释 |
|------|-----------|
| **Pod** | K8s 最小部署单元，容器共享网络和存储 |
| **Service** | 稳定访问入口，通过 Label/Selector 路由到 Pod |
| **Liveness Probe** | 检测 Pod 是否存活，失败则重启 |
| **Readiness Probe** | 检测 Pod 是否可接收流量，失败则从 Service 摘除 |
| **initialDelaySeconds** | Probe 启动延迟，给应用预留初始化时间 |
| **Taint / Toleration** | Node 设置"拒绝标记"，Pod 声明"容忍"才能进入 |
| **Node Selector** | Pod 主动指定要运行在哪类 Node 上 |
| **ReplicaSet** | 维护固定数量的 Pod 副本 |
| **Deployment** | ReplicaSet + 滚动发布 + 回滚管理 |
| **HPA** | 根据 metrics 自动水平扩缩容 |
| **maxSurge** | 滚动发布时最多额外新建的 Pod 数 |
| **maxUnavailable** | 滚动发布时最多允许不可用的 Pod 数（硬性保证）|
| **StatefulSet** | 有状态应用，固定 Pod ID + 有序启动 |
| **PV** | 实际存储资源（必须网络存储）|
| **PVC** | Pod 对存储的申请，与 PV 自动绑定 |
| **StorageClass** | 按需动态创建 PV，无需手动预备 |
| **ConfigMap** | 存储非敏感配置信息 |
| **Secret** | 存储敏感信息，配合 etcd AES 加密 + RBAC |
| **etcd** | K8s 集群大脑，存储所有集群状态和配置 |
| **Role / ClusterRole** | 定义权限范围（namespace 级 / 集群级）|
| **RoleBinding** | 把 Role 与 User/Group/ServiceAccount 绑定 |
| **ServiceAccount** | Pod 的身份标识，用于 K8s API 授权 |
| **kubelet** | 每台 Node 上的代理，定期发 Heartbeat |
| **pod-eviction-timeout** | Node 失联后等待多久才驱逐 Pod，越短越快但误判风险高 |
