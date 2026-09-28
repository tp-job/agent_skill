# Plan — Master Design and Master Agent on the Promethean-Parthenon foundation

Status: **All five phases complete (2026-09-28)** · follow-ups listed in §6
Branch: `consolidate-skills` — the owner chose to keep all phases on the existing branch (one commit per phase instead of one branch per phase)

---

## 1. Target (Task)

| Question | Answer |
| --- | --- |
| What is being built? | Two skills — `master-design` (architecture, art direction, creativity, drafting) and `master-agent` (inventory, MCP triage, routing, delegation, trust boundaries, MCP server building) — each applying Parthenon's Role · Task · Format doctrine to its domain, and routed from `promethean-parthenon` |
| For whom? | An AI coding agent in this library's install, and the human directing it |
| Under what limits? | CLAUDE.md hub-and-spoke rule (one aggregator only); aggregator description ≤ 1,536 chars (was 1,461 before this work); every skill folder usable when copied out alone; all three checks clean |
| Proven how? | `build-index`, `build-bundles && check-bundles`, `lint-skills` exit 0 · trigger evals in Phase 2 route ≥ 9/10 intended prompts and ≤ 1/10 adjacent prompts to each skill |

---

## 2. Architecture

```
                         promethean-parthenon  (the one aggregator)
                         Role · Task · Format doctrine + router
                          │ links + bundles (unchanged)        │ names in prose (new)
          ┌───────────────┴──────────────┐          ┌──────────┴───────────┐
   10 core spokes (bundled/)             │          master-design          master-agent
   senior-leadership-advisor, ...        │          (active, standalone)   (active, standalone)
                                         │           │ prose hand-offs      │ prose hand-offs
                                         │           ▼                      ▼
                                         │   frontend-design,        MCP servers, skills,
                                         │   google-design-system,   subagents, models
                                         │   css-architecture,       in the running session
                                         │   threejs-3d, Figma/
                                         │   Canva/Blender MCP
```

### Decision: standalone skills, not new aggregators or new spokes

| Option | Verdict | Why |
| --- | --- | --- |
| **A. Two active standalone skills, named in Parthenon's routing (chosen)** | ✅ | Complies with CLAUDE.md as written; no bundle growth; each skill carries its own trigger description |
| B. Add both to Parthenon's `CLOSURE` | ❌ | Deactivates them standalone; their triggers must then fit in Parthenon's description, which had 75 chars left |
| C. Make each a second aggregator linking to the design / AI skills | ❌ for now | Breaks the "exactly one aggregator" rule; `build-bundles.py` / `check-bundles.py` assume a single `HOST`. Revisit in Phase 5 only if the rule is deliberately changed |

**Premise this rests on:** the extra ~2,300 chars of always-loaded description (two new active skills) is acceptable. **Changes the decision if:** the active set's total description budget becomes a measured problem — then Option B with a trimmed Parthenon description.

**Interpretation note:** "architecture" in Master Design means *design* architecture (IA, flows, token tiers). Software architecture stays with `knowledge-base`.

---

## 3. Phases

| # | Phase | Deliverables | Gate (proof) | Status |
| --- | --- | --- | --- | --- |
| 1 | **Foundation** | `master-design/` (SKILL.md + 4 references), `master-agent/` (SKILL.md + 5 references), Parthenon routing rows + v3.1.0, regenerated index/plugin.json | all three checks exit 0 | ✅ done — `ef87a87` |
| 2 | **Trigger evals** | 10 should-trigger + 10 near-miss prompts per skill (EN + TH); run manually through the skill-creator eval loop; tune descriptions | ≥ 9/10 hits, ≤ 1/10 false fires, no regression in Parthenon RC-06 (skills that never fire) | ✅ done — `49abe48` |
| 3 | **Design depth** | worked example end-to-end (target → IA → thesis → 3 concepts + scorecard → HTML draft → design record) as `master-design/assets/example-design-record.md`; Figma/Canva/Blender drafting checklists validated against the live servers | one real job run through all four stages; record rebuildable by a fresh session | ✅ done — `6c99932` |
| 4 | **Agent operations** | `master-agent/scripts/inventory.py` — reads `.mcp.json` + settings, emits a capability-record skeleton; `master-agent/assets/capability-record.md` template; MCP server test checklist exercised against one real server | script runs clean on this repo; one server proven with read, write and refused-call rows | ✅ done — `c07e3f8` |
| 5 | **Review & decide** | measure description budget of the active set; decide whether to keep Option A, fold into `CLOSURE` (B), or change the rule for sub-aggregators (C); `github-report` write-up of phases 1–4 | a written decision with premise and expiry, signed off by the owner | ✅ done — this file |

