#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys, yaml
sys.path.insert(0, str(Path(__file__).resolve().parent))
from model_loader import load_model

def read_yaml(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))

def get_path(obj,dotted):
    cur=obj
    for part in dotted.split("."):
        if not isinstance(cur,dict) or part not in cur:
            return None
        cur=cur[part]
    return cur

def matches(obj,where,kind):
    if not where: return True
    if "type" in where and obj.get("type")!=where["type"]: return False
    if "type_in" in where and obj.get("type") not in where["type_in"]: return False
    if "id_in" in where and obj.get("id") not in where["id_in"]: return False
    if "specialization" in where and obj.get("specialization")!=where["specialization"]: return False
    if "name_contains" in where and where["name_contains"].casefold() not in (obj.get("name") or "").casefold(): return False
    props=obj.get("properties") or {}
    for k,v in (where.get("property_equals") or {}).items():
        if props.get(k)!=v: return False
    for k,vals in (where.get("property_in") or {}).items():
        if props.get(k) not in vals: return False
    ev=obj.get("evidence") or {}
    if "evidence_status_in" in where and ev.get("status") not in where["evidence_status_in"]: return False
    if "confidence_in" in where and ev.get("confidence") not in where["confidence_in"]: return False
    if "status_in" in where and obj.get("status") not in where["status_in"]: return False
    if "priority_in" in where and obj.get("priority") not in where["priority_in"]: return False
    if "lifecycle_in" in where and (obj.get("properties") or {}).get("lifecycle") not in where["lifecycle_in"]: return False
    if "temporal_status_source_in" in where and (obj.get("temporal") or {}).get("status_source") not in where["temporal_status_source_in"]: return False
    if kind=="relationship":
        if "source_in" in where and obj.get("source") not in where["source_in"]: return False
        if "target_in" in where and obj.get("target") not in where["target_in"]: return False
    return True

def traverse(elements,relationships,start_ids,cfg):
    by_id={e["id"]:e for e in elements}
    allowed=set(cfg.get("relationship_types") or [])
    target_types=set(cfg.get("target_types") or [])
    direction=cfg["direction"]
    frontier=set(start_ids)
    visited=set(start_ids)
    result=set(start_ids if cfg.get("include_start") else [])
    for _ in range(cfg["depth"]):
        nxt=set()
        for r in relationships:
            if allowed and r.get("type") not in allowed: continue
            s,t=r.get("source"),r.get("target")
            if direction in ("outgoing","both") and s in frontier and t in by_id and t not in visited:
                nxt.add(t)
            if direction in ("incoming","both") and t in frontier and s in by_id and s not in visited:
                nxt.add(s)
        for eid in nxt:
            visited.add(eid)
            if not target_types or by_id[eid].get("type") in target_types:
                result.add(eid)
        frontier=nxt
        if not frontier: break
    return [by_id[eid] for eid in sorted(result)]

def sort_rows(rows,cfgs):
    for cfg in reversed(cfgs or []):
        field=cfg["field"]
        reverse=cfg.get("direction","asc")=="desc"
        rows.sort(key=lambda x:(get_path(x,field) is None, str(get_path(x,field))),reverse=reverse)
    return rows

def project(rows,ret):
    if not ret: return rows
    return [{f:get_path(r,f) for f in ret["fields"]} for r in rows]

def aggregate(rows,cfg):
    if not cfg: return {}
    out={}
    if cfg.get("count"): out["count"]=len(rows)
    if cfg.get("group_by"):
        groups={}
        for r in rows:
            k=get_path(r,cfg["group_by"])
            k="null" if k is None else str(k)
            groups[k]=groups.get(k,0)+1
        out["groups"]=dict(sorted(groups.items()))
    return out

def execute(logical,doc):
    q=doc["query"]
    kind=q["select"]
    if kind=="elements":
        rows=[e for e in logical["model"]["elements"] if matches(e,q.get("where"),"element")]
        if q.get("traverse"):
            rows=traverse(logical["model"]["elements"],logical["model"]["relationships"],[e["id"] for e in rows],q["traverse"])
    else:
        if q.get("traverse"):
            raise ValueError("traverse is only supported for element queries in 0.1")
        collections={"relationships":logical["model"]["relationships"],"sources":logical.get("sources",[]),
                     "references":logical.get("references",[]),"issues":logical.get("issues",[]),
                     "observations":logical.get("observations",[])}
        rows=[r for r in collections[kind] if matches(r,q.get("where"),kind.rstrip("s"))]
    sort_rows(rows,q.get("sort"))
    if q.get("limit"): rows=rows[:q["limit"]]
    agg=aggregate(rows,q.get("aggregate"))
    result={"query_result":{"query_id":q["id"],"count":len(rows),"rows":project(rows,q.get("return"))}}
    result["query_result"].update(agg)
    return result

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("project_dir"); ap.add_argument("query_file")
    ap.add_argument("--json",action="store_true"); ap.add_argument("--output")
    a=ap.parse_args()
    logical,errors,_load=load_model(Path(a.project_dir))
    if errors:
        print("FAILED")
        for e in errors: print("-",e)
        return 1
    try:
        result=execute(logical,read_yaml(a.query_file))
    except Exception as e:
        print("FAILED"); print("-",str(e)); return 1
    text=json.dumps(result,indent=2,ensure_ascii=False) if a.json else yaml.safe_dump(result,sort_keys=False,allow_unicode=True,width=120)
    if a.output: Path(a.output).write_text(text,encoding="utf-8")
    else: print(text,end="" if text.endswith("\n") else "\n")
    return 0
if __name__=="__main__": raise SystemExit(main())
