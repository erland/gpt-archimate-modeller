#!/usr/bin/env python3
"""Fail if a project distribution contains generated outputs or nested distributions."""
import argparse
import io
import zipfile
from pathlib import Path

GENERATED = {"dist", "build", "release-artifacts", ".git", "__pycache__", ".pytest_cache", ".venv"}

def violations(archive):
    problems = []
    with zipfile.ZipFile(archive) as z:
        for item in z.infolist():
            name = item.filename
            path = Path(name)
            if path.is_absolute() or ".." in path.parts:
                problems.append(f"unsafe path: {name}")
            if any(part in GENERATED for part in path.parts):
                problems.append(f"generated directory: {name}")
            if path.suffix.lower() == ".zip" and path.name.startswith("archimate-yaml-ea-gpt-"):
                problems.append(f"nested distribution ZIP: {name}")
    return problems

def selftest():
    for name, expected in [
        ("README.md", False),
        ("release-artifacts/old.zip", True),
        ("dist/old.zip", True),
        ("build/stale.txt", True),
        ("examples/portable-project/ea-project-split.zip", False),
        ("docs/archimate-yaml-ea-gpt-chat-1.0.0.zip", True),
        ("../escape.txt", True),
    ]:
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, "w") as z:
            z.writestr(name, "test")
        stream.seek(0)
        assert bool(violations(stream)) == expected, name
    print("PASS: project ZIP hygiene negative/positive tests")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version")
    parser.add_argument("--dir", default="dist")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        selftest()
        return
    if not args.version:
        parser.error("--version is required unless --selftest is used")
    archives = list(Path(args.dir).glob(f"*-project-{args.version}.zip"))
    if len(archives) != 1:
        raise SystemExit(f"FAIL: expected exactly one project ZIP, found {len(archives)}")
    problems = violations(archives[0])
    if problems:
        raise SystemExit("FAIL: project ZIP contains unexpected content:\n" + "\n".join(problems))
    print(f"PASS: clean project ZIP ({archives[0].name})")

if __name__ == "__main__":
    main()
