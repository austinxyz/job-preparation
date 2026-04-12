---
title: AI Agents Architecture
category: tech/ai-basics
tags: [agents, agentic-ai, tool-use, planning, react, tool-calling, multi-agent, orchestration, memory, context-window]
status: draft
priority: high
last_updated: 2026-04-12
created_from_jd: [[positions/Tech Lead Manager - Agents - Perplexity]]
---

# AI Agents Architecture

## Knowledge Map
- 前置知识：LLM Fundamentals, Context Engineering and Tool Interfaces, vector databases (for memory retrieval)
- 延伸话题：Multi-agent orchestration, Memory and retrieval (MIPS/ANN algorithms, HNSW/FAISS), AI Evaluation, MCP (Model Context Protocol), ReAct / Reflexion patterns, prompt engineering
- 管理关联：Technical Roadmap, Engineering Team Management, agent reliability/safety, cost-latency tradeoffs

## Core Concepts

### System Architecture
- **Three core components**: Planning (task decomposition + self-reflection), Memory (short-term in-context + long-term external vector store), Tool Use (external API calls, code execution, search) — LLM acts as the "brain" orchestrating all three
- **Workflows vs Agents distinction** (Anthropic): Workflows = LLMs orchestrated through predefined code paths (predictable, consistent); Agents = LLMs dynamically directing their own process and tool usage (flexible, but higher cost and error risk) — most production use cases start with workflows
- **Augmented LLM as base building block**: LLM + retrieval + tools + memory; all agentic patterns build on top of this

### Planning Patterns
- **CoT (Chain of Thought)**: "think step by step" — decomposes hard tasks into sequential smaller steps; improves accuracy at the cost of latency
- **Tree of Thoughts (ToT)**: extends CoT by exploring multiple reasoning branches at each step via BFS/DFS; evaluates intermediate states; better for problems with many viable solution paths
- **ReAct**: alternates between Thought → Action → Observation loops; integrates reasoning traces with tool calls; more robust than action-only baselines because the thought step grounds actions
- **Reflexion**: adds dynamic self-reflection after failed trajectories; agent stores reflections in working memory (up to ~3); improves on ReAct for tasks where trial-and-error matters

### Memory Architecture
- **Short-term (in-context)**: what's in the active context window; finite; fast; maps to human working memory (~7 items, 20-30s in humans → context window length in LLMs)
- **Long-term (external vector store)**: embeddings stored in vector DB; retrieved via ANN search at query time; effectively unlimited capacity; maps to human long-term declarative memory
- **ANN algorithms for retrieval**: LSH (hash-based, approximate), ANNOY (random projection trees), **HNSW** (hierarchical small-world graphs — most popular, great recall/speed tradeoff), **FAISS** (Facebook's vector quantization — fast on GPU), ScaNN (anisotropic quantization, Google's approach)
- **Generative Agents memory model**: memory stream (all experiences) → retrieval scoring (recency + importance + relevance) → reflection (higher-level summaries) → planning & reacting; demonstrates emergent social behavior in simulation

### Workflow Patterns (Anthropic taxonomy)
- **Prompt chaining**: sequential steps where each LLM output feeds next; add programmatic gates to verify intermediate results; good when task cleanly decomposes into fixed subtasks; trades latency for accuracy
- **Routing**: classify input → dispatch to specialized sub-prompt or sub-model; enables model-size optimization (easy questions → Haiku, hard → Sonnet/Opus); good for multi-category tasks
- **Parallelization**: two variants — Sectioning (independent subtasks run in parallel) and Voting (same task run multiple times for diversity/confidence); speeds up throughput, improves reliability for high-stakes decisions
- **Orchestrator-workers**: central LLM dynamically breaks down and assigns subtasks to worker LLMs; unlike parallelization, subtasks aren't pre-defined; good for unpredictable multi-step coding or search tasks
- **Evaluator-optimizer**: generator LLM + evaluator LLM in a feedback loop; use when responses are measurably improvable and evaluation criteria are clear; analogous to a human writer + editor cycle

### Tool Use
- **MRKL systems**: LLM as router directing queries to expert modules (neural or symbolic — calculator, weather API, search); highlights that *knowing when to use a tool is as important as knowing how*
- **Function calling / tool schemas**: tools defined by name + description + parameter schema; LLM generates structured tool calls; model selection of right tool is critical — poor descriptions → wrong tool selection
- **Tool documentation as ACI (Agent-Computer Interface)**: Anthropic's core principle — invest heavily in tool descriptions, include when NOT to use a tool, provide examples; treat tool docs like a user-facing API
- **HuggingGPT pattern**: LLM as task planner → model selector → execution coordinator → response synthesizer; 4-stage pipeline for multi-modal multi-model orchestration

### Production Challenges
- **Finite context length**: limits history, tool call results, and long planning chains; vector retrieval partially compensates but lacks full-attention fidelity
- **Long-horizon planning failure**: LLMs struggle to re-plan when encountering unexpected errors mid-task; humans are more robust via trial-and-error adaptation
- **Natural language interface fragility**: output formatting errors and hallucinated tool calls are common; most agent frameworks spend significant code on output parsing and retries
- **Compounding errors**: in long agent loops, early mistakes propagate; mitigation = human checkpoints, stopping conditions (max iterations), sandboxed execution
- **Cost and latency**: agents require multiple LLM calls per task; each tool call adds latency; orchestrator-workers and evaluator-optimizer patterns multiply costs — must be justified by task complexity

### Design Principles (Anthropic)
1. **Simplicity first**: start with single LLM + retrieval; add agentic complexity only when simpler solutions demonstrably fall short
2. **Transparency**: explicitly show planning steps in agent output; aids debugging and user trust
3. **Tool documentation and testing**: treat ACI design as seriously as API design; test with adversarial inputs

