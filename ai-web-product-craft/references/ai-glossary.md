# AI & Web Product Glossary

Lookup reference for [ai-web-product-craft](../SKILL.md). Read a single entry when a term comes up — this file is not meant to be read start to finish.

Terms are grouped by the decision they inform. Where a term has a common misuse, the misuse is called out, because using these words loosely is how teams end up building the wrong thing.

---

## System shape

**Compound AI system** — A product feature built from several coordinated components (retrieval, one or more model calls, tool execution, validation, fallback) rather than a single model call. Most production AI features are compound systems; treating one as "just a prompt" is the usual reason quality plateaus. Improving a compound system usually means fixing the weakest non-model component, not swapping models.

**Orchestration** — The control flow that decides which component runs when: routing, retries, tool selection, termination. Distinct from the model itself. Failures here look like model failures but are not fixed by a better model.

**Agent** — A system where the model chooses its own sequence of actions against tools, rather than following a path the developer fixed in advance. Autonomy is a spectrum, not a binary. **Misuse:** calling any LLM feature an "agent." If the developer decided the steps, it is a workflow, and a workflow is easier to test, cheaper, and usually the right answer.

**Workflow (vs. agent)** — A predetermined sequence of steps, some of which call a model. Prefer this whenever the steps are knowable up front: it is debuggable, its cost is predictable, and it fails in ways you can enumerate.

**Tool / function calling** — Giving the model a typed interface it can invoke to read or change state. The quality of a tool-using feature is dominated by tool *description* quality and error-message quality, not by the model.

**RAG (Retrieval-Augmented Generation)** — Fetching relevant material at request time and putting it in the prompt, so the answer is grounded in your data rather than the model's training. **Misuse:** treating RAG as a fix for hallucination. It reduces unsupported claims about retrieved content; it does nothing about claims the retrieval did not cover.

---

## Prompting and context

**System prompt** — The persistent instruction block that establishes role, constraints, tone, and output format for every request. It is product surface area: it encodes policy decisions and should be reviewed and versioned like code, not edited casually in a dashboard.

**Context window** — The maximum number of tokens a model can attend to in one request, covering system prompt, conversation, retrieved material, tool definitions, and the response. Running near the limit degrades quality well before it errors.

**Context engineering** — Deciding what goes into the context window, in what order, and at what fidelity. The higher-leverage discipline compared to prompt wording: what you *include* matters more than how you phrase it. Includes summarization, retrieval ranking, and dropping stale conversation turns.

**Prompt engineering** — Crafting the instruction text itself: task framing, examples, output format, edge-case handling. Real but narrower than context engineering, and subject to diminishing returns.

**Few-shot / in-context learning** — Supplying worked examples in the prompt to demonstrate the task. Usually the cheapest large quality gain available, and the first thing to try before fine-tuning.

**Grounding** — Constraining output to supplied source material and, ideally, requiring citations. The main defence against confident fabrication in factual features.

**Prompt injection** — Instructions embedded in content the system ingests (a web page, a document, a user upload) that attempt to redirect model behaviour. The mitigation is architectural — never let ingested content authorize a side effect — not textual. Telling the model to ignore injections is not a control.

---

## Quality and failure

**Hallucination / confabulation** — Fluent output that is not supported by the source material or by fact. It is a property of how these models generate, not a bug to be patched away. Design so that unsupported output is *detectable and cheap*, via citations, confidence surfacing, and reversible actions.

**Calibrated trust** — The goal state where the user's confidence in the feature matches its actual reliability. Both directions are failures: over-trust means unchecked errors reach production; under-trust means the feature is ignored and the investment is wasted. Achieved by showing sources, marking uncertainty honestly, and making the feature's limits visible rather than papering over them.

**Automation bias** — The human tendency to accept a machine suggestion without the scrutiny they would apply to a human one. The stronger the UI implies authority, the worse it gets. A confident tone with no visible sourcing is the highest-risk combination.

**Eval (evaluation set)** — A fixed set of inputs with known-good outputs or graded criteria, used to measure change. Without one, every prompt edit is a guess. Build it before optimizing, not after something breaks.

