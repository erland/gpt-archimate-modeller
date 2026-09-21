#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys
import yaml
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
CONTRACT=ROOT/"runtime"/"runtime-contract.json"
SCHEMAS={
    "behavior":ROOT/"schemas"/"runtime-behavior-contract.schema.json",
    "capabilities":ROOT/"schemas"/"runtime-capability-contract.schema.json",
    "artifacts":ROOT/"schemas"/"runtime-artifact-contract.schema.json",
    "workspace_state":ROOT/"schemas"/"runtime-workspace-state-contract.schema.json",
    "tools":ROOT/"schemas"/"runtime-tool-contract.schema.json",
}
EXPECTED_ACTIVE=["chat_zip","custom_gpt","claude_projects","opencode"]

def main() -> int:
    errors=[]
    data=json.loads(CONTRACT.read_text(encoding="utf-8"))

    for key,path in SCHEMAS.items():
        schema=json.loads(path.read_text(encoding="utf-8"))
        problems=sorted(Draft202012Validator(schema).iter_errors(data[key]),key=lambda e:list(e.path))
        for p in problems:
            errors.append(f"{key}: {p.message}")

    project=yaml.safe_load((ROOT/"project.yaml").read_text(encoding="utf-8"))
    migration=project.get("runtime_migration",{})
    if migration.get("active_runtime_targets")!=EXPECTED_ACTIVE:
        errors.append("project runtime migration targets mismatch")

    compat=data.get("runtime_compatibility",{})
    active=[k for k,v in compat.items() if v.get("status") in {"implemented","planned"}]
    if active!=EXPECTED_ACTIVE:
        errors.append(f"runtime contract active targets mismatch: {active}")

    plugin=compat.get("openai_plugin",{})
    if plugin.get("status")!="not_planned" or plugin.get("target")!="reduced":
        errors.append("OpenAI Plugin v1 decision must remain explicit not_planned/reduced")

    if data["workspace_state"]["state"].get("conversation_fallback") is not False:
        errors.append("chat memory must not be workspace state authority")

    tools=data["tools"]["tools"]
    ids=[x["id"] for x in tools]
    if len(ids)!=len(set(ids)):
        errors.append("duplicate tool ids")
    for tool in tools:
        if tool["mutates_workspace"] and tool["approval"]!="ask":
            errors.append(f"mutating tool {tool['id']} must require approval")
    if any(t.get("concrete_projection")!="step-51" for t in tools):
        errors.append("concrete tool projection must be deferred to step 51")

    markers=data["behavior"]["required_markers"]
    instruction=(ROOT/data["behavior"]["canonical_instruction"]).read_text(encoding="utf-8")
    for marker in markers:
        if marker.casefold() not in instruction.casefold():
            errors.append(f"canonical instruction missing behavior marker: {marker}")

    if errors:
        print("FAILED")
        for e in errors: print("-",e)
        return 1
    print("OK")
    print("Runtime contract valid across behavior/capability/artifact/workspace_state/tool")
    print("Active targets:", ", ".join(EXPECTED_ACTIVE))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
