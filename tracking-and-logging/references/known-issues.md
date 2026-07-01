# Loading.tsx — Known Issues & Technical Debt Register

## Active Issues

### ISSUE-001: Inline LaserFlow Should Be External Module
**Layer:** L1 Architecture  
**Severity:** P2 High (maintainability)  
**Status:** Open — Comment in source: `// In project: replace inline LaserFlow with import from ./LaserFlow`

**Symptom:** LaserFlow (~200 lines + GLSL) lives inline in Loading.tsx, making the file ~650+ lines.  
**Root Cause:** Intentional for portability, but creates maintenance burden.  
**Fix:**
```
1. Extract LaserFlow to /components/LaserFlow/index.tsx
2. Extract VERT/FRAG to /components/LaserFlow/shader.glsl (or .ts constants)
3. Import in Loading.tsx: import LaserFlow from './LaserFlow'
4. Export hexToRGB as utility: /lib/color.ts
```

---

### ISSUE-002: Google Fonts Injected via DOM (Non-Next.js Pattern)
**Layer:** L4 CSS  
**Severity:** P2 High (performance + Next.js best practice)  
**Status:** Open — Comment: `// Fonts (add to next/font in layout.tsx)`

**Symptom:** Font link tag injected in useEffect — causes FOUT (Flash of Unstyled Text) and bypasses Next.js font optimization.  
**Root Cause:** Component is portable/standalone; doesn't assume Next.js layout context.  
**Fix:**
```typescript
// In layout.tsx:
import { Noto_Sans_JP, Inter } from 'next/font/google';

const notoSansJP = Noto_Sans_JP({ subsets: ['latin'], weight: ['300', '400'] });
const inter = Inter({ subsets: ['latin'], weight: ['300', '400', '600'] });

// Pass className to body or as CSS variable
```

---

### ISSUE-003: Style Injection in useEffect (CSP Risk)
**Layer:** L4 CSS  
**Severity:** P3 Medium (security + Next.js)  
**Status:** Open

**Symptom:** `<style id="__na-kf">` injected via DOM in useEffect.  
**Root Cause:** Keyframes defined inline for portability.  
**Fix:** Move to `globals.css` or CSS Module:
```css
/* loading.module.css */
@keyframes na-eq { from { height: 3px; } to { height: 11px; } }
@keyframes na-scan { 0% { top: -4px; } 100% { top: 100%; } }
@keyframes na-blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.12; } }
@keyframes na-pulse { 0%, 100% { opacity: 0.55; transform: scale(1); }
                      50% { opacity: 1; transform: scale(1.4); } }
@keyframes na-glitch { 0%, 94%, 100% { transform: translateX(0); }
                       95% { transform: translateX(-2px); }
                       97% { transform: translateX(2px); } }
```

---

### ISSUE-004: Missing `prefers-reduced-motion` Support
**Layer:** L4 CSS + L5 Motion  
**Severity:** P1 Critical (accessibility)  
**Status:** Open

**Symptom:** All animations play regardless of OS accessibility settings.  
**Root Cause:** No `@media (prefers-reduced-motion: reduce)` or Framer Motion `useReducedMotion()`.  
**Fix:**
```typescript
// In component:
import { useReducedMotion } from 'framer-motion';
const prefersReduced = useReducedMotion();

// Pass to LaserFlow:
<LaserFlow flowStrength={prefersReduced ? 0 : 0.22} wispDensity={prefersReduced ? 0 : 0.5} />

// For CSS keyframes:
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0.01ms !important; }
}
```

---

### ISSUE-005: onComplete Race Condition on Fast Unmount
**Layer:** L7 Integration  
**Severity:** P1 Critical (memory / callback)  
**Status:** Open

**Symptom:** If parent unmounts `<LoadingScreen>` before the 720ms onComplete timeout fires, the callback may execute into an unmounted tree, causing "Can't perform a React state update on unmounted component" warning (React <18) or silent callback into garbage-collected closure.  
**Fix:**
```typescript
const completeTimerRef = useRef<ReturnType<typeof setTimeout>>(null);

// Replace:
if(onComplete) setTimeout(onComplete, 720);

// With:
if(onComplete) {
  completeTimerRef.current = setTimeout(onComplete, 720);
}

// In cleanup:
return () => {
  clearTimeout(rt);
  if(timerRef.current) clearTimeout(timerRef.current);
  if(completeTimerRef.current) clearTimeout(completeTimerRef.current); // ← ADD
};
```

---

### ISSUE-006: Three.js r128 — OrbitControls Unavailable
**Layer:** L2 WebGL  
**Severity:** P4 Low (informational — not used here)  
**Status:** Won't Fix (camera is Orthographic, no controls needed)

**Note:** This component correctly uses `OrthographicCamera` with a full-screen triangle mesh — OrbitControls are irrelevant. Documented for AI generation guard.

---

### ISSUE-007: WaveformSVG Animation Uses Inline style (Not DS Motion)
**Layer:** L5 + L6  
**Severity:** P3 Medium  
**Status:** Open

**Symptom:** `na-eq` keyframe animation applied via `style` prop with template string. Not using Framer Motion variants (inconsistent with rest of component).  
**Fix:** Convert to motion.rect with `animate` prop or keep as CSS but document as intentional DS exception.

---

## Technical Debt Summary

| ID | Area | Effort | Impact | Priority |
|---|---|---|---|---|
| ISSUE-001 | Architecture | M | Medium | Sprint 2 |
| ISSUE-002 | Fonts/Next.js | S | High | Sprint 1 |
| ISSUE-003 | CSS/CSP | S | Medium | Sprint 2 |
| ISSUE-004 | Accessibility | M | Critical | Sprint 1 |
| ISSUE-005 | Race condition | S | High | Sprint 1 |
| ISSUE-007 | DS consistency | S | Low | Backlog |

**Effort:** S = 0.5 days, M = 1-2 days, L = 3+ days