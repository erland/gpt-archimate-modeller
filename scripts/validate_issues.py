#!/usr/bin/env python3
from pathlib import Path
import argparse,json,yaml
ROOT=Path(__file__).resolve().parents[1]
SCHEMA=ROOT/"schemas"/"issues-observations.schema.json"
def rd(p): return yaml.safe_load(Path(p).read_text(encoding="utf-8")) or {}
def validate_file(path,project_root=None):
    d=rd(path); errors=[]
    schema=json.loads(SCHEMA.read_text(encoding="utf-8"))
    try:
        import jsonschema
        errors += [e.message for e in jsonschema.Draft202012Validator(schema).iter_errors(d)]
    except ImportError: pass
    items=d.get("issues",[])+d.get("observations",[])
    ids=[x.get("id") for x in items]
    if len(ids)!=len(set(ids)): errors.append("Duplicate issue/observation ID")
    for x in items:
        if x.get("status")=="ignored" and not x.get("ignore_reason"): errors.append(f"{x.get('id')}: ignored requires ignore_reason")
        if x.get("status")=="dismissed" and not x.get("dismiss_reason"): errors.append(f"{x.get('id')}: dismissed requires dismiss_reason")
        if x.get("status")=="resolved" and not (x.get("resolution") or x.get("resolution_ref") or x.get("resolved_by_change")):
            errors.append(f"{x.get('id')}: resolved requires resolution metadata")
        if x.get("status")=="promoted" and not x.get("promoted_to_issue"): errors.append(f"{x.get('id')}: promoted requires promoted_to_issue")
    if project_root:
        root=Path(project_root); object_ids=set()
        for p in (root/"model"/"elements").glob("*.yaml"): object_ids |= {e.get("id") for e in rd(p).get("elements",[])}
        object_ids |= {r.get("id") for r in rd(root/"model"/"relationships.yaml").get("relationships",[])}
        src={x.get("id") for x in rd(root/"sources"/"sources.yaml").get("sources",[])}
        refs={x.get("id") for x in rd(root/"sources"/"references.yaml").get("references",[])}
        issues={x.get("id") for x in d.get("issues",[])}
        for x in items:
            for r in x.get("object_refs",[]) or []:
                if r not in object_ids: errors.append(f"{x.get('id')}: unknown object_ref {r}")
            for r in x.get("source_refs",[]) or []:
                if r not in src: errors.append(f"{x.get('id')}: unknown source_ref {r}")
            for r in x.get("reference_refs",[]) or []:
                if r not in refs: errors.append(f"{x.get('id')}: unknown reference_ref {r}")
            if x.get("promoted_to_issue") and x["promoted_to_issue"] not in issues:
                errors.append(f"{x.get('id')}: unknown promoted_to_issue {x['promoted_to_issue']}")
    return errors
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("issues_file"); ap.add_argument("--project-dir"); a=ap.parse_args()
    e=validate_file(a.issues_file,a.project_dir)
    if e:
        print("FAILED"); [print("-",x) for x in e]; return 1
    d=rd(a.issues_file); print("OK"); print(f"Issues: {len(d.get('issues',[]))}"); print(f"Observations: {len(d.get('observations',[]))}"); return 0
if __name__=="__main__": raise SystemExit(main())
