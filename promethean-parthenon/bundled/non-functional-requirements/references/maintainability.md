# Category 7 — Maintainability

ISO/IEC 25010:2023 sub-characteristics: modularity, reusability, analysability, modifiability and testability.

## NFR catalogue

| ID | Sub-characteristic | Statement | Must (typical) | Method |
| --- | --- | --- | --- | --- |
| MT-01 | Testability | statement and branch coverage of business-logic modules | ≥ 80% (≥ 90% for calculation code) | Analysis (`vitest --coverage`, `pytest --cov`) |
| MT-02 | Analysability | static checks are clean | 0 lint errors, 0 type errors in strict mode, run in CI | Analysis |
| MT-03 | Analysability | function complexity | cyclomatic complexity ≤ 10 per function, with listed exceptions | Analysis (ESLint `complexity`, radon) |
| MT-04 | Modularity | layer boundaries hold | no imports from UI into the data layer, or from routes into another route's internals (dependency-cruiser or import lint rules) | Analysis |
| MT-05 | Modifiability | reference change cost | a named reference change (e.g. "add a new assessment type") takes ≤ N files and ≤ N hours, measured once | Demonstration |
| MT-06 | Reusability | shared logic has one home | each business rule is implemented once; duplicate-code report under a threshold | Analysis (jscpd) |
| MT-07 | Analysability | onboarding | a new developer runs the app from the README in ≤ 30 min | Demonstration |
| MT-08 | Analysability | schema history | every database change is a versioned migration; no manual production edits | Inspection |

## Notes

- **Coverage is a floor, not proof.** High coverage with weak assertions catches little. Back up the critical modules with a mutation-testing sample (e.g. Stryker) to check that the assertions actually fail when the code is wrong.
- **Choose numbers your codebase already nearly meets, then ratchet.** Setting a threshold of 90% on a codebase sitting at 40% means the gate gets switched off within a week.
- **MT-05 and MT-07 are the human-facing measures.** They show maintainability to an examiner or a new team member better than any single metric.
