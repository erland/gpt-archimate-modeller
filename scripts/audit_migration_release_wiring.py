#!/usr/bin/env python3
"""Report whether legacy release wiring matches the GPT Byggaren 1.6.33 contract."""
from pathlib import Path
import json
import sys
import yaml

root=Path(__file__).resolve().parents[1]
config=yaml.safe_load((root/"gpt-project.yaml").read_text(encoding="utf-8"))
build=(root/".github/workflows/build-distributions.yml").read_text(encoding="utf-8")
release=(root/".github/workflows/release.yml").read_text(encoding="utf-8")
targets=config["build_system"]["targets"]
checks={
 "five_peer_targets":all(x in targets for x in ("chat","claude_project","claude_skills","opencode","plugin")),
 "custom_gpt_disabled":config["runtime"]["custom_gpt"]["enabled"] is False,
 "regular_build_uses_1_6_33":("gpt-byggaren-engine-1.6.33" in build),
 "tagged_release_uses_1_6_33":("gpt-byggaren-engine-1.6.33" in release or "build_distributions.py" in release),
 "tagged_release_legacy_validator_absent":("validate_release_assets_1_5.py" not in release),
}
blockers=[key for key,value in checks.items() if not value]
report={"migration_release_ready":not blockers,"checks":checks,"blockers":blockers,
 "note":"This is a source-level release wiring check, not a deployment or host runtime test."}
out=root/"release-wiring-audit-1.6.33.json"
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=False,indent=2))
# Audit is evidentiary and must not mask a release gate; separate release gate checks this report.
if not checks["five_peer_targets"] or not checks["custom_gpt_disabled"]:
    sys.exit(1)
