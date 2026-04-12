---
title: Agentic AI Frameworks
category: tech/ai-infra
tags: [langchain, langgraph, crewai, autogen, rag, vector-db, agentic, multi-agent, tool-use, claude-sdk, dspy]
status: draft
priority: medium
last_updated: 2026-04-12
created_from_jd: "[[positions/Manager, DevOps, SRE & AI Infrastructure - AppZen]]"
---

# Agentic AI Frameworks

## Knowledge Map
- 前置知识：LLM fundamentals, [[AI Agents Architecture]] (workflow patterns, planning, memory, tool use), RAG patterns, function calling / tool schemas
- 延伸话题：LangGraph stateful graph execution, CrewAI / AutoGen multi-agent orchestration, vector DB integration (Pinecone, Weaviate, pgvector), agent memory and state management, MCP (Model Context Protocol), agent observability (LangSmith, Phoenix/Arize)
- 管理关联：framework selection for production, agent observability and debugging, cost control for multi-step agents, safe execution / sandboxing, build-vs-buy for agentic platforms

## Core Concepts

### The Framework Landscape: Why and When to Use One

- **Anthropic's core advice** (from "Building Effective Agents"): start with direct LLM API calls — many patterns can be implemented in a few lines of code; frameworks simplify standard low-level tasks (calling LLMs, parsing tools, chaining calls) but often add abstraction layers that obscure prompts/responses and make debugging harder; only adopt a framework when it demonstrably reduces complexity without hiding critical behavior
- **Framework value**: accelerate boilerplate (tool registration, retry logic, streaming, memory backends); provide pre-built integrations (vector DBs, external APIs); give teams shared vocabulary and patterns
- **Framework risk**: abstraction leakage (unexpected prompt injections from framework internals), harder to debug when things go wrong, framework version upgrades can silently change behavior, vendor lock-in to framework ecosystem
- **Practical rule of thumb**: prototype with a framework, migrate hot paths to direct API calls once you understand the pattern; frameworks are better for exploration than production critical paths

### Major Frameworks

#### LangChain
- **What it is**: the original comprehensive LLM orchestration library (Python/JS); provides chains, agents, tools, memory, document loaders, vector store integrations
- **Core abstractions**: Chain (sequential steps), Agent (LLM + tool loop), Retriever (pluggable vector search), Memory (conversation history management)
- **Strengths**: massive ecosystem (100s of integrations), large community, well-documented; good for RAG pipelines, simple tool-use agents, rapid prototyping
- **Weaknesses**: heavy abstraction — prompt templates are buried, debugging requires tracing through layers; stateful multi-step workflows are awkward with plain LangChain; frequent breaking changes between versions
- **Production fit**: acceptable for RAG pipelines and simple chains; less ideal for complex agent loops where you need fine-grained control

#### LangGraph
- **What it is**: extension of LangChain for stateful, graph-based multi-actor workflows; models agent execution as a directed graph (nodes = LLM calls or functions, edges = conditional routing)
- **Key insight**: state is explicitly managed as a typed dict flowing through graph nodes; enables branching, cycles (agent loops), checkpointing (resume from mid-execution), and human-in-the-loop interrupts
- **Maps to Anthropic patterns**: orchestrator-workers (central node dispatches to worker nodes), evaluator-optimizer (generator → evaluator → loop edge), routing (conditional edges based on LLM output)
- **Strengths**: explicit state machine makes complex agent behavior predictable and debuggable; built-in persistence/checkpointing; human interrupt support; integrates with LangSmith for tracing
- **Weaknesses**: steeper learning curve than plain LangChain; graph mental model is unfamiliar to some engineers; still inherits LangChain ecosystem complexity
- **Production fit**: best choice in the LangChain ecosystem for production agentic workflows; the explicit graph structure makes it auditable

#### CrewAI
- **What it is**: role-based multi-agent orchestration framework; you define Agents (with roles, goals, backstories), Tasks (assigned to agents), and Crews (groups of agents with a process: sequential or hierarchical)
- **Core abstraction**: each agent acts like a specialist (e.g., "Researcher", "Writer", "QA reviewer"); the crew manager orchestrates task delegation
- **Maps to Anthropic patterns**: orchestrator-workers (manager agent + worker agents), prompt chaining (sequential task execution), parallelization (parallel task execution in crews)
- **Strengths**: intuitive for product teams — role abstraction is easy to explain; good for document processing pipelines, content generation workflows, research + synthesis workflows
- **Weaknesses**: role/backstory prompting can be flaky with weaker models; less control over exact inter-agent communication; harder to implement tight feedback loops; limited production observability out of the box
- **Production fit**: good for well-defined collaborative workflows with clear roles; less suitable for highly dynamic or unpredictable agent behavior

