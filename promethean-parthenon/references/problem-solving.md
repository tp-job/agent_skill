# Problem-solving — framing before the pillars

The pillars assume a problem worth building against. This file is for the step before that: when the ask is a symptom, a wish, or a mess, and nobody has yet said what the problem *is*.

**Hands off:** a problem statement one sentence long, a named hypothesis, and the cheapest test that could kill it. Task — brief consumes all three.

---

## The rule

**Solve the problem you were given only after checking it is the problem you have.** An agent handed "make the dashboard faster" will make the dashboard faster. If the real complaint is "I can't tell which number to act on", it has shipped a fast wrong answer.

| BAD | BETTER |
| --- | --- |
| "Add caching to the dashboard endpoint." | "Users say the dashboard is slow. Measured: API 180 ms, page usable at 6 s — 5.4 s is a 2 MB chart bundle. The problem is bundle size, not the endpoint." |
| "Build a retry wrapper for the flaky test." | "The test fails 1 in 12 runs, always when it runs after `test_import`. Shared fixture state — a retry would hide it." |

---

## Step 1 — Restate, then find the question behind it

Write the ask back in one sentence, then ask **why** until the answer stops being about software. Stop at the first answer that names a person and a consequence.

```
"Export to CSV"
  why? → finance wants the numbers in a spreadsheet
  why? → they reconcile against the bank statement monthly
  why? → mismatches are found by hand, three days a month
= the problem: reconciliation takes three days. CSV is one candidate fix.
```

Stop early when the ask is already specific and cheap. Two whys on a one-line change is ceremony; this step pays on anything that will take more than a day.

**Symptom vs. problem vs. solution** — label each clause in the ask:

| Clause | Type | Treat as |
| --- | --- | --- |
| "it's slow" | symptom | evidence — measure it |
| "we lose customers at checkout" | problem | the target |
| "add a spinner" | solution | a hypothesis, not a requirement |

A solution in the ask is a hypothesis the asker already holds. Respect it — they often know something you don't — but test it like any other.

---

## Step 2 — Measure before you theorize

One number beats three theories. Before proposing any cause, collect the cheapest observation that splits the hypothesis space in half.

| Question | Cheapest split |
| --- | --- |
| Slow — where? | One timing at each layer boundary |
| Broken — since when? | `git bisect`, or the deploy log against the first report |
| Wrong — for whom? | Does it reproduce for every user, or one shape of data? |
| "Nobody uses it" | Usage count, not a survey |

If you cannot measure, say so and label every claim that follows as **inferred**. An unmeasured claim stated as fact is how a warning ships louder than the problem (regression case RC-05).

---

## Step 3 — Decompose by hypothesis, not by topic

A topic list ("frontend, backend, database") produces work in every bucket. A hypothesis tree produces one test that eliminates whole branches.

```
Checkout conversion dropped 8% last week
├── Fewer people reach checkout?        → funnel step counts, week over week
├── Same reach, more abandon at pay?    → payment error rate by provider
│   ├── Provider errors up?             → provider status + our 4xx/5xx
│   └── Errors flat, abandon up?        → what changed on the page (deploy log)
└── Measurement changed, not behaviour? → did the tracking code ship?
```

Rules for the tree:

- **Mutually exclusive, collectively exhaustive** at each level — if two branches can both be true, the split is wrong; if there is a way the outcome happens that no branch covers, it is incomplete.
- **Always include "the instrument is wrong."** A changed metric is a changed instrument surprisingly often.
- **Order by cost × likelihood.** Test the cheap, likely branch first, not the interesting one.

---

## Step 4 — Pick the reasoning move that fits

| Move | Use when | The question |
| --- | --- | --- |
| **Work backwards** | The goal is clear, the path is not | What must be true the step before done? And before that? |
| **Inversion** | Designing anything that can fail | How would I guarantee this fails? Now prevent each one. |
| **First principles** | Convention is the only reason offered | What does physics / the data / the contract actually require? |
| **Analogy** | The shape looks familiar | Where have I solved this shape — and where does the analogy break? |
| **Bound it** | A decision hinges on a magnitude | Order-of-magnitude estimate: is this 10 ms or 10 s, 10 rows or 10 M? |
| **Smaller version** | The whole is too big to reason about | Solve it for one user, one row, one request — then generalize |
| **Relax a constraint** | Every option violates something | Which constraint, if dropped, makes this easy? Is it really fixed? |

**Analogy is the most dangerous move** because it feels like understanding. Name the point where the analogy breaks before relying on it.

---

## Step 5 — When stuck

Three failed attempts is the stop signal (operating rules). What to do *instead of* a fourth:

1. **Re-read the problem statement.** Most stalls are a wrong frame, not a hard problem.
2. **Change the representation.** Table → diagram, prose → state machine, code → the data it produces. A problem that is hard in one representation is often trivial in another.
3. **Write down what you know is true** — observed, not assumed. The gap between that list and your theory is usually where the bug lives.
4. **Explain it to someone** (or write it as if to someone). The sentence you cannot finish is the hole.
5. **Ask the human for what only they know** — see [human-judgment](human-judgment.md). Not "what should I do?" but "which of these two premises is true in your world?"

---

## When not to use this

- **The ask is already a well-formed problem** with a measured symptom and an owner. Go to Task.
- **A named bug with a repro.** That is debugging; the frame is already fixed.
- **Exploration.** When the goal is to learn what is possible, a fixed problem statement narrows too early — time-box it instead.
