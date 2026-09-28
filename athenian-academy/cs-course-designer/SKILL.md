---
name: cs-course-designer
description: Research, plan, and write course/unit outlines, Course Learning Outcomes (CLOs), lesson/teaching plans, and assessments (quizzes, exams, rubrics, project briefs) for general Computer Science, Database Management (DBMS), SQL, Python, and C programming. Also use to review or critique existing CLOs, lesson plans, or assessments for alignment. Adapts to the stated audience level (university, bootcamp, high school, professional training) and scales to request size — a single CLO gets a direct answer, a full course gets the full workflow. Trigger whenever the user asks to design a course, syllabus, curriculum, unit, or lesson plan for CS/DBMS/SQL/Python/C, wants learning outcomes written/reviewed/checked, needs a teaching plan or lab plan, or wants quizzes/exams/rubrics created or aligned to outcomes — even without the words "CLO" or "syllabus." Not for other languages (Java, JavaScript, ML frameworks, etc.) or for live one-on-one tutoring of a specific student in the moment.
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "1.0.0"
  source: CS curriculum & outcome-based education practice (compiled 2026)
---

# CS Course Designer

## Scope — read this before anything else

This skill covers **curriculum design artifacts** — CLOs, syllabi, lesson/teaching plans, and assessments — for **general CS, Database Management, SQL, Python, and C** specifically. Two boundaries matter enough to state explicitly:

- **Subject boundary.** If the request is about a different language or domain (Java, JavaScript/web frameworks, machine learning, mobile dev, etc.), the reference files here (topic sequencing, misconceptions) don't apply and will actively mislead if forced onto the wrong subject. Help with the request using general pedagogical judgment instead of pretending one of the five reference files fits — don't stretch, say, the Python file over a JavaScript request just because both are "programming."
- **Design vs. delivery boundary.** This skill is for building the *artifacts* of a course (the plan, the outcomes, the assessment). If someone wants live, adaptive, one-on-one tutoring of a specific student right now ("explain recursion to me," "help me debug this"), that's a direct-help task — just teach them. Don't wrap a real-time tutoring interaction in CLOs, rubrics, or alignment tables; that apparatus is for people designing a course, not for the student receiving it in the moment.

## Overview

This skill turns a course or topic request into an outcome-aligned teaching package, scaled to how big the request actually is. The throughline is **alignment**: everything downstream should trace back to something upstream.

```
Understand the task  →  Research the subject  →  Plan the structure  →  Write CLOs  →  Write lesson/teaching plans  →  Design assessments
   (what's actually        scope                    (sequence, timing)    (Bloom's verbs,      (each plan maps          (each assessment
    being asked for,   (what's normally taught,                           observable &          to one or more CLOs)     maps back to a CLO)
    at what scale)      in what order — one                                measurable)
                         defensible ordering,
                         not the only one)
```

A plan where the assessments don't test what the CLOs promised, or lessons that wander away from the stated outcomes, is the most common failure mode in real syllabi — the value this skill adds is keeping that chain intact, not just generating text that sounds like a syllabus. But that chain is only worth building when the request calls for it — see proportionality below.

## Step 0: Understand the task before building anything

This is the step most likely to be skipped under time pressure, and skipping it is what causes wasted, misdirected output. Work out four things before touching Step 1:

**A. What kind of task is this?**
- **Generate something new** (a CLO, a course, a lesson, an assessment) → proceed through the steps below.
- **Review or critique existing material** (a CLO, lesson plan, or assessment the user already has) → skip to Step 6 (Reviewing existing material) instead of generating from scratch.
- **A quick, single-item question** ("write one CLO for teaching while-loops," "give me three quiz questions on joins") → answer it directly, informed by the relevant reference file, without running the full six-step pipeline. Scale the effort to the size of the ask — a one-line request doesn't need a syllabus-grade apparatus wrapped around it.
- **Live tutoring of a specific student in the moment** → this skill doesn't apply; see Scope above and just help directly.

**B. What's the actual scope of the deliverable?**
- **Subject & specific topics** — "SQL joins and subqueries" is a different job than "a full semester DBMS course."
- **Audience level & prior knowledge** — university, bootcamp, high school, or professional/corporate training; beginner, intermediate, or advanced.
- **Duration & structure** — a single lesson? a 12-week course? a 3-day workshop? a self-paced module?
- **Delivery format** — lecture, hands-on lab, self-paced/async, hybrid.
- **What deliverables are actually wanted** — just CLOs? a full syllabus? lesson plans? assessments? all of it?
- **Is there a framework this needs to satisfy?** — mentions of ABET, accreditation, "program learning outcomes" / PLOs, or a named certification (e.g., a vendor cert exam) signal that plain Bloom's-style CLOs alone won't be enough. If so, look up that specific framework's outcome/mapping requirements (web search) rather than defaulting to the generic Bloom's CLOs this skill produces by default, and say plainly if PLO-level mapping is likely needed but wasn't part of the request — don't just silently produce course-level CLOs and imply that's the whole job.
- **Is there a specific dialect/version this needs to match?** — SQL behavior (e.g., NULL sorting, window function syntax, `LIMIT` vs `TOP`) varies by engine; Python and C behavior varies by version/standard. If the request names one (Postgres, Python 3.12, C11, etc.), use it. If not, state the one you're assuming (a reasonable default: current mainstream Postgres for SQL, current stable Python 3.x, C11/C17 for C) rather than writing examples that silently assume a dialect the user may not be using.

