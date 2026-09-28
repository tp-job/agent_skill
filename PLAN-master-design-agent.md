# Plan — Master Design and Master Agent on the Promethean-Parthenon foundation

Status: **Phase 1 complete (2026-09-28)** · Phases 2–5 open
Branch: one branch per phase (Parthenon rule: a phase is a branch)

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
| 1 | **Foundation** | `master-design/` (SKILL.md + 4 references), `master-agent/` (SKILL.md + 5 references), Parthenon routing rows + v3.1.0, regenerated index/plugin.json | all three checks exit 0 | ✅ done |
| 2 | **Trigger evals** | 10 should-trigger + 10 near-miss prompts per skill (EN + TH); run manually through the skill-creator eval loop; tune descriptions | ≥ 9/10 hits, ≤ 1/10 false fires, no regression in Parthenon RC-06 (skills that never fire) | open |
| 3 | **Design depth** | worked example end-to-end (target → IA → thesis → 3 concepts + scorecard → HTML draft → design record) as `master-design/assets/example-design-record.md`; Figma/Canva/Blender drafting checklists validated against the live servers | one real job run through all four stages; record rebuildable by a fresh session | open |
| 4 | **Agent operations** | `master-agent/scripts/inventory.py` — reads `.mcp.json` + settings, emits a capability-record skeleton; `master-agent/assets/capability-record.md` template; MCP server test checklist exercised against one real server | script runs clean on this repo; one server proven with read, write and refused-call rows | open |
| 5 | **Review & decide** | measure description budget of the active set; decide whether to keep Option A, fold into `CLOSURE` (B), or change the rule for sub-aggregators (C); `github-report` write-up of phases 1–4 | a written decision with premise and expiry, signed off by the owner | open |

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
