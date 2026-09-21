#!/usr/bin/env python3
from pathlib import Path
import hashlib,yaml
ROOT=Path(__file__).resolve().parents[1]
EXPECTED_RC="1.0.0-rc.6"
EXPECTED_PACKAGE="0.45.0"
RUNTIME_CONTRACTS={
    "runtime/runtime-contract.json",
    "runtime/archimate-tool-contract.json",
    "runtime/distribution-registry.yaml",
    "evals/runtime-parity-contract.yaml",
}
def sh(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()
def main():
    errors=[]
    rc=yaml.safe_load((ROOT/"release"/"RC-MANIFEST.yaml").read_text(encoding="utf-8"))["release_candidate"]
    if rc["version"]!=EXPECTED_RC: errors.append("Unexpected RC version")
    if rc["package_version"]!=EXPECTED_PACKAGE: errors.append("Unexpected package version")
    if rc["plan_step_completed"]!=45: errors.append("Unexpected completed product-plan step")
    if rc.get("runtime_migration_step_completed")!=57: errors.append("Runtime migration step mismatch")
    if rc.get("runtime_migration_complete") is not True: errors.append("Runtime migration must be complete")
    if rc.get("active_runtime_count")!=4: errors.append("Expected four active runtimes")
    for x in rc["canonical_contract_hashes"]:
        p=ROOT/x["path"]
        if not p.exists(): errors.append(f"Missing contract file: {x['path']}")
        elif sh(p)!=x["sha256"]: errors.append(f"Contract hash mismatch: {x['path']}")
    structural=set(rc.get("structurally_validated_runtime_contracts",[]))
    if structural!=RUNTIME_CONTRACTS: errors.append("Runtime structural contract set mismatch")
    for rel in RUNTIME_CONTRACTS:
        if not (ROOT/rel).is_file(): errors.append(f"Missing runtime contract: {rel}")
    project=yaml.safe_load((ROOT/"project.yaml").read_text(encoding="utf-8"))
    if project["project"]["project_version"]!=EXPECTED_PACKAGE: errors.append("project.yaml version mismatch")
    if project["project"]["plan_step_completed"]!=45: errors.append("project.yaml product-plan step mismatch")
    if project["architecture"].get("release_candidate")!=EXPECTED_RC: errors.append("project.yaml RC mismatch")
    mig=project.get("runtime_migration",{})
    if mig.get("track_status")!="complete" or mig.get("last_completed_step")!=57: errors.append("runtime migration status mismatch")
    if EXPECTED_RC not in (ROOT/"README.md").read_text(encoding="utf-8"): errors.append("README missing RC version")
    if errors:
        print("FAILED")
        for e in errors: print("-",e)
        return 1
    print("OK")
    print(f"Release candidate: {EXPECTED_RC}")
    print(f"Hashed legacy canonical contracts: {len(rc['canonical_contract_hashes'])}")
    print("Runtime contracts are structurally validated by dedicated CI validators")
    print("Product plan advanced to 45/48; runtime migration remains complete at step 57")
    return 0
if __name__=="__main__":
    raise SystemExit(main())
