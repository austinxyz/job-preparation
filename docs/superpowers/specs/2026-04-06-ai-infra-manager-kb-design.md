# AI Infra Manager Knowledge Base — Design Spec

**Date:** 2026-04-06  
**Status:** Approved  
**Project:** ai-infra-manager

---

## Overview

An Obsidian-based knowledge base to prepare for AI Infra Manager roles. The system supports semi-automated content ingestion (raw materials → Claude-summarized skill notes), JD-driven gap analysis, and resume tailoring. It complements the existing [Growing](../../../growing) project, which handles active practice (leetcode, interview tracking, job applications).

**Relationship to Growing:**
- Growing = active practice tool (drills, application tracking, interview records)
- ai-infra-manager = deep knowledge base (notes, raw material, knowledge maps, JD analysis)
- Soft-linked via `growing_link` fields in experience and JD notes

---

## Directory Structure

```
ai-infra-manager/              ← Obsidian vault root
│
├── skills/
│   ├── tech/
│   │   ├── algorithms/        ← 算法与数据结构
│   │   ├── system-design/     ← 系统设计
│   │   ├── software-eng/      ← 软件开发（设计模式、编程语言、工程实践）
│   │   ├── infra/             ← 基础设施（网络、存储、云、容器、K8s）
│   │   ├── ai-basics/         ← ML基础、深度学习、LLM原理
│   │   └── ai-infra/          ← 训练集群、推理优化、MLOps、存储
│   └── management/
│       ├── behavior/          ← STAR题库、常见BQ题
│       ├── people/            ← 团队管理、招聘、绩效
│       └── project/           ← 项目管理、roadmap、跨团队协作
│
├── experience/                ← 个人经历，每条一个note，STAR结构
│
├── raw_material/              ← 原文存档，按类目分子目录
│   ├── tech/
│   │   ├── algorithms/
│   │   ├── system-design/
│   │   ├── software-eng/
│   │   ├── infra/
│   │   ├── ai-basics/
│   │   └── ai-infra/
│   └── management/
│       ├── behavior/
│       ├── people/
│       └── project/
│
├── positions/                 ← JD目录，每个JD一个note
│
├── _templates/                ← Obsidian模板
│   ├── skill-template.md
│   ├── experience-template.md
│   ├── jd-template.md
│   └── raw-material-template.md
│
└── _meta/
    └── index.md               ← 全局索引，知识地图入口
```

---

## Obsidian Integration

- **Graph View:** wikilinks between skill notes form the visual knowledge map
- **Dataview:** YAML frontmatter enables dynamic queries (e.g., all `status: stub` + `priority: high` skills)
- **Templates:** Obsidian Templater plugin for consistent note creation
- Depth: wikilinks for cross-references (Option B), YAML + Dataview where content warrants it (Option C)

---

## Skill Note Structure

Each skill is a single `.md` file. Filename = skill name (e.g., `Kubernetes Scheduling.md`).

```markdown
---
title: Kubernetes Scheduling
category: tech/infra
tags: [k8s, scheduling, container-orchestration]
status: stub          # stub | draft | in-progress | reviewed
priority: high        # high | medium | low
last_updated: 2026-04-06
created_from_jd:      # optional: [[positions/Company-Role]]
---

# Kubernetes Scheduling

## Knowledge Map
- 前置知识：[[Container Basics]], [[Linux Namespaces]]
- 延伸话题：[[Karpenter]], [[GPU Scheduling]]
- 管理关联：[[Capacity Planning]]

## Core Concepts
<!-- Bullet-form distilled concepts -->

## Key Questions
<!-- High-frequency interview questions + answer frameworks -->

## Summary
<!-- 1-3 paragraph synthesis -->

## Raw Material
<!-- Links to source files -->
- [[raw_material/tech/infra/k8s-scheduling-deepdive]]
```

**Status lifecycle:** `stub → draft → in-progress → reviewed`

- `stub`: Created by jd-analyzer when a required skill is missing from the knowledge base
- `draft`: Raw material saved, not yet summarized
- `in-progress`: Claude has summarized; user is actively reviewing
- `reviewed`: User has validated the note

---

## Experience Note Structure

```markdown
---
title: 推动 ML 训练平台迁移到 K8s
type: experience
skills: [k8s, infra, project-management, stakeholder-management]
company: <company>
date: 2024-06
impact: high           # high | medium | low
growing_link:          # optional: link to Growing project entry
---

# 推动 ML 训练平台迁移到 K8s

## Situation
<!-- Background, scale, challenges -->

## Task
<!-- Scope of responsibility, ownership -->

## Action
<!-- Technical decisions, cross-team collaboration -->

## Result
<!-- Quantified outcomes: cost, efficiency, scale metrics -->

## Related Skills
- [[skills/tech/infra/Kubernetes Scheduling]]
- [[skills/management/project/Cross-team Collaboration]]

## Interview Usage
- 适用 BQ：Tell me about a time you drove a large-scale migration
- 适用 JD 关键词：platform migration, k8s, infra leadership
```

