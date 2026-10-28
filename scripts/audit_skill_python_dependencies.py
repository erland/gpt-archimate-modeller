#!/usr/bin/env python3
"""Audit local Python imports for candidate skill entrypoints.

Read-only, stdlib-only. Emits JSON to stdout and returns nonzero on missing
local imports. Does not claim to discover YAML/schema/runtime data dependencies.
"""
from __future__ import annotations
import argparse
import ast
import json
from pathlib import Path

ENTRYPOINTS = {
    "project-workflow": ["project_control.py", "update_project.py", "new_project.py", "pack_project.py"],
    "archimate-modeling": ["apply_changes.py", "validate.py", "identity.py", "quality_check.py"],
    "architecture-analysis": ["query.py", "impact_analysis.py", "render_report.py", "compile_view.py", "export_diagram.py"],
    "interoperability": ["import_model_exchange.py", "export_model_exchange.py"],
}

def local_imports(path: Path, names: set[str]) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    dependencies = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                if root in names:
                    dependencies.add(root)
        elif isinstance(node, ast.ImportFrom) and node.module:
            root = node.module.split(".")[0]
            if root in names:
                dependencies.add(root)
    return dependencies

def audit(root: Path) -> dict:
    scripts = root / "scripts"
    files = {p.stem: p for p in scripts.glob("*.py")}
    missing = []
    graph = {}
    for name, path in sorted(files.items()):
        try:
            graph[name] = sorted(local_imports(path, set(files)))
        except SyntaxError as exc:
            missing.append(f"invalid syntax {path.name}: {exc}")
    result = {}
    for skill, entrypoints in ENTRYPOINTS.items():
        visited = set()
        stack = [Path(name).stem for name in entrypoints]
        for name in stack:
            if name not in files:
                missing.append(f"{skill}: missing entrypoint {name}")
        while stack:
            name = stack.pop()
            if name in visited or name not in graph:
                continue
            visited.add(name)
            stack.extend(set(graph[name]) - visited)
        result[skill] = {
            "entrypoints": entrypoints,
            "python_import_closure": sorted(f"{name}.py" for name in visited),
        }
    return {
        "schema_version": 1,
        "scope": "static top-level Python import resolution only",
        "skills": result,
        "errors": sorted(set(missing)),
        "limitations": [
            "dynamic import and subprocess calls are not resolved",
            "runtime templates, schemas, YAML, data files and external dependencies are not resolved",
            "no distribution resource_policy is inferred from this output",
        ],
    }

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--output")
    args = parser.parse_args()
    report = audit(Path(args.root).resolve())
    data = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(data, encoding="utf-8")
    else:
        print(data, end="")
    return 1 if report["errors"] else 0

if __name__ == "__main__":
    raise SystemExit(main())