Phases 2 and 3/4 are independent — 3 and 4 can run in parallel branches once 2 has fixed the descriptions.

---

## 4. Risks

| Risk | Signal | Mitigation |
| --- | --- | --- |
| Trigger overlap with `frontend-design` / `google-design-system` | Phase 2 near-miss fires | tighten "Not for" clauses; keep master-design at the *whole-job* level |
| master-agent overlaps with the harness's own tool guidance | advice duplicates what the client already enforces | keep it to decisions (route, delegate, record), not restating client rules |
| MCP/Claude Code specifics go stale | a flag or state name no longer matches | version note at the top of each MCP file; re-verify on each library refresh |
| Description budget creep | active set grows past what a session tolerates | Phase 5 measurement, Option B as fallback |

---

## 5. Open questions (owner: repo maintainer)

1. Keep both as active standalone skills (default), or fold them behind Parthenon now? — default: keep standalone until Phase 5 data.
2. Should Master Design carry an opinionated default art direction for this vault's own artifacts? — default: no; the thesis is written per job.
3. Is changing CLAUDE.md to allow sub-aggregators on the table at all? — default: no.

---

## 6. Results

### Phase 2 — trigger evals

Blind run: a subagent saw only the 21 active skill descriptions and 40 shuffled prompts, with no labels. Cases are in `master-design/assets/trigger-evals.json` and `master-agent/assets/trigger-evals.json`.

| Skill | Should trigger → hit | Near-miss → false fire | Gate |
| --- | --- | --- | --- |
| master-design | 10 / 10 | 0 / 10 | ✅ (≥ 9, ≤ 1) |
| master-agent | 10 / 10 | 0 / 10 | ✅ |

**Watch list, not failures:** master-agent was the *runner-up* on two drift / "which skill" prompts (correctly routed to promethean-parthenon), and master-design was runner-up on a one-button Thai prompt (correctly routed to frontend-design). Descriptions left unchanged: the gate passed with margin, and editing without a failing case would be tuning to taste. **Caveat:** the grader is a model reading descriptions, which approximates the real skill selector but is not the same thing.

### Phase 3 — design depth

A clinic "Today" screen taken through all four stages. Observed checks: 12 contrast pairs computed (lowest 5.23:1, all ≥ 4.5:1 AA); 44px touch targets measured; no horizontal scroll at 375×667 or 1440×900; the four-slots-visible criterion passes (last row ends at y=584); dark tokens resolve correctly when forced. **Not checked:** dark mode via the OS setting, hallway test.

### Phase 4 — agent operations

`inventory.py` ran clean on this repo (it correctly reports no file-configured servers). A fixture with secrets in env, headers, the URL query and args leaked **0** of them. One real server (bioRxiv, public, read-only) passed the read and teaching-error checks. **Not proven:** write and refusal behaviour — no write-capable server was tested without the owner's yes. Dropped from the plan: a separate `capability-record.md` template, because the script's output *is* the template and a second copy would drift.

### Phase 5 — decision

| Measure | Value |
| --- | --- |
| Active descriptions, total | 17,035 chars across 21 skills (~4.3k tokens every session) |
| Added by the two new skills | 2,640 chars (~660 tokens, +18%) |
| promethean-parthenon description | 1,484 / 1,536 — 52 chars of headroom |

