#!/usr/bin/env python3
from __future__ import annotations
import argparse,zipfile
from pathlib import Path
import yaml

ENTRYPOINTS={
  "chat_zip":"gpt/SYSTEM_INSTRUCTION.md",
  "custom_gpt":"instructions.txt",
  "claude_projects":"project-instructions.md",
  "opencode":"AGENTS.md",
}

def read_member(zf, suffix):
    matches=[n for n in zf.namelist() if n.endswith("/"+suffix) or n==suffix]
    if len(matches)!=1:
        raise ValueError(f"expected exactly one {suffix}, found {matches}")
    return zf.read(matches[0]).decode("utf-8")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--contract",required=True)
    ap.add_argument("--runtime",required=True,choices=sorted(ENTRYPOINTS))
    ap.add_argument("--artifact",required=True)
    a=ap.parse_args()

    contract=yaml.safe_load(Path(a.contract).read_text(encoding="utf-8"))
    markers=contract["dimensions"]["behavior"]["canonical_markers"]
    errors=[]
    with zipfile.ZipFile(a.artifact) as zf:
        text=read_member(zf,ENTRYPOINTS[a.runtime]).casefold()
        for marker in markers:
            if marker.casefold() not in text:
                errors.append(f"missing behavior marker: {marker}")

        if a.runtime=="claude_projects":
            compat=read_member(zf,"compatibility.md").casefold()
            for marker in contract["reduced_runtime_requirements"]["claude_projects"]["must_document_limitations"]:
                if marker.casefold() not in compat:
                    errors.append(f"Claude limitation missing: {marker}")
            for marker in contract["reduced_runtime_requirements"]["claude_projects"]["must_preserve"]:
                if marker.casefold() not in compat:
                    errors.append(f"Claude preservation marker missing: {marker}")

    if errors:
        print("FAILED")
        for e in errors: print("-",e)
        return 1
    print(f"OK: {a.runtime} instruction adherence")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
