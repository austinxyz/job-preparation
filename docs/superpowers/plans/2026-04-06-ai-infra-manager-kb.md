# AI Infra Manager Knowledge Base Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bootstrap the AI Infra Manager Obsidian vault with full directory structure, templates, seed skill notes, and two Claude skills (jd-analyzer, raw-material-processor).

**Architecture:** Pure file-based Obsidian vault. No backend, no build step. All intelligence lives in Claude skill instruction files (`.claude/skills/*/SKILL.md`). Templates use Obsidian Templater plugin syntax. Dataview queries are embedded in `_meta/index.md`.

**Tech Stack:** Markdown, YAML frontmatter, Obsidian (Dataview plugin, Templater plugin, Graph View), Claude Code skills.

---

## File Map

| File | Responsibility |
|------|---------------|
| `skills/tech/algorithms/` | Skill notes for algorithms & data structures |
| `skills/tech/system-design/` | Skill notes for system design |
| `skills/tech/software-eng/` | Skill notes for software engineering |
| `skills/tech/infra/` | Skill notes for infrastructure (K8s, cloud, networking) |
| `skills/tech/ai-basics/` | Skill notes for ML/DL/LLM fundamentals |
| `skills/tech/ai-infra/` | Skill notes for AI infrastructure (training, inference, MLOps) |
| `skills/management/behavior/` | BQ skill notes |
| `skills/management/people/` | People management skill notes |
| `skills/management/project/` | Project management skill notes |
| `experience/` | Personal STAR-structured experience notes |
| `raw_material/tech/*/` | Raw article copies, mirroring skills/tech structure |
| `raw_material/management/*/` | Raw article copies, mirroring skills/management structure |
| `positions/` | JD notes with gap analysis |
| `_templates/skill-template.md` | Obsidian Templater template for skill notes |
| `_templates/experience-template.md` | Obsidian Templater template for experience notes |
| `_templates/jd-template.md` | Obsidian Templater template for JD notes |
| `_templates/raw-material-template.md` | Obsidian Templater template for raw material notes |
| `_meta/index.md` | Global knowledge map, Dataview dashboard |
| `_meta/resume-base.md` | Full-version resume content for jd-analyzer |
| `.claude/skills/jd-analyzer/SKILL.md` | jd-analyzer Claude skill instructions |
| `.claude/skills/raw-material-processor/SKILL.md` | raw-material-processor Claude skill instructions |

---

## Task 1: Vault Directory Structure

**Files:**
- Create: all directories listed in the file map above

- [ ] **Step 1: Create all vault directories**

```bash
mkdir -p skills/tech/algorithms
mkdir -p skills/tech/system-design
mkdir -p skills/tech/software-eng
mkdir -p skills/tech/infra
mkdir -p skills/tech/ai-basics
mkdir -p skills/tech/ai-infra
mkdir -p skills/management/behavior
mkdir -p skills/management/people
mkdir -p skills/management/project
mkdir -p experience
mkdir -p raw_material/tech/algorithms
mkdir -p raw_material/tech/system-design
mkdir -p raw_material/tech/software-eng
mkdir -p raw_material/tech/infra
mkdir -p raw_material/tech/ai-basics
mkdir -p raw_material/tech/ai-infra
mkdir -p raw_material/management/behavior
mkdir -p raw_material/management/people
mkdir -p raw_material/management/project
mkdir -p positions
mkdir -p _templates
mkdir -p _meta
mkdir -p .claude/skills/jd-analyzer
mkdir -p .claude/skills/raw-material-processor
```

Run from: `C:\Users\lorra\projects\ai-infra-manager`

- [ ] **Step 2: Verify structure**

```bash
find . -type d | grep -v '.git' | sort
```

Expected output includes all directories above.

- [ ] **Step 3: Commit**

```bash
git add .
git commit -m "chore: scaffold vault directory structure"
```

---

## Task 2: Obsidian Templates

**Files:**
- Create: `_templates/skill-template.md`
- Create: `_templates/experience-template.md`
- Create: `_templates/jd-template.md`
- Create: `_templates/raw-material-template.md`

- [ ] **Step 1: Create skill-template.md**

Create `_templates/skill-template.md` with this exact content:

