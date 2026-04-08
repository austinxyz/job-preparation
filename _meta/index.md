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
