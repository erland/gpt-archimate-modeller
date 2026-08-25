#!/usr/bin/env python3
from pathlib import Path
import argparse, json, os, shutil, subprocess, sys, tempfile, yaml, zipfile

sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_project_zip import validate_zip
from safe_unpack import safe_extract
from pack_project import pack as raw_pack
from validate import validate
from quality_check import load_yaml, run_quality, DEFAULT_PROFILE
from assemble_project import assemble

ROOT=Path(__file__).resolve().parents[1]

def read_yaml(p):
    return yaml.safe_load(Path(p).read_text(encoding="utf-8"))

def version_history_errors(project_root):
    root=Path(project_root)
    errors=[]
    mf=read_yaml(root/"project.yaml")
    idx=read_yaml(root/"changes"/"index.yaml") if (root/"changes"/"index.yaml").exists() else {"changes":[]}
    hist=read_yaml(root/"versioning"/"history.yaml") if (root/"versioning"/"history.yaml").exists() else {"history":[]}

    ids=[x.get("id") for x in idx.get("changes",[])]
    vers=[x.get("model_version") for x in hist.get("history",[])]
    if len(ids)!=len(set(ids)):
        errors.append("Duplicate change-set ID")
    if len(vers)!=len(set(vers)):
        errors.append("Duplicate model_version")

    for x in idx.get("changes",[]):
        f=x.get("file")
        if f and not (root/"changes"/f).exists():
            errors.append(f"Missing indexed change file: {f}")

    indexed={x.get("file") for x in idx.get("changes",[]) if x.get("file")}
    for p in (root/"changes").glob("CHG-*.yaml"):
        if p.name not in indexed:
            errors.append(f"Unindexed change file: {p.name}")

    if hist.get("history"):
        latest=hist["history"][-1].get("model_version")
        current=mf["project"].get("model_version")
        if latest!=current:
            errors.append(f"Current model_version {current} != latest history {latest}")

    return errors

def project_validation(project_root):
    logical,findings=validate(project_root)
    errors=[x for x in findings if x["severity"]=="error"]
    warnings=[x for x in findings if x["severity"]=="warning"]
    quality_findings=[]
    quality_score=None
    quality_counts={"error":0,"warning":0,"info":0}
    if logical is not None and not errors:
        profile=load_yaml(DEFAULT_PROFILE)
        quality_findings,quality_score,quality_counts=run_quality(logical,profile)
    history_errors=version_history_errors(project_root)
    return {
        "logical":logical,
        "validation_findings":findings,
        "validation_errors":errors,
        "validation_warnings":warnings,
        "quality_findings":quality_findings,
        "quality_score":quality_score,
        "quality_counts":quality_counts,
        "version_history_errors":history_errors
    }

def inspect_project(project_root):
    root=Path(project_root)
    v=project_validation(root)
    logical=v["logical"]
    if logical is None:
        return {
            "status":"invalid",
            "validation_errors":len(v["validation_errors"]),
            "version_history_errors":len(v["version_history_errors"])
        }

    p=logical["project"]
    files=lambda d,pat="*.yaml": len(list((root/d).glob(pat))) if (root/d).exists() else 0
    return {
        "status":"valid" if not v["validation_errors"] and not v["version_history_errors"] else "invalid",
        "project":{
            "id":p.get("id"),
            "name":p.get("name"),
            "model_version":p.get("model_version"),
            "archimate_version":p.get("archimate_version")
        },
        "format_version":logical.get("format_version"),
        "counts":{
            "elements":len(logical["model"]["elements"]),
            "relationships":len(logical["model"]["relationships"]),
            "sources":len(logical.get("sources",[])),
            "references":len(logical.get("references",[])),
            "issues":len(logical.get("issues",[])),
            "change_sets":len(list((root/"changes").glob("CHG-*.yaml"))) if (root/"changes").exists() else 0,
            "queries":files("queries"),
            "reports":files("reports"),
            "views":files("views")
        },
        "validation":{
            "errors":len(v["validation_errors"]),
            "warnings":len(v["validation_warnings"]),
            "version_history_errors":len(v["version_history_errors"])
        },
        "quality":{
            "score":v["quality_score"],
            "warnings":v["quality_counts"]["warning"],
            "info":v["quality_counts"]["info"]
        }
    }

def inspect_zip(zip_file):
    result,errors,warnings=validate_zip(zip_file)
    if result is None:
        return {"status":"invalid","errors":errors,"warnings":warnings}
    with zipfile.ZipFile(zip_file,"r") as z:
        file_count=sum(1 for x in z.infolist() if not x.is_dir())
    out=dict(result)
    out["file_count"]=file_count
    return out

