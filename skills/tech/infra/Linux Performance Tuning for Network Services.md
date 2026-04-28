---
title: Linux Performance Tuning for Network Services
category: tech/infra
tags: [linux, performance, sched-fifo, tcp-fast-open, tfo, tls-session-resumption, listen-backlog, memcached, latency, p99, scheduling, kernel]
status: in-progress
priority: high
last_updated: 2026-04-27
created_from_jd: "[[jobs/Manager II, Engineering - Infra - Pinterest]]"
---

# Linux Performance Tuning for Network Services

## Knowledge Map
- 前置知识：[[Linux Systems and Internals]], [[Networking Fundamentals]]
- 延伸话题：[[Memcached]], [[SRE Practices and SLO Engineering]], [[Observability and Incident Management]]
- 管理关联：infrastructure cost optimization, P99 SLO, fleet capacity planning

## Core Concepts

### Overview: Four Stacked Optimizations (Pinterest 2022 Case Study)

Pinterest published a 2022 blog (*Kevin Lin, "Improving Distributed Caching Performance and Efficiency at Pinterest"*) describing four OS/network-level optimizations that together achieved **~10% fleet cost reduction + 20% CPU ceiling increase** across their ~5,000-node memcached fleet. Each optimization is individually modest — the value is in stacking them.

| # | Optimization | Benefit | Complexity |
|---|---|---|---|
| 1 | **SCHED_FIFO real-time scheduling** | P99 latency -10–40%, CPU ceiling +20%, cost -10% | High (operational discipline required) |
| 2 | **TCP Fast Open (TFO)** | TCP connection duration -~10% | Medium (middlebox compatibility) |
| 3 | **Listen backlog tuning** | Availability under burst connections | Low (parameter tuning) |
| 4 | **TLS session resumption** | Connection timeout rate reduction | Medium (TLS stack adaptation) |

---

### 1. SCHED_FIFO Real-Time Scheduling

#### Linux Scheduler Hierarchy

```
High priority ─────────────────────────────────── Low priority

Real-time (RT) policies              Normal policies
┌──────────────┐ ┌──────────┐       ┌──────────────┐
│SCHED_DEADLINE│ │SCHED_FIFO│       │SCHED_OTHER   │
│(EDF, rare)   │ │(RT FIFO) │       │(CFS, default)│
└──────────────┘ └──────────┘       └──────────────┘
                     ↑                    ↑
               Pinterest uses        Default
```

RT policies (priority 1–99) **always preempt** SCHED_OTHER (CFS) regardless of CFS priority.

#### Why P99 Is Dominated by Scheduling Jitter

A memcached request lifecycle:
```
Request arrives → thread wakes from sleep → waits for CPU ← P99 killer
→ runs (read socket → hash key → lookup → write socket) → sleeps
```

Under CFS, P99 jitter sources:
| Source | Frequency | P99 impact |
|---|---|---|
| Timeslice preemption | Every few ms | Context switch ~1–10 μs |
| Co-tenant processes (monitoring, logging) | Each time a neighbor runs | 10s–100s μs |
| CPU migration (cache miss) | CFS load balancing | L1/L2 cold start ~10s μs |
| kworker / softirq interruption | Each kernel background activity | μs–10s μs |

P50 doesn't show these — most requests don't encounter them. P99 is dominated by them.

#### How SCHED_FIFO Eliminates Jitter

A SCHED_FIFO thread only stops for:
1. Voluntary yield (I/O block, sleep, futex wait)
2. Higher-priority RT thread preemption
3. System crash

It is **never** stopped by timeslice expiry (SCHED_FIFO has no timeslice) or CFS threads.

Effect: P50 stays the same (already near physical floor of network + memory access), P99 tightens dramatically.

```
Under CFS:      P50 = 150 μs,  P99 = 1500 μs   (P99/P50 = 10×)
Under SCHED_FIFO: P50 = 150 μs,  P99 = 900 μs   (P99/P50 = 6×, P99 -40%)
```

#### CPU Ceiling +20% Mechanism

Traditional services cap CPU at 70–80% because CFS queuing makes tail latency grow non-linearly beyond that. SCHED_FIFO decouples the service thread from system load — can push to 90%+ while maintaining latency targets. Same throughput on 10% fewer nodes.

#### Trade-offs

