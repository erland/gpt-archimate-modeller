#!/usr/bin/env python3
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from assemble_project import assemble

def validate_specializations(logical):
    specs = logical.get("specializations", {})
    issues, warnings = [], []

    for name, spec in specs.items():
        parent = spec.get("parent_specialization")
        if parent:
            if parent not in specs:
                issues.append(f"{name}: parent specialization not found: {parent}")
            elif specs[parent].get("base_type") != spec.get("base_type"):
                issues.append(f"{name}: base_type differs from parent {parent}")

    visiting, visited = set(), set()
    def visit(name, stack):
        if name in visited:
            return
        if name in visiting:
            issues.append("Specialization inheritance cycle: " + " -> ".join(stack + [name]))
            return
        visiting.add(name)
        parent = specs.get(name, {}).get("parent_specialization")
        if parent in specs:
            visit(parent, stack + [name])
        visiting.remove(name)
        visited.add(name)

    for name in specs:
        visit(name, [])

    for e in logical["model"]["elements"]:
        sname = e.get("specialization")
        if not sname:
            continue
        if sname not in specs:
            issues.append(f"{e['id']}: unknown specialization {sname}")
            continue
        spec = specs[sname]
        if e.get("type") != spec.get("base_type"):
            issues.append(f"{e['id']}: type {e.get('type')} incompatible with specialization {sname} base_type {spec.get('base_type')}")
        if (spec.get("governance") or {}).get("status") == "deprecated":
            warnings.append(f"{e['id']}: specialization {sname} is deprecated.")

    return issues, warnings

def main():
    if len(sys.argv) != 2:
        print("Usage: validate_specializations.py <project-dir>")
        return 2
    logical, errors = assemble(Path(sys.argv[1]))
    if errors:
        print("FAILED")
        for e in errors:
            print("-", e)
        return 1
    issues, warnings = validate_specializations(logical)
    if warnings:
        print("WARNINGS")
        for w in warnings:
            print("-", w)
    if issues:
        print("FAILED")
        for i in issues:
            print("-", i)
        return 1
    print("OK")
    print(f"Specializations: {len(logical.get('specializations', {}))}")
    print(f"Specialized elements: {sum(1 for e in logical['model']['elements'] if e.get('specialization'))}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
