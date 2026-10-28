#!/usr/bin/env python3
import argparse
from pathlib import Path
import hashlib
import json
import yaml
p=argparse.ArgumentParser()
p.add_argument("--version",required=True)
p.add_argument("--dir",default="dist")
p.add_argument("--print-paths",action="store_true")
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
manifest=json.loads((directory/"DELIVERY-MANIFEST.json").read_text(encoding="utf-8"))
assert manifest["project"]==project_id and manifest["version"]==a.version
entries={item["file"]:item for item in manifest["artifacts"]}
expected=names|{"SHA256SUMS.txt"}
assert set(entries)==expected, f"manifest entries mismatch: {set(entries) ^ expected}"
for filename,entry in entries.items():
    data=(directory/filename).read_bytes()
    assert entry["sha256"]==hashlib.sha256(data).hexdigest(), f"manifest hash mismatch: {filename}"
    assert entry["size"]==len(data), f"manifest size mismatch: {filename}"
if a.print_paths:
    for name in sorted(names): print((directory/name).resolve())
    print((directory/"SHA256SUMS.txt").resolve())
    print((directory/"DELIVERY-MANIFEST.json").resolve())
else:
    print("PASS: six archives, manifest and checksums")
