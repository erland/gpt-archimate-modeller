#!/usr/bin/env python3
from pathlib import Path,PurePosixPath
import argparse,collections,hashlib,stat,zipfile,yaml
ROOT=Path(__file__).resolve().parents[1]
CONTRACT=ROOT/"package"/"project-zip-contract.yaml"; ROBUSTNESS=ROOT/"package"/"zip-robustness.yaml"
def ly(p): return yaml.safe_load(Path(p).read_text(encoding="utf-8")) or {}
def sh(b): return hashlib.sha256(b).hexdigest()
def mode(i): return (i.external_attr>>16)&0xFFFF
def symlink(i): return stat.S_ISLNK(mode(i))
def regular_or_dir(i):
    m=mode(i)
    return m==0 or stat.S_ISREG(m) or stat.S_ISDIR(m)
def name_errors(n,maxlen):
    e=[]; pp=PurePosixPath(n)
    if "\\" in n:e.append(f"Backslash path not allowed: {n}")
    if pp.is_absolute() or n.startswith("/") or (len(n)>1 and n[1]==":"):e.append(f"Absolute path not allowed: {n}")
    if ".." in pp.parts:e.append(f"Parent traversal not allowed: {n}")
    if len(n)>maxlen:e.append(f"Path too long: {n}")
    return e
def validate_zip(path):
    limits=ly(ROBUSTNESS)["validation_limits"]; contract=ly(CONTRACT); errors=[]; warnings=[]; result={"status":"invalid","entries":0,"total_uncompressed_bytes":0}
    try:
        with zipfile.ZipFile(path,"r",allowZip64=True) as z:
            infos=z.infolist(); result["entries"]=len(infos)
            if len(infos)>limits["max_entries"]: errors.append("Too many ZIP entries")
            names=[i.filename for i in infos]
            for n,c in collections.Counter(names).items():
                if c>1: errors.append(f"Duplicate ZIP member: {n}")
            lower=collections.defaultdict(set)
            for n in names: lower[n.lower()].add(n)
            for vals in lower.values():
                if len(vals)>1: errors.append("Case-collision ZIP members: "+", ".join(sorted(vals)))
            total=0
            for i in infos:
                errors+=name_errors(i.filename,limits["max_path_length"])
                if symlink(i): errors.append(f"Symlink not allowed: {i.filename}")
                if not regular_or_dir(i): errors.append(f"Special file not allowed: {i.filename}")
                if i.is_dir(): continue
                total+=i.file_size
                if i.file_size>limits["max_single_file_uncompressed_bytes"]: errors.append(f"File too large: {i.filename}")
                if i.file_size and i.compress_size:
                    ratio=i.file_size/i.compress_size
                    if ratio>limits["max_compression_ratio"]: errors.append(f"Compression ratio too high: {i.filename} ({ratio:.1f})")
                elif i.file_size and i.compress_size==0: errors.append(f"Suspicious zero compressed size: {i.filename}")
            result["total_uncompressed_bytes"]=total
            if total>limits["max_total_uncompressed_bytes"]: errors.append("ZIP uncompressed total too large")
            nset=set(names)
            for f in contract.get("required_files",[]):
                if f not in nset: errors.append(f"Missing required file: {f}")
            for d in contract.get("required_directories",[]):
                prefix=d.rstrip("/")+"/"
                if prefix not in nset and not any(n.startswith(prefix) for n in names): errors.append(f"Missing required directory content: {d}")
            if "PACKAGE-MANIFEST.yaml" not in nset: errors.append("Missing PACKAGE-MANIFEST.yaml")
            else:
                try:
                    m=yaml.safe_load(z.read("PACKAGE-MANIFEST.yaml")) or {}; es=m.get("files",[]); mp=[x.get("path") for x in es]
                    if len(mp)!=len(set(mp)): errors.append("Duplicate manifest path")
                    payload={n for n in names if n!="PACKAGE-MANIFEST.yaml" and not n.endswith("/")}
                    for x in es:
                        p=x.get("path")
                        if p not in nset: errors.append(f"Manifest references missing file: {p}"); continue
                        b=z.read(p)
                        if x.get("sha256")!=sh(b): errors.append(f"Checksum mismatch: {p}")
                        if x.get("size") is not None and x["size"]!=len(b): errors.append(f"Size mismatch: {p}")
                    if set(mp)!=payload:
                        if payload-set(mp): errors.append("Manifest missing payload paths: "+", ".join(sorted(payload-set(mp))[:10]))
                        if set(mp)-payload: errors.append("Manifest has extra paths: "+", ".join(sorted(set(mp)-payload)[:10]))
                except Exception as ex: errors.append(f"Invalid PACKAGE-MANIFEST.yaml: {ex}")
    except zipfile.BadZipFile as ex: errors.append(f"Bad ZIP: {ex}")
    except Exception as ex: errors.append(f"ZIP validation error: {ex}")
    result["status"]="valid" if not errors else "invalid"
    return result,errors,warnings
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("zip_file"); a=ap.parse_args(); r,e,w=validate_zip(a.zip_file)
    print(yaml.safe_dump({"result":r,"errors":e,"warnings":w},sort_keys=False,allow_unicode=True,width=120),end=""); return 0 if not e else 1
if __name__=="__main__": raise SystemExit(main())
