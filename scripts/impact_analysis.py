#!/usr/bin/env python3
from pathlib import Path
import argparse,json,yaml,collections,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from model_loader import load_model

def rd(p): return yaml.safe_load(Path(p).read_text(encoding="utf-8")) or {}

def relation_certainty(rel):
    ev=rel.get("evidence") or {}
    conf=ev.get("confidence","unknown")
    status=ev.get("status","unknown")
    if conf in ("low","unknown") or status in ("inferred","unknown"):
        return "weak"
    if conf=="medium" or status=="mixed":
        return "moderate"
    return "strong"

def combine_certainty(current,new):
    rank={"strong":0,"moderate":1,"weak":2}
    return current if rank[current]>=rank[new] else new

def build_graph(logical, direction, allowed=None, excluded=None):
    allowed=set(allowed or [])
    excluded=set(excluded or [])
    graph=collections.defaultdict(list)
    for r in logical["model"]["relationships"]:
        if allowed and r.get("type") not in allowed: continue
        if r.get("type") in excluded: continue
        s,t=r.get("source"),r.get("target")
        edge={"relationship_id":r["id"],"relationship_type":r["type"],
              "source":s,"target":t,"certainty":relation_certainty(r)}
        if direction in ("outgoing","both"):
            graph[s].append((t,edge))
        if direction in ("incoming","both"):
            rev=dict(edge); rev["traversal"]="reverse"
            graph[t].append((s,rev))
    for k in graph:
        graph[k].sort(key=lambda x:(x[1]["relationship_type"],x[1]["relationship_id"],x[0]))
    return graph

def analyze(logical,seeds,direction="both",max_depth=3,relationship_types=None,
            exclude_relationship_types=None,include_seeds=False,stop_types=None,include_paths=True):
    elements={e["id"]:e for e in logical["model"]["elements"]}
    relationships={r["id"]:r for r in logical["model"]["relationships"]}
    all_ids=set(elements)|set(relationships)
    missing=[s for s in seeds if s not in all_ids]
    if missing: raise ValueError("Unknown seed object(s): "+", ".join(missing))
    # Relationship seeds are converted to their endpoints and kept as explicit seed metadata.
    normalized=[]
    seed_relationships=[]
    for s in seeds:
        if s in elements: normalized.append(s)
        else:
            r=relationships[s]; seed_relationships.append(s); normalized.extend([r["source"],r["target"]])
    normalized=sorted(set(normalized))
    graph=build_graph(logical,direction,relationship_types,exclude_relationship_types)
    stop_types=set(stop_types or [])
    queue=collections.deque()
    best={}
    for s in normalized:
        queue.append((s,0,[], "strong"))
        best[s]={"depth":0,"path":[],"certainty":"strong"}
    while queue:
        node,depth,path,certainty=queue.popleft()
        if depth>=max_depth: continue
        if depth>0 and elements.get(node,{}).get("type") in stop_types: continue
        for nxt,edge in graph.get(node,[]):
            nd=depth+1
            nc=combine_certainty(certainty,edge["certainty"])
            npath=path+[edge]
            old=best.get(nxt)
            if old is None or nd<old["depth"] or (nd==old["depth"] and npath<old["path"]):
                best[nxt]={"depth":nd,"path":npath,"certainty":nc}
                queue.append((nxt,nd,npath,nc))

    impacts=[]
    for oid,info in best.items():
        if info["depth"]==0 and not include_seeds: continue
        obj=elements.get(oid)
        if not obj: continue
        impacts.append({
            "id":oid,"type":obj.get("type"),"name":obj.get("name"),
            "specialization":obj.get("specialization"),
            "depth":info["depth"],
            "impact_basis":"seed" if info["depth"]==0 else ("direct" if info["depth"]==1 else "indirect"),
            "certainty":info["certainty"],
            **({"path":info["path"]} if include_paths else {})
        })
    impacts.sort(key=lambda x:(x["depth"],x["type"] or "",x["name"] or "",x["id"]))
    counts=collections.Counter(x["impact_basis"] for x in impacts)
    certainty_counts=collections.Counter(x["certainty"] for x in impacts)
    return {
        "seeds":list(seeds),"normalized_element_seeds":normalized,"seed_relationships":seed_relationships,
        "direction":direction,"max_depth":max_depth,
        "relationship_types":relationship_types or [],
        "excluded_relationship_types":exclude_relationship_types or [],
        "impacted_count":len(impacts),
        "counts_by_basis":dict(counts),
        "counts_by_certainty":dict(certainty_counts),
        "impacts":impacts,
        "interpretation":"Results show modeled graph reachability. They do not by themselves prove real-world causal impact."
    }

