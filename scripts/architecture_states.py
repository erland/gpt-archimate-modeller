#!/usr/bin/env python3
from pathlib import Path
import argparse,json,yaml
ROOT=Path(__file__).resolve().parents[1]; SCHEMA=ROOT/"schemas"/"architecture-states.schema.json"
def rd(p): return yaml.safe_load(Path(p).read_text(encoding="utf-8")) or {}
def pids(root):
 root=Path(root); e=set()
 for p in (root/"model"/"elements").glob("*.yaml"): e|={x.get("id") for x in rd(p).get("elements",[])}
 return e,{x.get("id") for x in rd(root/"model"/"relationships.yaml").get("relationships",[])}
def resolve_state(root,sid,path=None):
 root=Path(root); p=Path(path) if path else root/"architecture"/"states.yaml"; d=rd(p); by={s["id"]:s for s in d.get("states",[])}
 if sid not in by: raise ValueError(f"State not found: {sid}")
 def rec(x,stack):
  if x in stack: raise ValueError("State inheritance cycle")
  s=by[x]; e=set(); r=set()
  if s.get("inherits_from"):
   q=rec(s["inherits_from"],stack+[x]); e=set(q["elements"]); r=set(q["relationships"])
  inc=s.get("include") or {}; e|=set(inc.get("elements",[]) or []); r|=set(inc.get("relationships",[]) or [])
  de=s.get("delta") or {}; e|=set(de.get("add_elements",[]) or []); e-=set(de.get("remove_elements",[]) or []); r|=set(de.get("add_relationships",[]) or []); r-=set(de.get("remove_relationships",[]) or [])
  return {"elements":sorted(e),"relationships":sorted(r)}
 return rec(sid,[])
def validate_states(root,path=None):
 root=Path(root); p=Path(path) if path else root/"architecture"/"states.yaml"; d=rd(p); errors=[]
 schema=json.loads(SCHEMA.read_text())
 try:
  import jsonschema; errors += [e.message for e in jsonschema.Draft202012Validator(schema).iter_errors(d)]
 except ImportError: pass
 ss=d.get("states",[]); ts=d.get("transitions",[]); by={s.get("id"):s for s in ss if s.get("id")}; sids=[s.get("id") for s in ss]; tids=[t.get("id") for t in ts]
 if len(sids)!=len(set(sids)): errors.append("Duplicate architecture state ID")
 if len(tids)!=len(set(tids)): errors.append("Duplicate transition ID")
 for s in ss:
  if s.get("inherits_from") and s["inherits_from"] not in by: errors.append(f"{s.get('id')}: unknown inherits_from {s['inherits_from']}")
 for sid in by:
  seen=set(); cur=sid
  while cur:
   if cur in seen: errors.append(f"{sid}: state inheritance cycle"); break
   seen.add(cur); cur=by.get(cur,{}).get("inherits_from")
 eis,ris=pids(root)
 for s in ss:
  inc=s.get("include") or {}; de=s.get("delta") or {}
  for x in inc.get("elements",[]) or []:
   if x not in eis: errors.append(f"{s.get('id')}: unknown element {x}")
  for x in inc.get("relationships",[]) or []:
   if x not in ris: errors.append(f"{s.get('id')}: unknown relationship {x}")
  ae=set(de.get("add_elements",[]) or []); re=set(de.get("remove_elements",[]) or []); ar=set(de.get("add_relationships",[]) or []); rr=set(de.get("remove_relationships",[]) or [])
  if ae&re: errors.append(f"{s.get('id')}: same element both added and removed")
  if ar&rr: errors.append(f"{s.get('id')}: same relationship both added and removed")
  for x in ae|re:
   if x not in eis: errors.append(f"{s.get('id')}: unknown delta element {x}")
  for x in ar|rr:
   if x not in ris: errors.append(f"{s.get('id')}: unknown delta relationship {x}")
 for tr in ts:
  if tr.get("from_state") not in by: errors.append(f"{tr.get('id')}: unknown from_state {tr.get('from_state')}")
  if tr.get("to_state") not in by: errors.append(f"{tr.get('id')}: unknown to_state {tr.get('to_state')}")
 for s in ss:
  if s.get("object_status"):
   try: mem=resolve_state(root,s["id"],p)
   except Exception: continue
   allowed=set(mem["elements"])|set(mem["relationships"])
   for oid in s["object_status"]:
    if oid not in allowed: errors.append(f"{s.get('id')}: object_status for object not in state {oid}")
 return errors
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("project_dir"); g=ap.add_mutually_exclusive_group(required=True); g.add_argument("--validate",action="store_true"); g.add_argument("--resolve"); ap.add_argument("--json",action="store_true"); a=ap.parse_args()
 try:
  if a.validate:
   e=validate_states(a.project_dir)
   if e: print("FAILED"); [print("-",x) for x in e]; return 1
   out={"status":"valid"}
  else: out={"state_id":a.resolve,"membership":resolve_state(a.project_dir,a.resolve)}
  print(json.dumps(out,indent=2,ensure_ascii=False) if a.json else yaml.safe_dump(out,sort_keys=False,allow_unicode=True),end="" if not a.json else "\n"); return 0
 except Exception as e: print("FAILED"); print("-",str(e)); return 1
if __name__=="__main__": raise SystemExit(main())
