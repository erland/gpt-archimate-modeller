#!/usr/bin/env python3
from pathlib import Path
import yaml,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate import validate
from validate_issues import validate_file as validate_issues
from validate_temporal import validate_temporal
from architecture_states import validate_states
ROOT=Path(__file__).resolve().parents[1]; CAT=ROOT/"tests"/"fixtures"/"fixture-catalog.yaml"
def main():
    c=yaml.safe_load(CAT.read_text(encoding="utf-8")); fail=[]
    for x in c["reference_projects"]:
        r=ROOT/x["path"]; _,f=validate(r)
        e=[a for a in f if a["severity"]=="error"]
        if e: fail.append(f"{x['id']}: technical {e}")
        for label,errs in [("issues",validate_issues(r/"issues"/"issues.yaml",r)),("temporal",validate_temporal(r)[0]),("states",validate_states(r))]:
            if errs: fail.append(f"{x['id']}: {label} {errs}")
    if fail: print("FAILED"); [print("-",x) for x in fail]; return 1
    print("OK"); print(f"Reference projects: {len(c['reference_projects'])}"); return 0
if __name__=="__main__": raise SystemExit(main())
