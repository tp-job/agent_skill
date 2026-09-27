---
name: debug-master
description: >-
  Deep debug and auto-fix skill covering file system inspection, logic tracing, algorithm analysis, and AI workflow debugging. Trigger this skill whenever the user shares an error message, stack trace, broken file path, missing module, wrong output, or describes unexpected behavior in any codebase or workflow. Also trigger for: "why is this not working", "fix this bug", "check my paths", "trace this logic", "analyze this algorithm", "my workflow is broken", "find the error", "debug this agent", "check folder structure", "validate these files", "summarize this algorithm's complexity", or any variant of these. Use this skill even for vague reports like "something is wrong" — the skill's intake phase will extract what's needed. Covers Python, JavaScript/TypeScript, Go, Bash, SQL, LangChain/LangGraph, AutoGen, CrewAI, and generic AI agent workflows. This skill is intentionally broad — when in doubt, use it.
argument-hint: "<error, path, file, or workflow to debug>"
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "1.1.0"
  source: Multi-layer debugging methodology (compiled 2026)
---

# debug-master

> Senior-level debugging across **File System**, **Logic & Workflow**, and **Algorithm Analysis**. Four phases: Inspect → Isolate → Diagnose → Fix.

---

## Overview

This skill runs a structured, multi-layer debug session. It covers three orthogonal problem classes — file/path issues, logic/workflow failures, and algorithm bugs — then converges on a minimal, verified fix.

```
┌──────────────────────────────────────────────────────────────────────┐
│                        DEBUG-MASTER PIPELINE                         │
├──────────────────┬──────────────────┬──────────────────┬────────────┤
│  PHASE 1         │  PHASE 2         │  PHASE 3         │  PHASE 4   │
│  FILE SYSTEM     │  LOGIC &         │  ALGORITHM       │  FIX &     │
│  INSPECTION      │  WORKFLOW TRACE  │  ANALYSIS        │  VERIFY    │
│                  │                  │                  │            │
│  • Path exists?  │  • Entry point   │  • Complexity    │  • Patch   │
│  • Type correct? │  • Step order    │  • Edge cases    │  • Test    │
│  • Folder tree   │  • State flow    │  • Correctness   │  • Guard   │
│  • Permissions   │  • Long chain    │  • Summary       │  • Docs    │
└──────────────────┴──────────────────┴──────────────────┴────────────┘
```

Start at the phase that matches the reported problem. Many bugs span multiple phases — run all relevant phases before proposing a fix.

---

## PHASE 1 — File System Inspection

Paths, folder structure, file content, and dependency/import trace — run first for missing-module, wrong-path, and encoding errors. Full procedure: [file-system-inspection](references/file-system-inspection.md).

Covers: 1-A Path Validation Checklist · 1-B Folder Structure Scan · 1-C File Content Quick-Check · 1-D Dependency & Import Trace.

---

## PHASE 2 — Logic & Workflow Trace

Entry point, long-workflow decomposition, AI agent/LLM workflow debugging, and branch-logic audits — for wrong output with no crash. Full procedure: [logic-workflow-trace](references/logic-workflow-trace.md).

Covers: 2-A Locate the Entry Point · 2-B Long Workflow Decomposition · 2-C AI Agent / LLM Workflow Debugging · 2-D Conditional & Branch Logic Audit.

---

## PHASE 3 — Algorithm Analysis & Summary

Complexity, correctness audit, the summary block, and optimization recommendation — for slow or subtly wrong algorithms. Full procedure: [algorithm-analysis](references/algorithm-analysis.md).

Covers: 3-A Complexity Analysis · 3-B Correctness Audit · 3-C Algorithm Summary Block · 3-D Optimization Recommendation.

---

## PHASE 4 — Fix & Verify

### 4-A Root Cause Statement

Write one sentence in this form before proposing code:

> **Root cause:** `[specific function/line]` [does X] but [should do Y] because [reason]. First visible symptom: [error/output].

This forces precision and prevents fixing the symptom instead of the cause.

### 4-B Minimal Patch

Show only the changed lines with clear before/after:

```diff
# File: src/agents/coordinator.py  Line: 47
- result = self.tools[tool_name](input)
+ result = self.tools.get(tool_name)
+ if result is None:
+     raise KeyError(f"Tool '{tool_name}' not registered. "
+                    f"Available: {list(self.tools.keys())}")
+ result = result(input)
```

