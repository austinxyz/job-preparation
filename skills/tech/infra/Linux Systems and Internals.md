---
title: Linux Systems and Internals
category: tech/infra
tags:
  - linux
  - kernel
  - process-management
  - memory-management
  - storage
  - filesystems
  - networking
  - performance
  - cgroups
  - namespaces
  - signals
  - ipc
  - syscalls
  - debugging
  - overlayfs
  - inode
  - triage
status: draft
priority: high
last_updated: 2026-05-25
created_from_jd: "[[jobs/Cloud Leader - RD & SRE - TikTok]]"
---

# Linux Systems and Internals

## Knowledge Map
- 前置知识：Operating systems fundamentals, process lifecycle, virtual memory
- 延伸话题：[[Linux Namespaces]], [[Kernel Subsystems and NUMA]], [[Linux Performance Tuning for Network Services]], [[Container Basics]], [[Kubernetes]]
- 管理关联：SRE incident triage, K8s node troubleshooting, performance regression root cause analysis

## Core Concepts

### Kernel Mode vs User Mode

- **两种CPU特权级别。** Linux使用Ring 0（内核态）和Ring 3（用户态）。用户态：所有应用程序运行的地方，不能直接访问硬件，受限地址空间。内核态：内核代码、设备驱动、系统调用处理在这里运行，完整硬件访问权限。
- **System call是唯一合法入口。** 用户进程通过`syscall`指令请求内核服务（`read()`, `write()`, `open()`, `fork()`），CPU从Ring 3切换到Ring 0，执行完后切回Ring 3。每次模式切换约100ns开销，高频syscall（如小I/O循环）会积累成可测量的CPU消耗。
- **容器共享宿主内核。** 容器内所有进程调用同一个host kernel的syscall。没有第二个内核 = 容器比VM轻量。安全风险：内核漏洞会影响该host上的所有容器。

**K8s相关：**

| 机制 | 说明 |
|------|------|
| **seccomp** | 每个容器的syscall白名单。K8s默认profile屏蔽约44个危险syscall（如`ptrace`, `mount`） |
| **Privileged container** | 获得内核能力（CAP_SYS_ADMIN等），接近内核态，安全风险高 |
| **eBPF** | 在内核态运行用户编写的沙盒程序。Cilium用eBPF替换iptables做in-kernel包处理 |
| **FUSE** | 文件系统逻辑在用户态运行（每次I/O额外模式切换），灵活但慢。部分CSI driver使用FUSE |

```bash
strace -p <pid> -c    # 汇总syscall次数和耗时
strace -p <pid> -T    # 每个syscall的延迟
vmstat 1              # cs列 = 上下文切换次数/秒
```

---

### Linux File System Types

| 文件系统 | 用途 | 关键特点 |
|---------|------|---------|
| **ext4** | 通用默认 | journaling、extent树、最大16TB单文件 |
| **XFS** | 大文件/高吞吐（数据库、日志） | 并发写更好、不支持在线缩容 |
| **tmpfs** | 内存文件系统 | RAM-backed、重启丢失、极快 |
| **overlayFS** | 容器镜像分层 | Copy-on-Write，upper+lower+merged |
| **proc / sysfs** | 内核虚拟FS | `/proc`暴露进程/内核信息，`/sys`暴露设备驱动 |
| **cgroup FS** | 资源控制 | `/sys/fs/cgroup/`，K8s在此写pod资源限制 |
| **devtmpfs** | 设备文件 | `/dev/`，内核自动填充 |

---

### Core FS Concepts

**Inode**
- 每个文件 = inode（元数据：权限、属主、时间戳、数据块指针）+ 数据块。**inode不存文件名**，文件名存在目录项里（目录项 = 文件名 → inode编号映射）。
- 硬链接：两个文件名指向同一个inode（引用计数）。软链接：一个文件，内容是另一个路径字符串。
- `df -i`查inode使用率。**inode耗尽时磁盘空间未满也会报"No space left on device"**。大量小文件（日志、临时文件）容易耗尽inode。

