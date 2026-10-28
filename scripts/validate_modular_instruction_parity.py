#!/usr/bin/env python3
"""Validate byte-preserving transfer of original canonical instruction sections.

The source sections are compared verbatim, irrespective of which Skill owns them.
This validates section coverage, NOT runtime behavior, resource isolation or build.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

FILES = [
    "canonical/core.md",
    "canonical/skills/project-workflow/behavior.md",
    "canonical/skills/archimate-modeling/behavior.md",
    "canonical/skills/architecture-analysis/behavior.md",
    "canonical/skills/interoperability/behavior.md",
]

def sections(text):
    return {
        m.group(1): text[m.end():n.start() if n else len(text)].strip()
        for m, n in (
            (matches[i], matches[i + 1] if i + 1 < len(matches) else None)
            for matches in [list(re.finditer(r"^## (.+)$", text, re.M))]
            for i in range(len(matches))
        )
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    args = p.parse_args()
    root = Path(args.root)
    original = sections((root / "gpt/SYSTEM_INSTRUCTION.md").read_text(encoding="utf-8"))
    found = {}
    collisions = []
    for relative in FILES:
        data = sections((root / relative).read_text(encoding="utf-8"))
        for heading, body in data.items():
            if heading in found:
                collisions.append(heading)
            found[heading] = (relative, body)
    missing = sorted(set(original) - set(found))
    extras = sorted(set(found) - set(original))
    changed = sorted(h for h in original.keys() & found.keys() if original[h] != found[h][1])
    result = {
        "status": "pass" if not (missing or extras or changed or collisions) else "fail",
        "original_sections": len(original),
        "mapped_sections": len(found),
        "missing": missing,
        "extra": extras,
        "changed": changed,
        "duplicate_headings": sorted(set(collisions)),
        "scope": "original Markdown heading sections verbatim only",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "pass" else 1

if __name__ == "__main__":
    raise SystemExit(main())
