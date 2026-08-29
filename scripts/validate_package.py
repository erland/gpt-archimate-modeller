#!/usr/bin/env python3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from assemble_project import assemble

def main():
    if len(sys.argv) != 2:
        print("Usage: validate_package.py <project-dir>")
        return 2

    logical, errors = assemble(Path(sys.argv[1]))
    if errors:
        print("FAILED")
        for e in errors:
            print("-", e)
        return 1

    print("OK")
    print(f"Project: {logical['project']['id']}")
    print(f"Elements: {len(logical['model']['elements'])}")
    print(f"Relationships: {len(logical['model']['relationships'])}")
    print("Package layout: valid")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
