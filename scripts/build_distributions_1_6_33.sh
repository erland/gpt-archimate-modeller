#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
VERSION="${1:?version required}"
ENGINE_ROOT="${GPT_BUILDER_ENGINE_ROOT:-/tmp/gpt-byggaren-engine-1.6.33}"
test -f "$ENGINE_ROOT/scripts/build_distributions.py"
# The engine archives the project tree. Never carry previous build or release
# outputs into a new project ZIP (including staged release-artifacts/*.zip).
rm -rf -- dist build release-artifacts
mkdir -p schemas templates
for s in capability-contract.schema.json skill-contract.schema.json project-status.schema.json; do
  cp "$ENGINE_ROOT/schemas/$s" "schemas/$s"
done
for t in START-HERE.chat.md.tpl README.claude.md.tpl README.opencode.md.tpl README.plugin.md.tpl; do
  cp "$ENGINE_ROOT/templates/$t" "templates/$t"
done
# Override generic GPT Byggaren README templates with ArchiMate-specific instructions.
cp templates/README.archimate.opencode.md.tpl templates/README.opencode.md.tpl
cp templates/README.archimate.plugin.md.tpl templates/README.plugin.md.tpl
cp templates/START-HERE.archimate.chat.md.tpl templates/START-HERE.chat.md.tpl
python scripts/generate_skill_template_bundle.py
python "$ENGINE_ROOT/scripts/build_distributions.py" --project-root . --version "$VERSION"
python "$ENGINE_ROOT/scripts/validate_distributions.py" --project-root .
python scripts/add_runtime_requirements.py --version "$VERSION"
python scripts/build_archimate_engine_zip.py --version "$VERSION"
python scripts/verify_project_archive_hygiene.py --version "$VERSION"
python scripts/verify_skill_python_closure.py
python scripts/verify_migration_skill_archives.py
python scripts/smoke_test_packaged_skill_data.py
python scripts/smoke_test_packaged_project_flow.py

python scripts/verify_archimate_engine_zip.py --version "$VERSION"
