#!/usr/bin/env python3
from pathlib import Path
import argparse, html, json, sys, xml.etree.ElementTree as ET, yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from assemble_project import assemble
from compile_view import compile_view

ROOT=Path(__file__).resolve().parents[1]

def read_yaml(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))

def direction_code(direction):
    return {
        "left_to_right":"LR",
        "right_to_left":"RL",
        "top_to_bottom":"TB",
        "bottom_to_top":"BT",
    }.get(direction,"LR")

def node_label(node, view):
    cfg=(view.get("nodes") or {}).get("label") or {}
    primary=cfg.get("primary","name")
    secondary=cfg.get("secondary") or []
    lines=[]
    p=node.get(primary)
    if p:
        lines.append(str(p))
    for f in secondary:
        v=node.get(f)
        if v:
            lines.append(str(v))
    for k,v in (node.get("properties") or {}).items():
        if v is not None:
            lines.append(f"{k}: {v}")
    return "\n".join(lines) if lines else node["id"]

def edge_label(edge, view):
    cfg=view.get("edges") or {}
    lines=[]
    if cfg.get("show_type",True):
        lines.append(edge.get("type",""))
    if cfg.get("show_name") and edge.get("name"):
        lines.append(edge["name"])
    if cfg.get("show_confidence") and edge.get("confidence"):
        lines.append(f"confidence: {edge['confidence']}")
    return "\n".join(x for x in lines if x)

def group_order(nodes, groups):
    declared=[g["id"] for g in groups or []]
    extras=sorted({n.get("group") for n in nodes if n.get("group") and n.get("group") not in declared})
    return declared+extras+[None]

def layout_nodes(nodes, view):
    layout=view.get("layout") or {}
    algorithm=layout.get("algorithm","auto")
    direction=layout.get("direction","left_to_right")
    groups=view.get("groups") or []
    by_group={}
    for n in nodes:
        by_group.setdefault(n.get("group"),[]).append(n)
    for vals in by_group.values():
        vals.sort(key=lambda n:n["id"])

    width=220
    height=90
    gap_x=90
    gap_y=55
    coords={}

    if algorithm=="layered":
        order=[g for g in group_order(nodes,groups) if g in by_group]
        if not order:
            order=[None]
        for gi,g in enumerate(order):
            vals=by_group.get(g,[])
            for i,n in enumerate(vals):
                if direction in ("left_to_right","right_to_left"):
                    x=80+gi*(width+gap_x)
                    y=80+i*(height+gap_y)
                else:
                    x=80+i*(width+gap_x)
                    y=80+gi*(height+gap_y)
                coords[n["id"]]=(x,y,width,height)
    else:
        cols=max(1,int(len(nodes)**0.5))
        for i,n in enumerate(sorted(nodes,key=lambda n:n["id"])):
            row=i//cols
            col=i%cols
            x=80+col*(width+gap_x)
            y=80+row*(height+gap_y)
            coords[n["id"]]=(x,y,width,height)

    # Mirror directions deterministically.
    if direction=="right_to_left" and coords:
        maxx=max(x for x,_,_,_ in coords.values())
        minx=min(x for x,_,_,_ in coords.values())
        for k,(x,y,w,h) in list(coords.items()):
            coords[k]=(maxx+minx-x,y,w,h)
    if direction=="bottom_to_top" and coords:
        maxy=max(y for _,y,_,_ in coords.values())
        miny=min(y for _,y,_,_ in coords.values())
        for k,(x,y,w,h) in list(coords.items()):
            coords[k]=(x,maxy+miny-y,w,h)
    return coords

