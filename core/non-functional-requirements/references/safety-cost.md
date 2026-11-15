# Categories 9 and 14 — Safety; cost and sustainability

These two categories are N/A for most web and business applications. Read this file to decide quickly, record the decision, and move on.

## Category 9 — Safety (ISO/IEC 25010:2023, new characteristic)

Sub-characteristics: operational constraint, risk identification, fail safe, hazard warning and safe integration.

**In scope when** the software controls physical equipment (devices, vehicles, industrial or lab machines), affects health or medical decisions, or can cause large irreversible financial harm without a human check.

**N/A reason template:** "Safety: N/A. The system <does what>, controls no physical equipment, and every consequential output is reviewed by a person before it takes effect."

When it is in scope:

| ID | Statement | Method |
| --- | --- | --- |
| SF-01 | A hazard log lists each hazard, its cause, severity, likelihood and mitigation | Analysis |
| SF-02 | On failure, the system goes to a defined safe state (stops, holds its last safe value, or alerts) | Demonstration |
| SF-03 | The user is warned before an irreversible or dangerous action and must confirm it | Test |
| SF-04 | Operational limits (rates, ranges) are enforced in software and cannot be overridden from the UI | Test |

A regulated domain brings its own standard, such as IEC 62304 for medical device software or ISO 26262 for automotive. Name the standard and follow it. This skill's table is not a substitute for it.

## Category 14 — Cost and sustainability

The sources are the Cost Optimization and Sustainability pillars of the AWS Well-Architected Framework.

**In scope when** someone owns a budget, or the organisation has a carbon or efficiency goal.

**N/A reason template:** "Cost: N/A. Academic project on free tiers with no budget owner; free-tier limits are recorded under capacity."

When it is in scope:

| ID | Statement | Must (example) | Method |
| --- | --- | --- | --- |
| CO-01 | Monthly running cost at expected load | ≤ budget, with a per-service breakdown | Analysis (provider pricing calculator) |
| CO-02 | Cost at 3× load | stays within 3× (no pricing cliff) | Analysis |
| CO-03 | Free-tier limits | each limit (rows, bandwidth, function hours, sleep policy) listed with current usage | Inspection |
| CO-04 | Page weight | key pages transfer ≤ N KB compressed | Test (Lighthouse "total byte weight") |
| CO-05 | Idle resources | no always-on resources that go unused; previews and staging shut down when idle | Inspection |

CO-03 matters even for a thesis. A free tier that sleeps or caps rows can break the performance and reliability NFRs on demo day.
