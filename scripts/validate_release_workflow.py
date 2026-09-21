#!/usr/bin/env python3
from pathlib import Path
import re
import yaml

ROOT=Path(__file__).resolve().parents[1]
WF=ROOT/".github/workflows/release.yml"
BUILD_WF=ROOT/".github/workflows/build-distributions.yml"
SCRIPT=ROOT/"scripts/build_release.sh"

def main():
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
            "release-artifacts/*",
            "gh release upload",
            "actions/upload-artifact@v4",
        ]:
            if marker not in text:
                errors.append(f"release workflow missing {marker}")
        if "gh release create" in text:
            errors.append("release workflow must attach to an existing release, not create one")

    if BUILD_WF.is_file():
        text=BUILD_WF.read_text(encoding="utf-8")
        for marker in [
            "build_all_distributions.py",
            "validate_all_distributions.py",
            "distribution-build-manifest.json",
            "dist/*.zip",
        ]:
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
            "distribution-build-manifest.json",
            "SHA256SUMS.txt",
            "release-metadata.yaml",
            'VERSION="${TAG#v}"'.replace("\",""),
            "source_of_version",
            '"release_tag"',
            'validate_stable_release.py --distribution-version "$VERSION"',
        ]
        for marker in required:
            if marker not in text:
                errors.append(f"release script missing {marker}")

        if "FILE_VERSION=" in text or "does not match repository VERSION" in text:
            errors.append("release script still makes repository VERSION authoritative")

        for marker in [
            "archimate-yaml-ea-gpt-chat-v$VERSION.zip",
            "archimate-yaml-ea-gpt-custom-gpt-v$VERSION.zip",
            "archimate-yaml-ea-gpt-claude-projects-v$VERSION.zip",
            "archimate-yaml-ea-gpt-opencode-v$VERSION.zip",
        ]:
            if marker not in text:
                errors.append(f"release script missing runtime artifact {marker}")

        for runtime in ["chat_zip","custom_gpt","claude_projects","opencode"]:
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
