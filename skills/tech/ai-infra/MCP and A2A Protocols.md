---
title: MCP and A2A Protocols
category: tech/ai-infra
tags: [mcp, a2a, agent-protocol, tool-calling, json-rpc, oauth, tool-poisoning, multi-agent, context-protocol, agent-security]
status: draft
priority: high
last_updated: 2026-05-17
created_from_jd: ""
---

# MCP and A2A Protocols

## Knowledge Map
- 前置知识：[[AI Agents Architecture]], [[Agentic AI Frameworks]], LLM tool use / function calling, JSON-RPC 2.0, OAuth 2.1
- 延伸话题：[[Security Identity and Credential Management]] (OAuth/PKCE, Zero Trust), [[LLMOps and AI Pipeline Engineering]] (observability), RAG / Vector Databases, Agent sandboxing (Signadot, NVIDIA OpenShell)
- 管理关联：MCP governance (audit, rate limiting, compliance), tool security review process, agent identity and authorization policy

## Core Concepts

### MCP Overview

- **Model Context Protocol (MCP)**: open standard (Anthropic) for connecting LLMs / agents to external tools and data sources via a standardized client-server protocol — the "USB-C port for AI agents"
- **Problem it solves**: eliminates N×M custom integrations between agents and tools; any MCP client can connect to any MCP server without custom glue code
- **Transport over JSON-RPC 2.0**: MCP adds on top of JSON-RPC — unified tool description (`tool.json`), session & permission management, streaming/events, multi-transport support
- **Three roles**: **Host** (the LLM application / IDE), **Client** (MCP client within the Host), **Server** (MCP server exposing tools/resources/prompts)

### MCP Three Core Primitives

| Primitive | What it is | Analogy |
|-----------|-----------|---------|
| **Resources** | Data exposed to LLM as context (files, DB records, API responses, logs) | Provides background |
| **Tools** | Executable capabilities (search, query DB, call API) | Provides actions |
| **Prompts** | Server-defined reusable message templates, parameterized | Structures how to ask |

- **Resources**: identified by URI (`[protocol]://[host]/[path]`); static (fixed URI) or dynamic (URI template, RFC 6570); discovered via `resources/list`; read via `resources/read`; subscribable for real-time updates
- **Tools**: registered via `tools/list` (name + description + parameter schema); called via `tools/call`; model decides which tool to invoke based on description — **description quality is critical**
- **Prompts**: server-registered templates (`prompts/list` / `prompts/get`); support parameterization, resource embedding, multi-turn interaction; surfaced as Slash commands or menu items in UIs
- **Interplay**: Prompt structures the question → Resources provide background context → Tools execute actions

### MCP Session Lifecycle

Three phases for every MCP connection:
1. **Initialize**: Client sends `initialize` request (protocol version + capabilities); Server responds with `InitializeResult`; Client sends `InitializedNotification` to confirm handshake
2. **Communication**: bidirectional Request–Response (sync) and Notification (async event); model app calls Client interfaces; Server routes tool calls to user business functions
3. **Termination**: either side calls `close()` or transport channel drops

**Message types**: `Request` (expects response), `Result` (success response), `Error` (failure response), `Notification` (one-way, no response expected)

### Protocol Layer Architecture

- **BaseSession** (`mcp/shared/session.py`): common logic for JSON-RPC read/write, frame parsing, request-response correlation, notification dispatch — shared by client and server
- **ClientSession**: handles `initialize()` handshake; routes incoming server requests (`sampling/createMessage`, `roots/list`, `ping`) to registered callbacks; delegates unhandled messages to `message_handler`
- **ServerSession**: enforces initialization state machine (rejects requests before `InitializedNotification`); exposes high-level interfaces (`send_log_message`, `send_tool_list_changed`, `create_message`, `list_roots`); queues unhandled requests for framework-level routing via `@server.call_tool()` decorators

### Transport Layers

| Transport | Mechanism | Best For |
|-----------|-----------|---------|
| **Stdio** | stdin/stdout pipes | Local same-machine process communication |
| **HTTP + SSE** | SSE (server push) + HTTP POST (client send) | Browser frontend + microservice backend |
| **Streamable HTTP** | POST returns JSON or switches to SSE stream; `mcp-session-id` for session mgmt, resume support | Mixed HTTP/streaming with session persistence |
| **WebSocket** | Full-duplex after handshake | Low-latency, high-frequency real-time bidirectional |

### MCP Error Propagation