#### AutoGen (Microsoft)
- **What it is**: multi-agent conversation framework; agents communicate via message passing in conversation threads; focus on code execution and tool use in agentic loops
- **Key pattern**: AssistantAgent (LLM-backed) + UserProxyAgent (human or code executor proxy) in a conversation; agents can spawn sub-conversations
- **Strengths**: strong code execution support (Python sandbox via Docker); good for coding agents, data analysis pipelines; Microsoft ecosystem integration (Azure OpenAI); active research backing
- **Weaknesses**: conversation-centric model can be verbose; complex to control when conversations go off-track; heavier dependency footprint; debugging multi-agent conversations is hard
- **Production fit**: strong for code-centric agentic applications; less natural for non-code workflows; commonly used in research/eval contexts

#### Claude Agent SDK (Anthropic)
- **What it is**: Anthropic's managed agent infrastructure (`/v1/agents`, `/v1/sessions`); provides persistent sessions, built-in tool execution, managed memory, and multi-agent orchestration
- **Key differentiator**: managed sessions with automatic context management — SDK handles context window limits, conversation persistence, and tool execution lifecycle
- **Strengths**: first-party integration with Claude models (prompt caching, extended thinking, computer use); managed infrastructure (no need to build your own session store or tool execution runtime); simplest path for Claude-native agents
- **Weaknesses**: Claude-only (vendor lock-in); newer/less battle-tested than LangGraph; less community ecosystem
- **Production fit**: best choice for teams going all-in on Claude; reduces infra burden significantly for agent state management

#### Strands Agents SDK (AWS)
- **What it is**: AWS's open-source agent SDK (mentioned in Anthropic's "Building Effective Agents"); model-agnostic but AWS-native; integrates with Bedrock for LLM access and AWS services for tools
- **Strengths**: AWS ecosystem fit (IAM, S3, Lambda as tools); Bedrock access to multiple models; good for teams already on AWS
- **Production fit**: reasonable for AWS-native agentic applications; less community adoption than LangChain/LangGraph

#### DSPy (Stanford)
- **What it is**: not a traditional framework — a "compiler" for LLM programs; you declare signatures (input/output types) and modules, then DSPy optimizes prompts and few-shot examples automatically via teleprompters (optimizers)
- **Key insight**: replaces manual prompt engineering with programmatic optimization; instead of hand-crafting prompts, define what you want and let DSPy find the best prompts through evaluation on a dataset
- **Strengths**: significant performance gains on structured tasks; reproducible; reduces prompt brittleness; great for pipelines where you can define a metric
- **Weaknesses**: requires an eval dataset; optimization runs can be slow and expensive; less intuitive for teams new to it; not designed for open-ended agentic behavior
- **Production fit**: excellent for structured pipelines (RAG, classification, extraction) where you can measure quality; less suited for general-purpose agents

### Framework Selection Guide

| Use Case | Recommended |
|----------|-------------|
| Simple RAG pipeline | LangChain or direct API |
| Complex stateful agent workflow (prod) | LangGraph |
| Role-based collaborative agent team | CrewAI |
| Code execution / coding agent | AutoGen or LangGraph |
| Claude-native managed agents | Claude Agent SDK |
| AWS-native agents | Strands + Bedrock |
| Structured pipeline with measurable quality | DSPy |
| Prototype → understand → then simplify | Any framework → migrate to direct API |

### Production Considerations

#### Observability
- **LangSmith** (LangChain): trace every LLM call, tool invocation, token count, latency; essential for debugging LangChain/LangGraph agents; add `LANGCHAIN_TRACING_V2=true` to get full traces
- **Phoenix / Arize**: model-agnostic OpenTelemetry-based tracing; works with any framework; better choice for multi-framework stacks or non-LangChain pipelines
- **Key metrics to trace**: per-step latency, token consumption per node, tool call success rate, loop count per task, human interrupt frequency
- **Structured logging**: log tool inputs/outputs, LLM prompt/response pairs at each step; critical for debugging compounding errors

#### Cost Control
- **Token budgeting**: set max_tokens per agent step; use cheaper models (Haiku) for routing and classification nodes, expensive models (Sonnet/Opus) only for synthesis
- **Loop limits**: always set max_iterations on agent loops; infinite loops are a real failure mode; log and alert when limits are hit
- **Caching**: prompt caching (Anthropic API) for repeated system prompts; semantic caching (GPTCache, Redis) for repeated similar queries
- **Parallelization cost**: parallel workflows multiply cost — measure whether quality improvement justifies it

