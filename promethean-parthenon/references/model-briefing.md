# Model briefing — instructing a current Claude model

How to phrase the brief, run a long job and read the result, so the five levers actually reach the model. [output-quality](output-quality.md) says *what* moves quality. This file covers *how to say it* to the model.

**Version:** written against **Claude Opus 5.5** (2026), from Anthropic's guide *Getting the most out of Opus 5.5*. Model behaviour shifts between releases. When a newer model's guide contradicts a row here, the guide wins: update this file, don't argue with the model.

---

## 1. Writing the brief

| Do | BAD | BETTER |
| --- | --- | --- |
| **Delete thinking directives.** The model already reasons before replying. To get more depth, raise the effort level; don't add a phrase. | "Think carefully, step by step, before answering." | *(delete it; set effort `high` on the decision instead)* |
| **State the finish line.** Say what "done" looks like, as something you can observe. | "Clean up the auth module." | "Done when every route under `/api/auth` uses `requireSession` and `npm test` passes." |
| **State the stopping conditions,** meaning when to stop and ask instead of pushing on. | *(nothing, so the model decides alone)* | "Stop and ask before deleting files, changing a migration, or touching anything outside `src/auth`." |
| **Say "answer directly"** when you want a short answer. | "What's the default port?" → three paragraphs | "Answer directly: what's the default port?" |
| **Name what to avoid,** not the vibe you want. This matters most in design. | "Make it look modern and clean." | "No gradient text, no purple-to-blue hero, no three equal feature cards." |

A brief that has a finish line but no stopping condition gives the model two options: guess at the risky moment, or halt at every small choice. Write both.

---

## 2. Running a long job

| Do | Why |
| --- | --- |
| **Put the whole scope in one message:** the task, the finish line and the stopping conditions together. | A job fed in pieces gets planned for the first piece, then re-planned at every later one. |
| **Add follow-ups while the job runs;** don't stop and restart. | A restart throws away context the model already built. A mid-run message goes into the plan in progress. |
| **Fan big audits and migrations out to parallel subagents, then verify.** | Breadth goes parallel. A worker's "done" is a claim until checked. The orchestration side is in the hermes-olympus skill. |
| **Keep a task checklist in version control** that updates as the work runs. | This is lever 3: a checklist on disk survives compaction and the next session. The long-horizon ledger already is one, so reuse it. |

---

## 3. Reading the result

| Ask the model for | So that |
| --- | --- |
| **Blocking items first:** what it needs from you, above the summary | you can unblock it in 10 seconds without reading 60 lines |
| **Status notes attached to actions,** not a separate essay at the end | each claim sits next to the change it describes |
| **Unconfirmed claims marked, with where to check** (`file:line`, URL, command) | "inferred" can be checked instead of trusted. This is the same rule as *measure before you theorize* |
| **A review pass on its own diff before you look** (e.g. a code-review command) | the cheap errors are gone before human attention is spent |

---

## 4. Context to hand over

- **Attach the thing, don't describe it.** The screenshot, the chart, the diagram. A description passes on your reading of it, errors included.
- **Give the whole document when details matter.** Numbers, dates and cross-references are exactly what an excerpt drops.

---

## 5. Rules worth putting in CLAUDE.md

Paste this and adjust the paths:

```markdown
## Working rules
- Keep going without asking on: reading, searching, running tests, edits inside the task's scope.
- Stop and ask before: deleting files, rewriting history, migrations, dependency upgrades,
  anything outward-facing (push, publish, send), or edits outside the task's scope.
- Treat answers already given in this conversation as settled unless I question them.
- Report with the blocking items first, then status notes attached to each action.
- Mark any claim you could not confirm, and say where it can be checked (file:line or URL).
```

**Why "settled":** in a long chat, a model that re-opens decisions it already made looks thorough but is drift. This is the model-side twin of the operating rule *announce a skipped gate once, then comply*.

---

## When not to apply

- **A one-line, fully specified edit.** A stopping-condition list for a typo fix is ceremony.
- **Exploration.** A finish line works against learning what's possible. Time-box the exploration instead.
- **Permission prompts are not a briefing problem.** Keep them on for destructive actions even when the model interrupts less. The brief lowers risk, and the prompt is the backstop.
