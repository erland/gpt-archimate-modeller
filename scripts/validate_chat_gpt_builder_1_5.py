#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import zipfile
import yaml

ROOT=Path(__file__).resolve().parents[1]

def member(zf, suffix):
    matches=[n for n in zf.namelist() if n.endswith("/"+suffix) or n==suffix]
    if len(matches)!=1:
        raise ValueError(f"expected one {suffix}, found {matches}")
    return matches[0]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--artifact",required=True)
    a=ap.parse_args()

    errors=[]
    artifact=Path(a.artifact)
    if not artifact.is_absolute():
        artifact=ROOT/artifact

    contract=yaml.safe_load((ROOT/"runtime/gpt-builder-1.5-contract.yaml").read_text(encoding="utf-8"))
    runtime=json.loads((ROOT/contract["canonical"]["runtime_contract"]).read_text(encoding="utf-8"))
    canonical=(ROOT/contract["canonical"]["instruction"]).read_text(encoding="utf-8")

    if not artifact.is_file():
        print(f"FAILED: missing Chat ZIP: {artifact}")
        return 1

    with zipfile.ZipFile(artifact) as zf:
        if zf.testzip():
            errors.append("Chat ZIP is corrupt")

        names=[i.filename for i in zf.infolist() if not i.is_dir()]
        roots={n.split("/")[0] for n in names}
        if len(roots)!=1:
            errors.append(f"Chat ZIP must have exactly one root, got {sorted(roots)}")

        for req in [
            "CHAT_PACKAGE.md",
            "gpt/SYSTEM_INSTRUCTION.md",
            "gpt/runtime-policy.yaml",
            "scripts/project_control.py",
            "scripts/new_project.py",
            "scripts/update_project.py",
            "scripts/validate_project_zip.py",
            "schemas/ea-project.schema.json",
            "templates/ea-project-split/project.yaml",
        ]:
            try:
                member(zf,req)
            except ValueError as exc:
                errors.append(str(exc))

        try:
            packaged_instruction=zf.read(member(zf,"gpt/SYSTEM_INSTRUCTION.md")).decode("utf-8")
            if packaged_instruction!=canonical:
                errors.append("Chat canonical instruction is not byte-identical to source")
            for marker in contract["invariants"]:
                if marker.casefold() not in packaged_instruction.casefold():
                    errors.append(f"Chat instruction missing invariant: {marker}")
        except ValueError as exc:
            errors.append(str(exc))

        try:
            bootstrap=zf.read(member(zf,"CHAT_PACKAGE.md")).decode("utf-8")
            for marker in [
                "gpt/SYSTEM_INSTRUCTION.md",
                "gpt/runtime-policy.yaml",
                "knowledge/routing.yaml",
                "Kärnflödet ska kunna starta",
                "komplett validerat EA-projekt-ZIP",
            ]:
                if marker not in bootstrap:
                    errors.append(f"Chat bootstrap missing marker: {marker}")
        except ValueError as exc:
            errors.append(str(exc))

        forbidden_roots=["tests/","evals/","release/","docs/developer/"]
        for prefix in forbidden_roots:
            if any(("/"+prefix) in ("/"+n) for n in names):
                errors.append(f"Chat ZIP contains development-only content: {prefix}")

        abstract_tools={t["id"] for t in runtime["tools"]["tools"]}
        if abstract_tools!={
            "project-read","project-validate","project-change","project-create",
            "project-package","model-query","model-analyze","model-present","model-exchange"
        }:
            errors.append("Unexpected abstract tool surface for Chat parity")

        if runtime["workspace_state"]["state"]["authority"]!="project_files":
            errors.append("Chat workspace state authority must remain project_files")
        if runtime["workspace_state"]["workspace"]["authority"]!="ea_project_zip":
            errors.append("Chat portable workspace authority must remain ea_project_zip")
        if runtime["workspace_state"]["state"]["conversation_fallback"] is not False:
            errors.append("Chat history must not become authoritative workspace state")

        required_caps={k for k,v in runtime["capabilities"]["requirements"].items() if v["level"]=="required"}
        expected_caps={
            "filesystem_read","filesystem_write","code_execution",
            "structured_data","persistent_workspace","archive_io"
        }
        if required_caps!=expected_caps:
            errors.append(f"Chat required capability set changed: {sorted(required_caps)}")

    if errors:
        print("FAILED: Chat ZIP GPT Builder 1.5 verification")
        for e in errors:
            print("-",e)
        return 1

    print("OK: Chat ZIP GPT Builder 1.5 verification")
    print("Canonical instruction, runtime toolchain, workspace authority, ZIP contract and artifact parity preserved")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