### 4-C Regression Guard

Provide the minimal test that would have caught this bug:

```python
def test_<bug_name>():
    """Regression: <one-line description of what failed>"""
    # Arrange
    ...
    # Act
    with pytest.raises(KeyError, match="Tool 'X' not registered"):
        coordinator.run(tool_name="X")
    # Assert
    # (assertion is in the raises block above)
```

### 4-D Post-Fix Checklist

```
□ Does the fix address the ROOT CAUSE (not just the symptom)?
□ Does the fix break any other callers of this function?
□ Are all edge cases still handled?
□ Is the fix backward-compatible?
□ Is a migration / data fix needed (DB, files, cached state)?
□ Should a feature flag wrap this change?
□ Is there a log/metric to confirm the fix is live?
```

---

## Output: Debug Report Template

```markdown
## Debug Report: [Issue Summary]

### Classification
- **Type**: [ ] File/Path  [ ] Logic/Workflow  [ ] Algorithm  [ ] Multi-phase
- **Severity**: Critical / High / Medium / Low
- **Scope**: [function / module / service / system]

### Reproduction
- **Expected**: [what should happen]
- **Actual**: [what happens instead]
- **Reproduces consistently?**: Yes / Flaky (conditions: ...)

### Findings

#### Phase 1 — File System
[Path validation results, missing files, type mismatches, tree diffs]

#### Phase 2 — Logic & Workflow
[Workflow step table, first deviation, state audit, agent trace]

#### Phase 3 — Algorithm
[Complexity report, correctness table, algorithm summary block]

### Root Cause
[One sentence root cause statement from 4-A]

### Fix
[Diff from 4-B]

### Regression Test
[Code from 4-C]

### Prevention
[Checklist items from 4-D, plus any architectural suggestions]
```

---

## Decision Tree — Which Phase(s) to Run

```
User reports a bug
        │
        ▼
"File not found / import error / wrong path / missing module?"
   YES ──► Run PHASE 1 (File System Inspection)
   NO  ──► continue
        │
        ▼
"Wrong output / silent failure / agent loop / pipeline broken?"
   YES ──► Run PHASE 2 (Logic & Workflow Trace)
   NO  ──► continue
        │
        ▼
"Slow / incorrect result / want to understand algorithm?"
   YES ──► Run PHASE 3 (Algorithm Analysis)
        │
        ▼
All relevant phases complete → Run PHASE 4 (Fix & Verify)
```

**When in doubt, run all phases.** A file bug often masks a logic bug.

---

## Quick Reference — Common Error Patterns

| Error                    | Most Likely Phase | First Check                    |
| ------------------------ | ----------------- | ------------------------------ |
| `FileNotFoundError`      | Phase 1           | `os.path.abspath(path)` vs CWD |
| `ModuleNotFoundError`    | Phase 1           | `pip show` + `sys.path`        |
| `KeyError` in dict       | Phase 2           | Log `.keys()` before access    |
| `IndexError` in list     | Phase 2 + Phase 3 | Off-by-one audit               |
| `NoneType has no attr`   | Phase 2           | Find where `None` enters       |
| Wrong LLM output         | Phase 2           | Log full prompt + token count  |
| Agent infinite loop      | Phase 2           | Check termination condition    |
| TLE / timeout            | Phase 3           | Complexity audit               |
| Wrong math result        | Phase 3           | Float precision + off-by-one   |
| Flaky / race condition   | Phase 2           | Add timestamps + thread IDs    |
| "Works locally not prod" | Phase 1 + 2       | Env vars, paths, versions      |

---

## Notes for AI Workflow Architects

When debugging **multi-agent systems** or **prompt pipelines**, treat each agent/prompt as a black box with a defined input schema and output contract. Debug the **contract boundary**, not the internals first:

1. **Log the exact string** sent to each model — not a template, the rendered string.
2. **Log the exact response** — not a parsed version, the raw API response.
3. **Validate schemas** at every hand-off (use Pydantic / Zod / JSON Schema).
4. **Isolate agents** — run each agent in isolation with synthetic inputs before debugging the composed system.
5. **Replay failure cases** — save the exact input that caused the failure and replay it deterministically (fix seed, temperature=0) to reproduce.