Most real requests already answer most of B ("write CLOs for an intro Python course for high schoolers, 10 weeks, one 90-minute session a week"). When that's true, proceed directly. Ask a clarifying question only when a genuinely missing piece would send the whole plan in the wrong direction. Otherwise, pick the most reasonable default and **state it plainly, up front, not buried in paragraph three** — the goal is that a reader who disagrees with the assumption catches it immediately, not after reading past it into content built on top of it.

**C. For large, multi-deliverable requests, checkpoint before going deep.** If the ask spans a full course *and* multiple lesson plans *and* assessments in one go, generating all of it at full depth in a single pass risks building a lot of content on one unverified assumption, and risks the later lesson plans getting shallow as length grows. In that case: produce the outline/skeleton and CLOs first (Steps 1–3), show the scope assumptions clearly, and check whether that's on track before writing out every individual lesson plan and assessment — this is exactly the situation where a quick check saves real rework, versus the ordinary case where asking would just add friction.

## Step 1: Research the subject scope

Ground the plan in what's actually taught, and in what order, so the sequencing and depth feel like a real curriculum rather than an improvised list.

- Read the matching subject reference file before drafting content for that subject:
  - [computer-science](references/computer-science.md) — general CS1/CS2 fundamentals, algorithms, data structures
  - [database-management](references/database-management.md) — ER modeling, normalization, transactions, indexing, NoSQL overview
  - [sql](references/sql.md) — querying, joins, subqueries, window functions, query performance
  - [python](references/python.md) — syntax through OOP, error handling, common libraries, testing/debugging
  - [c-programming](references/c-programming.md) — pointers, memory management, structs, low-level concepts

  These give topic coverage, one reasonable sequencing, and the misconceptions students at each stage predictably run into. Treat the sequencing as **a** defensible order, not **the** order — institutions and instructors reasonably disagree (e.g., objects-first vs. objects-later, spiral vs. linear curricula). If the user's request implies a different philosophy or a specific textbook/institution's order, follow that instead and don't silently override it with the reference file's default.

- **Combining subjects.** Requests spanning more than one file (e.g., "a DBMS course that includes a SQL unit," "a Python course that also covers basic data structures") should draw on more than one reference file — but merge them by genuine topic dependency, not by concatenating each file's sequence end to end. Watch for content that legitimately overlaps (e.g., recursion or Big-O might matter to both a general-CS unit and a Python unit in the same course) and teach it once, in the place it's first needed, rather than repeating or contradicting it across units.

- If the request is anchored to something specific and current — a named textbook's chapter order, a particular institution's syllabus, a certification's exam blueprint, current industry practice for a topic — use web search rather than relying on the reference files alone. The reference files are a solid generic scaffold, not a substitute for checking the specifics the user actually cares about.

## Step 2: Plan the structure

Turn the topic scope into a sequence before writing anything else:

- Break the total duration into units, weeks, or sessions.
- Order topics by genuine dependency, not by convenience — you can't teach joins before `SELECT`, or pointers before variables and the memory model, or recursion before functions.
- Decide where labs/practice sit relative to lecture content (immediately after the concept, or batched at the end of a unit).
- Flag natural checkpoints for formative assessment — the end of a dependency chain is usually a good place to check whether it landed before building further on top of it.

Present this as a simple outline (unit/week → topics → format) before going deeper — it's the skeleton everything else hangs on, and it's cheap to adjust here versus after full lesson plans are written. For large requests, this is the checkpoint referenced in Step 0C.

## Step 3: Write the CLOs

Read [clo-writing](references/clo-writing.md) before drafting — it has the full Bloom's Taxonomy verb bank, quality criteria, and worked examples per subject. The condensed version:

- A CLO is a statement of what the student will be able to **do**, using an observable, measurable verb — not "understand" or "know," which can't be assessed directly.
- Match the verb to the actual cognitive demand of the course, not the highest-sounding one. An intro session on SQL `SELECT` syntax lives at *Apply* ("write basic SELECT queries with WHERE and ORDER BY"), not *Evaluate*. A capstone project genuinely reaches *Create*.
- A course generally needs a small number of CLOs (roughly 4–8) that summarize the whole arc, not one CLO per topic.
- If Step 0 flagged an accreditation/certification framework, write the CLOs to satisfy that framework's structure (and note the mapping to it explicitly) rather than only the generic Bloom's pattern below.

