---
name: cs-course-designer
description: >-
  Writes and reviews course outlines, Course Learning Outcomes (CLOs), lesson and lab plans, and
  assessments (quizzes, exams, rubrics, project briefs) for Computer Science, DBMS, SQL, Python and
  C, at university, bootcamp, high-school or training level. A single CLO gets a direct answer; a
  whole course gets the full workflow. Use when asked to design a course, syllabus, curriculum or
  unit, write or check learning outcomes, or build or align assessments, even without the words
  "CLO" or "syllabus". Not for other languages (Java, JavaScript, ML frameworks), building the
  slides for one lesson, or live one-on-one tutoring.
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "1.2.0"
  source: CS curriculum & outcome-based education practice (compiled 2026)
---

# CS Course Designer

Turns a course or topic request into an outcome-aligned teaching package, scaled to the size of the ask. The throughline is **alignment**: every lesson maps to a CLO, and every CLO is assessed. Assessments that don't test what the CLOs promise are the most common failure in real syllabi.

```
Understand → Research scope → Plan structure → Write CLOs → Lesson plans → Assessments
                                                  │              │               │
                                                  └── each plan maps to a CLO ── each item maps to a CLO
```

## Scope

- **Subjects: general CS, Database Management, SQL, Python, C.** For another language or domain (Java, JavaScript, ML, mobile), help with general pedagogical judgment and don't stretch a reference file over it; the sequencing and misconceptions would mislead.
- **Design, not delivery.** Live tutoring of one student ("explain recursion to me") is direct help. Don't wrap it in CLOs and rubrics.

## Step 0: Understand the task

**A. Which kind of task?**

| Task | Do |
| --- | --- |
| Generate something new (course, CLO, lesson, assessment) | Run the steps below |
| Review existing material | Go to Step 6 |
| One quick item ("one CLO for while-loops", "three quiz questions on joins") | Answer directly from the relevant reference file, no pipeline |
| Live tutoring | Out of scope; just help |

**B. What is the deliverable's scope?** Subject and topics · audience level and prior knowledge · duration (one lesson, 12-week course, 3-day workshop) · format (lecture, lab, async, hybrid) · which deliverables · any framework to satisfy · dialect or version.

- **Framework named** (ABET, accreditation, PLOs, a certification blueprint): look up its mapping requirements instead of defaulting to plain Bloom's CLOs, and say so if PLO mapping is probably needed but wasn't asked for.
- **Dialect/version**: SQL behaviour varies by engine, Python and C by version. Use the one named; otherwise state the assumption (default: PostgreSQL 16, Python 3.12, C17).

Most requests already answer most of B. Ask only when a missing piece would send the whole plan the wrong way; otherwise pick a default and **state it at the top**, where a reader who disagrees will see it.

**C. Large, multi-deliverable requests: checkpoint first.** Produce the outline and CLOs (Steps 1–3) with assumptions visible, and confirm before writing every lesson plan and assessment.

## Step 1: Research the subject scope

Read the matching subject file before drafting:

| Subject | Read |
| --- | --- |
| General CS (CS1/CS2, algorithms, data structures, OOP) | [computer-science](references/computer-science.md) |
| Database Management (ER, normalization, transactions, indexing, NoSQL) | [database-management](references/database-management.md) |
| SQL (queries, joins, subqueries, window functions, performance) | [sql](references/sql.md) |
| Python (syntax through OOP, errors, libraries, testing) | [python](references/python.md) |
| C (pointers, memory, structs, low-level) | [c-programming](references/c-programming.md) |

Each gives topic coverage, **one** defensible sequence, and predictable misconceptions. Follow the user's textbook, institution or philosophy (objects-first vs. objects-later) over the file's default. When a course spans two files, merge by topic dependency and teach shared topics (recursion, Big-O) once, where first needed. For a named textbook, syllabus or exam blueprint, search the web rather than relying on the files.

## Step 2: Plan the structure

Break the duration into units or sessions; order topics by real dependency (`SELECT` before joins, the memory model before pointers); place labs; mark formative checkpoints at the end of each dependency chain. Present it as an outline (unit → topics → format) before going deeper. It is the cheapest place to change course.

## Step 3: Write the CLOs

Read [clo-writing](references/clo-writing.md) for the Bloom's verb bank, quality checklist and worked examples.

- A CLO states what the student can **do**, with an observable verb. Never "understand" or "know".
- Match the verb to the real cognitive demand: intro `SELECT` is *Apply*; a capstone reaches *Create*.
- About 4–8 CLOs per course, covering the arc, not one per topic.
- If Step 0 found a framework, write to its structure and show the mapping.

| BAD | BETTER |
| --- | --- |
| Students will understand SQL joins. | Write SQL queries using inner and outer joins to retrieve data from three or more related tables. *(Apply)* |

## Step 4: Write the lesson plans

Use [lesson-plan template](assets/lesson-plan.template.md) per session, weighted for lab- or lecture-heavy formats. Every plan names the CLO(s) it serves, states the dialect/version for code, and lists the topic's misconceptions from the subject file.

## Step 5: Design assessments

Read [assessment-design](references/assessment-design.md) for formative vs. summative choices, assessment type by Bloom's level, and rubrics. State the dialect/version for every code or query item. Ship a mapping table with every assessment:

| CLO | Assessed by | Weight |
| --- | --- | --- |
| CLO1: … | Quiz 2, Q3–5 | 10% |
| CLO3: … | Midterm project | 25% |

A CLO with no "assessed by" entry, or an item that maps to no CLO, means the alignment needs fixing before delivery.

## Step 6: Review existing material

| Reviewing | Check |
| --- | --- |
| CLOs | Each against the [clo-writing](references/clo-writing.md) checklist (observable verb, right level, assessable, scoped); name the failed criterion |
| A lesson plan | Maps to a real CLO; covers the topic's misconceptions, not only the happy path; timing is realistic |
| An assessment or rubric | Build the Step 5 mapping table from what exists; flag uncovered CLOs, unmapped items, and level mismatches (a *Create* CLO tested only by multiple choice) |

Report specific, cited gaps ("CLO 3 uses 'understand', which isn't observable; use 'explain' or 'trace'"), not a general quality verdict.

## Step 7: Deliver

Default to structured Markdown, or a Markdown artifact for anything document-length. For a syllabus, lesson plan or exam meant to be printed or submitted, produce a real file with the docx or pdf skill if one is available.