```markdown
---
title: <% tp.file.title %>
category: tech/
tags: []
status: stub
priority: medium
last_updated: <% tp.date.now("YYYY-MM-DD") %>
created_from_jd:
---

# <% tp.file.title %>

## Knowledge Map
- 前置知识：
- 延伸话题：
- 管理关联：

## Core Concepts
<!-- Bullet-form distilled concepts. Filled by raw-material-processor skill. -->

## Key Questions
<!-- High-frequency interview questions + answer frameworks. Filled by raw-material-processor skill. -->

## Summary
<!-- 1-3 paragraph synthesis. Filled by raw-material-processor skill. -->

## Raw Material
<!-- Links to raw_material/ source files -->
```

- [ ] **Step 2: Create experience-template.md**

Create `_templates/experience-template.md`:

```markdown
---
title: <% tp.file.title %>
type: experience
skills: []
company: 
date: <% tp.date.now("YYYY-MM") %>
impact: medium
growing_link:
---

# <% tp.file.title %>

## Situation
<!-- Background, scale, challenges faced -->

## Task
<!-- Your scope of responsibility, ownership -->

## Action
<!-- Technical decisions made, cross-team collaboration, what you specifically did -->

## Result
<!-- Quantified outcomes: cost savings, efficiency gains, scale metrics -->

## Related Skills
<!-- [[skills/tech/infra/Example Skill]] -->

## Interview Usage
- 适用 BQ：
- 适用 JD 关键词：
```

- [ ] **Step 3: Create jd-template.md**

Create `_templates/jd-template.md`:

```markdown
---
title: <% tp.file.title %>
company: 
date_added: <% tp.date.now("YYYY-MM-DD") %>
status: analyzing
growing_link:
---

# <% tp.file.title %>

## Raw JD
<!-- Paste the original JD text here -->

## Key Requirements
<!-- Claude-extracted after running jd-analyzer skill -->

## Skill Gap Analysis
| Skill | Status | Priority |
|-------|--------|----------|

## Prep Checklist
<!-- Claude-generated, sorted by priority. Run jd-analyzer skill to populate. -->

## Experience Match
<!-- Claude-matched experience notes most relevant to this JD -->

## Resume Tailoring

### 关键词匹配
| JD 关键词 | 建议加入 resume 的表述 |
|----------|----------------------|

### 建议强调的 Experience
<!-- Which experience notes to prioritize in resume -->

### 建议弱化的内容
<!-- Current resume content less relevant to this JD -->
```

- [ ] **Step 4: Create raw-material-template.md**

Create `_templates/raw-material-template.md`:

```markdown
---
title: <% tp.file.title %>
source: 
date_saved: <% tp.date.now("YYYY-MM-DD") %>
processed: false
skill_note:
---

# <% tp.file.title %>

<!-- Paste original article content below. Do not edit — keep raw. -->
<!-- Run raw-material-processor skill to distill this into the linked skill note. -->
```

- [ ] **Step 5: Commit**

```bash
git add _templates/
git commit -m "feat: add obsidian templates for skill, experience, jd, raw-material"
```

---

## Task 3: Global Index and Resume Base

**Files:**
- Create: `_meta/index.md`
- Create: `_meta/resume-base.md`

- [ ] **Step 1: Create _meta/index.md**

Create `_meta/index.md`:

```markdown
---
title: AI Infra Manager Knowledge Base
---

# AI Infra Manager Knowledge Base

## Quick Stats

```dataview
TABLE WITHOUT ID
  length(rows) AS "Total Skills",
  length(filter(rows, (r) => r.status = "stub")) AS "Stub",
  length(filter(rows, (r) => r.status = "draft")) AS "Draft",
  length(filter(rows, (r) => r.status = "in-progress")) AS "In Progress",
  length(filter(rows, (r) => r.status = "reviewed")) AS "Reviewed"
