#!/usr/bin/env python3
from pathlib import Path
import argparse, sys, xml.etree.ElementTree as ET, yaml

ROOT=Path(__file__).resolve().parents[1]
NS="http://www.opengroup.org/xsd/archimate/3.0/"
XSI="http://www.w3.org/2001/XMLSchema-instance"

def q(ns,name):
    return f"{{{ns}}}{name}"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("xml_file")
    args=ap.parse_args()

    errors=[]
    try:
        tree=ET.parse(args.xml_file)
    except Exception as e:
        print("FAILED")
        print("-",f"XML parse error: {e}")
        return 1

    root=tree.getroot()
    if root.tag != q(NS,"model"):
        errors.append("Root element is not ArchiMate model namespace/model")
    if not root.get("identifier"):
        errors.append("Model identifier missing")
    if root.find(q(NS,"name")) is None:
        errors.append("Model name missing")

    elements=root.findall(f".//{q(NS,'element')}")
    rels=root.findall(f".//{q(NS,'relationship')}")
    defs=root.findall(f".//{q(NS,'propertyDefinition')}")

    ids=[]
    element_ids=set()
    for e in elements:
        eid=e.get("identifier")
        if eid:
            ids.append(eid); element_ids.add(eid)
        if not e.get(q(XSI,"type")):
            errors.append(f"Element {eid} missing xsi:type")

    for r in rels:
        rid=r.get("identifier")
        if rid: ids.append(rid)
        if not r.get(q(XSI,"type")):
            errors.append(f"Relationship {rid} missing xsi:type")
        if r.get("source") not in element_ids:
            errors.append(f"Relationship {rid} missing source target object: {r.get('source')}")
        if r.get("target") not in element_ids:
            errors.append(f"Relationship {rid} missing target object: {r.get('target')}")

    def_ids={d.get("identifier") for d in defs}
    ids.extend(x for x in def_ids if x)
    if len(ids)!=len(set(ids)):
        errors.append("Duplicate XML identifiers")

    for p in root.findall(f".//{q(NS,'property')}"):
        ref=p.get("propertyDefinitionRef")
        if ref not in def_ids:
            errors.append(f"Unknown propertyDefinitionRef: {ref}")

    known_elements={
        x["type"] for x in yaml.safe_load((ROOT/"metamodel"/"elements.yaml").read_text(encoding="utf-8"))["elements"]
    }
    known_rels={
        x["type"] for x in yaml.safe_load((ROOT/"metamodel"/"relationships.yaml").read_text(encoding="utf-8"))["relationships"]
    }
    for e in elements:
        typ=e.get(q(XSI,"type"))
        if typ not in known_elements:
            errors.append(f"Unknown ArchiMate element xsi:type: {typ}")
    for r in rels:
        typ=r.get(q(XSI,"type"))
        if typ not in known_rels:
            errors.append(f"Unknown ArchiMate relationship xsi:type: {typ}")

    if errors:
        print("FAILED")
        for e in errors:
            print("-",e)
        return 1

    print("OK")
    print(f"Elements: {len(elements)}")
    print(f"Relationships: {len(rels)}")
    print(f"Property definitions: {len(defs)}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
