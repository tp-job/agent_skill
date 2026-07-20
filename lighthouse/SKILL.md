---
name: lighthouse
description: >-
  Diagnose and fix a website so it earns high Lighthouse scores across all five categories — Performance, Accessibility, Best Practices, SEO, and Agentic Browsing — on BOTH desktop and mobile. Use this skill whenever the user shares a Lighthouse / PageSpeed / Core Web Vitals report, screenshot, or score; asks to "improve my Lighthouse score", "make my site faster", "fix my performance score", "pass Core Web Vitals", "get green scores", or mentions failing metrics like FCP, LCP, TBT, CLS, INP, or Speed Index — even if they don't say the word "Lighthouse". Also trigger for pre-launch audits and for hosting/cold-start slowness (e.g. Render/Heroku/Fly free tiers) that tanks load-time metrics.
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "1.0.0"
  source: Lighthouse Score Optimizer guidelines (compiled 2026)
---

# Lighthouse Score Optimizer

Turn a middling or failing Lighthouse report into consistent 90+ (ideally 95–100) scores across all five categories, on desktop **and** the harsher mobile profile. The job is not to game a number — it is to make real, measurable improvements to load speed, responsiveness, and correctness that the number reflects.

## Operating principle: diagnose before you touch code

Never guess at fixes from the category scores alone. The category number is a weighted roll-up; the **individual audits** tell you exactly which bytes, requests, and DOM nodes are costing points. Always get the specific failing audits first (from the report, the JSON, or by re-running), rank them by estimated savings, and fix the biggest levers first. One `4.3s` LCP image often outweighs ten cosmetic warnings.

## The loop

Work in tight measure → diagnose → fix → verify cycles. Do **not** batch twenty changes then re-run once; you lose the ability to attribute regressions.

1. **Measure** — capture a baseline for the _right_ form factor. Mobile and desktop use different throttling, so run both. Prefer the CLI for reproducibility:
    
    ```bash
    npx lighthouse https://example.com \  --preset=desktop --output=json --output=html \  --output-path=./lh-desktop --chrome-flags="--headless=new"npx lighthouse https://example.com \  --form-factor=mobile --output=json --output=html \  --output-path=./lh-mobile --chrome-flags="--headless=new"
    ```
    
    Run each **3 times** and take the median — lab numbers are noisy, and a single run can swing a score by 10+ points.
2. **Diagnose** — open the JSON/HTML, list failing and "needs improvement" audits, and sort by `overallSavingsMs` / `overallSavingsBytes`.
3. **Fix** — apply the smallest coherent change that addresses the top lever.
4. **Verify** — re-run the same command, confirm the metric moved and nothing regressed, then move to the next lever.

## Targets (what "high" means)

|Metric|Good (green)|Notes|
|---|---|---|
|Performance / A11y / Best Practices / SEO|≥ 90|95+ is the real goal|
|First Contentful Paint (FCP)|< 1.8 s|mobile is throttled ~4× CPU|
|Largest Contentful Paint (LCP)|< 2.5 s|usually the hero image or heading|
|Total Blocking Time (TBT)|< 200 ms|lab proxy for INP responsiveness|
|Cumulative Layout Shift (CLS)|< 0.1|visual stability|
|Speed Index|< 3.4 s|how fast content paints|
|Interaction to Next Paint (INP, field)|< 200 ms|the real-user responsiveness metric|

## Triage: where the points actually are

