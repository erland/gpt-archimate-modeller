#!/usr/bin/env python3
"""Require a matching Engine download URL in Chat/Plugin/OpenCode instructions."""
import argparse
import zipfile
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--version", required=True)
    p.add_argument("--dist", default="dist")
    args = p.parse_args()
    cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    project = cfg["project"]["id"]
    url = (f"https://github.com/erland/gpt-archimate-modeller/releases/download/v{args.version}/"
           f"{project}-engine-{args.version}.zip")
    for runtime, readme in (("chat", "START-HERE.md"), ("plugin", "README.md"), ("opencode", "README.md")):
        pattern = cfg["build_system"]["runtime_targets"][runtime]["filename_pattern"]
        archive = Path(args.dist) / pattern.replace("<project-id>", project).replace("<version>", args.version)
        with zipfile.ZipFile(archive) as z:
            text = z.read(readme).decode("utf-8")
        assert url in text, f"{runtime}: missing exact version-matched Engine URL in {readme}"
        assert "{{VERSION}}" not in text, f"{runtime}: unrendered version placeholder"
        print(f"PASS: {runtime} has Engine download URL for {args.version}")

if __name__ == "__main__":
    main()