| Bloom's level | Signal verbs | Typical fit |
|---|---|---|
| Remember | define, list, identify, recall | terminology, syntax names |
| Understand | explain, describe, summarize, classify | how a mechanism works |
| Apply | write, implement, execute, use, solve | writing code/queries to spec |
| Analyze | debug, compare, trace, decompose | tracing execution, finding bugs, comparing approaches |
| Evaluate | assess, critique, justify, optimize | choosing between designs, judging tradeoffs |
| Create | design, build, develop, construct | original programs, schemas, systems |

Example CLO: *"Write SQL queries using inner and outer joins to retrieve data from three or more related tables."* (Apply — observable, testable with a query the student writes.)

## Step 4: Write the teaching/lesson plan(s)

Use this template per session; adjust section weight for lab-heavy vs. lecture-heavy formats. Every plan should visibly point back to the CLO(s) it serves, and should state the dialect/version assumption if the session involves code or queries.

```markdown
# [Session/Unit Title]
**Maps to CLO(s):** [reference the specific CLO number(s)]
**Level:** [audience level]   **Duration:** [minutes]   **Format:** [lecture/lab/hybrid]
**Assumes:** [SQL dialect / language version, if this session involves code or queries]

## Objectives (session-level, narrower than the course CLOs)
- ...

## Prior knowledge assumed
- ...

## Materials / setup
- ...

## Warm-up / hook (5–10 min)
Brief activity or question that activates prior knowledge or motivates the topic.

## Direct instruction (time)
Core concept delivery — note key explanations, diagrams, or worked examples to use.

## Guided practice (time)
Students try it with support — pair up, live-coding along, worked problem walked through together.

## Independent practice / lab (time)
Students apply it alone — the actual task, with a clear "done" criterion.

## Formative check
A quick, low-stakes way to see who got it before moving on (poll, exit ticket, quick problem).

## Wrap-up & bridge to next session
What was learned, and how it connects to what's coming next.

## Common misconceptions to watch for
Pull from the matching subject reference file — anticipating these live is what separates a plan from a slide deck.
```

## Step 5: Design assessments aligned to CLOs

Read [assessment-design](references/assessment-design.md) before drafting — it covers formative vs. summative choices, matching assessment type to Bloom's level, rubric construction, and subject-specific question-bank notes. State the dialect/version any code or query questions assume, for the same reason as Step 4 — an assessment item is worse than useless if it's graded against behavior the student's actual environment doesn't produce.

Build a small mapping table alongside any assessment so the alignment is checkable at a glance:

| CLO | Assessed by | Weight |
|---|---|---|
| CLO1: ... | Quiz 2, Q3–5 | 10% |
| CLO3: ... | Midterm project | 25% |

A CLO with nothing in the "assessed by" column, or an assessment item that doesn't map to any CLO, is a sign to go back and fix the alignment rather than ship it as-is.

## Step 6: Reviewing existing material

Not every request is "build this from scratch" — reviewing or critiquing something the user already has is just as common, and deserves its own pass rather than being force-fit into the generation steps above.

- **Reviewing CLOs**: run each one through the checklist in [clo-writing](references/clo-writing.md) (observable verb, right level, assessable, properly scoped) and name specifically which criterion it fails — not just a silent rewrite.
- **Reviewing a lesson/teaching plan**: check that it states which CLO(s) it maps to (or, if not stated, work out what it's actually teaching and whether that traces to a real CLO); check that the misconceptions for that topic (per the relevant subject reference file) are addressed somewhere in the plan, not just the "happy path"; check that the timing is realistic for the activities listed.
- **Reviewing an assessment or rubric**: build the CLO-to-assessment mapping table from Step 5 against what's actually there — flag any CLO with no coverage, any item that doesn't map to a CLO, and any Bloom's-level mismatch (e.g., a Create-level CLO assessed only by multiple choice).

In every case, report findings as specific, cited gaps ("CLO 3 uses 'understand,' which isn't observable — consider 'explain' or 'trace'") rather than a vague quality judgment — that's what makes the review actually actionable for someone who has to revise the material or defend it to a colleague or accreditor.

## Step 7: Deliver the output

Default to structured Markdown in the conversation (or as a Markdown artifact for anything long enough to be a standalone document). If the user wants a document meant to be handed out, printed, or submitted — a formal syllabus, a printable lesson plan, an exam paper — check `/mnt/skills/public/docx/SKILL.md` or `/mnt/skills/public/pdf/SKILL.md` and produce an actual file rather than only showing the content inline.

## Quick-reference: what to open when

| Need | File |
|---|---|
| Full Bloom's verb bank, CLO quality checklist, worked examples | [clo-writing](references/clo-writing.md) |
| Formative/summative choices, rubric design, question types by Bloom's level | [assessment-design](references/assessment-design.md) |
| General CS (CS1/CS2, algorithms, data structures, OOP) topic map & misconceptions | [computer-science](references/computer-science.md) |
| Database Management topic map & misconceptions | [database-management](references/database-management.md) |
| SQL topic map & misconceptions | [sql](references/sql.md) |
| Python topic map & misconceptions | [python](references/python.md) |
| C programming topic map & misconceptions | [c-programming](references/c-programming.md) |

Only read the reference files relevant to the current request — no need to load all five subject files for a request about one of them.