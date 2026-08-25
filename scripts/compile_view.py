#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys, yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model_loader import load_model
from query import execute

ROOT=Path(__file__).resolve().parents[1]

def read_yaml(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))

def get_path(obj,dotted):
    cur=obj
    for part in dotted.split("."):
        if not isinstance(cur,dict) or part not in cur:
            return None
        cur=cur[part]
    return cur

def resolve_query(view_path,project_root,qref):
    candidates=[
        view_path.parent.parent/qref,
        ROOT/qref,
        Path(project_root)/qref
    ]
    return next((p for p in candidates if p.exists()),None)

def group_for(node,groups):
    for g in groups or []:
        m=g.get("match") or {}
        if m.get("ids") and node["id"] in m["ids"]:
            return g["id"]
        if m.get("types") and node.get("type") in m["types"]:
            return g["id"]
        if m.get("specializations") and node.get("specialization") in m["specializations"]:
            return g["id"]
    return None

def compile_view(logical,view_doc,view_path,project_root):
    v=view_doc["view"]
    qpath=resolve_query(Path(view_path),project_root,v["source"]["query"])
    if not qpath:
        raise FileNotFoundError(f"Query not found: {v['source']['query']}")

    qres=execute(logical,read_yaml(qpath))["query_result"]
    selected={row["id"] for row in qres.get("rows",[]) if isinstance(row,dict) and row.get("id")}

    for eid in v.get("include_elements",[]):
        selected.add(eid)
    selected-=set(v.get("exclude_elements",[]))

    by_id={e["id"]:e for e in logical["model"]["elements"]}
    missing=[eid for eid in selected if eid not in by_id]
    if missing:
        raise ValueError("View references missing elements: " + ", ".join(sorted(missing)))

    nodes=[]
    for eid in sorted(selected):
        e=by_id[eid]
        node={
            "id":e["id"],
            "type":e["type"],
            "name":e.get("name"),
            "specialization":e.get("specialization"),
            "group":group_for(e,v.get("groups"))
        }
        show_props=((v.get("nodes") or {}).get("show_properties") or [])
        if show_props:
            node["properties"]={k:(e.get("properties") or {}).get(k) for k in show_props}
        nodes.append(node)

    mode=v.get("include_relationships","between_selected")
    excluded=set(v.get("exclude_relationships",[]))
    edges=[]
    if mode!="none":
        for r in logical["model"]["relationships"]:
            if r["id"] in excluded:
                continue
            s,t=r["source"],r["target"]
            include = (s in selected and t in selected)
            if mode=="all_touching_selected":
                include = include or ((s in selected or t in selected) and s in selected and t in selected)
            if not include:
                continue
            edge={
                "id":r["id"],
                "type":r["type"],
                "source":s,
                "target":t
            }
            if (v.get("edges") or {}).get("show_name"):
                edge["name"]=r.get("name")
            if (v.get("edges") or {}).get("show_confidence"):
                edge["confidence"]=(r.get("evidence") or {}).get("confidence")
            edges.append(edge)

    return {
        "view_result":{
            "view_id":v["id"],
            "title":v["title"],
            "layout":v.get("layout",{}),
            "groups":v.get("groups",[]),
            "nodes":nodes,
            "edges":edges
        }
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("view_file")
    ap.add_argument("--json",action="store_true")
    ap.add_argument("--output")
    args=ap.parse_args()

    logical,errors,_load=load_model(Path(args.project_dir))
    if errors:
        print("FAILED")
        for e in errors:
            print("-",e)
        return 1
    try:
        result=compile_view(logical,read_yaml(args.view_file),args.view_file,args.project_dir)
    except Exception as e:
        print("FAILED")
        print("-",str(e))
        return 1

    text=json.dumps(result,indent=2,ensure_ascii=False) if args.json else yaml.safe_dump(result,sort_keys=False,allow_unicode=True,width=120)
    if args.output:
        Path(args.output).write_text(text,encoding="utf-8")
        print(f"OK: {args.output}")
    else:
        print(text,end="" if text.endswith("\n") else "\n")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
