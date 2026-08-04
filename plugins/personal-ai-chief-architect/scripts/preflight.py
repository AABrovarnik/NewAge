#!/usr/bin/env python3
"""Offline configuration check; never contacts external services."""
import json, os, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
required = [ROOT / ".codex-plugin/plugin.json", ROOT / ".mcp.json", ROOT / "hooks/hooks.json", ROOT / "policies/permissions.yaml"]
missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
bad = [k for k in ("name", "version", "description", "skills") if not manifest.get(k)]
if missing or bad:
    print("preflight: FAIL")
    if missing: print("missing:", ", ".join(missing))
    if bad: print("manifest fields:", ", ".join(bad))
    sys.exit(1)
print("preflight: OK")
print("plugin:", manifest["name"], manifest["version"])
print("secrets loaded:", sum(bool(os.getenv(k)) for k in ("TELEGRAM_BOT_TOKEN", "GOOGLE_REFRESH_TOKEN", "GITHUB_TOKEN")))
print("external calls: none")
