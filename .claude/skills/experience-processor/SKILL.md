# experience-processor

Read a raw experience note and distill it into a polished STAR-format experience note, saved to `experience/`.

## When to Use

When the user has saved a rough story, narrative dump, or interview Q&A into `raw_material/experience/` and wants Claude to:
- Restructure the content into clean STAR format
- Identify applicable skills and BQ question mappings
- Generate Key Questions with talking-point frameworks
- Write a Summary paragraph for quick pre-interview review
- Link back to the raw material source
- Produce a polished, interview-ready experience note

## Inputs

- **Raw material path** (required): path to the note under `raw_material/experience/`

## Steps

### 1. Read the raw material

Read the full content of the raw material note. It may contain any combination of:
- Freeform narrative paragraphs
- A "Story" section
- Raw interview Q&A transcripts
- Bullet points or fragments

Extract from the content (or infer if not explicitly stated):
- **Company** name
- **Approximate date** (YYYY-MM; default to company tenure period if unknown)
- **Event/story title** (use filename if not clear)
- **Core technical or leadership challenge**

### 2. Determine output path

The experience note should be saved to `experience/` at the top level.

- Filename format: `{Company} - {Short Title}.md`
  - e.g., `eBay - Resolving L7 Traffic Gap.md`
- Check if a note with this name (or very similar) already exists in `experience/`. If so, ask the user before overwriting.

### 3. Distill into STAR format

Rewrite the raw content into four clean sections. Be concise and specific — avoid filler phrases like "I took the initiative to" or "This experience taught me." Prioritize concrete actions and quantified outcomes.

#### Situation
- Set the stage: company, team, the problem or context
- Include scale/stakes if relevant (revenue impact, user count, system scale)
- 2–4 sentences

#### Task
- Your specific scope of ownership or responsibility
- What decision or outcome you were accountable for
- 2–3 sentences

#### Action
- What YOU specifically did — not the team in general
- Technical decisions, design choices, cross-team work, tradeoffs navigated
- Use bullet points if there were multiple distinct actions
- Include the "why" behind key decisions where possible

#### Result
- Quantified outcomes wherever possible (%, time saved, scale, cost, reliability metrics)
- If no numbers are available, describe the qualitative outcome clearly
- Mention timeline if notable ("within 1 month", "over 6 months")

### 4. Tag related skills

Scan the skills directory structure to identify 2–5 relevant skill notes to link under `## Related Skills`. Use wiki links:
```
[[skills/tech/ai-infra/Distributed Training Frameworks]]
[[skills/management/people/Engineering Team Management]]
```

Use this category map to guide tagging:
```
skills/tech/ai-infra/       — GPU, CUDA, training infra, MLOps
skills/tech/ai-basics/      — LLM theory, deep learning
skills/tech/infra/          — K8s, cloud, networking
skills/tech/system-design/  — Distributed systems, design
skills/management/behavior/ — Leadership, conflict, influence
skills/management/people/   — Hiring, team, performance
skills/management/project/  — Roadmap, planning, delivery
```

### 5. Generate Interview Usage

Under `## Interview Usage`, produce:
- **适用 BQ**: 2–4 behavioral question phrasings this story best answers
  - e.g., "Tell me about a time you disagreed with your manager"
  - e.g., "Describe a situation where you had to influence without authority"
- **适用 JD 关键词**: 4–8 JD keywords this story demonstrates

Focus on BQ questions that are commonly asked for senior engineering manager / AI Infra manager roles.

### 6. Write the frontmatter

```yaml
---
title: {Company} - {Short Title}
type: experience
skills: [{comma-separated tag list, no brackets in values}]
company: {Company}
date: {YYYY-MM}
impact: {low | medium | high}
growing_link:
---
```

- `skills`: short tag names (e.g., `distributed-training`, `cross-team-collaboration`) — not wiki paths
- `impact`: judge based on scope and business outcome
  - `high`: org-wide, revenue/reliability impact, or 10+ people affected
  - `medium`: team-level or multi-team, meaningful metric movement
  - `low`: individual or process improvement

### 7. Generate Key Questions

Produce 3–5 interview questions this story is well-suited to answer, with a brief talking-point framework for each (not a full answer — just the structure).

Format:
```
**Q: [Behavioral question]**
Talking points: [2–3 key beats to hit in the answer]
```

Prioritize questions that:
- Test conflict resolution, cross-team influence, or technical judgment
- Are commonly asked for senior EM / AI Infra manager roles
- Map directly to a concrete moment in this story

### 8. Write the Summary

Write 1–2 paragraphs that:
- Summarize what happened and why it was significant
- Call out the key judgment call or leadership behavior demonstrated
- Are readable as a standalone refresher before an interview

### 9. Write the experience note

Create the file at the determined path using the full structure:

```
---
[frontmatter]
---

# {Title}

## Situation
...

## Task
...

## Action
...

## Result
...

## Related Skills
...

## Interview Usage
- 适用 BQ：...
- 适用 JD 关键词：...

## Key Questions
...

## Summary
...

## Raw Material
- [[raw_material/experience/{source filename}]]
```

### 10. Mark raw material as processed

Add a `processed: true` field to the raw material note's frontmatter (add it if missing).
Add an `experience_note` field pointing to the created file:
```yaml
processed: true
experience_note: "[[experience/{filename}]]"
```

## Output

Summary to user:
- Experience note created: `experience/{filename}.md`
- Impact: {impact level}
- Skills tagged: {list}
- BQ mappings: {count}
- Raw material marked processed
