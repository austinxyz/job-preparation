---
title: "Hello Interview — Case: Distributed Job Executor"
source: "https://www.notion.so/1e3afa27ec7280ee8b7ce90c264e0e1f"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/System Design Case - Distributed Job Executor]]"
---

# Case: Distributed Job Executor

## Key Design Questions & Answers

### How will users view the status of all their scheduled or executed jobs?

Use userId as global second index:
- Row Key: userId
- Column Key: time + jobId
- Query job to find all jobs for one user; query execution with status (in progress, completed, failed) to find scheduled or executed jobs

### How to ensure system executes jobs within 2s of scheduled time?

1. Add a job scheduler to watch Job DB; get all jobs to execute every 5 minutes
2. Put jobs into message queue (AWS SQS); use SQS delivery delay feature to ensure message delivery at right time
3. For new jobs requiring execution within 5 minutes, Job service directly adds to message queue with small delay
4. Job executor handles jobs in Job queue
5. For jobs >5 minutes, let job scheduler calculate and handle specially

### Edge case: Jobs scheduled >5 minutes but before next scheduler run

Problem: A job scheduled to run in 7 minutes would be missed by the current scheduler run and only picked up 5 minutes later, potentially executing 3 minutes late.

Solutions:
- Sliding window approach: scheduler looks ahead slightly beyond its interval
- Job creation process calculates whether a job falls into this gap and handles it specially

### How to scale job execution to support up to 10,000 concurrent jobs?

1. Split Job creation service and job query service; add API gateway for microservices
2. Job creation service leverages LB and auto-scaling
3. Cassandra and SQS support large scale natively
4. Hundreds of job executors in containers; init base loads (10 servers warm up); set CPU/memory/storage constraints per container
5. AWS ECS or Kubernetes scale up/down containers based on queue depth
6. Router assigns jobs to right executor based on resource consumption and historical data

### How to handle retrying failed jobs?

1. Multiple failure modes:
   - Job execution failed: update status with retry count (max 3 times), put back into queue with exponential delay → Dead Letter Queue after hitting limit
   - Job executor dead: add global lock in Redis with TTL; router checks Redis before reassignment; if expired, reassign to another executor

### Fault Tolerance

Use Redis global lock:
- When router assigns a job to an executor, add a record into Redis global lock cache with TTL
- Router checks if message exists in Redis cache; if it does → no assignment; if expired → reassign to other executor
