---
name: tracking-and-debugging
description: >
  Autonomous bug triage, root-cause diagnosis, and issue reporting for PERN/MERN full-stack
  projects. Immediately outputs a structured issue report and fix guidance WITHOUT asking
  follow-up questions. Trigger when: a component/API/DB bug is described, visual glitch reported,
  performance degrades, crash or error log provided, animation/shader misbehaves, API fails,
  DB query is slow, auth breaks, or regression is suspected.
  Thai triggers: "แก้บัค", "หา bug", "debug", "ทำไม X ไม่ทำงาน", "crash", "error",
  "ช้า", "memory leak", "ไม่แสดงผล", "ส่ง API ไม่ได้", "login ไม่ได้".
  ALWAYS triage autonomously — classify layer, diagnose cause, produce issue report immediately.
---

# SKILL: Autonomous Bug Triage & Debugging
**Stack:** PERN / MERN · **Team:** 1–5 · **Output:** Markdown Issue Report

---

## AUTONOMOUS PROTOCOL

```
STEP 1  Classify symptom → assign Layer(s)
STEP 2  Run diagnostic checklist for each layer
STEP 3  Identify root cause (or top 2–3 candidates)
STEP 4  Generate fix guidance with code diff
STEP 5  Define verification steps
STEP 6  Add regression prevention note
STEP 7  Output complete Issue Report
```

**Confidence annotation:**
- `[CONFIRMED]` — directly visible in provided code/error
- `[LIKELY]` — matches common pattern for this symptom
- `[CANDIDATE]` — possible but needs verification
- `[UNKNOWN]` — insufficient context; note what to collect

---

## STEP 1 — Symptom → Layer Classification

### Layer Map

```
L0  Environment       Browser/Node version, OS, GPU, network, env vars
L1  React Lifecycle   Mount/unmount ordering, state, effects, StrictMode
L2  WebGL / Canvas    Context, renderer, DPR, resize, context loss
L3  GLSL Shader       Compilation, uniforms, precision, extensions
L4  CSS / Keyframes   Injection, animation, font loading, specificity
L5  Motion Library    Framer Motion variants, AnimatePresence, stagger
L6  Design System     Token misuse, DS version mismatch, palette violation
L7  SSR / Hydration   Next.js mismatch, window undefined, client-only code
L8  Express API       Routes, middleware order, CORS, validation, errors
L9  Database          Query perf, connection, schema mismatch, N+1
L10 Auth              JWT expiry, refresh failure, role checks, CORS+creds
L11 Integration       Cross-layer timing, callback races, cleanup order
```

### Quick Classification Table

| Symptom | Primary Layer | Secondary |
|---|---|---|
| Black canvas / nothing renders | L2 | L0 |
| Shader artifacts / wrong colors | L3 | L2 |
| Animation stuck / not playing | L4, L5 | L1 |
| Font shows wrong / boxes | L4 | L0 |
| Component flickers on mount | L1 | L7 |
| Memory grows, never freed | L1, L2 | L11 |
| Hydration mismatch error | L7 | L1 |
| API returns 401/403 unexpectedly | L10 | L8 |
| API returns 500 | L8 | L9 |
| Slow page / API response | L9 | L8 |
| Login broken / session lost | L10 | L11 |
| DB query returns wrong data | L9 | — |
| CORS error | L8, L10 | L0 |
| `onComplete` / callback not firing | L1 | L11 |
| Crash on tab switch | L2 | L1 |
| Build works, production broken | L0 | L7 |

---

## STEP 2 — Layer Diagnostic Checklists

### L1: React Lifecycle

```
Checklist:
☐ All useEffect hooks have a return cleanup function?
☐ All timers (setTimeout/setInterval) cleared on unmount?
☐ All RAF loops (requestAnimationFrame) cancelled on unmount?
☐ All event listeners removed on unmount?
☐ StrictMode double-mount: does cleanup fully reverse mount?
☐ State update after unmount? (async callbacks completing late)
☐ Effect dependencies array: missing dep causes stale closure?
☐ Initial state computed correctly (not dependent on window in SSR)?
```

