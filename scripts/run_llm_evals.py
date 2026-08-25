#!/usr/bin/env python3
from pathlib import Path
import argparse,json,yaml,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from grade_llm_eval import grade
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--responses-dir"); ap.add_argument("--format",choices=["text","json","yaml"],default="text"); ap.add_argument("--output"); a=ap.parse_args()
    cat=yaml.safe_load((ROOT/"evals"/"catalog.yaml").read_text(encoding="utf-8")); results=[]
    for x in cat["cases"]:
        c=yaml.safe_load((ROOT/x["file"]).read_text(encoding="utf-8"))
        if not a.responses_dir: results.append({"eval_id":x["id"],"status":"not_run","category":x["category"]}); continue
        p=Path(a.responses_dir)/f"{x['id']}.md"
        if not p.exists(): results.append({"eval_id":x["id"],"status":"missing_response","category":x["category"]}); continue
        g=grade(c,p.read_text(encoding="utf-8")); g["category"]=x["category"]; results.append(g)
    passed=sum(r["status"]=="passed" for r in results); failed=sum(r["status"]=="failed" for r in results); missing=len(results)-passed-failed
    out={"llm_eval_run":{"version":"0.1","summary":{"total":len(results),"passed":passed,"failed":failed,"missing":missing},"results":results}}
    if a.format=="json": text=json.dumps(out,indent=2,ensure_ascii=False)+"\n"
    elif a.format=="yaml": text=yaml.safe_dump(out,sort_keys=False,allow_unicode=True,width=120)
    else: text=f"Total: {len(results)} Passed: {passed} Failed: {failed} Missing: {missing}\n"+"\n".join(f"[{r['status'].upper()}] {r['eval_id']} {r.get('score','')}" for r in results)+"\n"
    if a.output: Path(a.output).write_text(text,encoding="utf-8")
    else: print(text,end="")
    return 1 if failed else 0
if __name__=="__main__": raise SystemExit(main())
