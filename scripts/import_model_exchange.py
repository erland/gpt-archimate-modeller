#!/usr/bin/env python3
from pathlib import Path
import argparse, json, re, shutil, sys, xml.etree.ElementTree as ET, yaml

NS="http://www.opengroup.org/xsd/archimate/3.0/"
XSI="http://www.w3.org/2001/XMLSchema-instance"
XML="http://www.w3.org/XML/1998/namespace"

PARTITIONS={
    "MOT":"motivation","STR":"strategy","BUS":"business","APP":"application",
    "TEC":"technology","PHY":"physical","IMP":"implementation-migration","CMP":"composite"
}

ID_RE=re.compile(r"^([A-Z]{2,3})-([0-9]{6})$")

def q(ns,name):
    return f"{{{ns}}}{name}"

def read_text(el,name):
    x=el.find(q(NS,name))
    return x.text if x is not None and x.text is not None else None

def property_definitions(root):
    out={}
    for pd in root.findall(f".//{q(NS,'propertyDefinition')}"):
        ident=pd.get("identifier")
        name=read_text(pd,"name")
        if ident:
            out[ident]=name or ident
    return out

def properties_of(el, defs):
    props={}
    for p in el.findall(f"./{q(NS,'properties')}/{q(NS,'property')}"):
        ref=p.get("propertyDefinitionRef")
        key=defs.get(ref,ref)
        val=read_text(p,"value")
        props[key]=val
    return props

def compatible_internal_id(value):
    return bool(ID_RE.match(value or ""))

def parse(xml_file):
    tree=ET.parse(xml_file)
    root=tree.getroot()
    if root.tag != q(NS,"model"):
        raise ValueError("Unsupported or missing ArchiMate model namespace")

    defs=property_definitions(root)
    model_props=properties_of(root,defs)

    preview={
        "model":{
            "id":root.get("identifier"),
            "name":read_text(root,"name"),
            "version":root.get("version"),
            "documentation":read_text(root,"documentation")
        },
        "elements":[],
        "relationships":[],
        "warnings":[],
        "unsupported":[]
    }

    for e in root.findall(f"./{q(NS,'elements')}/{q(NS,'element')}"):
        eid=e.get("identifier")
        typ=e.get(q(XSI,"type"))
        props=properties_of(e,defs)
        item={
            "id":eid,
            "type":typ,
            "name":read_text(e,"name"),
            "description":read_text(e,"documentation"),
            "properties":{}
        }

        if "ea.specialization" in props:
            item["specialization"]=props.pop("ea.specialization")
        if "ea.aliases" in props:
            item["aliases"]=[x.strip() for x in props.pop("ea.aliases").split(";") if x.strip()]

        ev_status=props.pop("ea.evidence.status",None)
        ev_conf=props.pop("ea.evidence.confidence",None)
        if ev_status or ev_conf:
            item["evidence"]={
                "status":ev_status or "imported",
                "confidence":ev_conf or "unknown",
                "assertions":[]
            }
        else:
            item["evidence"]={
                "status":"imported",
                "confidence":"unknown",
                "assertions":[]
            }

        original=props.pop("ea.original_id",None)
        if original:
            item["external_id"]=eid
            item["id"]=original

        if not compatible_internal_id(item["id"]):
            preview["warnings"].append(
                f"Element identifier {item['id']} is not compatible with internal ID strategy and needs allocation."
            )
            item["external_id"]=item["id"]
            item["needs_internal_id"]=True

        item["properties"]=props
        preview["elements"].append(item)

    ids={e["id"] for e in preview["elements"]}
    for r in root.findall(f"./{q(NS,'relationships')}/{q(NS,'relationship')}"):
        rid=r.get("identifier")
        props=properties_of(r,defs)
        item={
            "id":rid,
            "type":r.get(q(XSI,"type")),
            "source":r.get("source"),
            "target":r.get("target"),
            "name":read_text(r,"name"),
            "description":read_text(r,"documentation"),
            "properties":props
        }
        ev_status=props.pop("ea.evidence.status",None)
        ev_conf=props.pop("ea.evidence.confidence",None)
        item["evidence"]={
            "status":ev_status or "imported",
            "confidence":ev_conf or "unknown",
            "assertions":[]
        }

        original=props.pop("ea.original_id",None)
        if original:
            item["external_id"]=rid
            item["id"]=original

        if not compatible_internal_id(item["id"]):
            preview["warnings"].append(
                f"Relationship identifier {item['id']} is not compatible with internal ID strategy and needs allocation."
            )
            item["external_id"]=item["id"]
            item["needs_internal_id"]=True

        preview["relationships"].append(item)

    # Detect view/organization sections that are not imported in 0.1.
    if root.find(q(NS,"views")) is not None:
        preview["unsupported"].append("views")
    if root.find(q(NS,"organizations")) is not None:
        preview["unsupported"].append("organizations")

    return preview

