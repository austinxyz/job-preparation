# book-reader

Fetch an online book or article series from its table-of-contents URL, distill each chapter into structured reading notes, and map content to skill notes in the knowledge base.

## When to Use

When the user provides a URL to an online book's TOC (table of contents) or an article series index and wants to:
- Systematically read and extract key knowledge from all chapters
- Create reusable raw material notes in `raw_material/books/`
- Map book content to existing or new skill notes

## Inputs

- **TOC URL** (required): the book's table of contents or index page
- **Book slug** (required or inferred): short name for file naming, e.g. `gpu-infra`
- **Section filter** (optional): list of sections/chapters to include; defaults to all
- **Target skill notes** (optional): existing skill notes to append to; otherwise create new ones

## Steps

### 1. Fetch the TOC

Use WebFetch on the TOC URL with prompt:
> "Extract the full table of contents: all sections, chapters, and their relative URLs/links. List them in order with href paths."

Parse the output to build:
- Section list (major parts)
- Chapter list per section (title + full URL)

Present the structure to the user and confirm before proceeding. If the book has >30 chapters, ask the user to filter or proceed in batches.

### 2. Fetch chapters in parallel batches

For each section, fetch all chapter URLs in parallel (up to 5 at once):
- WebFetch with prompt: "Extract the full content: main concepts, key technical points, notable quotes, and important conclusions. Be specific and thorough."

Collect results per section. Note any failed/empty fetches.

### 3. Distill per section

For each section, synthesize the fetched chapter content into:

**Key Concepts** (bullet points):
- What does this section teach?
- Critical technical distinctions and mechanisms
- Important numbers, thresholds, or trade-offs
- Common mistakes or gotchas the author highlights
- Notable quotes (with attribution if author is known)

**Interview Relevance**:
- Which concepts map directly to interview topics?
- Which provide depth/differentiation beyond common knowledge?

### 4. Create raw material files

Create one file per **section** in `raw_material/books/[book-slug]/`:

```
raw_material/books/[book-slug]/[section-slug].md
```

File format:
```markdown
---
title: [Book Title] — [Section Title]
source: [section TOC URL or first chapter URL]
date_saved: [today]
processed: false
skill_note: "[[skills/path/to/SkillNote]]"
book: "[Book Title]"
book_url: "[TOC URL]"
chapters_included:
  - "[Chapter 1 title]"
  - "[Chapter 2 title]"
---

# [Section Title]

[Distilled key concepts, organized by chapter if needed]
```

Also create a book index file:
```
raw_material/books/[book-slug]/index.md
```

```markdown
---
title: [Book Title] — Index
book_url: [TOC URL]
date_read: [today]
sections:
  - file: "[section-slug].md"
    skill_note: "[[skills/...]]"
    status: unprocessed
---

# [Book Title]

[1–2 sentence description of the book's scope and value]

## Sections
- [[raw_material/books/[slug]/section1]] → [[skills/...]]
- ...
```

### 5. Map to skill notes

For each section, determine the best skill note target:
- Search existing `skills/` for matching topics (use Glob/Grep)
- If a match exists: note it in the raw material frontmatter AND suggest running `/raw-material-processor` on the section file
- If no match exists: note that a new skill note should be created

### 6. Create or update skill notes (optional, if user asks)

If the user wants to go beyond raw material and directly generate skill notes:
- Create a new skill note using the standard template for each major topic
- Or run the raw-material-processor logic inline for each section file

### 7. Report to user

Summary:
```
Book: [Title]
Chapters fetched: X / Y
Raw material files created:
  - raw_material/books/[slug]/section1.md → [[skills/...]]
  - raw_material/books/[slug]/section2.md → [[skills/...]] (new note needed)
  ...
Next step: run /raw-material-processor on each section file, or ask me to create skill notes directly.
```

## Output Format for Skill Notes (when created directly)

When creating a skill note directly from book content, follow the standard skill note template and populate:
- **Core Concepts**: 8–12 bullets from the book's key ideas
- **Key Questions**: 6–10 interview Q&As, weighted toward depth and trade-off questions
- **Summary**: 3–4 paragraphs synthesizing the book's arc and connecting to adjacent topics
- **Raw Material**: link to the `raw_material/books/[slug]/[section].md` file

## Notes for Claude

- Always fetch chapters in parallel (up to 5 at once) to minimize time
- If a chapter fetch returns minimal content (< 200 words), note it as "sparse" and move on
- Do not wait for all chapters before distilling — process each section as its chapters complete
- Book content is often in a target language; preserve key terms in their original language (Chinese terms may appear with English translations inline)
- The goal is interview-ready notes, not exhaustive summaries — filter for what a senior AI Infra Manager would need to know
