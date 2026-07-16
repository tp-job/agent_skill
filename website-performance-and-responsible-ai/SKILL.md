---
name: ai-web-product-craft
description: >
  Guidance for building, reviewing, or advising on web pages and apps that load images/iframes/embeds and/or include an AI feature (chatbot, AI agent, summarizer, recommender, generative UI). Combines HTML delivery performance (TTFB, caching, compression, CDNs, lazy loading of images and iframes, third-party embed facades) with responsible AI product design (privacy, fairness, calibrated trust, and choosing the right AI UX pattern — background, constrained, or open-ended). Use this whenever the user asks to build, optimize, or review a web page's loading performance, wants to add lazy loading or defer iframes/embeds, is designing an AI feature or AI UX flow, asks about AI governance/trust/transparency/bias, or uses terms like Core Web Vitals, TTFB, LCP, INP, prompt engineering, system prompt, or AI blueprint. Even if the user only mentions "performance" or "AI feature" without naming these specifics, consult this skill — it encodes the trade-offs that are easy to miss.
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "1.0.0"
  source: Web Performance + Responsible AI guidelines (compiled 2026)
---

# AI Web Product Craft

This skill pairs two things that ship together far more often than people plan for: a fast-loading page, and an AI feature bolted onto it. A summarizer widget that blocks the critical path, or a chat agent with no fallback when the model fails to load, undoes the UX it was meant to deliver. Treat performance and responsible AI design as one discipline when the deliverable is a web product, not two separate passes.

Acting as senior leadership across prompt engineering, context engineering, agent design, and AI workflow architecture means making the trade-offs below explicit before code is written, not patching them in after a review flags them.

## How to use this skill

1. Identify which of the two domains (or both) the task touches, using the table below.
2. Read the relevant reference file(s) for the depth you need — they're written to be loaded into context only when relevant.
3. Apply the **Combined checklist** at the end of this file whenever an AI feature lives inside a page that also has its own load-performance budget (this is the common case — most AI features are embedded in normal pages).

|Task touches...|Read|
|---|---|
|Page load speed, TTFB, caching HTML, compression, CDNs|[[html-performance]]|
|Images or `<iframe>`/embeds loading too eagerly, layout shift, third-party widgets (video, chat, ads)|[[html-performance]]|
|Privacy, data collection, bias/fairness, hallucination, calibrated trust, AI governance|[[ai-responsible-design]]|
|Deciding how visible/controllable an AI feature should be (auto-applied vs. button-triggered vs. open chat)|[[ai-ux-patterns]]|
|Unfamiliar AI/product term (compound AI, context engineering, data drift, EDD, model card, system prompt, etc.)|`references/ai-glossary.md`|

## Part 1 — HTML & resource-loading performance (summary)

Every page starts with a request for HTML; how fast that request resolves caps how fast everything else (including any AI UI) can render. The full reasoning, header examples, and code samples are in [[html-performance]]. The headline moves:

- **Minimize redirects**, especially chained ones (ad links → HTTP → HTTPS → final page). Same-origin redirects are fully under your control; fix them at the link level instead of relying on a server hop.
- **Cache HTML carefully.** Static HTML can usually take a short cache lifetime (a few minutes) plus `ETag`/`Last-Modified` revalidation. Personalized or authenticated HTML generally should not be cached at all — there's no way to purge a browser's local cache later.
- **Compress text responses** (HTML, CSS, JS, SVG) with Brotli where supported, gzip as fallback. Very small files barely benefit from compression; very large files cost extra parse/decompress time even when compressed well — neither extreme is free.
- **Use a CDN** to serve cached resources from edge servers near the user, cutting round-trip time and often layering in compression and HTTP/2/3 for you.
- **Lazy-load below-the-fold images and iframes** with the native `loading="lazy"` attribute. Never apply it to hero images or anything likely to be the Largest Contentful Paint candidate — lazy-loaded elements only get requested after layout is computed, which is strictly slower than the preload scanner picking them up immediately.
- **Use the facade pattern for heavy third-party embeds** (embedded video, chat widgets, social posts): show a lightweight static placeholder and swap in the real `<iframe>` only on user interaction. This is the single highest-leverage move for AI chat widgets specifically, since most visitors never open them.
- For elements without native lazy-loading support (`<video>`, CSS `background-image`, video poster images), use an Intersection-Observer-based JS library rather than rolling your own.

