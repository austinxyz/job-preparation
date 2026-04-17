---
title: LLMOps and AI Pipeline Engineering
category: tech/ai-infra
tags: [llmops, llm-pipeline, prompt-versioning, ai-evaluation, regression-monitoring, langfuse, braintrust, cost-optimization, latency, failure-handling]
status: draft
priority: high
last_updated: 2026-04-16
created_from_jd: "[[positions/Manager, DevOps, SRE & AI Infrastructure - AppZen]]"
---

# LLMOps and AI Pipeline Engineering

## Knowledge Map
- 前置知识：LLM fundamentals, CI/CD concepts, observability, MLOps basics
- 延伸话题：prompt versioning strategies, automated LLM testing (evals), hallucination/failure mode tracking, cost/latency tradeoffs, LLM gateways, Langfuse/Braintrust/Phoenix for monitoring, RAG Triad metrics, LLM-as-Judge, three-pillar observability (computational/semantic/agentic)
- 管理关联：AI pipeline reliability, LLM quality ownership, eval-driven development, "shift-left" for AI quality, cost governance at token-level, SLO design for stochastic components

## Core Concepts

- **LLMOps vs MLOps.** LLMOps extends MLOps with four deltas: *prompts are the primary artifact* (versioned alongside or instead of weights), *outputs are open-ended* (so human feedback + LLM-as-Judge replace pure objective metrics), *cost is measured in tokens not CPU-hours* (so routing and caching matter more than scheduling), and *pipelines are chains of stochastic components* (so semantic-layer observability is mandatory, not optional).

- **Six-layer reference architecture.** Production LLMOps stacks compose (1) Data Management (ingest/clean/embed → vector DB), (2) Model Development (foundation model + fine-tuning via LoRA/PEFT), (3) Inference & Deployment (quantization, token streaming, GPU autoscaling), (4) **LLM Gateway (the spine)**, (5) Security & Compliance (PII redaction, audit trails, SOC 2/HIPAA/GDPR), (6) Governance & Responsible AI (prompt/model versioning, hallucination tracking, bias detection).

- **LLM Gateway is the enforcement boundary.** Sits between applications and providers as a unified API. Core capabilities: routing (cost/perf/policy-based, including chaining), auth + rate limiting + PII redaction centrally, cost attribution per model/user/feature, automatic failover across providers, latency-based rerouting. Production-grade gateways add ~10ms p95 overhead and handle 350+ RPS on a single vCPU. Gateway-first design replaces N point integrations + N monitoring stacks with 1 control plane.

- **Three Pillars of Observability.** (1) **Computational** — cost/session, token throughput, latency breakdown by component. (2) **Semantic** — hallucination detection, relevance, toxicity. (3) **Agentic** — tool-selection accuracy, loop detection, planning coherence, time-to-completion vs. token cost. Traditional APM only covers pillar 1; a request can be 200 OK in <200ms and still be semantically wrong.

