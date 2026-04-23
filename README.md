# Infra Manager — Interview Prep Knowledge Base

An Obsidian vault + Claude Code workspace for structured interview preparation targeting Infrastructure Manager roles. Knowledge is distilled from books, articles, and personal experience into interview-ready skill notes and STAR stories.

---

## Prerequisites

- [Obsidian](https://obsidian.md/) (free)
- [Claude Code](https://claude.ai/code) CLI

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/austinxyz/job-preparation.git job-preparation
cd job-preparation
```

### 2. Open in Obsidian

1. Open Obsidian → **Open folder as vault** → select the `job-preparation` directory
2. Obsidian will prompt to trust the vault — click **Trust and enable all plugins**
3. Install required community plugins (one-time):
   - Open **Settings → Community plugins → Browse**
   - Install and enable **Dataview**
   - Install and enable **Templater**
4. Open `_meta/index.md` as your dashboard — Dataview tables will auto-populate

> The `.obsidian/` config (appearance, graph, plugin settings) is committed, so the vault should look right immediately after enabling plugins.

### 3. Set up Claude Code

```bash
# From the project root
claude
```

Claude Code reads `CLAUDE.md` automatically — no extra config needed. All custom skills are in `.claude/skills/` and register as slash commands.

**Available slash commands:**

| Command | What it does |
|---------|-------------|
| `/jd-importer` | Normalize a raw JD dropped at `jobs/` root → create `jobs/<Company>/` workspace + dashboard |
| `/jd-analyzer` | Analyze the JD → `jobs/<Company>/jd-analysis.md` with gap table, stub notes, prep checklist |
| `/resume-builder` | Generate a tailored resume from `_meta/resume-base.md` + JD analysis → `jobs/<Company>/resume.md` |
| `/raw-material-processor` | Distill a `raw_material/` note into its linked skill note |
| `/book-reader` | Fetch an online book by TOC URL → raw material notes + skill note |
| `/experience-processor` | Convert a raw experience note into a polished STAR story |
| `/mock-interview` | Run a targeted mock interview session (technical / behavioral / system-design) |
| `/git-commit-push` | Stage all changes, commit, and push to GitHub |

---

## Directory Structure

```
ai-infra-manager/
├── CLAUDE.md                   # Claude Code instructions (auto-loaded)
├── _meta/
│   └── index.md                # Main dashboard (Dataview)
├── _templates/                 # Templater templates for new notes
├── skills/                     # Interview knowledge notes
│   ├── tech/
│   │   ├── ai-infra/           # GPU clusters, training infra, MLOps, agentic frameworks
│   │   ├── ai-basics/          # LLM theory, agents architecture, deep learning
│   │   ├── infra/              # K8s, AWS/GCP/cloud, networking, SRE
│   │   ├── system-design/      # Distributed systems, databases, caching
│   │   ├── algorithms/         # Algorithms, data structures
│   │   └── software-eng/       # Design patterns, Python infra
│   └── management/
│       ├── behavior/           # Behavioral / leadership (STAR)
│       ├── people/             # Hiring, team, performance
│       └── project/            # Roadmap, planning, DORA, Agile
├── experience/                 # STAR-format stories from past roles
├── raw_material/               # Source articles before processing
│   ├── books/                  # Book notes from /book-reader
│   ├── tech/                   # Mirrored structure of skills/tech/
│   └── management/             # Mirrored structure of skills/management/
├── jobs/                       # Per-position workspaces (gitignored) ⚠️ see isolation rules
│   ├── README.md               # Cross-position dashboard
│   ├── <Job Title> - <Company>.md   # Raw JD files at root
│   └── <Company>/              # Per-company workspace
│       ├── README.md           # Status dashboard + interview loop + links
│       ├── jd-analysis.md      # JD analysis (from /jd-analyzer)
│       ├── resume.md           # Tailored resume (from /resume-builder)
│       ├── contacts/           # Recruiter / interviewer prep + raw correspondence
│       ├── prep/               # Round-specific prep docs
│       ├── mocks/              # Mock interview transcripts
│       └── correspondence/     # Email / LinkedIn / Slack history
├── daily/                      # Daily prep notes (gitignored) — private scratch, reflections
├── positions/                  # Legacy JD notes (being superseded by jobs/) (gitignored)
├── resumes/                    # Legacy tailored resumes (gitignored)
├── methodology/                # Prep methodology docs and Feynman technique guide
└── .claude/skills/             # Custom Claude Code slash commands
```

### ⚠️ Per-Position Isolation Rule

Each `jobs/<company>/` is a **physically independent workspace**. Never copy position-specific data (interview loop, interviewer names, schedule, comp numbers) from one company to another. See [CLAUDE.md](CLAUDE.md#per-position-workspace-jobs-rules) for the full rule + anti-patterns.

---

## Preparation Methodology

See **[methodology/README.md](methodology/README.md)** for the full three-phase prep system:

1. **Phase 1 — Build the knowledge base**: Two paths — start from a JD (gap-driven) or start from learning materials (accumulation-driven). Covers the full `stub → draft → in-progress → reviewed` lifecycle with concrete steps for each transition.
2. **Phase 2 — Consolidate**: Feynman technique, Obsidian review, LeetCode/Hello Interview practice, and English fluency drills.
3. **Phase 3 — Sprint for a target JD**: JD analysis → gap-based study plan → resume tailoring → AI mock interview.

---

## Typical Workflow

```
0. Find a JD
   └─ Paste raw text → jobs/<Job Title> - <Company>.md (at jobs/ root)
   └─ Run /jd-importer → creates jobs/<Company>/ workspace + dashboard
   └─ Run /jd-analyzer → jobs/<Company>/jd-analysis.md (gap table, stub notes, prep checklist)
   └─ Run /resume-builder → jobs/<Company>/resume.md (tailored resume)

1. Read a book or article series
   └─ Run /book-reader <TOC URL>
   └─ Creates raw_material/books/<name>/ section files
   └─ Creates or updates skill note directly

2. Process individual articles
   └─ Save article content to raw_material/tech/.../
   └─ Run /raw-material-processor <file>
   └─ Skill note is updated with concepts, Q&As, summary

3. Write experience stories
   └─ Dump raw notes to raw_material/experience/
   └─ Run /experience-processor → polished STAR note in experience/

4. Review & prioritize
   └─ Open _meta/index.md → Dataview tables show status by priority
   └─ Focus on high-priority notes not yet "in-progress"

5. As interviews get scheduled
   └─ Record contacts/correspondence in jobs/<Company>/contacts/
   └─ Synthesize per-round prep in jobs/<Company>/prep/
   └─ Run /mock-interview → store transcripts in jobs/<Company>/mocks/

6. Before interview
   └─ Re-run /jd-analyzer if JD analysis needs refresh
   └─ Re-run /resume-builder if resume needs tuning
   └─ Run /git-commit-push to save non-job artifacts (skills, experience); jobs/ stays private
```

---

## Note Status Lifecycle

`stub` → `draft` → `in-progress` → `reviewed`

- **stub**: skeleton only, created by jd-analyzer for gap topics
- **draft**: raw-material-processor has run once
- **in-progress**: actively being built out (multiple sources processed)
- **reviewed**: ready for interview use

---

## Note Language Convention

- **English is primary** for all skill notes (interviews are in English)
- Chinese may appear as inline annotations or parenthetical explanations
- `_templates/` files use Templater syntax — do not edit the `<% tp.* %>` placeholders

---

## Privacy

The following directories are gitignored — private job-search strategy and personal notes stay local:

- `jobs/` — per-position workspaces (JDs, analysis, tailored resumes, interviewer contacts, prep docs, mocks, correspondence)
- `daily/` — daily scratch notes, reflections, cross-position musings
- `positions/` and `raw_material/positions/` — legacy JD content
- `resumes/` — legacy tailored resumes
- `methodology/` — private methodology docs