Three error paths:
1. **Error Response**: per-RPC failure — server returns JSON-RPC `error` field with `code`, `message`, `data`
2. **Transport Error Event**: connectivity failure (pipe closed, socket drop) — framework emits error event to session error handler; distinct from business-logic errors
3. **Protocol-Level Error Handler**: catches unattributable errors (malformed JSON, version mismatch, serialization failure); `BaseSession.on_error` hook allows logging, session teardown, reconnect

### MCP Sampling — Human-in-the-Loop

Flow: Server sends `sampling/createMessage` → Client presents to user for review/modification → Client calls LLM → Client presents LLM output for user review → Approved content returned to Server

- Ensures users retain control over LLM interactions triggered by server
- Critical for high-stakes agentic workflows (financial actions, code execution)

### FastMCP (Python SDK)

- High-level abstraction wrapping MCP Python SDK; allows creating tool/resource/prompt servers with decorators and managers
- `@mcp.tool()`, `@mcp.resource()`, `@mcp.prompt()` decorators for registration
- `RagClient`: `stdio_client` + `ClientSession`; dynamically fetches tool list; passes to LLM; executes tool calls on LLM request

### Enterprise MCP Governance (production patterns)

From real production deployments (Tess MCP at enterprise scale):

| Mechanism | Purpose |
|-----------|---------|
| Role-based authorization | Control which users/agents can call which MCP tools |
| Pipeline output filter | Strip PII and sensitive internal data from agent outputs |
| Audit log | Full traceability of every MCP tool call (who, what, when, result) |
| MCP Gateway | Single entry point; decouples staging/production environments |
| Rate limiting | Prevent agent runaway / tool abuse; protect backend resources |
| Knowledge layer decoupling | Keep knowledge base (e.g., Obsidian) independent from agent logic — evolve separately |

### Cloudflare Code Mode Pattern

**Core insight**: LLMs are better at *writing code* to call MCP than at calling MCP tools directly.

- LLM generates TypeScript code using typed interfaces + doc comments (more natural than JSON schemas)
- Multiple MCP tools can be chained in a single code block — eliminates round-trip token overhead
- **Sandbox**: V8 Isolates (Cloudflare Workers); millisecond startup; disposable; network-restricted to declared MCP bindings; API keys stay in supervisor, not in generated code
- **Token efficiency**: eliminates multi-turn MCP tool call overhead for multi-step workflows

### MCP vs Skills — Token Efficiency

- **MCP**: schema descriptions (tool list + parameter definitions) consumed on every call → significant token overhead with many tools
- **Skills (lazy load)**: content loaded into context only when invoked → minimal baseline token cost
- **Decision rule**: use MCP for dynamic tool discovery, runtime state, external system connections; use Skills for static, structured knowledge and workflow guidance

---

### A2A Protocol Overview

- **Agent-to-Agent (A2A)**: open standard (Google, announced 2025) for communication between AI agents — standardizes how agents discover each other's capabilities and delegate tasks
- **Complements MCP**: MCP = "Agent's hands" (tools and resources); A2A = "Agent's mouth" (inter-agent communication)
- **Distributed multi-agent**: MCP + A2A together push single-agent apps toward distributed, modular intelligent ecosystems

### A2A Five Core Design Principles

1. **Embrace agent capability**: agents exchange free-form messages, not just structured tool calls; agents remain black boxes to each other (no internal plan exposure)
2. **Build on existing standards**: HTTP, SSE, JSON-RPC — seamless with existing IT infrastructure
3. **Enterprise-grade security**: built-in auth/authz at OpenAPI parity; compliance-ready
4. **Long-running task support**: manages tasks spanning hours or days; human-in-the-loop; real-time status feedback
5. **Multimodal**: native support for text, audio, video, rich forms, embedded iframes

### A2A Object Model

| Object | Description |
|--------|-------------|
| **Agent Card** | JSON describing agent capabilities, skills, service URL, auth mechanism — published by each agent for discovery |
| **Task** | Core collaboration unit; has lifecycle, state, history, and result (Artifact); supports instant and long-running modes |
| **Artifact** | Task result produced by Remote Agent; can have multiple typed parts (text, image, etc.) |
| **Message** | Communication between Client and Remote Agent; contains instructions, status, context; multi-part with content-type negotiation |

### A2A Interaction Flow

1. **Capability discovery**: Client fetches Remote Agent's Agent Card (via registration center or `get_agent_card` API)
2. **Task management**: Client creates a Task; Remote Agent updates state (input_required / completed / error)
3. **Message collaboration**: bidirectional messages carrying context, user instructions, artifacts; parts are typed for UI negotiation (images, forms, video)
4. **State sync**: SSE or Webhook keeps Client updated on long-running task progress in real-time

### A2A Authorization

**OAuth 2.1** for HTTP transport — same mechanism as MCP. Three identity components to manage:

| Component | Question |
|-----------|---------|
| **End User Identity** | Who is behind the action? (employee, manager, admin) |
| **Client Agent Identity** | Which agent is making the request? Is it trusted? |
| **Delegated Permissions** | What subset of user permissions has the user granted this agent? |

**Permission delegation rules**: permissions can only decrease through delegation chains — Agent A → Agent B → Agent C must enforce that C's permissions ⊆ B's ⊆ A's. Delegation amplification is a critical security invariant.

**CIBA (Client Initiated Backchannel Authentication)**: for non-browser agent flows — agent contacts user via push notification, email, or SMS instead of browser redirect.

---

## Key Questions

**Q: What is MCP and why does it matter for an AI infrastructure platform strategy?**
Answer framework: MCP standardizes the interface between LLMs/agents and external tools — think USB-C for AI. Instead of N×M custom integrations (each agent integrating each tool differently), you get N+M: any MCP client connects to any MCP server. Strategic value: (1) reduces framework lock-in — tool servers are reusable across agents; (2) growing ecosystem means less custom integration work; (3) enables governance at the protocol layer (auth, rate limiting, audit) rather than inside each agent. Recommend investing in MCP-compatible tool servers rather than framework-specific plugins.

**Q: What are the three MCP primitives and how do they compose?**
Answer framework: Resources (background data — files, DB records, logs, identified by URI), Tools (executable actions — search, API calls, DB queries), Prompts (server-defined reusable message templates). They compose into a capability chain: Prompt structures HOW to ask the question → Resources provide the background context the LLM needs → Tools execute the actions the LLM decides to take. The interplay is what makes MCP more than just a tool registry.

**Q: Walk me through the MCP session lifecycle and key message types.**
Answer framework: Three phases — Initialize (client sends capabilities, server responds with InitializeResult, client confirms with InitializedNotification), Communication (bidirectional Requests with Results/Errors, and one-way Notifications), Termination (either side closes). Four message types: Request (expects response), Result (success), Error (failure with code/message/data), Notification (one-way, no response). The BaseSession class handles all correlation and dispatch; ClientSession and ServerSession add role-specific logic.

**Q: What is the difference between MCP and A2A? When would you use each?**
Answer framework: MCP connects agents to tools and data sources (the "hands" — what an agent can DO). A2A enables agent-to-agent communication and task delegation (the "mouth" — how agents COORDINATE). MCP is the right choice when an agent needs to call an external API, read a file, or query a database. A2A is the right choice when you have multiple specialized agents and one needs to delegate a subtask to another. In practice, a production multi-agent system uses both: each agent uses MCP to access its own tools, and A2A for inter-agent delegation.

**Q: How would you design a secure MCP deployment for an enterprise with compliance requirements?**
Answer framework: Layer governance at the MCP Gateway: (1) role-based authorization controlling which agents/users can call which tools, (2) pipeline output filter stripping PII and sensitive data before returning to clients, (3) full audit log of every tool call with requester identity + arguments + result, (4) rate limiting to prevent agent runaway. Add OAuth 2.1 with PKCE for authentication. For code-execution tools, use sandbox isolation (V8 Isolates or containers) with network restrictions. Decouple knowledge bases from agent logic to allow independent evolution. These controls should be at the protocol/gateway layer, not inside individual agents — agents shouldn't carry security logic.

**Q: What are MCP tool poisoning attacks and how do you defend against them?**
Answer framework: Tool poisoning is prompt injection at the tool layer — attackers corrupt tool definitions, inputs, or outputs to manipulate agent behavior. Three attack vectors: (1) fake tool descriptions that promise benign behavior but execute malicious code; (2) polluted tool inputs embedding dangerous commands (e.g., "also delete /etc/passwd"); (3) tampered tool outputs containing hidden instructions that get injected into subsequent LLM context ("chain poisoning"). Advanced variants: Full-Schema Poisoning (hiding malicious instructions in parameter names/descriptions/enum values), ATPA (malicious instructions in tool return values), Rug Pull Attack (tool starts benign, description replaced after trust is established). Defense requires multi-layer: (1) tool whitelist with security audits before registration; (2) sandbox isolation (container per tool, restricted network/filesystem); (3) input validation before passing LLM-generated args to tools; (4) output sanitization to remove hidden payloads; (5) dynamic behavior monitoring for anomalous access patterns; (6) AI-based context analysis to distinguish user intent from injected instructions.