#### Safety & Sandboxing
- **Tool execution**: never execute LLM-generated code outside a sandbox (Docker, Firecracker, E2B); treat LLM tool call arguments as untrusted input
- **Permission scoping**: tools should have least-privilege access (read-only where possible, no prod write access for autonomous agents)
- **Stopping conditions**: always implement max iterations + timeout; log and page when agents hit limits unexpectedly
- **Human-in-the-loop**: for high-stakes actions (database writes, external API calls, email sends), require explicit human approval; LangGraph supports interrupt-before-node natively

#### MCP (Model Context Protocol)
- **What it is**: Anthropic's open standard for connecting LLMs to external tools and data sources via a standardized client-server protocol
- **Why it matters**: replaces ad-hoc tool integrations with a unified interface; growing ecosystem of MCP servers (filesystem, GitHub, databases, web search); any MCP client (Claude, LangChain, etc.) can use any MCP server
- **Production relevance**: reduces framework lock-in for tool integrations; invest in MCP-compatible tool servers rather than framework-specific plugins

### Claude Code Skills as Lightweight Agents

Claude Code Skills represent a tightly integrated form of agent definition within the Claude Code runtime — a distinct implementation path worth understanding on its own terms.

**Mapping Skills to standard agent components**:

| Agent Component | LangGraph | Claude Code Skill |
|---|---|---|
| Instructions / system prompt | System prompt string (code) | Skill markdown file (natural language) |
| Tool set | `tools=[search, write_file, ...]` explicitly registered | Claude Code built-in tools (Read/Write/Edit/Bash/Grep…) shared across all skills |
| Reasoning engine | LLM API call | Claude itself |
| Execution environment | Python code + separate runtime | Claude Code conversation |

