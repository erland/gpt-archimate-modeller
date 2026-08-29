#!/usr/bin/env python3
from pathlib import Path
import argparse, json, yaml

ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("report_file")
    args=ap.parse_args()

    path=Path(args.report_file)
    data=yaml.safe_load(path.read_text(encoding="utf-8"))
    schema=json.loads((ROOT/"schemas"/"report.schema.json").read_text(encoding="utf-8"))

    try:
        import jsonschema
        errors=list(jsonschema.Draft202012Validator(schema).iter_errors(data))
        if errors:
            print("FAILED")
            for e in errors:
                print("-",e.message)
            return 1
    except ImportError:
        if "report" not in data:
            print("FAILED")
            return 1

    # Cross-file checks for query references when report is inside package.
    errors=[]
    for section in data["report"]["sections"]:
        qref=section["source"]["query"]
        qpath=(path.parent.parent/qref) if not Path(qref).is_absolute() else Path(qref)
        if not qpath.exists():
            # Also allow refs relative to package root when validating standard report.
            alt=ROOT/qref
            if not alt.exists():
                errors.append(f"Query not found: {qref}")

        render=section["render"]
        if render["type"]=="table" and not render.get("columns"):
            errors.append(f"Section {section['id']}: table requires columns")
        if render["type"]=="list" and not render.get("item_fields"):
            errors.append(f"Section {section['id']}: list requires item_fields")

    if errors:
        print("FAILED")
        for e in errors:
            print("-",e)
        return 1

    print("OK")
    print(f"Report: {data['report']['id']}")
    print(f"Sections: {len(data['report']['sections'])}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
