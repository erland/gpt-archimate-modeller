#!/usr/bin/env python3
"""Deterministically serialize EA project template into a text resource for portable Skills."""
import argparse
import base64
import json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",default=str(Path(__file__).resolve().parents[1]))
    args=ap.parse_args()
    root=Path(args.root)
    source=root/"templates"/"ea-project-split"
    if not (source/"project.yaml").is_file():
        raise SystemExit("Missing authoritative EA project template")
    entries={}
    for file in sorted(source.rglob("*")):
        if file.is_file():
            rel=file.relative_to(source).as_posix()
            entries[rel]=base64.b64encode(file.read_bytes()).decode("ascii")
    out=root/"templates"/"ea-project-split.bundle.json"
    out.write_text(json.dumps({"format_version":1,"files":entries},ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n",encoding="utf-8")
    print(f"Serialized {len(entries)} template files into {out}")
if __name__=="__main__":
    main()