```bash
ls -i          # 显示inode编号
stat file      # inode全部元数据
df -i          # inode使用率（关键排查命令）
```

**VFS（Virtual File System）**
- 内核抽象层，让应用用统一接口（`open/read/write/close`）访问不同类型FS。K8s pod里可同时挂载overlayFS、tmpfs、NFS——对应用完全透明。

**File Descriptor（文件描述符）**
- 进程用FD（整数）引用打开的文件/socket/管道。
- 系统级上限：`fs.file-max`。进程级上限：`ulimit -n`（默认1024，高并发应用太低）。
- 症状：`Too many open files` → 应用无法打开新连接/文件。

```bash
lsof -p <pid>              # 某进程所有打开的FD
cat /proc/sys/fs/file-nr   # 已用/空闲/最大
ulimit -n 65536            # 临时提升
```

**Page Cache（页面缓存）**
- 内核自动将文件读写缓存在RAM里。`free -h`里的`buff/cache`是page cache，内核可随时回收，不是内存泄漏。
- **脏页（Dirty Pages）**：写操作先进page cache，后台刷盘。`vm.dirty_background_ratio`（默认10%）触发后台刷盘，`vm.dirty_ratio`（默认20%）触发进程阻塞写。定期写延迟毛刺 → 可能是脏页集中刷盘。

**Mount Namespace**
- 每个容器有独立的mount namespace，看到自己的`/`，看不到host FS（除非显式挂载hostPath/hostPID）。

```bash
nsenter -t <pid> -m -- ls /   # 进入容器的mount namespace调试
```

---

### OverlayFS — 容器镜像的底层实现

```
容器看到的（merged）= upper层（可写）+ lower层（只读镜像层）

        merged/       ← 容器实际看到的联合视图
       /       \
  upper/        lower/（镜像层，只读，可多层叠加）
（读写层）    layer3 → layer2 → layer1（base image）
```

- **读**：先找upper，没有找lower（从上往下）。
- **写**：Copy-on-Write——先从lower把文件复制到upper，再修改。第一次写某文件会稍慢。
- **删除**：upper层创建whiteout文件标记删除，lower不变。
- **容器重启**：upper层清空（数据丢失），lower（镜像）保留。要持久化数据必须挂载PV/emptyDir/hostPath。

```bash
mount | grep overlay                           # 查看overlay挂载
cat /proc/<container-pid>/mounts | grep overlay  # 容器FS层信息
```

---

### Swap

- Swap = 用磁盘模拟RAM的溢出空间。即使SSD（~100µs）也比RAM（~100ns）慢1000倍。
- **`vm.swappiness`（0-100）**：0=尽量不swap，60=默认，100=激进swap。**K8s节点必须设0或直接`swapoff -a`**。
- **K8s必须关swap的原因**：cgroup内存限制靠OOMKill实现，有swap时容器可以悄悄超限降速而不触发OOMKill，破坏K8s内存保证。K8s 1.22+有alpha级swap支持，生产不推荐。
- **OOM killer优先级**：`oom_score_adj` — Guaranteed pod = `-997`（受保护），BestEffort = `1000`（最先被杀）。

```bash
free -h                        # Swap行：total/used/free
vmstat 1                       # si/so列：swap in/out，非零=问题
swapon --show                  # 查看swap设备
swapoff -a                     # 立即关闭所有swap
sysctl vm.swappiness=0         # 临时设置
echo "vm.swappiness=0" >> /etc/sysctl.conf && sysctl -p  # 永久
```

---

### Triage Methodology — 文件系统问题排查框架

**框架：Observe → Isolate → Root Cause → Fix**

**Step 1：Observe（观察症状）**
```bash
df -h          # 各挂载点磁盘空间
df -i          # inode使用率
du -sh /*      # 找哪个目录占大
iostat -xz 1   # I/O等待率、吞吐量、await时间
dmesg | grep -i "error\|i/o\|ext4\|xfs"  # 内核FS错误日志
```

