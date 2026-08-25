#!/usr/bin/env python3
from pathlib import Path
import argparse, json, yaml

ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("view_file")
    args=ap.parse_args()
    path=Path(args.view_file)
    data=yaml.safe_load(path.read_text(encoding="utf-8"))
    schema=json.loads((ROOT/"schemas"/"view.schema.json").read_text(encoding="utf-8"))

    try:
        import jsonschema
        errors=list(jsonschema.Draft202012Validator(schema).iter_errors(data))
        if errors:
            print("FAILED")
            for e in errors:
                print("-",e.message)
            return 1
    except ImportError:
        if "view" not in data:
            print("FAILED")
            return 1

    qref=data["view"]["source"]["query"]
    candidates=[path.parent.parent/qref, ROOT/qref]
    if not any(p.exists() for p in candidates):
        print("FAILED")
        print(f"- Query not found: {qref}")
        return 1

    print("OK")
    print(f"View: {data['view']['id']}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
