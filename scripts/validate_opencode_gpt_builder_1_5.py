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
    tool_contract=json.loads((ROOT/"runtime/archimate-tool-contract.json").read_text(encoding="utf-8"))
    with zipfile.ZipFile(p) as zf:
        agents=zf.read(member(zf,"AGENTS.md")).decode("utf-8")
        if agents!=canonical: errors.append("OpenCode AGENTS.md is not byte-identical to canonical instruction")
        snap=json.loads(zf.read(member(zf,".opencode/runtime-contract.json")).decode("utf-8"))
        mapping=json.loads(zf.read(member(zf,".opencode/tool-mapping.json")).decode("utf-8"))
        cfg=json.loads(zf.read(member(zf,"opencode.json")).decode("utf-8"))
        if snap.get("compatibility")!="equivalent": errors.append("OpenCode must remain equivalent")
        root=snap.get("project_root",{})
        if root.get("explicit_argument")!="projectRoot": errors.append("OpenCode explicit projectRoot missing")
        if root.get("runtime_workspace_is_not_target_project") is not True: errors.append("OpenCode workspace/project separation missing")
        if root.get("path_traversal")!="forbidden": errors.append("OpenCode path traversal policy missing")
        if cfg.get("permission",{}).get("bash")!="deny": errors.append("OpenCode bash must remain denied")
        abstract_expected={t["abstract_tool"] for t in tool_contract["tools"]}
        abstract_actual={x["abstract_tool"] for x in mapping.get("tools",{}).values()}
        if abstract_actual!=abstract_expected: errors.append("OpenCode abstract tool mapping coverage mismatch")
        for x in mapping.get("tools",{}).values():
            if x.get("mutates_canonical_state") and x.get("approval")!="ask":
                errors.append("OpenCode mutating mapped tool must require ask approval")
        ts=zf.read(member(zf,".opencode/tools/archimate.ts")).decode("utf-8")
        if "tool.schema" not in ts: errors.append("OpenCode typed tool schemas missing")
        if "Path escapes OpenCode worktree" not in ts: errors.append("OpenCode path guard missing")
    if errors:
        print("FAILED: OpenCode GPT Builder 1.5 verification")
        for e in errors: print("-",e)
        return 1
    print("OK: OpenCode GPT Builder 1.5 verification")
    return 0

if __name__=="__main__": raise SystemExit(main())
