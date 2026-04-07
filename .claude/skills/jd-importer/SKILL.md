---
name: jd-importer
description: Use when the user has a raw JD file under raw_material/positions/ and wants to create a structured positions/ note before running jd-analyzer.
---

# jd-importer

Convert a raw JD file from `raw_material/positions/` into a properly formatted `positions/` note ready for `jd-analyzer`.

## When to Use

- User has saved a JD into `raw_material/positions/` and wants to convert it
- User says "process this JD" or "create a position note for this JD"

## Steps

### 1. Get the raw JD text

Read the file the user points to under `raw_material/positions/`.
If the user doesn't specify a file, list files in `raw_material/positions/` and ask which one to process.

### 2. Extract metadata from the JD text

Scan the text to identify:
- **Job title**: Usually in the heading or first few lines (e.g. "Senior AI Infrastructure Manager", "Director of ML Platform")
- **Company name**: Usually in the heading, intro paragraph, or "About Us" section

If either field is ambiguous, make a reasonable inference and note it in your reply — do not ask the user first.

### 3. Build the file path

```
positions/{Job Title} - {Company}.md
```

Examples:
- `positions/AI Infra Manager - DeepMind.md`
- `positions/Staff ML Platform Engineer - Anthropic.md`

If the title contains slashes or special characters, sanitize them (replace `/` with `-`, remove colons).

### 4. Create the positions/ note

Use this exact structure:

```markdown
---
title: {Job Title} - {Company}
company: {Company}
date_added: {today YYYY-MM-DD}
status: analyzing
match_score:
growing_link:
---

# {Job Title} - {Company}

## Raw JD
{paste full original JD text here, unmodified}

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

### 5. Report to user

Tell the user:
- File created: `positions/{filename}.md`
- Inferred title and company (so they can correct if wrong)
- Next step: run `/jd-analyzer` on this file

## Output

One created file. Short summary message with inferred metadata and next-step prompt.