def seeds_from_change_set(path):
    d=rd(path); cs=d.get("change_set") or d
    ids=[]
    for op in cs.get("operations",[]) or []:
        for key in ("id","relationship_id","element_id"):
            if op.get(key): ids.append(op[key])
        for key in ("element","relationship","issue","reference","source"):
            if isinstance(op.get(key),dict) and op[key].get("id"): ids.append(op[key]["id"])
    return sorted(set(x for x in ids if isinstance(x,str) and (x.startswith(("APP-","STR-","BUS-","TEC-","PHY-","IMP-","CMP-","MOT-","REL-")))))

def seeds_from_state_delta(project_root,from_state,to_state):
    from architecture_states import resolve_state
    a=resolve_state(project_root,from_state); b=resolve_state(project_root,to_state)
    ae=set(a["elements"]); be=set(b["elements"]); ar=set(a["relationships"]); br=set(b["relationships"])
    return sorted((ae^be)|(ar^br))

def to_markdown(result,title="Impact analysis"):
    lines=[f"# {title}","",f"- Direction: `{result['direction']}`",f"- Max depth: `{result['max_depth']}`",
           f"- Seeds: {', '.join('`'+x+'`' for x in result['seeds'])}",f"- Impacted objects: **{result['impacted_count']}**","",
           "> "+result["interpretation"],""]
    if not result["impacts"]:
        lines.append("No impacted objects found.")
        return "\n".join(lines)+"\n"
    lines += ["| Depth | Basis | Certainty | ID | Type | Name | Path |","|---:|---|---|---|---|---|---|"]
    for x in result["impacts"]:
        p=" → ".join(e["relationship_id"] for e in x.get("path",[])) or "—"
        name=(x.get("name") or "").replace("|","\\|")
        lines.append(f"| {x['depth']} | {x['impact_basis']} | {x['certainty']} | `{x['id']}` | {x.get('type','')} | {name} | {p} |")
    return "\n".join(lines)+"\n"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("--seed",action="append",default=[])
    ap.add_argument("--change-set")
    ap.add_argument("--from-state"); ap.add_argument("--to-state")
    ap.add_argument("--direction",choices=["outgoing","incoming","both"],default="both")
    ap.add_argument("--max-depth",type=int,default=3)
    ap.add_argument("--relationship-type",action="append")
    ap.add_argument("--exclude-relationship-type",action="append")
    ap.add_argument("--include-seeds",action="store_true")
    ap.add_argument("--stop-type",action="append")
    ap.add_argument("--no-paths",action="store_true")
    ap.add_argument("--format",choices=["yaml","json","markdown"],default="yaml")
    ap.add_argument("--output")
    a=ap.parse_args()
    try:
        logical,errors,_load=load_model(Path(a.project_dir))
        if errors: raise ValueError("; ".join(errors))
        seeds=list(a.seed)
        if a.change_set: seeds += seeds_from_change_set(a.change_set)
        if a.from_state or a.to_state:
            if not (a.from_state and a.to_state): raise ValueError("--from-state and --to-state must be used together")
            seeds += seeds_from_state_delta(a.project_dir,a.from_state,a.to_state)
        seeds=sorted(set(seeds))
        if not seeds: raise ValueError("At least one seed, change-set, or state delta is required")
        r=analyze(logical,seeds,a.direction,a.max_depth,a.relationship_type,a.exclude_relationship_type,
                  a.include_seeds,a.stop_type,not a.no_paths)
        if a.format=="json": text=json.dumps({"impact_analysis_result":r},indent=2,ensure_ascii=False)+"\n"
        elif a.format=="markdown": text=to_markdown(r)
        else: text=yaml.safe_dump({"impact_analysis_result":r},sort_keys=False,allow_unicode=True,width=120)
        if a.output: Path(a.output).write_text(text,encoding="utf-8")
        else: print(text,end="")
        return 0
    except Exception as e:
        print("FAILED"); print("-",str(e)); return 1

if __name__=="__main__": raise SystemExit(main())
