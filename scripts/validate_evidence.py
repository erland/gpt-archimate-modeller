#!/usr/bin/env python3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from assemble_project import assemble

def collect_assertions(logical):
    for obj in list(logical["model"]["elements"]) + list(logical["model"]["relationships"]):
        evidence = obj.get("evidence")
        if not evidence:
            yield obj, None
            continue
        for assertion in evidence.get("assertions", []):
            yield obj, assertion

def main():
    if len(sys.argv) != 2:
        print("Usage: validate_evidence.py <project-dir>")
        return 2

    logical, errors = assemble(Path(sys.argv[1]))
    if errors:
        print("FAILED")
        for e in errors:
            print("-", e)
        return 1

    evidence_errors = []
    seen_ev = set()
    sources = {s["id"] for s in logical.get("sources", [])}
    references = {r["id"] for r in logical.get("references", [])}

    for obj in list(logical["model"]["elements"]) + list(logical["model"]["relationships"]):
        ev = obj.get("evidence")
        if not ev:
            continue

        assertions = ev.get("assertions", [])
        kinds = {a.get("kind") for a in assertions}

        if ev.get("status") == "inferred" and not ({"inferred", "derived"} & kinds):
            evidence_errors.append(f"{obj['id']}: status inferred without inferred/derived assertion.")

        if ev.get("status") == "document_confirmed" and "explicit" not in kinds:
            evidence_errors.append(f"{obj['id']}: document_confirmed without explicit assertion.")

        if ev.get("status") == "user_confirmed" and "user_statement" not in kinds:
            evidence_errors.append(f"{obj['id']}: user_confirmed without user_statement assertion.")

        for a in assertions:
            aid = a.get("id")
            if aid in seen_ev:
                evidence_errors.append(f"Duplicate evidence assertion id: {aid}")
            seen_ev.add(aid)

            if not a.get("supports"):
                evidence_errors.append(f"{aid}: supports must not be empty.")

            if a.get("kind") in ("inferred", "derived") and not a.get("reason"):
                evidence_errors.append(f"{aid}: inferred/derived assertion requires reason.")

            for ref in a.get("source_refs", []):
                if ref not in sources:
                    evidence_errors.append(f"{aid}: source not found: {ref}")
            for ref in a.get("reference_refs", []):
                if ref not in references:
                    evidence_errors.append(f"{aid}: reference not found: {ref}")

    if evidence_errors:
        print("FAILED")
        for e in evidence_errors:
            print("-", e)
        return 1

    print("OK")
    print(f"Evidence assertions: {len(seen_ev)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
