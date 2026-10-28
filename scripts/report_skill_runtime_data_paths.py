#!/usr/bin/env python3
"""Report unresolved root-relative runtime data resources per modular Skill.

A declared resource copied into skill/assets or skill/references is not
automatically available at ROOT/<original path>. This gate deliberately
fails until each requirement has a verified runtime-compatible path.
"""
from __future__ import annotations
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
cfg = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
requirements = {
    "project-workflow": [
        ("scripts/new_project.py", "schemas/new-project.schema.json"),
        ("scripts/new_project.py", "templates/ea-project-split"),
        ("scripts/assemble_project.py", "schemas/ea-package.schema.json"),
        ("scripts/assemble_project.py", "schemas/ea-project.schema.json"),
    ],
    "archimate-modeling": [
        ("scripts/assemble_project.py", "schemas/ea-package.schema.json"),
        ("scripts/assemble_project.py", "schemas/ea-project.schema.json"),
        ("scripts/validate.py", "metamodel/elements.yaml"),
        ("scripts/validate.py", "metamodel/relationships.yaml"),
        ("scripts/validate.py", "metamodel/relationship-matrix.yaml"),
    ],
    "architecture-analysis": [
        ("scripts/assemble_project.py", "schemas/ea-package.schema.json"),
        ("scripts/assemble_project.py", "schemas/ea-project.schema.json"),
    ],
    "interoperability": [
        ("scripts/assemble_project.py", "schemas/ea-package.schema.json"),
        ("scripts/assemble_project.py", "schemas/ea-project.schema.json"),
    ],
}
report = []
for skill in cfg["skills"]["definitions"]:
    name = skill["id"]
    for consumer, resource in requirements.get(name, []):
        source = ROOT / resource
        # The engine copies references and assets into separate subdirectories.
        # That layout does not match scripts resolving ROOT/<resource>.
        report.append({
            "skill": name, "consumer": consumer, "resource": resource,
            "source_exists": source.exists(),
            "runtime_root_path_verified": False,
            "reason": "Engine asset/reference layout differs from script ROOT-relative lookup; runtime smoke required",
        })
print(json.dumps({"status": "requires_runtime_mapping", "requirements": report,
                  "count": len(report), "unverified": len(report)}, ensure_ascii=False, indent=2))
