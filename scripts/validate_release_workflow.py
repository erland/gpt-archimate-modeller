#!/usr/bin/env python3
from pathlib import Path
import re,yaml
ROOT=Path(__file__).resolve().parents[1]
WF=ROOT/".github/workflows/release.yml"
BUILD_WF=ROOT/".github/workflows/build-distributions.yml"
SCRIPT=ROOT/"scripts/build_release.sh"
def main():
    errors=[]
    for p in [WF,BUILD_WF,SCRIPT]:
        if not p.is_file(): errors.append(f"missing {p.relative_to(ROOT)}")
    if WF.is_file():
        text=WF.read_text(encoding="utf-8"); data=yaml.safe_load(text); trigger=data.get("on",data.get(True))
        push=(trigger or {}).get("push",{}) if isinstance(trigger,dict) else {}
        tags=push.get("tags",[]) if isinstance(push,dict) else []
        if "v*.*.*" not in tags and "v*" not in tags: errors.append("release tag trigger missing")
        if not isinstance(trigger,dict) or "workflow_dispatch" not in trigger: errors.append("release workflow_dispatch missing")
        if data.get("permissions",{}).get("contents")!="write": errors.append("contents: write missing")
        for m in ["bash scripts/build_release.sh","release-artifacts/*","gh release","actions/upload-artifact@v4"]:
            if m not in text: errors.append(f"release workflow missing {m}")
    if BUILD_WF.is_file():
        text=BUILD_WF.read_text(encoding="utf-8")
        for m in ["build_all_distributions.py","validate_all_distributions.py","distribution-build-manifest.json","dist/*.zip"]:
            if m not in text: errors.append(f"build workflow missing {m}")
        if "both distributions" in text.lower() or "båda" in text.lower(): errors.append("two-runtime wording remains")
    if SCRIPT.is_file():
        text=SCRIPT.read_text(encoding="utf-8")
        for m in ["build_all_distributions.py","validate_all_distributions.py","run_runtime_instruction_adherence.py","validate_runtime_parity.py","distribution-build-manifest.json","SHA256SUMS.txt","release-metadata.yaml",'VERSION="${TAG#v}"'.replace("\",""),"source_of_version","distribution_registry"]:
            if m not in text: errors.append(f"release script missing {m}")
        for m in ["archimate-yaml-ea-gpt-chat-v$VERSION.zip","archimate-yaml-ea-gpt-custom-gpt-v$VERSION.zip","archimate-yaml-ea-gpt-claude-projects-v$VERSION.zip","archimate-yaml-ea-gpt-opencode-v$VERSION.zip"]:
            if m not in text: errors.append(f"release script missing runtime artifact {m}")
        for rt in ["chat_zip","custom_gpt","claude_projects","opencode"]:
            if f"--runtime {rt}" not in text: errors.append(f"release adherence missing {rt}")
        for flag in ["--chat","--custom","--claude","--opencode"]:
            if flag not in text: errors.append(f"release parity missing {flag}")
        if re.search(r'VERSION\s*=\s*"[0-9]+\.[0-9]+\.[0-9]+',text): errors.append("hardcoded release version found")
    if errors:
        print("FAILED"); [print("-",e) for e in errors]; return 1
    print("OK"); print("Four-runtime release workflow validated"); return 0
if __name__=="__main__": raise SystemExit(main())
