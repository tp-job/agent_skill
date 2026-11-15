# Category 2 — Reliability

ISO/IEC 25010:2023 sub-characteristics: faultlessness (called maturity in 2011), availability, fault tolerance and recoverability.

## Availability in numbers

| Availability | Downtime per 30-day month | Downtime per year |
| --- | --- | --- |
| 99% | 7.2 h | 3.65 days |
| 99.5% | 3.6 h | 1.83 days |
| 99.9% | 43.2 min | 8.76 h |
| 99.99% | 4.3 min | 52.6 min |

Do not promise more availability than the hosting provider's SLA allows. A free tier usually has no SLA at all, so for a thesis or prototype write recoverability NFRs instead of an uptime number.

Terms used below: **MTBF** is the mean time between failures and **MTTR** the mean time to recover. **RPO** (recovery point objective) is the maximum data loss, measured in time. **RTO** (recovery time objective) is the maximum time to restore service.

## NFR catalogue

| ID | Statement | Must (typical) | Method |
| --- | --- | --- | --- |
| RL-01 | Availability | ≥ 99.5% monthly, measured by an external uptime monitor | Test (in production) |
| RL-02 | Error rate | 5xx responses < 0.5% of requests under normal load | Test (load run, logs) |
| RL-03 | Backup and restore | restore drill succeeds; RTO ≤ 60 min; RPO ≤ 24 h | Demonstration |
| RL-04 | Fault tolerance: dependency down | when the database or identity provider is unreachable, the user sees a clear message, not a stack trace, and no partial write happens | Test (stop the dependency) |
| RL-05 | Transactions | multi-row writes (import, bulk score update) are all-or-nothing | Test (fail midway) |
| RL-06 | Idempotent retry | repeating the same request (double-click, network retry) creates no duplicates | Test |
| RL-07 | Faultlessness | no open defect of severity critical or major at release | Inspection (issue tracker) |
| RL-08 | Graceful degradation | if a non-essential feature (charts, notifications) fails, the core task still works | Test |

## How to verify

- **The restore drill is the only proof that backups work.** Restore into a separate database, run a query that counts rows, and record how long it took. A backup that has never been restored is untested.
- **Fault injection without extra tooling:** point the app at a wrong database URL, revoke the identity provider's client secret in staging, or kill the API process during an import. Observe what the user sees and what ends up in the database.
- **Uptime:** an external monitor such as UptimeRobot or Better Stack polls a `/health` endpoint every 1–5 minutes. Report the monitor's own figure.

## Pitfalls

- **Assuming the platform's backups are on.** Check which plan is active, how long backups are retained, and whether point-in-time recovery is included.
- **Counting only planned downtime.** If cold starts on a sleeping free tier exceed the response-time NFR, users experience them as failures.
