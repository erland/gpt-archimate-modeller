#!/usr/bin/env python3
from pathlib import Path
import re,yaml
ROOT=Path(__file__).resolve().parents[1]
CAT=ROOT/"docs"/"developer"/"catalog.yaml"

def main():
    c=yaml.safe_load(CAT.read_text(encoding="utf-8"))
    errors=[]; ids=[]
    for d in c["documents"]:
        ids.append(d["id"])
        p=ROOT/d["file"]
        if not p.exists():
            errors.append(f"Missing developer document: {d['file']}")
            continue
        text=p.read_text(encoding="utf-8")
        if not text.startswith("# "):
            errors.append(f"{d['id']}: missing H1")
        for target in re.findall(r"\]\(([^)]+\.md)\)",text):
            if "://" in target or target.startswith("#"):
                continue
            if not (p.parent/target).resolve().exists():
                errors.append(f"{d['id']}: broken Markdown link {target}")
    if len(ids)!=len(set(ids)):
        errors.append("Duplicate developer-document ID")

    required={
        "architecture.md":["YAML","source of truth","Derived"],
        "modules.md":["assemble_project.py","apply_changes.py","pack_project.py"],
        "testing.md":["run_tests.py","fixtures","LLM evals"],
        "release-and-compatibility.md":["breaking","migration","release"]
    }
    for file,phrases in required.items():
        text=(ROOT/"docs"/"developer"/file).read_text(encoding="utf-8").lower()
        for phrase in phrases:
            if phrase.lower() not in text:
                errors.append(f"{file}: missing required concept {phrase}")

    readme=(ROOT/"README.md").read_text(encoding="utf-8")
    if "docs/developer/index.md" not in readme:
        errors.append("README does not link developer docs")

    if errors:
        print("FAILED")
        for e in errors: print("-",e)
        return 1
    print("OK")
    print(f"Developer documents: {len(c['documents'])}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
