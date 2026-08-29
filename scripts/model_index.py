#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,yaml,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from assemble_project import assemble

INDEX_NAME="MODEL-INDEX.json"
INDEX_VERSION="0.1"
EXCLUDED={INDEX_NAME,"PACKAGE-MANIFEST.yaml"}

def source_files(root):
    root=Path(root)
    out=[]
    for p in root.rglob("*"):
        if not p.is_file() or p.is_symlink():
            continue
        rel=p.relative_to(root).as_posix()
        if rel in EXCLUDED: continue
        # Canonical/project-semantic source only; generated exports/examples are not part of an EA project root.
        if p.suffix.lower() not in (".yaml",".yml",".json"):
            continue
        out.append((rel,p))
    return sorted(out)

def source_fingerprint(root):
    h=hashlib.sha256(); count=0
    for rel,p in source_files(root):
        count+=1
        h.update(rel.encode("utf-8")); h.update(b"\0")
        with p.open("rb") as f:
            for chunk in iter(lambda:f.read(1024*1024),b""):
                h.update(chunk)
        h.update(b"\0")
    return h.hexdigest(),count

def build_index(root):
    root=Path(root)
    logical,errors=assemble(root)
    if errors: raise ValueError("Project invalid: "+"; ".join(errors))
    fp,count=source_fingerprint(root)
    return {"model_index":{"version":INDEX_VERSION,"source_fingerprint":fp,"source_file_count":count,"logical":logical}}

def write_index(root,path=None):
    root=Path(root); path=Path(path) if path else root/INDEX_NAME
    data=build_index(root)
    path.write_text(json.dumps(data,ensure_ascii=False,separators=(",",":"),sort_keys=True),encoding="utf-8")
    return path,data

def load_valid_index(root,path=None):
    root=Path(root); path=Path(path) if path else root/INDEX_NAME
    if not path.exists(): return None,"missing"
    try:
        data=json.loads(path.read_text(encoding="utf-8"))
        idx=data["model_index"]
        if idx.get("version")!=INDEX_VERSION: return None,"version_mismatch"
        fp,count=source_fingerprint(root)
        if idx.get("source_fingerprint")!=fp: return None,"stale"
        if idx.get("source_file_count")!=count: return None,"stale"
        return idx["logical"],"valid"
    except Exception:
        return None,"invalid"

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("project_dir"); ap.add_argument("--output"); ap.add_argument("--check",action="store_true"); a=ap.parse_args()
    if a.check:
        logical,status=load_valid_index(a.project_dir,a.output)
        print(yaml.safe_dump({"status":status,"usable":logical is not None},sort_keys=False),end="")
        return 0 if logical is not None else 1
    p,data=write_index(a.project_dir,a.output)
    print(yaml.safe_dump({"status":"built","path":str(p),"source_file_count":data["model_index"]["source_file_count"]},sort_keys=False),end="")
    return 0
if __name__=="__main__": raise SystemExit(main())
