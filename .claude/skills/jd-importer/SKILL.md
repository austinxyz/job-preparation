---
name: jd-importer
description: Use when the user has a raw JD file in jobs/ root and wants to normalize it into the per-company structure before running jd-analyzer.
---

# jd-importer

Convert a raw JD file at `jobs/` root into a properly formatted JD note ready for `jd-analyzer`, and create the per-company folder structure.

## When to Use

- User has dropped a raw JD into `jobs/` (root) and wants to process it
- User says "process this JD" or "import this JD"

## Inputs

- **Raw JD file path** (required): a file at `jobs/<something>.md` or `jobs/<something>.txt` at the root of `jobs/`. If the user doesn't specify, list raw-looking files in `jobs/` (ignoring `README.md` and any `<Company>/` sub-directories) and ask which to process.

## Steps

### 1. Read the raw JD text

Read the full text of the file the user points to.

### 2. Extract metadata from the JD text

Scan the text to identify:
- **Job title**: Usually in the heading or first few lines
- **Company name**: Usually in the heading, intro paragraph, or "About Us" section
- **Role summary**: one-line description for frontmatter

If any field is ambiguous, make a reasonable inference and note it in your reply — do not ask the user first.

### 3. Normalize the raw-JD filename

Rename (or preserve) the raw JD file in `jobs/` root to follow this convention:

```
jobs/<Job Title> - <Company>.md
```

Sanitize: replace `/` with `-`, remove colons. If the source file was `.txt`, convert to `.md` during normalization.

If the file is already correctly named, skip the rename.

### 4. Rewrite the raw JD file with proper frontmatter

Ensure the file has this exact frontmatter at the top:

```markdown
---
title: <Job Title> - <Company>
company: <Company>
role: <Job Title>
date_added: <today YYYY-MM-DD>
analysis_file: "[[jobs/<Company>/jd-analysis]]"
---

# <Job Title> - <Company>

## Raw JD

<paste the original raw JD text here, unmodified except for markdown formatting of bullet lists if they came in as plain lines>
```

Do NOT add analysis sections here — those belong in `jd-analysis.md`.

### 5. Create the per-company folder structure

Create (if not already present):

```
jobs/<Company>/
├── (jd-analysis.md — created later by jd-analyzer)
├── (resume.md — created later by resume-builder)
├── contacts/
├── prep/
├── mocks/
└── correspondence/
```

Create the sub-directories as empty folders so the user has the right slots ready.

### 6. Create a starter README.md for the company folder

Create `jobs/<Company>/README.md` as the job dashboard:

```markdown
---
title: <Company> — <Job Title>
type: Job Dashboard
company: <Company>
role: <Job Title>
status: jd-imported
date_added: <today YYYY-MM-DD>
last_updated: <today YYYY-MM-DD>
---

# <Company> — <Job Title>

## Status

⚪ **Stage:** JD imported — pending analysis

**Next actions:**
- [ ] Run `/jd-analyzer` on [[jobs/<Job Title> - <Company>]] to generate analysis + skill gap + prep checklist
- [ ] Run `/resume-builder` once analysis is complete

---

## Key Artifacts

- **Raw JD:** [[jobs/<Job Title> - <Company>]]
- **JD analysis:** (not yet generated — run `/jd-analyzer`)
- **Resume (role-tailored):** (not yet generated — run `/resume-builder`)
- **Contacts log:** `jobs/<Company>/contacts/`
- **Round prep docs:** `jobs/<Company>/prep/`
- **Mocks:** `jobs/<Company>/mocks/`
- **Correspondence:** `jobs/<Company>/correspondence/`

---

## Log

- **<today>** — Raw JD imported; folder structure created. Next step: `/jd-analyzer`.
```

### 7. Report to user

Tell the user:
- Raw JD normalized: `jobs/<Job Title> - <Company>.md`
- Folder created: `jobs/<Company>/` with sub-dirs (contacts, prep, mocks, correspondence)
- Dashboard created: `jobs/<Company>/README.md`
- Inferred metadata: title = "<X>", company = "<Y>" (so user can correct if wrong)
- Next step: run `/jd-analyzer` pointing to `jobs/<Job Title> - <Company>.md`

## Output

- One normalized raw JD file in `jobs/` root
- One new company folder with sub-dirs + README
- Short summary message with inferred metadata and next-step prompt