**Step 2：Isolate（定位层次）**
```bash
iotop -o           # 只显示正在做I/O的进程
lsof +D /path      # 哪些进程访问此目录
findmnt            # 所有挂载点树状视图
cat /proc/mounts   # 原始挂载信息
```

**Step 3：常见场景处理**

| 症状 | 最可能原因 | 排查方向 |
|------|-----------|---------|
| "No space left" 但`df -h`有空间 | inode耗尽 | `df -i` → 找小文件密集目录 |
| K8s节点磁盘满 | 容器日志、overlayFS层积累 | `du -sh /var/lib/containerd/*` |
| I/O wait > 20% | 磁盘慢、脏页刷盘 | `iostat -xz`看await和%util |
| Pod写文件失败 | 挂载卷权限 | `kubectl exec`进去`ls -la`，检查`securityContext.fsGroup` |
| Too many open files | FD限制太低 | `ulimit -n`，`lsof -p <pid>` |

**K8s节点磁盘满标准流程：**
```bash
# 确认症状
kubectl describe node <node> | grep -A5 Conditions  # 看DiskPressure
kubectl get events | grep Evict                      # 有没有触发eviction

# 找大户
du -sh /var/lib/containerd/*    # 容器镜像和层
du -sh /var/log/pods/*          # pod日志
du -sh /var/lib/kubelet/pods/*  # pod volume

# 清理
crictl rmi --prune                                                  # 清理未使用镜像
journalctl --vacuum-size=500M                                       # 压缩系统日志
kubectl delete pod --field-selector=status.phase=Evicted -A        # 清理evicted pod
```

---

### How Kubernetes Uses Linux FS Features

| K8s功能 | 底层Linux机制 | 说明 |
|--------|-------------|------|
| 容器镜像 | **overlayFS** | 镜像只读层 + 容器可写层，containerd管理 |
| emptyDir（内存） | **tmpfs** | `medium: Memory`时挂载tmpfs，pod重启数据丢失，速度极快 |
| ConfigMap/Secret挂载 | **tmpfs + inotify** | kubelet监控变化，原子性重挂载 |
| hostPath | **bind mount** | host目录bind mount进pod的mount namespace |
| 本地PV | **bind mount** | 主机路径bind mount进pod |
| CSI存储（NFS/Ceph/EBS） | **FUSE或内核模块** | CSI driver负责挂载外部存储 |
| 资源限制（CPU/内存） | **cgroup FS** | kubelet写`/sys/fs/cgroup/<pod>/memory.max`等 |
| Pod隔离 | **mnt namespace** | 每个pod独立mount namespace，互相不可见 |
| 临时存储限制 | **du + eviction** | kubelet定期`du` overlayFS upper层，超限evict pod |
| 日志收集 | **symlinks + inode** | `/var/log/pods/<uid>/` → symlinks → overlayFS中的实际日志文件 |

**关键调试命令：**
```bash
# 进入容器FS namespace调试
PID=$(crictl inspect <container-id> | jq .info.pid)
nsenter -t $PID -m -- ls /

# 查看pod日志路径
ls -la /var/log/pods/<pod-uid>/
```

---

### Key Kernel Parameters

| 参数 | 用途 |
|------|------|
| `vm.swappiness` | swap激进程度（K8s节点设0） |
| `vm.dirty_ratio` | RAM可脏比例上限（超过阻塞写） |
| `vm.dirty_background_ratio` | 触发后台刷盘的阈值 |
| `fs.file-max` | 系统级FD上限 |
| `kernel.pid_max` | 最大PID数 |
| `net.core.somaxconn` | listen backlog最大值 |
| `net.ipv4.ip_local_port_range` | 临时端口范围 |
| `net.ipv4.tcp_tw_reuse` | 复用TIME_WAIT socket |

