# Case study — CMAS (course learning-outcome tracking)

The evidence behind the checkpoints. A student team built a web app that tracks course
learning outcomes: define outcomes, map assessments, import scores from Excel, show
attainment and at-risk students. Documentation doubled as thesis material.

- **Period:** July – October 2026, ~112 commits
- **Stack:** React 19 + Vite 7 + Tailwind 4 · Fastify 5 + Zod 4 · Prisma 6 · PostgreSQL on
  Supabase · npm workspaces · GitHub Actions · Windows dev machines
- **Sources:** git history, progress reports, planning documents, and six agent sessions
  read in full; other sessions sampled. Numbers are as recorded at the time, not
  re-measured for this file.

---

## Timeline of what went wrong

| When | Stage | Problem | Cost | Fix |
| --- | --- | --- | --- | --- |
| Jul | Setup | Clean clone did not run: missing seed file, stale README, lint scanned the bundle (1,159 errors), tests in the prod image, CRLF churn on 113 files, a critical advisory in a test dependency | Every new contributor blocked | One setup command, `.gitattributes`, lint ignores, test exclusion, dependency bump |
| Aug | Before design | Schema modelled many institutions; objective said one faculty | Inserted task, ~1 sprint, every document revised | Cut to 13 tables, course is the only data boundary |
| Aug | Before design | "Weight" readable two ways, ~20 points apart; "at risk" undefined with no scores | Calculation tests blocked | Escalated with a comparison table; rule: no code until rules are signed |
| Sep–Oct | Design | Use-case numbers disagreed between files; UML promised a delete the schema forbade; duplicate ER PDFs; stale editor tab overwrote a generated DFD | Diagrams not presentable; rework | One official file per type; generators; content-based checker |
| Sep 24 – Oct 15 | CI | Node 20 pin vs a dependency needing 22+ — CI failed at install | Three weeks of fake green | Node 24 everywhere |
| Oct | Security | Refresh token accepted as access token | 7-day token as 15-minute token | `typ` claim, access-only middleware |
| Oct | Security | Permission checks per route, easy to forget | Open endpoint risk | Boot refuses an undeclared route; 404 for not-yours |
| Oct | DB | Migration with a `%` placeholder and no argument | Deploy stopped at the previous migration | Fixed the never-applied migration, documented why editing was safe |
| Oct | Build | CORS default blocked PATCH/PUT/DELETE | Every edit failed in the browser | Allowed methods; E2E test |
| Oct | Tests | Parallel DB test files deleted each other's users; burst tripped the rate limiter; 5 s transaction timeout | Flaky CI that looked like app bugs | Serial DB tests, high test rate limit, 30 s timeout |
| Oct | Performance | Tokyo region (~250 ms/trip), transaction pooler (4 trips/query), sequential read batches, one request per student, IPv6 fallback on localhost (~216 ms) | Pages took ~6 s | Singapore (~50 ms), session pooler, `Promise.all`, class and summary endpoints, listen on `::` — the grading page went from ~6 s to ~2.4 s for data |
| Oct | Hosting | RLS off on every table; public key could read users and tokens | Data exposed through the hosted API | Lock-down migration (RLS on, no grants) |
| Oct | CI hardening | 14 workflow findings (7 high), no branch protection, unenforced coverage, 10 HIGH dependency advisories | Invisible risk on main | SHA pins, permissions, required gate, scanners |
| Throughout | Team | Generic commit titles, ~40 uncommitted files across features, long agent sessions hitting context and usage limits | Hard to review, revert or resume | One-concern commits, issues for teammates, session per phase |

---

## What worked

| Practice | Where it paid off |
| --- | --- |
| Measure first (no-DB vs DB endpoint, query log) | Turned "the query is heavy" into four separate, fixable causes |
| Server refuses to boot on an undeclared route | Forgotten permission checks cannot ship |
| Checkers that fail, proven by breaking them | Diagram drift, permission-matrix drift, missing auth events all caught |
| Checkers run the real code, not a copy | A copied function would have passed while the real one was broken |
| Expected-to-fail tests for known gaps | 20 routes tracked until the resolver existed |
| Generators for diagrams | ER, DFD, use case regenerate from one source |
| Marking drafts as superseded instead of renumbering someone else's work | Decision visible in the document people read |
| Worktree for unrelated work | CI hardening done without touching uncommitted feature work |
| Old database kept until the new one was verified | No data lost during the region move |
| Progress reports written as question → answer | Open questions and what they block stayed visible |
| Permission questions answered by counting the matrix | Showed that merging roles moves 9 of 18 capabilities |
| PRs that say what was not tested | Reviewers knew where to look |
