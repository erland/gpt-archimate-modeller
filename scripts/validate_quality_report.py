#!/usr/bin/env python3
from pathlib import Path
import argparse,json,yaml,sys

ROOT=Path(__file__).resolve().parents[1]

def main():
    errors=[]
    profile=ROOT/"quality"/"report-profile.yaml"
    descriptor=ROOT/"reports"/"dynamic"/"model-quality-report.yaml"
    engine=ROOT/"scripts"/"model_quality_report.py"
    quality=ROOT/"quality"/"profile.yaml"
    for p in (profile,descriptor,engine,quality):
        if not p.exists(): errors.append(f"Missing: {p.relative_to(ROOT)}")
    if descriptor.exists():
        d=yaml.safe_load(descriptor.read_text(encoding="utf-8"))
        r=d.get("dynamic_report") or {}
        if r.get("engine")!="scripts/model_quality_report.py":
            errors.append("Descriptor engine mismatch")
        if r.get("source")!="quality/profile.yaml":
            errors.append("Descriptor quality profile mismatch")
    if errors:
        print("FAILED")
        for e in errors: print("-",e)
        return 1
    print("OK")
    print("Dynamic model quality report configured.")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
