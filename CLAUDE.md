# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

An Obsidian-based interview prep knowledge base for an AI Infra Manager role. It is not a software project — there are no build steps, tests, or CI. All work is markdown note authoring and maintenance.

## Directory Structure

| Directory | Purpose |
|-----------|---------|
| `skills/` | Interview knowledge notes, organized by category (see below) |
| `raw_material/` | Source articles to be distilled — mirrored structure to `skills/` |
| `experience/` | STAR-format stories from past roles |
| `positions/` | Legacy JD notes (being superseded by `jobs/`) |
| `jobs/` | **Per-position workspaces** (gitignored) — one subfolder per company. Contains raw JD at root, then `<Company>/` with `jd-analysis.md`, `resume.md`, `contacts/`, `prep/`, `mocks/`, `correspondence/`. **See "Per-Position Workspace Rules" below for critical isolation principles.** |
| `daily/` | Daily prep notes (gitignored) — private scratch, reflections, mock transcripts not tied to a specific position |
| `_meta/` | Index (`index.md`) and resume base (`resume-base.md`) |
| `_templates/` | Templater templates for creating new notes |
| `.claude/skills/` | Custom Claude Code skills (see below) |

### Skills Category Map

```
skills/tech/ai-infra/       — GPU, CUDA, training infra, MLOps
skills/tech/ai-basics/      — LLM theory, deep learning, ML fundamentals
skills/tech/infra/          — K8s, cloud, networking, storage
skills/tech/system-design/  — Distributed systems, system design
skills/tech/algorithms/     — Algorithms, data structures
skills/tech/software-eng/   — Design patterns, software practices
skills/management/behavior/ — Behavioral / leadership stories
skills/management/people/   — Hiring, team, performance
skills/management/project/  — Roadmap, planning, stakeholders
```

## Note Status Lifecycle

`stub` → `draft` → `in-progress` → `reviewed`

- **stub**: skeleton only, no real content
- **draft**: raw-material-processor has run once
- **in-progress**: being actively built out
- **reviewed**: ready for interview use

## Custom Skills

### `raw-material-processor`
Distills a `raw_material/` note into the linked skill note. Updates Core Concepts, Key Questions, Summary, advances status, and marks raw material as processed.

Usage: `/raw-material-processor` then provide the path to the raw material note.

### `jd-analyzer`
Analyzes a `positions/` note containing a pasted JD. Extracts requirements, builds a skill gap table, creates stub notes for missing skills, generates a prep checklist, and suggests resume tailoring.

Usage: `/jd-analyzer` then provide the path to the positions note.

## Workflow

```
0. Find a JD → drop raw text in jobs/ root → run /jd-importer → run /jd-analyzer → run /resume-builder
1. For each stub skill → find learning materials → save to raw_material/
2. Run /raw-material-processor on each raw_material/ note
3. Write STAR stories in experience/ as you recall relevant incidents
4. Use _meta/index.md Dataview tables to track progress and prioritize
5. As interviews get scheduled → record contacts in jobs/<Company>/contacts/
6. Synthesize per-round prep docs in jobs/<Company>/prep/ from contacts + jd-analysis + resume
7. Per-position mocks go under jobs/<Company>/mocks/
```

## Per-Position Workspace (`jobs/`) Rules

**⚠️ CRITICAL ISOLATION PRINCIPLE:** Each `jobs/<company>/` is a **physically independent workspace**. Never cross-pollinate position-specific data between companies. This is the single most important rule for working in this repo.

### What is position-specific (must stay isolated per company)

- Interview loop structure (number, type, sequence of rounds)
- Interviewer names and roles (e.g., "Prashanth" at AppZen ≠ anyone at Pinterest)
- Schedule (dates, times, durations)
- Compensation conversations and target numbers
- HR / coordinator communications and message history
- Round-specific prep docs naming specific interviewers
- Company-stated signals (SLO targets, team size, tech stack specifics)

### What IS cross-position reusable (live outside `jobs/`)

- Skill notes (`skills/`) — general technical knowledge
- Experience stories (`experience/`) — STAR-format, company-neutral where possible
- Master resume base (`_meta/resume-base.md`)
- Reflections that span multiple positions (`daily/`)

### The "unknown" vs "TBD" distinction

| Label | Meaning | When to use |
|-------|---------|-------------|
| **unknown** | No information received at all | Any interview rounds, interviewers, or schedule the company has NOT communicated |
| **TBD** | Structure is confirmed; specifics pending | Only after the company has said "yes, there will be a VP round" — date may still be TBD |
| **scheduled** | Concrete date/time/interviewer exists | After a coordinator explicitly schedules it |

**Never use "TBD" as a speculative placeholder for unknown interview rounds.** TBD implies known structure. Using it for "I'm guessing there will be a Tech Round 2" creates a false impression that the structure is agreed.

### Anti-patterns (learned from actual mistakes)

1. **Don't copy interview loop tables between companies.** Company A's loop (HR → VP → Tech 1 with person X → Tech 2 with person Y → Final) does NOT imply Company B has the same loop. Every company's loop is different.

2. **Don't reference other companies' interviewer names in a company's prep docs.** If Pinterest has never told you who you're interviewing with, do not write "Tech Round 1 (Prashanth)" — Prashanth works at AppZen, not Pinterest.

3. **Don't speculate round types in prep doc `scope` frontmatter.** Write `scope: applicable to future technical rounds (loop TBD per recruiter)` instead of `scope: Tech Round 1 / Tech Round 2 / Hiring Manager`.

4. **Don't fill in placeholder rows in interview loop tables.** An empty table with a single confirmed row + a note "Subsequent rounds: not yet communicated" is more honest than 4 speculative rows with `TBD / TBD / TBD`.

5. **Don't infer comp bands from another company.** If AppZen's recruiter said "our band is $280–350K", that is not applicable data for Pinterest.

### When interview info arrives during an actual conversation

When an HR call or coordinator email reveals the real loop, **only then** update `jobs/<company>/README.md` with the real data. That is the moment when **unknown → TBD → scheduled**. Until that moment, keep the corresponding tables/fields empty or explicitly marked as unknown.

### Rule of thumb for new prep docs

Before writing anything position-specific, ask:
- "Is this information the company has explicitly communicated?" — if yes, write it
- "Am I inferring this from a pattern seen at another company?" — if yes, DO NOT write it into this company's files
- "Is this a generic principle from the company's public content (JD, engineering blog)?" — if yes, safe to write; cite the source

## Note Language Convention

- **English is primary** for all skill notes (interviews are conducted in English)
- Chinese may appear as inline annotations or parenthetical explanations to aid reading comprehension — not as the main content
- `_templates/` files use Templater syntax (`<% tp.* %>`) — do not remove or alter those placeholders

## Frontmatter Fields

**Skill notes** (`_templates/skill-template.md`):
```yaml
title, category, tags, status, priority, last_updated, created_from_jd
```

**Raw material notes** (`_templates/raw-material-template.md`):
```yaml
title, source, date_saved, processed, skill_note
```

**Experience notes** (`_templates/experience-template.md`):
```yaml
title, type, skills, company, date, impact, growing_link
```

**Position notes** (`_templates/jd-template.md`):
```yaml
title, company, date_added, status, growing_link
```
