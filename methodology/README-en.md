# Interview Preparation Methodology

This system uses an Obsidian knowledge base as its core, combined with AI-assisted tools, to prepare for technical interviews systematically. The preparation is structured in three phases: **Build the Knowledge Base → Reinforce Knowledge → Sprint for the Target JD**.

---

## Phase 1: Build the Knowledge Base

> Goal: Build a personal knowledge base in the style of [Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
> Each skill note should be self-contained — covering core concepts, common interview questions, and personal understanding.

The knowledge base is organized into two categories:

- **Tech**: Algorithms & Data Structures / System Design / Infra / Software Engineering / AI Basics / AI Infra
- **Management**: Behavioral / People Management / Project Management

### Path 1: Start from the JD — discover knowledge gaps

Use this when you're unsure what to study. Work backwards from the JD to identify what you need to know.

```
1. Paste the raw JD into jobs/<Job Title> - <Company>.md (in the jobs/ root)
2. Run /jd-importer → creates jobs/<Company>/ workspace + dashboard
3. Run /jd-analyzer → generates jobs/<Company>/jd-analysis.md, auto-identifies skill gaps, creates stub notes
4. Use the stub list and prep checklist to find corresponding learning materials
5. Save materials to raw_material/tech/ or raw_material/management/
6. Run /raw-material-processor → distills core content into the skill note
```

> **⚠️ Per-Position Isolation Rule:** Each `jobs/<company>/` is a **physically independent workspace**. Never copy interview loop structure, interviewer names, schedule, or comp data from one company to another. See the "Per-Position Workspace Rules" section in [CLAUDE.md](../CLAUDE.md).

### Path 2: Start from materials — proactively accumulate knowledge

Use this when you encounter a good article or video and want to capture it as a reusable note.

```
1. Save the original content/notes to the appropriate subdirectory under raw_material/
2. Fill in the skill_note field in the file frontmatter (pointing to the corresponding skill note)
3. Run /raw-material-processor → distills content and auto-updates the skill note
```

**For online books or article series:** Use `/book-reader` instead of saving manually:

```
1. Find the table-of-contents URL for the book or series
2. Run /book-reader, providing the TOC URL + book slug
   → Auto-fetches all chapters, generates raw_material/books/[slug]/ files by section
   → Auto-matches to existing skill notes (or prompts you to create new ones)
3. Run /raw-material-processor on each section file → fills in the skill note
```

Best for systematically working through technical books (e.g., DDIA, MLSys, GPU Performance), avoiding manual chapter-by-chapter organization.

### Path 3: Start from your own experience — capture STAR stories

Use this when recalling work experiences and distilling behavioral interview material.

```
1. Save the raw story, narrative, or interview transcript to raw_material/experience/
   (any format works: paragraphs, bullet points, Q&A fragments)
2. Run /experience-processor → automatically:
   - Restructures into standard STAR format (Situation / Task / Action / Result)
   - Identifies related skills and adds tags
   - Generates applicable BQ questions + answer frameworks
   - Outputs an interview-ready experience note to experience/
3. Use the generated experience note in /jd-analyzer resume suggestions and /mock-interview behavioral practice
```

### Skill Note Status Lifecycle

```
stub (skeleton only) → draft (has content) → in-progress (actively building) → reviewed (interview-ready)
```

Each status has a clear "definition of done" and corresponding action:

#### stub → draft: fill in core content

1. Based on the stub's `title` and `tags`, find 1–2 high-quality reference articles (recommended: official docs, papers, well-known blogs)
2. Save the original content to the appropriate subdirectory under `raw_material/`, set the `skill_note` field
3. Run `/raw-material-processor` → Claude Code auto-extracts Core Concepts, Key Questions, and Summary; status advances to `draft`

**What Claude Code can do:** Auto-distill structured content from raw materials without manual note-taking; identify related skills in the knowledge graph to extend the Knowledge Map.

#### draft → in-progress: add your own understanding

1. Read through the entire note; verify accuracy and completeness
2. Add personal insights: analogies, pitfalls encountered, connections to other skills
3. Rewrite the answer frameworks in Key Questions in your own words
4. Test yourself using the Feynman Technique (see Phase 2 below)

**What Claude Code can do:**
- Add more high-frequency interview questions (prompt: `"For [Skill], add 5 deep follow-up questions likely asked in a FAANG Senior EM interview"`)
- Check Core Concepts for gaps (prompt: `"Here are my notes on [Skill] — identify any important concepts not covered"`)

#### in-progress → reviewed: validate your ability to articulate

1. Without looking at notes, explain the entire skill from start to finish in English (Feynman method)
2. Use AI to simulate follow-up questions (see Phase 3, Step 4)
3. Once you can fluently answer all Key Questions → manually change `status` to `reviewed`

**What Claude Code can do:** Role-play as the interviewer to probe follow-up questions and expose logical gaps in your explanation; polish English answers and distill more professional technical phrasing.

Use the Dataview tables in `_meta/index.md` to track overall progress and priority at any time.

---

## Phase 2: Reinforce Knowledge

Building the knowledge base is just the first step. Real preparation is about whether you can **articulate it clearly out loud**. Use the following four approaches progressively:

### 1. Review in Obsidian

Open `_meta/index.md` and review by priority using the Dataview tables:
- Start with `high priority + stub/draft` (most in need of content)
- Then revisit `reviewed` notes (maintain familiarity)

Recommended: use Obsidian Graph View to browse the knowledge graph and build an intuitive sense of how concepts connect.

### 2. Feynman Technique

> Core principle: if you can explain it in simple terms, you truly understand it.

Detailed methods and full prompt templates → [[methodology/Feyman.md]]

**Four practice modes (with Claude):**

| Mode | Best for | Description |
|------|----------|-------------|
| Play the 10-year-old | First pass after learning — test if you can explain clearly | Claude plays a zero-background student; you explain; it asks follow-up questions on anything unclear |
| Gap analysis | You think you understand, but can't explain the details | Claude uses progressive questioning to locate your logical gaps |
| Generate analogies | Concept is too abstract or hard to remember | Claude provides real-world analogies + generates 3 progressively harder test questions |
| Socratic dialogue | You want to truly understand the underlying principles | Claude only asks "why" — never gives answers — guiding you to derive conclusions yourself |

**Fastest daily usage:**
> "I want to master [skill name] using the Feynman Technique. Please play a 10-year-old with no background knowledge. I'll explain the concept to you, and after I finish, point out anything I explained unclearly or ask questions you find confusing."

### 3. Practice with Tools

| Tool | Best for | Notes |
|------|----------|-------|
| **LeetCode** | Algorithm problems | Focus on Medium level; emphasize explaining your thought process |
| **Hello Interview** | System design + Behavioral | Has AI interviewer mode with timed practice |
| **Growing** | Schedule management for the above | Use Growing alongside LeetCode / Hello Interview to build a daily practice plan |

Suggested cadence: 3 algorithm problems per day, 2–3 system design problems per week, 2–3 behavioral stories reviewed per week.

### 4. Improve English Expression

Interviews are conducted in English — fluency and professional vocabulary matter equally.

**Daily accumulation:**
- When using raw-material-processor on materials, **pay attention to how the English original phrases things** — especially technical verbs and expressions (e.g., "horizontally partition," "evict stale entries," "back-pressure mechanism")
- Record good phrasings in the Key Questions section of skill notes as part of your answer framework

**Speaking practice (combined with Feynman):**
- Explain the full skill note in English out loud; record and play back
- Focus on: quantified expressions ("reduced latency by 40%"), structured answers (Situation-Task-Action-Result)

**AI-assisted polish:**
> Prompt template:
> "Below is my English explanation of [topic]. Please help me refine it — keep technical accuracy, make the expression more natural, like a Senior Engineer speaking in a FAANG interview. [paste content]"

---

## Phase 3: Sprint for the Target JD

Once you have a target JD, the system provides a complete workflow from analysis to simulation.

### Step 1: Analyze the JD

```
Paste raw JD into jobs/<Job Title> - <Company>.md
    ↓
/jd-importer → creates jobs/<Company>/ workspace + README dashboard
    ↓
/jd-analyzer → generates jobs/<Company>/jd-analysis.md (match score + gap analysis + resume tailoring suggestions)
```

Use `match_score` to decide how much effort to invest:

| Score | Recommendation |
|-------|---------------|
| `strong-matched` | Go directly to resume polish and mock interviews |
| `matched` | Fill in-progress notes; update resume keywords |
| `matched-with-gaps` | Prioritize high-priority stubs; focused 2–3 week study plan |
| `not-matched` | Evaluate whether long-term investment is worthwhile; don't deep-dive yet |

### Step 2: Gap-based Study Plan

The jd-analyzer generates a Prep Checklist. Execute in this order:

1. **stub (highest priority):** find materials → raw-material-processor → draft
2. **draft:** complete Key Questions; walk through with Feynman method
3. **in-progress:** do Hello Interview practice problems
4. **reviewed:** final validation with AI mock interview

### Step 3: Tailored Resume Edits

The Resume Tailoring section of `jobs/<Company>/jd-analysis.md` provides:
- Keyword mapping table (JD term → resume rewrite suggestion)
- Recommended experiences to highlight (prioritized)
- Content to de-emphasize

Fill in your personal instructions in the **"My Comments"** column of the keyword mapping table ("skip this," "keep as-is," specific rewrite phrases), then:

```
jobs/<Company>/jd-analysis.md (with Resume Tailoring analysis) → /resume-builder → jobs/<Company>/resume.md
```

`/resume-builder` will automatically:
- Read `_meta/resume-base.md` as the content foundation
- Read Resume Tailoring instructions from `jobs/<Company>/jd-analysis.md`
- Rewrite each bullet per the keyword mapping table (prioritizing "My Comments")
- Front-load the most JD-relevant skills and experiences
- Output an ATS-optimized markdown resume to `jobs/<Company>/resume.md` (fixed path, overwrites on re-run)

After editing, do a final check with this prompt:
> "Compare this JD and my resume — identify any JD keywords not yet reflected, and where the phrasing could better match the target role's language."

### Step 4: AI Mock Interview

Run `/mock-interview`, which supports three modes:

| Mode | Best for |
|------|----------|
| `technical` | Deep technical Q&A on a specific skill note |
| `behavioral` | STAR-format management experience Q&A |
| `system-design` | Open-ended system design problems, entirely candidate-led |

Optional parameters: specify a `positions/` note (sets company and role context), target skill, difficulty level (mid / senior / staff). After the interview, automatically generates Strengths, Gaps, and English expression feedback.

---

## Reference Reading

- **Karpathy LLM Wiki**: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
  — The primary reference for this project's skill note style; demonstrates how to cover the full LLM stack using a concise wiki format
- **Feynman Technique**: [[methodology/Feyman.md]] — Prompt templates and Claude integration details; original methodology background at [Farnam Street Guide](https://fs.blog/feynman-technique/)
- **Hello Interview**: https://www.hellointerview.com — System design and behavioral question bank with AI interviewer mode
