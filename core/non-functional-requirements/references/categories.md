# The 14 NFR categories

## Contents

- Where the list comes from
- The table
- Choosing IN or N/A
- Mapping the older names
- Applicability table to fill in

---

## Where the list comes from

Categories 1–9 are the non-functional characteristics of **ISO/IEC 25010:2023** (second edition, published 2023-11, replacing the 2011 edition). Functional suitability, the ninth ISO characteristic, is functional, so it appears here only as category 10's accuracy concern. Categories 10–14 cover what real projects must check but ISO does not list as a separate characteristic. Their sources are the Volere template's NFR sections (operational, cultural, legal), the AWS Well-Architected pillars (operational excellence, cost optimisation, sustainability), and data-protection law.

## The table

| # | Category | Sub-characteristics (ISO/IEC 25010:2023 where marked ISO) | Typical metrics | Main method |
| --- | --- | --- | --- | --- |
| 1 | **Performance efficiency** (ISO) | time behaviour · resource utilization · capacity | p95 response time, LCP / INP / CLS, throughput, peak memory, max concurrent users | Test |
| 2 | **Reliability** (ISO) | faultlessness · availability · fault tolerance · recoverability | uptime %, error rate, MTBF, MTTR, RPO, RTO | Test, Demonstration |
| 3 | **Security** (ISO) | confidentiality · integrity · non-repudiation · accountability · authenticity · resistance | ASVS level passed, access-control matrix pass rate, DAST High count, dependency Critical count | Test, Inspection |
| 4 | **Interaction capability** (ISO; "usability" in 2011) | appropriateness recognizability · learnability · operability · user error protection · user engagement · inclusivity · user assistance · self-descriptiveness | task success %, time on task, errors per task, SUS, SEQ | Test with users, Inspection |
| 5 | **Accessibility and color** | the *inclusivity* sub-characteristic, split out because WCAG brings its own success criteria and method | contrast ratio, keyboard completion, target size, axe violations | Test, Inspection |
| 6 | **Compatibility** (ISO) | co-existence · interoperability | browser × viewport matrix pass rate, import/export round-trip fidelity | Test |
| 7 | **Maintainability** (ISO) | modularity · reusability · analysability · modifiability · testability | coverage, cyclomatic complexity, lint/type errors, time to make a reference change | Analysis, Inspection |
| 8 | **Flexibility** (ISO, new in 2023; absorbs 2011 "portability") | adaptability · scalability · installability · replaceability | p95 at 10× load, minutes from clean clone to running | Test, Demonstration |
| 9 | **Safety** (ISO, new in 2023) | operational constraint · risk identification · fail safe · hazard warning · safe integration | hazard log closed, fail-safe state demonstrated | Analysis |
| 10 | **Data integrity and accuracy** | ISO functional correctness + security integrity, made concrete | deviation from a hand calculation, rounding edge cases, constraint rejections, audit rows per edit | Test |
| 11 | **Privacy and compliance** | personal-data handling, consent, retention, deletion, sector rules | personal data found in logs (should be 0), deletion request time, retention enforced | Inspection, Test |
| 12 | **Observability and operability** | logs · metrics · traces · health checks · alerts · runbooks | correlation ID coverage, alert latency, documented runbook per alert | Demonstration |
| 13 | **Localization and cultural** | language, calendar, number and date formats, word breaking, fonts, time zone | hard-coded strings (should be 0), locale-correct dates, non-ASCII import fidelity | Inspection, Test |
| 14 | **Cost and sustainability** | hosting cost per user, page weight, idle resources | monthly cost ≤ budget, page weight ≤ N KB | Analysis |

Methods follow ISO/IEC/IEEE 29148. **T**est runs the system and compares output with the threshold. **A**nalysis calculates or models the result. **I**nspection examines the artefact, such as code, configuration or documents. **D**emonstration operates the system and observes it without instruments.

## Choosing IN or N/A

**Categories 1, 3, 4, 5 and 10 are always IN** for software that people use and that stores data. Marking one of them N/A needs a strong reason, such as "headless batch job with no UI" for 4 and 5.

For each of the others, ask: *if this fails, who loses what?* With no concrete answer, mark it N/A and give the reason in one line.

| Category | Usually N/A when |
| --- | --- |
| 2 Reliability | prototype, demo or thesis build with no availability promise (still keep recoverability: back up the data) |
| 6 Compatibility | internal tool on one mandated browser (name that browser) |
| 7 Maintainability | throwaway spike with an end date |
| 8 Flexibility | fixed user count with no growth plan; single deployment target |
| 9 Safety | no control of physical equipment and no health, life or large financial impact |
| 11 Privacy | no personal data at all (check this: names, IDs and scores *are* personal data) |
| 12 Observability | single-user local tool |
| 13 Localization | single language and locale (still state which one) |
| 14 Cost | academic or free-tier work with no budget owner |

BAD: the table lists 4 categories and the rest are absent.
BETTER: all 14 rows appear, 9 are IN, and 5 are N/A with reasons such as "9 Safety: N/A, the system computes grades and controls no physical equipment."

## Mapping the older names

A document or thesis that cites the **2011** edition must use 2011 names throughout, and one that cites 2023 must use 2023 names. Mixing the two reads as an error.

| ISO/IEC 25010:2011 | ISO/IEC 25010:2023 |
| --- | --- |
| Usability | Interaction capability |
| Usability → accessibility | Interaction capability → inclusivity (plus self-descriptiveness, user assistance) |
| Usability → user interface aesthetics | Interaction capability → user engagement |
| Reliability → maturity | Reliability → faultlessness |
| Portability | Flexibility (adds scalability) |
| — | Safety (new) |
| Security (5 sub-characteristics) | Security (adds resistance) |

## Applicability table to fill in

```markdown
| # | Category | IN / N/A | Reason (one line) |
| --- | --- | --- | --- |
| 1 | Performance efficiency | IN | |
| 2 | Reliability | | |
| 3 | Security | IN | |
| 4 | Interaction capability | IN | |
| 5 | Accessibility and color | IN | |
| 6 | Compatibility | | |
| 7 | Maintainability | | |
| 8 | Flexibility | | |
| 9 | Safety | | |
| 10 | Data integrity and accuracy | IN | |
| 11 | Privacy and compliance | | |
| 12 | Observability and operability | | |
| 13 | Localization and cultural | | |
| 14 | Cost and sustainability | | |
```