## Key Questions

**Q: Walk me through the architecture of an LLM-powered agent. What are the core components?**
Answer framework: Planning (task decomposition via CoT/ToT, self-reflection via ReAct/Reflexion), Memory (short-term in-context, long-term external vector store with ANN retrieval), Tool Use (external APIs, code execution, search). LLM is the controller; emphasize that these three components interact — planning determines what tools to call, tool results feed back into context (short-term memory), and important observations can be stored long-term.

**Q: What's the difference between a workflow and an agent? When would you use each?**
Answer framework: Workflows = predefined code paths (more predictable, cheaper, easier to debug, preferred when task structure is known); Agents = LLM dynamically controls flow (flexible, higher cost and error risk, needed for open-ended tasks where steps can't be predicted). Most production systems should start with workflows and escalate to agents only when flexibility is demonstrably needed. Mention routing and prompt chaining as common workflow patterns.

**Q: How does ReAct work, and why does it outperform action-only approaches?**
Answer framework: ReAct interleaves Thought → Action → Observation loops. The Thought step forces explicit reasoning before taking action, which grounds the agent's decisions and makes it easier to detect and recover from errors. Action-only baselines skip this reasoning trace, leading to more hallucinated or unjustified tool calls. The tradeoff is more tokens per step; the benefit is measurably better performance on knowledge-intensive tasks.

**Q: How would you design the memory system for a long-running agent that needs to remember user preferences and past interactions?**
Answer framework: Two layers — short-term (active context window with recent turns + retrieved snippets), long-term (vector store with embeddings of past interactions). Retrieval scoring should combine recency (recent events weighted higher), importance (ask LLM to score significance), and relevance (cosine similarity to current query). For retrieval at scale, use HNSW or FAISS. Address context window management: summarize older turns rather than truncating, surface only top-k retrieved memories.

**Q: You're building an agent to automate software engineering tasks. What patterns would you use and what are the failure modes?**
Answer framework: Orchestrator-workers (central LLM plans which files to change, worker LLMs execute edits); evaluator-optimizer (reviewer LLM checks each change); tool set = code execution, file read/write, test runner, search. Key failure modes: compounding errors (early mistake propagates to later steps), hallucinated file paths, getting stuck in loops. Mitigations: sandboxed execution, stopping conditions, human checkpoints at major milestones, structured output formats for file edits.

**Q: How do you decide the right level of agentic complexity for a new product feature?**
Answer framework: Start by asking if a single optimized LLM call with retrieval and in-context examples suffices — it often does. Escalate to workflows (prompt chaining, routing) when the task has clear decomposable steps. Only escalate to agents when: the number of steps can't be predicted, flexibility is required at scale, and the latency/cost tradeoff is justified. Measure task success rate and cost-per-completion at each level before adding complexity.

**Q: Describe the challenges with long-horizon agent tasks and how you'd mitigate them.**
Answer framework: Three main challenges: (1) context length limits (history gets truncated) → mitigate with periodic summarization and external memory; (2) plan rigidity (LLMs struggle to re-plan on unexpected errors) → mitigate with Reflexion-style self-reflection loops and human checkpoints; (3) compounding errors → mitigate with sandboxed execution, per-step verification gates, and stopping conditions. Also: natural language output fragility → structured output schemas reduce parsing failures.

**Q: How would you evaluate whether an agent is performing reliably in production?**
Answer framework: Task completion rate (did the agent achieve the stated goal?), step-level accuracy (was each tool call correct?), error recovery rate (how often does the agent self-correct vs. fail?), cost-per-task (latency + token spend), and human oversight triggers (how often does the agent ask for help or hit stopping conditions?). Use sandboxed eval environments mirroring prod. Track failure mode distribution — context overflow, tool call errors, hallucinated reasoning — to prioritize improvements.

## Summary

LLM-powered agent systems combine three core capabilities — planning, memory, and tool use — with the LLM serving as the central controller. Planning enables complex task decomposition (CoT, Tree of Thoughts, ReAct, Reflexion); memory provides both short-term context (the active context window) and long-term recall via external vector stores with approximate nearest neighbor retrieval (HNSW, FAISS); and tool use extends the LLM beyond its training knowledge to interact with APIs, execute code, and access real-time data. The key architectural insight from Anthropic's production experience is that successful agent systems prioritize simplicity: most use cases are better served by composable workflows (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer) than by fully autonomous agents, which carry higher cost and compounding error risk.

For an AI Infra or engineering manager, the critical design decisions are: where to draw the workflow/agent boundary, how to instrument agents for observability (step-level logging, tool call tracing), how to set stopping conditions and human oversight checkpoints, and how to measure reliability in sandboxed eval environments before production. The ACI (Agent-Computer Interface) — the design of tool schemas and documentation — is as important as the prompt itself; poor tool descriptions are one of the most common sources of agent failure. Cost management also matters: each agentic workflow multiplies LLM API calls, so architectural choices (parallelization vs. sequential, model routing to cheaper models for simpler subtasks) have direct cost implications at scale.

Technically, the key topics to know deeply are ReAct (thought-action-observation loop), Reflexion (self-reflection to recover from failures), HNSW/FAISS for vector retrieval, and the five Anthropic workflow patterns. The field is evolving rapidly — MCP (Model Context Protocol) is emerging as a standard for tool integration, and multi-agent frameworks (orchestrator + specialized workers) are becoming the dominant architecture for complex coding and research tasks.

## Raw Material
- [[raw_material/tech/ai-basics/AI Agents Architecture - resources]]
