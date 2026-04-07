---
title: Container Basics
category: tech/infra
tags: [containers, docker, oci, image, layer, registry, dockerfile, containerd, runtime]
status: draft
priority: medium
last_updated: 2026-04-06
created_from_jd:
---

# Container Basics

## Knowledge Map
- Prerequisites（前置知识）：[[Linux Namespaces]]
- Related Topics（延伸话题）：[[Kubernetes]], [[K8s Control Plane]]
- Management（管理关联）：

## Core Concepts

**What a Container Is（容器的本质）**
- Container = **process + isolated environment**: uses Linux Namespace (view isolation) + cgroup (resource limits) to isolate a process from the host and other processes
- NOT a "lightweight VM": no independent kernel, shares the host Linux kernel, only the view and resources are isolated
- Core value: **environment consistency** (dependencies are packaged — the "works on my machine" problem disappears) + **fast startup** (milliseconds vs VM's minutes)

**Image and Layers（镜像与层）**
- Image = **read-only filesystem snapshot** composed of multiple **Layers** stacked together (Union File System) （只读快照 + 联合文件系统）
- Each `Dockerfile` instruction generates a new Layer; identical Layer content can be shared across images (local cache)
- At runtime, a **writable Container Layer** is added on top: writes inside the container only affect this layer, the image itself is unchanged
- Images are stored in a **Registry** (Docker Hub, ECR, GCR); `docker pull` only downloads Layers not already present locally

**OCI Standard（开放容器标准）**
- **OCI (Open Container Initiative)**: defines the industry standard for image format (Image Spec) and runtime interface (Runtime Spec)
- Any OCI-compliant image runs on any OCI-compliant Runtime — not tied to Docker
- Kubernetes uses CRI (Container Runtime Interface) to interface with OCI Runtimes (containerd, CRI-O)

**Docker vs containerd**
- Docker = complete toolchain: build (build) + distribute (push/pull) + run (run)
- **containerd** = container runtime extracted from Docker, focused on **container lifecycle management** (pull, create, start, stop, delete) （专注容器生命周期）
- K8s 1.20 deprecated dockershim (direct Docker integration as CRI), switching to containerd directly; image format (OCI) is unaffected — `docker build` images still work

**Dockerfile Core Instructions（核心指令）**
- `FROM`: base image; `RUN`: executes commands at build time (generates a new Layer); `COPY`/`ADD`: copy files
- `CMD`/`ENTRYPOINT`: container startup command (CMD can be overridden, ENTRYPOINT cannot)
- `ENV`: environment variables; `EXPOSE`: declares ports (documentation only, does not auto-map)
- Best practices: merge `RUN` commands to reduce Layer count; use `.dockerignore`; use multi-stage builds to minimize final image size

**Container Lifecycle（生命周期）**
- `created → running → paused / stopped → deleted`
- Data written inside the container is lost when the container is deleted (the writable layer is gone with the container)
- Persistent data requires mounting a Volume (corresponds to K8s PV/PVC) （持久化需挂 Volume）

## Key Questions

**Q: What is the core difference between a container and a VM? What are they each suited for?**
Answer framework: Containers share the kernel (lightweight/fast/weaker isolation); VMs have independent kernels (heavyweight/slow/stronger isolation); containers suit microservices, CI/CD, stateless apps; VMs suit strong isolation needs (multi-tenant), running a different OS, or special kernel requirements; K8s mixes both (Pods run on VM Nodes).
> 中文提示：容器共用内核（轻量快速），VM 独立内核（强隔离慢启动）；K8s 上可混用（Pod 在 VM Node 上运行）

**Q: What are the benefits of the image Layer mechanism?**
Answer framework: Layer sharing saves storage and transfer (base image Layers only need to be pulled once); build cache (unchanged Layers are not rebuilt — dramatically speeds up CI/CD); image immutability (read-only Layers + writable container layer) guarantees environment consistency; too many Layers hurt performance — merge `RUN` instructions appropriately.
> 中文提示：Layer 共享节省传输；构建缓存加速 CI/CD；不可变性保证环境一致性；Layer 过多影响性能

**Q: Can a `docker build` image run directly on K8s? What impact did K8s deprecating Docker have?**
Answer framework: Yes, because Docker and K8s both follow the OCI standard; what K8s deprecated was dockershim (the entire Docker stack as a CRI implementation), not the image format; developers still use `docker build`; containerd runs these images just fine; basically no impact on developers, cluster administrators need to confirm the Runtime has migrated to containerd.
> 中文提示：弃用的是 dockershim 不是 OCI 镜像格式；docker build 的镜像 containerd 照样运行；开发者无感知

**Q: What is the difference between ENTRYPOINT and CMD?**
Answer framework: ENTRYPOINT defines the container's main command (typically not overridden, defines what the container does); CMD defines default arguments (can be overridden at `docker run` time); used together: `ENTRYPOINT ["python"]` + `CMD ["app.py"]`; in K8s Pod spec, `command` corresponds to ENTRYPOINT, `args` corresponds to CMD.
> 中文提示：ENTRYPOINT 定义容器用途（不可轻易覆盖）；CMD 是默认参数（可覆盖）；K8s 的 command/args 对应两者

## Summary

The core of container technology is "package the application and its dependencies together so it runs consistently in any environment." The image Layer mechanism solves transmission and storage efficiency; the OCI standard solves ecosystem interoperability; Namespace/cgroup provides runtime isolation. These three layers combined form the underlying foundation of the entire container ecosystem from Docker to K8s.

containerd replacing dockershim is the result of K8s ecosystem specialization: Docker is the complete developer toolchain, containerd is the streamlined production runtime. For AI Infra engineers, understanding this division of labor matters — you operate containerd on the cluster (via `crictl`), while presenting Docker image format to developers (via ECR/GCR).

From an AI Infra perspective, container basics directly affect: ① training image management (CUDA versions, Python dependencies frozen in image Layers, guaranteeing reproducibility); ② multi-stage builds (large development image, small production inference image); ③ container writable layer's ephemeral nature (training checkpoints must be written to a Volume, not the container itself). Understanding image Layer caching is also the foundation for optimizing GPU cluster node startup speed (avoiding re-pulling large CUDA images every time).

> 面试重点：Layer 机制（共享+构建缓存+不可变性）→ OCI 标准（镜像格式与 Runtime 分离）→ dockershim 弃用（只弃 Runtime 不弃镜像格式）→ ENTRYPOINT vs CMD

## Raw Material
