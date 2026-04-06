---
title: Kubernetes
category: tech/infra
tags: [k8s, container-orchestration, scheduling, pods, deployments, statefulset, rbac, hpa, pv, pvc]
status: draft
priority: high
last_updated: 2026-04-06
created_from_jd:
---

# Kubernetes

## Knowledge Map
- 前置知识：[[Container Basics]], [[Linux Namespaces]], [[Networking Fundamentals]]
- 延伸话题：[[Kubernetes GPU Scheduling]], [[Karpenter]], [[Service Mesh]], [[etcd]], [[Admission Webhooks]], [[Custom Resource Definitions]]
- 管理关联：[[Platform Team Management]]

## Core Concepts

**Pod**
- K8s 最小部署单元；多个容器共享网络命名空间（localhost 互通）和存储，同一 Pod 内容器端口不可冲突
- Pod IP 会变，Service 通过 Label/Selector 提供稳定虚拟 IP 和 DNS 名

**调度 (Scheduling)**
- Scheduler 两步：Filter（过滤不符合条件 Node）→ Score（候选 Node 打分选最优）
- Taint/Toleration：Node 设"排斥标记"，Pod 需声明 Toleration 才能进入（GPU Node 隔离的核心机制）
- NodeSelector：Pod 主动指定目标 Node 的 Label；两者结合才能精准定向

**Probe**
- Liveness Probe：失败 → 重启 Pod（检测是否存活）
- Readiness Probe：失败 → 从 Service 摘除但不重启（检测是否可接流量）
- `initialDelaySeconds`：给 JVM 等慢启动应用预留初始化时间，防止误杀

**Deployment / HPA / 滚动发布**
- Deployment = ReplicaSet（维护副本数） + 滚动发布 + 版本回滚
- `maxSurge`：发布期间最多额外新建 Pod 数；`maxUnavailable`：最多允许不可用数（硬性保证）
- 新版 Pod 一直未 Ready 超时 → 自动回滚；也可 `kubectl rollout undo`
- HPA：基于 CPU/内存/自定义指标自动水平扩缩容

**StatefulSet（有状态应用）**
- 每个 Pod 有固定 ID（pod-0, pod-1）和有序启动（0→1→2）
- 数据存在 PV，Pod 重建后仍挂载原 PV，不丢数据
- 迁移复杂：按 ID 从高到低删除再重建，依赖网络存储可挂载
- 脑裂问题 K8s 不处理，需应用层解决（如 MySQL Group Replication）

**PV / PVC / StorageClass**
- PV = 实际存储资源（必须网络存储，保证可跨 Node 挂载）
- PVC = Pod 的存储申请，K8s 按最小满足原则自动绑定 PV
- StorageClass = 动态按需创建 PV，无需管理员手动预备；无匹配 PV 时 Pod 卡 Pending

**ConfigMap & Secret**
- ConfigMap：非敏感配置；Secret：敏感信息（Base64 + etcd AES 加密 + RBAC 才真安全）

**RBAC**
- Role（namespace 级）/ ClusterRole（集群级）定义权限
- RoleBinding / ClusterRoleBinding 将权限绑定到 User/Group/ServiceAccount
- ServiceAccount = Pod 的身份证，用于调用 K8s API；默认 default SA 无额外权限

**集群稳定性**
- kubelet 定期发 Heartbeat；`pod-eviction-timeout` 控制 Node 失联后驱逐时机（太短误判触发迁移风暴，太长服务不可用）
- etcd 挂掉 → 集群只读降级（已有 Pod 继续运行，不能创建/修改资源）

## Key Questions

**Q: Pod 和容器的区别是什么？为什么 K8s 不直接调度容器？**
Answer framework: Pod 是共享网络/存储命名空间的容器组，是 K8s 最小调度单元。说明 sidecar 模式（日志/监控容器与主容器共存）需要共享网络的场景，解释 Pod 抽象的必要性。

**Q: Service 如何知道流量转发给哪些 Pod？Pod 挂掉会继续转发吗？**
Answer framework: Label/Selector 机制；Readiness Probe 失败自动从 Endpoint 摘除；引申到 Probe 配置对服务稳定性的重要性。

**Q: 如何让 GPU 工作负载只调度到 GPU Node？**
Answer framework: Taint GPU Node（驱逐普通 Pod） + Pod 声明 Toleration（允许进入） + NodeSelector/NodeAffinity（精准定向）三者结合；提到 K8s device plugin 机制暴露 GPU 资源。

**Q: Deployment 滚动发布时如何保证服务不中断？新版本有 bug 如何处理？**
Answer framework: maxSurge/maxUnavailable 参数控制发布节奏；Readiness Probe 确保新 Pod 就绪才切流量；超时自动回滚 + kubectl rollout undo 手动回滚。

**Q: StatefulSet 和 Deployment 的核心区别？什么场景用 StatefulSet？**
Answer framework: 固定 Pod ID + 有序启动 + PV 绑定；举例 MySQL 主从（pod-0 主/pod-1 从固定角色）、Kafka（Broker ID 固定）；提到 PV 挂载失败和脑裂是常见坑。

**Q: Secret 的安全性如何保证？Base64 够用吗？**
Answer framework: Base64 只是编码不是加密；真正安全需要 etcd AES 加密（at-rest encryption） + RBAC 控制访问 + 外部 Secret 管理方案（Vault/KMS）三层。

**Q: etcd 挂掉集群会怎样？如何保证 etcd 高可用？**
Answer framework: 只读降级（已有 Pod 继续运行，无法创建/修改资源）；etcd 奇数节点（3/5）Raft 共识，超半数存活即可正常；说明 etcd 备份策略。

**Q: Node 突然失联，K8s 如何响应？pod-eviction-timeout 如何调优？**
Answer framework: kubelet Heartbeat → Node Controller 检测 → 等待 eviction-timeout → 驱逐 Pod 重建；太短触发迁移风暴（网络抖动误判），太长影响可用性；结合业务 SLA 取值。

## Summary

Kubernetes 是容器编排的工业标准，核心价值在于将基础设施声明化：你描述"期望状态"，K8s 负责收敛到这个状态并持续维护。理解 K8s 的关键是掌握它的控制循环思想（observe → diff → act），这一思想贯穿 Scheduler、kubelet、Deployment Controller、HPA 等所有核心组件。

从调度视角看，K8s 通过 Taint/Toleration + NodeSelector 实现工作负载隔离（这是 GPU 集群管理的基础），通过 HPA 实现弹性伸缩，通过 maxSurge/maxUnavailable 实现零停机发布。Readiness Probe 是这一切的安全阀——只有真正就绪的 Pod 才会承接流量，无论是正常服务还是滚动发布过程中。

从存储视角看，PV/PVC 抽象将存储资源与 Pod 生命周期解耦，StatefulSet 在此基础上为有状态应用提供固定身份，但代价是更复杂的迁移和更高的运维要求。etcd 是集群的唯一真相来源，其高可用和加密配置直接决定集群的可靠性和安全性上限。对于 AI Infra 场景，K8s 的 GPU device plugin、MIG 分区、GPU 拓扑感知调度是在核心概念之上需要重点深入的方向。

## Raw Material
- [[raw_material/tech/infra/k8s-core]]
