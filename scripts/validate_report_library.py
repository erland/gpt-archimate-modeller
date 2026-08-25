#!/usr/bin/env python3
from pathlib import Path
import json,yaml
ROOT=Path(__file__).resolve().parents[1]
def main():
    lib=yaml.safe_load((ROOT/"reports"/"standard-library.yaml").read_text(encoding="utf-8"))
    schema=json.loads((ROOT/"schemas"/"report.schema.json").read_text(encoding="utf-8"))
    errors=[]; ids=[]
    try: import jsonschema
    except ImportError: jsonschema=None
    for item in lib["reports"]:
        ids.append(item["id"]); p=ROOT/item["file"]
        if not p.exists(): errors.append(f"Missing report: {item['file']}"); continue
        d=yaml.safe_load(p.read_text(encoding="utf-8"))
        if d["report"]["id"]!=item["id"]: errors.append(f"ID mismatch: {item['file']}")
        if jsonschema:
            errors += [f"{item['id']}: {e.message}" for e in jsonschema.Draft202012Validator(schema).iter_errors(d)]
        for s in d["report"]["sections"]:
            if not (ROOT/s["source"]["query"]).exists(): errors.append(f"{item['id']}: missing query {s['source']['query']}")
    if len(ids)!=len(set(ids)): errors.append("Duplicate report ID")
    if errors:
        print("FAILED"); [print("-",e) for e in errors]; return 1
    print("OK"); print(f"Standard reports: {len(ids)}"); return 0
if __name__=="__main__": raise SystemExit(main())
