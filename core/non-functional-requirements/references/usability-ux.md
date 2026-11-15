# Category 4 — Interaction capability (usability and UX)

## Contents

- Three dimensions, three kinds of metric
- NFR catalogue
- SUS: administer, score, interpret
- Task-based test protocol
- Heuristic evaluation with severity
- Expert Likert forms vs user measurement

---

## Three dimensions, three kinds of metric

ISO 9241-11:2018 defines usability as the extent to which specified users achieve specified goals with **effectiveness**, **efficiency** and **satisfaction** in a specified context of use. Each dimension needs its own metric. A satisfaction questionnaire on its own covers only one of the three.

| Dimension | Metric | How |
| --- | --- | --- |
| Effectiveness | task success rate; errors per task | observe users doing defined tasks unaided |
| Efficiency | time on task | stopwatch or screen recording |
| Satisfaction | SUS (whole system); SEQ (per task) | questionnaire after the tasks |

## NFR catalogue

| ID | Metric | Must (typical) | Source of the number |
| --- | --- | --- | --- |
| UX-01 | Task success rate per core task | ≥ 80% | project target. Sauro and Lewis (2016) report about 78% as an average completion rate across studies |
| UX-02 | Errors per task | mean ≤ 1 | project target |
| UX-03 | Time on task | ≤ 2 × an expert's time on the same task | project target |
| UX-04 | SUS mean | ≥ 68 (average); aim ≥ 71.4 ("good") | Bangor, Kortum and Miller (2008, 2009); Sauro and Lewis (2016) |
| UX-05 | SEQ per task (7-point) | ≥ 5.5 | Sauro and Dumas (2009) |
| UX-06 | Heuristic evaluation | no unresolved severity 3–4 issue at release | Nielsen (1994a, 1994b) |
| UX-07 | Error messages | every message gives cause and remedy in the user's language | Nielsen (1994a) heuristic 9; WCAG 3.3.3 |
| UX-08 | Participants | ≥ 5 real target users per round, distinct from the expert panel | Nielsen and Landauer (1993) |

## SUS: administer, score, interpret

Administer SUS **after** the user has finished all tasks. It has 10 statements, each answered on a 1–5 scale from strongly disagree to strongly agree. Use Brooke's original wording, or a validated translation if one exists for the users' language. A home-made translation should be piloted and reported as such.

Scoring (Brooke, 1996):

- odd items (1, 3, 5, 7, 9): contribution = answer − 1
- even items (2, 4, 6, 8, 10): contribution = 5 − answer
- SUS = sum of contributions × 2.5, giving a range of 0–100

Interpretation:

| SUS | Adjective (Bangor et al., 2009) | Note |
| --- | --- | --- |
| ≥ 85.5 | Excellent | |
| ≥ 71.4 | Good | |
| ≥ 68 | — | average across about 500 studies (Sauro and Lewis, 2016) |
| ≥ 50.9 | OK | |
| ≥ 35.7 | Poor | |
| < 35.7 | Awful / Worst imaginable | |

These values are the mean SUS score of the responses that chose each adjective in Bangor et al. (2009). Using them as cut-offs is a convention, so describe them as approximate. Report the mean, SD and n. `scripts/sus_score.py` computes the per-respondent scores and the summary.

SUS is not a percentage. A score of 68 is about the 50th percentile of systems, not "68% usable".

## Task-based test protocol

1. **Write 5–6 core tasks as goals, not instructions.** "Record this student's midterm score" is a goal. "Click Scores, then Edit" is an instruction and gives the answer away.
2. **Define success for each task in advance**, for example "score saved and visible in the table".
3. **Recruit at least 5 target users** who have not seen the system.
4. **Run each session the same way:** think-aloud, no help given, and a time cap per task of about 3× the expert's time.
5. **Record** success (yes, partial or no), time, errors, and quotes.
6. **Ask SEQ** ("Overall, how difficult or easy was this task?", 1–7) after each task, and **SUS** at the end.
7. **Report** each task's success rate with its confidence interval. With 5 users, an 80% result could easily be 40–100%, so say so.

## Heuristic evaluation with severity

Have three evaluators review the interface **independently** against Nielsen's 10 heuristics before merging their findings. Rate each issue for severity on a 0–4 scale (Nielsen, 1994b):

| Severity | Meaning |
| --- | --- |
| 0 | not a usability problem |
| 1 | cosmetic; fix if time allows |
| 2 | minor; low priority |
| 3 | major; important to fix |
| 4 | catastrophe; must fix before release |

Severity combines frequency, impact and persistence.

## Expert Likert forms vs user measurement

A 5-point Likert form filled in by three experts, with IOC validation, is common in Thai theses. It is a valid **expert quality assessment**, but it does not measure whether users can complete tasks.

BAD: "Usability: experts rated 4.33 / 5, therefore the system is easy to use."
BETTER: "Experts rated usability 4.33 / 5 (n = 3). Five instructors completed 26 of 30 tasks (87%) with a mean SUS of 74.5 ('good')."

Keep both kinds of evidence, and label each one for what it measures.