---

### CPU Performance Debugging

**CPU使用率分类（`vmstat 1` / `top` 核心字段）**

| 字段 | 含义 | 高→说明 |
|------|------|---------|
| `us` | 用户态CPU | 应用代码热点，找函数 |
| `sy` | 内核态CPU | 大量syscall（I/O、锁、fork） |
| `wa` | I/O wait | 不是CPU问题，是磁盘/网络瓶颈 |
| `st` | stolen（云VM） | 宿主机资源竞争，换机型或实例类型 |

**工具链（由粗到精）**

```bash
# 1. 系统级定位
top -d 1              # 找高CPU进程（P键排序）
htop                  # 多核视图，更直观
mpstat -P ALL 1       # 每个CPU核独立使用率（找热点核）
vmstat 1              # us/sy/wa/st整体分布

# 2. 进程级定位
pidstat -u 1 -p <pid>     # 进程的us/sy分解，1秒采样
strace -p <pid> -c        # 统计syscall分布和耗时（-c汇总）
strace -p <pid> -T -e trace=file  # 实时看文件相关syscall耗时

# 3. 函数级定位（perf）
perf top -p <pid>                         # 实时热点函数
perf record -g -p <pid> sleep 30          # 采样30秒带调用栈
perf report --stdio                        # 分析热点函数树
# 火焰图：perf record → perf script → flamegraph.pl → svg
```

**K8s CPU Throttling（最容易被忽视的陷阱）**

- 症状：`kubectl top pod` CPU < limit，但P99延迟很高，P50正常
- 原因：cgroup CPU quota周期性耗尽 → 进程在该周期内完全停止运行
- 诊断：

```bash
# 在节点上找pod的cgroup路径
cat /sys/fs/cgroup/cpu/kubepods/burstable/<pod-uid>/<container-id>/cpu.stat
# 看 nr_throttled（throttle次数）和 throttled_time（纳秒）
# nr_throttled 非0 = 存在throttling
```

- 处理：提高CPU limit；或对latency-sensitive服务**不设CPU limit**（throttling比无limit更伤延迟）

---

### Memory Debugging

**内存概念辨析**

| 指标 | 含义 | 看哪里 |
|------|------|--------|
| `VSZ` | 虚拟内存大小（含mmap、未分配） | 通常虚高，无意义 |
| `RSS` | 实际占用物理内存（含共享库） | `/proc/PID/status` VmRSS |
| `PSS` | RSS按比例分摊共享内存 | `smem` 命令 |
| `USS` | 进程独占的物理内存 | 内存泄露追踪最准确的指标 |

**工具链**

```bash
# 系统级
free -h                          # total/used/available
# MemAvailable比MemFree更准：包含可回收的page cache
cat /proc/meminfo | grep -E "MemAvailable|Slab|SwapUsed"
vmstat 1                         # si/so: swap in/out，非0就是问题

# 进程级
cat /proc/<pid>/status | grep -i vm    # VmRSS, VmSize, VmPeak
pmap -x <pid>                          # 内存映射详情（每个段RSS）
smem -s uss -r | head -20              # 按USS排序，找内存大户

# 内存泄露检测
watch -n 10 'ps -p <pid> -o rss='     # 观察RSS是否持续增长（10秒采样）
```

**OOMKill排查**

```bash
# 系统层面
dmesg | grep -E "oom|Out of memory|Killed"
journalctl -k --since "1 hour ago" | grep -i oom

# K8s层面
kubectl describe pod <pod> | grep -A5 "Last State"   # OOMKilled + exit code 137
kubectl get events --field-selector reason=OOMKilling

# oom_score：越高越先被杀（0~1000）
cat /proc/<pid>/oom_score
# K8s QoS对应的oom_score_adj：
# Guaranteed = -997（最不容易被杀）
# Burstable   = 2~999（按内存使用比例）
# BestEffort  = 1000（最先被杀）
```

