---
title: System Design Case - Distributed Job Executor
category: tech/system-design
tags: [system-design-case, distributed-systems, message-queue, redis, scheduling, fault-tolerance]
status: draft
priority: high
last_updated: 2026-05-14
created_from_jd: ""
---

# System Design Case - Distributed Job Executor

## Knowledge Map
- 前置知识：message queues (SQS/Kafka), Redis distributed locks, cron scheduling, container orchestration (ECS/K8s), wide-column databases (Cassandra)
- 延伸话题：DAG-based workflow schedulers (Airflow), at-least-once vs. exactly-once delivery, distributed locking patterns, dead letter queues
- 管理关联：

## Core Concepts

- **Two-Tier Scheduling (Scheduler + Queue)**: A job scheduler polls the Job DB every 5 minutes for upcoming jobs and enqueues them into SQS with a delivery delay. This decouples scheduling logic from execution. Jobs needed within 5 minutes bypass the scheduler and are enqueued directly by the Job Service — preventing the "gap window" problem.
- **SQS Delivery Delay for Precision Timing**: Rather than building a custom delay mechanism, SQS's native delivery delay feature handles deferred message delivery. This achieves ~2-second execution precision without requiring a timer service.
- **Sliding Window Gap Problem**: A job scheduled 7 minutes from now will be picked up by the current scheduler run, but a job scheduled in 3 minutes will be missed if the scheduler just ran. Solution: the job creation path calculates whether a job falls in the gap window and enqueues it directly.
- **Redis Global Lock for Executor Fault Tolerance**: When a router assigns a job to an executor, it writes `key=jobId, value=executorId` to Redis with a TTL. If the executor dies, the TTL expires and the router can reassign. This prevents both double-execution and job loss.
- **Exponential Backoff Retry + Dead Letter Queue**: Failed jobs are retried up to 3 times with exponential delay. After hitting the retry limit, they go to a DLQ for manual inspection or alerting. Retry count is tracked in the Job DB.
- **Container-Based Horizontal Scaling**: Job executors run as containers (ECS/K8s). A base pool of ~10 warm containers handles steady-state load. Auto-scaling triggers based on queue depth. CPU/memory/storage constraints per container prevent resource interference between jobs.
- **Wide-Column DB for Job Queries**: Cassandra with `userId` as partition key and `time + jobId` as clustering key allows efficient per-user job history queries. Secondary indexes support status-based queries (in-progress, completed, failed).

## Key Questions

**Q: How do you ensure a scheduled job runs within 2 seconds of its scheduled time?**
Answer framework: Use SQS delivery delay — the job is enqueued ahead of time with the exact delay calculated to target execution time. For high precision, the scheduler runs frequently (every 5 minutes) and jobs due within that window are pre-queued with calculated delays. Jobs needed immediately bypass the scheduler entirely.

**Q: What is the "gap window" problem and how do you fix it?**
Answer framework: If the scheduler runs every 5 minutes and a new job is created that's due in 3 minutes, the scheduler just ran and won't pick it up for another 5 minutes (2 minutes late). Fix: job creation calculates if execution time falls within the next scheduler interval, and if so, enqueues directly to SQS with the appropriate delay.

**Q: How do you handle a job executor that dies mid-execution?**
Answer framework: Redis distributed lock with TTL. Router writes `jobId → executorId` to Redis when assigning. If executor dies, the lock expires. Router detects missing heartbeat or expired lock and reassigns to another executor. The job's status in DB stays "in-progress" until acknowledged, preventing silent loss.

**Q: How would you scale to 10,000 concurrent jobs?**
Answer framework: Separate job creation and query services. Job executors are stateless containers scaled by queue depth (ECS/K8s auto-scaling). Cassandra and SQS both scale natively. A router layer assigns jobs based on resource consumption history. Warm pool of ~10 base containers minimizes cold-start latency for burst jobs.

**Q: How do you prevent a job from running twice if it's in both the queue and a retry?**
Answer framework: Track job execution state in the DB (status + retry count). Redis lock prevents concurrent assignment. SQS visibility timeout ensures messages aren't visible to other consumers while in-flight. Idempotency key on the job record allows detecting re-delivery.

**Q: How would you support job dependencies (Job B runs after Job A completes)?**
Answer framework: This evolves the problem into a DAG scheduler (like Airflow). Each job tracks its dependencies in the DB. A dependency resolver checks completion status before enqueuing downstream jobs. This requires an event/completion notification path (Job A completion triggers dependency resolution).

## Summary

A distributed job executor must reliably schedule and run jobs within a 2-second window of their scheduled time, supporting up to 10,000 concurrent jobs with fault tolerance. The core components are: Job Service (CRUD), a periodic Scheduler (polls every 5 minutes), SQS as the job queue, and containerized Job Executors behind a Router.

The key scheduling insight is the two-tier approach: the scheduler handles jobs more than 5 minutes out, while the Job Service directly enqueues near-term jobs with SQS delivery delay for precision. This prevents the gap window problem where a just-created job misses the current scheduler run. SQS delivery delay eliminates the need for a custom timer service.

The interview tests whether candidates think about fault tolerance at every layer: executor crashes (Redis TTL lock + reassignment), failed jobs (retry with exponential backoff + DLQ), and scheduling gaps (direct enqueue path). The Redis global lock pattern — writing a record with TTL at assignment time — is a recurring pattern across multiple system design problems (Uber, TicketMaster) and worth mastering.

## Key Terms

**Technologies**
- `SQS` · `Redis` · `Cassandra` · `ECS / Kubernetes` · `Dead Letter Queue`

**Patterns**
- `Two-Tier Scheduling` · `SQS Delivery Delay` · `Redis Distributed Lock + TTL` · `Exponential Backoff` · `Auto-Scaling on Queue Depth`

**Decision Points**
- `scheduler poll interval vs. direct enqueue` · `gap window handling` · `retry limit + DLQ` · `container warm pool sizing`

## Raw Material
- [[raw_material/tech/system-design/hello-interview/case-distributed-job-executor.md]]
