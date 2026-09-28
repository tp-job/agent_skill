#!/usr/bin/env python3
"""Tests for inventory.py. Standard library only:

    python -m unittest hermes-agora/scripts/test_inventory.py -v
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import inventory  # noqa: E402

SECRETS = ("SECRETPW", "SECRETKEY", "SECRETTOKEN", "SECRETARG", "SECRETENV")


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data if isinstance(data, str) else json.dumps(data), encoding="utf-8")


class InventoryTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        self.home, self.proj = root / "home", root / "proj"
        self.home.mkdir()
        self.proj.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def run_inv(self):
        return inventory.build(self.proj.resolve(), self.home)

    def row(self, out, name):
        rows = [l for l in out.splitlines() if l.startswith("| %s |" % name)]
        self.assertEqual(len(rows), 1, out)
        return [c.strip() for c in rows[0].strip("|").split("|")]

    def user_cfg(self, project_entry=None, **top):
        cfg = dict(top)
        if project_entry is not None:
            cfg["projects"] = {str(self.proj.resolve()): project_entry}
        write(self.home / ".claude.json", cfg)

    # --- empty and malformed input -------------------------------------------------

    def test_nothing_configured(self):
        self.assertIn("No MCP servers configured", self.run_inv())

    def test_malformed_files_are_skipped(self):
        write(self.proj / ".mcp.json", "{ not json")
        write(self.home / ".claude.json", "[1, 2, 3]")
        write(self.proj / ".claude" / "settings.json", '"a string"')
        self.assertIn("No MCP servers configured", self.run_inv())

    def test_malformed_server_entries_do_not_crash(self):
        write(self.proj / ".mcp.json", {"mcpServers": {"a": "oops", "b": {"command": "x", "args": "notalist", "env": []}}})
        out = self.run_inv()
        self.assertEqual(self.row(out, "b")[2], "stdio")

    # --- scopes ----------------------------------------------------------------------

    def test_three_scopes(self):
        write(self.proj / ".mcp.json", {"mcpServers": {"p": {"command": "npx", "args": ["p-mcp"]}}})
        self.user_cfg({"mcpServers": {"l": {"type": "http", "url": "https://l.example/mcp"}}},
                      mcpServers={"u": {"command": "uvx", "args": ["u-mcp"]}})
        out = self.run_inv()
        self.assertEqual(self.row(out, "p")[1], "project")
        self.assertEqual(self.row(out, "l")[1], "local")
        self.assertEqual(self.row(out, "u")[1], "user")
        self.assertEqual(self.row(out, "l")[2], "http")

    # --- approval of project servers -------------------------------------------------

    def test_project_server_pending_by_default(self):
        write(self.proj / ".mcp.json", {"mcpServers": {"s": {"command": "x"}}})
        out = self.run_inv()
        self.assertEqual(self.row(out, "s")[5], "pending approval (folder not trusted)")
        self.assertIn("trust dialog has not been accepted", out)

    def test_trusted_but_unapproved_is_pending(self):
        write(self.proj / ".mcp.json", {"mcpServers": {"s": {"command": "x"}}})
        self.user_cfg({"hasTrustDialogAccepted": True})
        out = self.run_inv()
        self.assertEqual(self.row(out, "s")[5], "pending approval")
        self.assertNotIn("trust dialog", out)

    def test_approval_from_user_config_project_entry(self):
        write(self.proj / ".mcp.json", {"mcpServers": {"s": {"command": "x"}}})
        self.user_cfg({"enabledMcpjsonServers": ["s"], "hasTrustDialogAccepted": True})
        out = self.run_inv()
        self.assertEqual(self.row(out, "s")[5], "approved, unverified")
        self.assertNotIn("trust dialog", out)

    def test_approval_from_settings_and_enable_all(self):
        write(self.proj / ".mcp.json", {"mcpServers": {"a": {"command": "x"}, "b": {"command": "y"}}})
        write(self.proj / ".claude" / "settings.json", {"enableAllProjectMcpServers": True})
        write(self.proj / ".claude" / "settings.local.json", {"disabledMcpjsonServers": ["b"]})
        self.user_cfg({"hasTrustDialogAccepted": True})
        out = self.run_inv()
        self.assertEqual(self.row(out, "a")[5], "approved, unverified")
        self.assertEqual(self.row(out, "b")[5], "disabled")  # an explicit disable beats enable-all

    def test_untrusted_folder_keeps_servers_pending_despite_settings(self):
        # Observed on Claude Code 2.1.278: settings-file approval is not honoured before the trust dialog.
        write(self.proj / ".mcp.json", {"mcpServers": {"s": {"command": "x"}}})
        write(self.proj / ".claude" / "settings.json", {"enableAllProjectMcpServers": True})
        out = self.run_inv()
        self.assertEqual(self.row(out, "s")[5], "pending approval (folder not trusted)")
        self.assertIn("trust dialog has not been accepted", out)

    def test_disabled_list_does_not_touch_other_scopes(self):
        self.user_cfg({"disabledMcpjsonServers": ["u"]}, mcpServers={"u": {"command": "x"}})
        self.assertEqual(self.row(self.run_inv(), "u")[5], "unverified")

    # --- secrets ---------------------------------------------------------------------

    def test_no_secret_value_is_ever_printed(self):
        write(self.proj / ".mcp.json", {"mcpServers": {
            "db": {"command": "npx", "args": ["-y", "db-mcp", "--token=SECRETARG"], "env": {"DB_URL": "SECRETENV"}},
            "pg": {"command": "uvx", "args": ["pg", "postgres://u:SECRETPW@h/db"]},
            "api": {"type": "http", "url": "https://u:SECRETPW@api.example/mcp?key=SECRETKEY",
                    "headers": {"Authorization": "Bearer SECRETTOKEN"}},
        }})
        out = self.run_inv()
        for s in SECRETS:
            self.assertNotIn(s, out)
        self.assertEqual(self.row(out, "api")[3], "`https://api.example/mcp`")

    def test_literal_secret_in_committed_file_is_flagged(self):
        write(self.proj / ".mcp.json", {"mcpServers": {
            "bad": {"command": "x", "env": {"TOKEN": "SECRETENV"}, "headers": {"Authorization": "Bearer SECRETTOKEN"}},
            "good": {"command": "x", "env": {"TOKEN": "${TOKEN}", "MODE": "${MODE:-dev}"},
                     "headers": {"Authorization": "Bearer ${API_TOKEN}"}},
            "q": {"type": "http", "url": "https://x.example/mcp?key=SECRETKEY"},
            "qok": {"type": "http", "url": "https://x.example/mcp?key=${KEY}"},
        }})
        out = self.run_inv()
        self.assertIn("`bad` in .mcp.json holds a literal value for env:TOKEN, header:Authorization", out)
        self.assertIn("`q` in .mcp.json holds a literal value for url:query", out)
        self.assertNotIn("`good`", out)
        self.assertNotIn("`qok`", out)

    def test_literal_values_outside_project_scope_are_not_flagged(self):
        self.user_cfg(mcpServers={"u": {"command": "x", "env": {"TOKEN": "SECRETENV"}}})
        out = self.run_inv()
        self.assertNotIn("literal value", out)
        self.assertNotIn("SECRETENV", out)

    # --- skills ----------------------------------------------------------------------

    def test_skills_listed(self):
        write(self.proj / ".claude" / "skills" / "alpha" / "SKILL.md", "---\nname: alpha\n---\n")
        write(self.home / ".claude" / "skills" / "beta" / "SKILL.md", "---\nname: beta\n---\n")
        out = self.run_inv()
        self.assertIn("- project (1): alpha", out)
        self.assertIn("- user (1): beta", out)


if __name__ == "__main__":
    unittest.main()
