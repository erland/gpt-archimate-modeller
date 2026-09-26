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
    if plugin.get("status")!="not_planned":
        errors.append("runtime contract OpenAI Plugin status must remain not_planned")
    if plugin.get("target")!="reduced":
        errors.append("runtime contract OpenAI Plugin target must remain reduced")

    nplugin=normalized["runtime_policy"]["openai_plugin"]
    if nplugin.get("status")!="not_active" or nplugin.get("target")!="reduced":
        errors.append("normalized 1.5 plugin policy must remain not_active/reduced")
    if nplugin.get("assessment_required") is not True:
        errors.append("OpenAI Plugin assessment must remain required")

    rplugin=registry.get("inactive_targets",{}).get("openai_plugin",{})
    if rplugin.get("status")!="not_active" or rplugin.get("compatibility")!="reduced":
        errors.append("distribution registry plugin policy must remain not_active/reduced")
    if "openai_plugin" in registry.get("active_targets",[]):
        errors.append("OpenAI Plugin must not appear in active_targets")
    if "openai_plugin" in registry.get("targets",{}):
        errors.append("OpenAI Plugin must not have an active distribution target")

    caps={k for k,v in runtime["capabilities"]["requirements"].items() if v["level"]=="required"}
    if caps!=REQUIRED_FULL_PARITY_CAPS:
        errors.append(f"required full-parity capability set changed: {sorted(caps)}")

    markers=[
        "reduced / advisory only",
        "filesystem read",
        "filesystem write",
        "code execution",
        "persistent workspace",
        "archive i/o",
        "no-false-pass",
        "ingen",
    ]
    for marker in markers:
        if marker not in assessment:
            errors.append(f"plugin assessment missing marker: {marker}")

    if errors:
        print("FAILED: OpenAI Plugin GPT Builder 1.5 assessment")
        for e in errors:
            print("-",e)
        return 1

    print("OK: OpenAI Plugin remains not_active/reduced advisory only")
    print("No distribution or full runtime parity is claimed")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
