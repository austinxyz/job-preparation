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
