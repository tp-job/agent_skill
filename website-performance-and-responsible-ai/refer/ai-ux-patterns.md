# Designing the AI user experience

Source: web.dev Learn AI — "Designing the AI user experience."

From a user's perspective, AI systems are inherently uncertain — they can produce inconsistent results and fail in unpredictable ways. The interface is where you absorb, filter, and reduce the frustration that comes from those limitations. As the builder, you usually understand far better than the user where and how the AI is likely to fail, which makes the UI decisions below your responsibility, not the model's.

The central design question is **how much control the user has over the AI**. Some opportunities are invisible to the user; others involve explicit interaction. More exposure means more flexibility, but also more risk and complexity to manage. There are three exposure patterns: **background**, **constrained**, and **open-ended**.

## Background AI

Runs automatically, with no user trigger and often no user awareness that AI is involved at all. The product as a whole — not the user — is responsible for the feature's benefit, reliability, and graceful degradation.

Best suited when:

- the task is low-risk,
- user control wouldn't meaningfully improve the outcome, and
- the product still delivers its core value even if the AI feature fails or is unavailable.

Common examples: spam filters, entertainment recommendations, automatic video-call background blur. Many of these don't even register as "AI" to the end user — and that's often the point.

### Worked example: AI-generated review summaries

A product page with hundreds of reviews makes it hard for a shopper to judge what matters to them. Background AI can surface recurring themes (e.g., "sound quality," "battery life" for headphones) as a personalized highlight, reducing cognitive load and speeding up the decision. Because the summary is personalized per user, prefer a client-side/on-device platform (built-in AI, a Summarizer API) for privacy and latency reasons — see the privacy guidance in [[ai-responsible-design]].

### Best practices

- **Keep transparency lightweight.** A small, neutral label ("Summary," "Key insights") plus optional progressive disclosure (a tooltip) is usually enough.
- **Allow opt-out.** Reactions to AI vary — some users find it intrusive. Give a clear way to turn the feature off.
- **Watch your wording carefully.** Summaries should state trends, not assertions — add system-prompt rules to reduce overconfident phrasing.
- **Design a graceful no-AI fallback.** If the model is unavailable for a technical reason, the page should still show the underlying content (reviews) without the summary, then backfill once the model loads.
- **Minimize setup friction.** A first-time client-side model download can be disruptive — show the feature's value before triggering it, add a limited server-side fallback, or push the download to a later point in the user's journey.

## Constrained AI

Triggered by an explicit user action — usually a link or button — rather than running automatically. The developer encodes task, intent, constraints, and output format in the system prompt; unlike open-ended prompting, the user has little to no choice beyond starting the task and receiving the output. Scoping the AI tightly this way keeps behavior predictable. Like background AI, this pattern pairs well with a client-side model fine-tuned for the specific task.

### Worked example: title generation

A writing tool can use AI to help authors generate considered, on-topic headline options. The system prompt encodes the task, style constraints, and output structure; the UI sends only the post content, and a client-side implementation makes repeated runs free after initial setup. A server-side path is worth considering for domains needing deeper expertise (e.g., titles for a scientific journal).

### Best practices

- **Communicate clearly and confidently.** A specific action label beats generic phrasing — e.g., "Show titles" rather than "Ask AI." If the feature's latency is genuinely low, a label implying the result is already ready ("Show titles") sets better expectations than one implying work is about to start ("Generate titles").
- **Keep users engaged.** A small amount of friction (e.g., offering multiple options instead of one) keeps users alert and prevents them from feeling stuck with output they dislike; users should be able to explicitly accept or edit a result before it's saved.
- **Precompute where possible**, especially for client-side tasks, so results feel instant.
- **Support fast iteration.** Regeneration should be cheap, easy, and reversible, with an explicit undo. Use those interactions as feedback signal to improve future runs.
- **Add fine-grained controls if needed** (tone tags, length options, preset styles) — demand for finer control tends to grow over time as users' confidence and needs evolve, so build a feedback loop to track that.

### Background vs. constrained — same feature, different framing

The same underlying capability can be exposed either way depending on visibility, cognitive load, and timing — not on what it's technically capable of. For example, instead of requiring an explicit click, a title-suggestion feature could precompute suggestions in the background while the user writes, then surface them the moment they focus the title field.

