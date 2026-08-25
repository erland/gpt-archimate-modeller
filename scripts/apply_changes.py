#!/usr/bin/env python3
from pathlib import Path
import argparse, copy, json, shutil, sys, tempfile, yaml, re

sys.path.insert(0, str(Path(__file__).resolve().parent))
from assemble_project import assemble
from validate import validate
from quality_check import load_yaml, run_quality, DEFAULT_PROFILE
from identity import expected_prefix_for_type
from versioning import load_policy, compute_impact, bump_semver

ROOT = Path(__file__).resolve().parents[1]

PARTITION_BY_PREFIX = {
    "MOT":"motivation","STR":"strategy","BUS":"business","APP":"application",
    "TEC":"technology","PHY":"physical","IMP":"implementation-migration","CMP":"composite"
}

def read_yaml(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))

def write_yaml(path, data):
    Path(path).write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=120),
        encoding="utf-8"
    )

def get_path(obj, dotted):
    cur=obj
    for part in dotted.split("."):
        if not isinstance(cur,dict) or part not in cur:
            return None
        cur=cur[part]
    return cur

def set_path(obj, dotted, value):
    parts=dotted.split(".")
    cur=obj
    for part in parts[:-1]:
        cur=cur.setdefault(part,{})
    cur[parts[-1]]=value

def update_counter(project_root, object_id):
    m=re.match(r"^([A-Z]{2,3})-([0-9]{6})$",object_id or "")
    if not m:
        return
    prefix,num=m.group(1),int(m.group(2))
    p=Path(project_root)/"identity"/"id-counters.yaml"
    d=read_yaml(p)
    counters=d.setdefault("counters",{})
    counters[prefix]=max(int(counters.get(prefix,0)),num)
    write_yaml(p,d)

def find_element_file(project_root, element_id):
    for p in (Path(project_root)/"model"/"elements").glob("*.yaml"):
        d=read_yaml(p) or {}
        if any(e.get("id")==element_id for e in d.get("elements",[])):
            return p
    return None

def duplicate_candidate(logical, new_e):
    name=(new_e.get("name") or "").strip().casefold()
    aliases={a.strip().casefold() for a in new_e.get("aliases",[])}
    for e in logical["model"]["elements"]:
        if e.get("type")==new_e.get("type") and (e.get("name") or "").strip().casefold()==name:
            return e["id"]
        if aliases & {a.strip().casefold() for a in e.get("aliases",[])}:
            return e["id"]
    return None

def check_preconditions(obj, preconditions):
    for p in preconditions or []:
        if get_path(obj,p["path"]) != p["equals"]:
            raise ValueError(f"Precondition failed: {p['path']} != {p['equals']!r}")