**K8s内存保障机制**

- **memory.limit** → 触发OOMKill（cgroup级别，容器内的进程被SIGKILL）
- **Node内存压力** → kubelet Eviction（驱逐顺序：BestEffort → Burstable → Guaranteed）
- **防御**：request设合理值（调度依据）；limit不要设太低（会频繁OOMKill）；监控`container_memory_working_set_bytes` vs limit的比值

---

### Network Performance Debugging

**连接状态分析（`ss` 命令）**

```bash
ss -s                    # 连接数汇总（各状态总数）
ss -tunap                # 所有连接详情（-t tcp -u udp -n numeric -a all -p pid）
ss -tan | awk '{print $1}' | sort | uniq -c | sort -rn
# TIME_WAIT多：高并发短连接 → 考虑长连接或tcp_tw_reuse
# CLOSE_WAIT多：应用bug，对端关闭后本端未调用close()，连接泄露
```

**延迟分析**

```bash
# HTTP请求各阶段耗时
curl -w "\ndns:%{time_namelookup}s  connect:%{time_connect}s  ttfb:%{time_starttransfer}s  total:%{time_total}s\n" \
     -o /dev/null -s https://api.example.com
# dns: DNS解析时间（高→ndots:5或DNS服务慢）
# connect: TCP三次握手时间（高→网络延迟）
# ttfb: Time to First Byte（高→服务端处理慢）

# 路径追踪
mtr --report <host>          # 逐跳延迟+丢包（比traceroute实时）
traceroute -n <host>         # 路径跳数
```

**流量分析**

```bash
iftop -i eth0 -n             # 实时流量by连接（-n不反解DNS）
nethogs eth0                 # 实时流量by进程（找流量大户）
sar -n DEV 1                 # 网络接口收发统计（rxkB/s, txkB/s）
```

**抓包**

```bash
tcpdump -i eth0 -n port 8080                  # 抓指定端口
tcpdump -i any host <ip> -w /tmp/cap.pcap     # 抓所有接口，保存文件
tcpdump -i any 'tcp port 53'                  # 抓DNS
# 过滤SYN重传（找连接建立问题）
tcpdump -i eth0 'tcp[tcpflags] & tcp-syn != 0'
```

**带宽测试**

```bash
# 服务端
iperf3 -s -p 5201
# 客户端
iperf3 -c <server-ip> -p 5201 -t 30 -P 4    # -P 4: 4条并行流
# 结果看 sender/receiver Gbits/sec
```

**K8s网络场景排查**

```bash
# Pod能否到外网
kubectl exec <pod> -- ping -c3 8.8.8.8
kubectl exec <pod> -- curl -I --max-time 5 http://google.com

# Service访问不通的排查顺序
kubectl get endpoints <svc>                           # Pod Ready?
kubectl exec <pod> -- curl <pod-ip>:<port>            # 绕过Service直连Pod
kubectl exec <pod> -- curl <cluster-ip>:<port>        # 通过ClusterIP
iptables -t nat -L -n | grep <cluster-ip>             # kube-proxy规则存在?
kubectl logs -n kube-system -l k8s-app=kube-dns       # CoreDNS日志

# 节点间网络（CNI问题）
# 在pod里ping另一个节点上的pod
kubectl exec <pod-a> -- ping <pod-b-ip>
# 如果不通：检查CNI插件状态
kubectl get pods -n kube-system | grep -E "calico|cilium|flannel"
```

## Key Questions

**Q: "No space left on device"但磁盘空间没满，怎么排查？**
Answer framework: 先`df -i`确认是inode耗尽 → 找小文件密集的目录（日志、临时文件、K8s的pod目录）→ 清理或删除大量小文件 → 长期：限制日志大小、容器日志rotation。ext4创建时inode数量固定，只能清理，不能在线扩容。

