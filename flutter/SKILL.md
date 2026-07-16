---
name: flutter
description: >-
  Flutter application engineering skill covering architecture, layout debugging, responsive design, and widget previews. Use this skill when building, structuring, refactoring, or debugging Flutter/Dart apps. Also trigger for: "structure my Flutter project", "fix RenderFlex overflowed", "Vertical viewport was given unbounded height", "make this responsive on tablet and mobile", "add a widget preview", "Flutter architecture", "Flutter layout error", or any Flutter/Dart UI or structure request. Routes to the focused reference guides under refer/.
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "1.0.0"
  source: Flutter engineering best practices (compiled 2026)
---

# Flutter — Application Engineering

This skill bundles focused Flutter/Dart guides. Read the reference that matches the task; each is self-contained.

## When to use this skill

- Structuring a new Flutter project or refactoring for scalability
- Fixing layout errors (overflows, unbounded constraints)
- Making a UI adapt across mobile, tablet, and desktop
- Adding interactive widget previews for UI components

## Reference guides

| Guide | Use when |
|---|---|
| [refer/flutter-architecture.md](refer/flutter-architecture.md) | Architecting an app with the recommended layered approach (UI, Logic, Data) — new projects or scalability refactors. |
| [refer/flutter-layout-issues.md](refer/flutter-layout-issues.md) | Fixing layout errors such as "RenderFlex overflowed" or "Vertical viewport was given unbounded height". |
| [refer/flutter-responsive.md](refer/flutter-responsive.md) | Building responsive layouts with `LayoutBuilder`, `MediaQuery`, and `Expanded`/`Flexible` across form factors. |
| [refer/flutter-preview.md](refer/flutter-preview.md) | Adding interactive widget previews via the `previews.dart` system when creating or updating UI. |

## How to work

1. Identify which of the four problem classes the task falls into (architecture, layout bug, responsiveness, previews).
2. Open the matching reference guide and follow its steps.
3. If a task spans multiple areas (e.g. a new responsive screen with previews), consult each relevant guide in order.
