#!/usr/bin/env python3
"""Build a reproducible, standalone ArchiMate Engine ZIP from canonical sources."""
import argparse
import hashlib
import json
import tempfile
import zipfile
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"__pycache__", ".pytest_cache", ".git", "dist", "build", "release-artifacts"}
FIXED_TIME = (2020, 1, 1, 0, 0, 0)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", required=True)
    ap.add_argument("--dist", default="dist")
    args = ap.parse_args()
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    project_id = cfg["project"]["id"]
    files = {}
    for filename in ("archimate_engine.py", "selftest.py", "requirements.txt", "README.md"):
        files[filename] = (ROOT / "engine" / filename).read_bytes()
    script_names = {Path(p).name for skill in cfg["skills"]["definitions"] for p in skill.get("scripts", [])}
    # Additional supported CLI commands that are not declared by a Skill.
    script_names |= {"model_quality_report.py", "validate_project_zip.py"}
    for name in sorted(script_names):
        source = ROOT / "scripts" / name
        if not source.is_file():
            raise SystemExit(f"Missing Engine script: {source}")
        files[f"scripts/{name}"] = source.read_bytes()
    for directory in ("schemas", "metamodel", "quality", "package", "versioning"):
        for source in sorted((ROOT / directory).rglob("*")):
            if not source.is_file() or any(part in SKIP for part in source.relative_to(ROOT).parts):
                continue
            if source.suffix not in (".json", ".yaml", ".yml"):
                continue
            files[source.relative_to(ROOT).as_posix()] = source.read_bytes()
    template = ROOT / "templates" / "ea-project-split.bundle.json"
    if not template.is_file():
        raise SystemExit("Missing generated project template bundle; run generate_skill_template_bundle.py")
    files["assets/ea-project-split.bundle.json"] = template.read_bytes()
    files["VERSION"] = (args.version + "\n").encode()
    manifest = {
        "runtime_id": project_id + "-engine",
        "version": args.version,
        "files": [{"path": path, "sha256": digest(data), "size": len(data)}
                  for path, data in sorted(files.items())],
    }
    files["MANIFEST.json"] = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode()
    dist = Path(args.dist)
    dist.mkdir(parents=True, exist_ok=True)
    target = dist / f"{project_id}-engine-{args.version}.zip"
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    # Update the original GPT Byggaren delivery inventory after adding the sixth runtime archive.
    checksum_path = dist / "SHA256SUMS.txt"
    checksum_path.write_text("".join(
        f"{digest(p.read_bytes())}  {p.name}\n" for p in sorted(dist.glob("*.zip"))
    ), encoding="utf-8")
    manifest_path = dist / "DELIVERY-MANIFEST.json"
    delivery = json.loads(manifest_path.read_text(encoding="utf-8"))
    delivery["artifacts"] = [
        a for a in delivery["artifacts"]
        if a["file"] not in (target.name, "SHA256SUMS.txt")
    ]
    for path, kind in ((target, "engine_zip"), (checksum_path, "checksums")):
        delivery["artifacts"].append({
            "type": kind, "file": path.name, "sha256": digest(path.read_bytes()),
            "size": path.stat().st_size,
        })
    # Runtime ZIPs may have been postprocessed to add requirements.txt.
    # Refresh every artifact hash and size, not just the newly added Engine.
    for entry in delivery["artifacts"]:
        actual = dist / entry["file"]
        entry["sha256"] = digest(actual.read_bytes())
        entry["size"] = actual.stat().st_size
    delivery["artifacts"].sort(key=lambda a: a["file"])
    manifest_path.write_text(json.dumps(delivery, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Built standalone Engine ZIP: {target}")

if __name__ == "__main__":
    main()