**Decision: keep Option A (standalone, named in Parthenon's routing).** Option B would need ~2,600 characters of triggers inside a description with 52 to spare, which means deleting existing routing to make room. Option C stays off the table: nothing here needs a second aggregator.
**Premise:** ~660 tokens per session is an acceptable cost for two domains that previously had no skill.
**Expires when:** the active set passes ~25,000 characters, or a trigger eval shows either skill mis-firing on more than 1 in 10 near-misses. Either one reopens B.

### Testing pass (after Phase 5)

Everything that could be tested without a human or a real account was tested; each defect found was fixed and the fix re-tested.

| Area | Test | Result |
| --- | --- | --- |
| CLI claims in master-agent | compared against `claude mcp --help` (Claude Code 2.1.278) | `--transport`, `-e`, `-H`, `local / project / user` scopes all match |
| Write + refusal | local sandbox server driven over real stdio by the SDK client | 10 / 10 checks pass (`verify_sandbox.py`) |
| `${VAR}` and `${VAR:-default}` | unset variables under `claude mcp list` | plain form warns by name; `:-default` form does not — both as documented |
| `inventory.py` | 14 unit tests, then 8 deliberate regressions | 14 / 14 pass; all 8 regressions caught |
| Dark mode via the OS setting | localhost preview, `prefers-color-scheme: dark` emulated | tokens resolve correctly; light override guard works; focus ring visible on keyboard Tab |
| All three repo checks | `build-index`, `build-bundles && check-bundles`, `lint-skills` | clean |

**Defects found and fixed**

| # | Where | Defect | Fix |
| --- | --- | --- | --- |
| 1 | master-agent triage | no **Pending approval** state — project `.mcp.json` servers start there and never connect until approved | added to SKILL.md triage and mcp-lifecycle §2a |
| 2 | mcp-lifecycle | no warning that `claude mcp add --scope project -e K=v` writes the secret into the committed `.mcp.json` | documented as "the `-e` trap", with BAD/BETTER |
| 3 | inventory.py | never read approvals stored in `~/.claude.json`; ignored `enableAllProjectMcpServers` | reads all three sources |
| 4 | inventory.py | reported a pending server as "unverified", hiding that it will not connect | reports `pending approval (folder not trusted)` / `pending approval` / `approved, unverified` / `disabled`, matching `claude mcp list` |
| 5 | inventory.py | `disabledMcpjsonServers` also disabled same-named servers in user and local scope | applied to project scope only |
| 6 | inventory.py | crashed on a config whose top level is a list, or on non-list `args` / non-dict `env` | malformed input is skipped |
| 7 | inventory.py | case-folded paths on POSIX, where paths are case-sensitive | case-folds on Windows only |
| 8 | inventory.py | secret-looking command args printed as-is (found during Phase 4, fixed then) | redacted |
| 9 | inventory.py (new) | nothing flagged a literal secret committed in `.mcp.json` | warns by name for env, header, URL query and URL password |
| 10 | the sandbox server | an error message pointed at a tool that did not exist | fixed; rule added to the build checklist |

### Follow-ups (not blocking)

1. Prove write and refusal against a real remote, OAuth-protected server — needs the owner's yes for one real write (the local sandbox already covers the mechanics).
2. Hallway test of the example draft with real receptionists — needs people, not tooling.
4. Confirm the interactive approval path end to end: open `claude` in a trusted folder, approve a project server, re-run `inventory.py` and expect `approved, unverified`.
3. Consider trimming master-design's description (1,373 chars, 2nd longest) if the budget tightens.

---

## 7. Realms and the second hub (2026-09-28)

Requested by the owner: fewer names to remember, category folders named in the Parthenon's Greek and Roman register. This reverses the Phase 5 decision against Option C deliberately: design now has its own front door.

| Change | Before | After |
| --- | --- | --- |
| Folders at the repository root | 31 skill folders | 3 hubs + 5 realms (`pantheon`, `muses`, `mercury`, `hephaestus`, `athena`) |
| Skills that load on their own | 21 | **16** (`view-pdf` retired as a duplicate of the pdf-viewer plugin's own skill; the 4 design specialists now open through `master-design`) |
| Hubs (aggregators) | 1 | 2 — `promethean-parthenon` (10 spokes), `master-design` (4 spokes) |
| Layout source of truth | `CLOSURE` in `build-bundles.py`, flat globs in four scripts | `scripts/skills_layout.py`, read by every script |

**Trigger evals after the change** (blind, 16 active descriptions, 45 prompts): master-design 15/15 should-fire, including all five prompts that used to belong to its new spokes. The first run had 1/10 false fires ("implement this Figma frame in React"); after adding "implementing a finished design in code" to the negative scope, a fresh grader scored 0/10. master-agent 10/10 and 0/10 on both runs.

**Kept as they are, at the owner's request:** the four synced claude.ai skills that duplicate library skills (`lighthouse-score-optimizer`, `obsidian-vault`, `project-file-structure`, `skill-creator`).
**Not done:** merging the two Vercel deploy skills (step D) — optional, later.

**Renamed (same day, at the owner's request):** `master-design` → **`daedalus-atelier`** and `master-agent` → **`hermes-agora`**, so all three hubs share promethean-parthenon's register. This file keeps the old names above because it is a dated record; everywhere else uses the new ones.
