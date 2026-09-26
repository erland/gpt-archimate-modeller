#!/usr/bin/env python3
from pathlib import Path
import json
import yaml

ROOT=Path(__file__).resolve().parents[1]

def main():
    errors=[]
    contract=yaml.safe_load((ROOT/"runtime/gpt-builder-1.5-contract.yaml").read_text(encoding="utf-8"))
    runtime=json.loads((ROOT/contract["canonical"]["runtime_contract"]).read_text(encoding="utf-8"))
    tools=json.loads((ROOT/contract["canonical"]["tool_contract"]).read_text(encoding="utf-8"))
    registry=yaml.safe_load((ROOT/contract["canonical"]["distribution_registry"]).read_text(encoding="utf-8"))
    instruction=(ROOT/contract["canonical"]["instruction"]).read_text(encoding="utf-8")

    if contract["builder"]["target_version"]!="1.5.0":
        errors.append("target builder version must be 1.5.0")
    if contract["builder"]["behavior_preserving"] is not True:
        errors.append("migration must remain behavior-preserving")

    req_caps={k for k,v in runtime["capabilities"]["requirements"].items() if v["level"]=="required"}
    if req_caps!=set(contract["contracts"]["capabilities"]["required"]):
        errors.append(f"required capability mismatch: {sorted(req_caps)}")

    outputs=runtime["artifacts"]["outputs"]
    for name in contract["contracts"]["artifacts"]["required"]:
        if outputs.get(name,{}).get("requirement")!="required":
            errors.append(f"required artifact contract mismatch: {name}")

    ws=runtime["workspace_state"]
    if ws["state"]["authority"]!=contract["contracts"]["state"]["authority"]:
        errors.append("workspace state authority mismatch")
    if ws["workspace"]["authority"]!=contract["contracts"]["state"]["portable_authority"]:
        errors.append("portable workspace authority mismatch")
    if ws["state"]["conversation_fallback"] is not contract["contracts"]["state"]["conversation_authoritative"]:
        errors.append("conversation authority mismatch")

    if runtime["tools"].get("project_root_argument")!=contract["contracts"]["tools"]["project_root_argument"]:
        errors.append("projectRoot contract mismatch")
    if runtime["tools"].get("generic_shell_is_canonical_api") is not False:
        errors.append("generic shell must not be canonical API")

    abstract={x["id"] for x in runtime["tools"]["tools"]}
    concrete={x["abstract_tool"] for x in tools["tools"]}
    if abstract!=concrete:
        errors.append("concrete ArchiMate tool contract does not cover all abstract tools")
    for tool in runtime["tools"]["tools"]:
        if tool["mutates_workspace"] and tool["approval"]!=contract["contracts"]["tools"]["mutation_approval"]:
            errors.append(f"mutating abstract tool lacks ask approval: {tool['id']}")
    for tool in tools["tools"]:
        if tool["mutates_canonical_state"] and tool["approval"]!=contract["contracts"]["tools"]["mutation_approval"]:
            errors.append(f"mutating concrete tool lacks ask approval: {tool['id']}")

    expected_active=contract["runtime_policy"]["active"]
    if registry["active_targets"]!=expected_active:
        errors.append("distribution registry active targets differ from 1.5 contract")

    compat=runtime["runtime_compatibility"]
    for runtime_id,target in contract["runtime_policy"]["compatibility"].items():
        if compat.get(runtime_id,{}).get("target")!=target:
            errors.append(f"runtime compatibility mismatch: {runtime_id}")
        if compat.get(runtime_id,{}).get("status")!="implemented":
            errors.append(f"runtime must remain implemented: {runtime_id}")

    plugin=compat.get("openai_plugin",{})
    pc=contract["runtime_policy"]["openai_plugin"]
    if plugin.get("status")!="not_planned" or plugin.get("target")!=pc["target"]:
        errors.append("OpenAI Plugin assessment baseline changed unexpectedly")

    for marker in contract["invariants"]:
        if marker.casefold() not in instruction.casefold():
            errors.append(f"canonical instruction missing invariant: {marker}")

    if errors:
        print("FAILED: GPT Builder 1.5 normalized contract")
        for e in errors:
            print("-",e)
        return 1

    print("OK: GPT Builder 1.5 normalized contract")
    print("Preserved behavior/capability/artifact/state/tool contracts for four active runtimes")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