**Unique advantages of Skills as agents**:
- **Declarative**: describe intent in natural language; Claude infers execution steps — no control flow code required
- **Native human-in-the-loop**: the user sees every tool call and can reject or correct at any point; traditional frameworks require explicit interrupt mechanisms (e.g., LangGraph's `interrupt_before`)
- **Shared tool set**: all Skills share the same tools (Claude Code built-ins + MCP) with no per-agent registration
- **Conversation as state**: the active context window is the state — no explicit state machine needed; simple, but bounded by context window limits

**Limitations compared to a full agent framework**:
- Cannot spawn sub-agents in parallel (unless explicitly using the `Agent` tool for dispatch)
- No persistent checkpointing — execution state is lost when the conversation ends
- No programmatic retry / fallback logic
- Cannot be dynamically composed in code (no conditional Skill selection, parameterization, or branching from external code)

**Where Skills fit**: single-threaded, well-defined tasks that benefit from human review at each step (RAG pipelines, document processing, code review workflows) are the natural fit. When the task becomes "process 50 files in parallel and aggregate results" or requires persistent state across sessions, escalate to a proper agent framework or use the `Agent` tool for parallel dispatch.

**Relationship to MCP**: Skills access MCP tools natively through Claude Code — no additional configuration needed. MCP is the capability infrastructure; Skills are the behavioral specification on top of it.

### Anthropic's Core Principles (from "Building Effective Agents")
1. **Simplicity first**: start with the simplest solution (single LLM + retrieval); add agent complexity only when simpler solutions demonstrably fall short
2. **Transparency**: explicitly show planning steps; don't hide reasoning inside framework magic
3. **ACI (Agent-Computer Interface)**: treat tool documentation as seriously as API design — LLMs use tool descriptions to decide when and how to call tools; poor descriptions → wrong tool selection → cascading failures

## Key Questions

**Q: How do you choose between LangChain, LangGraph, and direct API calls for a production agentic system?**
Answer framework: Direct API calls for simple chains (2-3 steps), LangChain for RAG pipelines with many integrations, LangGraph for stateful multi-step agent workflows where you need checkpointing/branching/human-in-the-loop. Key question: does the framework abstraction help or obscure? If you find yourself fighting the framework to get the right prompt, simplify. Mention Anthropic's advice: prototype with frameworks, migrate hot paths to direct API once patterns are understood.

**Q: A team wants to build a multi-agent system where agents collaborate on a complex research task. Which framework and architecture would you recommend?**
Answer framework: Start with the Anthropic orchestrator-workers pattern — one orchestrator LLM breaks down the task, dispatches to specialized worker agents (search agent, synthesis agent, fact-checker). Implement with LangGraph (if stateful workflow with cycles needed) or CrewAI (if role-based collaboration is the mental model). Key design decisions: how do agents communicate (shared state vs message passing), how to prevent hallucination compounding (evaluator-optimizer loop), what the stopping condition is. Emphasize: measure quality at each step before adding more agents.

**Q: Your agentic pipeline is spending 5x more on LLM tokens than expected. How do you diagnose and fix it?**
Answer framework: First, instrument with LangSmith or Phoenix to trace per-step token consumption. Common culprits: (1) large system prompts repeated every step → use prompt caching; (2) no loop limit → agent stuck in retry loop; (3) using expensive model for trivial steps → route classification/simple tasks to Haiku; (4) tool outputs dumped into context without summarization → add tool output compression. Implement per-task cost budgets and alert on overruns. Prioritize fixes by token-per-step contribution.

**Q: How do you ensure a production agent doesn't take dangerous actions (delete prod data, send emails to customers)?**
Answer framework: Defense in depth — (1) tool-level: tools for dangerous actions require explicit human approval before execution (LangGraph interrupt-before-node); (2) permission scoping: agent service account has read-only access; write tools only in dev/staging by default; (3) input validation: treat all LLM-generated tool arguments as untrusted — validate before execution; (4) sandboxing: code execution tools run in isolated Docker/Firecracker containers; (5) stopping conditions: max iterations + timeout, alert on breach; (6) audit log: every tool call logged with full arguments for post-incident review.

**Q: What is MCP and why does it matter for your agentic platform strategy?**
Answer framework: MCP (Model Context Protocol) is Anthropic's open standard for connecting LLMs to external tools via a client-server protocol. It standardizes tool integration so any MCP client (Claude, LangChain, custom) can use any MCP server (GitHub, filesystem, databases) without custom code. Strategic importance: reduces framework lock-in (tool servers are framework-agnostic), enables reuse across teams (one MCP server, many agents), growing ecosystem means less custom integration work. Recommend investing in MCP-compatible tool servers rather than framework-specific plugins.

**Q: When would you choose DSPy over LangChain for building an LLM pipeline?**
Answer framework: DSPy when you have a well-defined task with a measurable quality metric and a dataset to optimize against — e.g., RAG accuracy, classification F1, extraction recall. DSPy's optimizer will find better prompts and few-shot examples than hand-crafted ones, and the result is reproducible. LangChain when you need broad integrations, rapid prototyping, or the task is too open-ended to define a metric. Key limitation: DSPy requires eval data and optimization compute upfront; not suitable for open-ended agent behavior.

**Q: How do you evaluate whether an agentic framework is ready for production vs just for prototyping?**
Answer framework: Four axes — (1) Observability: does it emit traces/spans you can inspect per step? (LangSmith for LangGraph, OpenTelemetry for others); (2) Reliability: does it handle LLM errors, tool timeouts, and context overflow gracefully? (3) Control: can you set loop limits, add human interrupts, and enforce stopping conditions? (4) Debuggability: when something goes wrong, can you replay the execution and identify which step failed? If the framework scores low on any of these, either add instrumentation or migrate that workflow to direct API calls with your own control plane.

## Summary

Agentic AI frameworks abstract the boilerplate of building LLM-powered systems — tool registration, prompt chaining, memory management, multi-agent coordination — but introduce abstraction layers that can obscure behavior and complicate debugging. The most important principle, from Anthropic's production experience, is to start with the simplest solution (direct API calls or simple workflows) and only adopt framework complexity when it demonstrably helps. Most production failures with frameworks come from hidden prompt modifications, uncapped agent loops, or obscured error handling that the framework swallows silently.

The framework landscape has stratified by use case: LangGraph dominates for stateful multi-step agent workflows on the LangChain ecosystem (its explicit graph model makes agent behavior auditable); CrewAI provides an intuitive role-based abstraction for collaborative multi-agent teams; AutoGen excels for code-execution-centric agents (coding agents, data analysis); the Claude Agent SDK reduces infrastructure burden for Claude-native managed agents; and DSPy is a programmatic optimizer for structured pipelines where quality is measurable. For teams building on AWS, Strands Agents integrates naturally with Bedrock and AWS services. MCP (Model Context Protocol) is emerging as the standard for tool integration across all frameworks, reducing ecosystem fragmentation.

From a management perspective, the key decisions are: (1) which framework fits your team's mental model and production maturity requirements, (2) how to instrument it for observability (LangSmith or Phoenix), (3) how to enforce cost controls (model routing, loop limits, caching), and (4) how to sandbox dangerous tool execution. The build-vs-buy question applies here too: for teams with deep ML infra expertise, a thin direct-API control plane is often more maintainable long-term than a heavy framework dependency; for teams moving fast, frameworks provide real velocity — just plan the migration path before you're too entangled.

## Raw Material
- [[raw_material/tech/ai-basics/AI Agents Architecture - resources]]
