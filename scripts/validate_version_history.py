#!/usr/bin/env python3
from pathlib import Path
import argparse, yaml
def read_yaml(p): return yaml.safe_load(Path(p).read_text(encoding="utf-8"))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("project_dir"); a=ap.parse_args()
    root=Path(a.project_dir)
    mf=read_yaml(root/"project.yaml")
    idx=read_yaml(root/"changes"/"index.yaml") if (root/"changes"/"index.yaml").exists() else {"changes":[]}
    hist=read_yaml(root/"versioning"/"history.yaml") if (root/"versioning"/"history.yaml").exists() else {"history":[]}
    errors=[]
    ids=[x["id"] for x in idx.get("changes",[])]
    vers=[x["model_version"] for x in hist.get("history",[])]
    if len(ids)!=len(set(ids)): errors.append("Duplicate change-set ID")
    if len(vers)!=len(set(vers)): errors.append("Duplicate model_version")
    for x in idx.get("changes",[]):
        if not (root/"changes"/x["file"]).exists(): errors.append(f"Missing {x['file']}")
    indexed={x["file"] for x in idx.get("changes",[])}
    for p in (root/"changes").glob("CHG-*.yaml"):
        if p.name not in indexed: errors.append(f"Unindexed change file {p.name}")
    if hist.get("history") and mf["project"]["model_version"]!=hist["history"][-1]["model_version"]:
        errors.append("Current model_version != latest history")
    if errors:
        print("FAILED"); [print("-",e) for e in errors]; return 1
    print("OK"); print(f"Model version: {mf['project']['model_version']}"); return 0
if __name__=="__main__": raise SystemExit(main())
