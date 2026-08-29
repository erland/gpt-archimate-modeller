#!/usr/bin/env python3
from pathlib import Path
import json,yaml
ROOT=Path(__file__).resolve().parents[1]
def main():
    lib=yaml.safe_load((ROOT/"views"/"standard-library.yaml").read_text(encoding="utf-8"))
    schema=json.loads((ROOT/"schemas"/"view.schema.json").read_text(encoding="utf-8"))
    errors=[]; ids=[]
    try: import jsonschema
    except ImportError: jsonschema=None
    for x in lib["views"]:
        ids.append(x["id"]); p=ROOT/x["file"]
        if not p.exists(): errors.append(f"Missing view: {x['file']}"); continue
        d=yaml.safe_load(p.read_text(encoding="utf-8"))
        if d["view"]["id"]!=x["id"]: errors.append(f"ID mismatch: {x['file']}")
        if d["view"].get("include_relationships")=="all_touching_selected": errors.append(f"{x['id']}: unsupported standard mode")
        if jsonschema: errors += [f"{x['id']}: {e.message}" for e in jsonschema.Draft202012Validator(schema).iter_errors(d)]
        if not (ROOT/d["view"]["source"]["query"]).exists(): errors.append(f"{x['id']}: missing query")
    if len(ids)!=len(set(ids)): errors.append("Duplicate view ID")
    if errors:
        print("FAILED"); [print("-",e) for e in errors]; return 1
    print("OK"); print(f"Standard views: {len(ids)}"); return 0
if __name__=="__main__": raise SystemExit(main())
