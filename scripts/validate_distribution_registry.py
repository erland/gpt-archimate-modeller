#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sys
import yaml

ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/"runtime"/"distribution-registry.yaml"
PROJECT=ROOT/"project.yaml"
CONTRACT=ROOT/"runtime"/"runtime-contract.json"
EXPECTED=["chat_zip","custom_gpt","claude_projects","opencode"]

def script_refs(command):
    return [x for x in command if isinstance(x,str) and x.startswith("scripts/")]

def main():
    errors=[]
    registry=yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    project=yaml.safe_load(PROJECT.read_text(encoding="utf-8"))
    contract=json.loads(CONTRACT.read_text(encoding="utf-8"))

    active=registry.get("active_targets",[])
    if active!=EXPECTED:
        errors.append(f"active targets must be {EXPECTED!r}, got {active!r}")
    if len(active)!=len(set(active)):
        errors.append("duplicate active targets")

    project_active=project.get("runtime_migration",{}).get("active_runtime_targets",[])
    if project_active!=active:
        errors.append("project runtime targets differ from distribution registry")

    targets=registry.get("targets",{})
    patterns=[]
    for runtime in active:
        cfg=targets.get(runtime)
        if not cfg:
            errors.append(f"missing target config: {runtime}")
            continue
        pattern=cfg.get("artifact_pattern")
        if not isinstance(pattern,str) or "{version}" not in pattern:
            errors.append(f"{runtime}: artifact_pattern must contain {{version}}")
        else:
            patterns.append(pattern)
        compat=contract.get("runtime_compatibility",{}).get(runtime,{})
        if compat.get("status")!="implemented":
            errors.append(f"{runtime}: runtime contract status must be implemented")
        if cfg.get("compatibility")!=compat.get("target"):
            errors.append(f"{runtime}: registry compatibility must match runtime contract target")
    if len(patterns)!=len(set(patterns)):
        errors.append("artifact patterns must be unique")

    for section in ["unified_builder","unified_validator"]:
        cmd=registry.get(section,{}).get("command")
        if not isinstance(cmd,list) or not cmd:
            errors.append(f"{section}.command missing")
            continue
        for rel in script_refs(cmd):
            if not (ROOT/rel).is_file():
                errors.append(f"{section}: referenced script missing: {rel}")

    hygiene=registry.get("hygiene",{})
    if not hygiene.get("generated_roots"):
        errors.append("hygiene.generated_roots missing")
    if not hygiene.get("forbidden_runtime_projection_paths"):
        errors.append("hygiene.forbidden_runtime_projection_paths missing")

    if errors:
        print("FAILED")
        for e in errors: print("-",e)
        return 1
    print("OK")
    print("Distribution registry synchronized with project and runtime contract")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
