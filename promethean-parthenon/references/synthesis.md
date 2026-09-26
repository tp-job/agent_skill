# Synthesis — from many sources to one position

The input is several things that disagree: expert articles, docs for two library versions, a colleague's advice, three blog posts, the codebase's own history. The output the Role pillar needs is **a position** — not a digest of the inputs.

**Hands off:** a position, the confidence behind it, the premise it rests on, and what would change it.

---

## Summary is not synthesis

| Summary (BAD) | Synthesis (BETTER) |
| --- | --- |
| "Article A recommends microservices for scale. Article B warns about operational cost. Article C says it depends on team size." | "For a 4-person team shipping one product: stay monolithic. A and B agree once you read A's premise — 40+ engineers, independent deploy cadence. Neither holds here. Revisit if we pass ~15 engineers or two teams need separate release schedules." |
| One paragraph per source | One claim, with sources as evidence under it |
| Every view weighted equally | Views weighted by evidence and fit to *this* context |
| Ends with "it depends" | Ends with what it depends *on*, and which way this case falls |

**The test:** could the reader act on it without reading the sources? If not, it is a summary.

---

## Step 1 — Grade each source before using it

| Grade | What it is | Weight |
| --- | --- | --- |
| **Measured** | Benchmark, incident data, experiment, production numbers — with method shown | Highest, if the conditions match yours |
| **Primary** | Official docs, spec, changelog, source code, the RFC | High — but check the version |
| **Practitioner** | Someone who built it and reports what happened | Medium — one context, honestly reported |
| **Opinion** | Reasoned argument, no data | Low — useful for the *arguments*, not the conclusion |
| **Echo** | Repeats another source | Zero additional weight — trace it to the original |

**Three checks on every source:**

1. **Version and date.** Advice about React 17, Python 3.8, or a model from two generations ago may be exactly backwards now. State the version the claim holds for.
2. **Premise.** What situation was the author in? Team size, scale, domain, constraints. Most "disagreements" between experts are the same reasoning applied to different premises.
3. **Incentive.** A vendor's benchmark of its own product is data, but not neutral data.

---

## Step 2 — Map the agreement and the conflict

Before forming a view, lay the claims out:

| Claim | Sources for | Sources against | Why they differ |
| --- | --- | --- | --- |
| Split into services early | A (opinion) | B (practitioner), C (measured) | A assumes 40+ engineers; B, C are small teams |
| Keep a single database | B, C | — | — |

**Where experts agree across different premises**, that is your strongest ground — the claim survives changing conditions.

**Where they disagree, find the hinge.** It is almost always one of: a different premise, a different version, a different definition of the same word ("scale", "real-time", "secure"), or one side measuring and the other reasoning. Name the hinge; then say which side of it *this* case sits on.

**Where only one source speaks**, say so. A single source is a lead, not a consensus.

---

## Step 3 — Add what the sources cannot know

Every source was written without knowing your situation. The synthesis is where that gap gets closed — and it is where the value is, because a model can summarize sources as well as anyone, but only this context knows:

- **The constraints that are not technical** — budget, deadline, who maintains it after launch, what the team already knows.
- **The history** — what was tried here and why it was abandoned.
- **The cost of being wrong** — reversible in an afternoon, or a migration nobody will fund twice.
- **What the people involved actually value** — speed vs. safety, novelty vs. familiarity.

If you do not know these, **ask** — they change the answer more than another source would. How to ask well: [human-judgment](human-judgment.md).

---

## Step 4 — Write the position

```
Position:    <one sentence — the call>
Because:     <the 2–3 claims it rests on, each with its grade>
Premise:     <what must stay true for this to stay right>
Confidence:  high | medium | low — and the single biggest reason it isn't higher
Against:     <the strongest opposing view, stated fairly, and why it loses here>
Revisit if:  <the observable change that would flip it>
```

**Label every claim** as measured, cited, or inferred. The reader must be able to tell a number from a guess without asking. (An inferred claim stated as measured is regression case RC-05.)

**State the strongest counter-argument in its best form.** If you cannot, you have not understood the disagreement yet.

**"Revisit if" is not optional.** A position without it cannot expire, and positions do expire — regression case RC-07 is a decision that stayed right after its premise changed.

---

## Anti-patterns

| Anti-pattern | Tell | Fix |
| --- | --- | --- |
| Source count as evidence | "Most articles say…" | Five echoes of one blog post are one source |
| Authority as evidence | "X at Google says…" | What was X's premise? Does it match yours? |
| Recency as evidence | "The newer approach is…" | Newer is a date, not an argument |
| False balance | Equal space to a measured result and an opinion | Weight by grade, not by turn |
| Hidden hedge | Every sentence qualified | One confidence statement, stated once |
| Synthesis as a list | Bullets per source, no position | Rewrite as Step 4's template |

---

## When not to use this

- **One authoritative source answers it.** The official docs for the version you run beat any synthesis. Read them and stop.
- **The question is factual and checkable.** Run it, measure it, or read the code — don't synthesize opinions about what a function returns.
- **The decision is cheap and reversible.** Try one option and observe. An experiment beats a literature review when the experiment costs less.