**Q: 解释OverlayFS，容器写文件时发生了什么？**
Answer framework: upper层（可写）+ lower层（只读镜像）= merged视图 → 写操作触发Copy-on-Write：先从lower把文件复制到upper，再在upper修改 → 容器重启upper层清空，这就是为什么容器内写的文件重启后消失 → 要持久化必须挂载PV/emptyDir/hostPath。

**Q: K8s节点为什么必须关swap？**
Answer framework: cgroup内存限制靠OOMKill实现——容器超过memory limit时内核直接SIGKILL进程，K8s感知到重启pod，产生可见信号 → 有swap时容器可以超限把内存swap到磁盘，悄悄降速而不OOMKill，破坏K8s的内存保证和QoS语义；另外swap的性能代价（SSD ~100µs vs RAM ~100ns）对latency-sensitive workload完全不可接受。

**Q: K8s节点磁盘满了，一步步怎么排查？**
Answer framework: (1) `kubectl describe node`确认DiskPressure条件 → (2) `kubectl get events | grep Evict`看是否已触发eviction → (3) `du -sh /var/lib/containerd/*` + `/var/log/pods/*` + `/var/lib/kubelet/pods/*`找大户 → (4) 清理：`crictl rmi --prune`清镜像、`journalctl --vacuum`压缩日志、删除evicted pod → (5) 长期：配置log rotation、设置ephemeral-storage limit。

**Q: 什么是Page Cache？`free -h`里buff/cache很大是内存泄漏吗？**
Answer framework: 不是内存泄漏。Page Cache是内核把文件读写缓存在RAM里的机制，buff/cache大说明热数据都在内存，I/O命中率高，是好事 → 内核在需要内存时会自动回收page cache → 只有在buffer/cache增长同时available很低且应用开始OOM，才需要关注。

**Q: 用户态和内核态切换的开销，在K8s里有什么实际影响？**
Answer framework: 每次syscall = 2次模式切换约100ns；大量小文件I/O（每次write一个小buffer）会产生极高的syscall频率 → 用`strace -p <pid> -c`可以看到系统调用的CPU占比 → 优化：增大write buffer、使用异步I/O、减少文件系统round-trips；K8s里FUSE-based CSI driver因额外的用户态↔内核态切换，比原生内核FS慢。

**Q: emptyDir的`medium: Memory`和默认有什么区别，什么时候用哪个？**
Answer framework: 默认emptyDir = 节点磁盘上的目录，受`ephemeral-storage`限制，性能受磁盘影响 → `medium: Memory` = tmpfs（RAM），速度极快（内存速度），但占用节点可用内存，pod重启数据消失，没有`ephemeral-storage`限制但受`memory limit`约束 → 用Memory：需要极低延迟的临时数据（比如model serving的中间buffer）、多容器共享内存数据；用默认：数据量大、不在乎速度、需要避免占用节点内存。

**Q: 如何诊断K8s容器的I/O问题？**
Answer framework: (1) `kubectl top pod`看CPU/内存，但I/O不直接显示 → (2) `kubectl exec`进容器用`iostat -xz 1`看I/O wait和await → (3) 在节点上`iotop -o`找高I/O进程，定位到容器 → (4) 检查是overlayFS upper层写放大（CoW开销）、日志写入过频、还是PV挂载的后端慢 → (5) 如果是overlayFS CoW问题：把频繁写的目录挂载为emptyDir或PV，绕开overlayFS。

**Q: 线上服务CPU使用率突然飙高，怎么排查？**
Answer framework: (1) `top` 先看是us还是sy高 — us高说明应用代码热点，sy高说明syscall密集 → (2) `pidstat -u 1 -p <pid>` 确认是哪个进程 → (3) us高：`perf top -p <pid>` 看热点函数，或 `perf record -g` 生成火焰图，定位热点 → (4) sy高：`strace -p <pid> -c` 看哪个syscall最耗时，通常是频繁write小buffer（可以合并）或大量fork/clone → (5) 如果wa高（I/O wait）：不是CPU问题，转向磁盘I/O排查。K8s里还要检查是否CPU throttling（`cpu.stat`里`nr_throttled`非0）。
> 中文提示：us高找函数（perf），sy高找syscall（strace），wa高不是CPU问题，st高换宿主机

