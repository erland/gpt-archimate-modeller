#!/usr/bin/env python3
from pathlib import Path
import argparse, json, yaml

ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/"runtime/distribution-registry.yaml"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--version",required=True)
    ap.add_argument("--dir",default="release-artifacts")
    ap.add_argument("--print-paths",action="store_true")
    a=ap.parse_args()

    registry=yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    out=Path(a.dir)
    if not out.is_absolute():
        out=ROOT/out

    runtime_files=[]
    for runtime in registry["active_targets"]:
        pattern=registry["targets"][runtime]["artifact_pattern"]
        runtime_files.append(pattern.format(version=a.version))

    metadata=list(registry["release"]["include_metadata"])
    expected=runtime_files+metadata

    missing=[name for name in expected if not (out/name).is_file()]
    actual_runtime=sorted(p.name for p in out.glob("*.zip"))
    if actual_runtime!=sorted(runtime_files):
        raise SystemExit(
            "FAILED: release runtime ZIP set differs from registry: "
            f"actual={actual_runtime} expected={sorted(runtime_files)}"
        )
    if missing:
        raise SystemExit("FAILED: missing release assets: "+", ".join(missing))

    if a.print_paths:
        for name in expected:
            print(out/name)
    else:
        print("OK: exact registry release asset set verified")
        print(json.dumps({"runtime_assets":runtime_files,"metadata":metadata},indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
