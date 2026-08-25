#!/usr/bin/env python3
from pathlib import Path
import argparse, csv, io, json, sys, yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model_loader import load_model
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

def resolve_query(report_path, project_root, qref):
    candidates=[
        report_path.parent.parent/qref,
        ROOT/qref,
        Path(project_root)/qref
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError(f"Query not found: {qref}")

def md_escape(value):
    if value is None:
        return ""
    s=str(value).replace("\\n"," ").replace("\r"," ")
    return s.replace("|","\\|")

def format_value(value, fmt="text", markdown=True, default=None):
    if value is None:
        value=default
    if value is None:
        return ""
    if fmt=="boolean":
        if markdown:
            return "Ja" if bool(value) else "Nej"
        return "true" if bool(value) else "false"
    if fmt=="code":
        return f"`{md_escape(value)}`" if markdown else str(value)
    return md_escape(value) if markdown else str(value)

def presentation_sort(rows,cfgs):
    rows=list(rows)
    for cfg in reversed(cfgs or []):
        f=cfg["field"]; rev=cfg.get("direction","asc")=="desc"
        rows.sort(key=lambda r:(get_path(r,f) is None,str(get_path(r,f))),reverse=rev)
    return rows

def section_data(logical, report_path, project_root, section):
    qpath=resolve_query(report_path,project_root,section["source"]["query"])
    result=execute(logical,read_yaml(qpath))["query_result"]
    rows=presentation_sort(result.get("rows",[]),section.get("presentation_sort"))
    return result,rows

def render_table(rows, columns):
    headings=[c["heading"] for c in columns]
    out=[
        "| " + " | ".join(md_escape(h) for h in headings) + " |",
        "| " + " | ".join("---" for _ in headings) + " |"
    ]
    for row in rows:
        vals=[]
        for c in columns:
            v=get_path(row,c["field"])
            vals.append(format_value(v,c.get("format","text"),True,c.get("default")))
        out.append("| " + " | ".join(vals) + " |")
    return "\n".join(out)

def render_list(rows, fields):
    out=[]
    for row in rows:
        vals=[get_path(row,f) for f in fields]
        vals=["" if v is None else md_escape(v) for v in vals]
        if not vals:
            continue
        first=vals[0]
        rest=[v for v in vals[1:] if v]
        line=f"- **{first}**"
        if rest:
            line+=" — " + " — ".join(rest)
        out.append(line)
    return "\n".join(out)

def render_summary(result):
    out=[]
    out.append(f"Totalt: **{result.get('count',0)}**")
    groups=result.get("groups")
    if groups:
        out += ["", "| Grupp | Antal |", "|---|---:|"]
        for key,count in groups.items():
            out.append(f"| {md_escape(key)} | {count} |")
    return "\n".join(out)

def render_section_markdown(logical, report_path, project_root, section):
    result,rows=section_data(logical,report_path,project_root,section)
    out=[f"## {section['title']}"]
    if section.get("intro"):
        out += ["", section["intro"].strip()]

    if not rows and not result.get("groups"):
        out += ["", section.get("empty_message","Inga resultat.")]
    else:
        group_cfg=section.get("group_by")
        render=section["render"]
        if group_cfg and rows:
            field=group_cfg["field"]
            groups={}
            for row in rows:
                key=get_path(row,field)
                key="Övrigt" if key is None else str(key)
                groups.setdefault(key,[]).append(row)
            for key in sorted(groups):
                out += ["", f"### {md_escape(key)}", ""]
                if render["type"]=="table":
                    out.append(render_table(groups[key],render["columns"]))
                elif render["type"]=="list":
                    out.append(render_list(groups[key],render["item_fields"]))
                elif render["type"]=="summary":
                    out.append(f"Antal: **{len(groups[key])}**")
        else:
            out.append("")
            if render["type"]=="table":
                out.append(render_table(rows,render["columns"]))
            elif render["type"]=="list":
                out.append(render_list(rows,render["item_fields"]))
            elif render["type"]=="summary":
                out.append(render_summary(result))

    if section.get("notes"):
        out += ["", "**Noteringar**"]
        for note in section["notes"]:
            out.append(f"- {note}")
    return "\n".join(out)

def render_markdown(project_root, report_file):
    logical,errors,_load=load_model(Path(project_root))
    if errors:
        raise ValueError("Project invalid: " + "; ".join(errors))
    report_path=Path(report_file)
    report=read_yaml(report_path)["report"]
    out=[f"# {report['title']}"]
    if report.get("description"):
        out += ["", report["description"].strip()]
    for section in report["sections"]:
        out += ["", render_section_markdown(logical,report_path,project_root,section)]
    return "\n".join(out).rstrip()+"\n"

def csv_text(rows,columns):
    buf=io.StringIO(newline="")
    writer=csv.writer(buf)
    writer.writerow([c["heading"] for c in columns])
    for row in rows:
        values=[]
        for c in columns:
            values.append(format_value(
                get_path(row,c["field"]),
                c.get("format","text"),
                False,
                c.get("default")
            ))
        writer.writerow(values)
    return buf.getvalue()

def render_csv_files(project_root, report_file):
    logical,errors,_load=load_model(Path(project_root))
    if errors:
        raise ValueError("Project invalid: " + "; ".join(errors))
    report_path=Path(report_file)
    report=read_yaml(report_path)["report"]
    files={}
    for section in report["sections"]:
        render=section["render"]
        if render["type"]!="table":
            continue
        result,rows=section_data(logical,report_path,project_root,section)
        name=f"{report['id']}--{section['id']}.csv"
        files[name]=csv_text(rows,render["columns"])
    return files

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("report_file")
    ap.add_argument("--format",choices=["markdown","csv"],default="markdown")
    ap.add_argument("--output")
    ap.add_argument("--output-dir")
    args=ap.parse_args()

    try:
        if args.format=="markdown":
            text=render_markdown(args.project_dir,args.report_file)
            if args.output:
                p=Path(args.output); p.parent.mkdir(parents=True,exist_ok=True)
                p.write_text(text,encoding="utf-8")
                print(f"OK: {p}")
            else:
                print(text,end="")
        else:
            if not args.output_dir:
                print("FAILED")
                print("- --output-dir is required for CSV")
                return 2
            files=render_csv_files(args.project_dir,args.report_file)
            outdir=Path(args.output_dir); outdir.mkdir(parents=True,exist_ok=True)
            for name,text in files.items():
                (outdir/name).write_text(text,encoding="utf-8",newline="")
                print(f"OK: {outdir/name}")
            if not files:
                print("OK: no table sections to export")
    except Exception as e:
        print("FAILED")
        print("-",str(e))
        return 1
    return 0

if __name__=="__main__":
    raise SystemExit(main())
