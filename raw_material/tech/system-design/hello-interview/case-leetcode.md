---
title: "Hello Interview — Case: LeetCode (Online Judge)"
source: "https://www.notion.so/1e8afa27ec72805ea06cfab49990f222"
date_saved: 2026-05-14
processed: true
skill_note: "[[skills/tech/system-design/System Design Case - Online Judge (LeetCode)]]"
---

# Case: LeetCode (Online Judge)

## Key Design Questions & Answers

### Code Execution Flow

1. User submits code → Solution Service picks up executor
2. Language executor = container with sandbox environment + language runtime; runs test cases; collects result (correctness, execution time, memory)
3. Executor returns result to Solution Service → stored in Problem DB → shown to user

### Live Leaderboard for Competitions

1. Competition Service handles live leaderboard
2. User submits solution → Solution Service → language executor → result + score
3. Create Redis sorted set per competition; score + user stored via ZAdd
4. Competition Service queries sorted set for live leaderboard

**Efficient leaderboard updates**: Redis sorted set API; AJAX fetches leaderboard every few seconds without page refresh. For specific user rank: keep key/value map in Redis (key=user, value=score) → find score → find ranking in sorted set.

### Isolation and Security for User Code Execution

1. Virtualization for isolation:
   - Setup timeouts to prevent resource exhaustion
   - Config CPU/memory/storage constraints
   - Setup readonly filesystem
   - Network access restrictions
   - Limit system calls via **seccomp profile** (Linux kernel feature restricting syscalls)
2. Options: VMs (heavyweight, runs guest OS), Containers (lightweight, perfect for above setup), AWS Lambda/serverless

**Monitoring tools**: Falco for runtime security monitoring (suspicious syscalls), auditd for system-level auditing, Prometheus with custom metrics for container resource anomalies.

### Scale to Handle Spikes During Competitions

1. API Gateway + LB distributes to stateless Solution Service instances (auto-scaling on CPU/memory)
2. **Queue per language**: SQS or Kafka for submissions; language-specific queues
3. GET API to poll submission status; AJAX polls for result
4. Language executor containers consume from their language queue; scale based on queue size
5. Circuit break for extreme cases: store message in secondary storage; resume when more executors ready
6. If executor crashes: SQS visible timeout reassigns unacknowledged message to another executor

### Leaderboard Real-Time Updates (no page refresh)

1. Redis sorted set for scores (ZAdd on result)
2. Client fetches leaderboard via AJAX every few seconds (polling)
3. Find user rank: key/value map in Redis → score → rank in sorted set