FROM "skills"
WHERE file.name != "_index"
FLATTEN file AS rows
```

## High Priority — Action Required

```dataview
TABLE title, category, status, priority
FROM "skills"
WHERE status != "reviewed" AND priority = "high"
SORT status ASC
```

## All Skills by Category

### Tech — AI Infra
```dataview
TABLE title, status, priority
FROM "skills/tech/ai-infra"
SORT priority DESC, status ASC
```

### Tech — AI Basics
```dataview
TABLE title, status, priority
FROM "skills/tech/ai-basics"
SORT priority DESC, status ASC
```

### Tech — Infra
```dataview
TABLE title, status, priority
FROM "skills/tech/infra"
SORT priority DESC, status ASC
```

### Tech — System Design
```dataview
TABLE title, status, priority
FROM "skills/tech/system-design"
SORT priority DESC, status ASC
```

### Tech — Algorithms
```dataview
TABLE title, status, priority
FROM "skills/tech/algorithms"
SORT priority DESC, status ASC
```

### Tech — Software Engineering
```dataview
TABLE title, status, priority
FROM "skills/tech/software-eng"
SORT priority DESC, status ASC
```

### Management — Behavior
```dataview
TABLE title, status, priority
FROM "skills/management/behavior"
SORT priority DESC, status ASC
```

### Management — People
```dataview
TABLE title, status, priority
FROM "skills/management/people"
SORT priority DESC, status ASC
```

### Management — Project
```dataview
TABLE title, status, priority
FROM "skills/management/project"
SORT priority DESC, status ASC
```

## Unprocessed Raw Materials

```dataview
TABLE title, date_saved
FROM "raw_material"
WHERE processed = false
SORT date_saved DESC
```

## Open Positions

```dataview
TABLE title, company, status, date_added
FROM "positions"
SORT date_added DESC
```

## Experience Library

```dataview
TABLE title, company, date, impact
FROM "experience"
SORT date DESC
```

## Workflow Reference

| Step | Action |
|------|--------|
| 0. Discover | Paste JD → run `jd-analyzer` skill |
| 1. Learn | Review stub notes → find articles → save to `raw_material/` |
| 2. Summarize | Run `raw-material-processor` skill on raw material note |
| 3. Experience | Write STAR notes in `experience/` |
| 4. Prep | Use Dataview tables above to prioritize review |
| 5. Tailor | Run `jd-analyzer` on target JD for resume suggestions |
```

- [ ] **Step 2: Create _meta/resume-base.md**

Create `_meta/resume-base.md`:

```markdown
---
title: Resume Base
last_updated: 
---

# Resume Base

> This is the full, unabridged version of your resume content.
> The jd-analyzer skill uses this file to generate tailored resume suggestions for specific JDs.
> Keep this file up to date as your experience evolves.

## Summary / Professional Profile
<!-- 2-3 sentence professional summary -->

## Work Experience

### [Most Recent Role Title] — [Company] ([Start Date] – Present)
<!-- Full bullet points for this role. Include all achievements with metrics. -->

### [Previous Role Title] — [Company] ([Start Date] – [End Date])
<!-- Full bullet points -->

## Key Projects
<!-- Projects not fully captured in work experience above -->

## Skills
<!-- Technical: languages, frameworks, platforms, tools -->
<!-- Management: team size, methodologies, scope -->

## Education
<!-- Degrees, certifications -->
```

- [ ] **Step 3: Commit**

```bash
git add _meta/
git commit -m "feat: add global index with dataview dashboard and resume base"
```

---

## Task 4: Seed Skill Notes

**Files:**
- Create: one starter skill note per category (9 total)

These seed notes give the Obsidian Graph View initial nodes and demonstrate the template in action. They are all `status: stub` — content will be filled later via `raw-material-processor`.

- [ ] **Step 1: Create seed note for ai-infra — GPU Cluster Management**

Create `skills/tech/ai-infra/GPU Cluster Management.md`:

```markdown
---
title: GPU Cluster Management
category: tech/ai-infra
tags: [gpu, cluster, nvidia, cuda, distributed-training]
status: stub
priority: high
last_updated: 2026-04-06
created_from_jd:
---

# GPU Cluster Management

## Knowledge Map
- 前置知识：[[Linux Basics]], [[Networking Fundamentals]]
- 延伸话题：[[NCCL Collective Communication]], [[RDMA and InfiniBand]], [[Kubernetes GPU Scheduling]]
- 管理关联：[[Capacity Planning]]

## Core Concepts
<!-- To be filled by raw-material-processor skill -->

## Key Questions
<!-- To be filled by raw-material-processor skill -->

## Summary
<!-- To be filled by raw-material-processor skill -->

## Raw Material
<!-- Add links here after saving articles to raw_material/tech/ai-infra/ -->
```

- [ ] **Step 2: Create seed note for ai-basics — LLM Fundamentals**

Create `skills/tech/ai-basics/LLM Fundamentals.md`:

