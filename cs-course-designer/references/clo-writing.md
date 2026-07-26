# Writing Course Learning Outcomes

Reference for [cs-course-designer](../SKILL.md), Step 3. Read before drafting CLOs, and use the checklist when reviewing CLOs someone else wrote.

---

## What a CLO is and is not

A Course Learning Outcome states what a student will be able to **do** by the end of the course, in terms observable enough that two independent assessors would agree whether it happened.

| Not a CLO | Why | CLO |
| --- | --- | --- |
| "Students will understand recursion." | "Understand" isn't observable. You cannot grade it. | "Trace the execution of a recursive function and predict its output and base-case behavior." |
| "Cover joins, subqueries, and window functions." | Describes what the *instructor* does, not what the student can do. | "Write SQL queries using inner and outer joins to retrieve data from three or more related tables." |
| "Students will appreciate the importance of memory safety." | Affective, not assessable in a CS course. | "Identify buffer overflow and use-after-free defects in C code and correct them." |
| "Students will learn Python." | No boundary — unassessable at any specific level. | "Implement a Python program using functions, lists, and dictionaries to solve a specified data-processing task." |

Three tests. A CLO must be:

1. **Observable** — names something a student produces or performs.
2. **Assessable** — you can describe the task that would demonstrate it.
3. **Bounded** — has a scope; "write SQL" is not bounded, "write SQL joins across three tables" is.

---

## The verb bank

Verbs are the whole game. Pick from the level that matches the actual cognitive demand of the course — not the most impressive-sounding one.

### Remember
define, list, identify, name, recall, state, label, recognize, match

*Fits:* terminology, syntax names, operator precedence tables, standard library names.
*Rarely the top level of a course.* If your highest CLO is at Remember, the course is a glossary.

### Understand
explain, describe, summarize, classify, illustrate, interpret, paraphrase, distinguish, give examples of

*Fits:* how a mechanism works — "explain how the call stack grows during recursion," "describe what an index does to query cost."
*Watch:* "explain" is assessable (the student produces an explanation); "understand" is not. The difference is not pedantry.

### Apply
write, implement, execute, use, solve, compute, demonstrate, modify, construct (routine), apply

*Fits:* the workhorse level for intro programming and SQL. Writing code or queries to a given specification.
*Signal:* the student is given the problem and applies a known technique.

### Analyze
debug, trace, compare, decompose, differentiate, examine, diagnose, profile, distinguish between

*Fits:* tracing execution, finding defects, comparing two approaches, reading unfamiliar code.
*Signal:* the student must take something apart to see how it works or why it fails.
*Underused.* Most CS courses assess Apply heavily and Analyze barely, then wonder why students can write code but not debug it.

### Evaluate
assess, critique, justify, optimize, defend, select (with rationale), recommend, judge, prioritize

*Fits:* choosing between designs, judging trade-offs, code review, normalization decisions.
*Signal:* there is more than one defensible answer, and the reasoning is the assessed object.

### Create
design, build, develop, construct (original), formulate, compose, architect, produce

*Fits:* capstone projects, original schema design, a program from an open-ended brief.
*Signal:* the student decides what to build, not just how.
*Warning:* genuinely reaching Create requires time. A single lab is almost never Create; a three-week project can be.

---

## Verbs to avoid entirely

understand, know, appreciate, learn, be familiar with, be exposed to, grasp, be aware of, become comfortable with, gain insight into

Every one describes an internal state. None can be assessed. If you catch yourself writing one, ask: *what would a student do to show me they've done this?* — the answer is the verb you actually wanted.

---

## Anatomy of a well-formed CLO

```
[verb] + [object with scope] + [condition or context, if it matters]
```

> **Write** *SQL queries using inner and outer joins* **to retrieve data from three or more related tables.**
> └ Apply    └ bounded object                        └ scope condition that makes it gradeable

> **Trace** *the execution of a recursive function on a given input* **and predict the output and the number of calls.**
> └ Analyze  └ bounded object                                       └ the observable evidence

The condition clause is what turns a vague outcome into a gradeable one. "Write SQL joins" leaves the difficulty entirely unspecified; "across three or more related tables" fixes it.

---

## How many, and at what level

- **4–8 CLOs for a course.** They summarize the whole arc — not one per topic. Twenty CLOs means you've written a topic list.
- **Session-level objectives are narrower** and can be numerous. Don't confuse the two: a lesson plan's objectives are the steps, the CLOs are the destination.
- **Spread across levels.** A course whose CLOs are all Apply teaches technique without judgment. A course whose CLOs are all Evaluate has no foundation. A typical healthy distribution for an intro course: one Understand, three or four Apply, one or two Analyze. For an advanced course, shift the mass toward Analyze/Evaluate/Create.
- **The top CLO sets the ceiling.** If the highest CLO is Apply, no assessment should demand Create — and if an assessment does, either the CLO is understated or the assessment is unfair.

---

## Worked examples by subject