Background framing works best when:

- the input the feature needs is already available by default,
- there are only a small number of AI-driven features competing for attention,
- the cost of precomputing is low, and
- a suggestion can be woven in without interrupting the user's current task.

Constrained framing fits better for products with several distinct AI actions, where an explicit trigger avoids unnecessary computation and gives users a stronger sense of intent and control.

## Open-ended AI

Lets the user drive the AI's behavior directly through free-form input — natural language instead of a predefined action. The system interprets intent, fills in missing context, and infers what to do next.

Input is highly personal and often unpredictable, so the system has to absorb that variance. This pattern offers the most flexibility and also carries the most UX risk:

- user input may be unclear or incomplete,
- output is harder to predict,
- there's a meaningfully higher chance of an incorrect or misleading answer,
- the risk of over-trust is higher, and
- the surface is more exposed to adversarial probing (attempts to get the system to produce inappropriate content).

If you're new to building AI features, start with background or constrained AI and grow into open-ended surfaces once you have evidence the underlying model/system performs reliably enough.

### Worked example: open-ended customer support agent

Support spans a wide range of issues — order tracking, returns, product questions, shipping problems, edge cases that don't fit a predefined flow. After constrained AI handles the most common single actions, an open-ended agent adds the flexibility to resolve unusual or compound requests, reduce wait times and support cost, and give immediate help across many topics without a rigid multi-step flow. Ultimately you're responsible for handling this input variance responsibly — even while hoping users exercise good judgment and arrive at properly calibrated trust, you may still be accountable for incorrect answers the model offers. Most production open-ended systems run server-side, often composed with other components (databases, external tools, business logic) into a compound AI architecture, and should have a clear handoff path to a human agent.

### Best practices

- **Guide users toward clear intent** — prompt suggestions ("I want to return an item") and suggested follow-ups reduce ambiguity.
- **Show system state and assumptions** — the agent should state what it understood ("It looks like you're asking about order 12345") and what data it used.
- **Confirm before acting**, especially for sensitive actions (returns, refunds, address changes) — summarize the action and ask for explicit confirmation first.
- **Design for correction and re-grounding** — users should be able to correct a misunderstanding, rephrase, or roll back the conversation without starting over.
- **Pair with constrained shortcuts.** Too much back-and-forth frustrates users — add structured elements as shortcuts, e.g., a clickable, editable order-number chip instead of forcing the user to retype it in prose.
- **Surface uncertainty and limits.** The agent should acknowledge uncertainty, signal missing information, and hand off to a human smoothly when confidence is low.

This pattern requires users to evaluate responses carefully and understand when to escalate — design the surrounding UX to support that, not undermine it.

## Quick reference table

Paraphrased from the source's UX-pattern matrix (required = needed for this exposure type; optional = situational; not needed = generally skip):

|UX theme|Pattern|Background|Constrained|Open-ended|
|---|---|---|---|---|
|Transparency|Explicit "AI used" labeling|optional|required|required|
|Transparency|Lightweight explanation of AI behavior|optional|optional|required|
|Transparency|Visible system state/assumptions|not needed|optional|required|
|Guidance|Prompt suggestions|not needed|optional|required|
|Guidance|Structured input (tags, presets)|not needed|optional|optional|
|Control|Explicit AI trigger|not needed|required|required|
|Control|Preview before applying output|not needed|required|required|
|Control|Multiple options|not needed|optional|optional|
|Control|Regenerate|not needed|optional|required|
|Control|Undo|not needed|required|required|
|Trust calibration|Careful wording|required|required|required|
|Trust calibration|Confidence indicators|optional|optional|required|
|Risk/failure handling|Intentional friction/checkpoints|not needed|optional|required|
|Risk/failure handling|Escalation to a human|not needed|not needed|optional|
|Risk/failure handling|Graceful no-AI fallback|required|required|required|

A short note worth keeping in mind when scoping any of this: once a technique works reliably enough, people generally stop calling it "AI" at all — a useful gut check for whether a feature needs explicit AI framing in the UI, or should just be a good silent default.

## Further reading

- Google's People + AI Guidebook
- Microsoft's HAX Toolkit, particularly its human-AI interaction guidelines
- "The Shape of AI" by Emily Campbell
- "The Art of AI Product Development," chapter 10