```markdown
---
title: LLM Fundamentals
category: tech/ai-basics
tags: [llm, transformer, attention, pretraining, finetuning]
status: stub
priority: high
last_updated: 2026-04-06
created_from_jd:
---

# LLM Fundamentals

## Knowledge Map
- 前置知识：[[Deep Learning Basics]], [[Attention Mechanism]]
- 延伸话题：[[LLM Inference Optimization]], [[RLHF]], [[Quantization]]
- 管理关联：[[AI Research Team Structure]]

## Core Concepts
<!-- To be filled by raw-material-processor skill -->

## Key Questions
<!-- To be filled by raw-material-processor skill -->

## Summary
<!-- To be filled by raw-material-processor skill -->

## Raw Material
```

- [ ] **Step 3: Create seed note for infra — Kubernetes**

Create `skills/tech/infra/Kubernetes.md`:

```markdown
---
title: Kubernetes
category: tech/infra
tags: [k8s, container-orchestration, scheduling, pods, deployments]
status: stub
priority: high
last_updated: 2026-04-06
created_from_jd:
---

# Kubernetes

## Knowledge Map
- 前置知识：[[Container Basics]], [[Linux Namespaces]], [[Networking Fundamentals]]
- 延伸话题：[[Kubernetes GPU Scheduling]], [[Karpenter]], [[Service Mesh]]
- 管理关联：[[Platform Team Management]]

## Core Concepts
<!-- To be filled by raw-material-processor skill -->

## Key Questions
<!-- To be filled by raw-material-processor skill -->

## Summary
<!-- To be filled by raw-material-processor skill -->

## Raw Material
```

- [ ] **Step 4: Create seed note for system-design — Distributed Systems**

Create `skills/tech/system-design/Distributed Systems.md`:

```markdown
---
title: Distributed Systems
category: tech/system-design
tags: [distributed, consistency, availability, cap-theorem, consensus]
status: stub
priority: high
last_updated: 2026-04-06
created_from_jd:
---

# Distributed Systems

## Knowledge Map
- 前置知识：[[Networking Fundamentals]], [[Storage Systems]]
- 延伸话题：[[Consensus Algorithms]], [[Distributed Storage]], [[Message Queues]]
- 管理关联：[[Engineering Reliability Culture]]

## Core Concepts
<!-- To be filled by raw-material-processor skill -->

## Key Questions
<!-- To be filled by raw-material-processor skill -->

## Summary
<!-- To be filled by raw-material-processor skill -->

## Raw Material
```

- [ ] **Step 5: Create seed note for algorithms — Big O and Complexity**

Create `skills/tech/algorithms/Big O and Complexity.md`:

```markdown
---
title: Big O and Complexity
category: tech/algorithms
tags: [algorithms, complexity, big-o, time-complexity, space-complexity]
status: stub
priority: medium
last_updated: 2026-04-06
created_from_jd:
---

# Big O and Complexity

## Knowledge Map
- 前置知识：
- 延伸话题：[[Sorting Algorithms]], [[Graph Algorithms]], [[Dynamic Programming]]
- 管理关联：

## Core Concepts
<!-- To be filled by raw-material-processor skill -->

## Key Questions
<!-- To be filled by raw-material-processor skill -->

## Summary
<!-- To be filled by raw-material-processor skill -->

## Raw Material
```

- [ ] **Step 6: Create seed note for software-eng — Design Patterns**

Create `skills/tech/software-eng/Design Patterns.md`:

```markdown
---
title: Design Patterns
category: tech/software-eng
tags: [design-patterns, oop, solid, architecture]
status: stub
priority: medium
last_updated: 2026-04-06
created_from_jd:
---

# Design Patterns

## Knowledge Map
- 前置知识：[[OOP Principles]]
- 延伸话题：[[System Design Patterns]], [[API Design]]
- 管理关联：

## Core Concepts
<!-- To be filled by raw-material-processor skill -->

## Key Questions
<!-- To be filled by raw-material-processor skill -->

## Summary
<!-- To be filled by raw-material-processor skill -->

## Raw Material
```

- [ ] **Step 7: Create seed note for management/behavior — STAR Method**

Create `skills/management/behavior/STAR Method.md`:

```markdown
---
title: STAR Method
category: management/behavior
tags: [behavioral, star, interview, storytelling]
status: in-progress
priority: high
last_updated: 2026-04-06
created_from_jd:
---

# STAR Method

## Knowledge Map
- 前置知识：
- 延伸话题：[[Conflict Resolution]], [[Influencing Without Authority]], [[Leadership Principles]]
- 管理关联：[[People Management]]

## Core Concepts
- **Situation:** Set the scene — context, scale, constraints. Be specific.
- **Task:** Your responsibility — what were YOU accountable for?
- **Action:** What YOU did. Use "I", not "we". Focus on decisions and trade-offs.
- **Result:** Quantify. Revenue, time saved, reliability improved, team grew.
- Common mistakes: too much Situation, not enough Action; saying "we" throughout; no numbers in Result.

## Key Questions
- Tell me about a time you dealt with conflict on your team.
- Tell me about a time you had to influence without authority.
- Tell me about a time a project failed. What did you do?
- Tell me about a time you drove a large technical change.

## Summary
The STAR method structures behavioral interview answers to be specific, verifiable, and impactful. The Action section is the most important — interviewers want to understand your decision-making process, not just the outcome. Quantify results whenever possible (e.g., "reduced training time by 40%", "grew team from 5 to 12 engineers").

## Raw Material
```

- [ ] **Step 8: Create seed note for management/people — Engineering Team Management**

Create `skills/management/people/Engineering Team Management.md`:

```markdown
---
title: Engineering Team Management
category: management/people
tags: [people-management, team-building, performance, hiring, eng-manager]
status: stub
priority: high
last_updated: 2026-04-06
created_from_jd:
---

# Engineering Team Management

## Knowledge Map
- 前置知识：[[STAR Method]]
- 延伸话题：[[Hiring and Interviewing]], [[Performance Reviews]], [[Technical Roadmap]]
- 管理关联：[[Project Management]]

## Core Concepts
<!-- To be filled by raw-material-processor skill -->

## Key Questions
<!-- To be filled by raw-material-processor skill -->

## Summary
<!-- To be filled by raw-material-processor skill -->

## Raw Material
```

- [ ] **Step 9: Create seed note for management/project — Technical Roadmap**

Create `skills/management/project/Technical Roadmap.md`:

```markdown
---
title: Technical Roadmap
category: management/project
tags: [roadmap, planning, prioritization, stakeholders, project-management]
status: stub
priority: medium
last_updated: 2026-04-06
created_from_jd:
---

# Technical Roadmap

## Knowledge Map
- 前置知识：[[Engineering Team Management]]
- 延伸话题：[[OKRs and Goal Setting]], [[Cross-team Collaboration]], [[Risk Management]]
- 管理关联：[[People Management]]

## Core Concepts
<!-- To be filled by raw-material-processor skill -->

## Key Questions
<!-- To be filled by raw-material-processor skill -->

## Summary
<!-- To be filled by raw-material-processor skill -->

## Raw Material
```

- [ ] **Step 10: Commit**

```bash
git add skills/
git commit -m "feat: add seed skill notes for all 9 categories"
```

---

## Task 5: jd-analyzer Claude Skill

**Files:**
- Create: `.claude/skills/jd-analyzer/SKILL.md`

- [ ] **Step 1: Create SKILL.md**

Create `.claude/skills/jd-analyzer/SKILL.md`:

````markdown
# jd-analyzer

Analyze a Job Description note and populate its analysis sections by comparing against the existing knowledge base.

## When to Use

When the user has pasted a JD into a `positions/` note and wants to:
- Extract key skill requirements
- See which skills are already in the knowledge base vs missing
- Get a prioritized prep checklist
- Find which experience notes are most relevant
- Get resume tailoring suggestions

## Inputs

- **JD note path** (required): the positions/ note containing the raw JD text
- **Resume base**: `_meta/resume-base.md` (used for resume tailoring section)

## Steps

### 1. Read the JD note

Read the full content of the JD note provided by the user. Focus on:
- Required skills and technologies (hard requirements)
- Preferred/nice-to-have skills
- Leadership scope (team size, org level, cross-functional scope)
- Company/domain context

### 2. Extract Key Requirements

Produce a structured list:
- **Required technical skills**: specific technologies, frameworks, platforms mentioned
- **Required leadership/management**: team size, scope, experience level
- **Nice-to-have**: preferred but not blocking
- **Domain signals**: what kind of AI/ML work, scale of infra, stage of company

### 3. Scan the knowledge base

Read frontmatter from ALL files in `skills/` directory (title, category, tags, status).
Read frontmatter from ALL files in `experience/` directory (title, skills, impact).

Match JD requirements against:
- Skill note titles and tags
- Experience note skills arrays

### 4. Build the Skill Gap Analysis table