**Q: 容器内存持续增长，怎么判断是内存泄露还是正常缓存？**
Answer framework: 关键区分指标是`working_set_bytes`（不含可回收page cache）vs `rss`（含共享内存）→ 用`watch -n 10 'ps -p <pid> -o rss='`观察RSS是否单调递增且不回落 → 如果RSS持续增长且进程没有主动缓存数据，是内存泄露 → 工具：`smem`看USS（进程独占内存），`pmap -x <pid>`看各段的RSS，比对多个时间点的smaps文件 → K8s里看`container_memory_working_set_bytes`指标vs memory limit的比值，超过80%是警戒线。
> 中文提示：RSS单调递增且不回落 = 泄露嫌疑；USS = 独占物理内存（最准）；page cache会在内存压力下自动回收不算泄露

**Q: 生产环境TCP连接建立失败，怎么排查？**
Answer framework: (1) `ss -s` 看连接数总量，`ss -tan | grep SYN_RECV`看半连接队列积压 → (2) `netstat -s | grep "SYN to LISTEN"` 看SYN丢包统计 → (3) 半连接（SYN）队列满：调`net.ipv4.tcp_max_syn_backlog`；全连接（accept）队列满：调`net.core.somaxconn`并同时修改应用listen backlog → (4) 用`tcpdump`抓SYN包验证是否到达服务端 → (5) K8s里还要检查Service的endpoint是否ready，以及iptables/IPVS规则是否正确。
> 中文提示：SYN_RECV积压 = 半连接队列满；TIME_WAIT多 = 短连接高并发；CLOSE_WAIT多 = 应用bug

**Q: 两个Pod之间网络不通，排查步骤？**
Answer framework: (1) 先排除DNS：`kubectl exec <pod> -- nslookup <svc>` → (2) 用ClusterIP直接curl：`kubectl exec <pod> -- curl <cluster-ip>:<port>` → (3) 用Pod IP直接curl（绕过Service）：`kubectl exec <pod> -- curl <pod-ip>:<port>` → (4) 如果ClusterIP不通但PodIP通：kube-proxy问题，检查iptables规则 → (5) 如果PodIP也不通：CNI问题，检查CNI组件状态（`kubectl get pods -n kube-system`）、两节点间网络路由、NetworkPolicy是否误封 → (6) 抓包：`tcpdump -i any host <pod-ip>`在源节点和目标节点同时抓包对比。

## Summary

Linux文件系统和内核机制是K8s infra面试的核心基础，面试官通常从FS概念问到K8s实际troubleshooting场景。

**文件系统层**：每个文件由inode（元数据）和数据块组成，文件名只存在目录项里——这个分离导致了inode耗尽（磁盘空间充足但`df -i`满了）这个经典陷阱。VFS抽象层让不同类型的FS对应用透明，K8s正是利用VFS在一个pod里同时挂载overlayFS（容器镜像）、tmpfs（emptyDir memory）、bind mount（hostPath/PV）。OverlayFS是容器镜像分层的实现：lower层（只读镜像层）+ upper层（容器可写层）= merged视图，写操作触发Copy-on-Write，容器重启upper层清空。理解这个机制是解释"为什么容器重启数据消失"的标准答案，也是排查节点磁盘满（overlayFS层积累）的基础。

**内核机制层**：用户态和内核态的分离是Linux安全模型的基础，syscall是唯一合法入口，容器共享host kernel意味着seccomp（syscall白名单）和privilege control是容器安全的核心手段。Swap在K8s节点上必须关闭，原因不是性能（虽然SSD swap也比RAM慢1000倍），而是语义正确性——cgroup内存限制依赖OOMKill，有swap会悄悄绕过内存保证。

