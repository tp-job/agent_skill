# NFR specification — <system name>

Version: <x.y> · Date: <YYYY-MM-DD> · Owner: <name or role> · Quality model: ISO/IEC 25010:2023

## 1. Context

<One paragraph: what the system does, user groups and their counts, typical and maximum data volume, hosting, and the mode (engineering or thesis).>

## 2. Measurement conditions

Every performance and capacity NFR below assumes these conditions unless its row says otherwise.

- Dataset: <typical> / <maximum>
- Environment: <hosting tier, region>; client <browser + version, device class>
- Network: <unthrottled desktop | named throttling profile>
- Runs: n ≥ 30; report median, p95, max
- Cache: warm; cold start reported separately

## 3. Applicability

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

## 4. Requirements

`scripts/nfr_lint.py` reads this table. Keep the header row exactly as written. Every row needs Scale, Meter, Condition, Must and Source. In the Source column, write "project target: <reason>" when no standard backs the number.

| ID | Category | Statement | Scale | Meter | Condition | Must | Plan | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PF-01 | 1 Performance | | | | §2 | | | |
| AX-01 | 5 Accessibility | | | | | | | |
| UX-04 | 4 Interaction | | | | | | | |
| DI-01 | 10 Data integrity | | | | | | | |

## 5. Conflicts and trade-offs

| Between | Decision | Why |
| --- | --- | --- |
| | | |
