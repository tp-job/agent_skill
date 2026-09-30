# Review — critique a draft before it leaves the room

The fifth discipline. Drafting produces something that *looks* finished. Review is what finds out whether it *is*, measured against what was written down before the draft existed: the target, the thesis and the never-rules. It is not measured against taste in the moment.

This file reviews a **draft**. Auditing a shipped product for dark-mode bugs, hard-coded colours or regressions is a UI-audit task in another skill.

---

## 1. Critique grammar: observation → impact → fix

A finding that can't be acted on is an opinion. Write every finding in three parts, and point at the element.

| BAD | BETTER |
| --- | --- |
| "The hero feels weak." | "Hero headline is 32 px against 18 px body, a 1.8× jump. The squint test leaves three equal blocks, so nothing leads. Take the headline to 64 px (3.5×) and drop the subhead to muted." |
| "Colours are off." | "The CTA red `#E8453C` also appears in 4 decorative dots, so the eye can't find the action. Remove the red from the dots, per never-rule 2." |
| "Make it pop." | (not a finding: delete it) |

**Also list what works and must be kept.** Without that list, the next iteration "fixes" the strong parts too.

---

## 2. The passes, cheapest first

Run them in order and stop at the first pass that turns up a blocker. There is no point checking contrast on a layout that is about to change.

| # | Pass | How to run it | Blocker when |
| --- | --- | --- | --- |
| 1 | **Thesis fit** | Read the thesis, then look at the draft for 5 seconds. Does a stranger's first impression match the thesis's feeling? Check each never-rule by name. | a never-rule is broken, or the draft reads as a different brand |
| 2 | **Target fit** | Re-run the Stage 0 "judged how" test: the task, the time, the reader. | the target's test fails |
| 3 | **Hierarchy (squint)** | Blur the view (or screenshot and downscale to about 10%). List what is still readable. | more than three things survive, or the wrong one leads |
| 4 | **Real content** | Replace placeholder text with the longest real strings, including Thai or other long scripts, 6-digit numbers and the empty state. See [imagery-and-content](imagery-and-content.md). | text overflows, truncates meaning, or the layout depends on lorem length |
| 5 | **Responsive** | Render at **375, 768 and 1440 px** wide, and at 200% zoom. | horizontal scroll, overlapping elements, targets under 24 px, or a line under ~30 characters in body text |
| 6 | **States** | Walk through the inventory from architecture: empty, loading, error, long, and first-run. | an in-scope state is undrawn |
| 7 | **Access** | Contrast ratio on every text pair (script below), a visible focus state, target size, and a reduced-motion path. | body text below 4.5:1, large text or UI below 3:1, no focus state |
| 8 | **Craft** | Alignment to the grid, consistent radii and spacing steps, orphaned words in headlines, optical centering of icons. | never a blocker: this is polish |

**Sized to the draft's rung** (see [drafting](drafting.md) §1): a wireframe gets passes 1–3 only. A hi-fi screen gets 1–8. A prototype also gets a hallway test of the flow.

---

## 3. Running the passes with tools

Where a browser is available, render the draft instead of imagining it:

| Check | With a browser pane | Without one |
| --- | --- | --- |
| Responsive | resize to each width, then screenshot | say "not run" in the record, and don't estimate |
| Squint | screenshot, then view at small scale | describe it from the layout and mark it *estimated* |
| Focus | tab through the page and screenshot each focus | read the CSS for `:focus-visible` rules |
| Contrast | compute it, below | compute it, below |

Contrast is arithmetic, not an eyeball judgement (WCAG 2.x relative luminance):

```python
def lum(hex_):
    r, g, b = (int(hex_.lstrip("#")[i:i+2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

def ratio(a, b):
    hi, lo = sorted((lum(a), lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)

print(f"{ratio('#8a8a8a', '#ffffff'):.2f}:1")  # 3.45:1, which fails body text (needs 4.5:1)
```

**Colour-mode rule:** if the target includes dark mode, run passes 3 and 7 in **both** modes. A pair that passes in light mode tells you nothing about dark mode.

---

## 4. Output: the review note

```markdown
## Review — <draft name>, rung <n>, <date>

Keep:     <2–4 things that work, with the reason>
Blockers: <finding: observation → impact → fix>   (must fix before hand-off)
Major:    <…>                                      (fix in this iteration)
Minor:    <…>                                      (fix if cheap)
Not run:  <passes skipped and why>
```

Copy the checks that actually ran into the design record's "Checks run". Copy "Not run" into "Open".

---

## 5. Loop limits

- **Fix blockers, then re-run only the passes those blockers touched.** You don't need all eight again.
- **Two review loops at most.** If blockers survive a second loop, stop polishing: the thesis or the target is wrong. Go back one stage and ask the lead one question. This is the same stop rule as three rejected drafts.
- **Never review your own draft as "fine" without running a pass.** "Looks good" with nothing in "Not run" is a claim with no evidence.

## When not to review

- Exploration and mood play, which have no target to review against.
- A rung-1 sketch whose only question was "what goes where". Once that question is answered, the job is done.
