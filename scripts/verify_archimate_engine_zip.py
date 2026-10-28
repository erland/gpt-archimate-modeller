#!/usr/bin/env python3
"""Validate the standalone Engine ZIP and run its selftest after extraction."""
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", required=True)
    ap.add_argument("--dist", default="dist")
    args = ap.parse_args()
    project_id = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))["project"]["id"]
    archive = Path(args.dist) / f"{project_id}-engine-{args.version}.zip"
    with tempfile.TemporaryDirectory(prefix="verify-archimate-engine-") as tmp:
        destination = Path(tmp)
        with zipfile.ZipFile(archive) as z:
            names = z.namelist()
            assert len(names) == len(set(names)), "duplicate archive paths"
            assert all(not Path(n).is_absolute() and ".." not in Path(n).parts for n in names), "unsafe paths"
            manifest = json.loads(z.read("MANIFEST.json"))
            assert manifest["version"] == args.version
            expected = {entry["path"]: entry for entry in manifest["files"]}
            assert set(expected) == set(names) - {"MANIFEST.json"}
            for name, entry in expected.items():
                data = z.read(name)
                assert hashlib.sha256(data).hexdigest() == entry["sha256"], name
                assert len(data) == entry["size"], name
            z.extractall(destination)
        result = subprocess.run(
            [sys.executable, str(destination / "archimate_engine.py"), "selftest"],
            capture_output=True, text=True, cwd=destination
        )
        if result.returncode:
            raise SystemExit(f"Engine selftest failed:\n{result.stdout}\n{result.stderr}")
        print(result.stdout.strip())
        print(f"PASS: standalone engine archive and manifest ({archive.name})")

if __name__ == "__main__":
    main()