**Triage方法论**：Observe（`df -h/i`, `iostat`, `dmesg`）→ Isolate（`iotop`, `lsof`, `findmnt`）→ Root Cause → Fix。K8s节点磁盘满的三大来源：容器镜像（`/var/lib/containerd`）、pod日志（`/var/log/pods`）、pod volume（`/var/lib/kubelet/pods`），清理工具分别是`crictl rmi --prune`、`journalctl --vacuum`、删除evicted pod。

## Key Terms

**Kernel / User mode**
- `Ring 0` · `Ring 3` · `syscall` · `mode switch (~100ns)` · `seccomp` · `CAP_SYS_ADMIN` · `privileged container` · `eBPF` · `FUSE`

**File System types**
- `ext4` · `XFS` · `tmpfs` · `overlayFS` · `proc` · `sysfs` · `cgroup FS` · `devtmpfs`

**FS core concepts**
- `inode` · `data block` · `directory entry` · `hard link` · `soft link / symlink`
- `VFS` · `file descriptor (FD)` · `ulimit -n` · `fs.file-max` · `lsof`
- `page cache` · `dirty page` · `vm.dirty_ratio` · `vm.dirty_background_ratio` · `pdflush`
- `mount namespace` · `bind mount` · `nsenter`

**OverlayFS**
- `lower dir (read-only)` · `upper dir (read-write)` · `merged dir` · `Copy-on-Write (CoW)` · `whiteout file`
- `containerd` · `container layer` · `image layer`

**Swap**
- `vm.swappiness` · `swapoff -a` · `OOMKill` · `oom_score_adj` · `Guaranteed (-997)` · `BestEffort (1000)`
- `cgroup memory limit` · `memory.max`

**Triage commands**
- `df -h` · `df -i` · `du -sh` · `iostat -xz` · `dmesg` · `iotop` · `lsof +D` · `findmnt`
- `crictl rmi --prune` · `journalctl --vacuum` · `kubectl describe node` · `kubectl get events`

**K8s FS integration**
- `emptyDir` · `medium: Memory` · `hostPath` · `ephemeral-storage limit`
- `CSI driver` · `PersistentVolume` · `bind mount` · `inotify`

**CPU debugging**
- `us / sy / wa / st` · `vmstat` · `mpstat -P ALL` · `pidstat -u`
- `perf top` · `perf record -g` · `perf report` · `flame graph`
- `strace -c` · `strace -T` · `cpu.stat` · `nr_throttled` · `throttled_time`
- `CPU limit throttling` · `leave CPU limit unset for latency-sensitive`

**Memory debugging**
- `VSZ` · `RSS` · `PSS` · `USS` · `VmRSS` · `smem` · `pmap -x`
- `MemAvailable` · `Slab` · `working_set_bytes`
- `OOMKill` · `exit code 137` · `oom_score` · `oom_score_adj`
- `memory.limit` · `BestEffort(1000)` · `Guaranteed(-997)`
- `dmesg | grep oom` · `watch rss`

**Network debugging**
- `ss -tunap` · `ss -s` · `TIME_WAIT` · `CLOSE_WAIT` · `SYN_RECV`
- `mtr` · `traceroute` · `tcpdump` · `iperf3` · `nethogs` · `iftop`
- `curl -w time_namelookup/time_connect/time_starttransfer`
- `net.ipv4.tcp_max_syn_backlog` · `net.core.somaxconn`
- `listen backlog` · `accept queue` · `SYN queue`

**Kernel params**
- `vm.swappiness` · `vm.dirty_ratio` · `fs.file-max` · `net.core.somaxconn` · `net.ipv4.tcp_tw_reuse`

## Raw Material
- [[raw_material/books/tiktok-prep/linux-network-prep]]
- Derived from: `[[jobs/TikTok/prep/2026-05-29-round1-linux-network-prep]]`
