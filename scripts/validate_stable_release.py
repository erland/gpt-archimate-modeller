#!/usr/bin/env python3
from pathlib import Path
import argparse,re,yaml

ROOT=Path(__file__).resolve().parents[1]
EXPECTED="1.0.0"
RUNTIMES={"chat_zip","custom_gpt","claude_projects","opencode"}
RUNTIME_CONTRACTS={
    "runtime/runtime-contract.json",
    "runtime/archimate-tool-contract.json",
    "runtime/distribution-registry.yaml",
    "evals/runtime-parity-contract.yaml",
}
FORMAT_CONTRACTS={
    "package/project-zip-contract.yaml",
    "schemas/ea-project.schema.json",
    "schemas/ea-package.schema.json",
    "quality/profile.yaml",
    "migrations/registry.yaml",
    "migrations/mig_000002_0_1_to_0_2.py",
}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--distribution-version")
    args=ap.parse_args()
    errors=[]
    source_version=(ROOT/"VERSION").read_text(encoding="utf-8").strip()
    if source_version!=EXPECTED:
        errors.append(f"source VERSION must be {EXPECTED}, got {source_version}")
    if args.distribution_version and not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?",args.distribution_version):
        errors.append(f"invalid distribution version: {args.distribution_version}")

    manifest=yaml.safe_load((ROOT/"release"/"RELEASE-MANIFEST.yaml").read_text(encoding="utf-8"))["release"]
    if manifest.get("version")!=EXPECTED: errors.append("release manifest version mismatch")
    if manifest.get("tag")!="v"+EXPECTED: errors.append("release tag mismatch")
    if manifest.get("package_version")!=EXPECTED: errors.append("release package version mismatch")
    if manifest.get("plan_step_completed")!=48 or manifest.get("product_plan_complete") is not True:
        errors.append("product plan must be complete at 48/48")
    if manifest.get("target_project_format")!="0.2": errors.append("stable target format must be 0.2")
    if set(manifest.get("readable_project_formats",[]))!={"0.1","0.2"}:
        errors.append("stable readable format set mismatch")
    if manifest.get("migration_from_0_1")!="MIG-000002":
        errors.append("stable 0.1 migration mismatch")
    if set(manifest.get("active_runtimes",[]))!=RUNTIMES:
        errors.append("stable runtime set mismatch")
    if manifest.get("active_runtime_count")!=4:
        errors.append("stable runtime count must be four")
    if set(manifest.get("structurally_validated_runtime_contracts",[]))!=RUNTIME_CONTRACTS:
        errors.append("runtime contract set mismatch")
    if set(manifest.get("structurally_validated_format_contracts",[]))!=FORMAT_CONTRACTS:
        errors.append("format contract set mismatch")

    project=yaml.safe_load((ROOT/"project.yaml").read_text(encoding="utf-8"))
    p=project.get("project",{})
    if p.get("project_version")!=EXPECTED: errors.append("project version mismatch")
    if p.get("plan_step_completed")!=48: errors.append("project plan step mismatch")
    if p.get("status")!="release_ready": errors.append("project must be release_ready")
    arch=project.get("architecture",{})
    if arch.get("release_version")!=EXPECTED: errors.append("architecture release_version mismatch")
    if "release_candidate" in arch: errors.append("release_candidate must not remain in stable metadata")
    if arch.get("ea_project_format_version")!="0.2": errors.append("project format target mismatch")
    scope=project.get("scope",{})
    if scope.get("current")!="Step 48 - v1.0.0" or scope.get("next") is not None:
        errors.append("final scope mismatch")
    final=project.get("final_release",{})
    if final.get("version")!=EXPECTED or final.get("tag")!="v"+EXPECTED:
        errors.append("final_release metadata mismatch")
    if final.get("product_plan_complete") is not True:
        errors.append("final release must mark product plan complete")

    for rel in RUNTIME_CONTRACTS|FORMAT_CONTRACTS:
        if not (ROOT/rel).is_file(): errors.append(f"Missing release contract: {rel}")
    for rel in ["release/RELEASE-NOTES.md","release/RELEASE-CHECKLIST.md"]:
        if not (ROOT/rel).is_file(): errors.append(f"Missing stable release file: {rel}")

    readme=(ROOT/"README.md").read_text(encoding="utf-8")
    if "48 / 48" not in readme or "1.0.0" not in readme:
        errors.append("README does not present stable 1.0.0 / 48-of-48 status")

    if errors:
        print("FAILED")
        for e in errors: print("-",e)
        return 1
    print("OK")
    print("Stable source readiness: 1.0.0")
    if args.distribution_version:
        print(f"Distribution version from release tag: {args.distribution_version}")
    print("Product plan: 48/48")
    print("Runtime distributions: 4")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
