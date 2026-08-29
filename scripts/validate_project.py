#!/usr/bin/env python3
from pathlib import Path
import json
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "ea-project.schema.json"

def fallback_validate(data):
    errors = []
    for k in ("format_version", "project", "model"):
        if k not in data:
            errors.append(f"Missing top-level key: {k}")
    if "project" in data:
        for k in ("id", "name", "model_version"):
            if k not in data["project"]:
                errors.append(f"Missing project.{k}")
    if "model" in data:
        for k in ("elements", "relationships"):
            if k not in data["model"]:
                errors.append(f"Missing model.{k}")
    for refobj in references:
        if refobj.get("source_ref") not in source_ids:
            errors.append(f"Reference {refobj.get('id')} references missing source {refobj.get('source_ref')}")
    return errors

def validate_references(data):
    errors = []
    elements = data.get("model", {}).get("elements", [])
    relationships = data.get("model", {}).get("relationships", [])
    sources = data.get("sources", [])
    references = data.get("references", [])

    element_ids = [e.get("id") for e in elements]
    rel_ids = [r.get("id") for r in relationships]
    source_ids = {s.get("id") for s in sources}
    reference_ids = {r.get("id") for r in references}

    for label, ids in (("element", element_ids), ("relationship", rel_ids)):
        seen = set()
        for x in ids:
            if x in seen:
                errors.append(f"Duplicate {label} id: {x}")
            seen.add(x)

    element_id_set = set(element_ids)
    for r in relationships:
        if r.get("source") not in element_id_set:
            errors.append(f"Relationship {r.get('id')} source not found: {r.get('source')}")
        if r.get("target") not in element_id_set:
            errors.append(f"Relationship {r.get('id')} target not found: {r.get('target')}")

    seen_ev = set()
    for obj in list(elements) + list(relationships):
        ev = obj.get("evidence") or {}
        for assertion in ev.get("assertions", []):
            aid = assertion.get("id")
            if aid in seen_ev:
                errors.append(f"Duplicate evidence assertion id: {aid}")
            seen_ev.add(aid)
            for ref in assertion.get("source_refs", []):
                if ref not in source_ids:
                    errors.append(f"{obj.get('id')} evidence {aid} references missing source {ref}")
            for ref in assertion.get("reference_refs", []):
                if ref not in reference_ids:
                    errors.append(f"{obj.get('id')} evidence {aid} references missing reference {ref}")
    return errors

def main():
    if len(sys.argv) != 2:
        print("Usage: validate_project.py <project-yaml>")
        return 2

    path = Path(sys.argv[1])
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    errors = []
    try:
        import jsonschema
        validator = jsonschema.Draft202012Validator(schema)
        for err in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path)):
            loc = ".".join(map(str, err.absolute_path)) or "<root>"
            errors.append(f"{loc}: {err.message}")
    except ImportError:
        errors.extend(fallback_validate(data))

    errors.extend(validate_references(data))

    if errors:
        print("FAILED")
        for err in errors:
            print("-", err)
        return 1

    print("OK")
    print(f"Project: {data['project']['id']}")
    print(f"Format: {data['format_version']}")
    print(f"Model version: {data['project']['model_version']}")
    print(f"Elements: {len(data['model']['elements'])}")
    print(f"Relationships: {len(data['model']['relationships'])}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
