# Maintaining the bundle

For whoever edits this package, not for running it. Load this only when changing a file under `bundled/` or refreshing the bundle.

## The rule

Every skill under `bundled/` is a verbatim copy of a standalone skill in the library. Refresh copies from the source; do not edit them in place. The spokes carry no links or bundles of their own; only this hub combines them.

## When a copy is actually broken

"Never hand-edit `bundled/`" is the right default and a bad absolute. `skill-creator` once shipped instructing eighteen scripts that do not exist in this bundle, which left the skill that repairs skills unable to run its own process.

1. Fix the copy if the break blocks work now.
2. Record it in the table below.
3. Carry the same fix to the source skill and regenerate. That is the only way it survives the next refresh. Until then the fix is a debt, not a state.

**Local fixes outstanding:** none.

| Skill | Fix | Paid to upstream |
| --- | --- | --- |
| `skill-creator` | Replaced the automated eval half with a manual loop; it referenced 18 scripts and 3 agent files that ship nowhere in this library | Yes, `skill-creator` v1.1.0 |
| `long-horizon-engineering-workflow` | Seven files carrying the RC-01…RC-08 fixes: the `git check-ignore` precheck, the ledger's `blocked` state, decision premises and expiry, Stage 2 house mechanics, prove-the-instrument-can-fail, idempotent bulk writes, one-concern commits | Yes, `long-horizon-engineering-workflow` v3.3.0 |

The second row is why the rule exists: those fixes lived only in `bundled/` for two months, so every project that installed the source skill never got them, and `check-bundles.py` reported them as drift to overwrite.

## Cross-skill links do not survive the trip upstream

A link from one spoke to another is legal in this hub and illegal in the spoke, which must stand alone. When propagating a bundled fix, convert any cross-skill link in it to plain prose in both copies.

## Verifying a change

Check every change to this package against [regression-cases](regression-cases.md): failures this skill actually caused, each with a known correct answer. Write a new case **before** the fix; a case written afterwards is shaped to fit the fix and stops being evidence. Then run the routing suite in the library's `evals/` folder.
