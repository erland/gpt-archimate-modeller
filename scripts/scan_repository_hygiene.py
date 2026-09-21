#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse,json,re,sys
import yaml

TEMP_NAMES={".DS_Store","Thumbs.db"}
TEMP_SUFFIXES={".tmp",".swp",".log"}
BASE_GENERATED={"node_modules","__pycache__",".pytest_cache","target","dist","dist-ci","release-artifacts","build","coverage",".venv"}
SECRET_NAMES={".env",".env.production",".env.local"}
KEY_PATTERNS=[
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)\b(api[_-]?key|token|password|secret)\s*[:=]\s*['\"]?[^\s'\"]{8,}")
]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("root",nargs="?",default=".")
    ap.add_argument("--json",action="store_true")
    a=ap.parse_args()
    root=Path(a.root).resolve()
    registry=yaml.safe_load((root/"runtime/distribution-registry.yaml").read_text(encoding="utf-8"))
    hp=registry.get("hygiene",{})
    generated=set(hp.get("generated_roots",[]))|BASE_GENERATED
    forbidden=set(hp.get("forbidden_runtime_projection_paths",[]))
    allowed=set(hp.get("allowed_canonical_runtime_paths",[]))
    findings={"pass":[],"warning":[],"blocked":[]}

    for rel in sorted(forbidden):
        if rel in allowed: continue
        if (root/rel).exists():
            findings["blocked"].append({"path":rel,"reason":"generated runtime projection present in canonical source tree"})

    for p in root.rglob("*"):
        rel=p.relative_to(root).as_posix()
        if ".git" in p.parts: continue
        if p.is_dir() and (p.name in generated or rel in generated):
            findings["warning"].append({"path":rel,"reason":"generated/dependency directory present"})
            continue
        if not p.is_file(): continue
        if p.name in TEMP_NAMES or p.suffix in TEMP_SUFFIXES:
            findings["warning"].append({"path":rel,"reason":"temporary/local artifact"})
        if p.name in SECRET_NAMES:
            findings["blocked"].append({"path":rel,"reason":"secret/environment file candidate"})
        if p.suffix==".zip" and not any(rel.startswith(x+"/") for x in generated):
            findings["warning"].append({"path":rel,"reason":"archive in canonical source tree"})
        if p.stat().st_size<=1024*1024:
            try: text=p.read_text(encoding="utf-8")
            except Exception: text=None
            if text:
                for pat in KEY_PATTERNS:
                    if pat.search(text):
                        findings["blocked"].append({"path":rel,"reason":"credential/private-key pattern candidate"})
                        break

    if not findings["blocked"]:
        findings["pass"].append({"reason":"no blocking hygiene findings detected"})

    if a.json:
        print(json.dumps(findings,indent=2))
    else:
        for level in ["pass","warning","blocked"]:
            print(level.upper())
            for item in findings[level]:
                print("-",item.get("path",""),item["reason"])
    return 2 if findings["blocked"] else 0

if __name__=="__main__":
    raise SystemExit(main())
