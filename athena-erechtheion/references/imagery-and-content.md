# Imagery and content — real words and real pictures before hi-fi

A layout is designed around the content it holds. Hi-fi drafted around lorem ipsum and random stock photos looks finished and then breaks when real content arrives. This file covers deciding what goes inside the boxes, before drafting fills them.

Use it between art direction and drafting, whenever a draft reaches rung 4 (hi-fi) or above.

---

## 1. Content first

Write a **content inventory** per screen before the hi-fi draft. It doesn't have to be final copy, but it has to be *real-shaped*.

| Slot | Write | Stress-test with |
| --- | --- | --- |
| Headline | the actual message, at its real length | the longest version the client might ask for |
| Names and labels | real examples from the domain | the longest name, and a name in another script |
| Numbers | realistic magnitudes | 6+ digits, negatives, zero, with currency and units |
| Lists | the real count | 0 items, 1 item, and 50 items |
| Empty / error text | the words the user will actually read | the error that happens most often |
| Alt text | a description of what the image is *for* | — |

**BAD:** `Lorem ipsum dolor sit amet` in the hero, and three testimonial cards with "John D.".
**BETTER:** "Book your check-up in two taps", with the real longest service name ("Annual comprehensive health screening, package B") placed in the card that has to hold it.

**Microcopy voice** (buttons, errors, empty states) follows the thesis. For UX-writing rules, open the google-design-system specialist through the fast path.

### Thai and other long scripts

| Issue | Rule |
| --- | --- |
| Stacked vowels and tone marks above and below the line | body line-height **≥ 1.6** for Thai. Latin-tuned 1.4 clips the marks |
| No spaces between words | line breaks need word segmentation: `word-break: normal` + `lang="th"`. Test a long paragraph, not one line |
| Thai glyphs sit visually smaller than Latin at the same px size | set Thai 1–2 px larger, or choose a family designed for both scripts |
| Pairing | pick a Thai family whose weight and x-height match the Latin one. Examples: IBM Plex Sans Thai (pairs with IBM Plex Sans), Noto Sans Thai, Anuphan, LINE Seed Sans TH. Check the licence of each. |
| Text expansion | translated UI runs about 30% longer than English (German, Thai). Leave the room in buttons and nav |

---

## 2. Imagery: decide the source by what the audience trusts

| Source | Choose when | Watch out for |
| --- | --- | --- |
| Own photography | real people, real product, real place: the most trust | budget, and consistency across shoots |
| Stock | generic contexts, and speed | the "stock look". Filter for one grade and one light direction |
| AI-generated | concepts, textures, abstract product scenes, moodboards | **never** show generated people as real customers, staff or testimonials. Hands and text still break |
| Illustration | abstract services, onboarding, empty states | style drift when several illustrators or tools are used |
| 3D render | products that don't exist yet, material studies | cost. A photo of a render is only an image, so it needs no three.js |
| None | dense tools and dashboards | the thesis must say so. Emptiness has to be a choice |

### Treatment rules, written once and applied to every image

Derive them from the thesis, then write them in the design record:

- **Grade:** warm or cool, saturation level, duotone, black-and-white.
- **Light:** one direction and one quality (soft or hard) across the whole set.
- **Crop and mask:** tight, loose or full-bleed; rectangle, circle or blob. One mask family per page.
- **Subject rule:** for example, "hands and objects, never faces", or "one person, looking away from the camera".

**BAD:** six stock photos, six lighting setups, one page.
**BETTER:** "Cool clinical grade, soft top light, circle masks for people and rounded rectangles for machines." Every photo is then chosen or generated against that sentence.

### Briefing a generated or commissioned image

```
Subject:     a robotic arm sorting pill blisters, close-up on the gripper
Composition: subject at the right third, empty left half for the headline
Light:       soft overhead, cool, no hard shadows
Lens/feel:   macro, shallow depth of field
Grade:       desaturated blue-white, matching the palette's surface colour
Avoid:       text, logos, people's faces
Aspect:      16:9 hero, safe crop for 4:5 on mobile
```

**Placeholders must be honest.** Until the real image exists, use a grey box labelled with the aspect ratio and the one-line brief. A random stock photo gets approved by accident.

---

## 3. Icons

- **One set, one stroke weight, one corner style.** Examples: Material Symbols, Lucide, Phosphor. Mixing sets is the fastest way to look templated.
- Size icons on the spacing grid (16, 20 or 24 px), and give them an optical nudge when they sit beside text.
- An icon with no label needs an accessible name. Unless the icon is universal, show a text label too.

---

## 4. Hand-off facts the build will need

Put these in the design record next to the tokens:

| Fact | Why |
| --- | --- |
| aspect ratio per image slot, for mobile and desktop | prevents layout shift (CLS) |
| the largest rendered width per slot | the build sizes `srcset` from it |
| which image is the hero (the likely LCP element) | it gets priority loading. Everything else lazy-loads |
| the format preference (AVIF or WebP with fallback) | file weight |
| the source and licence of every image and font | a design you can't legally ship isn't finished |

---

## Check before drafting hi-fi

- [ ] Every screen has a content inventory with real-shaped copy, and there is no lorem ipsum in hi-fi
- [ ] The longest string, the empty state and the error state are drawn
- [ ] Thai (or other script) line-height and font pairing are chosen, if in scope
- [ ] The image source and treatment rules are written, with one mask family per page
- [ ] No generated person stands in for a real customer
- [ ] Placeholders are labelled boxes, not random photos
- [ ] Licences are recorded
