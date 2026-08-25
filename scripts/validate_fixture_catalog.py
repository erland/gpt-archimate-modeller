#!/usr/bin/env python3
from pathlib import Path
import yaml,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate import validate
from validate_issues import validate_file as validate_issues
from validate_temporal import validate_temporal
from architecture_states import validate_states
ROOT=Path(__file__).resolve().parents[1]; CAT=ROOT/"tests"/"fixtures"/"fixture-catalog.yaml"
def collect(r,s):
    r=Path(r)
    if s in ("technical_validation","relationship_validation","evidence","extensions","specializations"):
        _,f=validate(r); return [f"{x.get('code','')}: {x.get('message','')}" for x in f if x["severity"]=="error"]
    if s=="temporal": return validate_temporal(r)[0]
    if s=="architecture_states": return validate_states(r)
    if s=="issues_observations": return validate_issues(r/"issues"/"issues.yaml",r)
    return []
def main():
    c=yaml.safe_load(CAT.read_text(encoding="utf-8")); fail=[]; ids=[]
    for g in ("reference_projects","invalid_fixtures"):
        for x in c[g]:
            ids.append(x["id"])
            if not (ROOT/x["path"]).exists(): fail.append(f"{x['id']}: missing path")
    if len(ids)!=len(set(ids)): fail.append("Duplicate fixture/reference ID")
    for x in c["invalid_fixtures"]:
        m=collect(ROOT/x["path"],x["subsystem"])
        if not m: fail.append(f"{x['id']}: unexpectedly valid")
        elif x["expected_fragment"].lower() not in "\n".join(m).lower(): fail.append(f"{x['id']}: expected fragment missing")
    if fail: print("FAILED"); [print("-",x) for x in fail]; return 1
    print("OK"); print(f"Invalid fixtures: {len(c['invalid_fixtures'])}"); return 0
if __name__=="__main__": raise SystemExit(main())
