# B · Day zero

Run when the repository is being set up, or as soon as someone cannot run the project
from a clean clone. Gaps here silently invalidate every later measurement.

Each item: **check** — **prove it** — *what happened when it was skipped*.

---

## B1 · A clean clone runs with one command

- **Check:** one idempotent setup command creates env files from examples, generates
  secrets, installs, and generates clients (`npm run setup` in a Node workspace).
- **Prove it:** in a fresh directory: clone → setup → dev → open the app. Run setup a
  second time; nothing is overwritten.
- *Skipped:* the seed script pointed at a file that did not exist; the README linked a
  missing doc and named a framework the server no longer used.

## B2 · Line endings, editor settings and runtime version pinned at commit one

- **Check:** `.gitattributes`, `.editorconfig`, and a runtime pin (`.nvmrc`) exist.
- **Prove it:** `git diff --stat` after a fresh checkout on Windows and on macOS/Linux is
  empty.
- *Skipped:* CRLF/LF churn showed 113 files as changed.

## B3 · One runtime major everywhere

- **Check:** the runtime major in `.nvmrc`, `package.json` `engines`, the setup script's
  version check, every CI job and every Dockerfile is the same.
- **Prove it:** grep all five places in one command and compare.
- *Skipped:* `.nvmrc` pinned Node 20 while a dependency required 22+. CI failed at
  `npm ci` for three weeks; no lint, test or build result in that window was real.

## B4 · CI is required, and each gate has been seen failing

- **Check:** the main branch is protected; one aggregate CI check is required; a red PR
  cannot merge.
- **Prove it:** push directly to main — refused. On a throwaway branch, break one thing
  per gate (lint error, failing test, schema change with no migration, coverage below
  threshold) — each turns red. Delete the branch.
- *Skipped:* PRs with red CI could merge; a coverage threshold was configured but CI ran
  `test`, not `test:coverage`, so it was never enforced.

## B5 · Workflow hygiene (GitHub Actions)

- **Check:** actions pinned by commit SHA, explicit minimal `permissions`, a timeout on
  every job, dependency updates automated, secret scanning on.
- **Prove it:** a workflow linter (zizmor) reports zero findings.
- *Skipped:* 14 findings in the existing workflows, 7 high.

## B6 · Build artefacts exclude what they should

- **Check:** lint ignores build output; test files are excluded from production builds;
  the start script does not hard-code a local env file.
- **Prove it:** build, then lint — no errors from minified output; list the production
  image — no `*.test.*`; start the container with env from the platform — it boots.
- *Skipped:* linting after a build reported 1,159 errors from the bundle; tests shipped in
  the production image; `--env-file=.env` crashed the container.

## B7 · Secrets never enter an image or a committed file

- **Check:** `.dockerignore` excludes `**/.env*` at every depth; env files hold only the
  current values (no commented-out old URLs with passwords); connector configs that are
  committed default to read-only.
- **Prove it:** build the image and list its files; grep the repo for connection strings.
- *Skipped:* a root-only `.env` pattern let `app/server/.env` (JWT secret, DB password)
  into the builder stage; an old database URL with its password stayed in the file as a
  comment; removing `read_only=true` from a committed MCP config would give every
  teammate a write-capable connector.

## B8 · Database region, pooler and latency measured in week one

- **Check:** the database sits in the region nearest the users and developers; the
  connection mode suits the ORM.
- **Prove it:** log per-query time; time `SELECT 1` twenty times; compare a no-DB
  endpoint with a DB endpoint.
- *Skipped (Supabase + Prisma 6):* Tokyo from Thailand was ~250 ms per round trip;
  Singapore was ~50 ms. The transaction pooler (port 6543, `pgbouncer=true`) wrapped
  every query in BEGIN / DEALLOCATE ALL / query / COMMIT — four round trips. The session
  pooler (port 5432) does not. A Supabase project cannot change region; moving means a
  new project and a data copy.

## B9 · Hosted database locked down (Supabase)

- **Check:** if the app talks to the database only through its own server, the hosted
  data API must expose nothing: RLS on for every table, no grants for `anon` /
  `authenticated`, and that applied by a migration so new tables are covered.
- **Prove it:** call the REST endpoint with the public key — denied; the provider's
  security advisor shows no RLS errors.
- *Skipped:* every table had RLS off and `anon` could read the user and refresh-token
  tables. An old project left behind with real data stayed exposed until deleted by hand.

## B10 · Free-tier limits written down before testing with real users

- **Check:** storage cap, auto-pause on inactivity, backups.
- **Prove it:** a capacity estimate from a measured sample; a backup schedule; someone
  owns keeping the project awake during breaks.
- *Example (Supabase Free):* 500 MB, paused after 7 idle days, no automatic backups,
  `VACUUM` only through the direct port. A three-month trial was estimated at 50–310 MB.

## B11 · Local dev environment quirks documented (Windows)

- **Check:** the README lists what breaks on a teammate's machine.
- *Seen:* `prisma generate` fails with `EPERM` while the dev server holds the engine DLL
  — stop the server first; `EADDRINUSE` from a stale dev server; `localhost` resolving to
  IPv6 first while the server listens on IPv4 only (~216 ms per request until the server
  listened on `::`); env changes not picked up by `tsx watch` until a restart.

---

## Exit for checkpoint B

Fresh clone runs · one runtime major · CI required and every gate seen red once ·
workflow lint clean · no secret in images or files · database latency measured and the
region/pooler chosen from the number · hosted data API locked.