- **RAG Triad (retrieval-quality metrics).** Context Recall (are retrieved docs relevant?), Context Precision (signal-to-noise of chunks), Faithfulness (does answer derive only from context?), Answer Relevance (does output address the user's intent?). These decouple "retrieval broke" from "generation broke" — essential for debugging RAG systems where a healthy response may still be factually wrong.

- **Prompt versioning + CI/CD eval gates.** Every prompt is version-controlled with a content hash; modifications trigger CI jobs that run the new prompt against a *golden dataset* (curated input-output examples). If eval scores drop below baseline, the merge is blocked — same discipline as regression tests in code. This is the "shift-left for AI quality" pattern.

- **Evaluation approaches: offline + online.** Offline: golden datasets, synthetic generation via stronger models, expert annotation, CI/CD regression gates. Online: explicit feedback (thumbs up/down), implicit signals (query rephrasing, session abandonment), LLM-as-Judge sampling on 1–5% of production traces. Production failures feed back into the golden dataset — the dataset grows as the system matures.

- **LLM-as-Judge techniques and pitfalls.** Pairwise comparison (has position bias — must test bidirectionally), single-point grading with explicit rubrics, reference-guided grading (for hallucination detection), chain-of-thought prompting for transparency. LLM-as-Judge is cost-effective at scale but calibrates poorly without rubrics and ground-truth spot checks.

- **Cost control mechanisms.** (1) Model routing — cheap model for simple tasks, premium for complex reasoning. (2) Caching — semantic cache hits on near-duplicate prompts. (3) Batching + quantization + token streaming at inference. (4) Per-user/per-feature token budgets enforced at gateway. (5) Fallback chains that prefer cheaper providers when quality is acceptable.

- **Common failure modes.** Prompt injection (requires designed-in defenses + red-teaming), hallucination (structured prompts + retrieval grounding reduce), silent drift (prompt-level drift detected via eval-score trends, not HTTP metrics), agent loops (repetitive reasoning; requires loop-detection in the orchestration layer), vendor outages (requires multi-provider routing at gateway).

## Key Questions

**Q: How does LLMOps differ from traditional MLOps?**
Answer framework: Name the four deltas — prompts as primary versioned artifact, open-ended outputs requiring human/LLM-as-Judge evaluation, token-level cost accounting, and stochastic component chains requiring semantic observability. Avoid the framing that LLMOps *replaces* MLOps — it extends it; the CI/CD discipline, feature stores, and governance patterns still apply.

**Q: How would you design a production LLM serving architecture for multiple providers?**
Answer framework: Gateway-first. Start with the LLM Gateway (unified API, auth, routing, telemetry, fallback), then layer in provider adapters, prompt management with version control, observability with the three pillars, and cost routing policy. Point out what goes wrong without a gateway: N integrations, scattered monitoring, vendor lock-in, no PII enforcement boundary.

**Q: How do you measure quality for open-ended LLM outputs?**
Answer framework: No single metric. For RAG: the RAG Triad (Context Recall/Precision, Faithfulness, Answer Relevance). For agents: tool-selection accuracy, loop detection, time-to-completion. Cross-cutting: LLM-as-Judge on a sampled 1–5% of traces, with explicit rubrics and pairwise bidirectional testing to control position bias. Anchor with golden datasets that grow over time as production failures feed back.

**Q: Walk me through how you'd run regression testing on prompt changes.**
Answer framework: Version-control every prompt with a hash. On every PR, run the new prompt against a curated golden dataset (multiple eval dimensions — relevance, faithfulness, toxicity, cost, latency). Block merges if any scored dimension regresses beyond a threshold. Promote production failure cases into the golden dataset. This is the same CI/CD discipline as code regression tests, applied to prompts.

**Q: Why is traditional APM insufficient for LLM applications?**
Answer framework: APM measures the *container*, not the *content*. A trace can show HTTP 200 in 200ms while the retrieved document was irrelevant and the generated answer was hallucinated. LLM observability adds semantic and agentic pillars — RAG Triad metrics, hallucination scores, tool-call correctness, planning coherence. Name the three-pillar model (Computational / Semantic / Agentic) as the cleanest framework.

**Q: How do you control cost and latency for a production LLM application at scale?**
Answer framework: Five levers — model routing at gateway (cheap for simple, premium for complex), semantic caching of near-duplicate prompts, token streaming + quantization at inference, per-user/per-feature token budgets enforced centrally, fallback chains preferring cheaper providers when quality is acceptable. Monitor token throughput and cost per session as first-class observability signals, not afterthoughts.

**Q: How do you handle hallucination in production?**
Answer framework: Detection via reference-based metrics (BERTScore, faithfulness for RAG), reference-free self-consistency across temperature samples, and LLM-as-Judge with reference-guided grading. Mitigation: retrieval grounding (RAG), structured prompts with explicit format requirements, guardrail models, and human-in-the-loop for high-risk paths. Note the trap: log-prob analysis is unreliable because modern models are often *confidently* incorrect.

**Q: How do you apply SRE/SLO discipline to LLM services?**
Answer framework: Availability and latency SLOs transfer directly to the LLM gateway and inference endpoints — same SLI/SLO/error-budget math. The new dimension is *quality SLOs*: define semantic-quality thresholds (faithfulness ≥ X, hallucination rate ≤ Y) measured via continuous LLM-as-Judge sampling. Quality SLO violations burn error budget the same way availability violations do. This is the bridge from traditional SRE practice (which I already apply to the K8s API server) into the LLM domain.

## Summary

LLMOps is the operational practice for running LLM applications in production — and it's best understood as MLOps plus four deltas: prompts become the primary versioned artifact, outputs are open-ended (so evaluation requires human feedback and LLM-as-Judge rather than BLEU/ROUGE alone), cost is accounted in tokens rather than CPU-hours, and pipelines are chains of stochastic components requiring semantic-layer observability. A production LLMOps stack typically organizes into six layers — data/embedding/retrieval, model development, inference and serving, an LLM Gateway as the control-plane spine, security/compliance, and governance — with the gateway being the load-bearing component that enforces auth, routing, rate limits, PII redaction, cost attribution, and provider failover. Gateway-first design replaces N point-integrations and N monitoring stacks with one centrally-governed control plane.

Observability in LLMOps follows a three-pillar model: Computational (cost, latency, token throughput), Semantic (hallucination detection, relevance, toxicity), and Agentic (tool-selection accuracy, loop detection, planning coherence). Traditional APM covers only the computational pillar — and in LLM systems a request can be HTTP 200 in under 200ms while the retrieved document was irrelevant and the answer hallucinated. For RAG systems the canonical retrieval-quality metrics are the RAG Triad (Context Recall, Context Precision, Faithfulness, Answer Relevance), which decouples "retrieval broke" from "generation broke". Evaluation runs on two tracks: offline with golden datasets, synthetic generation, and expert annotation gating CI/CD merges when prompts regress; online with explicit feedback, implicit signals (query rephrasing, session abandonment), and LLM-as-Judge sampling on 1–5% of production traces. Production failures feed back into the golden dataset, which grows with system maturity.

For AI Infra management this topic sits at the intersection of several existing disciplines: the CI/CD discipline that enforces prompt regression gates is the same one I applied to Kubernetes control-plane deployments; the SLO/SLI/error-budget math transfers directly to LLM gateway availability and latency (the new dimension is *quality SLOs* based on semantic thresholds); and cost governance at token level parallels capacity governance at compute level. Adjacent skills: [[AI Evaluation and Testing]] (deeper eval methodology), [[LLM Inference Optimization]] (serving-layer performance), [[Vector Databases]] (retrieval layer), [[AI-Native Infrastructure]] (broader infra patterns), [[SRE Practices and SLO Engineering]] (underlying reliability discipline).

## Key Terms

**Core lifecycle & architecture layers**
- `LLMOps` · `MLOps delta` · `data management layer` · `model development layer` · `inference & deployment layer` · `LLM gateway` · `security & compliance layer` · `governance & responsible AI layer`

**Deployment patterns**
- `API-centric` · `RAG` · `LLM + workflow orchestration` · `fine-tuned private LLM` · `hybrid cloud-edge`

**LLM Gateway**
- `unified API` · `cost/perf/policy routing` · `model chaining` · `PII redaction` · `rate limiting` · `automatic failover` · `latency-based rerouting` · `per-model cost attribution` · `10ms p95 overhead` · `350+ RPS / vCPU`

**Observability — Three Pillars**
- **Computational**: `token throughput` · `cost/session` · `latency breakdown` · `time-to-first-token (TTFT)`
- **Semantic**: `hallucination detection` · `relevance scoring` · `toxicity` · `BERTScore` · `faithfulness`
- **Agentic**: `tool-selection accuracy` · `loop detection` · `planning coherence` · `time-to-completion vs token cost`

**Tracing**
- `trace` · `span` · `SDK-based` · `proxy-based` · `OpenTelemetry`

**RAG Triad**
- `Context Recall` · `Context Precision` · `Faithfulness` · `Answer Relevance`

**Evaluation & quality**
- `golden dataset` · `synthetic generation` · `expert annotation` · `regression gate` · `prompt drift detection` · `LLM-as-Judge` · `pairwise comparison` · `position bias` · `single-point grading` · `reference-guided grading` · `chain-of-thought grading` · `RLHF`

**Prompt management**
- `prompt versioning` · `content hash` · `prompt template` · `playground` · `Opik` · `MCP server for prompts`

**Tools & platforms**
- `Langfuse` · `Braintrust` · `LangSmith` · `LangWatch` · `Phoenix` · `Arize` · `Comet Opik` · `MLflow` · `LangChain` · `LangGraph` · `LlamaIndex` · `vLLM` · `TrueFoundry` · `Pinecone` · `Weaviate`

**Cost control levers**
- `model routing` · `semantic cache` · `batching` · `quantization` · `token streaming` · `per-user token budget` · `fallback chain`

**Failure modes & defenses**
- `prompt injection` · `hallucination` · `silent drift` · `agent loop` · `vendor outage` · `red-teaming` · `guardrail model` · `jailbreak detection`

**Fine-tuning & adaptation**
- `foundation model` · `full fine-tuning` · `PEFT` · `LoRA` · `instruction tuning`

## Raw Material
- [[raw_material/tech/ai-infra/LLMOps and AI Pipeline Engineering - resources]]
