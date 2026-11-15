# Category 6 — Compatibility

ISO/IEC 25010:2023 sub-characteristics: **co-existence** (sharing an environment with other products without harm) and **interoperability** (exchanging and using information with other systems).

## Build the matrix from real users

Choose browsers and viewports from analytics or a short user survey, not from a generic list. Every cell must name a version.

| | 1366 × 768 | 1920 × 1080 | 390 × 844 (phone) |
| --- | --- | --- | --- |
| Chrome (latest) | core tasks | core tasks | view-only tasks |
| Edge (latest) | core tasks | core tasks | — |
| Firefox (latest) | core tasks | — | — |
| Safari (latest, macOS/iOS) | core tasks | — | view-only tasks |

Mark the cells you do not support as "not supported", so that nobody tests them or files bugs against them.

## NFR catalogue

| ID | Statement | Must | Method |
| --- | --- | --- | --- |
| CP-01 | Browser matrix | every core task passes in every supported cell | Test (Playwright projects for chromium, firefox, webkit) |
| CP-02 | Spreadsheet import | `.xlsx` files saved by Excel, Google Sheets and LibreOffice all import identically | Test (same data, three files) |
| CP-03 | CSV encoding | UTF-8 with BOM, UTF-8 without BOM, and (if any users run older Excel) TIS-620/Windows-874 handled or rejected with a message | Test |
| CP-04 | Export round-trip | export, then re-import, gives the same data | Test |
| CP-05 | API contract | responses match the published OpenAPI/JSON schema | Test (schema validation in CI) |
| CP-06 | Identity provider | sign-in works with the organisation's real accounts (e.g. a Google Workspace domain), not only personal test accounts | Demonstration |
| CP-07 | Co-existence | the app does not break when common extensions run (ad blockers, password managers, translation) | Test (manual, one pass) |

## Pitfalls

- **Safari date and number inputs.** They render and validate differently, so test the actual input controls in Safari, not only the page layout.
- **Excel's "CSV UTF-8" versus plain "CSV".** Plain CSV on a Thai Windows locale is saved as Windows-874, so Thai text arrives garbled unless the importer detects the encoding.
- **Dates in spreadsheets.** Excel stores dates as serial numbers, so a parser has to convert them deliberately rather than reading them as strings.
