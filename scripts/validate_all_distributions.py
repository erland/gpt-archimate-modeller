#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,subprocess,sys
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/"runtime"/"distribution-registry.yaml"

def render(parts,version,output_dir):
    values={"{python}":sys.executable,"{version}":version,"{output_dir}":str(output_dir)}
    return [values.get(x,x) for x in parts]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--manifest",required=True)
    a=ap.parse_args()

    mp=Path(a.manifest)
    if not mp.is_absolute(): mp=ROOT/mp
    manifest=json.loads(mp.read_text(encoding="utf-8"))
    registry=yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    expected=registry["active_targets"]
    artifacts=manifest.get("artifacts",{})
    if list(artifacts)!=expected:
        raise SystemExit("FAILED: manifest runtime order/set differs from registry")
    for runtime,path_text in artifacts.items():
        p=Path(path_text)
        if not p.is_absolute(): p=ROOT/p
        if not p.is_file():
            raise SystemExit(f"FAILED: missing artifact for {runtime}: {p}")

    out=mp.parent
    subprocess.run(
        render(registry["unified_validator"]["command"],manifest["version"],out),
        cwd=ROOT,check=True
    )
    print("OK")
    print("All registry runtimes validated:", ", ".join(expected))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
