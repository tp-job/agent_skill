# Thorough-Thinking Framework (Reference)

Seven habits a genuinely senior person applies before committing to an answer. Source concepts (English originally paired with Thai translations for personal reference): Think Thoroughly, Cover All Bases, Consider All Use Cases, Think Holistically, Edge-Case Analysis, First-Principles Thinking, Pre-Mortem.

This isn't a template to print in every answer — it's a pass to run silently so the *answer itself* is better. See SKILL.md Step 2 for when to surface any of it explicitly.

---

### 1. Think Thoroughly
Don't settle for the first plausible answer. Ask: have I actually considered this from more than one angle, or did I just pattern-match to something familiar?

### 2. Cover All Bases
Before finalizing, ask: what would have to be true for this to go wrong operationally — deployment, rollback, monitoring, ownership? A good answer accounts for what happens *after* the happy path, not just the happy path.

### 3. Consider All Use Cases
Ask: who else touches this besides the person in front of me right now? New users, power users, admins, the on-call engineer, the next developer who reads this code. A recommendation that only works for the primary persona isn't finished.

### 4. Think Holistically
Ask: does this decision look good in isolation but cause a problem one level up? Optimizing a single component at the expense of the system it lives in is a classic failure mode for narrow technical thinking — senior leadership thinking zooms out first.

### 5. Edge-Case Analysis
Ask: what's the rare or extreme version of this scenario, and have I said what happens there? Empty states, zero values, concurrent writes, network partition, malformed input, adversarial input. Naming the edge case explicitly is the difference between "I considered it" and actually having considered it.

### 6. First-Principles Thinking
Ask: am I recommending this because it's genuinely the right fundamental approach, or just because it's the conventional one? Strip away "that's how it's usually done" and check the reasoning still holds.

### 7. Pre-Mortem
Ask: imagine this shipped and it failed in six months — what's the most likely reason? If you can name a believable failure story, that's a risk worth addressing now, not after it happens.

---

## How to apply this without sounding like a checklist

Run all seven as a quick internal pass on every substantive request — it costs nothing to think it, and most of the time it just sharpens the answer without needing to be spelled out.

Surface a finding out loud only when it's actually load-bearing:
- A genuine edge case the user likely hasn't considered yet
- A pre-mortem failure mode worth a one-line flag
- A holistic tradeoff that changes the recommendation

When you do surface it, keep it to a sentence or a short bullet folded into the answer — not a labeled seven-part report. The goal is an answer that's obviously been thought through, not a visible audit trail.