## Part 2 — Building AI features responsibly (summary)

Every AI product decision sits in one of three layers: **Data** (what you collect and feed in), **Intelligence** (the model and its surrounding logic), and **User Experience** (what the person actually sees and controls). Responsible design touches all three for each of three pillars — full depth in [[ai-responsible-design]]:

- **Privacy** — collect only what improves the system, strip PII before it leaves the browser or hits an external model, set short retention windows, and prefer on-device/client-side inference for sensitive domains. In the UI, label what's happening ("processed on this device") and ask for consent in context rather than via a blanket opt-in.
- **Fairness** — document training data sources and coverage, run diagnostic tests that swap demographic-coded terms to surface inconsistent treatment, and rank/filter multiple candidate outputs for neutrality before showing one to the user. Make it easy to report a biased or wrong result, and actually close that feedback loop.
- **Trust & transparency** — the goal is _calibrated_ trust, not maximum trust: under-trust means nobody uses the feature, over-trust means errors slip through unreviewed. Use just-in-time, in-context explanations, surface confidence/fallback behavior, and design graceful degradation so a failed AI call still leaves the user with something usable.

## Part 3 — Picking the right AI UX pattern (summary)

Before designing the interface, decide how exposed the AI should be. Full decision criteria and a worked example are in [[ai-ux-patterns]].

- **Background AI** — runs automatically, no user trigger (spam filters, blurred video backgrounds, personalized recommendations). Use when the task is low-risk, user control wouldn't meaningfully change the outcome, and the product still delivers its core value if the AI silently fails.
- **Constrained AI** — triggered by an explicit user action (a button, a menu item); the system prompt tightly scopes task, tone, and output format. Use for well-defined, bounded tasks (generate a title, summarize this thread) where predictability matters more than flexibility.
- **Open-ended AI** — free-form natural-language input (a support agent, a chat box). Use only for genuinely high-variance domains, and pair it with structured shortcuts (clickable order numbers, suggested prompts) to cut down on ambiguity rather than leaving it purely conversational.

As AI pioneer John McCarthy put it, once a technique works reliably, people stop calling it AI — which is a useful test for whether a feature even needs "AI" framing in the UI at all, versus just being a good default.

## Combined checklist — shipping an AI feature inside a normal page

Use this when the task is "add an AI feature to a page," which is the most common real-world shape of this work:

- Does the AI feature block the critical rendering path? If not essential to first paint, defer its script/model download the same way you'd lazy-load an iframe — show the page's core content first.
- If the feature uses a client-side/on-device model, is there a visible fallback (e.g., reviews shown without a summary) while the model downloads, rather than a blocking spinner?
- If the AI surface is a chat widget or embedded third-party AI tool, apply the facade pattern: static affordance first, real widget loaded only on interaction.
- Is the AI-generated content visually distinguished from human-authored content, with a short transparency label?
- Is there an opt-out or a way to ignore the feature entirely without breaking the rest of the page?
- For anything beyond background AI, is there a clear, reversible undo/regenerate path, and is the system prompt scoped tightly enough to keep output predictable?
- Have you decided what happens when the model call fails or returns low-confidence output — does the user get a clear, non-blocking fallback rather than a silent error or a confident wrong answer?
- Have you minimized what user data crosses the network to power the feature, and is that documented somewhere a non-technical user could understand?

## Sources

This skill distills Google's web.dev "Learn Performance" (general HTML performance; lazy-loading images and iframes) and "Learn AI" (responsible AI governance; AI UX patterns; glossary) courses, licensed CC BY 4.0. Treat the reference files here as a working summary, not a replacement — link out to web.dev for code-level walkthroughs, interactive demos, and the parts of these courses (e.g., security/SAIF, prompt-engineering mechanics, evaluation-driven development) that fall outside this skill's scope.