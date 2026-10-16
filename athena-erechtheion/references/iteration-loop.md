# Iteration round — update, evaluate, revise, verdict, trade-offs

Review judges one draft against its thesis and target. A **round** judges a *revision*: it compares this draft with the last one and answers three things review alone does not — did the change help, was the feedback positive, and what did the change cost.

Without a round, every revision is judged alone. Each one "passes", and the design still drifts: the strong parts of round 1 erode by round 4 and nobody can say which change did it.

---

## 1. The round, in five steps

Run them in order. Each step has an output; a step with no output did not happen.

| # | Step | Do | Output |
| --- | --- | --- | --- |
| 1 | **Update** | Apply the change list agreed at the end of the last round, and only that. | the change list: 1–5 changes, each traced to the finding or feedback line it answers |
| 2 | **Evaluate** | Re-run pass 1 (thesis fit) plus every pass the changes touched. Collect the lead's feedback in their own words. See [critique](critique.md) §2. | a review note and the quoted feedback |
| 3 | **Revise** | Fix the blockers that evaluation surfaced. Nothing else. | the revised draft |
| 4 | **Verdict** | Classify the feedback as positive, mixed or negative (§2). | one verdict line with its reason |
| 5 | **Trade-offs** | List what the round gained and what it cost, with evidence (§3). Then decide. | a gained/cost table and one decision |

Two rules keep a round honest:

- **A new idea found during step 3 goes on the next round's change list.** Slipping it into this round changes the draft after it was evaluated, so the verdict describes a draft that no longer exists.
- **Keep the change list short.** Five changes and a negative verdict leave you unable to say which change caused it. When the question is "which of two options is better", change that one thing.

---

## 2. Verdict: classify the feedback, don't describe the mood

Feedback has three sources. Keep them apart, because they answer different questions.

| Source | Answers | Counts as evidence when |
| --- | --- | --- |
| Review passes | Does it meet the thesis, the target, the access floor? | the pass was actually run |
| The lead | Is this the direction? | quoted, not paraphrased |
| A hallway or task test | Can the intended reader do the job? | the Stage 0 "judged how" test was re-run |

Then classify:

| Verdict | When | Next |
| --- | --- | --- |
| **Positive** | no blockers, the target test passes, and the lead accepts with no reservation about direction | hand off; write the record |
| **Mixed** | the direction is accepted, and blockers, majors or named reservations remain | another round; the remaining items are its change list |
| **Negative** | pass 1 or 2 fails, the lead rejects the direction, or the draft is worse than the previous round on the very thing this round tried to fix | stop polishing; go back a stage (§4) |

| BAD | BETTER |
| --- | --- |
| "Feedback was mostly positive." | "Mixed. Lead accepted the layout ('finally reads as one page') and rejected the accent ('the pink still bothers me'). Pass 7 failed on one pair, 3.9:1." |
| "The client liked it." | "No verdict yet: the client said 'nice' and named nothing. Asked which of the two heroes they would ship." |

- **Politeness is not a positive.** In "nicer, but the pink still bothers me", the verdict is in the clause after "but".
- **Silence is not a positive.** Record `no feedback` and ask one question with the default you will take.
- **Your own satisfaction is not feedback.** It is a pass you have not run yet.
- **Separate what was said from what you infer.** Label the inference *inferred*.

---

## 3. Trade-offs: what the round gained and what it cost

Every revision buys something with something. Write both sides for each change.

| Change | Gained | Cost | Keep? |
| --- | --- | --- | --- |
| Headline 32 → 64 px | squint test leaves one leader, was three equal blocks | hero is 1.2 screens tall at 375 px; the CTA dropped below the fold | keep; move the CTA up next round |
| Accent pink → teal | lead: "calmer"; CTA pair now 5.1:1, was 3.9:1 | the teal matches the link colour, so links no longer stand apart | keep; re-pick the link colour |
| Added a testimonial strip | none observed | page is one section longer; breaks never-rule 3 ("no carousel") | revert |

- **Each side needs evidence**: a pass result, a quote, or a measurement. Otherwise label it *estimated*.
- **A gain that restates the change is not a gain.** "Bigger headline" is the change. "One thing leads" is the gain.
- **A change with no cost listed was not examined.** Look where costs hide: the other breakpoints, the other states, the never-rules, asset weight, build effort, and consistency with screens this round did not touch.
- **Compare with the previous round, then check round 1's Keep list.** A draft can beat the last round and still have lost what made the first one work.

End with one decision: hand off, another round with a named change list, or back to a named stage.

---

## 4. Negative verdict: return to the stage that owns the symptom

Do not redraw. A negative verdict means an earlier stage handed drafting the wrong input. Find which one.

| What the feedback says | Stage that owns it | Redo |
| --- | --- | --- |
| "This could be any company's site" | Art direction | the thesis is too broad; rewrite it until a stranger could reject an off-brand draft with it |
| "These parts don't belong together" | Art direction | derive each choice from the thesis again; cut any element with no reason behind it |
| "Too loud", accent on everything | Art direction | proportions of base, secondary and accent; check the never-rules |
| "It's fine, I just don't love any of it" | Creativity | the concepts did not differ enough; diverge again and re-score |
| "Where is the X screen?", a missing state | Architecture | the inventory; add the screen or state before drawing it |
| The "judged how" test fails twice | Stage 0 | the target; the test or the audience is wrong |
| Breaks with real copy, real images or 375 px | Drafting | this one *is* a drafting fix; stay in the loop |
| Effects or motion feel unrelated to the brand | Art direction | name what each motion says about the thesis; drop the ones that say nothing |

Ask the lead one question before redoing a stage, and attach the default you will take if they do not answer.

---

## 5. Output: the round log

Append one block per round to the design record, under `Rounds`.

```markdown
## Round <n> — <date>

Changed:  <1–5 changes, each → the finding or quote it answers>
Evidence: <passes re-run and their results; passes not run>
Feedback: "<verbatim>" — <who>
Verdict:  positive | mixed | negative — <one line of reason>
Gained:   <per change, with evidence>
Cost:     <per change, with evidence>
Decision: hand off | round <n+1>: <change list> | back to <stage>: <the one question for the lead>
```

---

## 6. Limits

- **No round without a change list.** "Make it better" is not a change; go back to the review note and pick findings.
- **Two rounds at most on the same blocker**, the same limit as [critique](critique.md) §5. A blocker that survives two rounds is not a drafting problem.
- **Two mixed verdicts in a row on the same item count as negative.** The reservation is about direction, not polish.
- **If round n is not better than round n−1 on its own goal, revert to n−1** and build from there. The later draft is not automatically the better one.

## When not to run a round

- **The first draft.** There is nothing to compare it with; run review only.
- **Exploration, mood play and rung-1 sketches.** They have no target and no thesis to return a verdict against.
- **A one-value fix with a checkable result**, such as one contrast pair. Run the pass, record the number, and finish.