For each required skill from the JD:
- If a matching skill note exists: record its current status and set priority = high
- If NO matching skill note exists: 
  - Create a stub note in the appropriate `skills/` subdirectory (see "Creating Stub Notes" below)
  - Record status = stub, priority = high

For nice-to-have skills: same logic but priority = medium.

Format as:
```
| Skill | Status | Priority |
|-------|--------|----------|
| GPU Cluster Management | in-progress | high |
| NCCL | stub | high |
| Kubernetes | reviewed | medium |
```

### 5. Create stub notes for missing skills

For each skill not found in the knowledge base, create a stub note:

Determine the correct subdirectory:
- AI training, inference, MLOps, GPU, CUDA → `skills/tech/ai-infra/`
- LLM, ML theory, deep learning → `skills/tech/ai-basics/`
- K8s, cloud, networking, storage, containers → `skills/tech/infra/`
- System design, distributed systems → `skills/tech/system-design/`
- Algorithms, data structures → `skills/tech/algorithms/`
- Design patterns, software practices → `skills/tech/software-eng/`
- Behavioral, leadership stories → `skills/management/behavior/`
- Team, hiring, performance → `skills/management/people/`
- Roadmap, planning, stakeholders → `skills/management/project/`

Stub note format:
```markdown
---
title: [Skill Name]
category: tech/[subcategory]
tags: []
status: stub
priority: high
last_updated: [today's date YYYY-MM-DD]
created_from_jd: [[positions/[JD filename]]]
---

# [Skill Name]

## Knowledge Map
- 前置知识：
- 延伸话题：
- 管理关联：

## Core Concepts
<!-- To be filled by raw-material-processor skill after you find learning materials -->

## Key Questions
<!-- To be filled by raw-material-processor skill -->

## Summary
<!-- To be filled by raw-material-processor skill -->

## Raw Material
<!-- Save source articles to raw_material/ then link here -->
```

### 6. Build Prep Checklist

Order by: stub (most urgent) → draft → in-progress, then by priority high → medium.

Format:
```
- [ ] **[high]** Learn [Skill] — no notes yet, find learning material first (`stub`)
- [ ] **[high]** Review and complete [Skill] notes (`draft`)
- [ ] **[medium]** Finalize [Skill] review (`in-progress`)
- [ ] **[medium]** Refresh [Skill] — already reviewed but relevant (`reviewed`)
```

### 7. Find Experience Matches

Scan `experience/` notes. For each experience note, check if its `skills` array overlaps with the JD's required skills. List the top 3-5 most relevant, with a one-line note on why.

Format:
```
- [[experience/[Title]]] — relevant for [JD skill 1], [JD skill 2]
```

### 8. Resume Tailoring

Read `_meta/resume-base.md`.

Produce three outputs:

**关键词匹配 table**: JD keyword → suggested rephrasing from resume-base content.
Only suggest changes where resume-base has content that could be reworded to match JD language.

**建议强调的 Experience**: Which experience/ notes have the highest overlap with this JD. List them in priority order with reason.

**建议弱化的内容**: Identify resume-base content (roles, projects, skills) that is NOT relevant to this JD and would dilute focus. Suggest de-emphasizing or moving to an appendix.

### 9. Write all sections into the JD note

Update the JD note by filling in:
- `## Key Requirements`
- `## Skill Gap Analysis` table
- `## Prep Checklist`
- `## Experience Match`
- `## Resume Tailoring` (all three subsections)

Also update the JD note frontmatter: set `status: ready`.

## Output