| Risk | Implication | Mitigation |
|---|---|---|
| **System starvation** | SCHED_FIFO loop → starves all normal processes including sshd | Kernel `sched_rt_runtime_us` caps RT at 95% by default (leaves 5% for CFS) |
| **CAP_SYS_NICE required** | Only root or processes with this capability can set RT scheduling | K8s: `securityContext.capabilities.add: ["SYS_NICE"]` |
| **No multi-RT co-tenancy** | Two SCHED_FIFO apps on the same host compete for CPU | Dedicated nodes, single RT application per host |
| **Bug amplification** | CFS loop: CPU pegged but machine alive; SCHED_FIFO loop: machine unreachable | Watchdog + health check + capability revocation |

#### Configuration

```bash
# Direct launch
chrt -f 50 /usr/local/bin/memcached ...    # -f = SCHED_FIFO, 50 = RT priority

# systemd service
[Service]
CPUSchedulingPolicy=fifo
CPUSchedulingPriority=50

# Verify RT throttling
cat /proc/sys/kernel/sched_rt_runtime_us   # default 950000 (95%)
cat /proc/sys/kernel/sched_rt_period_us    # default 1000000 (1s window)
```

**K8s pod:**
```yaml
securityContext:
  capabilities:
    add: ["SYS_NICE"]
# Then in entrypoint: exec chrt -f 50 memcached
```

---

### 2. TCP Fast Open (TFO)

#### Problem

Standard TCP three-way handshake adds 1 RTT before data can be sent:
```
Client ── SYN ──────────────→ Server
Client ←── SYN+ACK ────────── Server
Client ── ACK + data ────────→ Server   ← data only after 1 RTT
```

For short-lived connections (cache lookups, API calls), this 1 RTT is pure overhead.

#### Solution

First connection: normal handshake + server sends TFO cookie to client.

Subsequent connections (cookie in hand):
```
Client ── SYN + cookie + data →  Server   ← data in SYN itself!
Client ←── SYN+ACK + response ── Server
```

Saves 1 RTT. Pinterest achieved ~10% reduction in average TCP connection duration.

#### Trade-offs

| Risk | Implication |
|---|---|
| **Middlebox compatibility** | Some NATs/firewalls drop SYN packets with data (non-standard) → connection failures |
| **Replay attacks** | SYN with data can be replayed → non-idempotent operations could execute twice |
| **Cookie management** | Client must maintain cookie list; stale cookies need eviction |

```bash
sysctl -w net.ipv4.tcp_fastopen=3   # 3 = client + server mode
```

---

### 3. Listen Backlog Tuning

#### Mechanism

```
New connection arrives
  → kernel places in accept queue (listen backlog)
  → application calls accept() to dequeue
  → handles request
```

If `accept()` can't keep up → queue fills → kernel drops new SYNs → "connection refused" or timeout.

#### Default Problem

Kernel default `somaxconn` was 128 in older Linux (4096 in Linux 5.4+). Application's `listen(sockfd, backlog)` is limited by `min(app_backlog, somaxconn)`.

During burst connection events (service restart causing mass reconnect), 128 connections in queue is severely insufficient.

#### Configuration

```bash
# System
sysctl -w net.core.somaxconn=65535
sysctl -w net.ipv4.tcp_max_syn_backlog=65535
sysctl -w net.ipv4.tcp_syncookies=1     # SYN flood protection (must enable)

# memcached
memcached -b 65535 ...
```

---

### 4. TLS Session Resumption

#### Problem

Full TLS handshake = 2 RTTs + expensive asymmetric crypto (RSA/ECDH, certificate verification, key derivation) — CPU-intensive, especially with mutual authentication (both sides present certificates).

#### Session Resumption Mechanisms

**(a) Session ID** — server maintains session cache; client presents ID to skip crypto on reconnect.

**(b) Session Ticket** — server encrypts session state into a ticket the client stores. Stateless on server; any server can decrypt with shared ticket key.

```
Client ── ClientHello + ticket/session_id →  Server
Client ←── ServerHello + Finished ────────── Server   ← 1 RTT, almost no crypto
Client ── Finished ──────────────────────────→ Server
```

Saves ~1 RTT + most crypto overhead. Pinterest observed reduced fleet-wide client-side connection timeout rates, particularly important with mutual TLS + SPIFFE identity.

#### Trade-offs

| Risk | Implication |
|---|---|
| **Ticket key rotation** | Session tickets use symmetric key; key must rotate periodically; existing tickets invalidate on rotation |
| **PFS trade-off** | Resumption reuses key material; if ticket key leaks, past sessions decryptable (TLS 1.3 mitigates) |
| **Ticket key cross-server sync** | Multi-server deployments need shared ticket key distribution |

