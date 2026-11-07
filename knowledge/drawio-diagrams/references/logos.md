# Logos

A logo helps a reader who does not know the name. It never replaces the name.

## When to use one

| Use | Skip |
| --- | --- |
| A product or service the reader may have seen (Google, Supabase, React) | A part the reader's own team built |
| A part whose name alone says nothing to a newcomer | A step in a flowchart |
| System overview and sequence participants | ER entities, use-case actors |

## How

1. Get the logo as SVG when possible (small and sharp), else PNG at 128px or larger.
2. Embed it: `python scripts/embed_logo.py logo.svg` prints `image=data:image/svg+xml,...`. Put that in the LOGO style from [style-spec.md](style-spec.md).
3. Size 64 × 64, name beneath at 16px, one logo per part.

Never link a logo by URL. A CDN link breaks when the file is opened offline, exported, or when the host changes, and the validator rejects it.

## Data URI note

draw.io splits a style at every `;`, so write `data:image/png,<base64>` with no `;base64`. A standard data URI cut at the semicolon shows as a broken picture; the validator flags it.

## Sources

| Source | Good for | Licence note |
| --- | --- | --- |
| Devicon (devicon.dev) | Programming languages and frameworks | MIT; check each mark's brand terms |
| Simple Icons (simpleicons.org) | Single-colour brand marks | CC0; brand terms still apply |
| The product's own press or brand page | Anything else | Follow the terms posted there |

Use a mark to refer to its own product, unaltered. Do not recolour, crop or combine marks.

## Colour

Logos keep their own colours; they are pictures, not diagram ink. If the reader will print in black and white, use the single-colour version.

## Size budget

Keep the file small: a diagram with more than about 12 logos, or any logo over 60 KB, is a sign the diagram is carrying too much or the image should be SVG.
