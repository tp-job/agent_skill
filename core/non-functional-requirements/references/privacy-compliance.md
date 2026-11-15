# Category 11 — Privacy and compliance

This file turns data-protection duties into requirements that can be verified. It is not legal advice. When the stakes are real, have the organisation's data protection officer confirm the lawful basis and retention periods.

## Which law

| Jurisdiction | Law | Notes |
| --- | --- | --- |
| Thailand | Personal Data Protection Act B.E. 2562 (2019), "PDPA" | fully in force from 1 June 2022; regulator: the PDPC (สำนักงานคณะกรรมการคุ้มครองข้อมูลส่วนบุคคล) |
| EU / EEA data subjects | GDPR (Regulation (EU) 2016/679) | applies to EU residents' data regardless of where the server is |

Names, student or employee IDs, email addresses, grades and photos all count as personal data. Health, religion and biometric data are sensitive data and carry stricter conditions.

## NFR catalogue

| ID | Statement | Must | Method |
| --- | --- | --- | --- |
| PR-01 | No personal data in application logs | after running the full test suite and a manual session, a search of the logs finds no names, ID patterns, emails or score values | Inspection (grep the logs for the regex of ID formats and email) |
| PR-02 | Data minimisation | every stored personal field has a stated purpose in a data inventory; fields without a purpose are not collected | Inspection |
| PR-03 | Access limited by role | covered by the security access matrix (SC-01) | Test |
| PR-04 | Retention | each data class has a retention period, and expired data is deleted or anonymised by a scheduled job | Demonstration |
| PR-05 | Data-subject requests | access, correction and deletion requests can be fulfilled within the legal deadline using a documented procedure | Demonstration |
| PR-06 | Privacy notice | users see what is collected, why, for how long, and whom to contact, before data is collected | Inspection |
| PR-07 | Breach readiness | a breach procedure exists, including notifying the regulator within the statutory window (72 hours under both PDPA and GDPR, where notification is required) | Inspection |
| PR-08 | Exports protected | exported files containing personal data are only available to authorised roles and are not cached publicly | Test |
| PR-09 | Test data | non-production environments use synthetic or anonymised data | Inspection |

## Logging without personal data

BAD: `logger.info(\`Score saved for ${student.name} (${student.id}): ${score}\`)`
BETTER: `logger.info({ event: 'score.saved', courseId, recordId, actorId })`, using internal opaque IDs only. Add a redaction list to the logger configuration, such as pino `redact` or a structlog processor, as a safety net.

## Sector rules

Add the rules that bind the organisation and give each one an ID. Typical examples are a university's data policy, a hospital's health-record rules, and a government cloud standard. A rule that only exists as "we comply with policy X" cannot be verified until its clauses are listed.
