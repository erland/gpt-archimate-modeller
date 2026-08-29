#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate import validate
from quality_check import load_yaml, run_quality, DEFAULT_PROFILE

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("--strict-relationships",action="store_true")
    ap.add_argument("--permissive-extensions",action="store_true")
    ap.add_argument("--quality-profile",default=str(DEFAULT_PROFILE))
    ap.add_argument("--json",dest="json_out")
    args=ap.parse_args()

    logical,vfind=validate(
        args.project_dir,
        strict_relationships=args.strict_relationships,
        strict_extensions=not args.permissive_extensions
    )
    verr=[x for x in vfind if x["severity"]=="error"]
    qfind=[]; score=None; counts={"error":0,"warning":0,"info":0}
    if logical is not None and not verr:
        qfind,score,counts=run_quality(logical,load_yaml(args.quality_profile))

    status="FAILED" if verr else "OK"
    print(status)
    print(f"Validation errors: {len(verr)}")
    print(f"Validation warnings: {sum(1 for x in vfind if x['severity']=='warning')}")
    if score is not None:
        print(f"Quality score: {score:.1f}/100")
        print(f"Quality warnings: {counts['warning']}")
        print(f"Quality info: {counts['info']}")
    for x in vfind:
        oid=f" [{x['object_id']}]" if x.get("object_id") else ""
        print(f"- VALIDATION {x['severity'].upper()} {x['code']}{oid}: {x['message']}")
    for x in qfind:
        oid=f" [{x['object_id']}]" if x.get("object_id") else ""
        print(f"- QUALITY {x['severity'].upper()} {x['code']}{oid}: {x['message']}")
    if args.json_out:
        Path(args.json_out).write_text(json.dumps({
            "status":status,
            "validation":{"findings":vfind},
            "quality":{"score":score,"counts":counts,"findings":qfind}
        },indent=2,ensure_ascii=False),encoding="utf-8")
    return 1 if verr else 0

if __name__=="__main__":
    raise SystemExit(main())
