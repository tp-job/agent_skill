# NFR verification plan — <system name>

Spec version: <x.y> · Date: <YYYY-MM-DD>

Methods: **T** = Test · **A** = Analysis · **I** = Inspection · **D** = Demonstration
Timing: **CI** = every commit · **REL** = before release, on the deployed environment · **UAT** = with users · **PROD** = in production

| ID | Method | Tool / procedure | Timing | Evidence produced | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| PF-01 | T | `performance.measure()`, 30 runs, `latency_summary.py` | REL | `evidence/pf-01.csv` + summary | | planned |
| PF-09 | T | k6 `load.js` with thresholds | REL | `evidence/pf-09-summary.json` | | planned |
| AX-01 | T | `contrast_check.py tokens.csv` | CI | script output | | planned |
| AX-17 | T | axe (`@axe-core/playwright`), fail on serious | CI | test report | | planned |
| UX-04 | T | SUS form after 5 tasks, `sus_score.py` | UAT | `evidence/sus.csv` + summary | | planned |
| SC-01 | T | table-driven access-matrix test | CI | test report | | planned |
| DI-01 | T | oracle fixtures vs calculation module | CI | test report | | planned |
| RL-03 | D | restore drill into a scratch database | REL | timed log + row counts | | planned |

## User study protocol (if any UX NFR is IN)

- Participants: <n ≥ 5, who, how recruited, distinct from the expert panel>
- Tasks (goals, not instructions), each with a success definition:
  1. <task> — success when <observable end state>
- Per task: time cap, SEQ (1–7) after each task
- After all tasks: SUS (10 items, 1–5)
- Recording: <screen recording / observer sheet>; consent obtained

## Entry and exit

- Start verification when the build under test is deployed to <environment> and the spec is frozen at version <x.y>.
- Verification is done when every IN NFR has a status of passed, failed with a decision, or blocked with a reason.
