# resume-builder

Generate a tailored, interview-ready resume for a specific JD position by combining `_meta/resume-base.md` with the analysis from the positions/ note.

## When to Use

When the user wants to produce a customized resume for a specific job application. Requires `jd-analyzer` to have already run on the target positions/ note (so that Resume Tailoring analysis is available).

## Inputs

- **JD note path** (required): e.g. `positions/Manager, DevOps Engineering - NVIDIA.md`

## Steps

### 1. Read inputs

Read in parallel:
- The positions/ note (for: Key Requirements, Resume Tailoring section — keyword matches, experience priorities, de-emphasis list)
- `_meta/resume-base.md` (full unabridged resume content)

If the positions/ note has no `## Resume Tailoring` section, stop and tell the user to run `/jd-analyzer` first.

### 2. Read top experience notes

From the Resume Tailoring → 建议强调的 Experience list, read the top 3–4 experience/ notes in full. These provide the detailed bullet content to draw from.

### 3. Determine output filename

Format: `resumes/[Company] - [Short Role Title] - [YYYY-MM].md`

Example: `resumes/NVIDIA - Manager DevOps Engineering - 2026-04.md`

Extract company name and role from the positions/ note frontmatter (`company`, `title`). Use today's date for YYYY-MM.

### 4. Write the tailored resume

Generate a complete, ATS-optimized resume in markdown. Follow this structure exactly:

---

```markdown
---
position: [Full JD title]
company: [Company]
generated: [YYYY-MM-DD]
base_version: _meta/resume-base.md
jd_note: positions/[filename]
---

# [Your Name]

[Phone] | [Email] | [LinkedIn] | [GitHub]

---

## Summary

[2–3 sentences, tailored to this specific JD. Use JD language. Lead with years of experience + the exact role type. Mention 2–3 of the JD's most important keywords naturally. Do NOT copy generic summary from resume-base — write fresh for this JD.]

---

## Experience

### [Job Title] — [Company], [Location] ([Start] – [End])

[4–6 bullets. Reorder and rephrase bullets from resume-base to lead with JD-relevant content. Use exact JD keywords where truthful. Quantify every bullet that can be quantified. Put the most JD-relevant bullet FIRST.]

### [Job Title] — [Company], [Location] ([Start] – [End])

[3–5 bullets. Apply same tailoring. For older roles, keep shorter.]

[Continue for all roles in resume-base, compressing older/less-relevant roles to 2–3 bullets or a single line.]

---

## Skills

[Reorganize skills from resume-base to front-load the skills most relevant to this JD. Group by category. If JD mentions a specific technology, make sure it appears in skills.]

**[Category most relevant to JD]:** [tools/techs]
**[Category 2]:** [tools/techs]
...

---

## Education

[Verbatim from resume-base — no changes needed.]

## Certifications

[Verbatim from resume-base.]
```

---

### Tailoring rules

**User comments take highest priority:**

The 关键词匹配 table may contain a "我的comments" (or "comments") column added by the user. This column overrides AI suggestions for that row.

For each row in 关键词匹配:
- If the "我的comments" column is **non-empty**: use the user's comment as the primary directive for how to handle that keyword. The 建议优化 column becomes secondary reference only.
- If the "我的comments" column is **empty**: apply the 建议优化 suggestion as written.

User comment patterns and how to interpret them:
- "不用加" / "skip" / "不需要" → do NOT include this keyword or the suggested bullet; omit entirely
- "保持原来" / "keep as is" → copy the existing resume-base bullet verbatim, no rewording
- A rewritten phrase or specific wording → use that exact phrasing in the resume bullet
- "弱化" / "de-emphasize" → mention briefly in passing, do not give a standalone bullet
- "放在X角色" / "move to [role]" → place this content under the specified role instead of the current one
- Any other instruction → follow it literally

**Summary:**
- Must mention: years of experience, the exact management level (EM of EMs vs IC EM), domain (DevOps / AI Infra / Platform Eng)
- Must use 2–3 exact phrases from JD's "What You'll Be Doing" or "What We Need To See"
- No buzzword soup — each sentence must be grounded in a real credential

**Experience bullets:**
- Apply keyword handling from 关键词匹配 table, **respecting user comments first**
- De-emphasize content from 建议弱化的内容 list (move to brief mention or omit)
- Elevate content from 建议强调的 Experience list — give these roles more bullets
- Each bullet: lead with a verb (Led, Built, Designed, Reduced, Achieved), follow with what, then result
- Never fabricate metrics — only use numbers that appear in resume-base or experience/ notes

**Skills section:**
- Put the JD's primary technical domain first (e.g., if JD is CI/CD-heavy, put CI/CD skills first)
- Include every tool explicitly named in the JD if it appears anywhere in resume-base
- Remove or demote skills the JD doesn't mention and that may signal misalignment (e.g., GPU/ML skills for a non-ML DevOps role)

**What to omit entirely:**
- Hobbies/side projects unless specifically relevant to this JD
- Technologies that signal the wrong domain (per 建议弱化的内容)
- Any bullet that does not relate to this JD's requirements

### 5. Update resumes/README.md

Add a row to the index table:
```
| [filename] | [Position] | [date] | generated |
```

### 6. Output summary to user

- Resume written to: `resumes/[filename]`
- User comments applied: [for each row with a non-empty 我的comments, briefly note what directive was followed]
- Keywords injected: [list top 5 JD keywords used]
- Sections de-emphasized: [list what was removed/compressed]
- Suggested next step: review the generated resume, edit any bullet that doesn't feel authentic, then export to PDF

## Notes

- The generated resume is a **starting draft** — the user should review every bullet for authenticity before submitting
- Never invent metrics or claims not supported by resume-base or experience/ notes
- If a JD keyword has no honest mapping in the user's background, do NOT force it — note it as a gap instead
- The markdown format can be converted to PDF using Pandoc, Obsidian's export, or a markdown-to-PDF tool
