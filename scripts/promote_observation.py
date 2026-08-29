#!/usr/bin/env python3
from pathlib import Path
import argparse,yaml
def rd(p): return yaml.safe_load(Path(p).read_text(encoding="utf-8")) or {}
def wr(p,d): Path(p).write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True,width=120),encoding="utf-8")
def promote(path,obs_id,issue_id,issue_type="open_question",priority="medium"):
    d=rd(path); o=next((x for x in d.get("observations",[]) if x.get("id")==obs_id),None)
    if not o: raise ValueError(f"Observation not found: {obs_id}")
    if o.get("status")=="promoted": raise ValueError(f"Observation already promoted: {obs_id}")
    if any(x.get("id")==issue_id for x in d.get("issues",[])): raise ValueError(f"Issue ID already exists: {issue_id}")
    i={"id":issue_id,"type":issue_type,"status":"open","priority":priority,"description":o["description"]}
    for k in ["object_refs","source_refs","reference_refs"]:
        if o.get(k): i[k]=o[k]
    d.setdefault("issues",[]).append(i); o["status"]="promoted"; o["promoted_to_issue"]=issue_id; wr(path,d); return i
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("issues_file"); ap.add_argument("observation_id"); ap.add_argument("issue_id")
    ap.add_argument("--issue-type",default="open_question"); ap.add_argument("--priority",default="medium"); a=ap.parse_args()
    try: i=promote(a.issues_file,a.observation_id,a.issue_id,a.issue_type,a.priority); print("OK"); print(f"Created: {i['id']}"); return 0
    except Exception as e: print("FAILED"); print("-",str(e)); return 1
if __name__=="__main__": raise SystemExit(main())
