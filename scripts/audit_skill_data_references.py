#!/usr/bin/env python3
"""Read-only audit of literal repository data references in Skill entrypoints.

Intentionally conservative: dynamic paths are reported as limitations, not
inferred as complete dependencies.
"""
import argparse
import ast
import json
from pathlib import Path

ROOTS = ("schemas", "metamodel", "knowledge", "templates", "package", "queries", "reports", "views", "extensions", "specializations")
SCRIPT = "scripts/audit_skill_python_dependencies.py"

def inspect(root):
    scripts = root / "scripts"
    findings = []
    for path in sorted(scripts.glob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError as exc:
            findings.append({"script": path.name, "kind": "syntax_error", "value": str(exc)})
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                value = node.value.replace("\\", "/")
                if any(value.startswith(prefix + "/") for prefix in ROOTS):
                    candidate = root / value
                    findings.append({"script": path.name, "kind": "literal_path", "value": value, "exists": candidate.exists()})
    return {
        "schema_version": 1,
        "scope": "literal path candidates only; not a complete file dependency graph",
        "findings": findings,
        "limitations": [
            "Paths assembled from variables, ROOT joins, glob patterns and YAML are not resolved",
            "A missing literal may be an output path rather than a required input",
            "Manual mapping and runtime build validation remain mandatory"
        ]
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--output")
    args = ap.parse_args()
    result = inspect(Path(args.root).resolve())
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
