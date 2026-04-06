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
