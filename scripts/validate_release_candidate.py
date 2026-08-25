#!/usr/bin/env python3
from pathlib import Path
import hashlib,yaml
ROOT=Path(__file__).resolve().parents[1]
def sh(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()
def main():
    errors=[]
    m=yaml.safe_load((ROOT/"release"/"RC-MANIFEST.yaml").read_text(encoding="utf-8"))
    rc=m["release_candidate"]
    if rc["version"]!="1.0.0-rc.3": errors.append("Unexpected RC version")
    if rc["package_version"]!="0.44.1": errors.append("Unexpected package version")
    if rc["plan_step_completed"]!=44: errors.append("Unexpected completed step")
    for x in rc["canonical_contract_hashes"]:
        p=ROOT/x["path"]
        if not p.exists(): errors.append(f"Missing contract file: {x['path']}")
        elif sh(p)!=x["sha256"]: errors.append(f"Contract hash mismatch: {x['path']}")
    project=yaml.safe_load((ROOT/"project.yaml").read_text(encoding="utf-8"))
    if project["project"]["project_version"]!="0.44.1": errors.append("project.yaml version mismatch")
    if project["project"]["plan_step_completed"]!=44: errors.append("project.yaml step mismatch")
    if project["architecture"].get("release_candidate")!="1.0.0-rc.3": errors.append("project.yaml RC mismatch")
    if "1.0.0-rc.3" not in (ROOT/"README.md").read_text(encoding="utf-8"): errors.append("README missing RC version")
    if errors:
        print("FAILED")
        for e in errors: print("-",e)
        return 1
    print("OK")
    print("Release candidate: 1.0.0-rc.3")
    print(f"Contract hashes: {len(rc['canonical_contract_hashes'])}")
    return 0
if __name__=="__main__": raise SystemExit(main())
