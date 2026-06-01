Design a video moderation system for a global platform like TikTok that can ingest millions of daily video uploads, apply ML-based risk scoring and rule-based moderation logic in near real-time, and automatically handle policy violations while maintaining audit trails.

A video moderation system is the safety brain built into a global short‑video platform like TikTok. When creators upload videos, the system ingests the media, runs ML models to score risk (e.g., nudity, violence, hate symbols), applies evolving business rules, and triggers automated actions (remove, restrict, escalate) within seconds—all while keeping a complete, explainable audit trail. Interviewers ask this because it combines near real-time stream processing, ML inference at scale, policy/rule management, global reliability, and strong auditability. They want to see if you can decompose a multi-stage pipeline, choose appropriate data flows and stores, handle bursts and backpressure, ensure idempotent side effects, and design an operator-friendly policy surface. Expect to discuss SLAs, event-driven architectures, model/version governance, and operational safety.

## Common Functional Requirements

1. Users should be able to upload a video and have it evaluated for policy compliance in near real time with consistent outcomes worldwide.
    
2. Safety operators should be able to create, test, and roll out rule-based policies that use ML scores and metadata without redeploying services.
    
3. When a violation is detected, the system should automatically take the appropriate action (e.g., remove, age‑gate, geo‑block) and notify relevant parties.
    
4. Authorized reviewers and compliance stakeholders should be able to view a complete audit trail for each decision, including model versions, scores, rules fired, and actions taken.

## Common Deep Dives

meet a near real-time SLA
This is where many designs fall down: you need low latency and high throughput simultaneously. Break the pipeline into stages, define a latency budget per stage, and plan for bursts without dropping critical safety signals. - Establish a latency budget (e.g., P95 3–5s end-to-end) and split it across extraction, inference, rule evaluation, and enforcement; use backpressure-aware queues to decouple stages so you can autoscale independently. - Use a cascaded approach: run lightweight classifiers or frame sampling first, then escalate only risky items to heavier GPU models; prioritize content by creator trust, region, or prior violations to keep tail latency down. - Keep inference close to the edge (regional GPU pools), prefetch frames/keyframes, and cache common features; build graceful degradation paths (e.g., temporary hold or human review) when queues exceed thresholds.

rule engine - policy team can update rules safely without redeploys

Policy evolves faster than code. Interviewers look for externalized, versioned, and testable rules that are safe to change and easy to roll back, with clear observability and audit. - Externalize rules in a policy store with versioning and staged rollout (draft, shadow, canary, global); give ops a DSL or UI that composes ML scores, metadata, and context into decisions. - Make evaluation deterministic and side‑effect free; freeze inputs (scores, model versions, metadata) and persist the rule evaluation context to guarantee repeatability and explainability. - Provide simulation and shadow modes to test new rules against historical traffic; emit metrics on rule hits, action rates, false positive signals, and drift to catch regressions early.

event-driven pipeline - reliable, idempotent and complete auditability

At-least-once delivery is the norm in streaming systems. You must prevent duplicate takedowns and ensure every decision is explainable months later for appeals, legal holds, and regulator audits. - Use idempotency keys per video moderation cycle and a transactional outbox to publish decisions; design enforcement endpoints (remove, age‑gate) to be idempotent and record the moderation state machine. - Orchestrate with sagas/durable workflows for retries, timeouts, and compensations (e.g., revert an action on appeal); persist intermediate states to survive restarts. - Maintain an append-only audit log with immutable decision events, including timestamps, model hashes, rule versions, operators, and request IDs; partition for high write throughput and index for investigations.

global scale, data residency, multi-region
Global platforms face regional laws and network realities. Keep the hot path local, avoid cross-region writes on the critical path, and replicate only what’s necessary for safety and reporting. - Run ingestion, inference, and rules regionally; replicate compact decisions and audits asynchronously, and localize sensitive media to satisfy residency requirements. - Use per-region streaming (with topic mirroring for DR) to avoid cross-region fanout; design failover playbooks and acceptance criteria for temporary policy differences during partitions. - Manage model and policy versions via a global registry; roll out deterministically per region and pin evaluations to explicit versions to keep results consistent across sites.



