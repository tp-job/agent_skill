# Category 8 — Flexibility

**Flexibility** is new as a characteristic in ISO/IEC 25010:2023. It replaces 2011's portability and adds scalability. Its sub-characteristics are adaptability, scalability, installability and replaceability.

## NFR catalogue

| ID | Sub-characteristic | Statement | Must (typical) | Method |
| --- | --- | --- | --- | --- |
| FX-01 | Scalability | growth headroom | at 3× the expected peak users, p95 stays within 1.5× of the normal-load p95 | Test (k6 step load: 1×, 2×, 3×) |
| FX-02 | Scalability | data growth | with 5 years of data volume, key pages still meet PF-01 | Test (seeded large dataset) |
| FX-03 | Installability | clean setup | from a clean clone, one documented command sequence gives a running app in ≤ 30 min | Demonstration |
| FX-04 | Installability | environment parity | dev, CI and production use the same runtime major version (`.nvmrc`, `engines`, Docker image) | Inspection |
| FX-05 | Adaptability | configuration over code | environment-specific values (URLs, keys, limits) live in environment variables, documented in `.env.example` | Inspection |
| FX-06 | Adaptability | business rules as data | rules that change by term or by course (grade cut-offs, weights) are stored as data, not hard-coded | Inspection |
| FX-07 | Replaceability | swap a provider | the hosting, database or identity provider can be replaced by changing config and one adapter module | Analysis (dependency review) |

## Step load, not a single number

A single load number such as "supports 100 users" says nothing about how the system behaves on the way there. Run 1×, 2× and 3× the expected peak, and plot p95 against users. Then report the knee, meaning the load at which p95 or the error rate starts climbing steeply.

```js
export const options = {
  stages: [
    { duration: '2m', target: 30 },   // 1x
    { duration: '2m', target: 60 },   // 2x
    { duration: '2m', target: 90 },   // 3x
    { duration: '1m', target: 0 },
  ],
};
```

## When to mark N/A

Mark the category N/A when the user count is fixed and small, there is no growth plan, and there is a single deployment target. Keep FX-03 anyway: an examiner or the next maintainer still has to install the system.
