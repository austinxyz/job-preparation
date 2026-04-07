---
name: mock-interview
description: Use when the user wants to practice for a specific interview — technical, behavioral, or system design — based on a target JD or skill area.
---

# mock-interview

Run a structured mock interview session as a realistic interviewer, then deliver focused feedback.

## Inputs

- **Mode** (required): `technical` | `behavioral` | `system-design`
- **JD note** (optional): path to a `positions/` note — sets company context and role expectations
- **Skill focus** (optional): specific skill(s) to target (e.g. "GPU Cluster Management", "team building")
- **Difficulty** (optional): `mid` | `senior` | `staff` — defaults to `senior`

If the user doesn't specify, ask for mode first, then optionally a JD or skill area.

## Interview Flow

### Setup

Read the JD note if provided. Extract:
- Company name and role title (for persona framing)
- Key technical requirements (for question selection)
- Leadership scope (for behavioral calibration)

Open with: **"I'm [Name] from [Company], a [role] on the team. Let's start. [First question]"**
Keep the persona consistent throughout. Don't break character during the interview.

### Questioning rules

- Ask **one question at a time**. Wait for the full answer before continuing.
- After each answer: probe once if the answer is shallow or misses a key dimension.
  - "Can you go deeper on [specific part]?"
  - "What would you do differently if [constraint changed]?"
  - "How did you measure success there?"
- Don't correct or hint during the interview. Stay in interviewer mode.
- Run **4–6 questions** unless the user says stop.

### Question selection by mode

**technical** — Pick from the target skill's Key Questions in `skills/`. If no skill note exists, generate questions covering: core concept, trade-offs, failure modes, scaling implications.

**behavioral** — STAR-format questions calibrated to the JD's leadership scope:
- Team building / hiring
- Cross-functional conflict or alignment
- Technical decision under ambiguity
- Failure / post-mortem
- Prioritization under constraints

**system-design** — Open-ended design prompt relevant to the role:
- State the problem and scale constraints up front
- Ask the candidate to drive: clarify requirements → high-level design → deep dive → trade-offs
- Probe bottlenecks, failure modes, and scaling choices

### Closing

After the last question, say: **"That's all I have. Thanks for your time — I'll share some thoughts now."**

Then switch out of character and deliver feedback (see below).

## Feedback Format

Deliver feedback in three parts:

**Strengths** (2–3 bullets)
What landed well — specific, not generic. Reference actual things the user said.

**Gaps** (2–3 bullets)
What was missing, shallow, or off-topic. Be direct. Each gap should name the specific dimension missed (e.g. "didn't address failure recovery", "answer lacked quantified impact").

**English expression** (2–3 suggestions)
Where phrasing was awkward or imprecise. Offer a more natural/professional alternative.
Format: ~~what was said~~ → suggested phrasing

## Example opener (behavioral, senior EM, Perplexity)

> "I'm Jordan, an engineering director at Perplexity. We're hiring a TLM for our Agents team, so I want to understand your leadership style.
>
> Tell me about a time you had to build a team quickly under significant time pressure. Walk me through what you did."

## After the session

Ask: "Want to retry any question, or move on to the next topic?"
This lets the user drill a weak area immediately.
