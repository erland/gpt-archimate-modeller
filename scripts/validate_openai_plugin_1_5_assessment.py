#!/usr/bin/env python3
from pathlib import Path
import json
import yaml

ROOT=Path(__file__).resolve().parents[1]

REQUIRED_FULL_PARITY_CAPS={
    "filesystem_read",
    "filesystem_write",
    "code_execution",
    "structured_data",
    "persistent_workspace",
    "archive_io",
}

def main():
    errors=[]
    runtime=json.loads((ROOT/"runtime/runtime-contract.json").read_text(encoding="utf-8"))
    normalized=yaml.safe_load((ROOT/"runtime/gpt-builder-1.5-contract.yaml").read_text(encoding="utf-8"))
    registry=yaml.safe_load((ROOT/"runtime/distribution-registry.yaml").read_text(encoding="utf-8"))
    assessment=(ROOT/"docs/openai-plugin-1.5-assessment.md").read_text(encoding="utf-8").casefold()

    plugin=runtime["runtime_compatibility"].get("openai_plugin",{})
    if plugin.get("status")!="implemented":
        errors.append("runtime contract OpenAI Plugin status must be implemented")
    if plugin.get("target")!="equivalent_runtime_dependent":
        errors.append("runtime contract OpenAI Plugin target must be equivalent_runtime_dependent")

    nplugin=normalized["runtime_policy"]["openai_plugin"]
    if nplugin.get("status")!="active" or nplugin.get("target")!="equivalent_runtime_dependent":
        errors.append("normalized 1.5 plugin policy must be active/equivalent_runtime_dependent")
    if nplugin.get("assessment_required") is not True:
        errors.append("OpenAI Plugin assessment must remain required")

    rplugin=registry.get("targets",{}).get("openai_plugin",{})
    if rplugin.get("status")!="active" or rplugin.get("compatibility")!="equivalent_runtime_dependent":
        errors.append("distribution registry plugin policy must be active/equivalent_runtime_dependent")
    if "openai_plugin" not in registry.get("active_targets",[]):
        errors.append("OpenAI Plugin must appear in active_targets")

    caps={k for k,v in runtime["capabilities"]["requirements"].items() if v["level"]=="required"}
    if caps!=REQUIRED_FULL_PARITY_CAPS:
        errors.append(f"required full-parity capability set changed: {sorted(caps)}")

    markers=[
        "equivalent_runtime_dependent",
        "filesystem read",
        "filesystem write",
        "code execution",
        "persistent workspace",
        "archive i/o",
        "no-false-pass",
        "approval",
        "project zip contract",
    ]
    for marker in markers:
        if marker not in assessment:
            errors.append(f"plugin assessment missing marker: {marker}")

    if errors:
        print("FAILED: OpenAI Plugin GPT Builder 1.5 assessment")
        for e in errors:
            print("-",e)
        return 1

    print("OK: OpenAI Plugin active/equivalent_runtime_dependent")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
