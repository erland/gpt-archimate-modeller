#!/usr/bin/env python3
import argparse
from pathlib import Path
import hashlib
import yaml
p=argparse.ArgumentParser()
p.add_argument("--version",required=True)
p.add_argument("--dir",default="dist")
a=p.parse_args()
root=Path(__file__).resolve().parents[1]
cfg=yaml.safe_load((root/"gpt-project.yaml").read_text())
project_id=cfg["project"]["id"]
names={t["filename_pattern"].replace("<project-id>",project_id).replace("<version>",a.version) for t in cfg["build_system"]["runtime_targets"].values()}
names.add(f"{project_id}-project-{a.version}.zip")
directory=Path(a.dir)
actual={x.name for x in directory.glob("*.zip")}
assert actual==names, f"archive mismatch: {actual ^ names}"
lines=(directory/"SHA256SUMS.txt").read_text().splitlines()
checks={}
for line in lines:
    digest,filename=line.split(None,1)
    checks[filename.strip()]=digest
assert set(checks)==names
for name in names:
    assert hashlib.sha256((directory/name).read_bytes()).hexdigest()==checks[name]
assert (directory/"DELIVERY-MANIFEST.json").is_file()
print("PASS: six archives, manifest and checksums")
