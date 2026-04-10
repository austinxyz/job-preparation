---
title: Agile in AI-Augmented Development - blog
source: https://austinxyz.github.io/blogs/blog/2026/03/09/agile-development-in-ai-coding
date_saved: 2026-04-10
processed: true
skill_note: "[[skills/management/project/Agile Methodology]]"
---

# Twenty Years of Agile, One Year of AI — Here's What Survived

Source: Austin Xu personal blog — based on 50K-line project experiment with AI coding tools.

Core thesis: Agile principles become **more critical**, not less, in AI-augmented development. Speed of code generation amplifies the need for coherent architecture and verified correctness.

## Key reframing: the development bottleneck has shifted

Previously: writing code was the constraint → Agile managed human execution speed.
Now: "knowing what to build and verifying correctness" is the constraint → Agile manages judgment and coherence.

## Agile practices that become load-bearing in AI workflows

**TDD** → becomes the "closing loop" mechanism. AI can run failing tests and self-correct iteratively. Without tests, reviewing AI code requires slow human reading. With tests, evaluation becomes tractable: "does this pass?"

**Small iterations** → the unit shrinks dramatically. Rule of thumb: if a task takes > 5 minutes, break it down. Rationale: long AI sessions accumulate drift as context windows forget earlier architectural decisions. Calibrating granularity is a core AI developer skill.

**Pair programming** → works authentically in exploratory workflows (rough requirement → AI design → prototype → human feedback → iterate). Failure mode: over-formalizing the interaction replaces collaboration with document management.

**Refactoring** → AI enables more aggressive refactoring (understands contextual meaning, not just mechanical transformations). Dual risk: over-focusing on feature delivery accumulates complexity faster than ever, producing code illegible to both humans and AI.

**Working software as measure** → tensions with AI-native documentation emphasis. Discipline: documentation should be minimal, structural, and kept in sync by automated means. CLAUDE.md for architecture decisions + tests documenting behavior. Working software remains truth; documentation is scaffolding.

**Retrospection** → lessons captured in files (CLAUDE.md, project principles) compound across sessions rather than repeating mistakes.

## The "File as Truth" vs. "Code as Truth" tension

Traditional Agile: code is truth (executable is unambiguous).
AI-native: specs and structured state as source of truth.
Problem: natural-language docs are inherently ambiguous — same spec can produce very different code.
Resolution: both matter; **tests bridge them** by verifying intent-to-implementation alignment.

## What doesn't change

Agile was designed to manage complexity and uncertainty. AI doesn't eliminate these — it amplifies them. The core judgment problems (what to build, how to verify correctness, when to refactor) are precisely what Agile methodology develops.
