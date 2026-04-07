# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

An Obsidian-based interview prep knowledge base for an AI Infra Manager role. It is not a software project — there are no build steps, tests, or CI. All work is markdown note authoring and maintenance.

## Directory Structure

| Directory | Purpose |
|-----------|---------|
| `skills/` | Interview knowledge notes, organized by category (see below) |
| `raw_material/` | Source articles to be distilled — mirrored structure to `skills/`; also `raw_material/positions/` for raw JD text |
| `experience/` | STAR-format stories from past roles |
| `positions/` | Job description notes with analysis |
| `_meta/` | Index (`index.md`) and resume base (`resume-base.md`) |
| `_templates/` | Templater templates for creating new notes |
| `.claude/skills/` | Two custom Claude Code skills (see below) |

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
0. Find a JD → save raw text to raw_material/positions/ → run jd-importer skill → run jd-analyzer skill
1. For each stub skill → find learning materials → save to raw_material/
2. Run raw-material-processor on each raw_material/ note
3. Write STAR stories in experience/ as you recall relevant incidents
4. Use _meta/index.md Dataview tables to track progress and prioritize
5. Before a target interview → re-run jd-analyzer for resume tailoring
```

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
