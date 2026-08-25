#!/usr/bin/env python3
from pathlib import Path
import datetime as dt
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from assemble_project import assemble

def kind_ok(value, value_type):
    if value_type == "string":
        return isinstance(value, str)
    if value_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if value_type == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if value_type == "boolean":
        return isinstance(value, bool)
    if value_type == "date":
        if not isinstance(value, str):
            return False
        try:
            dt.date.fromisoformat(value)
            return True
        except ValueError:
            return False
    if value_type == "enum":
        return True
    if value_type == "list":
        return isinstance(value, list)
    if value_type == "reference":
        return isinstance(value, str)
    return False

def evidence_supports(obj, prop):
    target = f"property:{prop}"
    ev = obj.get("evidence") or {}
    return any(target in a.get("supports", []) for a in ev.get("assertions", []))

def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: validate_extensions.py <project-dir> [strict|permissive]")
        return 2

    mode = sys.argv[2] if len(sys.argv) == 3 else "strict"
    if mode not in ("strict","permissive"):
        print("Mode must be strict or permissive")
        return 2

    logical, errors = assemble(Path(sys.argv[1]))
    if errors:
        print("FAILED")
        for e in errors:
            print("-", e)
        return 1

    ext = logical.get("extensions", {})
    issues = []
    warnings = []

    elements = logical["model"]["elements"]
    relationships = logical["model"]["relationships"]

    def validate_obj(obj, kind):
        props = obj.get("properties", {})
        for key, value in props.items():
            definition = ext.get(key)
            if not definition:
                msg = f"{obj.get('id')}: unknown property '{key}'"
                (issues if mode == "strict" else warnings).append(msg)
                continue

            governance = definition.get("governance", {})
            if governance.get("status") == "deprecated":
                warnings.append(f"{obj.get('id')}: property '{key}' is deprecated.")

            applies = definition.get("applies_to", {})
            if kind not in applies.get("kinds", []):
                issues.append(f"{obj.get('id')}: property '{key}' does not apply to {kind}.")
                continue

            allowed_types = applies.get("archimate_types")
            if kind == "element" and allowed_types and obj.get("type") not in allowed_types:
                issues.append(
                    f"{obj.get('id')}: property '{key}' does not apply to type {obj.get('type')}."
                )

            vt = definition.get("value_type")
            if not kind_ok(value, vt):
                issues.append(f"{obj.get('id')}: property '{key}' has invalid type for {vt}.")
                continue

            if vt == "enum":
                allowed = definition.get("allowed_values", [])
                if value not in allowed:
                    issues.append(
                        f"{obj.get('id')}: property '{key}' value {value!r} not in allowed_values."
                    )

            if vt == "list":
                item_type = definition.get("item_type")
                if item_type:
                    for item in value:
                        if not kind_ok(item, item_type):
                            issues.append(
                                f"{obj.get('id')}: property '{key}' contains invalid {item_type} item."
                            )

            if definition.get("evidence_required") and not evidence_supports(obj, key):
                issues.append(
                    f"{obj.get('id')}: property '{key}' requires evidence support property:{key}."
                )

        # required extensions
        for key, definition in ext.items():
            applies = definition.get("applies_to", {})
            if kind not in applies.get("kinds", []):
                continue
            allowed_types = applies.get("archimate_types")
            if kind == "element" and allowed_types and obj.get("type") not in allowed_types:
                continue
            if definition.get("required") and key not in props:
                issues.append(f"{obj.get('id')}: required property '{key}' is missing.")

    for e in elements:
        validate_obj(e, "element")
    for r in relationships:
        validate_obj(r, "relationship")

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
    print(f"Extensions: {len(ext)}")
    print(f"Mode: {mode}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
