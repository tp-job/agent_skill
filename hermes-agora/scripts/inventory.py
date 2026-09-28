#!/usr/bin/env python3
"""Print a capability-record skeleton for the current project.

Reads MCP server configuration from the three Claude Code scopes and the
skills installed for this project and user, then prints a markdown record.
Proving a server works is a separate step — this script only reports what is
*configured*, and whether a project server is approved to connect at all.

    python inventory.py [project_dir] > capability-record.md

Sources read (all optional; a missing or malformed file is skipped):
  project   <project>/.mcp.json                          -> mcpServers
  local     ~/.claude.json  projects[<project>]          -> mcpServers
  user      ~/.claude.json                               -> mcpServers
  approval  <project>/.claude/settings(.local).json and
            ~/.claude.json projects[<project>]           -> enabledMcpjsonServers,
                                                            disabledMcpjsonServers,
                                                            enableAllProjectMcpServers
  trust     ~/.claude.json projects[<project>]           -> hasTrustDialogAccepted
  skills    <project>/.claude/skills/*/SKILL.md, ~/.claude/skills/*/SKILL.md

Project (.mcp.json) servers start as "pending approval" and do not connect
until approved — interactively in `claude`, or through the keys above.
Observed on Claude Code 2.1.278: in a folder whose trust dialog has not been
accepted, the settings-file keys did not approve a server.

Secrets: env values, header values, URL query strings and secret-looking args
are never printed. A literal (non-${VAR}) env or header value in the project's
.mcp.json — a file meant to be committed — is flagged by name. Written for
Python 3.8+, standard library only.
"""
import datetime
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit

ENV_REF = re.compile(r"^\$\{[A-Za-z_][A-Za-z0-9_]*(:-[^}]*)?\}$")
SECRETISH = ("token", "key", "secret", "password", "passwd", "auth", "://")