Performance is weighted heavily toward LCP and TBT. A report showing (as is common) accessibility/SEO already in the 90s but Performance stuck in the 50s with FCP ≈ LCP ≈ 4 s, TBT near 900 ms, and CLS healthy is a textbook **load-and-execution** problem, not a layout problem. That pattern means: slow first byte (often a cold-starting/unCDN'd host) + render-blocking CSS/JS + a heavy JavaScript bundle. Spend your effort there, and treat the already-green categories as "maintain and polish."

---

## 1. Performance (the biggest lever)

### 1a. Fix time-to-first-byte and hosting first

If FCP is already ~4 s, the server is often the culprit before a single byte of your bundle is blamed. This is the #1 silent killer on free hosting tiers.

- **Cold starts** (Render/Heroku/Fly/Railway free tiers spin down when idle; the next visit pays a multi-second boot). Options, best first:
    1. Serve static/prerendered output from a CDN edge (Netlify, Vercel, Cloudflare Pages, GitHub Pages) so there is no server to wake.
    2. Upgrade to an always-on instance, or add a health-check pinger (e.g. a cron hitting the URL every ~10 min) to keep it warm.
    3. Add SSR/SSG caching so the wake path serves cached HTML.
- Enable **Brotli/gzip** compression and **HTTP/2 or HTTP/3**.
- Set long-lived **cache headers** (`Cache-Control: public, max-age=31536000, immutable`) on hashed static assets; put everything behind a CDN.

### 1b. Eliminate render-blocking resources (fixes FCP + Speed Index)

- Inline **critical CSS** for above-the-fold content; load the rest async (`<link rel="preload" as="style" onload="this.rel='stylesheet'">`).
- Add `defer` (or `type="module"`) to scripts; move non-critical JS out of the critical path. Nothing render-blocking should sit in `<head>` without reason.
- `preconnect`/`dns-prefetch` to third-party origins (fonts, analytics, CDNs).

### 1c. Nail the LCP element (fixes LCP)

- Identify the LCP node in the report (usually the hero image or largest heading). `preload` it: `<link rel="preload" as="image" href="hero.avif" fetchpriority="high">`.
- Serve modern formats (**AVIF/WebP**), correctly sized with `srcset`/`sizes` so mobile never downloads a desktop-sized image.
- Never lazy-load the LCP image. Do lazy-load everything below the fold (`loading="lazy"`).
- For web fonts, use `font-display: swap` and `preload` the one font used in the LCP text; self-host fonts to avoid a third-party round trip.

### 1d. Cut Total Blocking Time / JavaScript (fixes TBT + INP)

TBT ~900 ms means the main thread is jammed parsing/executing JS.

- **Ship less JS.** Audit the bundle (`npx vite-bundle-visualizer`, `source-map-explorer`, or `webpack-bundle-analyzer`). Remove unused deps, drop heavy libraries (moment→date-fns/dayjs, lodash→per-method imports).
- **Code-split** by route and lazy-load below-the-fold / interaction-gated components (`React.lazy` + `Suspense`, dynamic `import()`).
- Tree-shake and **minify**; ensure production builds (no dev bundles shipped).
- Defer third-party scripts (chat widgets, analytics); load them on idle or interaction, not at startup.
- For SPAs, prefer **SSR/SSG/prerender** so users see content before hydration.

### 1e. Prevent layout shift (keeps CLS green)

- Set explicit `width`/`height` (or `aspect-ratio`) on all images, videos, iframes, and ad/emb, slots so space is reserved.
- Reserve space for dynamically injected content; never insert above existing content after paint.
- Use `font-display: optional` or size-adjust metrics to avoid FOUT reflow.
- Animate only `transform`/`opacity`, never layout-affecting properties.

---

## 2. Accessibility

Most a11y points come from a short, high-value checklist. Keep it green:

- Every image has meaningful `alt` (empty `alt=""` for decorative).
- Sufficient **color contrast** (≥ 4.5:1 body text, 3:1 large text). This is the single most common a11y point-loss.
- All form controls have associated `<label>`s; icon-only buttons have `aria-label`.
- Logical **heading order** (one `<h1>`, no skipped levels).
- `<html lang="…">` set; page has a descriptive `<title>`.
- Visible **focus indicators**; full keyboard operability; no positive `tabindex`.
- Landmarks (`<main>`, `<nav>`, `<header>`, `<footer>`) present.
- Touch targets ≥ 24×24 px (48 px comfortable) — also helps mobile Best Practices.

## 3. Best Practices

- Serve over **HTTPS**; no mixed content.
- **Zero console errors** during load (Lighthouse penalizes them) — fix the actual errors, don't suppress.
- No use of deprecated/`unload` APIs; valid `<!doctype html>` and `charset`.
- Images displayed at correct aspect ratio and sufficient resolution.
- No known-vulnerable JS libraries (audit and upgrade dependencies).
- Set a reasonable **Content-Security-Policy** and other security headers (`X-Content-Type-Options: nosniff`).

## 4. SEO

- Unique, descriptive `<title>` and `<meta name="description">`.
- `<meta name="viewport" content="width=device-width, initial-scale=1">` present (also gates mobile usability).
- `robots.txt` reachable and not blocking; page is indexable (no stray `noindex`).
- Add a **sitemap.xml** and a `<link rel="canonical">`.
- Links have descriptive, crawlable text (no bare "click here"; real `href`s, not JS-only handlers).
- Add **structured data** (JSON-LD) where relevant (e.g. `Person`/`Portfolio` for a personal site) — validate with the Rich Results test.
- Open Graph / Twitter Card tags for good link previews (indirect SEO benefit).

## 5. Agentic Browsing

This newer Lighthouse category checks whether an AI agent can understand and operate the page. Much of it overlaps with good semantics and SEO:

- **Semantic HTML** and ARIA give elements accessible names an agent can act on (buttons are `<button>`, links are `<a href>`, forms have labels).
- Content is present in the **initial HTML** / server-rendered, not hidden behind client-only rendering an agent can't wait for.
- Machine-readable metadata: structured data (JSON-LD), clear page `<title>`, descriptive headings.
- Consider an **`/llms.txt`** and a clean, crawlable link graph so agents can navigate.
- Stable, meaningful element identifiers and labels for interactive controls.

If this category is already passing (e.g. 2/2), the accessibility and SEO work above keeps it there — verify it didn't regress after JS/DOM changes.

---

## Desktop vs. Mobile — treat them as two targets

Mobile is where scores collapse, because Lighthouse mobile applies ~4× CPU throttling and a slow-4G network profile. A site that's 90 on desktop can be 50 on mobile. So:

- **Always test both**; optimize to pass the mobile bar and desktop follows.
- Mobile magnifies JS cost — TBT/INP fixes (§1d) matter most here.
- Serve **smaller images to small screens** via `srcset`/`sizes`; don't ship a 2000px hero to a phone.
- Ensure a correct viewport, no horizontal scroll, and comfortable tap targets.
- Verify font sizes are legible (≥ ~16px body) — Lighthouse flags tiny text.

## Framework quick-notes

- **Next.js / Nuxt**: use SSG/ISR, `next/image` (or equivalent), `next/font`, route-level code splitting; enable output caching on the host.
- **Vite/CRA SPA**: add prerendering (`vite-plugin-ssr`, `react-snap`) so first paint isn't blank; lazy-load routes; check the production bundle, not dev.
- **Static sites**: you're mostly fighting images, fonts, and hosting — put it on a CDN and optimize assets.

## Verification gate (definition of done)

Before declaring success, confirm on the **median of 3 runs, mobile profile**:

- Performance ≥ 90 (target 95+), and all Core Web Vitals in the green band (LCP < 2.5 s, TBT < 200 ms, CLS < 0.1).
- Accessibility, Best Practices, SEO each ≥ 95.
- Agentic Browsing passing.
- Desktop is at least as good.
- **No regressions**: re-check that speeding things up didn't strip alt text, break focus order, or hide content from crawlers/agents.

Report results as a before→after table per category and per metric, and list the top three changes that moved the numbers so the user understands the wins.

## Anti-patterns (don't do these)

- Chasing cosmetic warnings while a 4 s LCP image sits ignored.
- "Optimizing" by removing content, disabling JS blindly, or hiding elements from Lighthouse — that breaks the real site and often other categories.
- Tuning only desktop and calling it done.
- Deferring the LCP image or the critical font (makes LCP worse).
- Testing once and trusting a noisy single run.
- Adding an aggressive CSP/preload that breaks functionality — verify the page still works after every change.