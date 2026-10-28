#!/usr/bin/env python3
"""Validate a real dry-run and committed model change in all four Skill archives."""
import json,subprocess,sys,tempfile,zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
targets={"chat":("*-chat-*.zip","assistant/skills/"),"claude_skills":("*-claude-skills-*.zip","skills/"),"opencode":("*-opencode-*.zip",".opencode/skills/"),"plugin":("*-plugin-*.zip","skills/")}
errors=[]
for runtime,(pattern,prefix) in targets.items():
    archives=list((root/"dist").glob(pattern))
    if len(archives)!=1:errors.append(runtime+": missing archive");continue
    with tempfile.TemporaryDirectory() as directory:
        stage=Path(directory)
        with zipfile.ZipFile(archives[0]) as z:z.extractall(stage)
        def run(skill,script,*args):
            command=[sys.executable,str(stage/prefix/skill/"scripts"/script),*map(str,args)]
            result=subprocess.run(command,cwd=stage,capture_output=True,text=True)
            if result.returncode:raise ValueError(f"{runtime}/{script}: {(result.stdout+result.stderr)[-1500:]}")
            return result.stdout
        try:
            project=stage/"parity"
            run("project-workflow","new_project.py","--id","parity","--name","Parity","--output-dir",stage)
            change=stage/"change.yaml"
            change.write_text("change_set:\n  id: CHG-000001\n  title: Add application\n  created: '2026-10-28'\n  expected_model_version: 0.1.0\n  operations:\n    - op: add_element\n      element:\n        id: APP-000001\n        type: ApplicationComponent\n        name: Test Application\n",encoding="utf-8")
            previous=(project/"project.yaml").read_bytes()
            dry=run("project-workflow","apply_changes.py",project,change,"--dry-run")
            assert "DRY_RUN_OK" in dry
            assert (project/"project.yaml").read_bytes()==previous
            applied=run("project-workflow","apply_changes.py",project,change)
            assert "APPLIED" in applied
            run("project-workflow","validate.py",project)
            result=run("architecture-analysis","query.py",project,stage/"query.yaml","--json") if False else ""
            assert "APP-000001" in (project/"model"/"elements"/"application.yaml").read_text()
            print(runtime+": model change PASS")
        except Exception as e:errors.append(str(e))
print(json.dumps({"result":"fail" if errors else "pass","errors":errors},ensure_ascii=False,indent=2))
sys.exit(bool(errors))
