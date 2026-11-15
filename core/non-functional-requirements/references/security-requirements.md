# Category 3 — Security (requirement level)

## Contents

- Scope of this file
- Pick an ASVS level
- NFR catalogue
- The access-control matrix test
- Tools

---

## Scope of this file

This file writes security **requirements** and **verification steps**. It does not review code for vulnerabilities. When a check fails and the code needs fixing, hand the finding to a dedicated security-review skill or specialist with the failing NFR ID.

ISO/IEC 25010:2023 sub-characteristics map to concrete checks:

| Sub-characteristic | Check |
| --- | --- |
| Confidentiality | only authorised roles read the data (access matrix); TLS everywhere |
| Integrity | input validated against a schema; database constraints; no unauthorised modification |
| Non-repudiation | sensitive changes are logged with who, when, old value and new value |
| Accountability | every action traces to an authenticated identity |
| Authenticity | sign-in via a trusted identity provider; token signature and expiry verified |
| Resistance (new in 2023) | rate limits, size limits, and graceful rejection of malformed or oversized input |

## Pick an ASVS level

The OWASP Application Security Verification Standard (ASVS) defines three levels. Choose one level and cite the version you used. The chapter numbering changed between 4.0.3 and 5.0, so a chapter reference only makes sense together with its version.

| Level | For |
| --- | --- |
| L1 | every application. The baseline, mostly checkable from the outside. |
| L2 | applications holding personal or sensitive data. The usual target for business, education and health systems. |
| L3 | high-value targets such as finance, critical infrastructure and medical devices |

Do not claim "ASVS L2 compliant" unless every L2 item was checked. Write "N of M L2 items in scope verified" instead.

## NFR catalogue

| ID | Statement | Must | Method |
| --- | --- | --- | --- |
| SC-01 | Access control across tenants, courses or owners | every route × role × own/other resource returns the designed status; other-resource requests return 404 (no existence leak) | Test (matrix) |
| SC-02 | Authorisation at every protected route | 100% of protected routes declare a required role; checked by a test that enumerates the route table | Test |
| SC-03 | Input validation | malformed payloads return 400 with a message, never 500 | Test |
| SC-04 | Authentication | tokens verified for signature, issuer, audience and expiry; session ends on sign-out | Test |
| SC-05 | Dynamic scan | ZAP baseline: 0 High alerts on the deployed app | Test |
| SC-06 | Dependencies | `npm audit` / `pip-audit`: 0 High or Critical without a recorded exception | Test (CI) |
| SC-07 | Transport and headers | HTTPS only; HSTS, `X-Content-Type-Options: nosniff`, a Content-Security-Policy, `frame-ancestors` | Inspection (Mozilla HTTP Observatory) |
| SC-08 | Secrets | no secrets in the repository or client bundle; secret scan clean | Inspection (gitleaks or similar) |
| SC-09 | Resource limits | upload size, rows, request rate and pagination limits enforced | Test (OWASP API4:2023) |
| SC-10 | Audit trail | each sensitive change recorded with actor, time, before and after | Test |

## The access-control matrix test

Build the matrix from the route table. Do not build it from memory.

| Route | Admin | Instructor (own course) | Instructor (other course) | Anonymous |
| --- | --- | --- | --- | --- |
| `GET /courses/:id/scores` | 200 | 200 | 404 | 401 |
| `PUT /courses/:id/scores/:sid` | 403 | 200 | 404 | 401 |
| `DELETE /users/:id` | 200 (soft) | 403 | 403 | 401 |

Generate one test per cell, for example a table-driven test using Fastify `inject()` or supertest. When a route is added to the app without a matrix row, the suite must fail.

## Tools

| Tool | Checks |
| --- | --- |
| Table-driven integration tests | SC-01 to SC-04, SC-10 |
| ZAP baseline scan (Docker) | SC-05 |
| `npm audit`, `pip-audit`, Dependabot | SC-06 |
| Mozilla HTTP Observatory | SC-07 |
| gitleaks, trufflehog | SC-08 |
| OWASP ASVS checklist | coverage across all chapters at the chosen level |
