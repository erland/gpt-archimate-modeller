#!/usr/bin/env python3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from assemble_project import assemble

def main():
    if len(sys.argv) != 2:
        print("Usage: validate_sources.py <project-dir>")
        return 2

    logical, errors = assemble(Path(sys.argv[1]))
    if errors:
        print("FAILED")
        for e in errors:
            print("-", e)
        return 1

    srcs = logical.get("sources", [])
    refs = logical.get("references", [])
    issues = []

    src_ids = {s["id"] for s in srcs}
    seen_locators = set()

    for s in srcs:
        origin = s.get("origin") or {}
        kind = origin.get("kind")
        if kind == "file" and not origin.get("path"):
            issues.append(f"{s['id']}: file origin requires path.")
        if kind == "url" and not origin.get("uri"):
            issues.append(f"{s['id']}: url origin requires uri.")
        if kind == "conversation" and not origin.get("conversation_ref"):
            issues.append(f"{s['id']}: conversation origin requires conversation_ref.")
        if kind == "external_system" and not origin.get("system"):
            issues.append(f"{s['id']}: external_system origin requires system.")

    for r in refs:
        if r["source_ref"] not in src_ids:
            issues.append(f"{r['id']}: source_ref not found.")
        loc = r.get("locator") or {}
        key = (r.get("source_ref"), loc.get("kind"), loc.get("value"), loc.get("start"), loc.get("end"))
        if key in seen_locators:
            issues.append(f"{r['id']}: duplicate source+locator reference.")
        seen_locators.add(key)

        if loc.get("kind") == "line_range":
            if "start" not in loc or "end" not in loc:
                issues.append(f"{r['id']}: line_range requires start and end.")

    if issues:
        print("FAILED")
        for i in issues:
            print("-", i)
        return 1

    print("OK")
    print(f"Sources: {len(srcs)}")
    print(f"References: {len(refs)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
