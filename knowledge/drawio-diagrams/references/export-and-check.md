# Export and check

## Files to leave behind

| File | Purpose |
| --- | --- |
| `<name>.drawio` | Source; edit this |
| `<name>.drawio.svg` | Shareable picture that still opens for editing in draw.io |

## Make the `.drawio.svg`

draw.io desktop, if installed (`drawio --help` lists the exact flags for your version):

```bash
drawio -x -f svg -e -o diagram.drawio.svg diagram.drawio
```

`-e` embeds the diagram so the SVG stays editable. Without the desktop app, open the `.drawio` in draw.io (app.diagrams.net), then File → Export as → SVG, tick **Include a copy of my diagram**, and tick **Embed fonts** if offered.

The validator reads the embedded copy, so run it on the `.drawio.svg` too:

```bash
python scripts/validate_drawio.py diagram.drawio.svg --strict
```

## Look at it

The script cannot see these; check them on a rendered view:

| Check | Fix |
| --- | --- |
| Two lines cross | Move a box, or change which side the line leaves from (`exitX`/`entryX`) |
| A line passes through a box | Add a waypoint, or reorder the boxes |
| Thai text is clipped or wraps to 3 lines | Widen the box; do not shrink the font |
| A line label sits on top of another line | Move the label or widen the gap to 100 |
| A logo is blurry | Switch to SVG or a larger PNG |
| The font looks like Helvetica | `fontSource` missing or the machine is offline; confirm in the export dialog |

## Report back

State: the file paths, what the diagram says in one sentence, what the focus colour marks, and any rule you bent (for example a 10th box kept in one frame) with the reason.
