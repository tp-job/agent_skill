#!/usr/bin/env python3
"""Turn a logo (local file or https URL) into the value for a draw.io style's image= key.

Usage:  python embed_logo.py logo.svg
        python embed_logo.py https://example.com/logo.png
Prints:  image=data:image/svg+xml,<base64>
draw.io splits styles at ';', so the usual 'data:...;base64,' form is written without ';base64'.
Python 3.8+, standard library only.
"""
import base64
import sys
import urllib.request
from pathlib import Path

TYPES = {".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg",
         ".jpeg": "image/jpeg", ".gif": "image/gif", ".webp": "image/webp"}
WARN_BYTES = 60_000


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = sys.argv[1]
    if src.startswith("https://"):
        with urllib.request.urlopen(src, timeout=20) as r:
            data = r.read()
        ext = Path(src.split("?")[0]).suffix.lower()
    elif src.startswith("http://"):
        sys.exit("use https")
    else:
        data = Path(src).read_bytes()
        ext = Path(src).suffix.lower()
    if ext not in TYPES:
        sys.exit("unsupported type %r; use svg, png, jpg, gif or webp" % ext)
    if len(data) > WARN_BYTES:
        print("note: %d KB; large logos bloat the file, prefer SVG or a smaller PNG" % (len(data) // 1000), file=sys.stderr)
    print("image=data:%s,%s" % (TYPES[ext], base64.b64encode(data).decode("ascii")))


if __name__ == "__main__":
    main()
