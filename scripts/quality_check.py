#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys, unicodedata, re, yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model_loader import load_model

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE = ROOT / "quality" / "profile.yaml"

def load_yaml(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))

def normalize_name(value):
    value = unicodedata.normalize("NFKC", value or "").casefold().strip()
    value = re.sub(r"[\W_]+", " ", value, flags=re.UNICODE)
    return " ".join(value.split())

def finding(results, profile, code, message, object_id=None, related_ids=None, recommendation=None):
    cfg = profile["checks"].get(code, {})
    if not cfg.get("enabled", True):
        return
    results.append({
        "severity": cfg.get("severity", "warning"),
        "code": code,
        "object_id": object_id,
        "related_ids": related_ids or [],
        "message": message,
        "recommendation": recommendation
    })

def run_quality(logical, profile):
    results=[]
    elements=logical["model"]["elements"]
    relationships=logical["model"]["relationships"]
    incoming={e["id"]:[] for e in elements}
    outgoing={e["id"]:[] for e in elements}
    for r in relationships:
        if r.get("source") in outgoing: outgoing[r["source"]].append(r)
        if r.get("target") in incoming: incoming[r["target"]].append(r)

    for e in elements:
        if not incoming[e["id"]] and not outgoing[e["id"]]:
            finding(results,profile,"Q-CONN-001",
                f"{e['type']} '{e.get('name')}' has no relationships.",e["id"],
                recommendation="Connect the element to relevant context or confirm intentional isolation.")

    support=set(profile.get("capability_support_relationships",[]))
    for e in elements:
        if e.get("type")!="Capability": continue
        rels=[r for r in incoming[e["id"]] if r.get("type") in support]
        if not rels:
            finding(results,profile,"Q-CAP-001",
                f"Capability '{e.get('name')}' has no incoming realization/support relationship.",e["id"],
                recommendation="Identify architecture elements that realize or support the capability.")
        elif all(r.get("type")=="Association" for r in rels):
            finding(results,profile,"Q-CAP-001",
                f"Capability '{e.get('name')}' is only connected through Association.",e["id"],
                recommendation="Use a more precise relationship when justified.")

    owner_types=set(profile.get("owner_recommended_types",[]))
    for e in elements:
        if e.get("type") in owner_types and not (e.get("properties") or {}).get("owner"):
            finding(results,profile,"Q-OWNER-001",
                f"{e['type']} '{e.get('name')}' has no owner.",e["id"],
                recommendation="Add owner when known and evidence it when required.")

    for e in elements:
        ev=e.get("evidence")
        if not ev or not ev.get("assertions"):
            finding(results,profile,"Q-EVID-001",
                f"{e['type']} '{e.get('name')}' has no evidence assertions.",e["id"],
                recommendation="Add source-backed evidence or explicitly retain uncertainty.")
        elif ev.get("confidence") in ("low","unknown"):
            finding(results,profile,"Q-EVID-002",
                f"{e['type']} '{e.get('name')}' has {ev.get('confidence')} confidence.",e["id"],
                recommendation="Seek stronger evidence.")

    for r in relationships:
        ev=r.get("evidence")
        if not ev or not ev.get("assertions"):
            finding(results,profile,"Q-REL-001",
                f"Relationship {r.get('type')} {r.get('source')} -> {r.get('target')} has no evidence.",r["id"],
                recommendation="Document why the relationship exists and cite evidence.")
        elif ev.get("confidence") in ("low","unknown"):
            finding(results,profile,"Q-EVID-002",
                f"Relationship {r.get('id')} has {ev.get('confidence')} confidence.",r["id"],
                recommendation="Seek stronger evidence.")

    src_by_id={s["id"]:s for s in logical.get("sources",[])}
    precise=set(profile.get("precise_reference_source_types",[]))
    for obj in elements+relationships:
        for a in (obj.get("evidence") or {}).get("assertions",[]):
            if a.get("reference_refs"): continue
            srcs=[src_by_id.get(x) for x in a.get("source_refs",[])]
            if any(s and s.get("type") in precise for s in srcs):
                finding(results,profile,"Q-SRC-001",
                    f"Evidence {a.get('id')} cites a locatable source but no exact reference.",obj["id"],
                    recommendation="Add page/section/line/table/anchor reference when available.")

    by_name={}
    alias_map={}
    for e in elements:
        n=normalize_name(e.get("name"))
        if n: by_name.setdefault((e.get("type"),n),[]).append(e["id"])
        for a in e.get("aliases",[]):
            an=normalize_name(a)
            if an: alias_map.setdefault(an,[]).append(e["id"])
    emitted=set()
    for (typ,n),ids in by_name.items():
        if len(ids)>1:
            key=tuple(sorted(ids))
            emitted.add(key)
            finding(results,profile,"Q-DUP-001",
                f"Possible duplicate {typ} elements with normalized name '{n}'.",ids[0],ids[1:],
                "Review evidence, aliases and external IDs before merging.")
    for a,ids in alias_map.items():
        ids=sorted(set(ids))
        key=tuple(ids)
        if len(ids)>1 and key not in emitted:
            finding(results,profile,"Q-DUP-001",
                f"Possible duplicate elements sharing alias '{a}'.",ids[0],ids[1:],
                "Review whether the alias refers to one canonical object.")

    types={e["type"] for e in elements}
    has_cap="Capability" in types
    tech_types={
        "DataObject","Node","Device","SystemSoftware","TechnologyCollaboration","TechnologyInterface",
        "Path","CommunicationNetwork","TechnologyFunction","TechnologyProcess","TechnologyInteraction",
        "TechnologyEvent","TechnologyService","Artifact"
    }
    has_apptech=any(t.startswith("Application") or t in tech_types for t in types)
    has_business_strategy=any(t.startswith("Business") or t in {
        "Product","Contract","Representation","Resource","Capability","ValueStream","CourseOfAction"
    } for t in types)

    if has_cap and not has_apptech:
        finding(results,profile,"Q-BAL-001",
            "Model contains capabilities but no Application/Technology realization layer.",
            recommendation="Add realization context if within model scope.")
    if has_apptech and not has_business_strategy:
        finding(results,profile,"Q-BAL-002",
            "Model contains Application/Technology elements but no Business/Strategy context.",
            recommendation="Add business/strategy context if within model scope.")

    score=float(profile["score"]["start"])
    deductions=profile["score"]["deductions"]
    for r in results:
        score-=float(deductions.get(r["severity"],0))
    score=max(float(profile["score"]["minimum"]),min(float(profile["score"]["maximum"]),score))
    counts={s:sum(1 for x in results if x["severity"]==s) for s in ("error","warning","info")}
    return results,score,counts

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("--profile",default=str(DEFAULT_PROFILE))
    ap.add_argument("--json",dest="json_out")
    args=ap.parse_args()
    logical,errors,_load=load_model(Path(args.project_dir))
    if errors:
        print("FAILED")
        for e in errors: print("-",e)
        return 1
    results,score,counts=run_quality(logical,load_yaml(args.profile))
    print("OK")
    print(f"Quality score: {score:.1f}/100")
    print(f"Warnings: {counts['warning']}")
    print(f"Info: {counts['info']}")
    for r in results:
        oid=f" [{r['object_id']}]" if r.get("object_id") else ""
        print(f"- {r['severity'].upper()} {r['code']}{oid}: {r['message']}")
    if args.json_out:
        Path(args.json_out).write_text(json.dumps({
            "status":"OK","quality_score":score,"counts":counts,"findings":results
        },indent=2,ensure_ascii=False),encoding="utf-8")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
