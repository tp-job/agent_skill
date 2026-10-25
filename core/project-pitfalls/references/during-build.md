# C · During build

Run at each phase close, before merging to main, and whenever something is slow, flaky
or out of sync. Four groups: performance, security, tests, docs.

Each item: **check** — **prove it** — *what happened when it was skipped*.

---

## Performance

### C1 · Measure where the time goes before changing anything

- **Check:** time a no-database endpoint and a database endpoint; turn on the ORM query
  log with durations (never with parameter values — they can hold emails and tokens).
- **Prove it:** a before/after table per endpoint for every change.
- *Seen:* the health endpoint answered in ~5 ms while database endpoints took 0.5–2 s.
  That one comparison ruled out the server and pointed at round trips.

### C2 · Count round trips, not rows

- **Check:** the cost is the number of sequential trips to the database.
- **Prove it:** 5,000 rows in one INSERT took 320 ms; 20 rows as separate INSERTs took
  1,080 ms (Singapore, ~50 ms per trip). Bulk writes (`createMany`, one upsert) and
  parallel reads win.

### C3 · Read-only batches run in parallel, not in a transaction

- **Check (Prisma 6):** `prisma.$transaction([a, b, c])` runs its queries one after
  another on one connection and adds BEGIN/COMMIT. For reads that need no atomicity,
  `Promise.all([a, b, c])` runs them concurrently.
- **Prove it:** query log shows overlapping timestamps; the endpoint time drops.
- *Seen:* a grading page made ~12 sequential trips; after the change its 10 queries
  finished together in ~270 ms. Writes stay in transactions.

### C4 · One request per screen, not one per row

- **Check:** a page that loads a list must not fetch details per item, and three widgets
  must not each reload the same base data.
- **Prove it:** count requests in the network panel while opening the page.
- *Seen:* a results page made one request per student (40 requests, ~400 queries for a
  class of 40) and burned the rate-limit quota; an overview made three calls that each
  reloaded the whole course. One class endpoint and one summary endpoint replaced them.

### C5 · Rate limit keyed sensibly

- **Check:** a per-IP limit puts everyone behind one campus NAT on one quota.
- **Prove it:** state the key and the limit; consider per-user or per-token limits for
  production.

### C6 · Measure page speed on a production build

- **Check:** Lighthouse on a dev server measures the bundler's module loading, not the app.
- **Prove it:** run it on the production preview.
- *Seen:* score 40 on dev, 71 on the production build of the same app.

### C7 · Duplicate calls from React StrictMode

- **Check:** in development, effects run twice; a session-resume call must be idempotent
  (one in-flight promise).
- **Prove it:** the network panel shows the call once after a reload.

---

## Security

### C8 · One access gate, enforced at boot

- **Check:** every route declares its access rule (`public`, `authenticated`, or a
  capability); the server refuses to start when a route declares nothing.
- **Prove it:** add a route with no declaration — boot fails.
- *Why:* a forgotten permission check becomes a startup error instead of an open endpoint.

### C9 · "Not yours" looks exactly like "not found"

- **Check:** a resource the caller cannot see returns the same 404 body as a missing one
  and as a malformed id. A 403 confirms the id exists.
- **Prove it:** an isolation test calls every route with another owner's ids and expects
  404 for all of them; the route list is read from the app, not typed by hand.

### C10 · Token types are distinct; roles come from the live record

- **Check:** access and refresh tokens carry a `typ` claim and the middleware accepts
  only `access`; the role and active status are re-read from the database per request.
- *Seen:* both tokens were signed with the same secret and payload, so a 7-day refresh
  token worked as a 15-minute access token. Old tokens without `typ` are rejected —
  everyone signs in once.

### C11 · Errors do not leak data

- **Check:** the error log holds the error name and code, not the ORM message (it quotes
  row values); auth and cookie headers are redacted; framework 4xx errors keep their
  status instead of becoming 500.

### C12 · CORS allows the methods the app uses

- **Check (@fastify/cors):** the default allows GET, HEAD and POST only.
- *Seen:* every PATCH, PUT and DELETE from the browser was refused. Only an end-to-end
  test in a real browser caught it.

### C13 · Third-party sign-in verified on the server

- **Check:** the client only forwards the provider's ID token; the server verifies
  signature, `iss`, `aud` (your client id), expiry and `email_verified`. Nothing else the
  client sends about identity is trusted.
- **Bootstrap:** the first administrator comes from an env list (`ADMIN_EMAILS`), never a
  personal email in the repository. Removing an address from the list does not demote an
  existing admin — change the role in the database.

### C14 · Dependencies scanned in CI

- **Check:** dependency review, static analysis (CodeQL), secret scanning, image scanning.
- *Seen:* turning these on revealed 10 HIGH advisories in production dependencies and an
  outdated OpenSSL in the web server image — already on main, just invisible.

---

## Tests

### C15 · Database tests do not share state in parallel

- **Check:** test files that write to one shared database run serially, or each uses its
  own data.
- *Seen:* parallel files deleted each other's test users — 401, 404 and `undefined`
  responses that looked like application bugs.

### C16 · Test settings do not trip production guards

- **Check:** a test that calls every route in a burst hits the rate limiter; set a high
  limit for tests unless the test is about the limiter.
- *Seen:* 429 instead of the expected 404.

### C17 · Timeouts sized for the real database

- **Check (Prisma 6):** interactive transactions default to 5 s; a remote database at
  0.2–1 s per query needs more (error P2028).

### C18 · Known gaps kept as expected failures

- **Check:** a contract test that cannot pass yet is marked expected-to-fail (`it.fails`)
  so it turns red the day the gap closes and gets moved into the normal suite.

### C19 · Each test proven able to fail

- **Check:** break the code under test and watch the test go red. Mutation testing does
  this systematically.
- *Seen:* 9 surviving mutants in the JWT module — nothing checked the algorithm, `sub`
  or the role claim.

---

## Docs and diagrams

### C20 · Code is the source of truth; docs change in the same commit

- **Check:** when a doc disagrees with code, fix the doc in the same change.
- **Prove it:** a script compares the API design file with the registered routes,
  capabilities and schema, and runs in CI.
- *Seen:* one document gave three different endpoint counts (57 / 58 / 68).

### C21 · Generated files regenerated, never hand-edited

- **Check:** close every editor tab of a generated diagram before pulling; regenerate
  from the script after a merge conflict instead of resolving the XML by hand.
- *Seen:* a stale draw.io tab saved an old diagram over the generated one, bringing back
  an arrow the rules forbid.

### C22 · Prototype ahead of the app is tracked, not copied

- **Check:** a document says what each page takes from the prototype and what it must
  never copy (client-side calculation, demo passwords).
- **Prove it:** the page calculates nothing; every number comes from the server.

---

## Exit for checkpoint C

A before/after table for every performance change · isolation test green · every new
test seen failing once · docs and diagrams regenerated and checked · any item left open
listed as blocking or as a deliberate deferral with its owner.
