# HTML delivery & resource-loading performance

Source: web.dev Learn Performance — "General HTML performance considerations" and "Lazy-load images and iframe elements."

## Why the first HTML request matters

Every page load starts with a `GET` request for the HTML document. The time that takes — Time to First Byte (TTFB) — isn't itself a user-facing metric, but a slow TTFB makes it mechanically hard to hit good scores on First Contentful Paint (FCP) and Largest Contentful Paint (LCP), since nothing can render before the HTML arrives.

## Minimize redirects

Redirects (`301` permanent, `302` temporary) cost a full extra HTTP round trip.

- **Same-origin redirects** are entirely within your control (e.g., a server-side rule). Fix the underlying link instead of relying on the redirect — a common offender is internal links pointing to a URL that just redirects to the canonical trailing-slash/no-trailing-slash variant.
- **Cross-origin redirects** (ad networks, URL shorteners, third-party services) are usually outside your control, but you can still avoid compounding them — e.g., don't link to an HTTP page that then redirects to HTTPS when you could link to HTTPS directly.

## Caching the HTML response

HTML is harder to cache than static assets because it typically references other resources (CSS, JS, images) by filename, and those filenames often contain content hashes that change on every deploy. A long-cached HTML document can end up pointing at stale sub-resources.

- A **short cache lifetime** (e.g., 5 minutes) for static HTML is a reasonable default: long enough to offload repeat requests to a CDN edge or let the browser revalidate instead of re-downloading, short enough that updates aren't missed for long.
- If the HTML is **personalized or generated per authenticated user**, avoid caching it at all — once a browser has cached a response, you cannot remotely purge it, which creates real staleness and security risk for anything user-specific.
- A middle-ground approach uses validation headers:
    - `ETag` is a hash-like fingerprint of the resource. On a later request, the browser sends it back via `If-None-Match`; if it still matches, the server replies `304 Not Modified` with no body, which is far smaller than re-sending the full document (though it still costs a network round trip).
    - `Last-Modified` works the same way, using a timestamp instead of a hash.
- There's no universally correct choice here — it's a genuine trade-off between implementation effort and freshness guarantees. Decide deliberately rather than defaulting to "don't cache HTML at all" out of caution.

## Measuring and reducing server response time

If nothing is cached, TTFB is largely a function of hosting infrastructure and backend stack. Pages backed by a database query will generally have higher TTFB than ones served statically with no backend computation. Pushing more work to client-side fetching after an initial loading state shifts load from a more predictable server environment to a less predictable client one — reducing client-side effort tends to help user-centric metrics more than it might seem.

To diagnose a slow TTFB in the field, the `Server-Timing` response header can report durations for named server-side phases:

```
Server-Timing: auth;dur=55.5, db;dur=220
```

This data can be picked up via the Navigation Timing API and aggregated across real users to see which backend phase is the bottleneck. Also worth checking: whether the hosting tier has enough resources for the traffic — shared hosting tends to have higher TTFB than dedicated solutions, which is a cost/performance trade-off to make consciously.

## Compression

Compress text-based responses — HTML, JS, CSS, SVG. Brotli outperforms gzip by roughly 15-20% and is supported by all major browsers; use it where possible, with gzip as a fallback for older clients. Two nuances:

- **File size matters.** Very small files (under ~1 KiB) barely compress, since compression algorithms need enough data to find redundancy. But bigger isn't automatically better either — large JS/CSS bundles take longer to parse and evaluate after decompression, and any small change invalidates the whole bundle's content hash.
- **Static vs. dynamic compression** is about _when_ compression happens. Static compression (pre-compressing files ahead of time) avoids adding compression time to the response — appropriate for static assets like images, JS, CSS, SVG. Dynamic compression happens at request time (sometimes on every request) and is the right call for HTML that's generated per-user, since you can't pre-compress something that doesn't exist yet.

Most hosting providers and CDNs handle this automatically; understanding the trade-offs lets you verify they're configured well rather than assuming so.

