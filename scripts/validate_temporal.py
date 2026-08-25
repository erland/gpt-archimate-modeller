#!/usr/bin/env python3
from pathlib import Path
import argparse,datetime as dt,json,yaml

def rd(p): return yaml.safe_load(Path(p).read_text(encoding="utf-8")) or {}
def pd(v,label,errors):
    if v is None: return None
    try: return dt.date.fromisoformat(str(v))
    except Exception: errors.append(f"{label}: invalid date {v}"); return None

def objects(root):
    root=Path(root)
    for p in (root/"model"/"elements").glob("*.yaml"):
        for x in rd(p).get("elements",[]) or []: yield x
    for x in rd(root/"model"/"relationships.yaml").get("relationships",[]) or []: yield x

def validate_temporal(root):
    root=Path(root); errors=[]; warnings=[]
    for obj in objects(root):
        oid=obj.get("id","?"); tm=obj.get("temporal") or {}
        vf=pd(tm.get("valid_from"),f"{oid}.valid_from",errors)
        vt=pd(tm.get("valid_to"),f"{oid}.valid_to",errors)
        pf=pd(tm.get("planned_from"),f"{oid}.planned_from",errors)
        pt=pd(tm.get("planned_to"),f"{oid}.planned_to",errors)
        ro=pd(tm.get("retired_on"),f"{oid}.retired_on",errors)
        if vf and vt and vf>vt: errors.append(f"{oid}: valid_from is after valid_to")
        if pf and pt and pf>pt: errors.append(f"{oid}: planned_from is after planned_to")
        if vf and ro and ro<vf: errors.append(f"{oid}: retired_on is before valid_from")
        lc=(obj.get("properties") or {}).get("lifecycle")
        src=tm.get("status_source")
        if lc=="active" and ro: warnings.append(f"{oid}: lifecycle active conflicts with retired_on")
        if lc=="retired" and src=="actual" and not (ro or vt):
            warnings.append(f"{oid}: actual retired lifecycle lacks retired_on/valid_to")
        if lc=="phase_out" and ro and src=="actual":
            warnings.append(f"{oid}: phase_out with actual retired_on may need lifecycle retired")
    sp=root/"architecture"/"states.yaml"
    if sp.exists():
        d=rd(sp)
        for s in d.get("states",[]) or []:
            sid=s.get("id","?")
            ef=pd(s.get("effective_from"),f"{sid}.effective_from",errors)
            et=pd(s.get("effective_to"),f"{sid}.effective_to",errors)
            if ef and et and ef>et: errors.append(f"{sid}: effective_from is after effective_to")
            if s.get("type")=="baseline" and s.get("time_basis")=="scenario":
                warnings.append(f"{sid}: baseline uses scenario time_basis")
            if s.get("type")=="target" and s.get("time_basis")=="actual":
                warnings.append(f"{sid}: target uses actual time_basis")
        for tr in d.get("transitions",[]) or []:
            tid=tr.get("id","?")
            ps=pd(tr.get("planned_start"),f"{tid}.planned_start",errors)
            pe=pd(tr.get("planned_end"),f"{tid}.planned_end",errors)
            acs=pd(tr.get("actual_start"),f"{tid}.actual_start",errors)
            ace=pd(tr.get("actual_end"),f"{tid}.actual_end",errors)
            if ps and pe and ps>pe: errors.append(f"{tid}: planned_start is after planned_end")
            if acs and ace and acs>ace: errors.append(f"{tid}: actual_start is after actual_end")
            if ace and not acs: warnings.append(f"{tid}: actual_end exists without actual_start")
    return errors,warnings

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("project_dir"); ap.add_argument("--json",action="store_true"); a=ap.parse_args()
    errors,warnings=validate_temporal(a.project_dir)
    out={"status":"valid" if not errors else "invalid","errors":errors,"warnings":warnings}
    print(json.dumps(out,indent=2,ensure_ascii=False) if a.json else yaml.safe_dump(out,sort_keys=False,allow_unicode=True),end="" if not a.json else "\n")
    return 0 if not errors else 1
if __name__=="__main__": raise SystemExit(main())
