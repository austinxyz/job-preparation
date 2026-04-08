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
| `/jd-analyzer` | Analyze a job description → gap table, stub notes, prep checklist |
| `/jd-importer` | Import raw JD text into a structured `positions/` note |
| `/book-reader` | Fetch an online book by TOC URL → raw material notes + skill note |
| `/raw-material-processor` | Distill a `raw_material/` note into its linked skill note |
| `/experience-processor` | Convert a raw experience note into a polished STAR story |
| `/mock-interview` | Run a targeted mock interview session |
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
│   │   ├── ai-infra/           # GPU, CUDA, training infra, MLOps
│   │   ├── ai-basics/          # LLM theory, deep learning
│   │   ├── infra/              # K8s, cloud, networking
│   │   ├── system-design/      # Distributed systems
│   │   ├── algorithms/         # Algorithms, data structures
│   │   └── software-eng/       # Design patterns
│   └── management/
│       ├── behavior/           # Behavioral / leadership
│       ├── people/             # Hiring, team, performance
│       └── project/            # Roadmap, planning
├── experience/                 # STAR-format stories from past roles
├── raw_material/               # Source articles before processing
│   ├── books/                  # Book notes from /book-reader
│   ├── tech/                   # Mirrored structure of skills/tech/
│   └── management/             # Mirrored structure of skills/management/
├── positions/                  # Job descriptions (gitignored)
└── .claude/skills/             # Custom Claude Code slash commands
```

---

## Typical Workflow

```
0. Find a JD
   └─ Paste raw text → raw_material/positions/
   └─ Run /jd-importer → creates structured positions/ note
   └─ Run /jd-analyzer → gap table, stub notes, prep checklist

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

5. Practice
   └─ Run /mock-interview for a targeted session

6. Before interview
   └─ Re-run /jd-analyzer for resume tailoring suggestions
   └─ Run /git-commit-push to save all progress
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

`positions/` and `raw_material/positions/` are gitignored — job applications stay local.
