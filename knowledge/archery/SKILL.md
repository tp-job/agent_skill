---
name: archery
description: >-
  Plans a lesson or training session and builds the slides that carry it, as one job: write the
  learning target, choose a teaching method that fits it (demonstration, role play, case study,
  game, simulation, concept attainment, or a plain explanation), lay out the session, design
  slides that support the teaching, add active-learning moments, make the deck accessible, and
  deliver it. Any subject, for school, university, workshops and corporate training, in PowerPoint,
  Google Slides, Keynote or Canva. Trigger for: "plan a lesson", "make teaching slides", "how should
  I teach this", "make my slides less boring", "one slide one idea", "add an activity to my
  lesson", "สร้างสื่อการสอน", "ทำสไลด์สอน", "วิธีสอน", "แผนการสอน", "ทำ PowerPoint ให้น่าสนใจ".
  Not for writing CLOs, syllabi, exams or rubrics for a whole course, a sales, investor or
  conference deck meant to persuade rather than teach, generating a .pptx file from code, or
  live one-on-one tutoring in the moment.
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "1.0.0"
  source: >-
    Six public guides, five read in full and one in part: a Thai guide to 21 teaching methods
    (kru2day, 2017, after Tisana Khammani 2000), Northern Illinois University CITL "Teaching with
    PowerPoint", and four slide guides (IT-Guides 2026, COMSIAM, Teachers Tech, KCT Academy 2024).
    Numeric slide limits are the guides' own recommendations, not measured findings (compiled 2026)
---

# Archery

**Archery** — one discipline in four motions: choose the target, aim, draw, release. A lesson misses the way an arrow does: aimed at nothing, aimed at the wrong thing, or released before it was drawn. The slides are the bow, and they are not the arrow. They carry the lesson, but they are not the lesson.

```
  TARGET ──► AIM ──► DRAW ──► RELEASE ──► SCORE
  what can   which   slides   deliver     did they
  the learner method and the  it live     hit it?
  do after?          session
```

| Stage | Produces | Done when | Depth |
| --- | --- | --- | --- |
| **Target** | one sentence: who can do what, checked how | a stranger could tell from it whether the lesson worked | Stage 0 below |
| **Aim** | a method for that target, and a session outline with timings | every minute of the session has a job | [teaching-methods](references/teaching-methods.md) · [lesson-structure](references/lesson-structure.md) |
| **Draw** | the slides, one idea each, plus the active-learning moments | every slide passes the three-second test | [slide-design](references/slide-design.md) · [engagement-activities](references/engagement-activities.md) · [tools-and-ai](references/tools-and-ai.md) |
| **Release** | an accessible deck, a pre-flight check, and a plan B | the file opens on the real machine and the backup exists | [accessibility-and-delivery](references/accessibility-and-delivery.md) |
| **Score** | evidence that the target was hit, and what to change | the check from Stage 0 has been run | Stage 0 and [lesson-structure](references/lesson-structure.md) |

Fill-in template for the whole job: [lesson-plan-template](assets/lesson-plan-template.md). Trigger tests for this skill's description: [trigger-evals](assets/trigger-evals.json). Where each rule comes from and how far to trust it: [sources](references/sources.md).

---

## Fast path

When the request names its need, skip the stages and open the file.

| The request is… | Open now |
| --- | --- |
| "How should I teach X?", "which method", role play, case, game, simulation | [teaching-methods](references/teaching-methods.md) |
| Turn a topic into a session with timings, an opening and a summary | [lesson-structure](references/lesson-structure.md) |
| Fix or build slides: too much text, fonts, colours, charts, animation | [slide-design](references/slide-design.md) |
| Make the class participate: quiz, poll, pair work, feedback | [engagement-activities](references/engagement-activities.md) |
| Accessibility, handouts, presenting, the file must work tomorrow | [accessibility-and-delivery](references/accessibility-and-delivery.md) |
| Using Canva, PowerPoint Designer or AI to build the deck | [tools-and-ai](references/tools-and-ai.md) |

Everything else, such as a lesson that starts as a topic or a deck that needs a lesson behind it, starts at Stage 0.

---

## Stage 0 — write the target

Before choosing a method or opening PowerPoint, answer four questions in writing. One line each is enough for a short session. Never zero.

| Question | BAD | BETTER |
| --- | --- | --- |
| Who is learning? | "students" | "Year 10, mixed ability, first time seeing ratios" |
| After the session they can… | "understand ratios" (not observable) | "scale a recipe from 4 to 6 servings without help" |
| Time and setting? | "a lesson" | "45 min, projector, 30 students, no devices" |
| How will we know? | "they seemed to get it" | "3-question exit ticket; 80% get all three right" |

**Why the verb matters:** "understand" can't be checked, but "scale a recipe" can. The verb picks the method: watching a procedure calls for a different method than weighing a dilemma. The mapping is in [teaching-methods](references/teaching-methods.md).

If the target can't be checked, don't build slides yet. A deck built on an unchecked target looks finished and teaches nothing you can prove.

---

## Sizing: how much for how much

Running every stage at full weight for a five-minute explanation is this skill's failure mode.

| Job | Target | Aim | Draw | Release |
| --- | --- | --- | --- | --- |
| A 5-minute explanation or one concept | one line | usually plain explanation + one example | 3–6 slides | open the file once beforehand |
| One lesson (45–60 min) | four lines | one method plus a short summary | 20–45 slides at most, see the timing rule | full pre-flight |
| A workshop or training day | four lines per block | a method per block, with breaks | a master template, and a deck per block | full pre-flight, plus handouts |
| Self-paced or online | four lines | shorter chunks, more visuals | larger type, short slides | test on a phone |

---

## Operating rules

- **The target is never skipped, only sized.**
- **Aim before you draw.** Choose the method before the slides. A method changes what the slides look like, and a slide deck can't repair a method that doesn't fit the target.
- **One slide, one idea.** More slides beat denser slides.
- **If it has to be read, it's a handout.** Slides cue the talk. Don't put the lecture on them.
- **Every method ends in a summary.** The activity is the means, and the debrief is where the learning is consolidated.
- **Slide counts are not minutes.** A discussion slide can take ten minutes, so plan by minutes and let the slide count follow.
- **Numbers in the slide guides are guidance, not evidence.** They come from practitioners. Use them as defaults, then check with the back-row test on the real screen.
- **Never claim "accessible" without a check** that was actually run.
- **Verify what AI wrote.** Generated content goes through the same fact-check as any source.
- **Test the file on the machine that will present it,** and keep a backup format.

---

## When not to use this

- **Designing a whole course.** Outcomes, syllabi, exams and rubrics for a full programme are course-design work. Archery starts once a lesson exists to teach.
- **Persuasion decks.** Sales, investor and conference decks have a different target (a decision, not a skill). Rules like "one idea per slide" travel well, but the method and activity guidance doesn't.
- **Building the file.** This skill decides what goes on each slide. Producing the .pptx programmatically is file mechanics.
- **Live tutoring.** When one student needs an explanation now, explain it. Don't wrap that moment in a lesson plan.
- **A lesson someone else has already planned** that just needs a visual polish. Go straight to [slide-design](references/slide-design.md).
