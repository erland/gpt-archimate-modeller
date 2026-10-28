#!/usr/bin/env python3
"""Check packaged Skill scripts for the five GPT Byggaren 1.6.33 distributions."""
import io
import json
import sys
import zipfile
from pathlib import Path

import yaml

root = Path(__file__).resolve().parents[1]
cfg = yaml.safe_load((root / "gpt-project.yaml").read_text(encoding="utf-8"))
dist = root / "dist"
expected = {s["id"]: [Path(p).name for p in s.get("scripts", [])] for s in cfg["skills"]["definitions"]}
patterns = {
    "chat": ("*-chat-*.zip", "assistant/skills/"),
    "claude_skills": ("*-claude-skills-*.zip", "skills/"),
    "opencode": ("*-opencode-*.zip", ".opencode/skills/"),
    "plugin": ("*-plugin-*.zip", "skills/"),
}
errors = []
for runtime, (pattern, prefix) in patterns.items():
    archives = sorted(dist.glob(pattern))
    if len(archives) != 1:
        errors.append(f"{runtime}: expected one archive, found {len(archives)}")
        continue
    with zipfile.ZipFile(archives[0]) as archive:
        names = set(archive.namelist())
        for skill_id, scripts in expected.items():
            if prefix + skill_id + "/SKILL.md" not in names:
                errors.append(f"{runtime}/{skill_id}: missing SKILL.md")
            for script in scripts:
                if prefix + skill_id + "/scripts/" + script not in names:
                    errors.append(f"{runtime}/{skill_id}: missing script {script}")
# Claude Project is a text-first package: inspect instructions, not installed host Skills.
claude = sorted(dist.glob("*-claude-project-*.zip"))
if len(claude) != 1:
    errors.append(f"claude_project: expected one archive, found {len(claude)}")
else:
    with zipfile.ZipFile(claude[0]) as archive:
        if "project/instructions.md" not in archive.namelist():
            errors.append("claude_project: missing instructions")
report = {"status": "fail" if errors else "pass", "skills": expected, "archives_checked": 5, "errors": errors}
print(json.dumps(report, ensure_ascii=False, indent=2))
sys.exit(bool(errors))