### General Computer Science (CS1)
1. *(Understand)* Explain how variables, control flow, and function calls execute step by step, including the role of the call stack.
2. *(Apply)* Implement programs using conditionals, loops, functions, and standard collections to solve specified problems.
3. *(Analyze)* Trace unfamiliar code to predict its output, and locate the source of a defect from observed incorrect behavior.
4. *(Analyze)* Compare the running time of two algorithms for the same task using Big-O notation.
5. *(Create)* Design and build a multi-function program from an open-ended problem brief, justifying the decomposition chosen.

### Database Management
1. *(Understand)* Describe the relational model and explain how keys enforce entity and referential integrity.
2. *(Apply)* Construct an ER diagram from a set of business requirements and translate it into relational schemas.
3. *(Evaluate)* Assess a schema for normalization anomalies and justify a normalization to 3NF, or a deliberate denormalization.
4. *(Analyze)* Diagnose the cause of a slow query using an execution plan and recommend an indexing change.
5. *(Understand)* Explain ACID properties and the practical consequences of each isolation level.

### SQL
1. *(Apply)* Write SELECT queries with filtering, ordering, and aggregation to answer specified business questions.
2. *(Apply)* Write queries using inner and outer joins to retrieve data from three or more related tables.
3. *(Analyze)* Distinguish cases requiring a subquery, a CTE, or a window function, and implement the appropriate one.
4. *(Evaluate)* Critique a query for correctness and performance, and rewrite it to eliminate a specific inefficiency.
5. *(Analyze)* Predict the result of a query involving NULLs, outer joins, and grouping, and explain the semantics that produce it.

### Python
1. *(Apply)* Implement programs using Python's core data structures — lists, dictionaries, sets, tuples — selecting the appropriate one for a given access pattern.
2. *(Apply)* Write functions with appropriate parameters, return values, and docstrings, and compose them into a working program.
3. *(Apply)* Handle runtime errors using exceptions, distinguishing recoverable from unrecoverable conditions.
4. *(Analyze)* Debug a failing Python program using tracebacks, print/logging instrumentation, and a debugger.
5. *(Apply)* Write unit tests that verify the behavior of a function, including its edge cases.
6. *(Create)* Design and implement a program using classes to model a problem domain given an open brief.

### C Programming
1. *(Understand)* Explain C's memory model, distinguishing stack, heap, and static storage and their lifetimes.
2. *(Apply)* Implement programs using pointers, arrays, and structs, including pointer arithmetic over an array.
3. *(Apply)* Manage heap memory correctly with `malloc`/`free`, avoiding leaks and double frees.
4. *(Analyze)* Diagnose segmentation faults and memory errors using compiler warnings and a tool such as Valgrind or a sanitizer.
5. *(Analyze)* Trace the effect of pass-by-value versus passing a pointer on a caller's data.

---

## Review checklist

Run each CLO through this. When one fails, **name the criterion it fails** rather than silently rewriting it — the author needs to know which rule was broken.

- [ ] **Observable verb.** Not understand/know/appreciate/learn/be familiar with.
- [ ] **Right Bloom's level.** Does the verb match what students will actually be asked to do? An *Evaluate* verb with only Apply-level assessments is a mismatch.
- [ ] **Bounded scope.** Could two instructors read this and set assessments of wildly different difficulty? Then it needs a condition clause.
- [ ] **Assessable.** Can you name the task that demonstrates it? If not, it isn't an outcome.
- [ ] **Student-centered.** Describes what the student does, not what the course covers.
- [ ] **Single outcome.** One verb, one outcome. "Write and evaluate and optimize queries" is three CLOs wearing a trenchcoat — and it is ungradeable, because partial success is unscoreable.
- [ ] **Assessed somewhere.** Cross-check against the assessment mapping table. A CLO with no assessment is decoration.
- [ ] **Level-appropriate.** Matches the stated audience. *Create* in a 6-hour intro workshop is aspirational, not real.
- [ ] **Right count.** 4–8 for a course. More means these are topics, not outcomes.

---

## Accreditation and certification contexts

If the request mentions ABET, program learning outcomes (PLOs), or a named certification, generic Bloom's CLOs alone are not enough:

- **ABET-style** requires mapping each CLO to program-level student outcomes, usually with an indication of the strength of the mapping and named performance indicators with a measurable target.
- **Certification-aligned** courses map outcomes to the vendor's published exam blueprint domains and weightings, not to a taxonomy.

In both cases, look up the specific framework's current requirements rather than assuming — they get revised. And if PLO-level mapping is likely needed but wasn't part of the request, say so plainly rather than producing course-level CLOs that imply the job is done.

---

## Related

- [assessment-design](assessment-design.md) — matching assessment type to Bloom's level, rubrics
- Subject topic maps: [computer-science](computer-science.md) · [database-management](database-management.md) · [sql](sql.md) · [python](python.md) · [c-programming](c-programming.md)
