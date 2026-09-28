# Capability record — worked example

One server taken through the master-agent loop — inventory, triage, route, verify, record — in a real session on 2026-09-28. The server was chosen because it is public and read-only, so verifying it touched no one's account or data.

---

## Inventory and triage

| Observed | Meaning |
| --- | --- |
| `scripts/inventory.py` on the project: "No MCP servers configured in any scope" | nothing in `.mcp.json` or `~/.claude.json` for this project — the session's servers come from plugins and app connectors instead |
| Session notice: bioRxiv server "still connecting", later listed as deferred tools | not failed — searched once, then loaded |
| Session notice: 26 plugin servers "require authentication" | configured, not authorised — reported to the user, no tokens requested |
| Session notice: one server "failed to connect" with a cached retry | reported as a connection failure, not as a missing capability |

## Route

Job: prove the verification checklist from [mcp-lifecycle](../references/mcp-lifecycle.md) §Verify on a real server.
Route: dedicated MCP tools, loaded by exact name in **one** batched schema load (`select:get_categories,get_preprint`), not by broad keyword.

## Verify

| Check | Call | Observed | Result |
| --- | --- | --- | --- |
| Read succeeds, returns expected data | `get_categories()` | `success: true`, 27 categories, matching the tool description's list | ✅ pass |
| Invalid input produces a teaching error | `get_preprint(doi="10.1101/0000.00.00.000000")` | `success: false`, `"No preprint found with DOI: …"` — structured, no crash, names the input | ✅ pass |
| Write succeeds and is visible | — | server exposes no write tools | n/a (read-only) |
| A call that should be refused is refused | — | no destructive or scoped tools to test against | n/a |

## Record

```markdown
| server  | scope  | transport | state     | tools actually used          | proven by                                   |
| biorxiv | plugin | (plugin)  | connected | get_categories, get_preprint | 27 categories + structured not-found error, 2026-09-28 |
```

**What this example does not prove:** write and refusal behaviour. Prove those on a server that has write tools, against a sandbox or with the user's yes for one real write.
