#!/usr/bin/env python3
from pathlib import Path, PurePosixPath
import argparse, shutil, stat, tempfile, zipfile, yaml

def unsafe_name(name):
    p=PurePosixPath(name)
    return p.is_absolute() or ".." in p.parts or name.startswith("/")

def is_symlink(info):
    mode=(info.external_attr >> 16) & 0xFFFF
    return stat.S_ISLNK(mode)

def safe_extract(zip_file, destination):
    zip_file=Path(zip_file)
    destination=Path(destination)
    destination.mkdir(parents=True,exist_ok=True)
    dest_resolved=destination.resolve()

    with zipfile.ZipFile(zip_file,"r") as z:
        for info in z.infolist():
            name=info.filename
            if unsafe_name(name):
                raise ValueError(f"Unsafe ZIP path: {name}")
            if is_symlink(info):
                raise ValueError(f"Symlink ZIP member not allowed: {name}")

            rel=PurePosixPath(name)
            target=(destination/Path(*rel.parts)).resolve()
            try:
                target.relative_to(dest_resolved)
            except ValueError:
                raise ValueError(f"ZIP member escapes destination: {name}")

            if info.is_dir():
                target.mkdir(parents=True,exist_ok=True)
            else:
                target.parent.mkdir(parents=True,exist_ok=True)
                with z.open(info,"r") as src, target.open("wb") as dst:
                    shutil.copyfileobj(src,dst)

    if (destination/"project.yaml").is_file():
        return destination
    roots=[p for p in destination.iterdir() if p.name not in ("__MACOSX",)]
    roots=[p for p in roots if p.is_dir()]
    candidates=[p for p in roots if (p/"project.yaml").is_file()]
    if len(candidates)!=1:
        raise ValueError(f"Expected flat project root or exactly one project directory, found {len(candidates)}")
    return candidates[0]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("zip_file")
    ap.add_argument("output_dir")
    a=ap.parse_args()
    try:
        root=safe_extract(a.zip_file,a.output_dir)
        print(f"OK: {root}")
        return 0
    except Exception as e:
        print("FAILED")
        print("-",e)
        return 1

if __name__=="__main__":
    raise SystemExit(main())
