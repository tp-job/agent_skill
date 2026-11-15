---
name: non-functional-requirements
description: >-
  Writes measurable non-functional requirements (NFRs) and verifies them with evidence across 14
  categories built on ISO/IEC 25010:2023: performance, reliability, security, usability/UX,
  accessibility and color contrast (WCAG 2.2), compatibility, maintainability, flexibility, safety,
  data integrity, privacy, observability, localization, cost. Each NFR gets a scale, meter, condition,
  pass threshold and cited source, then a verification method and a traceable results report; has a
  thesis mode with Thai citations. Trigger for: "write the non-functional requirements", "is this NFR
  measurable", "how do I verify response time", "what contrast ratio do I need", "SUS score", "ISO
  25010", "ตรวจสอบ non-functional", "เขียน NFR", "เกณฑ์ความเร็วในการตอบสนอง". Not for auditing code
  for vulnerabilities, fixing a Lighthouse score, auditing UI theme tokens, or designing functional
  test cases.
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "1.0.0"
  source: >-
    ISO/IEC 25010:2023, ISO/IEC/IEEE 29148:2018, ISO 9241-11:2018, WCAG 2.2, OWASP ASVS, Gilb's
    Planguage, the Volere template, Google Web Vitals, and HCI response-time research (compiled 2026)
---

# non-functional-requirements

> Pick categories → write each NFR with a number → reject the vague ones → plan how each is proven → measure → report. An NFR without a meter is a wish, and a "pass" without raw numbers is a claim.

## The flow

```
 0 CONTEXT ── system type · users · data size · environment · mode (engineering | thesis)
   │
 1 CATEGORIES ── 14 rows, each marked IN or N/A with a one-line reason
   │
 2 WRITE ── per NFR: Scale · Meter · Condition · Must · Plan · Source
   │
 3 QUALITY GATE ── every NFR measurable, singular, feasible? ── no ──► rewrite (back to 2)
   │ yes
 4 PLAN ── method (Test · Analysis · Inspection · Demonstration) · tool · when · owner
   │
 5 MEASURE ── raw numbers: n, median, p95, max · environment · date
   │
 6 REPORT ── NFR → method → threshold → measured → pass/fail · traceability
```

Three rules hold the flow together:

1. **Gate 3 is hard.** A requirement with no number and no meter goes back to step 2. Verifying it later is impossible, so the defect is cheapest to fix here.
2. **The threshold is written before the measurement.** A threshold chosen after seeing the result describes the result instead of testing it.
3. **Every number has a source or is labelled as the project's own choice.** "2 seconds (Miller, 1968)" and "30 concurrent users (project target, from department headcount)" are both honest. A bare "2 seconds" is not.

---

## Step by step

| Step | Do | Output | Depth |
| --- | --- | --- | --- |
| **0 Context** | Settle system type, user groups, realistic data volume, hosting, and mode. If a web app or API is already evident, do not ask. | one paragraph | — |
| **1 Categories** | Walk the 14 categories. Mark each IN or N/A with a reason. Never drop one silently. | applicability table | [categories](references/categories.md) |
| **2 Write** | Write each NFR in the template: ID, category/sub-characteristic, statement, Scale, Meter, Condition, Must, Plan, priority, Source. | [nfr-spec template](assets/nfr-spec.template.md) | [writing-measurable-nfrs](references/writing-measurable-nfrs.md) |
| **3 Gate** | Run the quality checks and the banned-word list on every row. With a file, run `python scripts/nfr_lint.py nfr-spec.md`. | rewritten rows | [writing-measurable-nfrs](references/writing-measurable-nfrs.md) |
| **4 Plan** | Give each NFR at least one method, a tool, a moment (every commit, pre-release, UAT), and an owner. | [verification-plan template](assets/verification-plan.template.md) | [verification-methods](references/verification-methods.md) |
| **5 Measure** | Run the checks. Keep raw output, state the environment, and report n, median, p95 and max, not a mean alone. | evidence folder | the category reference |
| **6 Report** | Fill in the results table, with failures first. Each failure needs a fix plan or a written risk acceptance. | [verification-report template](assets/verification-report.template.md) | [verification-methods](references/verification-methods.md) |

---

## Category references

Load only the categories marked IN at step 1.

