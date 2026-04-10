---
title: AI Native Infrastructure — Appendix
source: https://jimmysong.io/book/ai-native-infra/glossary/
date_saved: 2026-04-09
processed: true
skill_note: "[[skills/tech/ai-infra/AI-Native Infrastructure]]"
book: "AI Native Infrastructure — Systems Designed for Uncertainty"
book_url: https://jimmysong.io/book/ai-native-infra/
chapters_included:
  - "Glossary"
  - "Executive Checklist"
---

# Appendix

## Glossary of Key Terms

| Term | Definition |
|------|-----------|
| **AI-Native Infrastructure** | Infrastructure premised on "models/agents as execution entities, compute as scarce assets, and uncertainty as the norm" |
| **Model-as-Actor** | Models function as execution entities capable of invoking tools and producing side effects |
| **Compute-as-Scarcity** | GPU, interconnects, and power represent constrained core resources (not elastic) |
| **Uncertainty-by-Default** | Behavior and resource consumption are highly unpredictable, particularly in agentic scenarios |
| **Intent Plane** | The API and policy expression layer for stating "what I want" |
| **Execution Plane** | The training/inference layer translating intent into actual operations |
| **Governance Plane** | The quota, budget, and cost control layer bounding resource consequences |
| **The Loop** | Closed cycle: intent → consumption → cost/risk outcomes (Admission → Translation → Metering → Enforcement) |
| **Compute Governance** | Managing resource consequences across token economics, accelerator time, interconnects, storage, org budgets |
| **FinOps** | Embedding cost governance into architecture decisions (not post-hoc reconciliation) |
| **Agent** | Execution entity completing tasks through tool selection and iterative reasoning |
| **MCP** | Model Context Protocol — standardized protocol for tool access as declarable capability boundaries |
| **Operating Model** | Institutional design addressing responsibility boundaries and collaboration mechanisms between teams |
| **AI Landing Zone** | Bounded zone combining compute governance loop + context tier architecture + org contracts |
| **KV Cache** | Key-Value cache for inference state reuse; elevated from optimization to critical infrastructure asset |
| **Tail Latency** | P99/P999 latency; dominates AI workload economics because average performance is misleading under uncertainty |

## External References
- ISO/IEC 22989: AI Concepts and Terminology
- NIST AI Glossary
- OECD AI Glossary

---

## Executive Checklist (10-Question Framework)

A diagnostic tool for assessing whether infrastructure is genuinely AI-native or merely AI-grafted-onto-traditional-systems.

### Strategy
1. **Unit cost defined?** — Can you define cost per workload type (tokens, tasks, batch jobs)?
2. **Budget controls in place?** — Are quota mechanisms enforced at runtime (not just monitored)?
3. **Policy trade-offs explicit?** — Are performance vs. cost vs. risk trade-offs named and decided, not implicit?

### Governance
4. **Uncertainty handling?** — Do you have mechanisms for agent path explosions causing resource spikes?
5. **Resource mapping?** — Can you connect agent intent to billable resource consequences?
6. **Utilization strategy?** — Are isolation, sharing, preemption, and prioritization implemented (not just planned)?

### Execution
7. **Observability end-to-end?** — Can you trace from application request through infrastructure to cost attribution?
8. **Hardware evolution path?** — Is your platform designed to adopt new hardware and topologies without full rearchitecture?

### Organization
9. **Team alignment?** — Is AI SRE/ModelOps + FinOps collaboration formalized with clear accountability?
10. **Architecture documented?** — Can you articulate the three-plane architecture with governance strategy in a 5-minute whiteboard?

### Scoring Interpretation
- **0–3**: AI-grafted (traditional infra with AI bolt-ons; high cost/risk runway risk)
- **4–6**: AI-transitioning (governance loops exist but incomplete)
- **7–9**: AI-native (governance-first; scalable and sustainable)
- **10/10**: AI-native + institutionalized (FinOps and org contracts are operational)

## Interview Relevance

- **"How would you assess whether an organization's AI infra is mature?"** — Walk through this checklist
- **"What questions do you ask when joining a new AI team?"** — Questions 1, 2, 5, 7, 9 are the fastest signal
- **"What does 'AI-native' actually mean in practice?"** — Contrast AI-grafted vs. AI-native using the checklist scores
