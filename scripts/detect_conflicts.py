#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys,yaml

sys.path.insert(0,str(Path(__file__).resolve().parent))
from assemble_project import assemble
from identity import normalize_name

def detect(project_root, incoming_file=None):
    logical,errors=assemble(Path(project_root))
    if errors:
        raise ValueError("; ".join(errors))

    findings=[]
    elements=logical["model"]["elements"]
    by_id={e["id"]:e for e in elements}

    # Existing duplicate candidates
    for i,a in enumerate(elements):
        for b in elements[i+1:]:
            reasons=[]
            if a.get("type")==b.get("type") and a.get("name")==b.get("name"):
                reasons.append("exact_name_type")
            if normalize_name(a.get("name",""))==normalize_name(b.get("name","")):
                reasons.append("normalized_name")
            aa={normalize_name(x) for x in (a.get("aliases") or [])}
            ba={normalize_name(x) for x in (b.get("aliases") or [])}
            if aa.intersection(ba):
                reasons.append("shared_alias")
            if reasons:
                findings.append({
                    "conflict_type":"possible_duplicate",
                    "existing_id":a["id"],
                    "incoming_id":b["id"],
                    "reasons":sorted(set(reasons))
                })

    # Optional incoming object/change-set inspection
    if incoming_file:
        doc=yaml.safe_load(Path(incoming_file).read_text(encoding="utf-8")) or {}
        objects=[]
        if "element" in doc:
            objects=[doc["element"]]
        elif "elements" in doc:
            objects=doc["elements"]
        elif "change_set" in doc:
            for op in doc["change_set"].get("operations",[]):
                if op.get("op")=="add_element" and op.get("element"):
                    objects.append(op["element"])

        for inc in objects:
            iid=inc.get("id")
            if iid in by_id:
                old=by_id[iid]
                if old.get("type")!=inc.get("type"):
                    findings.append({
                        "conflict_type":"identity_conflict",
                        "existing_id":iid,
                        "incoming_id":iid,
                        "existing_type":old.get("type"),
                        "incoming_type":inc.get("type")
                    })
                elif old.get("name")!=inc.get("name"):
                    findings.append({
                        "conflict_type":"identity_conflict",
                        "existing_id":iid,
                        "incoming_id":iid,
                        "existing_name":old.get("name"),
                        "incoming_name":inc.get("name")
                    })

            for old in elements:
                if iid and old["id"]==iid:
                    continue
                reasons=[]
                if inc.get("name") and old.get("name")==inc.get("name") and inc.get("type")==old.get("type"):
                    reasons.append("exact_name_type")
                if inc.get("name") and normalize_name(old.get("name",""))==normalize_name(inc["name"]):
                    reasons.append("normalized_name")
                if reasons:
                    findings.append({
                        "conflict_type":"possible_duplicate",
                        "existing_id":old["id"],
                        "incoming_id":iid,
                        "reasons":sorted(set(reasons))
                    })

                if inc.get("name") and normalize_name(old.get("name",""))==normalize_name(inc["name"]) \
                   and inc.get("type") and old.get("type")!=inc.get("type"):
                    findings.append({
                        "conflict_type":"type_conflict",
                        "existing_id":old["id"],
                        "incoming_id":iid,
                        "existing_type":old.get("type"),
                        "incoming_type":inc.get("type")
                    })

    return findings

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("--incoming")
    ap.add_argument("--json",action="store_true")
    a=ap.parse_args()
    try:
        findings=detect(a.project_dir,a.incoming)
        out={"conflict_detection":{"count":len(findings),"findings":findings}}
        if a.json:
            print(json.dumps(out,indent=2,ensure_ascii=False))
        else:
            print(yaml.safe_dump(out,sort_keys=False,allow_unicode=True,width=120),end="")
        return 0
    except Exception as e:
        print("FAILED"); print("-",str(e)); return 1

if __name__=="__main__":
    raise SystemExit(main())
