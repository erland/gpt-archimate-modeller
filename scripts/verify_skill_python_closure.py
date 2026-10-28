#!/usr/bin/env python3
"""Fail when a Skill omits statically discoverable local Python imports."""
from __future__ import annotations
import ast
import json
from pathlib import Path
import yaml

root = Path(__file__).resolve().parents[1]
files = {p.stem: p for p in (root / "scripts").glob("*.py")}
cfg = yaml.safe_load((root / "gpt-project.yaml").read_text(encoding="utf-8"))
graph = {}
for name, path in files.items():
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    graph[name] = imports & files.keys()
errors = []
results = {}
for skill in cfg["skills"]["definitions"]:
    entries = {Path(p).stem for p in skill["scripts"]}
    visited, pending = set(), list(entries)
    while pending:
        name = pending.pop()
        if name in visited:
            continue
        visited.add(name)
        pending.extend(graph.get(name, set()) - visited)
    missing = sorted(visited - entries)
    results[skill["id"]] = {"declared": len(entries), "closure": len(visited), "missing": missing}
    errors.extend(f"{skill['id']}: scripts/{name}.py" for name in missing)
print(json.dumps({"result": "fail" if errors else "pass", "skills": results, "errors": errors,
    "limitations": "Static Python imports only; dynamic imports, subprocesses, external packages and data resources are not covered."}, indent=2))
raise SystemExit(bool(errors))
