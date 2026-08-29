#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys, yaml, re, datetime as dt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from assemble_project import assemble
from identity import expected_prefix_for_type, ID_RE
from validate_temporal import validate_temporal

def load_yaml(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))

def add(results, severity, code, message, object_id=None):
    results.append({
        "severity": severity,
        "code": code,
        "object_id": object_id,
        "message": message,
    })

def check_types(logical, results):
    metamodel_elements = load_yaml(ROOT/"metamodel"/"elements.yaml")["elements"]
    metamodel_rels = load_yaml(ROOT/"metamodel"/"relationships.yaml")["relationships"]
    known_e = {x["type"] for x in metamodel_elements}
    known_r = {x["type"] for x in metamodel_rels}

    for e in logical["model"]["elements"]:
        if e.get("type") not in known_e:
            add(results, "error", "ARCH-ELEMENT-TYPE", f"Unknown ArchiMate element type {e.get('type')}", e.get("id"))
        exp = expected_prefix_for_type(e.get("type"))
        if exp and e.get("id") and not e["id"].startswith(exp+"-"):
            add(results, "error", "ID-PREFIX", f"Expected prefix {exp} for {e.get('type')}", e.get("id"))

    for r in logical["model"]["relationships"]:
        if r.get("type") not in known_r:
            add(results, "error", "ARCH-REL-TYPE", f"Unknown ArchiMate relationship type {r.get('type')}", r.get("id"))

def check_relationship_pairs(logical, results, strict_relationships=False):
    rules = load_yaml(ROOT/"metamodel"/"relationship-matrix.yaml")
    table = {
        (x["source_type"], x["target_type"]): set(x["allowed"])
        for x in rules.get("validated_pairs", [])
    }
    elements = {e["id"]: e for e in logical["model"]["elements"]}

    for r in logical["model"]["relationships"]:
        s = elements.get(r.get("source"))
        t = elements.get(r.get("target"))
        if not s or not t:
            continue
        pair = (s["type"], t["type"])
        if pair not in table:
            sev = "error" if strict_relationships else "warning"
            add(
                results, sev, "ARCH-REL-PAIR-UNCOVERED",
                f"No portable exact pair rule yet for {pair[0]} -> {pair[1]}; relationship {r['type']} not asserted valid.",
                r["id"]
            )
            continue
        allowed = table[pair]
        if r["type"] not in allowed:
            add(
                results, "error", "ARCH-REL-PAIR-INVALID",
                f"{r['type']} is not allowed for {pair[0]} -> {pair[1]}; allowed: {', '.join(sorted(allowed))}",
                r["id"]
            )

def check_evidence(logical, results):
    source_ids = {s["id"] for s in logical.get("sources", [])}
    ref_ids = {r["id"] for r in logical.get("references", [])}
    seen_ev = set()
    for obj in logical["model"]["elements"] + logical["model"]["relationships"]:
        ev = obj.get("evidence")
        if not ev:
            continue
        kinds = {a.get("kind") for a in ev.get("assertions", [])}
        if ev.get("status") == "inferred" and not ({"inferred","derived"} & kinds):
            add(results, "error", "EV-STATUS", "inferred status requires inferred/derived assertion", obj["id"])
        if ev.get("status") == "document_confirmed" and "explicit" not in kinds:
            add(results, "error", "EV-STATUS", "document_confirmed requires explicit assertion", obj["id"])
        if ev.get("status") == "user_confirmed" and "user_statement" not in kinds:
            add(results, "error", "EV-STATUS", "user_confirmed requires user_statement assertion", obj["id"])
        for a in ev.get("assertions", []):
            aid = a.get("id")
            if aid in seen_ev:
                add(results, "error", "EV-DUPLICATE-ID", f"Duplicate evidence assertion {aid}", obj["id"])
            seen_ev.add(aid)
            if a.get("kind") in ("inferred","derived") and not a.get("reason"):
                add(results, "error", "EV-REASON", f"{aid} requires reason", obj["id"])
            for x in a.get("source_refs", []):
                if x not in source_ids:
                    add(results, "error", "EV-SOURCE-REF", f"{aid} references missing source {x}", obj["id"])
            for x in a.get("reference_refs", []):
                if x not in ref_ids:
                    add(results, "error", "EV-REFERENCE-REF", f"{aid} references missing reference {x}", obj["id"])

def check_sources(logical, results):
    source_ids = {s["id"] for s in logical.get("sources", [])}
    seen_locators = set()
    for s in logical.get("sources", []):
        origin = s.get("origin") or {}
        kind = origin.get("kind")
        required = {"file":"path","url":"uri","conversation":"conversation_ref","external_system":"system"}.get(kind)
        if required and not origin.get(required):
            add(results, "error", "SRC-ORIGIN", f"{kind} origin requires {required}", s["id"])
    for ref in logical.get("references", []):
        if ref.get("source_ref") not in source_ids:
            add(results, "error", "REF-SOURCE", f"Missing source {ref.get('source_ref')}", ref["id"])
        loc = ref.get("locator") or {}
        if loc.get("kind") == "line_range" and ("start" not in loc or "end" not in loc):
            add(results, "error", "REF-LINE-RANGE", "line_range requires start and end", ref["id"])
        key=(ref.get("source_ref"),loc.get("kind"),loc.get("value"),loc.get("start"),loc.get("end"))
        if key in seen_locators:
            add(results, "warning", "REF-DUPLICATE-LOCATOR", "Duplicate source+locator", ref["id"])
        seen_locators.add(key)

