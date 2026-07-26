# Credits

This skill's overall shape — a `.raw/` + generated-notes split, a compact
`hot.md` rolling-context cache, a master `index.md`, and per-entity/concept
notes stitched together with wikilinks — was inspired by the public
"LLM Wiki" pattern for Claude + Obsidian, as implemented in:

- AgriciDaniel/claude-obsidian — https://github.com/AgriciDaniel/claude-obsidian
- kepano/obsidian-skills — https://github.com/kepano/obsidian-skills (Obsidian's
  own agent-skills reference for Markdown, Bases, and JSON Canvas conventions)

The pattern itself traces back to Andrej Karpathy's description of an "LLM wiki"
as a persistent, compounding knowledge base that an agent maintains over time.

This SKILL.md is an original, independently written implementation of that idea
scoped down to a single self-contained skill file — it does not reuse code or
prose from the projects above. If you want the full multi-skill system (ingest
pipelines, methodology modes, canvas orchestration, autoresearch loops, MCP
server wiring for the Obsidian REST API, etc.), see the claude-obsidian repo
directly.