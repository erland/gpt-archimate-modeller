#!/usr/bin/env python3
from pathlib import Path
import argparse,importlib.util,json,shutil,sys,tempfile,yaml

sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate import validate

ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/"migrations"/"registry.yaml"

def read_yaml(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))

def write_yaml(path,data):
    path=Path(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(yaml.safe_dump(data,sort_keys=False,allow_unicode=True,width=120),encoding="utf-8")

def get_registry():
    return read_yaml(REGISTRY)

def project_versions(root):
    p=read_yaml(Path(root)/"project.yaml")
    return {
        "format_version":str(p.get("format_version")),
        "package_layout_version":str(p.get("package_layout_version")),
        "archimate_version":str((p.get("project") or {}).get("archimate_version"))
    }

def version_tuple(v):
    try:
        return tuple(int(x) for x in str(v).split("."))
    except Exception:
        return ()

def migration_history(root):
    p=Path(root)/"migrations"/"history.yaml"
    return read_yaml(p) if p.exists() else {"history":[]}

def build_plan(root):
    reg=get_registry()
    target=str(reg["supported_targets"]["format_version"])
    cur=project_versions(root)["format_version"]
    applied={x.get("id") for x in migration_history(root).get("history",[])}
    steps=[]
    for _ in range(100):
        if cur==target:
            return steps
        candidates=[m for m in reg["migrations"] if m["dimension"]=="format" and str(m["from"])==cur]
        if not candidates:
            return []
        step=sorted(candidates,key=lambda x:x["id"])[0]
        if step["id"] in applied:
            raise ValueError(f"Migration already applied but source version remains old: {step['id']}")
        steps.append(step)
        cur=str(step["to"])
    raise ValueError("Migration plan loop detected")

def compatibility(root):
    reg=get_registry()
    targets=reg["supported_targets"]
    cur=project_versions(root)
    out={"current":cur,"supported_targets":targets}
    if cur["format_version"]==str(targets["format_version"]) and cur["package_layout_version"]==str(targets["package_layout_version"]):
        out["status"]="current"
        return out
    if version_tuple(cur["format_version"]) > version_tuple(targets["format_version"]):
        out["status"]="unsupported_future"
        return out
    steps=build_plan(root)
    out["status"]="migration_available" if steps else "invalid"
    out["steps"]=[x["id"] for x in steps]
    return out

def load_migration(step):
    spec=importlib.util.spec_from_file_location(step["id"],ROOT/step["script"])
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def validate_migrated(root):
    _,findings=validate(root)
    errs=[x for x in findings if x["severity"]=="error"]
    if errs:
        raise ValueError("Migrated project failed validation: "+"; ".join(x["message"] for x in errs))

def apply_to_copy(src):
    src=Path(src)
    temp=Path(tempfile.mkdtemp(prefix="ea-migrate-"))
    copy_root=temp/src.name
    shutil.copytree(src,copy_root)
    steps=build_plan(copy_root)
    hist=migration_history(copy_root)
    hist.setdefault("history",[])
    for step in steps:
        load_migration(step).migrate(copy_root)
        hist["history"].append({
            "id":step["id"],
            "dimension":step["dimension"],
            "applied_from":str(step["from"]),
            "applied_to":str(step["to"])
        })
        write_yaml(copy_root/"migrations"/"history.yaml",hist)
        after=project_versions(copy_root)
        if after["format_version"]!=str(step["to"]):
            raise ValueError(f"Migration {step['id']} did not reach expected target")
    if steps:
        validate_migrated(copy_root)
    return temp,copy_root,steps

def apply(root):
    root=Path(root)
    comp=compatibility(root)
    if comp["status"]=="current":
        return {"status":"no_change","steps":[],"versions":project_versions(root)}
    if comp["status"]!="migration_available":
        raise ValueError(f"Project is not migratable: {comp['status']}")

    temp,copy_root,steps=apply_to_copy(root)
    try:
        backup=root.parent/(root.name+".pre-migration-backup")
        if backup.exists():
            shutil.rmtree(backup)
        root.rename(backup)
        shutil.move(str(copy_root),str(root))
        shutil.rmtree(backup)
        return {"status":"migrated","steps":[x["id"] for x in steps],"versions":project_versions(root)}
    finally:
        shutil.rmtree(temp,ignore_errors=True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("project_dir")
    g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--compatibility",action="store_true")
    g.add_argument("--plan",action="store_true")
    g.add_argument("--preview",action="store_true")
    g.add_argument("--apply",action="store_true")
    ap.add_argument("--json",action="store_true")
    a=ap.parse_args()
    try:
        if a.compatibility:
            out={"compatibility":compatibility(a.project_dir)}
        elif a.plan:
            comp=compatibility(a.project_dir)
            out={"migration_plan":{
                "status":comp["status"],
                "current":comp["current"],
                "target":comp["supported_targets"],
                "steps":[x["id"] for x in build_plan(a.project_dir)] if comp["status"]=="migration_available" else []
            }}
        elif a.preview:
            comp=compatibility(a.project_dir)
            if comp["status"]=="current":
                out={"migration_preview":{"status":"no_change","steps":[]}}
            elif comp["status"]!="migration_available":
                raise ValueError(f"Project is not migratable: {comp['status']}")
            else:
                temp,copy_root,steps=apply_to_copy(a.project_dir)
                try:
                    out={"migration_preview":{
                        "status":"ok",
                        "steps":[x["id"] for x in steps],
                        "result_versions":project_versions(copy_root)
                    }}
                finally:
                    shutil.rmtree(temp,ignore_errors=True)
        else:
            out={"migration_result":apply(a.project_dir)}
        print(json.dumps(out,indent=2,ensure_ascii=False) if a.json
              else yaml.safe_dump(out,sort_keys=False,allow_unicode=True,width=120),end="" if not a.json else "\n")
        return 0
    except Exception as e:
        print("FAILED")
        print("-",str(e))
        return 1

if __name__=="__main__":
    raise SystemExit(main())
