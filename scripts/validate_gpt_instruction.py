#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
FULL=ROOT/"gpt"/"SYSTEM_INSTRUCTION.md"
CUSTOM=ROOT/"gpt"/"CUSTOM_GPT_INSTRUCTION.txt"

REQUIRED_FULL=[
    "YAML-projektet är source of truth",
    "Stable ID",
    "change set",
    "Project ZIP contract",
    "Model Exchange",
    "Query",
    "Report",
    "View",
    "technical",
    "quality",
    "migration"
]

REQUIRED_CUSTOM=[
    "YAML-projektet är source of truth",
    "Stable IDs",
    "CHANGE WORKFLOW",
    "QUERY/REPORT/VIEW",
    "SLUTREGEL"
]

def main():
    errors=[]
    full=FULL.read_text(encoding="utf-8")
    custom=CUSTOM.read_text(encoding="utf-8")

    for term in REQUIRED_FULL:
        if term.casefold() not in full.casefold():
            errors.append(f"Full instruction missing: {term}")
    for term in REQUIRED_CUSTOM:
        if term.casefold() not in custom.casefold():
            errors.append(f"Custom instruction missing: {term}")

    custom_len=len(custom)
    if custom_len>8000:
        errors.append(f"Custom GPT instruction exceeds 8000 chars: {custom_len}")

    if errors:
        print("FAILED")
        for e in errors:
            print("-",e)
        return 1

    print("OK")
    print(f"Full instruction chars: {len(full)}")
    print(f"Custom GPT instruction chars: {custom_len}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
