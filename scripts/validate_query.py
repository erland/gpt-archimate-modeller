#!/usr/bin/env python3
from pathlib import Path
import argparse,json,yaml
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("query_file"); a=ap.parse_args()
    data=yaml.safe_load(Path(a.query_file).read_text(encoding="utf-8"))
    schema=json.loads((ROOT/"schemas"/"query.schema.json").read_text(encoding="utf-8"))
    try:
        import jsonschema
        errors=list(jsonschema.Draft202012Validator(schema).iter_errors(data))
        if errors:
            print("FAILED")
            for e in errors: print("-",e.message)
            return 1
    except ImportError:
        if "query" not in data:
            print("FAILED"); return 1
    print("OK"); print(f"Query: {data['query']['id']}"); return 0
if __name__=="__main__": raise SystemExit(main())
