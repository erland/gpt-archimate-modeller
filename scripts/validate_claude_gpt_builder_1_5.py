#!/usr/bin/env python3
from pathlib import Path
import argparse, json, zipfile, yaml

ROOT=Path(__file__).resolve().parents[1]

def member(zf,suffix):
    m=[n for n in zf.namelist() if n.endswith("/"+suffix) or n==suffix]
    if len(m)!=1: raise ValueError(f"expected one {suffix}, found {m}")
    return m[0]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--artifact",required=True); a=ap.parse_args()
    p=Path(a.artifact); p = p if p.is_absolute() else ROOT/p
    errors=[]
    parity=yaml.safe_load((ROOT/"evals/runtime-parity-contract.yaml").read_text(encoding="utf-8"))
    canonical=(ROOT/"gpt/SYSTEM_INSTRUCTION.md").read_text(encoding="utf-8")
    with zipfile.ZipFile(p) as zf:
        inst=zf.read(member(zf,"project-instructions.md")).decode("utf-8")
        if inst!=canonical: errors.append("Claude project instructions are not byte-identical to canonical instruction")
        compat=zf.read(member(zf,"compatibility.md")).decode("utf-8").casefold()
        for marker in parity["reduced_runtime_requirements"]["claude_projects"]["must_document_limitations"]:
            if marker.casefold() not in compat: errors.append(f"Claude missing limitation: {marker}")
        for marker in parity["reduced_runtime_requirements"]["claude_projects"]["must_preserve"]:
            if marker.casefold() not in compat: errors.append(f"Claude missing preservation marker: {marker}")
        names=zf.namelist()
        if any("/scripts/" in "/"+n for n in names): errors.append("Claude package must not include executable runtime scripts")
        rc=json.loads(zf.read(member(zf,"runtime-contract.json")).decode("utf-8"))
        cc=rc["runtime_compatibility"]["claude_projects"]
        if cc.get("status")!="implemented" or cc.get("target")!="reduced":
            errors.append("Claude runtime contract must remain implemented/reduced")
        ws=rc["workspace_state"]
        if ws["state"]["authority"]!="project_files" or ws["state"]["conversation_fallback"] is not False:
            errors.append("Claude workspace-state authority mismatch")
    if errors:
        print("FAILED: Claude GPT Builder 1.5 verification")
        for e in errors: print("-",e)
        return 1
    print("OK: Claude GPT Builder 1.5 verification")
    return 0

if __name__=="__main__": raise SystemExit(main())
