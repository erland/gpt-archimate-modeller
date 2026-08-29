#!/usr/bin/env python3
from pathlib import Path
import argparse,shutil,yaml
ROOT=Path(__file__).resolve().parents[1]; TEMPLATE=ROOT/"templates"/"ea-project-split"
def wy(p,d): Path(p).write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True,width=120),encoding="utf-8")
def generate(out,elements=2000,relationships=1999):
    out=Path(out)
    if out.exists(): shutil.rmtree(out)
    shutil.copytree(TEMPLATE,out)
    p=yaml.safe_load((out/"project.yaml").read_text()); p["project"]["id"]="large-synthetic"; p["project"]["name"]="Large Synthetic Fixture"; wy(out/"project.yaml",p)
    wy(out/"model"/"elements"/"application.yaml",{"elements":[{"id":f"APP-{i:06d}","type":"ApplicationComponent","name":f"Synthetic Application {i:06d}"} for i in range(1,elements+1)]})
    n=min(relationships,max(0,elements-1))
    wy(out/"model"/"relationships.yaml",{"relationships":[{"id":f"REL-{i:06d}","type":"Association","source":f"APP-{i:06d}","target":f"APP-{i+1:06d}"} for i in range(1,n+1)]})
    c=yaml.safe_load((out/"identity"/"id-counters.yaml").read_text())["counters"]; c["APP"]=elements; c["REL"]=n; wy(out/"identity"/"id-counters.yaml",{"counters":c})
    return out
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("output_dir"); ap.add_argument("--elements",type=int,default=2000); ap.add_argument("--relationships",type=int,default=1999); a=ap.parse_args(); generate(a.output_dir,a.elements,a.relationships); print(a.output_dir)
if __name__=="__main__": raise SystemExit(main())