| # | Category | Read |
| --- | --- | --- |
| 1 | Performance efficiency: response time, Web Vitals, load, capacity | [performance](references/performance.md) |
| 2 | Reliability: availability, fault tolerance, recoverability | [reliability](references/reliability.md) |
| 3 | Security at requirement level: ASVS, access-control matrix, scans | [security-requirements](references/security-requirements.md) |
| 4 | Interaction capability: usability, UX metrics, SUS, heuristics | [usability-ux](references/usability-ux.md) |
| 5 | Accessibility and color: WCAG 2.2 AA, contrast, color-blindness | [accessibility-color](references/accessibility-color.md) |
| 6 | Compatibility: browsers, devices, file formats, interoperability | [compatibility](references/compatibility.md) |
| 7 | Maintainability: coverage, complexity, static analysis | [maintainability](references/maintainability.md) |
| 8 | Flexibility: scalability, installability, replaceability | [flexibility-scalability](references/flexibility-scalability.md) |
| 9, 14 | Safety; cost and sustainability | [safety-cost](references/safety-cost.md) |
| 10 | Data integrity: calculation accuracy, rounding, null vs zero, audit trail | [data-integrity](references/data-integrity.md) |
| 11 | Privacy and compliance: PDPA/GDPR, personal data in logs, retention | [privacy-compliance](references/privacy-compliance.md) |
| 12 | Observability and operability: logs, metrics, alerts, runbooks | [observability](references/observability.md) |
| 13 | Localization: Thai language, Buddhist Era dates, encodings, time zones | [localization-thai](references/localization-thai.md) |

| Need | Read |
| --- | --- |
| NFRs for a thesis or academic report: placing them in chapters 2–4, justifying each number | [academic-mode](references/academic-mode.md) |
| A citation for a threshold, in APA 7 or Thai thesis style | [sources](references/sources.md) |

---

## Scripts

All four use only the Python 3.10+ standard library. Run each with `--help` to see its usage.

| Script | Does |
| --- | --- |
| `scripts/nfr_lint.py <spec.md>` | Flags rows in the NFR table that are missing Scale, Meter, Condition, Must or Source, and rows that use banned vague words. Exits 1 when it finds any. |
| `scripts/contrast_check.py <pairs.csv>` | Computes the WCAG contrast ratio for each `name,foreground,background,kind` row (`kind` = `text`, `large`, or `non-text`) and checks it against AA and AAA. |
| `scripts/latency_summary.py <file>` | Reads a k6 `--summary-export` JSON or a one-column CSV of milliseconds and prints n, median, p95, p99, max as a markdown table. |
| `scripts/sus_score.py <answers.csv>` | Takes one row per respondent with 10 answers on a 1–5 scale and prints the SUS score per respondent, plus the mean, SD and adjective rating. |

---

## Operating rules

- **Pick the percentile as well as the number.** "p95 ≤ 2 s over 30 runs" can be checked. "Average 2 s" hides the slowest tail, and the tail is what users remember.
- **State the measurement condition.** A response time with no data size, load, network or warm/cold state can be made to pass on any machine.
- **Automated checks are a floor.** axe and Lighthouse catch only part of WCAG. Focus order, error wording, and meaning carried by color still need a person.
- **Expert opinion is not user measurement.** A Likert form filled in by three experts tells you what experts think. To learn whether users can do the job, measure task success, time and SUS with real users.
- **N/A needs a reason.** "Safety: N/A, no physical actuation or health impact" is a decision. A missing row looks like an oversight.
- **Separate the project's targets from the standard's.** WCAG's 4.5:1 is normative. "80% task success" is a project choice, so label it as one.
- **Hand off the fixing.** This skill sets the bar and proves whether it is met. Code-level vulnerability audits, Lighthouse score repair, UI token audits and functional test-case design each belong to a dedicated skill or specialist, so mention that in prose and pass the failing NFR on.

## When not to use this

- **A failing Lighthouse score that needs fixing.** That is repair work, not a requirement.
- **A security code review.** This skill writes the security requirement and the verification plan. It does not read code looking for vulnerabilities.
- **Functional behaviour** ("the system shall export CSV"). That is a functional requirement and its tests.
- **A one-off "is this fast enough?" with a number already agreed.** Just measure it against that number.
