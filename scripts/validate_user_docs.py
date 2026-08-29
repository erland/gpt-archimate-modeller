#!/usr/bin/env python3
from pathlib import Path
import re,yaml
ROOT=Path(__file__).resolve().parents[1]
CAT=ROOT/"docs"/"user"/"catalog.yaml"

def main():
    c=yaml.safe_load(CAT.read_text(encoding="utf-8"))
    errors=[]
    ids=[]
    for d in c["documents"]:
        ids.append(d["id"])
        p=ROOT/d["file"]
        if not p.exists():
            errors.append(f"Missing user document: {d['file']}")
            continue
        text=p.read_text(encoding="utf-8")
        if not text.startswith("# "):
            errors.append(f"{d['id']}: missing H1")
        for target in re.findall(r"\]\(([^)]+\.md)\)",text):
            if "://" in target or target.startswith("#"):
                continue
            resolved=(p.parent/target).resolve()
            if not resolved.exists():
                errors.append(f"{d['id']}: broken Markdown link {target}")
    if len(ids)!=len(set(ids)):
        errors.append("Duplicate user-document ID")

    quick=(ROOT/"docs"/"user"/"quickstart.md").read_text(encoding="utf-8")
    for phrase in ("YAML är source of truth","Stable IDs","komplett nytt projekt-ZIP"):
        if phrase.lower() not in quick.lower():
            errors.append(f"Quickstart missing core concept: {phrase}")

    readme=(ROOT/"README.md").read_text(encoding="utf-8")
    if "docs/user/index.md" not in readme:
        errors.append("README does not link to user documentation")

    if errors:
        print("FAILED")
        for e in errors: print("-",e)
        return 1
    print("OK")
    print(f"User documents: {len(c['documents'])}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