def unpack_project(zip_file, output_dir):
    zres,zerr,zwarn=validate_zip(zip_file)
    if zerr:
        raise ValueError("ZIP contract validation failed: "+"; ".join(zerr))

    out=Path(output_dir)
    if out.exists() and any(out.iterdir()):
        raise ValueError("Output directory must be empty or not exist")

    temp_parent=Path(tempfile.mkdtemp(prefix="ea-unpack-"))
    try:
        extracted_root=safe_extract(zip_file,temp_parent)
        v=project_validation(extracted_root)
        if v["validation_errors"]:
            raise ValueError("Project validation failed after extraction")
        if v["version_history_errors"]:
            raise ValueError("Version history validation failed after extraction")

        project_id=read_yaml(extracted_root/"project.yaml")["project"]["id"]
        final_root=out/project_id
        out.mkdir(parents=True,exist_ok=True)
        if extracted_root.resolve()==temp_parent.resolve():
            shutil.copytree(extracted_root,final_root)
        else:
            shutil.move(str(extracted_root),str(final_root))

        marker={
            "project_control":{
                "contract_version":"0.1",
                "source_package":str(Path(zip_file).name),
                "verified":True
            }
        }
        (final_root/".project-control.yaml").write_text(
            yaml.safe_dump(marker,sort_keys=False,allow_unicode=True),
            encoding="utf-8"
        )
        return final_root
    finally:
        shutil.rmtree(temp_parent,ignore_errors=True)

def pack_project(project_root, output_zip):
    root=Path(project_root)
    v=project_validation(root)
    if v["validation_errors"]:
        raise ValueError("Project validation failed before pack")
    if v["version_history_errors"]:
        raise ValueError("Version history validation failed before pack")

    tempdir=Path(tempfile.mkdtemp(prefix="ea-repack-"))
    try:
        staged=tempdir/root.name
        shutil.copytree(root,staged)
        (staged/".project-control.yaml").unlink(missing_ok=True)

        temp_zip=tempdir/"candidate.zip"
        raw_pack(staged,temp_zip)
        zres,zerr,zwarn=validate_zip(temp_zip)
        if zerr:
            raise ValueError("Generated ZIP failed contract validation: "+"; ".join(zerr))

        out=Path(output_zip)
        out.parent.mkdir(parents=True,exist_ok=True)
        temp_out=out.parent/(out.name+".tmp")
        shutil.copy2(temp_zip,temp_out)
        os.replace(temp_out,out)
        return out
    finally:
        shutil.rmtree(tempdir,ignore_errors=True)

def roundtrip(zip_file):
    z1=inspect_zip(zip_file)
    if z1.get("status")!="valid":
        return {"status":"failed","stage":"input_zip","input_zip":z1}

    temp=Path(tempfile.mkdtemp(prefix="ea-roundtrip-"))
    try:
        workspace=temp/"workspace"
        root=unpack_project(zip_file,workspace)
        p1=inspect_project(root)
        if p1.get("status")!="valid":
            return {"status":"failed","stage":"project","project":p1}

        repacked=temp/"roundtrip.zip"
        pack_project(root,repacked)
        z2=inspect_zip(repacked)
        if z2.get("status")!="valid":
            return {"status":"failed","stage":"repacked_zip","output_zip":z2}

        return {
            "status":"ok",
            "input_zip":z1,
            "project":p1,
            "output_zip":z2
        }
    finally:
        shutil.rmtree(temp,ignore_errors=True)

def emit(data,as_json=False):
    if as_json:
        print(json.dumps(data,indent=2,ensure_ascii=False))
    else:
        print(yaml.safe_dump(data,sort_keys=False,allow_unicode=True,width=120),end="")

def main():
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="cmd",required=True)

    p=sub.add_parser("inspect-zip")
    p.add_argument("zip_file"); p.add_argument("--json",action="store_true")

    p=sub.add_parser("unpack")
    p.add_argument("zip_file"); p.add_argument("--output-dir",required=True)

    p=sub.add_parser("inspect-project")
    p.add_argument("project_dir"); p.add_argument("--json",action="store_true")

    p=sub.add_parser("validate-project")
    p.add_argument("project_dir"); p.add_argument("--json",action="store_true")

    p=sub.add_parser("pack")
    p.add_argument("project_dir"); p.add_argument("--output",required=True)

    p=sub.add_parser("roundtrip")
    p.add_argument("zip_file"); p.add_argument("--json",action="store_true")

    a=ap.parse_args()

    try:
        if a.cmd=="inspect-zip":
            data=inspect_zip(a.zip_file); emit(data,a.json)
            return 0 if data.get("status")=="valid" else 1

        if a.cmd=="unpack":
            root=unpack_project(a.zip_file,a.output_dir)
            print(f"OK: {root}")
            return 0

        if a.cmd=="inspect-project":
            data=inspect_project(a.project_dir); emit(data,a.json)
            return 0 if data.get("status")=="valid" else 1

        if a.cmd=="validate-project":
            v=project_validation(a.project_dir)
            data={
                "status":"valid" if not v["validation_errors"] and not v["version_history_errors"] else "invalid",
                "validation_errors":v["validation_errors"],
                "validation_warnings":v["validation_warnings"],
                "version_history_errors":v["version_history_errors"],
                "quality_score":v["quality_score"],
                "quality_counts":v["quality_counts"],
                "quality_findings":v["quality_findings"]
            }
            emit(data,a.json)
            return 0 if data["status"]=="valid" else 1

        if a.cmd=="pack":
            out=pack_project(a.project_dir,a.output)
            print(f"OK: {out}")
            return 0

        if a.cmd=="roundtrip":
            data=roundtrip(a.zip_file); emit(data,a.json)
            return 0 if data.get("status")=="ok" else 1

    except Exception as e:
        print("FAILED")
        print("-",str(e))
        return 1

if __name__=="__main__":
    raise SystemExit(main())
