---
name: web-design-trends
description: >-
  Turns a year's web design trends into deliberate design decisions, filed by year. Picks the trend
  file for the year the site launches, separates baseline rules every site owes (accessibility,
  intentional motion, fluid layouts) from statement trends a brand opts into (cinematic heroes,
  typographic statements, interactive 3D, mixed scroll directions, noise and chromatic mash-ups,
  illustrated worlds, exploratory layouts, AI-assisted personalisation), then scores each
  candidate on thesis fit, build cost, accessibility risk and shelf life before one or two are
  adopted. Use when asked "what's trending in web design", "web design trends 2026", "is this
  design dated", "make it feel current", "modern website style for this year", or "เทรนด์เว็บดีไซน์
  2026". Not for a whole design job from scratch, for Material 3 conformance, or for implementing
  a 3D scene.
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "1.0.0"
  source: >-
    2026 file compiled from Sam Crawford, "The New Rules of Web Design for 2026" (bycrawford.com,
    dated 16 Feb, year taken from the title) and Iveta Pavlova, "Web Design Trends 2026" (reallygooddesigns.com); risk and
    shelf-life scoring is this skill's own assessment (compiled 2026)
---

# Web Design Trends

A trend is a **lever, not a goal**. A trend list tells you what other sites are doing. It says nothing about whether this site should. This skill turns a year's trends into one or two choices you can defend, and keeps the rest out.

---

## 1. Pick the year file by launch date

Design for the year the site **goes live**, not the year the brief was written. A site briefed in November and launched in March belongs to next year.

| Launch year | Read |
| --- | --- |
| 2026 | [2026](references/2026.md) |
| a year with no file | the latest file, and say so. Then add the new year with [year-template](assets/year-template.md) |

**Version note:** a year file is a snapshot of opinion articles, not measured data. Neither 2026 source cites statistics. Treat every trend as a claim about taste, and check it against the site's own audience.

---

## 2. Baseline vs statement

Every year file splits trends into two kinds. Handle them differently.

| Kind | What it is | How to use it |
| --- | --- | --- |
| **Baseline** | rules every current site owes its users, such as accessibility from day one, motion with a purpose, and fluid layouts | apply all of them, always. Missing a baseline rule is a defect, not a style choice |
| **Statement** | a visible aesthetic a brand opts into, such as a cinematic hero, oversized type, 3D, or grain and glow | pick **one, at most two**, per site. Three statements compete, and the site reads as a trend collage |

**BAD:** "Make it 2026: add 3D, a cinematic video hero, horizontal scroll, grain, and illustrations."
**BETTER:** "Baseline rules applied. One statement: typographic hero, because the brand is a writing studio and its product *is* words. Everything else stays quiet."

---

## 3. Score each candidate statement

Score before adopting. Write the scorecard down, and keep the losers visible so the choice can be revisited.

| Criterion | 3 | 1 |
| --- | --- | --- |
| **Thesis fit:** does the trend say what the brand is? | the trend *is* the brand's subject (type for a writing studio, 3D for a product you want to handle) | decoration borrowed from elsewhere |
| **Audience fit** | the audience expects or enjoys it | the audience is in a hurry, on low-end devices, or needs to trust the site |
| **Build cost** (inverse) | CSS only | a 3D pipeline, a video shoot, or commissioned illustration |
| **Accessibility risk** (inverse) | no new risk | motion or flashing, unreadable text over media, or non-standard navigation |
| **Shelf life** | a craft skill that ages slowly (typography, good photography) | a visual fad with a recognisable year stamp (glitch, heavy grain) |

**Adopt only a statement that scores 3 on thesis fit.** A high total with low thesis fit is still decoration. For each adopted statement, write its **risk guard** from the year file: the reduced-motion path, text alternative, fallback or budget that makes it safe.

---

## 4. Write the decision down

```markdown
Trends — <site>, launch <year>, file <year>.md
Baseline:   all applied (a11y from day one · motion with purpose · fluid · personality · AI as tool)
Statement:  <trend> — thesis fit: <one line> — guard: <reduced-motion / fallback / budget>
Rejected:   <trend> (<lowest criterion>), <trend> (<lowest criterion>)
Review by:  <launch year + 1>. A statement's shelf life is the reason for this date.
```

---

## 5. Adding a year

Copy [year-template](assets/year-template.md) to `references/<year>.md`. Rules:

- **Read the sources in full.** Summaries of trend articles are unreliable: they invent caveats, statistics and example sites the article never mentioned. Record what the author wrote, and label your own assessment as yours.
- **At least two independent sources.** One article is one person's taste.
- **Carry baseline rules forward** unless a source gives a reason to drop one. Baselines accumulate; statements rotate.
- **Mark returning trends.** A trend that appears in three consecutive years is on its way to becoming a baseline or a cliché. Say which.
- Add the row to the table in §1.

---

## When not to use this

- **The brand already has a strong system.** A trend layered on top dilutes it. Only baseline rules apply.
- **Products and tools** such as dashboards and admin panels. Their users want speed and familiarity. Apply the baseline and skip statements.
- **"Make it trendy" with no brief behind it.** Write the target and the visual thesis first. Without a thesis there is nothing to score thesis fit against.
