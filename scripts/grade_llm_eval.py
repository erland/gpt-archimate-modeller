#!/usr/bin/env python3
from pathlib import Path
import argparse,json,re,yaml
def norm(s): return re.sub(r"\s+"," ",str(s).strip().lower())
def token_match(phrase,text,ratio=0.6):
    p=norm(phrase)
    if p in text: return True
    toks=[t for t in re.findall(r"[a-z0-9_:-]+",p) if len(t)>=4]
    return bool(toks) and sum(t in text for t in toks)/len(toks)>=ratio
def forbidden_hit(phrase,text):
    p=norm(phrase)
    # Literal phrase preceded by common negations should not count as proposing the forbidden action.
    for m in re.finditer(re.escape(p),text):
        prefix=text[max(0,m.start()-28):m.start()]
        if re.search(r"(do not|don't|never|inte|ej|utan att|ska inte|bör inte|no )\s*$",prefix):
            continue
        return True
    # For fuzzy match, require high token overlap and absence of explicit nearby/global prohibition language.
    toks=[t for t in re.findall(r"[a-z0-9_:-]+",p) if len(t)>=4]
    hit=bool(toks) and sum(t in text for t in toks)/len(toks)>=0.8
    if hit and re.search(r"\b(do not|don't|never|inte|ej|utan att|ska inte|bör inte)\b",text):
        return False
    return hit
def grade(case_doc,response):
    c=case_doc["eval_case"]; e=c["expectations"]; text=norm(response); checks=[]
    def add(kind,item,passed): checks.append({"kind":kind,"item":item,"passed":bool(passed)})
    for x in e.get("must_include",[]) or []: add("must_include",x,norm(x) in text)
    for x in e.get("must_not_include",[]) or []: add("must_not_include",x,norm(x) not in text)
    for key in ("required_actions","required_concepts"):
        for x in e.get(key,[]) or []: add(key,x,token_match(x,text,0.6))
    for x in e.get("forbidden_actions",[]) or []: add("forbidden_actions",x,not forbidden_hit(x,text))
    passed=sum(1 for x in checks if x["passed"]); score=passed/len(checks) if checks else 1.0
    threshold=(c.get("grading") or {}).get("pass_threshold",0.8)
    return {"eval_id":c["id"],"score":round(score,4),"threshold":threshold,"status":"passed" if score>=threshold else "failed","checks":checks}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("case"); ap.add_argument("response"); ap.add_argument("--json",action="store_true"); a=ap.parse_args()
    r=grade(yaml.safe_load(Path(a.case).read_text(encoding="utf-8")),Path(a.response).read_text(encoding="utf-8"))
    print(json.dumps(r,indent=2,ensure_ascii=False) if a.json else yaml.safe_dump(r,sort_keys=False,allow_unicode=True),end="" if not a.json else "\n")
    return 0 if r["status"]=="passed" else 1
if __name__=="__main__": raise SystemExit(main())
