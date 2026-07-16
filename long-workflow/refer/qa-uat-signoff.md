# QA, UAT & Deployment (Stages 4–6)

## Stage 4 — QA

Testing happens against the use cases written in Stage 2. If a use case was never written, testing degrades into guesswork — go back and write it rather than testing blind.

- [ ] Every use case tested and the result recorded, even briefly.
- [ ] Edge cases and error states from Stage 2 verified, not assumed to work because the happy path does.
- [ ] Regression check on anything the change touches, not just the new surface.
- [ ] No critical or high-severity issues left open.

**Define and validate the output, before you call something done:** write down what the expected output actually is — the data shape, the UI state, the API response — *before* writing the function, and use that written definition as the test case at the end. Compare the actual output to it directly rather than eyeballing whether it "looks right." Where it matters, get a second look — a fresh read catches what the person who wrote the code stops seeing.

## Stage 5 — UAT

UAT is not the first time the user sees the feature. If it is, the earlier stages were skipped, not skippable.

- [ ] UAT script prepared from the Stage 2 use cases, not written from scratch at this stage.
- [ ] Tested in an environment that matches what's described as production-equivalent.
- [ ] Tested by someone in the actual user role — not just by whoever built it.
- [ ] Feedback captured using [[structured-feedback-format]].
- [ ] Sign-off — even an explicit "looks good, ship it" from the user — recorded before deployment, not assumed from silence.

## Stage 6 — Deployment

- [ ] Deployment plan stated, even briefly: what's shipping, in what order.
- [ ] Rollback plan named before shipping, not improvised after something breaks.
- [ ] Monitoring or a smoke-test step named for right after deploy.
- [ ] Who's watching the release window is clear, even if that's just "I'll check back after this lands."

## Leaving a written trail

The last of the five core skills: produce artifacts that let anyone — including a future you, in a session that's lost this context — understand, test, and maintain the work.

- A short note for every feature: what it does, how to configure or invoke it, known limitations.
- Keep the use case document current through development — update it the moment scope changes, not at the end.
- Store artifacts somewhere durable (the conversation, a file, a doc) rather than letting the only record live in your own working memory for the session.

**Failure mode this whole section prevents:** the only place the system is understood is the developer who built it — and on a long, multi-session build, that "developer" might just be an earlier, now-inaccessible part of this same conversation.