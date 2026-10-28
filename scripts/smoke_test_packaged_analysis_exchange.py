#!/usr/bin/env python3
"""Exercise query and Model Exchange roundtrip from extracted runtime Skills."""
import json,subprocess,sys,tempfile,zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
targets={"chat":("*-chat-*.zip","assistant/skills/"),"claude_skills":("*-claude-skills-*.zip","skills/"),"opencode":("*-opencode-*.zip",".opencode/skills/"),"plugin":("*-plugin-*.zip","skills/")}
errors=[]
for runtime,(pattern,prefix) in targets.items():
    archives=list((root/"dist").glob(pattern))
    if len(archives)!=1:
        errors.append(runtime+": missing archive");continue
    with tempfile.TemporaryDirectory() as tmp:
        stage=Path(tmp)
        with zipfile.ZipFile(archives[0]) as z:z.extractall(stage)
        def run(skill,script,*args):
            cmd=[sys.executable,str(stage/prefix/skill/"scripts"/script),*map(str,args)]
            result=subprocess.run(cmd,cwd=stage,text=True,capture_output=True)
            if result.returncode:raise ValueError(f"{runtime}/{skill}/{script}: {(result.stdout+result.stderr)[-1200:]}")
            return result.stdout
        try:
            project=stage/"parity"
            run("project-workflow","new_project.py","--id","parity","--name","Parity","--output-dir",stage)
            query=stage/"query.yaml"
            query.write_text("id: Q-PARITY\nfrom: elements\n",encoding="utf-8")
            output=run("architecture-analysis","query.py",project,query,"--json")
            assert "query_result" in json.loads(output)
            xml=stage/"model.xml"
            run("interoperability","export_model_exchange.py",project,"--output",xml)
            assert xml.exists() and "<" in xml.read_text()
            result=json.loads(run("interoperability","import_model_exchange.py",xml,"--preview","--json"))
            assert "import_preview" in result
            print(runtime+": query and exchange roundtrip PASS")
        except Exception as error:
            errors.append(str(error))
print(json.dumps({"result":"fail" if errors else "pass","errors":errors},ensure_ascii=False,indent=2))
sys.exit(bool(errors))
