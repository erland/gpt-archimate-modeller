#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
import sys
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
CONTRACT=ROOT/"runtime"/"archimate-tool-contract.json"
SCHEMA=ROOT/"schemas"/"archimate-runtime-tool-contract.schema.json"
RUNTIME=ROOT/"runtime"/"runtime-contract.json"

def placeholders(command):
    out=set()
    for token in command:
        out.update(re.findall(r"\{([A-Za-z][A-Za-z0-9]*)\}",token))
    return out

def main() -> int:
    errors=[]
    data=json.loads(CONTRACT.read_text(encoding="utf-8"))
    schema=json.loads(SCHEMA.read_text(encoding="utf-8"))
    for err in sorted(Draft202012Validator(schema).iter_errors(data),key=lambda e:list(e.path)):
        errors.append(err.message)

    runtime=json.loads(RUNTIME.read_text(encoding="utf-8"))
    abstract={x["id"]:x for x in runtime["tools"]["tools"]}
    ids=[]
    covered=set()
    for tool in data.get("tools",[]):
        ids.append(tool["id"])
        covered.add(tool["abstract_tool"])
        if tool["abstract_tool"] not in abstract:
            errors.append(f"{tool['id']}: unknown abstract tool {tool['abstract_tool']}")
        script=ROOT/tool["implementation"]["script"]
        if not script.is_file():
            errors.append(f"{tool['id']}: mapped script missing: {tool['implementation']['script']}")
        props=tool["input_schema"].get("properties",{})
        required=set(tool["input_schema"].get("required",[]))
        if "projectRoot" not in required:
            errors.append(f"{tool['id']}: projectRoot must be required")
        missing=placeholders(tool["implementation"]["command"])-set(props)
        if missing:
            errors.append(f"{tool['id']}: command placeholders missing from input schema: {sorted(missing)}")
        if tool["mutates_canonical_state"] and tool["approval"]!="ask":
            errors.append(f"{tool['id']}: canonical mutation must require approval")
        if tool["abstract_tool"] in abstract:
            expected=abstract[tool["abstract_tool"]]["mutates_workspace"]
            if expected and not tool["mutates_canonical_state"]:
                errors.append(f"{tool['id']}: abstract mutation contract requires canonical mutation")
        if any(x in tool["implementation"]["script"] for x in ["build_distributions","run_tests","validate_distributions"]):
            errors.append(f"{tool['id']}: development/release script exposed")

    if len(ids)!=len(set(ids)):
        errors.append("duplicate concrete tool ids")
    required_abstract={x["id"] for x in runtime["tools"]["tools"] if x["requirement"]=="required"}
    if not required_abstract.issubset(covered):
        errors.append(f"required abstract tools lack concrete coverage: {sorted(required_abstract-covered)}")
    if data["path_policy"].get("traversal")!="forbidden":
        errors.append("path traversal must be forbidden")

    if errors:
        print("FAILED")
        for e in errors: print("-",e)
        return 1
    print("OK")
    print(f"Concrete runtime tools: {len(ids)}")
    print("Required abstract tools covered:", ", ".join(sorted(required_abstract)))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
