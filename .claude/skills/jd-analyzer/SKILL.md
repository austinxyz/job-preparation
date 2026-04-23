# jd-analyzer

Analyze a Job Description (raw JD in `jobs/` root) and produce a `jobs/<Company>/jd-analysis.md` file populated with match score, key requirements, skill gap, prep checklist, experience match, and resume tailoring directives.

## When to Use

When the user has a raw JD file at `jobs/<Job Title> - <Company>.md` (typically via `jd-importer`) and wants to:
- Get a match score against current background
- Extract key skill requirements
- See which skills are already in the knowledge base vs missing
- Get a prioritized prep checklist
- Find which experience notes are most relevant
- Get resume tailoring suggestions

## Inputs

- **Raw JD path** (required): e.g. `jobs/Manager, DevOps, SRE & AI Infrastructure - AppZen.md`
- **Resume base**: `_meta/resume-base.md` (used for resume tailoring section)

## Output

- `jobs/<Company>/jd-analysis.md` — the analysis note (created or overwritten)
- Stub skill notes in `skills/` for any missing required skills (unless `not-matched`)
- Updated `jobs/<Company>/README.md` with analysis link and next-step prompts

## Steps

### 1. Read the raw JD

Read the full content of the JD file provided by the user. Focus on:
- Required skills and technologies (hard requirements)
- Preferred/nice-to-have skills
- Leadership scope (team size, org level, cross-functional scope)
- Company/domain context

Extract the company name from the JD frontmatter (`company:` field) — this determines the target folder `jobs/<Company>/`.

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

### 4. Calculate Match Score

Assess overall fit across two dimensions:

**Technical fit**: How many required technical skills are covered by existing skill notes (any status) or experience notes?

**Leadership/experience fit**: Does the management scope, years of experience, and domain align with the user's background (infer from `experience/` notes)?

Assign one of four scores:

| Score | Criteria |
|-------|----------|
| **strong-matched** | 80%+ required skills covered; leadership scope and domain strongly align |
| **matched** | 60–79% required skills covered; leadership scope reasonably aligns |
| **matched-with-gaps** | 40–59% required skills covered, OR key leadership/domain requirements are a stretch |
| **not-matched** | <40% required skills covered, OR fundamental misalignment (wrong role type, missing core qualifications) |

**Present the score to the user now** with a 2-3 sentence rationale before continuing.

---

### If `not-matched`: STOP here

Create `jobs/<Company>/jd-analysis.md` with only:
- Frontmatter: `match_score: not-matched`, `status: not-pursued`
- Match score section with rationale
- Key Requirements section (already extracted)
- Brief note: "Not pursued — reason: [rationale]."

Update `jobs/<Company>/README.md`:
- Status: 🔴 not-pursued
- Do NOT create stub notes, prep checklist, or resume tailoring for not-matched positions.

---

### 5. Build the Skill Gap Analysis table

_(Only for strong-matched / matched / matched-with-gaps)_

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

### 6. Create stub notes for missing skills

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

Stub note format (note the `created_from_jd` wikilink now points into `jobs/` root):
```markdown
---
title: [Skill Name]
category: tech/[subcategory]
tags: []
status: stub
priority: high
last_updated: [today's date YYYY-MM-DD]
created_from_jd: "[[jobs/[Job Title] - [Company]]]"
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

### 7. Build Prep Checklist

Order by: stub (most urgent) → draft → in-progress, then by priority high → medium.

Format:
```
- [ ] **[high]** Learn [Skill] — no notes yet, find learning material first (`stub`)
- [ ] **[high]** Review and complete [Skill] notes (`draft`)
- [ ] **[medium]** Finalize [Skill] review (`in-progress`)
- [ ] **[medium]** Refresh [Skill] — already reviewed but relevant (`reviewed`)
```

### 8. Find Experience Matches

Scan `experience/` notes. For each experience note, check if its `skills` array overlaps with the JD's required skills. List the top 3-5 most relevant, with a one-line note on why.

Format:
```
- [[experience/[Title]]] — relevant for [JD skill 1], [JD skill 2]
```

### 9. Resume Tailoring

Read `_meta/resume-base.md`.

Produce three outputs:

**关键词匹配 table**: JD keyword → suggested rephrasing from resume-base content.
Only suggest changes where resume-base has content that could be reworded to match JD language.

**建议强调的 Experience**: Which experience/ notes have the highest overlap with this JD. List them in priority order with reason.

**建议弱化的内容**: Identify resume-base content (roles, projects, skills) that is NOT relevant to this JD and would dilute focus. Suggest de-emphasizing or moving to an appendix.

### 10. Write the analysis file

Create `jobs/<Company>/jd-analysis.md` with this structure:

```markdown
---
title: <Company> JD Analysis
type: JD Analysis
company: <Company>
role: <Job Title>
date_added: <today YYYY-MM-DD>
last_updated: <today YYYY-MM-DD>
status: prep-in-progress
match_score: <matched / strong-matched / matched-with-gaps / not-matched>
source_jd: "[[jobs/<Job Title> - <Company>]]"
---

# <Company> JD Analysis

Analysis output for [[jobs/<Job Title> - <Company>]]. Covers match score, key requirements, skill gap, prep checklist, experience match, and resume tailoring.

---

## Match Score

**<score>** — 2-3 sentence rationale.

---

## Key Requirements

[from step 2]

---

## Skill Gap Analysis

[from step 5]

---

## Prep Checklist

[from step 7]

---

## Experience Match

[from step 8]

---

## Resume Tailoring

### 关键词匹配

[from step 9]

### 建议强调的 Experience

[from step 9]

### 建议弱化的内容

[from step 9]

---

## Progress Log

- **<today>** — JD analyzed. Match score: <score>. Skill gap: N skills, M stubs created.
```

### 11. Update the company README

Update `jobs/<Company>/README.md`:
- Change `status:` frontmatter to `jd-analyzed`
- Update "Key Artifacts" section to link the newly created `jd-analysis.md`
- Add the next-step prompt: "Run `/resume-builder` to generate role-tailored resume"
- Add log entry: "YYYY-MM-DD — JD analyzed. Match score: <score>."

## Output Summary to User

- Match score + rationale
- N required skills found
- M skills already in knowledge base (with status breakdown)
- K stub notes created (or "none — not-matched position")
- Top 3 experience matches (if applicable)
- File written: `jobs/<Company>/jd-analysis.md`
- README updated: `jobs/<Company>/README.md`
- Suggested next step: `/resume-builder` pointing to the raw JD file
