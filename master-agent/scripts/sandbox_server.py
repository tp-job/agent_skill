"""Sandbox MCP server: a note store with read, write and destructive tools.

Built by following ../references/building-mcp-servers.md literally, so the reference's
example and tool-surface rules can be checked against the real `mcp` SDK. State is a JSON
file (path in SANDBOX_NOTES, default: the system temp dir) so a write is observable from
outside the server. Needs `pip install mcp` (checked on 1.26.0). Run it through
verify_sandbox.py; it touches no account or service.
"""
import json
import os
import tempfile
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

STORE = Path(os.environ.get("SANDBOX_NOTES") or Path(tempfile.gettempdir()) / "mcp-sandbox-notes.json")
mcp = FastMCP("sandbox-notes")


def _load() -> dict:
    return json.loads(STORE.read_text(encoding="utf-8")) if STORE.exists() else {}


def _save(data: dict) -> None:
    STORE.write_text(json.dumps(data, indent=2), encoding="utf-8")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))
def find_notes(prefix: str = "", limit: int = 20) -> dict:
    """Find notes whose id starts with prefix. Use before update_note or delete_note."""
    items = sorted(k for k in _load() if k.startswith(prefix))
    limit = max(1, min(limit, 100))
    return {"count": len(items), "ids": items[:limit], "truncated": len(items) > limit}


@mcp.tool()
def create_note(note_id: str, text: str) -> dict:
    """Create a new note. Fails if note_id already exists — call find_notes first."""
    data = _load()
    if note_id in data:
        raise ValueError(f"note '{note_id}' already exists — pick another id, or delete_note it first (needs the user's approval)")
    data[note_id] = text
    _save(data)
    return {"created": note_id}


@mcp.tool(annotations=ToolAnnotations(destructiveHint=True))
def delete_note(note_id: str, confirm: bool = False) -> dict:
    """Delete a note permanently. Requires confirm=true, which must come from the user."""
    if not confirm:
        raise ValueError("refused: delete_note needs confirm=true, and the user must have approved this delete")
    data = _load()
    if note_id not in data:
        raise ValueError(f"note '{note_id}' not found — call find_notes first")
    del data[note_id]
    _save(data)
    return {"deleted": note_id}


if __name__ == "__main__":
    mcp.run()  # stdio by default