Key patterns for small-team PERN/MERN:
```typescript
// Stale closure trap — missing dep
useEffect(() => {
  const id = setInterval(() => console.log(count), 1000); // stale count
  return () => clearInterval(id);
}, []); // ← should have [count]

// Race condition — async in effect
useEffect(() => {
  let cancelled = false;
  fetchData().then(data => {
    if (!cancelled) setData(data); // ← guard required
  });
  return () => { cancelled = true; };
}, [id]);
```

---

### L2: WebGL / Canvas

```
Environment probe (run in browser console):
const gl = document.createElement('canvas').getContext('webgl');
console.table({
  available: !!gl,
  renderer: gl?.getParameter(gl.RENDERER),
  version: gl?.getParameter(gl.VERSION),
  derivatives: !!gl?.getExtension('OES_standard_derivatives'),
  dpr: window.devicePixelRatio,
});

Checklist:
☐ Canvas appended to DOM before setSize() called?
☐ Parent container has non-zero width/height?
☐ renderer.dispose() called on unmount?
☐ renderer.forceContextLoss() called on unmount?
☐ geometry.dispose() + material.dispose() called?
☐ ResizeObserver.disconnect() on unmount?
☐ Context loss handler (webglcontextlost/restored) present?
☐ Visibility change pauses RAF loop?
```

---

### L3: GLSL Shader

```
Enable shader error logging:
renderer.debug.checkShaderErrors = true; // Three.js r129+

Checklist:
☐ precision highp float declared?
☐ GL_OES_standard_derivatives extension available before using fwidth()?
☐ All uniforms initialized with correct type (vec3 not vec2)?
☐ uniformsRef.current null-checked before updating?
☐ hexToRGB() input is valid hex string?

Visual artifact → cause map:
All black        → uFade = 0, or shader compile error
Wrong color      → uColor uniform not updated, or hexToRGB NaN
No fog           → FOG_ON define = 0, or uFogIntensity = 0
Clipped edges    → EDGE_X constants out of range
Jitter/flicker   → iMouse stuck, or DPR changed mid-frame
```

---

### L4: CSS / Keyframes

```
Checklist:
☐ Keyframe @keyframe names match animation: property values exactly?
☐ Style/link tags injected once? (check for duplicate IDs in <head>)
☐ Font file loaded? (Network tab → fonts.gstatic.com → 200?)
☐ animation-play-state: running (not paused)?
☐ prefers-reduced-motion not forcing duration to 0?
☐ z-index stacking correct for overlapping animated elements?

Debug: DevTools → Elements → Animations panel
```

---

### L5: Motion Library (Framer Motion)

```
Checklist:
☐ `animate` prop value matches a key in `variants`?
☐ Parent stagger variant propagating to children? (children must have variants too)
☐ AnimatePresence: key on child changes when content should swap?
☐ AnimatePresence mode="wait": exit animation completing before enter starts?
☐ useReducedMotion() checked for accessibility?

Timing formula for stagger:
total_delay = delayChildren + (numChildren - 1) × staggerChildren
```

---

### L7: SSR / Hydration (Next.js)

```
Checklist:
☐ window/document accessed only inside useEffect (not during render)?
☐ Component using dynamic() with { ssr: false } if WebGL/canvas?
☐ Server-rendered HTML matches client hydrated HTML?
☐ Date/random values consistent between server and client?
☐ localStorage/sessionStorage not accessed during SSR?

Fix pattern for window-dependent code:
const [mounted, setMounted] = useState(false);
useEffect(() => setMounted(true), []);
if (!mounted) return <Skeleton />; // ← avoids hydration mismatch
```

---

### L8: Express API

```
Checklist:
☐ Route middleware order: auth → validate → handler?
☐ CORS configured for client origin (including credentials if auth)?
☐ async/await errors caught? (missing try/catch = unhandled rejection)
☐ Request body parsed? (express.json() middleware present)
☐ Validation errors return 400 (not 500)?
☐ Error handler middleware last in chain?

CORS + Auth pattern:
app.use(cors({
  origin: process.env.CLIENT_URL,
  credentials: true,  // ← required for cookies/sessions
}));
```

