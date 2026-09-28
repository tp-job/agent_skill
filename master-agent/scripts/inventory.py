#!/usr/bin/env python3
"""Print a capability-record skeleton for the current project.

Reads MCP server configuration from the three Claude Code scopes and the
skills installed for this project and user, then prints a markdown record
with every server marked "unverified". Proving a server works is a separate
step — this script only reports what is *configured*.

    python inventory.py [project_dir] > capability-record.md

Sources read (all optional; a missing file is skipped):
  project  <project>/.mcp.json                       -> mcpServers
  local    ~/.claude.json  projects[<project>]       -> mcpServers
  user     ~/.claude.json                            -> mcpServers
  settings <project>/.claude/settings(.local).json   -> enabledMcpjsonServers,
                                                        disabledMcpjsonServers
  skills   <project>/.claude/skills/*/SKILL.md, ~/.claude/skills/*/SKILL.md

Secrets: env values, headers and URL query strings are never printed — only
the names of env variables and headers. Written for Python 3.8+, standard
library only.
"""
import datetime
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def transport(cfg):
    kind = cfg.get("type") or cfg.get("transport")
    if kind:
        return kind
    if "command" in cfg:
        return "stdio"
    if "url" in cfg:
        return "http"
    return "?"


def target(cfg):
    if "url" in cfg:
        u = urlsplit(cfg["url"])
        return "%s://%s%s" % (u.scheme, u.netloc, u.path)  # query dropped: may carry a key
    cmd = [cfg.get("command", "")] + [redact_arg(str(a)) for a in cfg.get("args", [])[:3]]
    return " ".join(c for c in cmd if c)


SECRETISH = ("token", "key", "secret", "password", "passwd", "auth", "://")


def redact_arg(arg):
    # An arg like --api-key=abc, a connection string, or a long opaque blob may be a secret.
    low = arg.lower()
    if "=" in arg or any(s in low for s in SECRETISH) or len(arg) > 40:
        return "<redacted>"
    return arg


def secret_names(cfg):
    names = ["env:" + k for k in sorted(cfg.get("env", {}))]
    names += ["header:" + k for k in sorted(cfg.get("headers", {}))]
    return ", ".join(names) or "-"


def skills_in(root):
    if not root.is_dir():
        return []
    return sorted(p.parent.name for p in root.glob("*/SKILL.md"))


def find_project_entry(projects, project):
    want = str(project).replace("\\", "/").rstrip("/").lower()
    for key, value in projects.items():
        if key.replace("\\", "/").rstrip("/").lower() == want:
            return value
    return {}


def main(argv):
    project = Path(argv[1] if len(argv) > 1 else ".").resolve()
    home = Path.home()
    user_cfg = load_json(home / ".claude.json")

    rows = []
    scopes = (
        ("project", load_json(project / ".mcp.json").get("mcpServers", {})),
        ("local", find_project_entry(user_cfg.get("projects", {}), project).get("mcpServers", {})),
        ("user", user_cfg.get("mcpServers", {})),
    )
    for scope, servers in scopes:
        for name, cfg in sorted(servers.items()):
            rows.append((name, scope, transport(cfg), target(cfg), secret_names(cfg)))

    enabled, disabled = set(), set()
    for f in ("settings.json", "settings.local.json"):
        s = load_json(project / ".claude" / f)
        enabled |= set(s.get("enabledMcpjsonServers", []))
        disabled |= set(s.get("disabledMcpjsonServers", []))

    project_skills = skills_in(project / ".claude" / "skills")
    user_skills = skills_in(home / ".claude" / "skills")

    out = []
    out.append("# Capability record — %s" % project.name)
    out.append("")
    out.append("Date:        %s" % datetime.date.today().isoformat())
    out.append("Model:       <model id> @ effort <level>")
    out.append("Generated:   master-agent/scripts/inventory.py — configured state only; nothing below is verified")
    out.append("")
    out.append("## MCP servers")
    out.append("")
    if rows:
        out.append("| server | scope | transport | target | secrets (names only) | state | tools used | proven by |")
        out.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
        for name, scope, kind, where, secrets in rows:
            state = "disabled" if name in disabled else "unverified"
            if scope == "project" and name in enabled:
                state = "unverified (approved)"
            out.append("| %s | %s | %s | `%s` | %s | %s | - | - |" % (name, scope, kind, where, secrets, state))
    else:
        out.append("No MCP servers configured in any scope. Connectors added through the claude.ai")
        out.append("app or a plugin are not in these files — check the session's server-status notices.")
    out.append("")
    out.append("## Skills")
    out.append("")
    out.append("- project (%d): %s" % (len(project_skills), ", ".join(project_skills) or "-"))
    out.append("- user (%d): %s" % (len(user_skills), ", ".join(user_skills) or "-"))
    out.append("- plugin skills: not listed here — read them from the session's skill listing")
    out.append("")
    out.append("## Subagents")
    out.append("")
    out.append("- <type · why · model>")
    out.append("")
    out.append("## Known issues")
    out.append("")
    out.append("- <server X fails on cold start; retry after 15 min>")
    out.append("")
    out.append("## Never")
    out.append("")
    out.append("- <tools or actions this project must not use>")
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
