#!/usr/bin/env python3
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
MM = ROOT / "metamodel"

def load(name):
    with (MM / name).open(encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    errors = []
    index = load("index.yaml")
    elements = load("elements.yaml")["elements"]
    relationships = load("relationships.yaml")["relationships"]
    connectors = load("connectors.yaml")["relationship_connectors"]
    layers = load("layers.yaml")
    aspects = load("aspects.yaml")

    etypes = [e["type"] for e in elements]
    rtypes = [r["type"] for r in relationships]

    if len(etypes) != len(set(etypes)):
        errors.append("Duplicate element type names.")
    if len(rtypes) != len(set(rtypes)):
        errors.append("Duplicate relationship type names.")

    expected = index["counts"]
    if len(elements) != expected["ordinary_element_types"]:
        errors.append("Element count does not match index.")
    if len(relationships) != expected["relationship_types"]:
        errors.append("Relationship count does not match index.")
    if len(connectors) != expected["relationship_connector_types"]:
        errors.append("Connector count does not match index.")

    known_aspects = {a["id"] for a in aspects["aspects"]}
    for e in elements:
        if e["aspect"] not in known_aspects:
            errors.append(f"Unknown aspect {e['aspect']} on {e['type']}.")

    if errors:
        print("FAILED")
        for e in errors:
            print("-", e)
        return 1

    print("OK")
    print(f"ArchiMate profile: {index['version']}")
    print(f"Elements: {len(elements)}")
    print(f"Relationships: {len(relationships)}")
    print(f"Connectors: {len(connectors)}")
    print("Exact normative pair matrix: deferred to validation step 10")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