def load_json(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def as_dict(value):
    return value if isinstance(value, dict) else {}


def as_list(value):
    return value if isinstance(value, list) else []


def transport(cfg):
    kind = cfg.get("type") or cfg.get("transport")
    if kind:
        return str(kind)
    if "command" in cfg:
        return "stdio"
    if "url" in cfg:
        return "http"
    return "?"


def redact_arg(arg):
    # An arg like --api-key=abc, a connection string, or a long opaque blob may be a secret.
    low = arg.lower()
    if "=" in arg or any(s in low for s in SECRETISH) or len(arg) > 40:
        return "<redacted>"
    return arg


def target(cfg):
    if "url" in cfg:
        u = urlsplit(str(cfg["url"]))
        return "%s://%s%s" % (u.scheme, u.hostname or "", u.path)  # query and userinfo dropped
    cmd = [str(cfg.get("command", ""))] + [redact_arg(str(a)) for a in as_list(cfg.get("args"))[:3]]
    return " ".join(c for c in cmd if c)


def secret_names(cfg):
    names = ["env:" + k for k in sorted(as_dict(cfg.get("env")))]
    names += ["header:" + k for k in sorted(as_dict(cfg.get("headers")))]
    return ", ".join(names) or "-"


def literal_secrets(cfg):
    """Names of env/header entries whose value is a literal rather than a ${VAR} reference."""
    found = []
    for kind in ("env", "headers"):
        for k, v in sorted(as_dict(cfg.get(kind)).items()):
            text = str(v)
            if kind == "headers":
                text = text.split(" ", 1)[-1]  # "Bearer ${TOKEN}" -> "${TOKEN}"
            if text and not ENV_REF.match(text):
                found.append("%s:%s" % ("env" if kind == "env" else "header", k))
    if "url" in cfg:
        parts = urlsplit(str(cfg["url"]))
        if any(v and not ENV_REF.match(v) for _, v in parse_qsl(parts.query, keep_blank_values=True)):
            found.append("url:query")
        if parts.password and not ENV_REF.match(parts.password):
            found.append("url:password")
    return found


def skills_in(root):
    if not root.is_dir():
        return []
    return sorted(p.parent.name for p in root.glob("*/SKILL.md"))


def norm_path(p):
    s = str(p).replace("\\", "/").rstrip("/")
    return s.lower() if os.name == "nt" else s  # Windows paths are case-insensitive; POSIX are not


def find_project_entry(projects, project):
    want = norm_path(project)
    for key, value in as_dict(projects).items():
        if norm_path(key) == want:
            return as_dict(value)
    return {}


def approval(project, entry):
    enabled, disabled, enable_all = set(), set(), False
    sources = [load_json(project / ".claude" / f) for f in ("settings.json", "settings.local.json")] + [entry]
    for s in sources:
        enabled |= {str(n) for n in as_list(s.get("enabledMcpjsonServers"))}
        disabled |= {str(n) for n in as_list(s.get("disabledMcpjsonServers"))}
        enable_all = enable_all or s.get("enableAllProjectMcpServers") is True
    return enabled, disabled, enable_all


def project_state(name, enabled, disabled, enable_all, trusted):
    if name in disabled:
        return "disabled"
    if not trusted:
        return "pending approval (folder not trusted)"
    if name in enabled or enable_all:
        return "approved, unverified"
    return "pending approval"


def build(project, home):
    user_cfg = load_json(home / ".claude.json")
    entry = find_project_entry(user_cfg.get("projects"), project)
    enabled, disabled, enable_all = approval(project, entry)
    trusted = entry.get("hasTrustDialogAccepted") is True

    rows, warnings = [], []
    scopes = (
        ("project", as_dict(load_json(project / ".mcp.json").get("mcpServers"))),
        ("local", as_dict(entry.get("mcpServers"))),
        ("user", as_dict(user_cfg.get("mcpServers"))),
    )
    for scope, servers in scopes:
        for name, cfg in sorted(servers.items()):
            cfg = as_dict(cfg)
            if scope == "project":
                state = project_state(name, enabled, disabled, enable_all, trusted)
                leaks = literal_secrets(cfg)
                if leaks:
                    warnings.append("`%s` in .mcp.json holds a literal value for %s — this file is committed; "
                                    "use a ${VAR} reference instead" % (name, ", ".join(leaks)))
            else:
                state = "unverified"
            rows.append((name, scope, transport(cfg), target(cfg), secret_names(cfg), state))

    if any(r[1] == "project" for r in rows) and not trusted:
        warnings.append("this folder's trust dialog has not been accepted — project servers stay pending "
                        "until you open `claude` here and approve them")

    out = []
    out.append("# Capability record — %s" % project.name)
    out.append("")
    out.append("Date:        %s" % datetime.date.today().isoformat())
    out.append("Model:       <model id> @ effort <level>")
    out.append("Generated:   hermes-agora/scripts/inventory.py — configured state only; nothing below is verified")
    out.append("")
    out.append("## MCP servers")
    out.append("")
    if rows:
        out.append("| server | scope | transport | target | secrets (names only) | state | tools used | proven by |")
        out.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
        for name, scope, kind, where, secrets, state in rows:
            out.append("| %s | %s | %s | `%s` | %s | %s | - | - |" % (name, scope, kind, where, secrets, state))
    else:
        out.append("No MCP servers configured in any scope. Connectors added through the claude.ai")
        out.append("app or a plugin are not in these files — check the session's server-status notices.")
    if warnings:
        out.append("")
        out.append("**Warnings**")
        out.append("")
        out.extend("- " + w for w in warnings)
    out.append("")
    out.append("## Skills")
    out.append("")
    project_skills = skills_in(project / ".claude" / "skills")
    user_skills = skills_in(home / ".claude" / "skills")
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
    return "\n".join(out)


def main(argv):
    project = Path(argv[1] if len(argv) > 1 else ".").resolve()
    print(build(project, Path.home()))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
