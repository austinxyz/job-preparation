---
title: System Design Case - Online Judge (LeetCode)
category: tech/system-design
tags: [system-design-case, sandboxing, containerization, redis, leaderboard, message-queue, security]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# System Design Case - Online Judge (LeetCode)

## Knowledge Map
- 前置知识：Linux containers, seccomp profiles, Redis sorted sets, SQS/Kafka, auto-scaling, circuit breakers
- 延伸话题：code plagiarism detection, multi-language runtime management, distributed tracing for execution, contest fairness (anti-cheat)
- 管理关联：

## Core Concepts

- **Language-Specific Execution Queues**: A single queue for all languages creates head-of-line blocking (slow Java submissions delay fast Python ones). Partitioned queues per language allow each language's executor pool to scale independently based on that language's queue depth and execution time characteristics.
- **Container Sandbox with seccomp**: User code is untrusted. Containers enforce: CPU/memory/storage limits, read-only filesystem, network isolation, and restricted system calls via **seccomp profiles** (Linux kernel feature that whitelists allowed syscalls). This stops malicious code from accessing host resources or other users' submissions.
- **Redis Sorted Set for Live Leaderboard**: `ZADD competition:id score userId` on each accepted submission. `ZRANGE` retrieves the top N with O(log N + N) complexity. For "find my rank": maintain a separate Redis hash `userId → score`, then use `ZRANK` to get position. This avoids scanning the full sorted set.
- **Polling vs. WebSocket for Results**: Code execution is async (seconds to complete). Polling via AJAX every few seconds is simpler and stateless on the server side. WebSocket adds complexity. For competitions where latency matters more, SSE/WebSocket can push results when ready.
- **SQS Visibility Timeout for Crash Recovery**: If an executor crashes mid-execution, the SQS message becomes visible again after the visibility timeout and is redelivered to another executor. No separate dead-letter mechanism needed for the normal crash case.
- **Circuit Breaker for Spike Handling**: During competitions, sudden submission spikes can exhaust the executor pool. A circuit breaker stores excess submissions in secondary storage (overflow queue or DB) and resumes processing as executors become available, rather than dropping requests or causing cascading failures.
- **Runtime Security Monitoring**: Falco monitors for suspicious syscalls at runtime (beyond seccomp static filtering). auditd provides system-level audit logs. Prometheus with custom metrics tracks container resource anomalies (unexpected CPU spikes from crypto-mining attempts, etc.).

## Key Questions

**Q: How do you prevent user-submitted code from harming your system or other users' submissions?**
Answer framework: Multi-layer isolation. Container per execution (not shared): CPU/memory/storage limits enforced by cgroup. Read-only filesystem. Network access blocked. seccomp profile whitelists only the syscalls needed for the language runtime (e.g., read, write, exit — not fork, execve, socket). Runtime monitoring with Falco catches evasion attempts. VMs provide stronger isolation but are too slow for fast feedback.

**Q: A competition starts and 50,000 users submit code simultaneously. How does the system handle the spike?**
Answer framework: Auto-scaling executor containers based on queue depth (not CPU, which lags). Language-specific queues let each language scale independently. A warm pool of base containers is always running to absorb initial burst. Circuit breaker stores overflow in secondary storage rather than dropping. SQS visibility timeout ensures no submission is lost if an executor crashes during the spike.

**Q: How do you build a leaderboard that updates in real-time during a competition without page refreshes?**
Answer framework: Redis sorted set per competition. On each accepted submission: ZADD with score. Client polls via AJAX every few seconds (lightweight, stateless). For the user's own rank: Redis hash for score lookup + ZRANK. For very large competitions, pagination with ZRANGE BYSCORE limits result size. WebSocket/SSE as upgrade path if sub-second updates are required.

**Q: What happens if a code execution takes forever (infinite loop)?**
Answer framework: Each container has a hard execution timeout (e.g., 2-3 seconds for most problems). The container orchestrator kills the container after the timeout. The executor returns a "Time Limit Exceeded" result to the Solution Service. The container is then destroyed and a fresh one is allocated (preventing state leakage from long-running processes).

**Q: Why use language-specific queues instead of a single shared queue?**
Answer framework: Different languages have different execution times (Python scripts are fast, JVM startup adds latency). A single queue with mixed jobs creates unfair head-of-line blocking. Language-specific queues allow: independent scaling of executor pools, language-specific timeout tuning, and fairness between language communities during competitions.

**Q: How would you handle a competition where results must be final (no retroactive corrections)?**
Answer framework: Freeze leaderboard writes at competition end time. Any in-flight submissions at end time are still processed but scored with a "late" flag. The leaderboard Redis set is snapshotted to the DB at end time. Idempotent submission IDs prevent duplicate scoring if a result is redelivered after snapshot.

## Summary

An online judge must execute user-submitted code safely, efficiently, and at scale — especially during timed competitions where thousands of users submit simultaneously. Core requirements: multi-language code execution, correctness checking against test cases, real-time leaderboard, and isolation guaranteeing one user's code cannot affect others.

The security-first design constraint shapes everything: execution happens in containers (not bare VMs for speed) with seccomp profiles restricting syscalls, read-only filesystems, and strict resource limits. The container lifecycle is short — one execution per container to prevent state leakage. Language-specific queues allow independent auto-scaling based on queue depth, handling submission spikes without cross-language interference.

The leaderboard is a canonical Redis sorted set problem. The non-obvious piece is the user rank lookup: maintaining a userId→score hash allows O(1) score lookup, then ZRANK gives O(log N) rank — avoiding a full scan. The interview often probes the spike handling path: interviewers want to see circuit breakers and overflow storage rather than just "add more servers," and the resilience path when executors crash (SQS visibility timeout, not custom retry logic).

## Key Terms

**Technologies**
- `Linux Containers` · `seccomp` · `Redis Sorted Sets` · `SQS` · `Falco` · `Prometheus` · `AWS Lambda`

**Patterns**
- `Language-Specific Queues` · `Container Sandbox` · `Circuit Breaker + Overflow Storage` · `SQS Visibility Timeout for Crash Recovery`

**Decision Points**
- `container vs. VM isolation` · `polling vs. WebSocket for results` · `single queue vs. per-language queues` · `execution timeout enforcement`

## Raw Material
- [[raw_material/tech/system-design/hello-interview/case-leetcode.md]]
