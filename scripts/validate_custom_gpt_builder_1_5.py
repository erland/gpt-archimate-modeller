#!/usr/bin/env python3
from pathlib import Path
import argparse
import zipfile
import yaml

ROOT=Path(__file__).resolve().parents[1]

def member(zf,suffix):
    matches=[n for n in zf.namelist() if n.endswith("/"+suffix) or n==suffix]
    if len(matches)!=1:
        raise ValueError(f"expected one {suffix}, found {matches}")
    return matches[0]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--artifact",required=True)
    a=ap.parse_args()
    artifact=Path(a.artifact)
    if not artifact.is_absolute():
        artifact=ROOT/artifact

    errors=[]
    contract=yaml.safe_load((ROOT/"runtime/gpt-builder-1.5-contract.yaml").read_text(encoding="utf-8"))
    if not artifact.is_file():
        print(f"FAILED: missing Custom GPT ZIP: {artifact}")
        return 1

    with zipfile.ZipFile(artifact) as zf:
        if zf.testzip():
            errors.append("Custom GPT ZIP is corrupt")

        for req in [
            "instructions.txt","builder-config.md","README.md",
            "knowledge/00-runtime-workflows.md",
            "knowledge/06-archimate-reference.yaml",
            "knowledge/08-runtime-contracts.yaml",
        ]:
            try:
                member(zf,req)
            except ValueError as exc:
                errors.append(str(exc))

        try:
            instructions=zf.read(member(zf,"instructions.txt")).decode("utf-8")
            if len(instructions)>8000:
                errors.append(f"Custom GPT instructions exceed 8000 chars: {len(instructions)}")
            for marker in contract["invariants"]:
                if marker.casefold() not in instructions.casefold():
                    errors.append(f"Custom GPT instructions missing invariant: {marker}")
        except ValueError as exc:
            errors.append(str(exc))

        try:
            builder=zf.read(member(zf,"builder-config.md")).decode("utf-8").casefold()
            required_markers=[
                "code interpreter / data analysis",
                "equivalent parity med plattformsbegränsningar",
                "projektfilerna och projekt-zip:en är auktoritativ state",
                "chattminne är inte projektets source of truth",
                "unrun verification",
                "false pass",
                "faktiskt har skapats och validerats",
            ]
            for marker in required_markers:
                if marker.casefold() not in builder:
                    errors.append(f"Custom GPT builder config missing 1.5 limitation marker: {marker}")
        except ValueError as exc:
            errors.append(str(exc))

        names=[n for n in zf.namelist() if not n.endswith("/")]
        if any("/scripts/" in "/"+n for n in names):
            errors.append("Custom GPT package must not expose repo scripts as runtime API")
        if any("/tests/" in "/"+n or "/evals/" in "/"+n for n in names):
            errors.append("Custom GPT package contains development test/eval files")

    if errors:
        print("FAILED: Custom GPT GPT Builder 1.5 verification")
        for e in errors:
            print("-",e)
        return 1

    print("OK: Custom GPT GPT Builder 1.5 verification")
    print("Compiled instruction, Knowledge, platform constraints, workspace authority and no-false-PASS preserved")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
