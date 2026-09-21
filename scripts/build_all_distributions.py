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
    ap.add_argument("--version",required=True)
    ap.add_argument("--output-dir",required=True)
    a=ap.parse_args()

    registry=yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    out=Path(a.output_dir)
    if not out.is_absolute(): out=ROOT/out
    out.mkdir(parents=True,exist_ok=True)

    cmd=render(registry["unified_builder"]["command"],a.version,out)
    subprocess.run(cmd,cwd=ROOT,check=True)

    artifacts={}
    for runtime in registry["active_targets"]:
        pattern=registry["targets"][runtime]["artifact_pattern"]
        artifact=out/pattern.format(version=a.version)
        if not artifact.is_file():
            raise SystemExit(f"FAILED: builder did not create {artifact}")
        artifacts[runtime]=artifact.relative_to(ROOT).as_posix() if artifact.is_relative_to(ROOT) else artifact.as_posix()

    expected={Path(x).name for x in artifacts.values()}
    actual={p.name for p in out.glob("*.zip")}
    if actual!=expected:
        raise SystemExit(f"FAILED: built ZIP set differs from registry: actual={sorted(actual)} expected={sorted(expected)}")

    manifest={
        "schema_version":1,
        "version":a.version,
        "registry":"runtime/distribution-registry.yaml",
        "artifacts":artifacts,
    }
    mp=out/"distribution-build-manifest.json"
    mp.write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print(mp)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
