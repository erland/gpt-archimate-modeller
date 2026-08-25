#!/usr/bin/env python3
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
K=ROOT/"knowledge"

def main():
    errors=[]
    idx=yaml.safe_load((K/"knowledge-index.yaml").read_text(encoding="utf-8"))
    route=yaml.safe_load((K/"routing.yaml").read_text(encoding="utf-8"))

    required=["00-overview.md","01-runtime-contract.md","02-archimate-core.md","03-project-format.md",
              "04-identity-evidence.md","05-change-versioning.md","06-query-report-view.md",
              "07-validation-quality.md","08-interoperability.md","09-project-package-migration.md"]

    for f in required:
        if not (K/f).exists():
            errors.append(f"Missing knowledge file: {f}")

    for entry in idx.get("core",[]):
        if not (ROOT/entry["file"]).exists():
            errors.append(f"Knowledge index points to missing file: {entry['file']}")

    for f in idx.get("authoritative_machine_readable",[]):
        if not (ROOT/f).exists():
            errors.append(f"Authoritative file missing: {f}")

    for f in idx.get("reference_docs",[]):
        if not (ROOT/f).exists():
            errors.append(f"Reference doc missing: {f}")

    known={p.name for p in K.glob("*.md")}
    for r in route.get("routes",[]):
        for f in r.get("knowledge",[]):
            if f not in known:
                errors.append(f"Routing points to unknown knowledge file: {f}")

    if errors:
        print("FAILED")
        for e in errors:
            print("-",e)
        return 1

    print("OK")
    print(f"Core knowledge files: {len(idx['core'])}")
    print(f"Machine-readable authoritative refs: {len(idx['authoritative_machine_readable'])}")
    print(f"Reference docs: {len(idx['reference_docs'])}")
    print(f"Intent routes: {len(route['routes'])}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
