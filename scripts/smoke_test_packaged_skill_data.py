#!/usr/bin/env python3
"""Smoke-test root-relative data paths from actual generated runtime Skills."""
from __future__ import annotations
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVES = {
    "chat": ("*-chat-*.zip", "assistant/skills"),
    "claude_skills": ("*-claude-skills-*.zip", "skills"),
    "opencode": ("*-opencode-*.zip", ".opencode/skills"),
    "plugin": ("*-plugin-*.zip", "skills"),
}
checks = {
    "project-workflow": ["new_project", "assemble_project", "validate"],
    "archimate-modeling": ["assemble_project", "validate"],
    "architecture-analysis": ["assemble_project"],
    "interoperability": ["assemble_project"],
}
errors = []
results = []
with tempfile.TemporaryDirectory(prefix="archimate-skill-smoke-") as temporary:
    for runtime, (pattern, prefix) in ARCHIVES.items():
        archives = sorted((ROOT / "dist").glob(pattern))
        if len(archives) != 1:
            errors.append(f"{runtime}: expected one archive, found {len(archives)}")
            continue
        destination = Path(temporary) / runtime
        destination.mkdir()
        with zipfile.ZipFile(archives[0]) as archive:
            archive.extractall(destination)
        for skill, modules in checks.items():
            skill_root = destination / prefix / skill
            script_dir = skill_root / "scripts"
            python = """
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1])))
import new_project, assemble_project, validate
assets=Path(sys.argv[1]).parent / 'assets'
expected=['ea-project.schema.json','ea-package.schema.json','elements.yaml','relationships.yaml','relationship-matrix.yaml']
for filename in expected:
    assert (assets / filename).is_file(), f'missing bundled asset: {filename}'
assert assemble_project.PACKAGE_SCHEMA.is_file()
assert assemble_project.LOGICAL_SCHEMA.is_file()
assert validate.resource_yaml('elements.yaml').is_file()
assert validate.resource_yaml('relationships.yaml').is_file()
assert validate.resource_yaml('relationship-matrix.yaml').is_file()
if sys.argv[2]=='project-workflow':
    assert new_project.SCHEMA.is_file()
"""
            # Import only modules explicitly declared in the current Skill.
            python = python.replace("import new_project, assemble_project, validate", "import " + ", ".join(modules))
            if skill != "project-workflow":
                python = python.replace("if sys.argv[2]=='project-workflow':\n    assert new_project.SCHEMA.is_file()\n", "")
            result = subprocess.run([sys.executable, "-c", python, str(script_dir), skill],
                                    text=True, capture_output=True, cwd=skill_root)
            results.append({"runtime": runtime, "skill": skill, "passed": result.returncode == 0})
            if result.returncode:
                errors.append(f"{runtime}/{skill}: {result.stderr.strip()[-1200:]}")
print(json.dumps({"result": "fail" if errors else "pass", "checks": results, "errors": errors,
    "scope": "Python module import and flattened schema/metamodel asset resolution, not full functional parity"},
    ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