The updated JD note with all sections filled. Summary to user:
- N required skills found
- M skills already in knowledge base (with status breakdown)
- K stub notes created
- Top 3 experience matches
````

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/jd-analyzer/
git commit -m "feat: add jd-analyzer claude skill"
```

---

## Task 6: raw-material-processor Claude Skill

**Files:**
- Create: `.claude/skills/raw-material-processor/SKILL.md`

- [ ] **Step 1: Create SKILL.md**

Create `.claude/skills/raw-material-processor/SKILL.md`:

````markdown
# raw-material-processor

Read a raw material note and distill its content into the corresponding skill note.

## When to Use

When the user has saved a source article or learning material into `raw_material/` and wants Claude to:
- Extract the key concepts
- Generate interview-ready questions and answer frameworks
- Write a concise summary
- Update the linked skill note

## Inputs

- **Raw material note path** (required): the `raw_material/` note to process
- Optionally: a directory path to process all unprocessed notes in bulk (`processed: false`)

## Steps

### 1. Read the raw material note

Read the full content. Note the `skill_note` frontmatter field — this is the path to the corresponding skill note.

If `skill_note` is empty:
- Infer the skill note path from the raw material's filename and location.
  - `raw_material/tech/ai-infra/nccl-overview.md` → look for a skill note in `skills/tech/ai-infra/` whose title or filename matches "nccl" or "NCCL".
- If no matching skill note exists, create a new stub note first (see "Creating a new skill note" below), then proceed.

### 2. Read the current skill note

Read the skill note to understand:
- What's already in Core Concepts, Key Questions, Summary (avoid duplication)
- Current status (stub/draft/in-progress)
- Existing wikilinks in Knowledge Map (don't remove them)

### 3. Distill Core Concepts

From the raw material, extract 5-10 bullet points covering:
- The main idea / what this technology/concept does
- Key mechanisms or algorithms (how it works internally)
- When to use it vs alternatives (trade-offs)
- Important numbers, limits, or benchmarks if present
- Common failure modes or gotchas

Format as concise bullets. Each bullet should be self-contained.

### 4. Generate Key Questions

Produce 5-8 interview questions that could be asked about this topic, with answer frameworks (not full answers — just the structure a good answer would follow).

Format:
```
**Q: [Question]**
Answer framework: [2-3 sentence structure for a strong answer]
```

Prioritize questions that:
- Test depth of understanding (not just definition recall)
- Could reveal design trade-offs
- Are commonly asked in FAANG/AI company interviews for infra/engineering manager roles

### 5. Write the Summary

Write a 2-3 paragraph synthesis that:
- Explains what the topic is and why it matters for AI Infra
- Covers the most important technical depth points
- Connects to adjacent topics (what you need to know before/after this)

This should be readable as a standalone review note — assume the reader won't go back to the raw material.

### 6. Update the Knowledge Map (if applicable)

If the raw material mentions technologies or concepts that should be wikilinked but aren't in the skill note's Knowledge Map yet, suggest additions in the 延伸话题 section. Do NOT remove existing wikilinks.

### 7. Update the skill note

Write the distilled content into the skill note:
- Fill `## Core Concepts` (append if content already exists; don't overwrite)
- Fill `## Key Questions` (append if content already exists)
- Fill `## Summary` (replace if stub placeholder, append otherwise)
- Add a link under `## Raw Material`: `- [[raw_material/[path/to/note]]]`
- Update `last_updated` frontmatter to today's date
- Advance `status`:
  - `stub` → `draft`
  - `draft` → `in-progress`
  - `in-progress` stays `in-progress` (user marks as reviewed manually)

### 8. Mark raw material as processed

Update the raw material note's frontmatter:
- Set `processed: true`
- Set `skill_note: [[skills/path/to/SkillNote]]` if it was empty

### Creating a new skill note

If no matching skill note exists for a raw material:
1. Determine correct subdirectory (same logic as jd-analyzer)
2. Create the note using the standard template structure (see spec)
3. Set `status: stub`, then this skill will advance it to `draft`

## Output

Summary to user:
- Skill note updated: [path]
- Sections updated: Core Concepts, Key Questions, Summary
- Status advanced: [old] → [new]
- Raw material marked processed: [path]
````

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/raw-material-processor/
git commit -m "feat: add raw-material-processor claude skill"
```

---

## Task 7: Smoke Test — End-to-End Workflow

Verify the vault and skills work correctly with a sample run.

- [ ] **Step 1: Verify directory structure is complete**

```bash
find . -type d | grep -v '.git' | sort
```

Expected directories (17 skill dirs + 9 raw_material dirs + positions + experience + _templates + _meta + .claude/skills):
```
./.claude
./.claude/skills
./.claude/skills/jd-analyzer
./.claude/skills/raw-material-processor
./_meta
./_templates
./docs
./experience
./positions
./raw_material
./raw_material/management
./raw_material/management/behavior
./raw_material/management/people
./raw_material/management/project
./raw_material/tech
./raw_material/tech/ai-basics
./raw_material/tech/ai-infra
./raw_material/tech/algorithms
./raw_material/tech/infra
./raw_material/tech/software-eng
./raw_material/tech/system-design
./skills
./skills/management
./skills/management/behavior
./skills/management/people
./skills/management/project
./skills/tech
./skills/tech/ai-basics
./skills/tech/ai-infra
./skills/tech/algorithms
./skills/tech/infra
./skills/tech/software-eng
./skills/tech/system-design
```

- [ ] **Step 2: Verify seed skill notes exist**

```bash
find skills/ -name "*.md" | sort
```

Expected: 9 seed notes, one per category.

- [ ] **Step 3: Verify templates exist**

```bash
ls _templates/
```

Expected: `experience-template.md  jd-template.md  raw-material-template.md  skill-template.md`

- [ ] **Step 4: Verify Claude skills exist**

```bash
ls .claude/skills/jd-analyzer/
ls .claude/skills/raw-material-processor/
```

Expected: `SKILL.md` in each.

- [ ] **Step 5: Create a sample raw material note and run raw-material-processor**

Create `raw_material/tech/ai-infra/sample-gpu-overview.md`:

```markdown
---
title: Sample GPU Overview
source: https://example.com
date_saved: 2026-04-06
processed: false
skill_note: [[skills/tech/ai-infra/GPU Cluster Management]]
---

