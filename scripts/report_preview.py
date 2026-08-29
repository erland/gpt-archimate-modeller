#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys, yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from assemble_project import assemble
from query import execute

ROOT=Path(__file__).resolve().parents[1]

def read_yaml(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))

def get_path(obj,dotted):
    if isinstance(obj,dict) and dotted in obj:
        return obj[dotted]
    cur=obj
    for part in dotted.split("."):
        if not isinstance(cur,dict) or part not in cur:
            return None
        cur=cur[part]
    return cur

def presentation_sort(rows,cfgs):
    for cfg in reversed(cfgs or []):
        f=cfg["field"]; rev=cfg.get("direction","asc")=="desc"
        rows.sort(key=lambda r:(get_path(r,f) is None,str(get_path(r,f))),reverse=rev)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("report_file")
    ap.add_argument("--json",action="store_true")
    args=ap.parse_args()

    logical,errors=assemble(Path(args.project_dir))
    if errors:
        print("FAILED")
        for e in errors: print("-",e)
        return 1

    report_path=Path(args.report_file)
    report=read_yaml(report_path)["report"]
    out={"report_preview":{"report_id":report["id"],"title":report["title"],"sections":[]}}

    for section in report["sections"]:
        qref=section["source"]["query"]
        candidates=[
            report_path.parent.parent/qref,
            ROOT/qref,
            Path(args.project_dir)/qref
        ]
        qpath=next((p for p in candidates if p.exists()),None)
        if not qpath:
            print("FAILED"); print("-",f"Query not found: {qref}"); return 1

        result=execute(logical,read_yaml(qpath))["query_result"]
        rows=list(result.get("rows",[]))
        presentation_sort(rows,section.get("presentation_sort"))

        groups=None
        if section.get("group_by"):
            field=section["group_by"]["field"]
            groups={}
            for row in rows:
                key=get_path(row,field)
                key="null" if key is None else str(key)
                groups.setdefault(key,[]).append(row)

        out["report_preview"]["sections"].append({
            "id":section["id"],
            "title":section["title"],
            "render_type":section["render"]["type"],
            "count":result["count"],
            "rows":rows,
            "groups":groups,
            "aggregate_groups":result.get("groups")
        })

    if args.json:
        print(json.dumps(out,indent=2,ensure_ascii=False))
    else:
        print(yaml.safe_dump(out,sort_keys=False,allow_unicode=True,width=120),end="")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