---

### L9: Database

```
PERN (PostgreSQL):
☐ Query uses parameterized values? (no string interpolation = SQL injection)
☐ Queried field has an index?
☐ Connection pool size appropriate? (default pg pool = 10)
☐ Transaction used for multi-step writes?
☐ EXPLAIN ANALYZE output checked for Seq Scan on large tables?

MERN (MongoDB):
☐ .lean() used on read-only queries?
☐ Index exists for queried field? (db.collection.getIndexes())
☐ $lookup (join) has index on foreign field?
☐ Query selectivity high enough? (avoid full collection scan)

Slow query debug:
// PostgreSQL
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'x@x.com';
// MongoDB
db.users.find({email:'x@x.com'}).explain('executionStats')
```

---

### L10: Auth (JWT)

```
Checklist:
☐ JWT secret in env variable (not hardcoded)?
☐ Token expiry appropriate (access: 15m, refresh: 7d)?
☐ Refresh endpoint exists and interceptor configured?
☐ 401 interceptor retries with refresh before redirecting to login?
☐ Role/permission check on protected routes (not just authentication)?
☐ CORS allows credentials if using cookies?
☐ HttpOnly flag on auth cookies?
```

---

## STEP 3 — Root Cause Statement

```
ROOT CAUSE: [one sentence, concrete]
Evidence:   [file:line or log entry or behavior]
Confidence: CONFIRMED | LIKELY | CANDIDATE
```

If multiple candidates, rank them and diagnose the most likely first.

---

## STEP 4 — Fix Guidance

```diff
// FILE: [path/to/file.tsx]  LINE: [~N]

- [broken code]
+ [fixed code]
```

Keep diffs minimal — change only what's needed. Note if fix requires:
- DB migration
- Env variable change
- Package update

---

## STEP 5 — Verification Steps

```
1. [Action to reproduce bug — confirm it was present]
2. [Action to confirm fix — specific observable outcome]
3. [Edge case to also verify — adjacent scenario]
```

---

## STEP 6 — Regression Prevention

```
TEST TO ADD:
Type:    unit | integration | e2e
File:    [suggested test file path]
Scenario: [what to test]
Assertion: [what to assert]
```

For small teams: focus on integration tests for API routes and unit tests for
business logic. Skip heavy e2e for every bug fix.

---

## STEP 7 — Output: Issue Report Template

Agent generates using this structure:

```markdown
# ISSUE-[YYYYMMDD]-[N]: [Short Title]

**Layer:** L[N] [Layer Name]
**Severity:** P0 Blocker | P1 High | P2 Medium | P3 Low
**Status:** Open
**Reporter:** [agent — autonomous analysis]
**Date:** [YYYY-MM-DD]

## Symptom
[What the user observed]

## Root Cause
[ROOT CAUSE statement with confidence level]

## Evidence
[Code pattern / error log / console output]

## Fix
[Code diff with file + line reference]

## Verification
[3-step verification sequence]

## Regression Prevention
[Test to add]

## Escalation
[See escalation guide below — only add if P0 or UNKNOWN]

---
*Assumptions: [CANDIDATE or UNKNOWN items that need human verification]*
```

---

## Small-Team Escalation Guide

For a 1–5 person team, escalate when:

| Situation | Action |
|---|---|
| Root cause is UNKNOWN after 30min | Pair with another dev — fresh eyes |
| Bug is in shared DB schema | Sync whole team before fixing |
| Fix requires breaking API change | Discuss versioning strategy first |
| P0 in production | One person fixes, one person monitors, communicate ETA |
| Bug reproduces only on specific device/OS | Borrow device or use BrowserStack |

---

## Reference Files

- `references/known-issues.md` — Documented issues for the Nocturnal Atelier Loading component
- `references/full-stack-debug-deep-dive.md` — Deep-dive debugging for L8/L9/L10 full-stack layers