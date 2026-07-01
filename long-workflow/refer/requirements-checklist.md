# Requirements Checklist (Stage 1)

No development starts on a fuzzy requirement. If you can't write the items below in plain language, the feature isn't ready to build yet — say so, and ask the questions needed to get there before touching code.

## Required before moving to design

- [ ] **Problem statement** in plain language, 1–3 sentences. Not a feature description — the actual problem being solved.
- [ ] **Acceptance criteria**, numbered and testable. "Works well" is not a criterion; "form rejects an email without an @ and shows an inline error" is.
- [ ] **Out-of-scope**, stated explicitly. What this change is *not* doing, even if it sounds related.
- [ ] **Dependencies and integrations** identified — other services, APIs, or features this touches or relies on.
- [ ] **Data inputs and expected outputs** defined — shape, types, what comes in and what goes out.
- [ ] **Edge cases and error states** documented — empty input, failure modes, permission boundaries.

## How to elicit it

- Ask "what does success look like?" before asking "how should I build it?" Solving the wrong problem efficiently is still solving the wrong problem.
- Challenge vague words on sight: "fast," "simple," "better," "intuitive." Ask what they mean in terms you could actually test.
- Once you think you understand the requirement, write it back as a short summary and get it confirmed before starting work. This is cheap insurance against building the wrong thing.
- Explicitly ask what's out of scope, even if the user didn't mention it. People under-specify scope far more often than they over-specify it.

## Failure mode this prevents

Starting development from a verbal description with no written, confirmed summary. The cost shows up later: rework on a misunderstood requirement typically runs 3–5× the cost of getting it right the first time, because the rework competes with whatever the team has moved on to.