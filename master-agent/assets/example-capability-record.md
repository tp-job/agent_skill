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

---

## Second server — a local sandbox, for the checks bioRxiv could not cover

Write and refusal cannot be proven on a read-only server, and proving them on a real account needs the user's yes. So a throwaway note-store server ([sandbox_server.py](../scripts/sandbox_server.py), rerun with [verify_sandbox.py](../scripts/verify_sandbox.py)) was written by following [building-mcp-servers](../references/building-mcp-servers.md) literally (FastMCP, `mcp` SDK 1.26.0, state in a local JSON file), then driven over real stdio by an SDK client.

| Check | Observed | Result |
| --- | --- | --- |
| Tools listed; annotations reach the client | 3 tools; `destructiveHint=True` on delete, `readOnlyHint=True` on find | ✅ |
| Read succeeds | `{"count": 0, "ids": [], "truncated": false}` | ✅ |
| Write succeeds **and is visible outside the server** | `create_note` → the JSON file on disk holds the note | ✅ |
| Duplicate write refused with a teaching error | `isError: true`, names the next step | ✅ |
| Destructive call refused without confirmation | `delete_note` without `confirm` → `isError: true`, note still on disk | ✅ |
| Wrong-typed argument rejected before the tool runs | `limit="many"` → validation error | ✅ |
| Confirmed delete succeeds; not-found names a real tool | note gone; `"call find_notes first"` | ✅ |

**10 / 10 passed.** The run also caught a defect *in the sandbox itself*: its duplicate-write error told the model to "use update_note", a tool that did not exist. Fixed, and added to the build checklist as "every tool name mentioned in an error exists on this server".

**Registered through the real CLI** (`claude mcp add --scope project`), the same server showed two behaviours now written into [mcp-lifecycle](../references/mcp-lifecycle.md): it sat at `⏸ Pending approval` — approval keys in the project's settings files were not honoured because the folder's trust dialog had never been accepted — and `-e TOKEN=value` wrote the value in plain text into the committed `.mcp.json`.

**Still not proven:** write and refusal against a real, remote, OAuth-protected service. That needs the user's yes for one real write.
