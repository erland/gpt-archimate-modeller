#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,yaml
def read_yaml(p): return yaml.safe_load(Path(p).read_text(encoding="utf-8"))
def sha256(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()
def role_for(rel):
    s=rel.as_posix()
    if s.startswith("exports/"): return "generated"
    if s=="README.md": return "documentation"
    if s=="project.yaml" or s=="CHANGELOG.md" or s.startswith(
        ("model/","sources/","extensions/","issues/","identity/","changes/","versioning/","queries/","reports/","views/")
    ): return "canonical"
    return "documentation"
def build_manifest(root):
    root=Path(root); p=read_yaml(root/"project.yaml")
    files=[]
    for f in sorted(root.rglob("*")):
        if not f.is_file(): continue
        rel=f.relative_to(root)
        if rel.as_posix() in ("PACKAGE-MANIFEST.yaml",".project-control.yaml"): continue
        if rel.name in (".DS_Store","Thumbs.db") or "__MACOSX" in rel.parts: continue
        files.append({"path":rel.as_posix(),"sha256":sha256(f),"role":role_for(rel)})
    return {"package_manifest":{
        "contract_version":"0.1",
        "project_id":p["project"]["id"],
        "model_version":p["project"]["model_version"],
        "format_version":p["format_version"],
        "package_layout_version":p["package_layout_version"],
        "archimate_version":p["project"].get("archimate_version"),
        "hash_algorithm":"sha256",
        "files":files
    }}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("project_dir"); ap.add_argument("--output"); a=ap.parse_args()
    root=Path(a.project_dir); out=Path(a.output) if a.output else root/"PACKAGE-MANIFEST.yaml"
    out.write_text(yaml.safe_dump(build_manifest(root),sort_keys=False,allow_unicode=True,width=120),encoding="utf-8")
    print(f"OK: {out}"); return 0
if __name__=="__main__": raise SystemExit(main())
