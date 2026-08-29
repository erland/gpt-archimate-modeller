#!/usr/bin/env python3
from pathlib import Path
import argparse,csv,io,json,collections,yaml,sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from model_loader import load_model
from quality_check import load_yaml,run_quality,DEFAULT_PROFILE

def summarize(findings,score,counts):
    by_rule=collections.Counter(x["code"] for x in findings)
    by_severity=collections.Counter(x["severity"] for x in findings)
    objects=collections.defaultdict(list)
    for f in findings:
        if f.get("object_id"):
            objects[f["object_id"]].append(f)
    return {
        "score":score,
        "counts":counts,
        "finding_count":len(findings),
        "by_rule":dict(sorted(by_rule.items())),
        "by_severity":dict(sorted(by_severity.items())),
        "objects_with_findings":len(objects)
    }

def result_for_project(project_dir,profile_path=None):
    logical,errors,_load=load_model(Path(project_dir))
    if errors:
        raise ValueError("; ".join(errors))
    profile=load_yaml(profile_path or DEFAULT_PROFILE)
    findings,score,counts=run_quality(logical,profile)
    return {
        "model_quality_result":{
            "project_id":logical["project"]["id"],
            "model_version":logical["project"]["model_version"],
            "quality_profile":str(profile_path or DEFAULT_PROFILE),
            "summary":summarize(findings,score,counts),
            "findings":findings,
            "interpretation":"Quality score is a diagnostic signal derived from enabled checks and configured deductions. It is not an absolute architecture maturity rating."
        }
    }

def md_escape(v):
    if v is None: return ""
    if isinstance(v,list): v=", ".join(str(x) for x in v)
    return str(v).replace("|","\\|").replace("\n"," ")

def to_markdown(result):
    r=result["model_quality_result"]; s=r["summary"]; findings=r["findings"]
    lines=[
        "# Modellkvalitetsrapport","",
        f"- Projekt: `{r['project_id']}`",
        f"- Modellversion: `{r['model_version']}`",
        f"- Quality score: **{s['score']:.1f}/100**",
        f"- Findings: **{s['finding_count']}**",
        f"- Objekt med findings: **{s['objects_with_findings']}**","",
        "> "+r["interpretation"],"",
        "## Sammanfattning","",
        f"- Errors: {s['counts'].get('error',0)}",
        f"- Warnings: {s['counts'].get('warning',0)}",
        f"- Info: {s['counts'].get('info',0)}","",
        "## Findings per regel","",
        "| Regel | Antal |","|---|---:|"
    ]
    for code,count in s["by_rule"].items():
        lines.append(f"| `{code}` | {count} |")
    lines += ["","## Åtgärdslista",""]
    if not findings:
        lines.append("Inga quality findings.")
    else:
        lines += ["| Severity | Regel | Objekt | Meddelande | Rekommendation | Relaterade objekt |",
                  "|---|---|---|---|---|---|"]
        sev_order={"error":0,"warning":1,"info":2}
        for f in sorted(findings,key=lambda x:(sev_order.get(x["severity"],9),x["code"],x.get("object_id") or "",x["message"])):
            lines.append("| "+ " | ".join([
                md_escape(f["severity"]),
                f"`{md_escape(f['code'])}`",
                f"`{md_escape(f.get('object_id') or '—')}`",
                md_escape(f["message"]),
                md_escape(f.get("recommendation") or "—"),
                md_escape(f.get("related_ids") or "—")
            ])+" |")
    lines += ["","## Tolkning","",
              "Rapporten är dynamiskt beräknad från den aktuella modellen och quality-profilen.",
              "Den skapar inte automatiskt issues eller observations. Sådana arbetsobjekt ska skapas explicit genom change workflow.",""]
    return "\n".join(lines)

def csv_text(result):
    out=io.StringIO()
    w=csv.writer(out,lineterminator="\n")
    w.writerow(["severity","code","object_id","message","recommendation","related_ids"])
    for f in result["model_quality_result"]["findings"]:
        w.writerow([
            f.get("severity",""),f.get("code",""),f.get("object_id") or "",
            f.get("message",""),f.get("recommendation") or "",
            ";".join(f.get("related_ids") or [])
        ])
    return out.getvalue()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("--profile")
    ap.add_argument("--format",choices=["markdown","csv","json","yaml"],default="markdown")
    ap.add_argument("--output")
    a=ap.parse_args()
    try:
        result=result_for_project(a.project_dir,a.profile)
        if a.format=="markdown": text=to_markdown(result)
        elif a.format=="csv": text=csv_text(result)
        elif a.format=="json": text=json.dumps(result,indent=2,ensure_ascii=False)+"\n"
        else: text=yaml.safe_dump(result,sort_keys=False,allow_unicode=True,width=120)
        if a.output: Path(a.output).write_text(text,encoding="utf-8")
        else: print(text,end="" if text.endswith("\n") else "\n")
        return 0
    except Exception as e:
        print("FAILED"); print("-",str(e)); return 1

if __name__=="__main__":
    raise SystemExit(main())
