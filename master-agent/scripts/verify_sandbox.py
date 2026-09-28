#!/usr/bin/env python3
"""Run the §Verify checklist of ../references/mcp-lifecycle.md against sandbox_server.py
over real stdio, using the official `mcp` SDK client. Exits non-zero on any failed check.

    pip install mcp            # checked on 1.26.0
    python verify_sandbox.py
"""
import asyncio
import json
import os
import sys
import tempfile
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

HERE = Path(__file__).parent
STORE = Path(tempfile.gettempdir()) / "mcp-sandbox-verify-notes.json"
results = []


def check(name, ok, detail):
    results.append((name, ok))
    print(("PASS" if ok else "FAIL"), "-", name, "::", detail)


def text(res):
    return " ".join(getattr(c, "text", "") for c in res.content)


async def main():
    if STORE.exists():
        STORE.unlink()
    params = StdioServerParameters(command=sys.executable, args=[str(HERE / "sandbox_server.py")],
                                   env={**os.environ, "SANDBOX_NOTES": str(STORE)})
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            tools = {t.name: t for t in (await s.list_tools()).tools}
            check("tools listed", set(tools) == {"find_notes", "create_note", "delete_note"}, sorted(tools))
            ann = tools["delete_note"].annotations
            check("destructive annotated", bool(ann and ann.destructiveHint), ann)
            ro = tools["find_notes"].annotations
            check("read tool annotated read-only", bool(ro and ro.readOnlyHint), ro)

            res = await s.call_tool("find_notes", {})
            check("read succeeds", not res.isError and '"count": 0' in text(res).replace(":0", ": 0"), text(res))

            res = await s.call_tool("create_note", {"note_id": "n1", "text": "hello"})
            on_disk = json.loads(STORE.read_text(encoding="utf-8")) if STORE.exists() else {}
            check("write succeeds and is visible outside the server", not res.isError and on_disk.get("n1") == "hello", on_disk)

            res = await s.call_tool("create_note", {"note_id": "n1", "text": "again"})
            check("duplicate write refused with teaching error", res.isError and "pick another id" in text(res), text(res))

            res = await s.call_tool("delete_note", {"note_id": "n1"})
            still = json.loads(STORE.read_text(encoding="utf-8"))
            check("destructive call refused without confirm", res.isError and "n1" in still, text(res))

            res = await s.call_tool("find_notes", {"limit": "many"})
            check("invalid input rejected", res.isError, text(res)[:120])

            res = await s.call_tool("delete_note", {"note_id": "n1", "confirm": True})
            gone = json.loads(STORE.read_text(encoding="utf-8"))
            check("confirmed delete succeeds", not res.isError and "n1" not in gone, gone)

            res = await s.call_tool("delete_note", {"note_id": "ghost", "confirm": True})
            check("not-found names the next step", res.isError and "find_notes" in text(res), text(res))
    failed = [n for n, ok in results if not ok]
    print("\n%d/%d passed" % (len(results) - len(failed), len(results)))
    return 1 if failed else 0


sys.exit(asyncio.run(main()))
