# AI acceptance testing

Acceptance asks one question: *did we build what was asked?* It is checked against written acceptance criteria, one by one, from the user's side of the screen.

## Split the work

| AI agent checks | Human judges |
| --- | --- |
| Each criterion that has an observable outcome: a value shown, a state reached, an email sent, an error message | Whether it *feels* right: tone, clarity, effort, trust |
| The same path across roles, devices and locales | Trade-offs the criteria never mentioned |
| Negative paths a busy human skips | Whether a criterion itself was the right one |

## How the agent plays the user

1. **Take a persona from the requirement**, not an invented one: "a receptionist on a phone, one hand free".
2. **Drive only the public surface** — the browser or the API. No database peeking, no reading the source.
3. **For each criterion**, act, observe, and record evidence: a screenshot, a response body, a log line.
4. **Try one wrong way per criterion**: empty input, back button mid-flow, double submit, expired session.
5. **Return a verdict per criterion**: Pass, Fail, or **Cannot verify** with the reason.

## Verdict table

| AC | Criterion | Verdict | Evidence | Note |
| --- | --- | --- | --- | --- |
| AC-1 | Member can refund within 60 days | Pass | screenshot `ac1-refund.png` | |
| AC-2 | Final-sale items show "no refund" before purchase | Fail | product page has no notice | D-09 |
| AC-3 | Refund email arrives within 5 min | Cannot verify | no mail catcher in this env | needs human or mailpit |

## Limits

- **The agent can share the builder's misreading.** If the same model wrote the code and the criteria interpretation, it may confirm its own mistake. Give the acceptance agent the criteria text only, not the implementation notes.
- **"Cannot verify" is a valid result.** Reporting a pass that was not observed is the failure this step exists to prevent.
- **No criteria, no acceptance test.** If the requirement has none, write them with the human first; testing against criteria the agent invented proves the invention.
