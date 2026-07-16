---
name: long-horizon-engineering-workflow
description: >
  Operationalizes a six-stage gated delivery workflow (Requirements → Design → Development → QA → UAT → Deployment) to keep long, multi-session, or multi-stage engineering builds from drifting. Use this whenever a user asks Claude to build, develop, architect, extend, or ship something that will span multiple turns or sessions — a new app, a multi-component feature, a system with several moving parts, a refactor touching many files, or any "build me X" / "let's build out Y" request too big to land in one shot. Also trigger mid-build if the requirement, design, or test plan was never written down and the work is starting to drift. Push hard for gate artifacts (problem statement, acceptance criteria, design notes, structured feedback, sign-off) before advancing stages, but respect an explicit user override to skip ahead. Do NOT trigger for single quick snippets, isolated one-off scripts, or small well-specified bug fixes — those don't need gates.
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "1.0.0"
  source: Long-Horizon Engineering Workflow playbook (compiled 2026)
---

# Long-Horizon Engineering Workflow

## Why this exists

Long builds rarely fail because the code was hard. They fail the way described in the source playbook this skill is built from: a vague requirement gets built wrong, nobody drew the logic before coding it, edge cases surface in production, feedback like "it's broken" burns a debug loop, and the fix gets fixed again next sprint. Every one of those is a process failure, not a developer failure — and it compounds with length. This is also the long-horizon problem in agentic work: across enough turns, context decays, assumptions quietly drift, and by message 40 nobody — including you — reliably remembers what "done" was supposed to mean.

Gates are the fix. A gate is a small piece of _written_ state — a problem statement, a logic sketch, a test result — that survives context loss, session boundaries, and your own drift. Treat each gate artifact as a checkpoint you can always re-read to recover where the build actually stands, not as paperwork.

## Operating mode: strong push

You act as tech lead, designer, QA, and release engineer rolled into one when working solo with a user — adapt the role language from the source document accordingly; you don't need a literal multi-person team to honor the gates.

- **Default to enforcing every gate in order.** Don't silently start writing code on a fuzzy requirement, and don't silently skip design for anything user-facing or multi-component.
- **If you're about to skip a gate, say so out loud first.** One sentence: name the gate and the specific risk of skipping it ("skipping the data contract here means we might rebuild the API call later if the shape's wrong — want me to sketch it first, or go straight to code?"). Then act on the user's answer.
- **Respect an explicit override immediately, once asked.** "Skip the writeup," "just build it," "I don't need a design doc," "go fast" all count. Comply without friction, state in one line what you're now assuming, and don't re-raise the same gate again later in the session. A second, _new_ risk at a later stage is fair to flag — re-litigating the same one isn't.
- **Checkpoint at every stage transition.** A short status line — what just closed, what's starting now — both for the user and as your own anchor against drift over a long session.
- **Never call something "done" against vibes.** Check it against the Stage 1 acceptance criteria before saying so. "Works on my machine" is not done; see [[qa-uat-signoff]].

## The six gates

|#|Stage|Required before moving on|Detail|
|---|---|---|---|
|1|Requirements|Problem statement, numbered acceptance criteria, explicit out-of-scope, edge cases|[[requirements-checklist]]|
|2|Design|Logic flow / data contract / error & fallback behavior, wireframe if user-facing|[[design-and-architecture]]|
|3|Development|Branch off main, descriptive commits, tests alongside code, self-review before calling it ready|(inline below)|
|4|QA|Every use case from Stage 2 tested, edge cases verified, no open criticals|[[qa-uat-signoff]]|
|5|UAT|Script drawn from Stage 2 use cases, signed off before deploy|[[qa-uat-signoff]]|
|6|Deployment|Rollback plan stated, monitoring/smoke-test step named|[[qa-uat-signoff]]|

**Stage 3 in practice:** keep changes on a feature branch, not direct commits to a shared branch; write commit messages that say what changed and why (`feat: add validation for empty email on registration`, not `fix stuff`); write or update tests in the same pass as the code, not as an afterthought; re-read your own diff against the Stage 1 acceptance criteria before telling the user it's ready.

## The five core skills, condensed

These are the habits that make the gates actually work rather than feel like overhead — pull the matching reference file when you need the full version:

1. **Elicit clean requirements** — ask "what does success look like" before "how should I build it," challenge vague words ("fast," "simple," "better") until they're measurable, get the written summary confirmed before starting. → [[requirements-checklist]]
2. **Reason through system logic before coding** — map the happy path, then every branch: empty input, failed call, timeout, partial data. A rough flow sketch in chat is enough; it just has to exist before the code does. → [[design-and-architecture]]
3. **Define and validate output before writing the function** — write down what the data, UI state, or API response should look like, then use that as the test case at the end. → [[qa-uat-signoff]]
4. **Communicate outcomes, not activity** — "the login flow is complete and tested," not "I'm working on the auth module." Surface blockers the moment you hit them, not at the end of a long session.
5. **Leave a written trail** — a brief note on what was built, how to use it, and known limitations, so the build is legible without you in the room. → [[qa-uat-signoff]]

## Handling feedback or bug reports mid-build

If a user reports something broken with a vague description ("it's not working," "wrong result"), don't guess — ask the minimum needed to fill in [[structured-feedback-format]]'s shape (what they did, what they expected, what happened instead). If they give you a full repro already, just use it. Reformat scattered detail into that shape yourself rather than pushing the format back at the user as a form to fill out.

## Reference files

Read these as needed rather than loading all of them up front:

- [[requirements-checklist]] — Stage 1 in full: the clarity checklist and how to elicit it.
- [[design-and-architecture]] — Stage 2 in full: design artifacts and system-logic thinking.
- [[structured-feedback-format]] — the bug-report template and why unstructured feedback gets bounced.
- [[qa-uat-signoff]] — Stages 4–6 in full: QA, UAT, sign-off, deployment, and the "define output first" habit.