**Q: How does A2A handle the challenge of permission delegation in multi-agent chains?**
Answer framework: A2A requires managing three identity components — end user identity, agent identity, and delegated permissions (the subset the user granted the agent). The critical security invariant is permission attenuation: in an A→B→C delegation chain, C's permissions must be ⊆ B's ⊆ A's — permissions can only decrease, never amplify. For non-browser agent flows, A2A supports CIBA (Client Initiated Backchannel Authentication), where the agent contacts the user for approval via push notification or email instead of a browser redirect. For audit purposes, every delegation step should be logged with the full authorization chain, enabling post-facto compliance review.

**Q: What's the Cloudflare Code Mode insight, and when would you apply it?**
Answer framework: LLMs are better at writing code that calls MCP tools than at calling MCP tools directly. Reasons: (1) LLM training data has far more real code than synthetic tool-calling examples; (2) multiple MCP tool calls can be chained in one code block, eliminating round-trips and dramatically reducing token usage; (3) TypeScript interfaces + doc comments are a more natural API surface for LLMs than JSON schemas. Apply when: a workflow requires 3+ sequential tool calls, token budget is constrained, or tool schemas are complex. The security model requires a sandbox (V8 Isolates or containers) with network restrictions and API keys kept outside the generated code.

## Summary

Model Context Protocol (MCP) is Anthropic's open standard that solves the N×M integration problem between LLMs and external tools. Built on JSON-RPC 2.0, it provides three core primitives — Resources (data context), Tools (executable actions), and Prompts (reusable templates) — that compose into a structured capability chain for agent workflows. The protocol supports four transport layers (Stdio for local, HTTP+SSE and Streamable HTTP for web, WebSocket for real-time), with a three-phase lifecycle (Initialize → Communicate → Terminate) and three-path error propagation. In production, the critical design decisions are: placing governance (auth, audit, rate limiting, output filtering) at an MCP Gateway rather than inside individual agents; using sandbox isolation per tool (V8 Isolates or containers); and addressing tool poisoning through multi-layer defense (whitelist → sandbox → input validation → output sanitization → behavioral monitoring).

Agent-to-Agent (A2A) protocol is the companion standard for inter-agent communication, using an object model of Agent Cards (capability advertisement), Tasks (lifecycle-managed collaboration units), Artifacts (results), and Messages (multi-part typed communication). A2A's five design principles emphasize black-box agent autonomy, enterprise security, long-running task support, and standard HTTP/SSE foundations. The authorization model adds a critical challenge beyond single-agent OAuth: managing delegated permissions across agent chains requires strict permission attenuation (permissions can only decrease through delegation) and explicit identity tracking of user identity, agent identity, and delegated permission subsets. Trust network attacks — identity impersonation via crafted Agent Cards, collaborative chain hijacking, and trust propagation pollution — require architectural defenses including zero-trust verification at every delegation step.

Together, MCP and A2A represent the emerging protocol layer for the multi-agent ecosystem: MCP handles agent-to-tool integration, A2A handles agent-to-agent coordination, and governance lives at protocol gateways rather than in agent prompts.

## Key Terms

**MCP Primitives**
- `Resources` · `Tools` · `Prompts` · `URI template` · `mimeType` · `resources/list` · `resources/read` · `tools/list` · `tools/call` · `prompts/list` · `prompts/get`

**MCP Protocol Layer**
- `BaseSession` · `ClientSession` · `ServerSession` · `InitializeRequest` · `InitializeResult` · `InitializedNotification` · `Request` · `Result` · `Error` · `Notification` · `JSON-RPC 2.0`

**MCP Transport**
- `Stdio Transport` · `HTTP+SSE Transport` · `Streamable HTTP` · `WebSocket Transport` · `mcp-session-id` · `Server-Sent Events`

**MCP Security**
- `OAuth 2.1` · `PKCE` · `Tool Poisoning` · `Full-Schema Poisoning` · `ATPA` · `Rug Pull Attack` · `prompt injection` · `MCP Gateway` · `V8 Isolates` · `FastMCP`

**MCP Enterprise Patterns**
- `role-based authorization` · `pipeline output filter` · `audit log` · `rate limiting` · `Code Mode` · `sampling` · `human-in-the-loop`

**A2A Protocol**
- `Agent Card` · `Task` · `Artifact` · `Message` · `A2A Server` · `capability discovery` · `state sync` · `CIBA` · `permission attenuation` · `delegated permissions`

**A2A Security**
- `identity impersonation` · `collaborative chain hijacking` · `trust propagation pollution` · `permission amplification` · `zero-trust verification`

## Raw Material
- `jobs/Weekly/2026-W20 (May 12 - May 18)/MCP 学习笔记.md`
- `jobs/Weekly/2026-W20 (May 12 - May 18)/Wenli 对话整理 — MCP, Agent, Spec-driven.md`
