# Assessment Design

Reference for [cs-course-designer](../SKILL.md), Step 5. Read before drafting quizzes, exams, rubrics, or project briefs.

---

## The alignment rule

An assessment measures a CLO or it does not belong in the course. Two failure modes, both common:

- **Orphan CLO** — an outcome nothing assesses. It is a promise the course never checks.
- **Orphan item** — a question mapping to no CLO. Usually a question the instructor finds interesting, testing something never taught.

Build the mapping table before writing items, not after:

| CLO | Assessed by | Weight |
| --- | --- | --- |
| CLO1: Write SELECT queries with filtering and aggregation | Quiz 1 Q1–6; Lab 2 | 15% |
| CLO2: Write joins across three or more tables | Quiz 2 Q1–4; Midterm Part B | 25% |
| CLO5: Critique and rewrite a query for performance | Final project, section 3 | 20% |

Gaps in either direction are a signal to fix the design, not to ship it.

---

## Formative vs. summative

| | Formative | Summative |
| --- | --- | --- |
| Purpose | Find out who's lost, while you can still fix it | Certify what was achieved |
| Stakes | Low or zero | Graded |
| Timing | During a topic, at dependency boundaries | End of unit/course |
| Feedback | Immediate, specific, actionable | Often a score |
| Examples | Exit ticket, poll, code-trace warm-up, pair check | Quiz, midterm, project, final |

**Where formative checks belong:** at the end of every dependency chain, before the next topic builds on it. In CS this matters more than in most subjects, because dependencies are hard — a student who never understood pointers cannot learn linked lists, and every subsequent week compounds the deficit. The check exists to catch that in week 4, not week 11.

A good formative check is short (2–5 minutes), targets one specific misconception (see subject reference files), and produces information the instructor acts on immediately.

---

## Matching assessment type to Bloom's level

Mismatch here is the most common design flaw. A multiple-choice test cannot assess *Create*, and a three-week project is an expensive way to assess *Remember*.

