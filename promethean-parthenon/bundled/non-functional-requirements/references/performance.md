# Category 1 — Performance efficiency

## Contents

- Where the thresholds come from
- Measurement conditions (write once, apply to all)
- NFR catalogue
- Tools and how to read them
- Pitfalls

---

## Where the thresholds come from

| Threshold | Meaning | Source |
| --- | --- | --- |
| **0.1 s** | feels instantaneous; no feedback needed | Miller (1968); Card, Robertson and Mackinlay (1991); Nielsen (1993) |
| **1 s** | the user's flow of thought stays uninterrupted, though the delay is noticed | same |
| **10 s** | the limit for keeping attention on the task; beyond this, show progress | same |
| **LCP ≤ 2.5 s** | main content visible ("good") | Google Web Vitals |
| **INP ≤ 200 ms** | interaction responds visibly ("good"). INP replaced FID as a Core Web Vital in March 2024. | Google Web Vitals |
| **CLS ≤ 0.1** | layout stays stable ("good") | Google Web Vitals |

Google assesses Web Vitals at the **75th percentile** of real page loads. A lab measurement such as Lighthouse is a proxy for that and does not replace it.

## Measurement conditions (write once, apply to all)

Put this block in the spec once, and have every performance NFR refer to it.

- **Dataset**: a realistic size and a maximum size. Example: typical 150 students × 25 assessments; maximum = the import limit.
- **Environment**: the deployed server, not localhost. Give the hosting tier, region, browser and version, and device class.
- **Network**: unthrottled desktop, or a named throttling profile.
- **Runs**: at least 30 per measurement. Report n, median, p95 and max.
- **Cache state**: warm, with cold start (first request after the server sleeps) reported separately. Free hosting tiers often sleep.

## NFR catalogue

| ID | Statement | Scale / Meter | Must (typical) | Source |
| --- | --- | --- | --- | --- |
| PF-01 | Main data page renders | s, navigation → last row painted, `performance.measure()` | p95 ≤ 2.0 s | Miller (1968); Nielsen (1993) |
| PF-02 | Key computation API responds | ms server time, k6 `http_req_duration` | p95 ≤ 1000 ms | Miller (1968) |
| PF-03 | Main content appears | LCP, Lighthouse / PageSpeed Insights | ≤ 2.5 s | Google Web Vitals |
| PF-04 | Inputs respond | INP, DevTools or `web-vitals` library | ≤ 200 ms | Google Web Vitals |
| PF-05 | Layout stays stable | CLS | ≤ 0.1 | Google Web Vitals |
| PF-06 | Overall lab score | Lighthouse Performance, desktop, key pages | ≥ 90 | project target |
| PF-07 | Largest allowed upload processes | s and peak RSS, `process.memoryUsage()` | ≤ 10 s; peak < host memory limit | Nielsen (1993) 10 s limit |
| PF-08 | Oversize input rejected safely | file 1 unit over each limit | rejected with message; no crash | OWASP API4:2023 |
| PF-09 | Peak concurrent use | k6 VUs for 5 min | p95 ≤ 2 s and error rate < 1% at N users | project target (state N's origin) |
| PF-10 | Waiting is visible | inspection | spinner/skeleton for waits > 1 s; progress bar for > 10 s | Nielsen (1993); Nielsen (1994) heuristic 1 |

## Tools and how to read them

| Tool | Use | Pass/fail in CI |
| --- | --- | --- |
| `performance.mark()` / `measure()` | exact app-defined timings (e.g. "table painted") | log to console; collect over 30 runs |
| Chrome DevTools → Performance | find what makes a slow interaction slow (INP breakdown) | — |
| Lighthouse / PageSpeed Insights | LCP, CLS, TBT in the lab; PSI adds field data when there is enough traffic | Lighthouse CI `assertions` |
| k6 (Grafana) | API latency and load | `thresholds: { http_req_duration: ['p(95)<1000'], http_req_failed: ['rate<0.01'] }` |
| `scripts/latency_summary.py` | turn a k6 export or timing CSV into n/median/p95/p99/max | — |

Minimal k6 script:

```js
import http from 'k6/http';
export const options = {
  vus: 30, duration: '5m',
  thresholds: { http_req_duration: ['p(95)<2000'], http_req_failed: ['rate<0.01'] },
};
export default function () { http.get(`${__ENV.BASE_URL}/api/courses/1/summary`, { headers: { Authorization: `Bearer ${__ENV.TOKEN}` } }); }
```

Run it with `k6 run --summary-export=summary.json load.js`, then `python scripts/latency_summary.py summary.json`.

## Pitfalls

- **Measuring on localhost.** That leaves out network, TLS, the hosting cold start and the database round-trip, which together are most of the real delay.
- **Load-testing production without permission.** Run load against a staging copy, or get written approval and a time window.
- **A mean as the only figure.** One 8-second cold start disappears into an average of 30 runs.
- **Lab-only Web Vitals presented as field results.** Say "Lighthouse lab" when that is what was measured.
- **Thresholds with no dataset size.** Ten rows render fast on anything, so a threshold without a dataset proves nothing.
