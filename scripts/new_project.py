#!/usr/bin/env python3
from pathlib import Path
import argparse,json,shutil,sys,tempfile,yaml
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate import validate
from quality_check import load_yaml,run_quality,DEFAULT_PROFILE
from pack_project import pack
from validate_project_zip import validate_zip

ROOT=Path(__file__).resolve().parents[1]
TEMPLATE=ROOT/"templates"/"ea-project-split"
SCHEMA=ROOT/"schemas"/"new-project.schema.json"
PARTITION_BY_PREFIX={"MOT":"motivation","STR":"strategy","BUS":"business","APP":"application",
                     "TEC":"technology","PHY":"physical","IMP":"implementation-migration","CMP":"composite"}
COUNTERS=["MOT","STR","BUS","APP","TEC","PHY","IMP","CMP","REL","SRC","REF","ISS","OBS","RES","EV","CHG","STA","TRN"]

def read_yaml(p): return yaml.safe_load(Path(p).read_text(encoding="utf-8"))
def write_yaml(p,d):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(yaml.safe_dump(d,sort_keys=False,allow_unicode=True,width=120),encoding="utf-8")

def validate_spec(spec):
    schema=json.loads(SCHEMA.read_text(encoding="utf-8"))
    try:
        import jsonschema
        errs=list(jsonschema.Draft202012Validator(schema).iter_errors(spec))
        if errs: raise ValueError("; ".join(e.message for e in errs))
    except ImportError:
        p=(spec or {}).get("new_project") if isinstance(spec,dict) else None
        if not isinstance(p,dict) or not p.get("id") or not p.get("name"):
            raise ValueError("new_project.id and new_project.name are required")

def normalize_spec(spec):
    validate_spec(spec); p=dict(spec["new_project"])
    p.setdefault("language","sv"); p.setdefault("model_version","0.1.0")
    p.setdefault("archimate_version","3.2"); p.setdefault("tags",[])
    prof=dict(p.get("profiles") or {})
    prof.setdefault("include_standard_extensions",True)
    prof.setdefault("include_standard_specializations",True)
    p["profiles"]=prof
    seed=dict(p.get("seed") or {})
    for k in ["elements","relationships","sources","references"]: seed.setdefault(k,[])
    p["seed"]=seed
    return p

def bump(counters,item_id):
    if item_id and "-" in item_id:
        prefix,num=item_id.split("-",1)
        if prefix in counters and num.isdigit():
            counters[prefix]=max(counters[prefix],int(num))