def build_drawio(view_result, view_doc):
    v=view_doc["view"]
    nodes=view_result["nodes"]
    edges=view_result["edges"]
    coords=layout_nodes(nodes,v)

    mxfile=ET.Element("mxfile",{
        "host":"app.diagrams.net",
        "modified":"2026-08-25T00:00:00.000Z",
        "agent":"archimate-yaml-ea-gpt",
        "version":"0.1",
        "type":"device"
    })
    diagram=ET.SubElement(mxfile,"diagram",{"id":v["id"],"name":v["title"]})
    model=ET.SubElement(diagram,"mxGraphModel",{
        "dx":"1200","dy":"800","grid":"1","gridSize":"10","guides":"1",
        "tooltips":"1","connect":"1","arrows":"1","fold":"1","page":"1",
        "pageScale":"1","pageWidth":"1169","pageHeight":"827","math":"0","shadow":"0"
    })
    root=ET.SubElement(model,"root")
    ET.SubElement(root,"mxCell",{"id":"0"})
    ET.SubElement(root,"mxCell",{"id":"1","parent":"0"})

    for node in sorted(nodes,key=lambda n:n["id"]):
        x,y,w,h=coords[node["id"]]
        label=node_label(node,v).replace("\n","&#xa;")
        style=(
            "rounded=0;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;"
            "fontSize=12;spacing=6;"
        )
        cell=ET.SubElement(root,"mxCell",{
            "id":node["id"],
            "value":label,
            "style":style,
            "vertex":"1",
            "parent":"1"
        })
        ET.SubElement(cell,"mxGeometry",{
            "x":str(x),"y":str(y),"width":str(w),"height":str(h),"as":"geometry"
        })

    for edge in sorted(edges,key=lambda e:e["id"]):
        label=edge_label(edge,v).replace("\n","&#xa;")
        style=(
            "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;"
            "jettySize=auto;html=1;endArrow=block;endFill=1;"
        )
        cell=ET.SubElement(root,"mxCell",{
            "id":edge["id"],
            "value":label,
            "style":style,
            "edge":"1",
            "parent":"1",
            "source":edge["source"],
            "target":edge["target"]
        })
        ET.SubElement(cell,"mxGeometry",{"relative":"1","as":"geometry"})

    return ET.tostring(mxfile,encoding="unicode",short_empty_elements=True)

def mermaid_id(object_id):
    return object_id.replace("-","_")

def mermaid_escape(text):
    return str(text).replace('"','\\"').replace("\n","<br/>")

def build_mermaid(view_result, view_doc):
    v=view_doc["view"]
    direction=direction_code((v.get("layout") or {}).get("direction","left_to_right"))
    lines=[f"flowchart {direction}"]
    nodes=view_result["nodes"]
    edges=view_result["edges"]

    groups={}
    for n in nodes:
        groups.setdefault(n.get("group"),[]).append(n)

    group_titles={g["id"]:g["title"] for g in v.get("groups") or []}
    emitted=set()

    # Emit declared groups first.
    for gid in [g["id"] for g in v.get("groups") or []]:
        vals=sorted(groups.get(gid,[]),key=lambda n:n["id"])
        if not vals:
            continue
        lines.append(f'  subgraph G_{gid}["{mermaid_escape(group_titles.get(gid,gid))}"]')
        for n in vals:
            nid=mermaid_id(n["id"])
            label=mermaid_escape(node_label(n,v))
            lines.append(f'    {nid}["{label}"]')
            emitted.add(n["id"])
        lines.append("  end")

    # Ungrouped or undeclared.
    for n in sorted(nodes,key=lambda n:n["id"]):
        if n["id"] in emitted:
            continue
        nid=mermaid_id(n["id"])
        label=mermaid_escape(node_label(n,v))
        lines.append(f'  {nid}["{label}"]')

    for e in sorted(edges,key=lambda e:e["id"]):
        s=mermaid_id(e["source"])
        t=mermaid_id(e["target"])
        label=mermaid_escape(edge_label(e,v))
        if label:
            lines.append(f'  {s} -->|"{label}"| {t}')
        else:
            lines.append(f"  {s} --> {t}")
    return "\n".join(lines)+"\n"

def export(project_dir, view_file, fmt):
    logical,errors=assemble(Path(project_dir))
    if errors:
        raise ValueError("Project invalid: "+"; ".join(errors))
    view_doc=read_yaml(view_file)
    compiled=compile_view(logical,view_doc,view_file,project_dir)["view_result"]
    if fmt=="drawio":
        return build_drawio(compiled,view_doc)
    if fmt=="mermaid":
        return build_mermaid(compiled,view_doc)
    raise ValueError(f"Unsupported format: {fmt}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("view_file")
    ap.add_argument("--format",choices=["drawio","mermaid"],required=True)
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    try:
        text=export(args.project_dir,args.view_file,args.format)
        p=Path(args.output)
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(text,encoding="utf-8")
        print(f"OK: {p}")
    except Exception as e:
        print("FAILED")
        print("-",str(e))
        return 1
    return 0

if __name__=="__main__":
    raise SystemExit(main())