**EDD (Eval-Driven Development)** — Writing the eval before the feature, then developing against it — the AI analogue of test-driven development. The discipline that converts prompt tweaking from folklore into engineering.

**Golden set** — A small, hand-curated, high-confidence subset of the eval, usually reviewed by a domain expert. Used as the final gate when the full eval is too large or too noisy to inspect.

**LLM-as-judge** — Using a model to grade another model's output against a rubric. Scales evaluation cheaply but inherits the judge's biases (notably toward length and confident phrasing). Always validate the judge against human labels before trusting its scores.

**Data drift** — Real input distribution moving away from what the system was built and evaluated against. Detected by monitoring input characteristics, not just output quality — by the time output quality drops, drift has been happening for a while.

**Model drift / regression** — Behaviour changing because the underlying model changed (a provider version bump, a different default). Pin model versions in production and re-run evals before adopting a new one.

**Graceful degradation** — Defined behaviour when the AI component is slow, unavailable, or low-confidence. Every AI feature needs a designed non-AI path. "The page hangs" is a design decision made by not making one.

---

## Responsible AI

**Model card** — Structured documentation of a model: intended use, training data characteristics, evaluation results, known limitations, and out-of-scope uses. Read the provider's card before choosing a model; publish your own for systems you ship to others.

**Fairness** — Whether outcomes differ across groups in ways that are not justified by the task. Requires a stated definition (equal outcomes? equal error rates? equal opportunity?) — these are mutually incompatible in general, so picking one is a product decision that must be made explicitly rather than defaulted into.

**Disparate impact** — A neutral-seeming rule producing systematically different outcomes across groups. Common in AI features because proxies for protected attributes are abundant in real data.

**Human-in-the-loop (HITL)** — A person reviews or approves before an action takes effect. Effective only when the reviewer has enough context and time to genuinely evaluate — a rubber-stamp confirmation dialog provides oversight theatre, not oversight.

**Human-on-the-loop** — A person monitors an autonomous system and can intervene, rather than approving each action. Appropriate when volume makes per-action review impossible; requires good observability and a fast, reliable stop control.

**Explainability** — Being able to say why a system produced a given output. For LLM features this usually means showing retrieved sources and the reasoning surface, not interpreting model internals.

**Data minimization** — Collecting and sending only the data the feature actually needs. The most reliable privacy control: data never sent to a provider cannot be retained, logged, or breached there. Check what your provider retains and for how long, and whether your inputs may be used for training.

**AI governance** — The organizational process defining which AI uses are allowed, who approves them, what evaluation is required before launch, and what monitoring is required after. Distinct from the technical controls; without it the technical controls get applied inconsistently.

---

## Performance (web delivery)

**TTFB (Time to First Byte)** — Delay from request to the first byte of response. Dominated by server processing, cold starts, and network distance. The metric most affected by cheap hosting tiers.

**LCP (Largest Contentful Paint)** — When the largest above-the-fold element finishes rendering. Core Web Vital; target under 2.5s. Usually fixed by prioritizing the hero image and eliminating render-blocking resources.

**INP (Interaction to Next Paint)** — Responsiveness across all interactions in a session, replacing FID. Target under 200ms. Dominated by long JavaScript tasks blocking the main thread.

**CLS (Cumulative Layout Shift)** — How much content jumps during load. Target under 0.1. Fixed by reserving dimensions for images, ads, and embeds before they load.

**Core Web Vitals** — The LCP / INP / CLS trio, measured at the 75th percentile of real users. Field data, not lab data, is what counts.

**Facade pattern** — Replacing a heavy third-party embed (video player, map, chat widget) with a lightweight placeholder that loads the real thing on interaction. Frequently the single largest performance win on a content page.

**Streaming (response)** — Sending output token by token as it is generated rather than waiting for completion. Does not reduce total latency, but transforms perceived latency — the most valuable UX change available to most LLM features.

---

## Related

- [ai-responsible-design](ai-responsible-design.md) — privacy, fairness, and trust in depth
- [ai-ux-patterns](ai-ux-patterns.md) — background vs. constrained vs. open-ended AI features
- [html-performance](html-performance.md) — delivery, caching, and lazy-loading detail
