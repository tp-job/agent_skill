# Capability inventory — what is really loaded

The first step of every orchestration pass. The model's belief about its tools is not the tool list; check it.

---

## 1. The five layers

| Layer | What it is | Where it shows up | Cost in context |
| --- | --- | --- | --- |
| **Built-in tools** | file, shell, search, edit | always in the tool list | fixed |
| **Skills** | packaged instructions, loaded on demand | a name + description listing; body loads when invoked | description always; body only when used |
| **MCP servers** | external processes exposing tools, resources, prompts | tools named `mcp__<server>__<tool>`; some deferred | full schema when loaded; name only when deferred |
| **Subagents** | separate model instances with their own context | an agent-type listing | a cold start per spawn |
| **Model + effort** | which model answers, and how hard it thinks | session settings | the whole session |

---

## 2. Take the inventory

Answer these in order; stop when the job's capability is found.

1. **Is there a dedicated skill?** Scan the skill listing for the job's trigger phrases.
2. **Is there a connected MCP tool?** Look for `mcp__<server>__*` in the loaded tools.
3. **Is it deferred?** Search the deferred list by keyword before concluding it is absent.
4. **Is the server connecting, unauthenticated or failed?** Check the session's server-status notices — see [mcp-lifecycle](mcp-lifecycle.md).
5. **Only then:** it is genuinely unavailable. Say which of steps 1–4 you checked.

**BAD:** "I don't have access to your calendar."
**BETTER:** "The calendar server is configured but needs authorisation — connect it in the connector settings, then I can list next week's events."

---

## 3. Budget the context

Every loaded schema and every skill description occupies context in every turn.

| Situation | Move |
| --- | --- |
| 20+ servers, most unused this task | leave them deferred; load only what the job needs |
| A skill library with overlapping triggers | put adjacent skills behind one router skill so only one description loads |
| A server with 60 tools, job needs 2 | load by exact name (`select:` form), not by broad keyword |
| Subagent would re-read everything you already read | do it inline |

---

## 4. Record

Generate the skeleton with [inventory.py](../scripts/inventory.py) rather than typing it; it fills the servers and skills from configuration, reports each project server's approval state, flags literal secrets in the committed `.mcp.json`, and marks everything else unverified. Its tests: `python -m unittest master-agent/scripts/test_inventory.py`. A filled-in example: [example-capability-record](../assets/example-capability-record.md).

Write this when setup took more than one attempt, or before handing the session to someone else. Keep it next to the project's other notes, not in the transcript.

```markdown
# Capability record — <project>

Date:       <YYYY-MM-DD>
Model:      <model id> @ effort <level>
Skills used:<names>
MCP servers:
  | server | scope | transport | state | tools actually used | proven by |
  | notion | project | http | connected | search, append-block | append visible 2026-09-28 |
  | figma  | user    | http | needs auth | — | — |
Subagents:  <type · why · model>
Known issues: <server X fails on cold start; retry after 15 min>
Never:      <tools or actions this project must not use>
```

"Proven by" names an observed result. A server with no proof row is configured, not working.
