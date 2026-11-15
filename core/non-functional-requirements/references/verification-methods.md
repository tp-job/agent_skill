# Verification methods, timing and reporting

## Contents

- The four methods
- When each check runs
- Reporting numbers honestly
- Turning a failure into a decision

---

## The four methods

ISO/IEC/IEEE 29148 names four ways to verify a requirement. Choose the cheapest one that can actually decide pass or fail.

| Method | What it is | Good for | Not enough for |
| --- | --- | --- | --- |
| **Test** | run the system with defined inputs and measure the output | response time, contrast, access control, accuracy | anything that needs judgement |
| **Analysis** | calculate or model it: complexity metrics, capacity maths, cost estimate | maintainability, cost, scalability projections | claims about the real deployment |
| **Inspection** | examine artefacts such as code, config, logs and documents against a checklist | privacy in logs, ASVS items, localization strings | runtime behaviour |
| **Demonstration** | operate the system and observe without instruments | restore drill, alert firing, install from clean clone | anything with a numeric threshold below human perception |

A single NFR can use two methods. AX-07 (keyboard), for example, is a Test of each task plus an Inspection of focus order.

## When each check runs

| Moment | What belongs there | Example |
| --- | --- | --- |
| **Every commit (CI)** | cheap, deterministic and automatable checks | accuracy unit tests, access-control matrix, `npm audit`, axe on key pages, lint/type check, `nfr_lint.py` on the spec |
| **Before release** | slower checks, or checks that need the deployed environment | Lighthouse on the deployed URL, k6 load run, ZAP baseline, browser matrix, restore drill |
| **UAT / user study** | checks that need people | task success, time on task, SUS, SEQ, screen-reader walk-through |
| **In production** | checks that need real traffic | Web Vitals at the 75th percentile from real users, uptime, error rate |

In CI, put the threshold in the tool so that a regression fails the build. Examples are a k6 `thresholds` block, Lighthouse CI assertions, a coverage threshold in `vitest.config`, and axe with `failOn: serious`.

## Reporting numbers honestly

| Rule | BAD | BETTER |
| --- | --- | --- |
| Report the distribution | "average 1.2 s" | "n = 30, median 0.9 s, p95 1.6 s, max 2.3 s" |
| State the environment | "page loads in 1 s" | "Vercel production, Chrome 131 desktop, unthrottled, warm, 2026-11-15" |
| Keep raw evidence | a screenshot of the summary only | JSON export plus the command that produced it, saved in `evidence/` |
| Separate cold from warm | cold-start runs mixed into the sample | cold start reported on its own line |
| Say what was not covered | silence | "Screen-reader check done with NVDA only; VoiceOver not tested" |

**Sample size.** Use at least 30 runs for timings, which gives a stable p95. Usability studies need 5 users per round to find the most frequent problems (Nielsen and Landauer, 1993). A SUS benchmark wants 12 or more respondents for a tight confidence interval (Sauro and Lewis, 2016), so with fewer than that, report the interval as wide.

## Turning a failure into a decision

Each failed NFR ends in exactly one of three states, and the report records which.

1. **Fix**: name the change, the owner and the re-test date.
2. **Relax**: the Must was wrong. Change it, record the reason, and keep the old value in the history.
3. **Accept the risk**: a named person signs that the system ships with the gap until a stated date.

"Will improve later" is none of the three, so it does not count as a decision.
