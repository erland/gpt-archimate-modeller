#!/usr/bin/env python3
"""Install actionable fallback guidance in the SKILL.md files the plugin actually loads."""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def patch(archive, version, project_id):
    url = (f"https://github.com/erland/gpt-archimate-modeller/releases/download/v{version}/"
           f"{project_id}-engine-{version}.zip")
    fallback = f"""

## Obligatoriskt Engine-fallback vid blockerad skriptexekvering

Om ett begärt arbete kräver ett av de medföljande originalskripten och det inte går att
anropa skriptet i denna värdmiljö, **stanna innan resultatet påstås vara validerat**.
Skapa inte en handskriven ersättning och redovisa den som resultat från originalskriptet.

1. Förklara konkret att den installerade Skillens skript inte går att köra här.
2. Ge användaren en **klickbar länk** till versionsmatchad ArchiMate Engine ZIP:
   [Hämta ArchiMate Engine {version}]({url})
3. Be användaren hämta och bifoga denna ZIP i konversationen så att du kan försöka
   köra originalmotorn i en kompatibel Pythonmiljö.
4. Innan länken beskrivs som fungerande: verifiera att GitHub-releasen och filen
   är publicerade. Om det inte går, säg det och länka till
   https://github.com/erland/gpt-archimate-modeller/releases .
5. När ZIP-filen finns: packa upp säkert, installera beroenden om möjligt,
   kör `python archimate_engine.py selftest`, och kör sedan de relevanta
   operationerna. Om Pythonexekvering fortfarande saknas, rapportera blockeraren.

Detta gäller **även om** enklare manuella YAML-/XML-kontroller har passerat.
Ett test där originalskripten inte körts får endast redovisas som PARTIAL eller FAIL,
aldrig som fullständig funktionell acceptans.
"""
    with zipfile.ZipFile(archive) as z:
        data = {n:z.read(n) for n in z.namelist()}
    paths = sorted(n for n in data if n.startswith("skills/") and n.endswith("/SKILL.md"))
    if len(paths) != 4:
        raise SystemExit(f"Expected 4 plugin SKILL.md files, got {len(paths)}")
    for name in paths:
        original = data[name].decode("utf-8")
        if "## Obligatoriskt Engine-fallback" not in original:
            data[name] = (original.rstrip() + "\n" + fallback).encode("utf-8")
    manifest = json.loads(data["MANIFEST.json"])
    manifest["files"] = [{"path":name,"sha256":hashlib.sha256(payload).hexdigest(),"size":len(payload)}
                         for name,payload in sorted(data.items()) if name!="MANIFEST.json"]
    data["MANIFEST.json"] = (json.dumps(manifest,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    temp = archive.with_suffix(".zip.tmp")
    with zipfile.ZipFile(temp,"w",zipfile.ZIP_DEFLATED) as z:
        for name,payload in sorted(data.items()):
            z.writestr(name,payload)
    temp.replace(archive)
    # Verify that the actual packaged Skill instructions contain the link.
    with zipfile.ZipFile(archive) as z:
        for name in paths:
            assert url in z.read(name).decode("utf-8"), name
    print(f"PASS: all {len(paths)} installed plugin Skills include Engine fallback for {version}")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--version",required=True)
    p.add_argument("--dist",default="dist")
    args=p.parse_args()
    cfg=yaml.safe_load((ROOT/"gpt-project.yaml").read_text(encoding="utf-8"))
    project_id=cfg["project"]["id"]
    patch(Path(args.dist)/f"{project_id}-plugin-{args.version}.zip",args.version,project_id)
