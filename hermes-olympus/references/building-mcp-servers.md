# Building an MCP server

When a capability is genuinely missing and will be reused, write it as a server. Against MCP specification revision **2025-11-25**; the Python snippets below were run against the `mcp` SDK **1.26.0**. Check the official SDK's current major version before starting (TypeScript `@modelcontextprotocol/sdk`, Python `mcp`).

---

## 1. Should this be a server at all?

| Need | Build |
| --- | --- |
| Instructions or a workflow, no new I/O | a skill, not a server |
| One project, one script | a script the agent runs |
| Reused across projects or teammates, touches an external system | **an MCP server** |
| Already exists in a registry | install it — search the registry first |

---

## 2. Design the tool surface

Tools are an API whose caller is a model. Design for that caller.

| Rule | BAD | BETTER |
| --- | --- | --- |
| Name by outcome | `api_call(endpoint, method, body)` | `create_invoice(customer_id, lines)` |
| Few, composable tools | 40 thin endpoint wrappers | 6 task-shaped tools + one bulk operation |
| Describe when to use it | "Gets data." | "Find invoices by customer or date range. Use before `update_invoice`." |
| Typed, constrained inputs | `filter: string` | `status: "draft" \| "sent" \| "paid"` |
| Errors that teach | `500` | `"customer_id not found — call search_customers first"` |
| Name only tools that exist | `"already exists — use edit_record"` when no such tool ships | point at a tool the server really exposes, or at none |
| Bounded outputs | full table dump | paginated, with a `next` cursor and a count |

Mark destructive tools as such in their annotations, and make read tools idempotent. Annotations are hints to the client, not enforcement — a destructive tool still has to refuse on its own:

```python
from mcp.types import ToolAnnotations

@mcp.tool(annotations=ToolAnnotations(destructiveHint=True))
def delete_invoice(invoice_id: str, confirm: bool = False) -> dict:
    """Delete an invoice permanently. Requires confirm=true, which must come from the user."""
    if not confirm:
        raise ValueError("refused: needs confirm=true, and the user must have approved this delete")
    ...
```

With FastMCP, an exception raised inside a tool reaches the client as a result with `isError: true` and the exception's message as its text, and an argument of the wrong type is rejected with a validation error before your function runs.

---

## 3. Minimal server (Python, `mcp` SDK)

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("invoices")

@mcp.tool()
def find_invoices(customer_id: str, status: str = "any", limit: int = 20) -> list[dict]:
    """Find invoices for one customer. Use before update_invoice."""
    return db.find(customer_id=customer_id, status=status, limit=min(limit, 100))  # db: your data layer

if __name__ == "__main__":
    mcp.run()  # stdio by default
```

Credentials come from the environment, never from tool arguments.

---

## 4. Verify before shipping

- [ ] Every tool called once through a real client with valid input — result observed
- [ ] Every tool called once with invalid input — the error tells the model what to do next
- [ ] Every tool name mentioned in an error message or description exists on this server
- [ ] Destructive tools refuse without the required argument or confirmation
- [ ] Output of the largest realistic query fits the page limit
- [ ] No secret appears in any tool description, log line or error
- [ ] A capability record row written with "proven by" filled in — see [capability-inventory](capability-inventory.md) §Record

**When not to polish:** an internal, single-user prototype. Get one tool working end to end first; the surface rules pay off once a second caller exists.
