---
title: Linux Namespaces
category: tech/infra
tags: [linux, namespaces, cgroups, containers, isolation, pid, network, mount, ipc, uts]
status: draft
priority: medium
last_updated: 2026-04-06
created_from_jd:
---

# Linux Namespaces

## Knowledge Map
- Prerequisites（前置知识）：[[Linux Fundamentals]]
- Related Topics（延伸话题）：[[Container Basics]], [[Kubernetes]], [[K8s Control Plane]]
- Management（管理关联）：

## Core Concepts

**What a Namespace Is（资源隔离机制）**
- Linux Namespace is a **kernel-provided resource isolation mechanism**: makes the "world" visible to a process separate from the host and other processes
- Containers are fundamentally a group of processes isolated by Namespaces — without Namespaces, there are no containers
- Complementary to cgroups (which limit resource consumption): Namespace = isolated view, cgroup = usage ceiling （隔离视图 vs 限制上限）

**Six Namespace Types（六大类型）**

| Namespace | What It Isolates | Role in Containers |
|-----------|-----------------|-------------------|
| **PID** | Process ID space | Container processes start with PID 1; cannot see host processes |
| **Network** | Network stack (NIC, IP, routing, ports) | Each container has its own IP and network stack, no conflicts |
| **Mount** | Filesystem mount points | Container sees a filesystem isolated from the host (rootfs) |
| **UTS** | Hostname and domain name | Container can have its own hostname |
| **IPC** | Inter-process communication resources (shared memory, semaphores) | IPC is isolated between containers |
| **User** | User and group IDs | Container root mapped to unprivileged host user (security enhancement) |

**Pod Shares a Network Namespace（Pod 共享 Network Namespace）**
- All containers in a K8s Pod share the same **Network Namespace**: they share one IP address, ports must not conflict, containers communicate via localhost
- This is the foundational mechanism for the sidecar pattern (Envoy, logging containers co-located with the main container)
- Each container has its own **Mount Namespace** (its own filesystem view) and **PID Namespace** (independent process tree)

**Namespace vs Virtual Machine（容器 vs 虚拟机）**
- VM = **Hypervisor-level isolation**: each VM has its own kernel, full OS — strong isolation, high overhead
- Container = **process-level isolation**: shares the host kernel; Namespace provides view isolation; fast startup, low resource overhead
- Container isolation is weaker than VM: kernel vulnerabilities (e.g., container escape) can affect the host; GPU isolation requires additional mechanisms (MIG)

**cgroup and Namespace Relationship（cgroup 与 Namespace 的关系）**
- Namespace controls "what can be seen" (isolated view); **cgroup controls "how much can be used"** (CPU/memory/IO ceiling)
- K8s requests/limits → containerd translates them into cgroup configurations → creates a dedicated cgroup directory per container
- GPU isolation: basic cgroups don't directly manage GPUs; requires device plugin (to expose GPU resources) + MIG (hardware-level partitioning)

## Key Questions

**Q: How does a container achieve isolation? What is the fundamental difference from a VM?**
Answer framework: Namespace (isolates views: PID/Network/Mount/UTS/IPC/User) + cgroup (limits resources: CPU/memory); containers share the host kernel, VMs have independent kernels; containers are lighter but weaker isolation; security-sensitive scenarios (multi-tenant) should consider gVisor/Kata Containers (between containers and VMs).
> 中文提示：Namespace = 隔离视图，cgroup = 限制上限；容器共用内核，VM 独立内核；安全敏感场景考虑 gVisor/Kata

**Q: How do containers within a K8s Pod communicate via localhost?**
Answer framework: All containers in a Pod share the same Network Namespace (same IP, shared network stack); localhost communication is possible because they are in the same network namespace; ports must not conflict (same IP, two containers binding the same port would conflict); this is the underlying mechanism that allows Istio Sidecar injection (Envoy) to intercept the main container's traffic.
> 中文提示：Pod 内共享 Network Namespace（同 IP），localhost 互通；这是 Istio Sidecar 能拦截流量的底层原因

**Q: What is the relationship between PID 1 inside a container and the host?**
Answer framework: The container has its own PID Namespace — processes inside start from PID 1 (typically the container's main process); from the host's perspective, that process has a different real PID; killing PID 1 inside the container = exiting the container (signal handling is key to container lifecycle management).
> 中文提示：容器内 PID 1 是主进程；宿主机视角有不同真实 PID；kill PID 1 = 退出容器

**Q: How does the User Namespace improve container security?**
Answer framework: User Namespace maps UID 0 (root) inside the container to an unprivileged user on the host; even if a container process runs as root, its actual privileges are limited; prevents container escape from directly gaining host root privileges; this is the foundation of rootless containers (e.g., Podman).
> 中文提示：容器内 root 映射到宿主机普通用户；防止容器逃逸直接获得宿主机 root 权限

## Summary

Linux Namespace is the foundation of the entire container technology stack — Docker, containerd, and K8s Pods are all built on these six Namespace types. Understanding Namespace means understanding the essence of containers: "isolated but not disconnected" — processes see an isolated world, but share the same Linux kernel.

K8s Pod design (multiple containers in a Pod sharing a Network Namespace) comes directly from Namespace semantics: Sidecar containers can intercept the main container's traffic, and communicate via localhost, all because they are in the same Network Namespace. This is also the underlying feasibility of Istio Sidecar injection.

From an AI Infra perspective, GPU isolation is the extension challenge of the Namespace/cgroup mechanism in GPU scenarios: CPU/memory can be hard-isolated with cgroups, but GPU resources require K8s device plugin + NVIDIA MIG partitioning for true isolation. Namespace provides the software foundation for container isolation, MIG provides hardware-level GPU partitioning — combining both layers achieves secure isolation in multi-tenant GPU clusters.

> 面试重点：六大 Namespace 类型及作用 → Pod 共享 Network Namespace（sidecar 底层原理）→ Namespace vs cgroup 区别 → GPU 隔离的额外挑战（device plugin + MIG）

## Raw Material