def type_ok(value, vt):
    if vt=="string": return isinstance(value,str)
    if vt=="integer": return isinstance(value,int) and not isinstance(value,bool)
    if vt=="number": return isinstance(value,(int,float)) and not isinstance(value,bool)
    if vt=="boolean": return isinstance(value,bool)
    if vt=="date":
        try: dt.date.fromisoformat(value); return isinstance(value,str)
        except Exception: return False
    if vt=="enum": return True
    if vt=="list": return isinstance(value,list)
    if vt=="reference": return isinstance(value,str)
    return False

def evidence_supports(obj, prop):
    return any(
        f"property:{prop}" in a.get("supports",[])
        for a in (obj.get("evidence") or {}).get("assertions",[])
    )

def check_extensions(logical, results, strict=True):
    ext=logical.get("extensions",{})
    for kind, objs in (("element", logical["model"]["elements"]), ("relationship",logical["model"]["relationships"])):
        for obj in objs:
            props=obj.get("properties",{})
            for key,val in props.items():
                d=ext.get(key)
                if not d:
                    add(results, "error" if strict else "warning", "EXT-UNKNOWN", f"Unknown property {key}", obj["id"])
                    continue
                applies=d.get("applies_to",{})
                if kind not in applies.get("kinds",[]):
                    add(results,"error","EXT-APPLIES",f"{key} does not apply to {kind}",obj["id"])
                    continue
                ats=applies.get("archimate_types")
                if kind=="element" and ats and obj.get("type") not in ats:
                    add(results,"error","EXT-ARCH-TYPE",f"{key} does not apply to {obj.get('type')}",obj["id"])
                vt=d.get("value_type")
                if not type_ok(val,vt):
                    add(results,"error","EXT-VALUE-TYPE",f"{key} invalid value type for {vt}",obj["id"])
                if vt=="enum" and val not in d.get("allowed_values",[]):
                    add(results,"error","EXT-ENUM",f"{key} value {val!r} not allowed",obj["id"])
                if d.get("evidence_required") and not evidence_supports(obj,key):
                    add(results,"error","EXT-EVIDENCE",f"{key} requires evidence support",obj["id"])
                if (d.get("governance") or {}).get("status")=="deprecated":
                    add(results,"warning","EXT-DEPRECATED",f"{key} is deprecated",obj["id"])

def check_specializations(logical, results):
    specs=logical.get("specializations",{})
    visiting=set(); visited=set()
    def visit(name,stack):
        if name in visited: return
        if name in visiting:
            add(results,"error","SPEC-CYCLE"," -> ".join(stack+[name]))
            return
        visiting.add(name)
        p=specs.get(name,{}).get("parent_specialization")
        if p:
            if p not in specs:
                add(results,"error","SPEC-PARENT",f"{name} parent {p} not found")
            else:
                if specs[p].get("base_type") != specs[name].get("base_type"):
                    add(results,"error","SPEC-BASE",f"{name} base_type differs from parent {p}")
                visit(p,stack+[name])
        visiting.remove(name); visited.add(name)
    for n in specs: visit(n,[])
    for e in logical["model"]["elements"]:
        s=e.get("specialization")
        if not s: continue
        if s not in specs:
            add(results,"error","SPEC-UNKNOWN",f"Unknown specialization {s}",e["id"])
        elif e.get("type") != specs[s].get("base_type"):
            add(results,"error","SPEC-TYPE",f"{s} base_type is {specs[s].get('base_type')}",e["id"])

def check_temporal(project_dir, results):
    errors, warnings = validate_temporal(project_dir)
    for message in errors:
        add(results, "error", "TIME-INVALID", message)
    for message in warnings:
        add(results, "warning", "TIME-WARNING", message)

def validate(project_dir, strict_relationships=False, strict_extensions=True):
    results=[]
    try:
        logical, assembly_errors = assemble(Path(project_dir))
    except Exception as e:
        return None, [{"severity":"error","code":"PACKAGE-LOAD","object_id":None,"message":str(e)}]
    for e in assembly_errors:
        add(results,"error","PACKAGE-INTEGRITY",e)
    if assembly_errors:
        return logical, results

    check_types(logical,results)
    check_relationship_pairs(logical,results,strict_relationships)
    check_sources(logical,results)
    check_evidence(logical,results)
    check_extensions(logical,results,strict_extensions)
    check_specializations(logical,results)
    check_temporal(project_dir,results)
    return logical,results

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("--strict-relationships",action="store_true")
    ap.add_argument("--permissive-extensions",action="store_true")
    ap.add_argument("--json",dest="json_out")
    args=ap.parse_args()
    logical,results=validate(
        args.project_dir,
        strict_relationships=args.strict_relationships,
        strict_extensions=not args.permissive_extensions
    )
    errors=[x for x in results if x["severity"]=="error"]
    warnings=[x for x in results if x["severity"]=="warning"]
    status="FAILED" if errors else ("OK_WITH_WARNINGS" if warnings else "OK")
    print(status)
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    for x in results:
        oid=f" [{x['object_id']}]" if x.get("object_id") else ""
        print(f"- {x['severity'].upper()} {x['code']}{oid}: {x['message']}")
    if args.json_out:
        Path(args.json_out).write_text(json.dumps({
            "status":status,"errors":len(errors),"warnings":len(warnings),"findings":results
        },indent=2,ensure_ascii=False),encoding="utf-8")
    return 1 if errors else 0

if __name__=="__main__":
    raise SystemExit(main())