def create(root,spec):
    p=normalize_spec(spec); root=Path(root)
    if root.exists() and any(root.iterdir()):
        raise ValueError("Project output directory must be empty or not exist")
    root.parent.mkdir(parents=True,exist_ok=True)
    shutil.copytree(TEMPLATE,root,dirs_exist_ok=True)
    (root/"PACKAGE-MANIFEST.yaml").unlink(missing_ok=True)

    doc=read_yaml(root/"project.yaml")
    doc["format_version"]="0.1"; doc["package_layout_version"]="0.1"
    doc["project"]={"id":p["id"],"name":p["name"],"model_version":p["model_version"],
                    "archimate_version":p["archimate_version"],"language":p["language"],"tags":p["tags"]}
    if p.get("description"): doc["project"]["description"]=p["description"]
    doc.setdefault("identity",{})["strategy_version"]="0.1"
    write_yaml(root/"project.yaml",doc)

    parts={name:[] for name in PARTITION_BY_PREFIX.values()}
    for e in p["seed"]["elements"]:
        eid=e.get("id")
        if not eid or "-" not in eid: raise ValueError("Seed element requires stable ID")
        part=PARTITION_BY_PREFIX.get(eid.split("-",1)[0])
        if not part: raise ValueError(f"Unsupported seed element ID prefix: {eid}")
        parts[part].append(e)
    for part,els in parts.items(): write_yaml(root/"model"/"elements"/f"{part}.yaml",{"elements":els})

    write_yaml(root/"model"/"relationships.yaml",{"relationships":p["seed"]["relationships"]})
    write_yaml(root/"sources"/"sources.yaml",{"sources":p["seed"]["sources"]})
    write_yaml(root/"sources"/"references.yaml",{"references":p["seed"]["references"]})
    write_yaml(root/"issues"/"issues.yaml",{"issues":[],"observations":[]})

    if not p["profiles"]["include_standard_extensions"]:
        write_yaml(root/"extensions"/"extensions.yaml",{"extensions":{}})
    if not p["profiles"]["include_standard_specializations"]:
        write_yaml(root/"extensions"/"specializations.yaml",{"specializations":{}})

    counters={k:0 for k in COUNTERS}
    for obj in p["seed"]["elements"]+p["seed"]["relationships"]+p["seed"]["sources"]+p["seed"]["references"]:
        bump(counters,obj.get("id"))
        for a in (obj.get("evidence") or {}).get("assertions",[]): bump(counters,a.get("id"))
    write_yaml(root/"identity"/"id-counters.yaml",{"counters":counters})

    write_yaml(root/"architecture"/"states.yaml",{"states":[],"transitions":[]})
    write_yaml(root/"changes"/"index.yaml",{"changes":[]})
    write_yaml(root/"versioning"/"history.yaml",{"history":[
        {"model_version":p["model_version"],"impact":"initial","reason":"Initial project creation"}]})
    (root/"migrations").mkdir(parents=True,exist_ok=True)
    write_yaml(root/"migrations"/"history.yaml",{"history":[]})

    for d in ["queries","reports","views","exports"]:
        dp=root/d; dp.mkdir(parents=True,exist_ok=True)
        for child in list(dp.iterdir()):
            if child.is_file(): child.unlink()
            elif child.is_dir(): shutil.rmtree(child)

    (root/"CHANGELOG.md").write_text(f"# Changelog\n\n## {p['model_version']}\n\nInitial project creation.\n",encoding="utf-8")

    logical,findings=validate(root)
    errors=[x for x in findings if x["severity"]=="error"]
    if errors: raise ValueError("New project failed validation: "+"; ".join(x["message"] for x in errors))
    qf,score,qc=run_quality(logical,load_yaml(DEFAULT_PROFILE))
    return {"project_root":str(root),"project_id":p["id"],"model_version":p["model_version"],
            "validation_errors":0,"validation_warnings":len([x for x in findings if x["severity"]=="warning"]),
            "quality_score":score,"quality_counts":qc}

def create_zip(spec,output_zip):
    p=normalize_spec(spec); temp=Path(tempfile.mkdtemp(prefix="ea-new-project-"))
    try:
        root=temp/p["id"]; result=create(root,{"new_project":p})
        pack_result=pack(root,output_zip)
        zres,zerr,zwarn=validate_zip(output_zip)
        if zerr: raise ValueError("Generated ZIP failed contract validation: "+"; ".join(zerr))
        result["zip"]=str(output_zip); result["zip_warnings"]=zwarn
        result["pack"]=pack_result
        return result
    finally: shutil.rmtree(temp,ignore_errors=True)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--spec"); ap.add_argument("--id"); ap.add_argument("--name")
    ap.add_argument("--description"); ap.add_argument("--language",default="sv"); ap.add_argument("--model-version",default="0.1.0")
    ap.add_argument("--output-dir"); ap.add_argument("--output-zip"); ap.add_argument("--json",action="store_true")
    a=ap.parse_args()
    if not a.output_dir and not a.output_zip:
        print("FAILED"); print("- --output-dir or --output-zip is required"); return 2
    try:
        if a.spec: spec=read_yaml(a.spec)
        else:
            if not a.id or not a.name: raise ValueError("--id and --name are required without --spec")
            spec={"new_project":{"id":a.id,"name":a.name,"language":a.language,"model_version":a.model_version}}
            if a.description: spec["new_project"]["description"]=a.description
        if a.output_zip: result=create_zip(spec,a.output_zip)
        else:
            p=normalize_spec(spec); result=create(Path(a.output_dir)/p["id"],spec)
        payload={"new_project_result":result}
        print(json.dumps(payload,indent=2,ensure_ascii=False) if a.json else
              yaml.safe_dump(payload,sort_keys=False,allow_unicode=True,width=120),end="" if not a.json else "\n")
        return 0
    except Exception as e:
        print("FAILED"); print("-",str(e)); return 1
if __name__=="__main__": raise SystemExit(main())
