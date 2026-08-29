#!/usr/bin/env python3
from pathlib import Path
import json,yaml
ROOT=Path(__file__).resolve().parents[1]
REQUIRED_RUNTIME_EVALS={
    'EVAL-013':'runtime_bootstrap',
    'EVAL-014':'runtime_retention',
    'EVAL-015':'knowledge_routing',
}
def main():
    cat=yaml.safe_load((ROOT/"evals"/"catalog.yaml").read_text(encoding="utf-8")); schema=json.loads((ROOT/"schemas"/"llm-eval-case.schema.json").read_text(encoding="utf-8")); errors=[]; ids=[]
    try: import jsonschema
    except ImportError: jsonschema=None
    for x in cat["cases"]:
        ids.append(x["id"]); p=ROOT/x["file"]
        if not p.exists(): errors.append(f"Missing case {x['file']}"); continue
        d=yaml.safe_load(p.read_text(encoding="utf-8"))
        if d["eval_case"]["id"]!=x["id"]: errors.append(f"ID mismatch {x['file']}")
        if d["eval_case"]["category"]!=x["category"]: errors.append(f"Category mismatch {x['file']}")
        if jsonschema: errors += [f"{x['id']}: {e.message}" for e in jsonschema.Draft202012Validator(schema).iter_errors(d)]
    if len(ids)!=len(set(ids)): errors.append("Duplicate eval ID")
    by_id={x["id"]:x for x in cat["cases"]}
    for eid,category in REQUIRED_RUNTIME_EVALS.items():
        if eid not in by_id:
            errors.append(f"Missing runtime adherence eval: {eid}")
        elif by_id[eid].get("category") != category:
            errors.append(f"{eid}: expected category {category}")
    if errors: print("FAILED"); [print("-",e) for e in errors]; return 1
    print("OK"); print(f"LLM eval cases: {len(ids)}"); return 0
if __name__=="__main__": raise SystemExit(main())
