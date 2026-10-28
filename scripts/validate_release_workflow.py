#!/usr/bin/env python3
from pathlib import Path
import re
import yaml

ROOT=Path(__file__).resolve().parents[1]
WF=ROOT/".github/workflows/release.yml"
BUILD_WF=ROOT/".github/workflows/build-distributions.yml"
SCRIPT=ROOT/"scripts/build_release.sh"

def validate_canonical_1_6_33():
    errors=[]
    release=WF.read_text(encoding="utf-8")
    build=BUILD_WF.read_text(encoding="utf-8")
    data=yaml.safe_load(release)
    trigger=data.get("on",data.get(True))
    if not isinstance(trigger,dict) or "workflow_dispatch" not in trigger or "published" not in (trigger.get("release",{}).get("types",[]) if isinstance(trigger.get("release"),dict) else []):
        errors.append("release must support published releases and manual dispatch")
    if data.get("permissions",{}).get("contents")!="write":
        errors.append("release must have contents write")
    for marker in ["Checkout released tag", "ref: ${{ steps.tag.outputs.tag }}",
                   "build_distributions_1_6_33.sh", "validate_release_assets_1_6_33.py",
                   "release-artifacts/DELIVERY-MANIFEST.json", "release-artifacts/SHA256SUMS.txt",
                   "gh release upload"]:
        if marker not in release: errors.append("release missing "+marker)
    for marker in ["build_distributions_1_6_33.sh","DELIVERY-MANIFEST.json",
                   "SHA256SUMS.txt","dist/*.zip"]:
        if marker not in build: errors.append("build missing "+marker)
    for marker in ["gpt-byggaren-engine-1.6.33.zip"]:
        if marker not in release or marker not in build: errors.append("pinned engine missing "+marker)
    if "gh release create" in release: errors.append("release creates a new GitHub release")
    for file in ["scripts/build_distributions_1_6_33.sh","scripts/validate_release_assets_1_6_33.py"]:
        if not (ROOT/file).is_file(): errors.append("missing "+file)
    if errors:
        print("FAILED")
        for error in errors: print("-",error)
        return 1
    print("OK: pinned 1.6.33 release and build workflows with exact assets")
    return 0

def main():
    if WF.is_file() and BUILD_WF.is_file() and "build_distributions_1_6_33.sh" in WF.read_text(encoding="utf-8"):
        return validate_canonical_1_6_33()
    errors=[]
    for p in [WF,BUILD_WF,SCRIPT]:
        if not p.is_file():
            errors.append(f"missing {p.relative_to(ROOT)}")

    if WF.is_file():
        text=WF.read_text(encoding="utf-8")
        data=yaml.safe_load(text)
        trigger=data.get("on",data.get(True))
        release=(trigger or {}).get("release",{}) if isinstance(trigger,dict) else {}
        types=release.get("types",[]) if isinstance(release,dict) else []
        if "published" not in types:
            errors.append("release workflow must trigger on release: published")
        if isinstance(trigger,dict) and "push" in trigger:
            errors.append("release workflow must not use tag push as primary trigger")
        if not isinstance(trigger,dict) or "workflow_dispatch" not in trigger:
            errors.append("release workflow_dispatch fallback missing")
        if data.get("permissions",{}).get("contents")!="write":
            errors.append("contents: write missing")
        for marker in [
            "github.event.release.tag_name",
            "Checkout released tag",
            "ref: ${{ steps.tag.outputs.tag }}",
            "bash scripts/build_release.sh",
            "validate_release_assets_1_5.py",
            "gh release upload",
            "actions/upload-artifact@v4",
        ]:
            if marker not in text:
                errors.append(f"release workflow missing {marker}")
        if "gh release create" in text:
            errors.append("release workflow must attach to an existing release, not create one")

    if BUILD_WF.is_file():
        text=BUILD_WF.read_text(encoding="utf-8")
        for marker in ["build_all_distributions.py","validate_all_distributions.py","distribution-build-manifest.json","dist/*.zip"]:
            if marker not in text:
                errors.append(f"build workflow missing {marker}")
        if re.search(r"(?m)^\s*release:\s*$",text):
            errors.append("build-distributions must not also trigger on release")
        if "release-assets:" in text:
            errors.append("duplicate release-assets job remains in build-distributions")

    if SCRIPT.is_file():
        text=SCRIPT.read_text(encoding="utf-8")
        required=[
            "build_all_distributions.py",
            "validate_all_distributions.py",
            "run_runtime_instruction_adherence.py",
            "validate_runtime_parity.py",
            "validate_gpt_builder_1_5_contract.py",
            "validate_openai_plugin_1_5_assessment.py",
            "validate_chat_gpt_builder_1_5.py",
            "validate_custom_gpt_builder_1_5.py",
            "validate_claude_gpt_builder_1_5.py",
            "validate_opencode_gpt_builder_1_5.py",
            "validate_release_assets_1_5.py",
            "distribution-build-manifest.json",
            "SHA256SUMS.txt",
            "release-metadata.yaml",
            'VERSION="${TAG#v}"',
            "source_of_version",
            '"release_tag"',
            'validate_stable_release.py --distribution-version "$VERSION"',
        ]
        for marker in required:
            if marker not in text:
                errors.append(f"release script missing {marker}")

        if "FILE_VERSION=" in text or "does not match repository VERSION" in text:
            errors.append("release script still makes repository VERSION authoritative")

        if "runtime/distribution-registry.yaml" not in (ROOT/"scripts/validate_release_assets_1_5.py").read_text(encoding="utf-8"):
            errors.append("release asset validator must derive runtime assets from distribution registry")

        for runtime in ["chat_zip","custom_gpt","claude_projects","opencode","openai_plugin"]:
            if f"--runtime {runtime}" not in text:
                errors.append(f"release adherence missing {runtime}")

        if re.search(r'VERSION\s*=\s*"[0-9]+\.[0-9]+\.[0-9]+',text):
            errors.append("hardcoded release version found")

    if errors:
        print("FAILED")
        for e in errors:
            print("-",e)
        return 1
    print("OK")
    print("Release-published workflow uses GitHub Release tag as distribution version source")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
