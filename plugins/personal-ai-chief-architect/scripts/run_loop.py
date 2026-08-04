#!/usr/bin/env python3
"""Print a loop plan. Real execution belongs to a configured MCP adapter."""
import argparse, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("loop", choices=[p.stem for p in (ROOT / "loops").glob("*.yaml")])
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()
path = ROOT / "loops" / f"{args.loop}.yaml"
print(path.read_text())
print("mode:", "dry-run" if args.dry_run else "plan-only")
print("external writes: blocked until explicit confirmation")