---

## Raw Material Note Structure

```markdown
---
title: K8s Scheduling Deep Dive
source: https://...
date_saved: 2026-04-06
processed: false       # false → true after Claude summarizes
---

<!-- Original article content -->
```

---

## JD Note Structure

```markdown
---
title: AI Infra Manager - Google DeepMind
company: Google DeepMind
date_added: 2026-04-06
status: analyzing      # analyzing | ready | applied
growing_link:          # optional: link to Growing job application entry
---

# AI Infra Manager - Google DeepMind

## Raw JD
<!-- Paste original JD text -->

## Key Requirements
<!-- Claude-extracted: required skills, nice-to-haves, leadership requirements -->

## Skill Gap Analysis
| Skill | Status | Priority |
|-------|--------|----------|
| GPU Cluster Management | in-progress | high |
| LLM Inference Optimization | stub | high |
| People Management (10+ engineers) | reviewed | medium |

## Prep Checklist
<!-- Claude-generated, sorted by priority -->
- [ ] ...

## Experience Match
<!-- Claude-matched experience notes most relevant to this JD -->
- [[experience/ML训练平台迁移]]

## Resume Tailoring

### 关键词匹配
| JD 关键词 | 建议加入 resume 的表述 |
|----------|----------------------|
| LLM inference optimization | 改写 XX 项目描述突出推理优化 |
| Cross-functional leadership | 引用 [[experience/ML训练平台迁移]] |

### 建议强调的 Experience
<!-- Which experience notes to prioritize in resume -->

### 建议弱化的内容
<!-- Current resume content less relevant to this JD -->
```

---

## Workflow

```
0. Discovery (JD-driven)
   You      → Paste JD into positions/ → run jd-analyzer skill
   Claude   → Extracts required skills
            → Finds gaps vs existing skill notes
            → Creates stub notes for unknown skills
            → Fills Key Requirements, Skill Gap Analysis, Experience Match sections

1. Learning (stub-driven)
   You      → Review stub notes → find learning materials
            → Paste originals into raw_material/

2. Summarization
   Claude   → Reads raw_material note
            → Fills Core Concepts, Key Questions, Summary in skill note
            → Sets processed: true on raw_material note
            → Advances status: stub → draft → in-progress

3. Personal Experience
   You      → Write experience notes in STAR format
            → Link to relevant skill notes

4. Interview Prep
   Dataview → Query: status in [stub, draft, in-progress] + priority: high
   You      → Prioritized review list
            → Update skill notes to reviewed as you go

5. Resume Tailoring
   You      → Run jd-analyzer on target JD
   Claude   → Compares resume-base.md + experience notes to JD keywords
            → Fills Resume Tailoring section
```

---

## Claude Skills

### `jd-analyzer`
**Trigger:** User pastes a JD into a positions/ note and invokes the skill.

**Steps:**
1. Extract required skills, nice-to-haves, leadership signals from JD
2. Scan `skills/` frontmatter for matches (by tags and title)
3. Scan `experience/` frontmatter for skill overlaps
4. For each required skill not found: create stub note with `created_from_jd` set
5. Output: Key Requirements, Skill Gap Analysis table, Prep Checklist, Experience Match, Resume Tailoring sections

**Input:** JD note path  
**Output:** Filled sections in the JD note

### `raw-material-processor`
**Trigger:** User invokes on a raw_material note (or directory).

**Steps:**
1. Read raw material content
2. Identify or create the corresponding skill note
3. Distill Core Concepts and Key Questions
4. Write Summary section
5. Set `processed: true` on raw material note
6. Advance skill note status from `stub`/`draft` → `in-progress`

---

## Templates to Create

| Template | Purpose |
|----------|---------|
| `skill-template.md` | New skill note with full frontmatter + section headers |
| `experience-template.md` | STAR-structured experience note |
| `jd-template.md` | JD note with all analysis sections pre-populated |
| `raw-material-template.md` | Minimal frontmatter for source articles |

Also: `_meta/resume-base.md` — full-version resume content, used as source material by jd-analyzer for tailoring suggestions.

---

## Complementary System: Growing

| Concern | Tool |
|---------|------|
| Deep knowledge notes, raw material, knowledge maps | ai-infra-manager (Obsidian) |
| Leetcode practice, algorithm drills | Growing |
| STAR answer practice, BQ question bank | Growing |
| Job application tracking, interview stages | Growing |
| Resume versions, AI resume analysis | Growing |
| JD gap analysis, prep priority list | ai-infra-manager |
| Skill notes with wikilinks + Graph View | ai-infra-manager |

Cross-reference via `growing_link` field in experience and JD notes.
