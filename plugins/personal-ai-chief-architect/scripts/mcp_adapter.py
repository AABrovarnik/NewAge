#!/usr/bin/env python3
"""Transport placeholder for a real MCP bridge; intentionally refuses network calls."""
import json, sys
service = sys.argv[1] if len(sys.argv) > 1 else "unknown"
print(json.dumps({"service": service, "status": "not_configured", "message": "Configure a reviewed MCP server before enabling external calls."}))
sys.exit(2)
