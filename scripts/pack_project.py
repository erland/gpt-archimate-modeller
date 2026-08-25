#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,zipfile,yaml
from model_index import build_index, INDEX_NAME
ROOT=Path(__file__).resolve().parents[1]
ROBUSTNESS=ROOT/"package"/"zip-robustness.yaml"
CONTRACT=ROOT/"package"/"project-zip-contract.yaml"
FIXED_DT=(1980,1,1,0,0,0)
def ly(p): return yaml.safe_load(Path(p).read_text(encoding="utf-8")) or {}
def sha256(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()
def files(root):
    root=Path(root); out=[]
    for p in root.rglob("*"):
        if p.is_symlink(): raise ValueError(f"Symlink not allowed: {p.relative_to(root)}")
        if p.is_file() and p.name not in ("PACKAGE-MANIFEST.yaml",INDEX_NAME):
            out.append((p.relative_to(root).as_posix(),p))
    return sorted(out)
def required_dirs():
    return sorted(d.rstrip("/")+"/" for d in ly(CONTRACT).get("required_directories",[]))
def manifest(root,index_bytes):
    entries=[{"path":r,"sha256":sha256(p),"size":p.stat().st_size} for r,p in files(root)]
    entries.append({"path":INDEX_NAME,"sha256":hashlib.sha256(index_bytes).hexdigest(),"size":len(index_bytes)})
    return {"package_manifest_version":"0.2","files":entries}
def zi(name,is_dir=False):
    z=zipfile.ZipInfo(name,FIXED_DT); z.compress_type=zipfile.ZIP_STORED if is_dir else zipfile.ZIP_DEFLATED; z.create_system=3
    mode=0o40755 if is_dir else 0o100644
    z.external_attr=(mode&0xFFFF)<<16
    if is_dir: z.external_attr|=0x10
    return z
def pack(project_root,output_zip):
    root=Path(project_root); out=Path(output_zip)
    limits=ly(ROBUSTNESS)["validation_limits"]; fs=files(root); dirs=required_dirs()
    if len(fs)+len(dirs)+1>limits["max_entries"]: raise ValueError("Project exceeds max_entries")
    total=0
    for rel,p in fs:
        s=p.stat().st_size; total+=s
        if s>limits["max_single_file_uncompressed_bytes"]: raise ValueError(f"File exceeds max_single_file_uncompressed_bytes: {rel}")
        if len(rel)>limits["max_path_length"]: raise ValueError(f"Path exceeds max_path_length: {rel}")
    if total>limits["max_total_uncompressed_bytes"]: raise ValueError("Project exceeds max_total_uncompressed_bytes")
    index_bytes=json.dumps(build_index(root),ensure_ascii=False,separators=(",",":"),sort_keys=True).encode("utf-8")
    mb=yaml.safe_dump(manifest(root,index_bytes),sort_keys=False,allow_unicode=True,width=120).encode()
    tmp=out.with_suffix(out.suffix+".tmp"); out.parent.mkdir(parents=True,exist_ok=True)
    if tmp.exists(): tmp.unlink()
    try:
        with zipfile.ZipFile(tmp,"w",allowZip64=True,compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for d in dirs: z.writestr(zi(d,True),b"")
            for rel,p in fs: z.writestr(zi(rel),p.read_bytes())
            z.writestr(zi(INDEX_NAME),index_bytes)
            z.writestr(zi("PACKAGE-MANIFEST.yaml"),mb)
        tmp.replace(out)
    finally:
        if tmp.exists(): tmp.unlink()
    return {"status":"packed","files":len(fs)+2,"directories":len(dirs),"output":str(out)}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("project_dir"); ap.add_argument("output_zip"); a=ap.parse_args()
    try: print(yaml.safe_dump(pack(a.project_dir,a.output_zip),sort_keys=False),end=""); return 0
    except Exception as e: print("FAILED"); print("-",e); return 1
if __name__=="__main__": raise SystemExit(main())
