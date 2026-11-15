# Category 12 — Observability and operability

This category answers one question: when something goes wrong in production, how quickly can the team see it, find out why, and act? The sources are the "operational and environmental" section of the Volere template and the Operational Excellence pillar of the AWS Well-Architected Framework.

## NFR catalogue

| ID | Statement | Must (typical) | Method |
| --- | --- | --- | --- |
| OB-01 | Structured logs | logs are JSON with timestamp, level, event, request ID and actor ID; no free-text-only lines on server paths | Inspection |
| OB-02 | Request correlation | every request carries a correlation ID through the API, the service layer and the logs, and error responses show it to the user | Test |
| OB-03 | Health endpoint | `GET /health` reports app and database status in under 500 ms and does not require authentication or reveal internals | Test |
| OB-04 | Error tracking | unhandled errors reach an error tracker (e.g. Sentry) with stack trace and release version | Demonstration (throw a test error) |
| OB-05 | Metrics | request rate, error rate and p95 latency per route are visible on a dashboard | Demonstration |
| OB-06 | Alerting | an alert fires within 5 min when the error rate goes above 5% or the health check fails | Demonstration (trigger it in staging) |
| OB-07 | Runbook | every alert links to a runbook entry: what it means, first checks, how to roll back | Inspection |
| OB-08 | Release traceability | the running version (commit SHA) is visible in an endpoint or footer | Inspection |
| OB-09 | Log retention | logs are kept for N days and access to them is restricted | Inspection |

## Sizing to the project

| Project | Keep |
| --- | --- |
| Thesis or prototype | OB-01, OB-03, OB-08 |
| Internal production tool | plus OB-02, OB-04, OB-06 |
| Customer-facing service | all |

Mark the rest N/A, with the project type as the reason.

## Pitfall

Logging is where personal data leaks most often, so an observability requirement must not break PR-01. Log IDs, never names or scores.
