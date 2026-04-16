# experience-processor

Read a raw experience note and distill it into a polished CARL-format experience note, saved to `experience/`.

## When to Use

When the user has saved a rough story, narrative dump, or interview Q&A into `raw_material/experience/` and wants Claude to:
- Restructure the content into CARL format (Context, Actions, Results, Learnings)
- Map the story to Signal Areas
- Assign Core or Additional type
- Generate Key Questions with talking-point frameworks
- Write a Summary for quick pre-interview review
- Link back to the raw material source
- Produce a polished, interview-ready experience note

## Inputs

- **Raw material path** (required): path to the note under `raw_material/experience/`

---

## Core Principles (read before writing anything)

### CARL, not STAR

All experience notes use CARL structure:
- **Context** — replaces Situation + Task. Sets the stage AND establishes the specific accountability/decision the user owned. No artificial separation.
- **Actions** — what the user specifically did. Must be accurate to their actual role (see Don't Lie).
- **Results** — quantified outcomes wherever possible. Include timeline if notable.
- **Learnings** — specific, honest reflection. What would you do differently? What did this reveal? Not generic lessons.

### Don't Lie

This is the most important constraint. Before writing any action:
- Attribute team work to the team, not to the user personally.
- Distinguish between "I designed/built" (personal) vs. "I led the team to build" (directed) vs. "I supported" (enabled).
- Do not claim credit for frameworks, methodologies, or systems invented by other teams — acknowledge adoption and the judgment call to apply them.
- Do not overstate the user's role in large cross-functional programs — scope claims to the specific workstream or contribution owned.
- After writing, flag specific claims for user verification: "Did you personally do X, or did the team?"

Common patterns and how to attribute them correctly:

| What happened | Correct framing |
|---|---|
| User personally built something | "I built..." |
| Team built under user's direction | "I led the team to build..." |
| User supported a team lead's initiative | "I supported / provided resources for..." |
| User adopted another team's framework | "I adopted [X]'s framework and applied it to..." |
| Working group reached consensus on user's proposal | "I developed a proposal; the working group reached consensus on..." |
| User participated in a cross-functional program | "As [team]'s representative in the broader program, I..." |

### Senior Staff / Principal framing

Write from the perspective of someone operating at org-wide impact, not individual execution:
- Emphasize mental model shifts, philosophy changes, and judgment calls — not just what was delivered.
- Show influence without authority: cross-team alignment, persuasion, building shared contracts.
- Show outcomes that outlast the individual: tools adopted by other teams, practices that continued after the user moved on, playbooks that reduced future cycle time.
- Use the word "I" for decisions and judgment; use "team" or "we" for execution.

### Signal Areas

Every story maps to one or more of these 8 areas. Assign Primary (what the story is most about) and Secondary (additional signal available for follow-up):

| Signal Area | What it demonstrates |
|---|---|
| **Scope** | Scale of impact — team size, user/system count, org-wide reach, multi-year investment |
| **Ownership** | End-to-end accountability; identified the problem and drove the outcome without being asked |
| **Ambiguity** | Made sound decisions with incomplete information; created forcing functions to resolve unclear requirements |
| **Perseverance** | Sustained execution through obstacles, changing requirements, or sustained pressure over months |
| **Conflict Resolution** | Resolved genuine disagreements between peers, leads, or with manager; created conditions for consensus |
| **Communication** | Stakeholder management, transparent documentation, shared vocabulary that aligned teams |
| **Growth** | Personal or team capability shift; chose discomfort as the learning mechanism; adopted new mental models |
| **Leadership** | Changed how a team operated; built capability in others; influenced culture or practice beyond immediate team |

---

## Steps

### 1. Read the raw material

Read the full content of the raw material note. It may contain freeform narrative, bullet points, Q&A transcripts, or fragments.

Extract or infer:
- **Company** name
- **Approximate date** (YYYY-MM)
- **Story title** (use filename if not clear)
- **Core challenge** — technical, organizational, or people

### 2. Determine output path and type

**Filename format:** `{Company} - {Short Title}.md`
- e.g., `eBay - Resolving L7 Traffic Gap.md`

Check if a note already exists at that path. If so, ask the user before overwriting.

**Assign type** — ask the user if unclear:
- `Core`: highest-impact, most versatile stories (typically 3–5 total; the ones used in every interview)
- `Additional`: fills specific signal area gaps; used when a question calls for it specifically

### 3. Distill into CARL format

Write four sections. Be concise and specific — no filler phrases like "I took the initiative to" or "leveraged synergies."

#### Context
- Company, team, the problem or gap
- Why it mattered — stakes, scale, business impact
- The specific accountability or decision the user owned
- 3–5 sentences; do NOT separate into "Situation" + "Task"

#### Actions
- Bullet points, one action per bullet
- Lead each bullet with a verb: "I designed...", "I directed the team to...", "I partnered with...", "I established..."
- For multi-part stories, group actions under bold subheadings
- Include the *why* behind key decisions: "I chose X rather than Y because..."
- Apply the Don't Lie attribution rules throughout

#### Results
- Quantified outcomes with units (%, time, count, scale)
- Timeline where notable ("within 3 months", "over 6 months")
- Outcomes that outlasted the immediate delivery (adopted by other teams, reduced future cycle time, etc.)

#### Learnings
- 2–4 specific, honest reflections — not generic wisdom
- Format: "I should have...", "X was the right call because...", "The thing I'd do differently..."
- Include at least one thing the user would change or do earlier
- Avoid lessons that are obviously true ("communication is important")

### 4. Assign Signal Areas

Based on the CARL content, assign:
- **Primary**: 1–2 signal areas the story most directly demonstrates
- **Secondary**: 1–2 additional signal areas available for follow-up questions

Write these as a `## Signal Areas` section:
```markdown
**Primary:** Ownership (...brief rationale...), Leadership (...brief rationale...)

**Secondary:** Scope (...), Communication (...)
```

Update the frontmatter `signal_areas` field to match.

### 5. Tag related skills

Scan the skills directory structure to identify 2–5 relevant skill notes. Use wiki links:
```
[[skills/tech/infra/Kubernetes]]
[[skills/management/people/Engineering Team Management]]
```

Category map:
```
skills/tech/ai-infra/       — GPU, CUDA, training infra, MLOps
skills/tech/ai-basics/      — LLM theory, deep learning
skills/tech/infra/          — K8s, cloud, networking
skills/tech/system-design/  — Distributed systems, design
skills/management/behavior/ — Leadership, conflict, influence
skills/management/people/   — Hiring, team, performance
skills/management/project/  — Roadmap, planning, delivery
```

### 6. Write Interview Usage

Under `## Interview Usage`, produce:
- **适用 BQ**: 3–5 behavioral question phrasings this story best answers
- **适用 JD 关键词**: 4–8 JD keywords this story demonstrates

Focus on BQ questions commonly asked for Senior EM / AI Infra Manager roles. Use the Signal Areas to guide which question types to include.

### 7. Write Key Questions

Produce 3–5 interview questions with talking-point frameworks (not full answers — just the structure).

Format:
```
**Q: [Behavioral question]**
Talking points: [2–3 key beats to hit — what to name, what to show, what outcome to land on]
```

Prioritize questions that:
- Map directly to a concrete moment in this story
- Test judgment, conflict, cross-team influence, or scale
- Correspond to the assigned Primary signal areas

### 8. Write the frontmatter

```yaml
---
title: {Company} - {Short Title}
type: {Core | Additional}
signal_areas: [{list of assigned signal areas}]
skills: [{comma-separated tag list}]
company: {Company}
date: {YYYY-MM}
impact: {low | medium | high}
growing_link:
---
```

Impact guide:
- `high`: org-wide, revenue/reliability impact, or 10+ people affected
- `medium`: team-level or multi-team, meaningful metric movement
- `low`: individual or process improvement

### 9. Write the Summary

Write 2 paragraphs:
- **Paragraph 1**: What happened and why it was significant. Name the scale, the stakes, the outcome.
- **Paragraph 2**: The key judgment call or leadership behavior demonstrated. What made this hard and how did you navigate it? What would a less experienced manager have done instead?

Readable as a standalone pre-interview refresher — assume the reader won't go back to the full note.

### 10. Assemble the full experience note

```markdown
---
[frontmatter]
---

# {Title}

## Context
...

## Actions
...

## Results
...

## Learnings
...

## Signal Areas
**Primary:** ...
**Secondary:** ...

## Related Skills
- [[skills/...]]

## Interview Usage
- 适用 BQ：...
- 适用 JD 关键词：...

## Key Questions

**Q: ...**
Talking points: ...

## Summary
...

## Raw Material
- [[raw_material/experience/{source filename}]]
```

### 11. Flag accuracy claims for user verification

After writing, explicitly list 3–5 specific claims for the user to verify before accepting the note:

```
Accuracy checks before you confirm:
1. "[Specific action claim]" — did you personally do this, or did the team?
2. "[Specific metric]" — accurate number/timeline?
3. "[Attribution]" — is this correctly attributed?
```

Focus on: personal vs. team actions, exact metrics, role scope in large programs, and attribution of ideas/frameworks to originating teams.

### 12. Mark raw material as processed

Add to the raw material note's frontmatter:
```yaml
processed: true
experience_note: "[[experience/{filename}]]"
```

---

## Output

Summary to user:
- Experience note created: `experience/{filename}.md`
- Type: Core or Additional
- Signal areas assigned: Primary + Secondary
- Impact: {level}
- Skills tagged: {list}
- BQ mappings: {count}
- Accuracy checks: {list of claims to verify}
