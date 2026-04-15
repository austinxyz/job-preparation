---
title: 系统设计 - Job Scheduler
source:
date_saved: 2026-04-11
processed: false
skill_note:
---

# 系统设计 - Job Scheduler

<!-- Paste original article content below. Do not edit — keep raw. -->
<!-- Run raw-material-processor skill to distill this into the linked skill note. -->
Requirement
- schedule jobs, immediately or future, recurring schedule
- monitor status
NFR
- high availabilty
- immediately - within 2s
- scalability
- at-least-once
Deepdive
- within 2 second， job DB, cron job to query and put to Message Queue -> SQS （Delayed message delivery）, < 5min, directly sent to SQS
- 10k jobs, 
	- Queue, JobDB (DynomoDB/Cassandra), partition key - job_id (Jobs), time_bucket(Execution)
	- SQS - not special configuration
	- Workers - container/lambda
	- At-least-once, 
		- visible failure - update job status, retry
		- invisible failure - worker crash - SQS visibility timeout, extend the timeout
		Job needs idempotent
![[raw_material/tech/system-design/images/jobscheduler.png]]