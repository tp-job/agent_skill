---
name: skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy. Also for laying out a skill folder — SKILL.md, references/, scripts/, assets/ — and organising a library of agent skills. Not for writing application code or product documentation.
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "1.3.0"
  source: Claude Code Skill Creator pattern (compiled 2026)
---

# Skill Creator

Creates new skills and improves existing ones through a measured loop: capture intent → draft → test cases → baseline → change one rule → grade → show the user the diff. Find where the user is in that loop and start there. A user with a draft goes straight to testing; a user who says "skip the evals, just write it" gets a draft without them.

Every draft and review is held to [authoring-standard](references/authoring-standard.md): hard limits, description rules, what belongs in the body, and the review checklist.

Match vocabulary to the user. "Evaluation" and "benchmark" are usually fine; explain "JSON", "assertion" or "frontmatter" in a few words unless the user has shown they know them.

---

## Creating a skill

### 1. Capture intent

If the conversation already contains the workflow ("turn this into a skill"), extract it first: tools used, step order, corrections the user made, input and output formats. Then confirm the gaps with the user:

1. What should the skill let Claude do?
2. When should it trigger: which phrases and contexts, and which adjacent requests should it **not** catch?
3. What output format is expected?
4. Does it need test cases? Verifiable outputs (file transforms, extraction, code generation, fixed workflows) do; subjective ones (style, art) often don't. Suggest a default, let the user decide.

### 2. Interview and research

Ask about edge cases, formats, example files, success criteria and dependencies before writing test prompts. If MCP servers or subagents can research docs or similar skills, use them so the user isn't asked what can be looked up.

### 3. Write the draft

```
skill-name/
├── SKILL.md        name + description (frontmatter), then the workflow
├── references/     detail loaded on demand, one concern per file
├── scripts/        deterministic or repeated work, run rather than read
└── assets/         templates, icons, fonts used in output
```

- **description**: what it does, when to use it, literal trigger phrases, and what it is not for, within 1,024 characters. All "when to use" information lives here; the body is invisible until the skill is chosen.
- **body**: the workflow and a fast path to the right reference. Imperative steps; explain *why* a rule matters instead of writing it in capitals.
- **references**: anything a reader needs only sometimes. Link each from `SKILL.md` with when to read it.

Output formats go in as templates; style-dependent output gets input/output example pairs. Patterns for both, and for degrees of freedom, are in [authoring-standard](references/authoring-standard.md).

**No surprises.** A skill's contents must match what its description says it does. Never write a skill that hides malware, exploit code, unauthorized access or data exfiltration. A role-play persona ("act as a senior reviewer") is fine.

Draft, then reread with fresh eyes and cut anything that doesn't change behaviour.

### 4. Write test cases

Write 2–3 realistic prompts, the kind a real user would type, and confirm them with the user. Save them to `evals/evals.json`; add assertions later, while the first runs are in progress.

```json
{
  "skill_name": "example-skill",
  "evals": [
    { "id": 1, "prompt": "User's task prompt", "expected_output": "Description of expected result", "files": [] }
  ]
}
```

Full schema, including `assertions`: [schemas](references/schemas.md).

## Running and evaluating test cases

**This loop needs no tooling beyond what is already available.** No eval runner or packaging script ships with this skill; do not tell anyone to run one.

### Step 1 — Write the cases before you touch the skill

A test case is a **prompt plus the observable thing the revised skill must do**. Write both
halves before editing, for the same reason a feature's verification steps are written before its
code: afterwards, cases get quietly shaped to fit whatever the skill already says.

| Field | Meaning |
| --- | --- |
| `prompt` | What the user would actually type, in their own words |
| `context` | The repo or environment state that makes this case interesting |
| `expected` | The **observable** behaviour — a question asked, a file checked, a refusal |
| `failure_mode` | What the skill did *before* the fix, so a regression is recognisable |

The best cases come from real failures. A skill that has been used in anger has a list of them
already: every place it produced something wrong is a case with a known correct answer.

### Step 2 — Establish the baseline honestly

Run each prompt **against the current skill** and write down what happens, before changing
anything. This is the step most often skipped, and without it every later comparison is a guess.

If subagents are available, spawn one per case so each runs without your context — you wrote the
skill, so running it yourself is the weakest possible test. If they are not available, run the
cases yourself but read the skill fresh and follow it literally, including steps you would
normally skip. Note in the results which of the two you did; they are not equally trustworthy.

### Step 3 — Change one thing

Edit the skill, then re-run the cases. **Change one rule per round.** Two edits and a moved
number leave you unable to attribute the difference, which is how skills accumulate rules that
never helped.

### Step 4 — Grade against the case, not against your taste

For each case record `pass` / `fail` / `unclear`, and for a fail, *which sentence in the skill
should have prevented it*. If no sentence exists, that is the edit for the next round. If a
sentence exists and was ignored, the problem is placement or emphasis, not content — a rule
buried in a reference file that the skill never tells you to open has not been stated.

`unclear` is a real result and must not be rounded to `pass`.

### Step 5 — Show the user the diff, not the score

Present before/after **for the cases that changed**, in their own words. A table of numbers
answers "did it move"; the pair of outputs answers "is it better", which is the question.

---

## Improving the skill

**Undertriggering is the common failure, not overtriggering.** A skill that never fires costs
its whole value; one that fires unnecessarily costs a few tokens. When a case fails because the
skill was never consulted, the fix is in the `description`, not the body.

**Rules that fire late are worth more than rules that fire early.** A caution at the end of a
long skill is read after the decision it was meant to inform. Move it to the step it governs.

**Prefer a step over a principle.** "Verification errors get caught by nothing" is true and
changes no behaviour. "Break the assertion, watch it fail, restore it" is the same idea as an
action, and it gets done.

### Description optimization, by hand

1. Write 10–15 queries a user might send: some that **should** trigger the skill, some
   deliberately adjacent that should **not**.
2. For each, judge from the description alone whether it would trigger.
3. Rewrite the description to fix the misses, then re-judge the whole set — including the ones
   that already passed, since a broader description can start catching things it should not.

Keep the trigger vocabulary in the `description`; keep the method in the body. Claude decides
whether to open a skill from the description alone, so a trigger phrase in the body is invisible
at the moment it matters.

**Queries must be substantive.** Claude handles simple one-step requests without consulting any
skill, so "read this file" is a poor test case regardless of how well the description matches.

---

## Packaging

If a `present_files` tool is available, hand the user the skill folder directly. There is no
packaging script in this bundle; do not instruct anyone to run one.

---

## Reference files

- [authoring-standard](references/authoring-standard.md) — limits, description rules and the review checklist every skill is held to
- [schemas](references/schemas.md) — JSON structures for test-case and grading files
- [index](references/index.md) — what else lives in this skill
- [project-problem-solver](references/project-problem-solver.md) — diagnosing a skill that is
  technically correct but not helping
- [agent-skill-structure](references/agent-skill-structure.md) — folder layout and organisation of agent skills
- [agent-skill](references/agent-skill.md) — agent skill anatomy, in depth
