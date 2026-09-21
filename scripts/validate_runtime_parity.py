#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,zipfile
from pathlib import Path
import yaml

def member(zf,suffix):
    matches=[n for n in zf.namelist() if n.endswith("/"+suffix) or n==suffix]
    if len(matches)!=1:
        raise ValueError(f"expected one {suffix}, found {matches}")
    return matches[0]

def jmember(zf,suffix):
    return json.loads(zf.read(member(zf,suffix)).decode("utf-8"))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--contract",required=True)
    ap.add_argument("--runtime-contract",required=True)
    ap.add_argument("--tool-contract",required=True)
    ap.add_argument("--chat",required=True)
    ap.add_argument("--custom",required=True)
    ap.add_argument("--claude",required=True)
    ap.add_argument("--opencode",required=True)
    a=ap.parse_args()

    parity=yaml.safe_load(Path(a.contract).read_text(encoding="utf-8"))
    runtime=json.loads(Path(a.runtime_contract).read_text(encoding="utf-8"))
    tools=json.loads(Path(a.tool_contract).read_text(encoding="utf-8"))
    errors=[]

    expected=parity["active_runtimes"]
    compat=runtime["runtime_compatibility"]
    active=[x for x in expected if compat.get(x,{}).get("status")=="implemented"]
    if active!=expected:
        errors.append(f"implemented runtime set mismatch: {active}")

    for dim in ["behavior","capability","artifact","workspace_state","tool"]:
        exp=parity["dimensions"][dim]["expectations"]
        for rt in expected:
            if exp.get(rt)!=compat[rt]["target"]:
                errors.append(f"{dim}/{rt}: expectation differs from runtime target")

    req_caps=set(parity["dimensions"]["capability"]["required"])
    actual_caps={k for k,v in runtime["capabilities"]["requirements"].items() if v["level"]=="required"}
    if req_caps!=actual_caps:
        errors.append(f"required capability set mismatch: {sorted(actual_caps)}")

    outputs=runtime["artifacts"]["outputs"]
    for x in parity["dimensions"]["artifact"]["required_outputs"]:
        if outputs.get(x,{}).get("requirement")!="required":
            errors.append(f"artifact {x} must be required")
    for x in parity["dimensions"]["artifact"]["conditional_outputs"]:
        if outputs.get(x,{}).get("requirement")!="conditional":
            errors.append(f"artifact {x} must be conditional")

    ws=runtime["workspace_state"]
    if ws["state"]["authority"]!=parity["dimensions"]["workspace_state"]["authority"]:
        errors.append("workspace state authority mismatch")
    if ws["workspace"]["authority"]!=parity["dimensions"]["workspace_state"]["portable_authority"]:
        errors.append("portable workspace authority mismatch")
    if ws["state"]["conversation_fallback"] is not parity["dimensions"]["workspace_state"]["conversation_fallback"]:
        errors.append("conversation fallback mismatch")

    abstract={x["id"] for x in runtime["tools"]["tools"]}
    if abstract!=set(parity["dimensions"]["tool"]["abstract_tools"]):
        errors.append("abstract tool set mismatch")
    if len(tools["tools"])!=parity["dimensions"]["tool"]["concrete_tool_count"]:
        errors.append("concrete tool count mismatch")

    with zipfile.ZipFile(a.claude) as zf:
        compat_text=zf.read(member(zf,"compatibility.md")).decode("utf-8").casefold()
        for marker in parity["reduced_runtime_requirements"]["claude_projects"]["must_document_limitations"]:
            if marker.casefold() not in compat_text:
                errors.append(f"Claude reduced parity limitation not documented: {marker}")
        for marker in parity["reduced_runtime_requirements"]["claude_projects"]["must_preserve"]:
            if marker.casefold() not in compat_text:
                errors.append(f"Claude reduced parity preservation not explicit: {marker}")

    with zipfile.ZipFile(a.opencode) as zf:
        snap=jmember(zf,".opencode/runtime-contract.json")
        mapping=jmember(zf,".opencode/tool-mapping.json")
        cfg=jmember(zf,"opencode.json")
        req=parity["opencode_requirements"]
        root=snap.get("project_root",{})
        if root.get("explicit_argument")!=req["project_root_argument"]:
            errors.append("OpenCode projectRoot mismatch")
        mapped={x["abstract_tool"] for x in mapping.get("tools",{}).values()}
        if mapped!=abstract:
            errors.append("OpenCode abstract tool mapping coverage mismatch")
        if req["typed_custom_tools"]:
            ts=zf.read(member(zf,".opencode/tools/archimate.ts")).decode("utf-8")
            if "tool.schema" not in ts:
                errors.append("OpenCode typed custom tools missing")
        if req["direct_shell_for_canonical_mutation"] is False and cfg.get("permission",{}).get("bash")!="deny":
            errors.append("OpenCode bash must be denied for canonical mutation policy")
        for x in mapping.get("tools",{}).values():
            if x.get("mutates_canonical_state") and x.get("approval")!=req["mutating_tools_approval"]:
                errors.append("OpenCode mutating tool approval mismatch")

    # Artifact presence / structure smoke checks for other runtimes.
    with zipfile.ZipFile(a.chat) as zf:
        for req in ["gpt/SYSTEM_INSTRUCTION.md","gpt/runtime-policy.yaml","scripts/project_control.py"]:
            member(zf,req)
    with zipfile.ZipFile(a.custom) as zf:
        for req in ["instructions.txt","builder-config.md"]:
            member(zf,req)

    if errors:
        print("FAILED")
        for e in errors: print("-",e)
        return 1
    print("OK")
    print("Runtime parity accepted across behavior/capability/artifact/workspace_state/tool")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