# Sample GPU Overview

GPUs accelerate deep learning by parallelizing matrix operations.
Key components: CUDA cores, memory bandwidth, NVLink for multi-GPU.
NCCL handles collective communication (AllReduce, Broadcast) across GPUs.
Common configurations: 8xA100 per node, NVLink within node, InfiniBand across nodes.
Key metric: GPU utilization — should be >85% during training. Low utilization indicates data loading bottleneck.
```

Then invoke: `/raw-material-processor` on `raw_material/tech/ai-infra/sample-gpu-overview.md`

Expected result:
- `skills/tech/ai-infra/GPU Cluster Management.md` updated with Core Concepts, Key Questions, Summary
- `raw_material/tech/ai-infra/sample-gpu-overview.md` frontmatter has `processed: true`
- Skill note status advanced from `stub` → `draft`

- [ ] **Step 6: Create a sample JD note and run jd-analyzer**

Create `positions/Sample AI Infra Manager - Test Co.md`:

```markdown
---
title: Sample AI Infra Manager - Test Co
company: Test Co
date_added: 2026-04-06
status: analyzing
growing_link:
---

# Sample AI Infra Manager - Test Co

## Raw JD
We are looking for an AI Infrastructure Manager to lead our GPU cluster operations team.

Requirements:
- 5+ years managing large-scale GPU clusters (A100/H100)
- Deep knowledge of NCCL and distributed training frameworks (PyTorch, DeepSpeed)
- Experience with Kubernetes for ML workloads
- Strong understanding of InfiniBand and high-speed networking
- Experience managing a team of 8-15 infrastructure engineers
- Proven ability to drive cross-functional technical projects

Nice to have:
- Experience with model serving and inference optimization
- Knowledge of cost optimization for GPU fleets
- Experience with on-premise to cloud hybrid deployments
```

Then invoke: `/jd-analyzer` on `positions/Sample AI Infra Manager - Test Co.md`

Expected result:
- Key Requirements section populated
- Skill Gap Analysis table filled (GPU Cluster Management found as draft, NCCL likely stub)
- Stub notes created for any skills not yet in knowledge base
- Prep Checklist generated
- Experience Match section populated (empty if no experience notes exist yet)
- Resume Tailoring section populated
- JD note `status` updated to `ready`

- [ ] **Step 7: Final commit**

```bash
git add .
git commit -m "test: add smoke test sample files for raw-material-processor and jd-analyzer"
```

---

## Self-Review

**Spec coverage check:**

| Spec Requirement | Covered by Task |
|-----------------|----------------|
| Vault directory structure | Task 1 |
| skill-template.md | Task 2 |
| experience-template.md | Task 2 |
| jd-template.md | Task 2 |
| raw-material-template.md | Task 2 |
| _meta/index.md with Dataview | Task 3 |
| _meta/resume-base.md | Task 3 |
| Seed skill notes | Task 4 |
| jd-analyzer skill | Task 5 |
| raw-material-processor skill | Task 6 |
| Status lifecycle (stub→draft→in-progress→reviewed) | Tasks 4, 5, 6 |
| growing_link field in experience + JD notes | Tasks 2 (templates) |
| Stub note creation in jd-analyzer | Task 5 |
| processed: true marking in raw-material-processor | Task 6 |
| Resume Tailoring section in JD note | Tasks 2, 5 |
| End-to-end workflow verification | Task 7 |

All spec requirements covered. No gaps found.