| Level | Assessment types that work | Types that don't |
| --- | --- | --- |
| Remember | MCQ, matching, short answer, fill-in | Projects (wasteful) |
| Understand | Explain-in-your-own-words, concept MCQ with plausible distractors, diagram labelling | Code-writing (conflates with Apply) |
| Apply | Write a program/query to spec, lab exercise, code completion | MCQ (can't show working) |
| Analyze | **Code tracing** ("what does this print?"), **debugging** ("find and fix the defect"), compare-two-approaches, read-unfamiliar-code | Recall questions |
| Evaluate | Code review with justification, design critique, "choose between X and Y and defend it," optimization with rationale | Auto-graded anything |
| Create | Open-ended project, original design brief, capstone | Timed exam |

**The two most valuable and most neglected CS item types are code tracing and debugging.** Both sit at Analyze. Students who can write code from a spec but cannot trace or debug have a brittle, pattern-matched competence that collapses on unfamiliar problems. If a course has no tracing and no debugging items, that is the first thing to fix.

---

## Writing good items

### Multiple choice
- Distractors must be **plausible and diagnostic** — each wrong answer should correspond to a specific known misconception, so the response pattern tells you what to reteach. A distractor nobody picks is wasted.
- Avoid "all of the above" / "none of the above" — they reward test-taking strategy over knowledge.
- Keep the stem complete: the student should be able to answer before reading the options.
- Never use MCQ to assess code-writing. It assesses code-*reading*, which is a different (also valuable) skill — assess it deliberately as such.

### Code tracing
- Give short, complete, runnable code. Ask for exact output, or the value of a variable at a marked point.
- Target one mechanism per item: the loop boundary, the aliasing, the base case.
- **State the language version/dialect.** Integer division, string formatting, and evaluation order have all changed across versions; grading against behavior the student's environment doesn't produce is indefensible.

### Debugging
- Seed one specific defect drawn from the misconceptions list in the subject reference file.
- Ask for three things: *what is wrong*, *why it produces the observed symptom*, and *the fix*. Only asking for the fix lets a lucky guess score full marks.
- Provide the symptom (error message, wrong output), not just the code — that's the realistic version of the task.

### Code writing
- State the specification precisely, including edge-case behavior. Ambiguity in the spec becomes unfairness in the grading.
- Give the test cases, or at least their shape. Hidden acceptance criteria assess mind-reading.
- Specify what may be used — standard library only? A particular structure? Otherwise students optimize for the wrong constraints.

### Projects
- Give the brief, the rubric, and a worked example of an adequate submission at the same time. Withholding the rubric does not increase rigor; it increases anxiety and grading disputes.
- Build in a checkpoint at roughly one-third — it catches the misread brief while it is still cheap.
- Assess the *design decisions*, not just working output, if the CLO is at Evaluate or Create. Otherwise you are assessing Apply with extra steps.

---

## Rubrics

A rubric needs criteria that map to CLOs, levels that describe observable differences, and enough specificity that two graders agree.

**Weak rubric row** — unusable, because "good" is not defined:

| Criterion | Excellent | Good | Poor |
| --- | --- | --- | --- |
| Code quality | Very good code | Good code | Bad code |

**Strong rubric row** — each level names what the grader can see:

| Criterion (CLO2) | 4 — Proficient | 3 — Competent | 2 — Developing | 1 — Beginning |
| --- | --- | --- | --- | --- |
| Join correctness | All joins produce correct result sets; join type (inner/left) is correct for each relationship's semantics | Correct results; one join type is defensible but not the best fit | Result set correct for the sample data but a join type would produce wrong rows for unmatched cases | Joins produce incorrect rows, or a cross join was used unintentionally |
| Query readability | Consistent aliasing, formatted, non-obvious logic commented | Consistent aliasing, readable | Inconsistent aliasing or formatting hinders reading | Unformatted single-line query |

Rules of thumb:
- **3–5 criteria.** More becomes unusable in practice; graders collapse them anyway.
- **4 levels.** Three collapses to a middle default; five invites false precision.
- **Describe evidence, not quality adjectives.** "Handles the empty-input case" beats "thorough."
- **Weight by CLO importance**, and make the weights visible to students.
- **Separate correctness from style.** A working ugly program and a beautiful broken one deserve different feedback, not the same middling mark.

---

## Blueprinting an exam

Before writing items, fix the distribution — it prevents the drift toward whatever is easiest to write (which is always recall).

| CLO | Bloom's | Items | Marks | % |
| --- | --- | --- | --- | --- |
| CLO1 | Understand | 5 MCQ | 10 | 20% |
| CLO2 | Apply | 2 code-writing | 15 | 30% |
| CLO3 | Analyze | 3 tracing + 1 debug | 15 | 30% |
| CLO4 | Evaluate | 1 critique | 10 | 20% |

Check the weighting matches what the course actually emphasized. An exam that is 70% recall for a course that spent 70% of its time on labs is measuring the wrong thing, however well-written the items are.

---

## Subject-specific notes

### General CS
Trace-the-recursion and trace-the-loop items are the highest-signal questions available. For Big-O, ask students to *justify* a complexity from the code rather than recall it — recalled complexities are memorized table lookups.

### Database Management
Give a requirements paragraph and ask for the ER diagram (Apply), then give a flawed schema and ask which normal form is violated, with evidence (Evaluate). Normalization is best assessed by having students *find* the anomaly, not recite the definitions.

### SQL
- **Always name the engine and version.** `LIMIT` vs `TOP`, NULL sort order, and window-function syntax differ.
- Provide the schema and sample data with every item. A query question without visible data is a memory test.
- The highest-value items involve NULL semantics and outer joins — that is where confident students are reliably wrong.
- Auto-grading by result-set comparison is efficient but blind to a query that is accidentally right on the sample data. Include at least one item graded on the query text.

### Python
State the Python version. Assess exception handling with a scenario that *should* raise, not just try/except syntax. Mutable-default-argument and list-aliasing items are excellent Analyze questions because the code looks correct.

### C
State the standard (C11/C17). Memory-management items should require identifying *which* error (leak, double free, use-after-free, overflow) — not just "there's a bug." Pointer-arithmetic tracing items should give the sizes explicitly. Avoid grading undefined behavior as if it had a defined answer; if the item's answer is "this is UB," make that the expected answer.

---

## Review checklist

- [ ] Every CLO appears in the mapping table with at least one assessment
- [ ] Every assessment item maps to a CLO
- [ ] Assessment type matches the CLO's Bloom's level
- [ ] Weighting reflects instructional emphasis
- [ ] Formative checks sit at dependency boundaries, not only at the end
- [ ] Dialect/version stated for every code or query item
- [ ] Rubric levels describe observable evidence, not adjectives
- [ ] At least one tracing item and one debugging item exist
- [ ] MCQ distractors correspond to real misconceptions
- [ ] Students see the rubric before they start

---

## Related

- [clo-writing](clo-writing.md) — outcome verbs and Bloom's levels
- Subject misconception lists: [computer-science](computer-science.md) · [database-management](database-management.md) · [sql](sql.md) · [python](python.md) · [c-programming](c-programming.md)
