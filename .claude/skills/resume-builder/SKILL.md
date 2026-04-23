# resume-builder

Generate a tailored, interview-ready resume for a specific job by combining `_meta/resume-base.md` with the analysis output from `jobs/<Company>/jd-analysis.md`. Output is written into the per-company folder under `jobs/`.

## When to Use

When the user wants to produce a customized resume for a specific job application. Requires `/jd-analyzer` to have already run and produced `jobs/<Company>/jd-analysis.md` (so that Resume Tailoring analysis is available).

## Inputs

- **Raw JD path or Company name** (required): e.g. `jobs/Manager, DevOps, SRE & AI Infrastructure - AppZen.md` or just "AppZen"

From either input, derive:
- The raw JD file (in `jobs/` root)
- The per-company folder `jobs/<Company>/`
- The analysis file `jobs/<Company>/jd-analysis.md`

## Steps

### 1. Read inputs

Read in parallel:
- The raw JD file (for company, role, JD language)
- `jobs/<Company>/jd-analysis.md` (for Key Requirements, Resume Tailoring section — keyword matches, experience priorities, de-emphasis list)
- `_meta/resume-base.md` (full unabridged resume content)

If `jobs/<Company>/jd-analysis.md` has no `## Resume Tailoring` section, stop and tell the user to run `/jd-analyzer` first.

### 2. Read top experience notes

From the Resume Tailoring → 建议强调的 Experience list, read the top 3–4 experience/ notes in full. These provide the detailed bullet content to draw from.

### 3. Determine output path

The resume is always written to:

```
jobs/<Company>/resume.md
```

Overwrite if it exists (user is re-generating after feedback or analysis updates).

### 4. Write the tailored resume

Generate a complete, ATS-optimized resume in markdown. Follow this structure exactly:

---

```markdown
---
position: [Full JD title]
company: [Company]
generated: [YYYY-MM-DD]
base_version: "[[_meta/resume-base]]"
source_jd: "[[jobs/<Job Title> - <Company>]]"
jd_analysis: "[[jobs/<Company>/jd-analysis]]"
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

### 5. Update the company README

Update `jobs/<Company>/README.md`:
- Update "Key Artifacts → Resume" to link `jobs/<Company>/resume.md`
- Change status frontmatter to `resume-ready` (if currently `jd-analyzed`)
- Add log entry: "YYYY-MM-DD — Role-tailored resume generated."

### 6. Output summary to user

- Resume written to: `jobs/<Company>/resume.md`
- User comments applied: [for each row with a non-empty 我的comments, briefly note what directive was followed]
- Keywords injected: [list top 5 JD keywords used]
- Sections de-emphasized: [list what was removed/compressed]
- Suggested next step: review the generated resume, edit any bullet that doesn't feel authentic, then export to PDF

## Notes

- The generated resume is a **starting draft** — the user should review every bullet for authenticity before submitting
- Never invent metrics or claims not supported by resume-base or experience/ notes
- If a JD keyword has no honest mapping in the user's background, do NOT force it — note it as a gap instead
- The markdown format can be converted to PDF using Pandoc, Obsidian's export, or a markdown-to-PDF tool
