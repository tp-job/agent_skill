# Writing measurable NFRs

## Contents

- The template (Planguage fields)
- Quality gate (ISO/IEC/IEEE 29148)
- Banned vague words
- BAD / BETTER pairs
- Priorities and conflicts

---

## The template (Planguage fields)

Gilb's Planguage splits a quality requirement into named parts. This skill keeps six of them, adds a source, and requires all seven.

| Field | Answers | Example |
| --- | --- | --- |
| **ID** | stable handle for traceability | `PF-01` (prefix by category: PF, RL, SC, UX, AX, CP, MT, FX, SF, DI, PR, OB, LC, CO) |
| **Statement** | one sentence, one quality | The score table page renders all rows quickly. |
| **Scale** | the unit of measure | seconds from navigation start to the last table row painted |
| **Meter** | how the number is obtained | `performance.measure()` in the page, 30 runs, p95 reported |
| **Condition** | the circumstances under which it holds | 150 students × 25 assessments, deployed server, warm cache, desktop Chrome, unthrottled |
| **Must** | the pass/fail threshold | p95 ≤ 2.0 s |
| **Plan** | the target you aim for (optional, better than Must) | p95 ≤ 1.0 s |
| **Source** | where the number comes from | Miller (1968); Nielsen (1993) — *or* "project target: <reason>" |

Priority (MoSCoW) and the verification method sit in the plan, not in this row.

## Quality gate (ISO/IEC/IEEE 29148)

Every row must pass all seven checks before step 4.

| Check | Fails when | Fix |
| --- | --- | --- |
| **Necessary** | nobody loses anything if it is removed | delete it |
| **Unambiguous** | two readers would measure it differently | define Scale and Meter |
| **Verifiable** | no test, analysis, inspection or demonstration could decide pass/fail | add a threshold and a meter |
| **Singular** | it contains "and" joining two qualities | split it into two IDs |
| **Feasible** | the threshold is beyond what the stack or budget can reach | lower Must, keep the ambition in Plan |
| **Consistent** | it contradicts another NFR (e.g. 10-minute session timeout vs "never lose unsaved scores") | resolve, and record the trade-off |
| **Traceable** | it has no source and no stated rationale | cite, or label as a project target with a reason |

## Banned vague words

When one of these words appears without a number in the same row, the row fails. `nfr_lint.py` checks for the English and Thai forms.

| English | Thai |
| --- | --- |
| fast, quick, responsive, efficient | เร็ว, รวดเร็ว, มีประสิทธิภาพ |
| easy, simple, intuitive, user-friendly | ง่าย, ใช้งานง่าย, เป็นมิตร |
| secure, safe, robust | ปลอดภัย, มั่นคง |
| reliable, stable, available | เสถียร, น่าเชื่อถือ |
| scalable, flexible, support(s) | รองรับ, ยืดหยุ่น |
| appropriate, adequate, sufficient, good | เหมาะสม, เพียงพอ, ดี |
| as soon as possible, minimal, maximise | โดยเร็ว, น้อยที่สุด, มากที่สุด |

The words may stay in the **Statement**. They become acceptable once Scale, Meter and Must give them a meaning.

## BAD / BETTER pairs

| BAD | BETTER |
| --- | --- |
| The system shall be fast. | PF-01: Score table, p95 ≤ 2.0 s from navigation to last row painted, 150 × 25 dataset, deployed server, 30 runs. |
| The system shall be easy to use. | UX-04: Mean SUS ≥ 68 from ≥ 5 instructors after completing the 5 core tasks unaided. |
| Colors shall have good contrast. | AX-01: Body text contrast ≥ 4.5:1 against its background in every theme (WCAG 2.2 SC 1.4.3). |
| The system shall be secure and keep data private. | Split: SC-01 cross-course access returns 404 for every route × role; PR-01 zero student names, IDs or scores in application logs after the full test suite. |
| The system shall support many users. | FX-01: 30 concurrent virtual users for 5 min, p95 ≤ 2 s, error rate < 1% (project target: department has 28 instructors). |
| Errors shall be handled properly. | UX-02: Every form and import error names the field or row, the cause, and a fix, in Thai (WCAG 3.3.1, 3.3.3). |
| Data shall be backed up. | RL-03: Daily backup; a restore drill recovers the database within 60 min (RTO) with ≤ 24 h of data lost (RPO). |

## Priorities and conflicts

- **Use Must for the release gate and Plan for ambition.** If every NFR is "Must = perfect", nothing can ship, and the team will start ignoring the gate.
- **Write down the conflicts you find.** Performance and security often pull against each other (encryption and audit logging cost latency), and so do accessibility and visual design (brand colors that fail contrast). Record which side won and why, in one line under both IDs.
- **Keep the list short.** Ten measured NFRs beat forty unmeasured ones. When the list grows past about 25, merge rows that share a Meter.
