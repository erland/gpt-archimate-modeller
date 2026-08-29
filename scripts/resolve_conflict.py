#!/usr/bin/env python3
from pathlib import Path
import argparse,json,yaml

ROOT=Path(__file__).resolve().parents[1]
SCHEMA=ROOT/"schemas"/"resolution.schema.json"

def read_yaml(p): return yaml.safe_load(Path(p).read_text(encoding="utf-8"))

def validate_resolution(doc):
    schema=json.loads(SCHEMA.read_text(encoding="utf-8"))
    try:
        import jsonschema
        errs=list(jsonschema.Draft202012Validator(schema).iter_errors(doc))
        if errs:
            raise ValueError("; ".join(e.message for e in errs))
    except ImportError:
        if not isinstance(doc,dict) or "resolution" not in doc:
            raise ValueError("Invalid resolution document")
    r=doc["resolution"]
    if r["action"]=="merge" and not r.get("canonical_id"):
        raise ValueError("merge requires canonical_id")
    if r["conflict_type"]=="property_conflict" and not r.get("property"):
        raise ValueError("property_conflict requires property")
    return r

def translate(doc):
    r=validate_resolution(doc)
    action=r["action"]
    ops=[]
    notes=[]

    if action=="keep_separate":
        if r.get("issue_id"):
            ops.append({
                "op":"add_issue",
                "issue":{
                    "id":r["issue_id"],
                    "type":"possible_duplicate",
                    "status":"resolved",
                    "description":r["reason"]
                }
            })
        notes.append("No element merge; objects remain separate.")

    elif action=="defer":
        if not r.get("issue_id"):
            raise ValueError("defer requires issue_id")
        issue_type="possible_duplicate" if r["conflict_type"]=="possible_duplicate" else "conflicting_information"
        ops.append({
            "op":"add_issue",
            "issue":{
                "id":r["issue_id"],
                "type":issue_type,
                "status":"open",
                "description":r["reason"]
            }
        })

    elif action=="prefer_existing":
        notes.append("Incoming conflicting value/object is not applied.")
        if r.get("issue_id"):
            ops.append({
                "op":"add_issue",
                "issue":{
                    "id":r["issue_id"],
                    "type":"conflicting_information",
                    "status":"resolved",
                    "description":r["reason"]
                }
            })

    elif action=="prefer_incoming":
        if r["conflict_type"]=="property_conflict":
            ops.append({
                "op":"update_element",
                "id":r["existing_id"],
                "set":{f"properties.{r['property']}":r.get("incoming_value")}
            })
        else:
            notes.append("Incoming preference requires domain-specific change set; no unsafe automatic retype/merge generated.")

    elif action=="reject_incoming":
        notes.append("Incoming object/value rejected; model unchanged.")

    elif action=="merge":
        notes.append("Merge decision confirmed, but structural merge must be materialized as explicit change operations.")
        notes.append("Retain canonical_id and repoint/remove through normal change workflow; no implicit merge executed.")

    return {
        "resolution_result":{
            "resolution_id":r["id"],
            "action":action,
            "generated_operations":ops,
            "notes":notes
        }
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("resolution_file")
    ap.add_argument("--json",action="store_true")
    a=ap.parse_args()
    try:
        out=translate(read_yaml(a.resolution_file))
        if a.json:
            print(json.dumps(out,indent=2,ensure_ascii=False))
        else:
            print(yaml.safe_dump(out,sort_keys=False,allow_unicode=True,width=120),end="")
        return 0
    except Exception as e:
        print("FAILED"); print("-",str(e)); return 1

if __name__=="__main__":
    raise SystemExit(main())