def apply(project_root, change_set, dry_run=False):
    project_root=Path(project_root)
    logical, errors=assemble(project_root)
    if errors:
        raise ValueError("Project invalid before change: " + "; ".join(errors))

    cs=change_set["change_set"]
    changes_index_path=project_root/"changes"/"index.yaml"
    existing_changes=read_yaml(changes_index_path) if changes_index_path.exists() else {"changes":[]}
    if any(x.get("id")==cs["id"] for x in existing_changes.get("changes",[])):
        raise ValueError(f"Change set already applied: {cs['id']}")
    manifest=read_yaml(project_root/"project.yaml")
    if cs.get("expected_model_version") and cs["expected_model_version"] != manifest["project"]["model_version"]:
        raise ValueError(
            f"Expected model version {cs['expected_model_version']}, actual {manifest['project']['model_version']}"
        )

    tmp=Path(tempfile.mkdtemp(prefix="ea-change-"))
    target=tmp/"project"
    shutil.copytree(project_root,target)

    touched=[]

    try:
        for op in cs["operations"]:
            kind=op["op"]

            if kind=="add_element":
                current,_=assemble(target)
                e=copy.deepcopy(op["element"])
                if any(x["id"]==e["id"] for x in current["model"]["elements"]):
                    raise ValueError(f"Element ID already exists: {e['id']}")
                dup=duplicate_candidate(current,e)
                if dup:
                    raise ValueError(f"Possible duplicate element: {dup}")
                exp=expected_prefix_for_type(e.get("type"))
                if exp and not e["id"].startswith(exp+"-"):
                    raise ValueError(f"Wrong ID prefix for {e.get('type')}: {e['id']}")
                partition=PARTITION_BY_PREFIX[e["id"].split("-")[0]]
                p=target/"model"/"elements"/f"{partition}.yaml"
                d=read_yaml(p) or {"elements":[]}
                d["elements"].append(e)
                write_yaml(p,d)
                update_counter(target,e["id"])
                touched.append(e["id"])

            elif kind=="update_element":
                p=find_element_file(target,op["id"])
                if not p: raise ValueError(f"Element not found: {op['id']}")
                d=read_yaml(p)
                e=next(x for x in d["elements"] if x["id"]==op["id"])
                check_preconditions(e,op.get("preconditions"))
                if "type" in (op.get("set") or {}):
                    raise ValueError("Changing element type via update_element is not allowed")
                for key,val in (op.get("set") or {}).items():
                    set_path(e,key,val)
                write_yaml(p,d)
                touched.append(op["id"])

            elif kind=="deprecate_element":
                p=find_element_file(target,op["id"])
                if not p: raise ValueError(f"Element not found: {op['id']}")
                d=read_yaml(p)
                e=next(x for x in d["elements"] if x["id"]==op["id"])
                check_preconditions(e,op.get("preconditions"))
                e.setdefault("properties",{})["lifecycle"]="phase_out"
                write_yaml(p,d)
                touched.append(op["id"])

            elif kind=="remove_element":
                if not op.get("reason"):
                    raise ValueError("remove_element requires reason")
                cur,_=assemble(target)
                if any(r["source"]==op["id"] or r["target"]==op["id"] for r in cur["model"]["relationships"]):
                    raise ValueError(f"Cannot remove {op['id']}: relationships still reference it")
                p=find_element_file(target,op["id"])
                if not p: raise ValueError(f"Element not found: {op['id']}")
                d=read_yaml(p)
                d["elements"]=[e for e in d["elements"] if e["id"]!=op["id"]]
                write_yaml(p,d)
                touched.append(op["id"])

            elif kind=="add_relationship":
                cur,_=assemble(target)
                r=copy.deepcopy(op["relationship"])
                if any(x["id"]==r["id"] for x in cur["model"]["relationships"]):
                    raise ValueError(f"Relationship ID already exists: {r['id']}")
                ids={e["id"] for e in cur["model"]["elements"]}
                if r["source"] not in ids or r["target"] not in ids:
                    raise ValueError("Relationship source/target missing")
                p=target/"model"/"relationships.yaml"
                d=read_yaml(p) or {"relationships":[]}
                d["relationships"].append(r)
                write_yaml(p,d)
                update_counter(target,r["id"])
                touched.append(r["id"])

            elif kind=="update_relationship":
                p=target/"model"/"relationships.yaml"
                d=read_yaml(p)
                r=next((x for x in d["relationships"] if x["id"]==op["id"]),None)
                if not r: raise ValueError(f"Relationship not found: {op['id']}")
                check_preconditions(r,op.get("preconditions"))
                for key,val in (op.get("set") or {}).items():
                    if key in ("source","target"):
                        raise ValueError("Changing relationship endpoints via update_relationship is not allowed")
                    set_path(r,key,val)
                write_yaml(p,d)
                touched.append(op["id"])

            elif kind=="remove_relationship":
                p=target/"model"/"relationships.yaml"
                d=read_yaml(p)
                before=len(d["relationships"])
                d["relationships"]=[r for r in d["relationships"] if r["id"]!=op["id"]]
                if len(d["relationships"])==before:
                    raise ValueError(f"Relationship not found: {op['id']}")
                write_yaml(p,d)
                touched.append(op["id"])

            elif kind=="add_source":
                p=target/"sources"/"sources.yaml"
                d=read_yaml(p) or {"sources":[]}
                s=copy.deepcopy(op["source"])
                if any(x["id"]==s["id"] for x in d["sources"]):
                    raise ValueError(f"Source ID already exists: {s['id']}")
                d["sources"].append(s); write_yaml(p,d)
                update_counter(target,s["id"])
                touched.append(s["id"])

            elif kind=="add_reference":
                p=target/"sources"/"references.yaml"
                d=read_yaml(p) or {"references":[]}
                r=copy.deepcopy(op["reference"])
                if any(x["id"]==r["id"] for x in d["references"]):
                    raise ValueError(f"Reference ID already exists: {r['id']}")
                d["references"].append(r); write_yaml(p,d)
                update_counter(target,r["id"])
                touched.append(r["id"])

            elif kind=="add_issue":
                p=target/"issues"/"issues.yaml"
                d=read_yaml(p) or {"issues":[]}
                issue=copy.deepcopy(op["issue"])
                if any(x["id"]==issue["id"] for x in d["issues"]):
                    raise ValueError(f"Issue ID already exists: {issue['id']}")
                d["issues"].append(issue); write_yaml(p,d)
                update_counter(target,issue["id"])
                touched.append(issue["id"])

            elif kind=="resolve_issue":
                p=target/"issues"/"issues.yaml"
                d=read_yaml(p) or {"issues":[]}
                issue=next((x for x in d["issues"] if x["id"]==op["id"]),None)
                if not issue: raise ValueError(f"Issue not found: {op['id']}")
                issue["status"]="resolved"; write_yaml(p,d)
                touched.append(op["id"])

            else:
                raise ValueError(f"Unsupported operation: {kind}")

        # Technical validation
        _, findings=validate(target)
        errors=[x for x in findings if x["severity"]=="error"]
        if errors:
            raise ValueError("Changed project failed validation: " + "; ".join(x["message"] for x in errors))

        # Version and changelog only after successful validation.
        mf=read_yaml(target/"project.yaml")
        oldv=mf["project"]["model_version"]
        impact=compute_impact(change_set,load_policy(ROOT))
        newv=bump_semver(oldv,impact)
        mf["project"]["model_version"]=newv
        write_yaml(target/"project.yaml",mf)

        changes_dir=target/"changes"
        changes_dir.mkdir(exist_ok=True)
        archived=copy.deepcopy(change_set)
        archived["change_set"]["applied_model_version"]=newv
        archived["change_set"]["computed_impact"]=impact
        write_yaml(changes_dir/f"{cs['id']}.yaml",archived)

        idx_path=changes_dir/"index.yaml"
        idx=read_yaml(idx_path) if idx_path.exists() else {"changes":[]}
        idx.setdefault("changes",[]).append({
            "id":cs["id"],"model_version":newv,"date":cs["created"],
            "impact":impact,"file":f"{cs['id']}.yaml"
        })
        write_yaml(idx_path,idx)

        hist_path=target/"versioning"/"history.yaml"
        hist=read_yaml(hist_path) if hist_path.exists() else {"history":[]}
        hist.setdefault("history",[]).append({
            "model_version":newv,"previous_model_version":oldv,
            "change_set":cs["id"],"date":cs["created"],"impact":impact
        })
        write_yaml(hist_path,hist)

        changelog=target/"CHANGELOG.md"
        text=changelog.read_text(encoding="utf-8") if changelog.exists() else "# Changelog\n"
        ops="\n".join(
            f"- {x['op']}: {x.get('id') or (x.get('element') or x.get('relationship') or x.get('source') or x.get('reference') or x.get('issue') or {}).get('id','')}"
            for x in cs["operations"]
        )
        entry=f"\n## {newv} – {cs['created']}\n\n### {cs['id']} – {cs['title']}\n\nImpact: `{impact}`\n\n{ops}\n"
        changelog.write_text(text.rstrip()+entry+"\n",encoding="utf-8")

        if dry_run:
            shutil.rmtree(tmp)
            return {"status":"DRY_RUN_OK","old_version":oldv,"new_version":newv,"impact":impact,"touched":touched}

        # Commit temp result back to project root transactionally at directory level.
        backup=project_root.parent/(project_root.name+".pre-change-backup")
        if backup.exists(): shutil.rmtree(backup)
        project_root.rename(backup)
        shutil.move(str(target),str(project_root))
        shutil.rmtree(backup)
        shutil.rmtree(tmp,ignore_errors=True)
        return {"status":"APPLIED","old_version":oldv,"new_version":newv,"impact":impact,"touched":touched}

    except Exception:
        shutil.rmtree(tmp,ignore_errors=True)
        raise

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("change_set")
    ap.add_argument("--dry-run",action="store_true")
    ap.add_argument("--json",dest="json_out")
    args=ap.parse_args()
    cs=read_yaml(args.change_set)
    try:
        result=apply(args.project_dir,cs,dry_run=args.dry_run)
    except Exception as e:
        print("FAILED")
        print("-",str(e))
        return 1
    print(result["status"])
    print(f"Version: {result['old_version']} -> {result['new_version']} ({result['impact']})")
    print("Touched:",", ".join(result["touched"]))
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding="utf-8")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