def write_yaml(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(yaml.safe_dump(data,sort_keys=False,allow_unicode=True,width=120),encoding="utf-8")

def create_project(preview, outdir):
    outdir=Path(outdir)
    if outdir.exists():
        if any(outdir.iterdir()):
            raise ValueError("Output project directory must be empty or not exist")
    else:
        outdir.mkdir(parents=True)

    bad_elements=[e for e in preview["elements"] if e.get("needs_internal_id")]
    bad_rels=[r for r in preview["relationships"] if r.get("needs_internal_id")]
    if bad_elements or bad_rels:
        raise ValueError("Cannot create staging project until incompatible identifiers have been allocated")

    project_id=preview["model"]["id"] or "imported-model"
    write_yaml(outdir/"project.yaml",{
        "format_version":"0.1",
        "package_layout_version":"0.1",
        "project":{
            "id":project_id,
            "name":preview["model"]["name"] or "Imported ArchiMate model",
            "description":preview["model"].get("documentation"),
            "model_version":preview["model"].get("version") or "0.1.0",
            "language":"sv",
            "archimate_version":"3.2"
        }
    })

    by_partition={v:[] for v in PARTITIONS.values()}
    for e in preview["elements"]:
        prefix=e["id"].split("-")[0]
        part=PARTITIONS.get(prefix)
        if not part:
            raise ValueError(f"Cannot partition imported element {e['id']}")
        out={
            "id":e["id"],"type":e["type"],"name":e.get("name"),
            "evidence":e["evidence"]
        }
        for key in ["description","specialization","aliases","properties"]:
            if e.get(key):
                out[key]=e[key]
        by_partition[part].append(out)

    for part,els in by_partition.items():
        write_yaml(outdir/"model"/"elements"/f"{part}.yaml",{"elements":els})

    rels=[]
    for r in preview["relationships"]:
        out={
            "id":r["id"],"type":r["type"],"source":r["source"],"target":r["target"],
            "evidence":r["evidence"]
        }
        for key in ["name","description","properties"]:
            if r.get(key):
                out[key]=r[key]
        rels.append(out)
    write_yaml(outdir/"model"/"relationships.yaml",{"relationships":rels})

    write_yaml(outdir/"extensions"/"extensions.yaml",{"extensions":{}})
    write_yaml(outdir/"extensions"/"specializations.yaml",{"specializations":{}})
    write_yaml(outdir/"issues"/"issues.yaml",{"issues":[],"observations":[]})
    write_yaml(outdir/"sources"/"sources.yaml",{"sources":[]})
    write_yaml(outdir/"sources"/"references.yaml",{"references":[]})
    write_yaml(outdir/"changes"/"index.yaml",{"changes":[]})
    write_yaml(outdir/"versioning"/"history.yaml",{"history":[]})

    counters={}
    for e in preview["elements"]:
        m=ID_RE.match(e["id"])
        if m:
            counters[m.group(1)]=max(counters.get(m.group(1),0),int(m.group(2)))
    for r in preview["relationships"]:
        m=ID_RE.match(r["id"])
        if m:
            counters[m.group(1)]=max(counters.get(m.group(1),0),int(m.group(2)))
    write_yaml(outdir/"identity"/"id-counters.yaml",{"counters":counters})

    (outdir/"queries").mkdir(exist_ok=True)
    (outdir/"reports").mkdir(exist_ok=True)
    (outdir/"views").mkdir(exist_ok=True)
    (outdir/"exports").mkdir(exist_ok=True)
    (outdir/"CHANGELOG.md").write_text(
        "# Changelog\n\nImported from ArchiMate Model Exchange.\n",encoding="utf-8"
    )

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("xml_file")
    ap.add_argument("--preview",action="store_true")
    ap.add_argument("--output-project")
    ap.add_argument("--json",action="store_true")
    args=ap.parse_args()

    try:
        preview=parse(args.xml_file)
    except Exception as e:
        print("FAILED"); print("-",str(e)); return 1

    if args.output_project:
        try:
            create_project(preview,args.output_project)
            print(f"OK: {args.output_project}")
        except Exception as e:
            print("FAILED"); print("-",str(e)); return 1
    else:
        result={
            "import_preview":{
                "model":preview["model"],
                "element_count":len(preview["elements"]),
                "relationship_count":len(preview["relationships"]),
                "warnings":preview["warnings"],
                "unsupported":preview["unsupported"],
                "elements":preview["elements"] if args.preview else [],
                "relationships":preview["relationships"] if args.preview else []
            }
        }
        if args.json:
            print(json.dumps(result,indent=2,ensure_ascii=False))
        else:
            print(yaml.safe_dump(result,sort_keys=False,allow_unicode=True,width=120),end="")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
