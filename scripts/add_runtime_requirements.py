#!/usr/bin/env python3
"""Include explicit Python dependencies in the four script-capable runtime ZIPs."""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def patch_archive(path, requirements):
    with zipfile.ZipFile(path) as archive:
        files = {name: archive.read(name) for name in archive.namelist()}
    manifest = json.loads(files["MANIFEST.json"])
    files["requirements.txt"] = requirements
    entries = {entry["path"]: entry for entry in manifest["files"]}
    entries["requirements.txt"] = {
        "path": "requirements.txt",
        "sha256": hashlib.sha256(requirements).hexdigest(),
        "size": len(requirements),
    }
    manifest["files"] = [entries[name] for name in sorted(entries)]
    files["MANIFEST.json"] = json.dumps(manifest, ensure_ascii=False, indent=2).encode()
    temp = path.with_suffix(".zip.tmp")
    with zipfile.ZipFile(temp, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, (2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)
    temp.replace(path)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", required=True)
    ap.add_argument("--dist", default="dist")
    args = ap.parse_args()
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    project_id = cfg["project"]["id"]
    requirements = (ROOT / "engine" / "requirements.txt").read_bytes()
    for runtime in ("chat", "claude_skills", "opencode", "plugin"):
        pattern = cfg["build_system"]["runtime_targets"][runtime]["filename_pattern"]
        name = pattern.replace("<project-id>", project_id).replace("<version>", args.version)
        patch_archive(Path(args.dist) / name, requirements)
        print(f"Added requirements.txt: {name}")

if __name__ == "__main__":
    main()
