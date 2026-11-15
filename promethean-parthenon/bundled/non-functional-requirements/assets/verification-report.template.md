# NFR verification report — <system name>

Spec version: <x.y> · Build: <commit SHA> · Date: <YYYY-MM-DD>

## Summary

<N> NFRs in scope: <p> passed, <f> failed, <b> blocked. Failed items and their decisions are listed first.

## Environment

- Hosting: <tier, region> · Database: <tier>
- Client: <browser + version, OS, device class> · Network: <profile>
- Dataset: <description and size>
- Measurement dates: <range>

## Failed or blocked (first)

| ID | Must | Measured | Decision (fix / relax / accept risk) | Owner and date |
| --- | --- | --- | --- | --- |
| | | | | |

## Results

| ID | Category | Method | Must | Measured (n, median, p95, max or value) | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| PF-01 | Performance | T | p95 ≤ 2.0 s | n=30, 0.84 / 1.31 / 1.62 s | pass | `evidence/pf-01.csv` |
| | | | | | | |

## Traceability

| Requirement / user need | NFR IDs | Verified by | Result |
| --- | --- | --- | --- |
| <e.g. instructors record scores before the deadline without waiting> | PF-01, PF-04, PF-09 | k6 run, Performance API | pass |

## Not covered

<What was not verified, and why. Examples: VoiceOver not tested; production Web Vitals not yet available because of low traffic.>
