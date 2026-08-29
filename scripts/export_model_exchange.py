#!/usr/bin/env python3
from pathlib import Path
import argparse, re, sys, xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
from assemble_project import assemble

NS="http://www.opengroup.org/xsd/archimate/3.0/"
XSI="http://www.w3.org/2001/XMLSchema-instance"
XML="http://www.w3.org/XML/1998/namespace"
SCHEMA_URL="https://www.opengroup.org/xsd/archimate/3.1/archimate3_Model.xsd"

ET.register_namespace("",NS)
ET.register_namespace("xsi",XSI)

def q(ns,name):
    return f"{{{ns}}}{name}"

def xml_id(value):
    value=str(value)
    candidate=re.sub(r"[^A-Za-z0-9_.-]","_",value)
    if not re.match(r"^[A-Za-z_]",candidate):
        candidate="id_"+candidate
    return candidate

def scalar(value):
    if value is None:
        return ""
    if isinstance(value,bool):
        return "true" if value else "false"
    if isinstance(value,(list,tuple)):
        return "; ".join(scalar(x) for x in value)
    if isinstance(value,dict):
        return "; ".join(f"{k}={scalar(v)}" for k,v in sorted(value.items()))
    return str(value)

def collect_properties(obj):
    props=dict(obj.get("properties") or {})
    if obj.get("specialization"):
        props["ea.specialization"]=obj["specialization"]
    if obj.get("aliases"):
        props["ea.aliases"]="; ".join(obj["aliases"])
    ev=obj.get("evidence") or {}
    if ev.get("status"):
        props["ea.evidence.status"]=ev["status"]
    if ev.get("confidence"):
        props["ea.evidence.confidence"]=ev["confidence"]
    return props

def add_name(parent,text,lang=None):
    if not text:
        return
    el=ET.SubElement(parent,q(NS,"name"))
    if lang:
        el.set(q(XML,"lang"),lang)
    el.text=str(text)

def add_documentation(parent,text,lang=None):
    if not text:
        return
    el=ET.SubElement(parent,q(NS,"documentation"))
    if lang:
        el.set(q(XML,"lang"),lang)
    el.text=str(text)

def add_properties(parent,props,propdef_ids):
    if not props:
        return
    container=ET.SubElement(parent,q(NS,"properties"))
    for key in sorted(props):
        p=ET.SubElement(container,q(NS,"property"),{
            "propertyDefinitionRef":propdef_ids[key]
        })
        value=ET.SubElement(p,q(NS,"value"))
        value.text=scalar(props[key])

def build_exchange(logical):
    project=logical["project"]
    model_id=xml_id(project["id"])
    lang=project.get("language")

    root=ET.Element(q(NS,"model"),{
        "identifier":model_id,
        "version":project.get("model_version","")
    })
    root.set(q(XSI,"schemaLocation"),f"{NS} {SCHEMA_URL}")

    add_name(root,project.get("name"),lang)
    add_documentation(root,project.get("description"),lang)

    all_objs=logical["model"]["elements"]+logical["model"]["relationships"]
    prop_keys=set()
    for obj in all_objs:
        prop_keys.update(collect_properties(obj).keys())

    if model_id != project["id"]:
        prop_keys.add("ea.original_model_id")

    propdef_ids={k:xml_id("propdef-"+re.sub(r"[^A-Za-z0-9_.-]","-",k)) for k in sorted(prop_keys)}

    element_id_map={}
    elements_el=ET.SubElement(root,q(NS,"elements"))
    for e in sorted(logical["model"]["elements"],key=lambda x:x["id"]):
        xid=xml_id(e["id"])
        element_id_map[e["id"]]=xid
        attrs={"identifier":xid,q(XSI,"type"):e["type"]}
        el=ET.SubElement(elements_el,q(NS,"element"),attrs)
        add_name(el,e.get("name"),lang)
        add_documentation(el,e.get("description") or e.get("documentation"),lang)
        props=collect_properties(e)
        if xid != e["id"]:
            props["ea.original_id"]=e["id"]
            if "ea.original_id" not in propdef_ids:
                propdef_ids["ea.original_id"]=xml_id("propdef-ea.original_id")
        add_properties(el,props,propdef_ids)

    if logical["model"]["relationships"]:
        rels_el=ET.SubElement(root,q(NS,"relationships"))
        for r in sorted(logical["model"]["relationships"],key=lambda x:x["id"]):
            xid=xml_id(r["id"])
            attrs={
                "identifier":xid,
                "source":element_id_map[r["source"]],
                "target":element_id_map[r["target"]],
                q(XSI,"type"):r["type"]
            }
            rel=ET.SubElement(rels_el,q(NS,"relationship"),attrs)
            add_name(rel,r.get("name"),lang)
            add_documentation(rel,r.get("description"),lang)
            props=collect_properties(r)
            if xid != r["id"]:
                props["ea.original_id"]=r["id"]
                if "ea.original_id" not in propdef_ids:
                    propdef_ids["ea.original_id"]=xml_id("propdef-ea.original_id")
            add_properties(rel,props,propdef_ids)

    # Model-level original ID only if needed.
    if model_id != project["id"]:
        props=ET.SubElement(root,q(NS,"properties"))
        p=ET.SubElement(props,q(NS,"property"),{
            "propertyDefinitionRef":propdef_ids["ea.original_model_id"]
        })
        v=ET.SubElement(p,q(NS,"value"))
        v.text=project["id"]

    if propdef_ids:
        defs=ET.SubElement(root,q(NS,"propertyDefinitions"))
        for key in sorted(propdef_ids):
            pd=ET.SubElement(defs,q(NS,"propertyDefinition"),{
                "identifier":propdef_ids[key],
                "type":"string"
            })
            add_name(pd,key,lang)

    ET.indent(ET.ElementTree(root),space="  ")
    return '<?xml version="1.0" encoding="UTF-8"?>\n'+ET.tostring(root,encoding="unicode")+"\n"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("--output",required=True)
    args=ap.parse_args()

    logical,errors=assemble(Path(args.project_dir))
    if errors:
        print("FAILED")
        for e in errors: print("-",e)
        return 1
    try:
        text=build_exchange(logical)
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