## CDNs

A CDN is a distributed network of edge servers that cache origin resources and serve them from a location physically closer to the user, cutting round-trip time. CDNs typically also layer in HTTP/2/3, caching, and compression — using one can meaningfully improve TTFB, especially for traffic far from your origin server.

## Lazy-loading images

The `loading` attribute on `<img>` tells the browser when to fetch it:

- `"eager"` (the default) — fetch immediately, even if off-screen.
- `"lazy"` — defer until the image is within a browser-defined distance of the viewport (this threshold varies by browser and connection type).

Rules of thumb:

- Apply `loading="lazy"` only to images **outside the initial viewport**. This is genuinely hard to determine precisely (viewport size varies a lot across devices and orientations), but the clear case to get right is: **never** lazy-load hero images or anything likely to be the LCP element — lazy-loaded images are only requested _after_ the browser finishes layout, which is strictly slower than the preload scanner picking them up from raw markup immediately.
- If you're using `<picture>`, put the `loading` attribute on the child `<img>`, not on `<picture>` itself — `<picture>` is just a container of candidate `<source>`s; the browser's chosen image still resolves to the `<img>`.
- The `loading` attribute does **not** affect network priority. If you need to influence priority directly, use the Fetch Priority API (`fetchpriority`) — but note that an in-viewport image marked both `fetchpriority="high"` and `loading="lazy"` will still wait for layout before it's requested, since lazy-loading gates the request regardless of priority.
- Because `loading="lazy"` is supported by all major browsers, there's generally no need for a JavaScript-based lazy-loading solution for plain `<img>` elements — adding JS to replicate a native browser capability has its own performance cost (e.g., to INP).

## Lazy-loading `<iframe>` elements

`<iframe>` supports the same `loading` attribute and values as `<img>`. Because an iframe is an entire separate HTML document with its own sub-resources, lazy-loading it can save substantially more than lazy-loading an image — and improves Interaction to Next Paint (INP) at startup, since iframe sub-resources (especially JS) competing for the main thread can make the page sluggish to early input.

Concretely: lazy-loading an embedded YouTube video can save 500+ KiB on first load; lazy-loading a Facebook "Like" button embed can save 200+ KiB, mostly JS. Any below-the-fold third-party `<iframe>` embed (video players, social widgets, ad creative) is a strong candidate for `loading="lazy"`.

Note: browsers reserve layout space and show a placeholder while a lazy iframe is still being fetched, but you should still set explicit `width`/`height` (and supporting CSS) to minimize layout shift.

## The facade pattern for third-party embeds

For embeds that are expensive _and_ often unused by a given visitor — embedded video players, chat widgets — go a step further than lazy-loading: show a lightweight static placeholder (an image that looks like the paused video, a fake "Start chat" button) and only swap in the real third-party `<iframe>`/widget once the user actually interacts with it.

This means visitors who never click never download the embed's resources at all — a stronger guarantee than lazy-loading alone, which still triggers a download once the element scrolls into view. Open-source facade implementations exist for common cases: `lite-youtube-embed`, `lite-vimeo-embed`, and `React Live Chat Loader` for chat widgets. This pattern is the single most relevant performance technique for AI chat widgets specifically, since the bulk of visitors to most pages never open the chat at all.

## JS-based lazy loading for unsupported elements

The native `loading` attribute only covers `<img>` and `<iframe>`. For `<video>`, video poster images, or CSS `background-image`, lazy-loading isn't a browser-native feature — use a library such as `lazysizes` or `yall.js`, both of which work via the Intersection Observer API (and a Mutation Observer for content injected after initial load). These libraries watch for a marker (commonly a `data-src`-style attribute) and swap it to the real `src` once the element nears the viewport.

A muted, autoplaying, looping `<video>` with no audio track is a much lighter alternative to an animated GIF for the same visual effect, but can still be sizeable enough that lazy-loading it is worthwhile.