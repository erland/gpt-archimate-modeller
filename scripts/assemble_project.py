#!/usr/bin/env python3
from pathlib import Path
import json
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_SCHEMA = ROOT / "schemas" / "ea-package.schema.json"
LOGICAL_SCHEMA = ROOT / "schemas" / "ea-project.schema.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from identity import ID_RE, expected_prefix_for_type

def read_yaml(path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)

def schema_errors(data, schema_path):
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    try:
        import jsonschema
    except ImportError:
        return []
    validator = jsonschema.Draft202012Validator(schema)
    errors = []
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path)):
        loc = ".".join(map(str, err.absolute_path)) or "<root>"
        errors.append(f"{loc}: {err.message}")
    return errors

def safe_resolve(project_root, rel):
    p = (project_root / rel).resolve()
    root = project_root.resolve()
    if p != root and root not in p.parents:
        raise ValueError(f"Path escapes project root: {rel}")
    return p

def assemble(project_root):
    project_root = Path(project_root)
    manifest_path = project_root / "project.yaml"
    if not manifest_path.exists():
        raise FileNotFoundError("project.yaml not found")

    manifest = read_yaml(manifest_path)
    errors = schema_errors(manifest, PACKAGE_SCHEMA)

    files = manifest.get("files", {})
    elements = []
    seen_partition_ids = set()

    for part in files.get("element_partitions", []):
        pid = part.get("id")
        if pid in seen_partition_ids:
            errors.append(f"Duplicate partition id: {pid}")
        seen_partition_ids.add(pid)
        path = safe_resolve(project_root, part["path"])
        if not path.exists():
            errors.append(f"Missing element partition: {part['path']}")
            continue
        data = read_yaml(path) or {}
        if set(data.keys()) - {"elements"}:
            errors.append(f"Unexpected keys in {part['path']}")
        elements.extend(data.get("elements", []))

    def load_wrapped(rel, key, default):
        path = safe_resolve(project_root, rel)
        if not path.exists():
            errors.append(f"Missing file: {rel}")
            return default
        data = read_yaml(path) or {}
        extra = set(data.keys()) - {key}
        if extra:
            errors.append(f"Unexpected keys in {rel}: {sorted(extra)}")
        return data.get(key, default)

    relationships = load_wrapped(files["relationships"], "relationships", [])
    sources = load_wrapped(files["sources"], "sources", [])
    references = load_wrapped(files["references"], "references", [])
    extensions = load_wrapped(files["extensions"], "extensions", {})
    specializations = load_wrapped(files["specializations"], "specializations", {})
    issues_path = safe_resolve(project_root, files["issues"])
    issues = []
    observations = []
    if not issues_path.exists():
        errors.append(f"Missing file: {files['issues']}")
    else:
        issues_data = read_yaml(issues_path) or {}
        extra = set(issues_data.keys()) - {"issues", "observations"}
        if extra:
            errors.append(f"Unexpected keys in {files['issues']}: {sorted(extra)}")
        issues = issues_data.get("issues", [])
        observations = issues_data.get("observations", [])

    architecture_states = {"states": [], "transitions": []}
    architecture_path = safe_resolve(project_root, files["architecture_states"])
    if not architecture_path.exists():
        errors.append(f"Missing file: {files['architecture_states']}")
    else:
        architecture_states = read_yaml(architecture_path) or architecture_states

    # Identity counters
    counter_path = safe_resolve(project_root, files["identity_counters"])
    counters_data = {}
    if not counter_path.exists():
        errors.append(f"Missing file: {files['identity_counters']}")
    else:
        counters_data = read_yaml(counter_path) or {}
        if "counters" not in counters_data:
            errors.append("Identity counter file missing 'counters'.")

    logical = {
        "format_version": manifest["format_version"],
        "project": manifest["project"],
        "model": {"elements": elements, "relationships": relationships},
        "sources": sources,
        "references": references,
        "extensions": extensions,
        "specializations": specializations,
        "issues": issues,
        "observations": observations,
        "architecture_states": architecture_states,
    }

    errors.extend(schema_errors(logical, LOGICAL_SCHEMA))

    element_ids = [e.get("id") for e in elements]
    rel_ids = [r.get("id") for r in relationships]
    source_ids = [s.get("id") for s in sources]
    reference_ids = [r.get("id") for r in references]
    issue_ids = [i.get("id") for i in issues]

    for label, ids in (
        ("element", element_ids),
        ("relationship", rel_ids),
        ("source", source_ids),
        ("reference", reference_ids),
        ("issue", issue_ids)
    ):
        seen = set()
        for item_id in ids:
            if item_id in seen:
                errors.append(f"Duplicate {label} id: {item_id}")
            seen.add(item_id)
            if item_id and not ID_RE.match(item_id):
                errors.append(f"Invalid {label} id format: {item_id}")

    # Prefix correctness
    for e in elements:
        exp = expected_prefix_for_type(e.get("type"))
        if exp and e.get("id") and not e["id"].startswith(exp + "-"):
            errors.append(f"{e['id']} uses wrong prefix for {e.get('type')}; expected {exp}")

    for r in relationships:
        if r.get("id") and not r["id"].startswith("REL-"):
            errors.append(f"{r['id']} uses wrong prefix for relationship; expected REL")
    for s in sources:
        if s.get("id") and not s["id"].startswith("SRC-"):
            errors.append(f"{s['id']} uses wrong prefix for source; expected SRC")
    for rref in references:
        if rref.get("id") and not rref["id"].startswith("REF-"):
            errors.append(f"{rref['id']} uses wrong prefix for reference; expected REF")
    for i in issues:
        if i.get("id") and not i["id"].startswith("ISS-"):
            errors.append(f"{i['id']} uses wrong prefix for issue; expected ISS")

    # Referential integrity
    element_set = set(element_ids)
    source_set = set(source_ids)
    reference_set = set(reference_ids)

    for rref in references:
        if rref.get("source_ref") not in source_set:
            errors.append(f"Reference {rref.get('id')} source not found: {rref.get('source_ref')}")
    for rel in relationships:
        if rel.get("source") not in element_set:
            errors.append(f"Relationship {rel.get('id')} source not found: {rel.get('source')}")
        if rel.get("target") not in element_set:
            errors.append(f"Relationship {rel.get('id')} target not found: {rel.get('target')}")

    for obj in list(elements) + list(relationships):
        ev = obj.get("evidence") or {}
        for assertion in ev.get("assertions", []):
            for ref in assertion.get("source_refs", []):
                if ref not in source_set:
                    errors.append(f"{obj.get('id')} evidence {assertion.get('id')} references missing source {ref}")
            for ref in assertion.get("reference_refs", []):
                if ref not in reference_set:
                    errors.append(f"{obj.get('id')} evidence {assertion.get('id')} references missing reference {ref}")

    # Counter consistency: max allocated ID must be <= counter.
    counters = counters_data.get("counters", {})
    evidence_ids = []
    for obj in list(elements) + list(relationships):
        for assertion in (obj.get("evidence") or {}).get("assertions", []):
            evidence_ids.append(assertion.get("id"))
    all_ids = element_ids + rel_ids + source_ids + reference_ids + issue_ids + evidence_ids
    maxima = {}
    for item_id in all_ids:
        if not item_id or not ID_RE.match(item_id):
            continue
        prefix, num = item_id.split("-")
        maxima[prefix] = max(maxima.get(prefix, 0), int(num))
    for prefix, max_num in maxima.items():
        counter = int(counters.get(prefix, 0))
        if counter < max_num:
            errors.append(
                f"Identity counter {prefix}={counter} is behind existing max ID {prefix}-{max_num:06d}"
            )

    return logical, errors

def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: assemble_project.py <project-dir> [output-yaml]")
        return 2

    logical, errors = assemble(Path(sys.argv[1]))
    if errors:
        print("FAILED")
        for e in errors:
            print("-", e)
        return 1

    print("OK")
    print(f"Project: {logical['project']['id']}")
    print(f"Elements: {len(logical['model']['elements'])}")
    print(f"Relationships: {len(logical['model']['relationships'])}")

    if len(sys.argv) == 3:
        out = Path(sys.argv[2])
        out.write_text(
            yaml.safe_dump(logical, sort_keys=False, allow_unicode=True, width=120),
            encoding="utf-8"
        )
        print(f"Assembled: {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
