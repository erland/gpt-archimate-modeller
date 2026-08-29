#!/usr/bin/env python3
from pathlib import Path
import argparse,json,shutil,sys,tempfile,yaml

sys.path.insert(0,str(Path(__file__).resolve().parent))

from project_control import inspect_zip,unpack_project,inspect_project,project_validation,pack_project
from migrate_project import compatibility,apply as migrate_apply
from identity import normalize_name
from assemble_project import assemble
from apply_changes import apply as apply_changes

def read_yaml(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))

def change_set_id(doc):
    return (doc.get("change_set") or {}).get("id")

def current_model_version(root):
    return read_yaml(Path(root)/"project.yaml")["project"]["model_version"]

def applied_change_ids(root):
    p=Path(root)/"changes"/"index.yaml"
    d=read_yaml(p) if p.exists() else {"changes":[]}
    return {x.get("id") for x in d.get("changes",[]) if x.get("id")}

def duplicate_candidates(root,change_doc):
    logical,errors=assemble(Path(root))
    if errors:
        raise ValueError("Cannot inspect duplicate candidates: "+"; ".join(errors))
    existing=logical["model"]["elements"]
    out=[]
    for op in (change_doc.get("change_set") or {}).get("operations",[]):
        if op.get("op")!="add_element":
            continue
        e=op.get("element") or {}
        eid=e.get("id"); name=e.get("name"); typ=e.get("type")
        aliases={normalize_name(x) for x in (e.get("aliases") or [])}
        norm=normalize_name(name) if name else None
        for old in existing:
            reasons=[]
            if eid and old["id"]==eid: reasons.append("same_id")
            if name and old.get("name")==name and (not typ or old.get("type")==typ):
                reasons.append("exact_name_type")
            if norm and normalize_name(old.get("name",""))==norm and old["id"]!=eid:
                reasons.append("normalized_name")
            old_aliases={normalize_name(x) for x in (old.get("aliases") or [])}
            if aliases and aliases.intersection(old_aliases):
                reasons.append("shared_alias")
            if reasons:
                out.append({
                    "new_id":eid,
                    "existing_id":old["id"],
                    "existing_name":old.get("name"),
                    "reasons":sorted(set(reasons))
                })
    return out

def do_update(input_zip,change_file,output_zip,allow_migration=False,allow_duplicate_candidates=False):
    state={"status":"failed","stage":"inspect_zip"}
    z=inspect_zip(input_zip)
    if z.get("status")!="valid":
        state["input_zip"]=z
        return state

    temp=Path(tempfile.mkdtemp(prefix="ea-update-"))
    try:
        root=unpack_project(input_zip,temp/"workspace")

        state["stage"]="compatibility"
        comp=compatibility(root)
        if comp["status"]=="unsupported_future":
            state["compatibility"]=comp
            return state
        if comp["status"]=="migration_available":
            if not allow_migration:
                return {"status":"migration_required","stage":"compatibility","compatibility":comp}
            migrate_apply(root)
        elif comp["status"]!="current":
            state["compatibility"]=comp
            return state

        state["stage"]="inspect_project"
        before_info=inspect_project(root)
        if before_info.get("status")!="valid":
            state["project_before"]=before_info
            return state

        before_version=current_model_version(root)
        doc=read_yaml(change_file)
        cid=change_set_id(doc)
        if not cid:
            raise ValueError("Change set ID missing")

        if cid in applied_change_ids(root):
            return {"status":"already_applied","stage":"change_gate","change_set_id":cid}

        expected=(doc.get("change_set") or {}).get("expected_model_version")
        if expected and str(expected)!=str(before_version):
            return {
                "status":"stale_change_set",
                "stage":"change_gate",
                "change_set_id":cid,
                "expected_model_version":str(expected),
                "actual_model_version":str(before_version)
            }

        state["stage"]="duplicate_check"
        dupes=duplicate_candidates(root,doc)
        if dupes and not allow_duplicate_candidates:
            return {
                "status":"duplicate_candidates",
                "stage":"duplicate_check",
                "change_set_id":cid,
                "candidates":dupes
            }

        state["stage"]="dry_run"
        dry=apply_changes(root,doc,dry_run=True)

        state["stage"]="apply"
        applied=apply_changes(root,doc,dry_run=False)

        state["stage"]="post_validation"
        pv=project_validation(root)
        if pv["validation_errors"]:
            state["validation_errors"]=pv["validation_errors"]
            return state
        if pv["version_history_errors"]:
            state["version_history_errors"]=pv["version_history_errors"]
            return state

        after_info=inspect_project(root)
        after_version=current_model_version(root)

        state["stage"]="pack"
        out=pack_project(root,output_zip)
        final=inspect_zip(out)
        if final.get("status")!="valid":
            state["final_zip"]=final
            return state

        return {
            "status":"updated",
            "stage":"complete",
            "project_id":after_info["project"]["id"],
            "change_set_id":cid,
            "model_version_before":before_version,
            "model_version_after":after_version,
            "computed_impact":applied.get("impact"),
            "touched":applied.get("touched",[]),
            "duplicate_candidates":dupes,
            "validation":{
                "errors":after_info["validation"]["errors"],
                "warnings":after_info["validation"]["warnings"],
                "version_history_errors":after_info["validation"]["version_history_errors"]
            },
            "quality":after_info["quality"],
            "output_zip":str(out),
            "final_zip_warnings":final.get("warnings",[])
        }
    except Exception as e:
        state["error"]=str(e)
        return state
    finally:
        shutil.rmtree(temp,ignore_errors=True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("input_zip")
    ap.add_argument("change_set")
    ap.add_argument("--output",required=True)
    ap.add_argument("--allow-migration",action="store_true")
    ap.add_argument("--allow-duplicate-candidates",action="store_true")
    ap.add_argument("--json",action="store_true")
    a=ap.parse_args()

    result=do_update(
        a.input_zip,a.change_set,a.output,
        allow_migration=a.allow_migration,
        allow_duplicate_candidates=a.allow_duplicate_candidates
    )
    payload={"update_project_result":result}
    if a.json:
        print(json.dumps(payload,indent=2,ensure_ascii=False))
    else:
        print(yaml.safe_dump(payload,sort_keys=False,allow_unicode=True,width=120),end="")
    return 0 if result.get("status")=="updated" else 1

if __name__=="__main__":
    raise SystemExit(main())
