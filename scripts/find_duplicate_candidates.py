#!/usr/bin/env python3
from pathlib import Path
import sys
import yaml
sys.path.insert(0, str(Path(__file__).resolve().parent))
from assemble_project import assemble
from identity import normalize_name

def main():
    if len(sys.argv) != 2:
        print("Usage: find_duplicate_candidates.py <project-dir>")
        return 2

    logical, errors = assemble(Path(sys.argv[1]))
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1

    elements = logical["model"]["elements"]
    by_norm = {}
    alias_map = {}

    for e in elements:
        n = normalize_name(e.get("name"))
        if n:
            by_norm.setdefault((e.get("type"), n), []).append(e["id"])
        for a in e.get("aliases", []):
            an = normalize_name(a)
            if an:
                alias_map.setdefault(an, []).append(e["id"])

    candidates = []
    for (typ, n), ids in by_norm.items():
        if len(ids) > 1:
            candidates.append(("same_normalized_name", typ, n, ids))
    for n, ids in alias_map.items():
        uniq = sorted(set(ids))
        if len(uniq) > 1:
            candidates.append(("shared_alias", None, n, uniq))

    if not candidates:
        print("OK: no strong duplicate candidates")
        return 0

    print("DUPLICATE CANDIDATES")
    for kind, typ, value, ids in candidates:
        print(f"- {kind}: type={typ} value={value!r} ids={','.join(ids)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
