#!/usr/bin/env python3
"""Run real create -> validate -> pack -> zip validation from extracted Skills."""
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

root=Path(__file__).resolve().parents[1]
targets={"chat":("*-chat-*.zip","assistant/skills/project-workflow"),
         "claude_skills":("*-claude-skills-*.zip","skills/project-workflow"),
         "opencode":("*-opencode-*.zip",".opencode/skills/project-workflow"),
         "plugin":("*-plugin-*.zip","skills/project-workflow")}
errors=[]
for target,(glob,skill_path) in targets.items():
    archives=list((root/"dist").glob(glob))
    if len(archives)!=1:
        errors.append(f"{target}: expected exactly one archive")
        continue
    with tempfile.TemporaryDirectory(prefix="ea-migration-e2e-") as temp:
        stage=Path(temp)
        with zipfile.ZipFile(archives[0]) as z:
            z.extractall(stage)
        scripts=stage/skill_path/"scripts"
        archive=stage/"created.zip"
        cmd=[sys.executable,str(scripts/"new_project.py"),"--id","runtime-smoke",
             "--name","Runtime Smoke","--output-zip",str(archive),"--json"]
        run=subprocess.run(cmd,cwd=stage,capture_output=True,text=True)
        if run.returncode:
            errors.append(f"{target}: new_project failed: {(run.stdout+run.stderr)[-1200:]}")
            continue
        if not archive.is_file():
            errors.append(f"{target}: ZIP not created")
            continue
        check=subprocess.run([sys.executable,str(scripts/"validate_project_zip.py"),str(archive)],
                             cwd=stage,capture_output=True,text=True)
        if check.returncode:
            errors.append(f"{target}: ZIP validation failed: {(check.stdout+check.stderr)[-1200:]}")
        print(f"{target}: create+validate+pack {'PASS' if check.returncode==0 else 'FAIL'}")
print(json.dumps({"result":"fail" if errors else "pass","errors":errors},ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
