# Category 13 — Localization and cultural (Thai focus)

The source is the "cultural" section of the Volere template, together with ISO/IEC 25010:2023 adaptability. The examples here are Thai, and the checks carry over to any locale.

## NFR catalogue

| ID | Statement | Must | Method |
| --- | --- | --- | --- |
| LC-01 | UI language | every user-facing string comes from one message catalogue; 0 hard-coded strings in components | Inspection (grep or an i18n lint rule) |
| LC-02 | Error language | every error the user can reach is in Thai, including validation, network and import errors, not only the happy-path ones | Test (trigger each error class) |
| LC-03 | Calendar | dates show in the agreed calendar (พ.ศ. = ค.ศ. + 543) consistently; storage stays ISO 8601 in Gregorian/UTC | Test |
| LC-04 | Academic year and term | displayed in local convention (e.g. ปีการศึกษา 2569 ภาคเรียนที่ 1) | Inspection |
| LC-05 | Time zone | times display in Asia/Bangkok (UTC+7) and are stored in UTC; no midnight off-by-one at day boundaries | Test (create a record at 23:30 and at 00:30 local time) |
| LC-06 | Numbers | decimal and thousands separators follow the locale; Thai digits only if the users ask for them | Inspection |
| LC-07 | Line breaking | Thai text wraps at word boundaries, not mid-word, in tables, buttons and chart labels | Inspection (narrow viewport) |
| LC-08 | Font | the chosen font covers Thai, including tone marks and vowels above and below the line, with no clipping in inputs or tight line-heights | Inspection |
| LC-09 | Sorting | Thai names sort in dictionary order (`Intl.Collator('th')`), not by code point | Test |
| LC-10 | Imported text | Thai in imported CSV/XLSX survives without garbling (see the encoding checks under compatibility) | Test |

## How-to notes

- **Buddhist Era dates:** `new Intl.DateTimeFormat('th-TH', { dateStyle: 'long' })` formats in the Buddhist calendar by default. Use `'th-TH-u-ca-gregory'` for Gregorian. Never store a converted year.
- **Word breaking:** browsers break Thai using dictionaries, but `word-break: break-all` turns that off and splits words. Check for it in your CSS and remove it. `overflow-wrap: anywhere` is a safer fallback for long codes.
- **Line-height:** Thai stacks marks above and below the baseline. A `line-height` under about 1.5 clips them in many fonts.
- **Sorting:** `['ไก่','กา','ขวด'].sort()` gives code-point order. `.sort(new Intl.Collator('th').compare)` gives dictionary order.

## BAD / BETTER

BAD: "The system supports Thai."
BETTER: LC-01 + LC-02 + LC-03 + LC-07, each with its own pass condition.