---

## Key Questions

**Q: Why does SCHED_FIFO improve P99 but not P50?**
Answer framework: P50 requests don't encounter scheduling jitter — they run near the physical floor (network round-trip + memory access). P99 requests are precisely the ones that hit scheduler preemption, co-tenant interference, or CPU migration events. SCHED_FIFO eliminates those sources entirely. Physical floor stays the same; the jitter tail disappears.

**Q: What's the CPU ceiling mechanism for SCHED_FIFO?**
Answer framework: Under CFS, services must cap CPU at 70–80% because queuing makes tail latency non-linear beyond that — so throughput-per-dollar plateaus. SCHED_FIFO decouples the service from system load, so it can run to 90%+ without the latency cliff. Same fleet achieves 20% more throughput per node → 10% fewer nodes for the same workload.

**Q: What are the risks of SCHED_FIFO in production?**
Answer framework: Three: (1) A SCHED_FIFO thread in a bug loop starves all normal processes including SSH — mitigated by `sched_rt_runtime_us` (default 95% cap). (2) Requires CAP_SYS_NICE — needs explicit container/K8s capability grant. (3) No multi-RT co-tenancy — dedicated nodes only. The ROI justifies it at Pinterest scale (5,000 nodes); below ~200 nodes probably not worth the operational overhead.

**Q: What other OS-level optimizations would you consider for high-throughput cache services?**
Answer framework: The Pinterest 2022 stack: SCHED_FIFO (P99 reduction + CPU headroom), TCP Fast Open (1 RTT saved on short connections), listen-backlog tuning (burst absorb), TLS session resumption (crypto overhead reduction). Each is 1–10% alone; stacked they produce order-of-magnitude improvements. All are lower-risk on dedicated nodes vs multi-tenant environments.

**Q: How does listen-backlog relate to SYN flood protection?**
Answer framework: `tcp_syncookies=1` must be enabled when increasing `somaxconn` — it provides SYN flood mitigation by encoding connection state in the SYN-ACK cookie, so the listen queue isn't consumed by flood. Without it, a large backlog is actually a larger attack surface.

## Key Terms

`SCHED_FIFO` · `SCHED_OTHER` · `CFS (Completely Fair Scheduler)` · `RT priority` · `sched_rt_runtime_us` · `CAP_SYS_NICE` · `chrt` · `TCP Fast Open (TFO)` · `TFO cookie` · `listen backlog` · `somaxconn` · `tcp_max_syn_backlog` · `tcp_syncookies` · `TLS session resumption` · `session ticket` · `session ID` · `mutual TLS` · `SPIFFE` · `P99 latency` · `scheduling jitter` · `context switch` · `CPU ceiling` · `fleet cost optimization`

## Summary

Four stacked OS/network-level optimizations proven at Pinterest's 5,000-node memcached fleet:

**SCHED_FIFO** is the highest-impact lever — it eliminates the scheduling jitter sources (timeslice preemption, co-tenant interference, CPU migration) that dominate P99 latency while leaving P50 unchanged. The secondary effect — decoupling service performance from system load — pushes the CPU utilization ceiling from ~80% to ~90%, enabling the same workload on 10% fewer nodes. The operational cost is real: dedicated nodes, CAP_SYS_NICE capability, watchdog discipline.

**TCP Fast Open** saves 1 RTT on connection establishment for short-lived connections. The 10% improvement in connection duration directly affects workloads with frequent reconnects (cache burst, service restarts). The main risk is middlebox incompatibility in environments with non-standard NAT/firewall behavior.

**Listen backlog tuning** is the simplest: increase `somaxconn` and the application backlog parameter to absorb burst connection storms that would otherwise cause SYN drops. Must pair with `tcp_syncookies=1` for SYN flood protection.

**TLS session resumption** (session ID or ticket) eliminates the asymmetric crypto cost of repeated full handshakes, particularly valuable under mutual TLS where both sides verify certificates. Pinterest used this to reduce fleet-wide connection timeout rates for their mTLS + SPIFFE identity configuration.

## Raw Material
- Source: Kevin Lin, "Improving Distributed Caching Performance and Efficiency at Pinterest" (May 2022)
- Derived from: `[[jobs/Pinterest/prep/performance-tuning-deep-dive]]`
