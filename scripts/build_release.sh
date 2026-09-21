#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
PYTHON="${PYTHON:-python3}"
TAG="${RELEASE_TAG:-${1:-}}"
if [[ -z "$TAG" ]]; then echo "ERROR: release tag required"; exit 2; fi
if [[ ! "$TAG" =~ ^v[0-9]+\.[0-9]+\.[0-9]+(-[0-9A-Za-z.-]+)?(\+[0-9A-Za-z.-]+)?$ ]]; then
  echo "ERROR: invalid SemVer release tag: $TAG"; exit 2
fi
VERSION="${TAG#v}"
FILE_VERSION="$(tr -d '[:space:]' < VERSION)"
if [[ "$FILE_VERSION" != "$VERSION" ]]; then
  echo "ERROR: release tag version $VERSION does not match repository VERSION $FILE_VERSION"
  exit 2
fi
ARTIFACT_DIR="${ARTIFACT_DIR:-release-artifacts}"
MANIFEST="$ARTIFACT_DIR/distribution-build-manifest.json"
CHECKSUMS="$ARTIFACT_DIR/SHA256SUMS.txt"
METADATA="$ARTIFACT_DIR/release-metadata.yaml"
rm -rf "$ARTIFACT_DIR"; mkdir -p "$ARTIFACT_DIR"

$PYTHON scripts/run_tests.py --format text
$PYTHON scripts/validate_llm_evals.py
$PYTHON scripts/validate_user_docs.py
$PYTHON scripts/validate_developer_docs.py
$PYTHON scripts/validate_reference_projects.py
$PYTHON scripts/validate_fixture_catalog.py
$PYTHON scripts/validate_runtime_contract.py
$PYTHON scripts/validate_archimate_tool_contract.py
$PYTHON scripts/validate_distribution_registry.py
$PYTHON scripts/scan_repository_hygiene.py .
$PYTHON scripts/validate_stable_release.py

$PYTHON scripts/build_all_distributions.py --version "$VERSION" --output-dir "$ARTIFACT_DIR"
$PYTHON scripts/validate_all_distributions.py --manifest "$MANIFEST"

CHAT="$ARTIFACT_DIR/archimate-yaml-ea-gpt-chat-v$VERSION.zip"
CUSTOM="$ARTIFACT_DIR/archimate-yaml-ea-gpt-custom-gpt-v$VERSION.zip"
CLAUDE="$ARTIFACT_DIR/archimate-yaml-ea-gpt-claude-projects-v$VERSION.zip"
OPENCODE="$ARTIFACT_DIR/archimate-yaml-ea-gpt-opencode-v$VERSION.zip"

$PYTHON scripts/run_runtime_instruction_adherence.py --contract evals/runtime-parity-contract.yaml --runtime chat_zip --artifact "$CHAT"
$PYTHON scripts/run_runtime_instruction_adherence.py --contract evals/runtime-parity-contract.yaml --runtime custom_gpt --artifact "$CUSTOM"
$PYTHON scripts/run_runtime_instruction_adherence.py --contract evals/runtime-parity-contract.yaml --runtime claude_projects --artifact "$CLAUDE"
$PYTHON scripts/run_runtime_instruction_adherence.py --contract evals/runtime-parity-contract.yaml --runtime opencode --artifact "$OPENCODE"
$PYTHON scripts/validate_runtime_parity.py \
  --contract evals/runtime-parity-contract.yaml \
  --runtime-contract runtime/runtime-contract.json \
  --tool-contract runtime/archimate-tool-contract.json \
  --chat "$CHAT" --custom "$CUSTOM" --claude "$CLAUDE" --opencode "$OPENCODE"

$PYTHON - "$MANIFEST" "$CHECKSUMS" "$METADATA" "$TAG" "$VERSION" <<'PY'
from pathlib import Path
import hashlib,json,sys,yaml
manifest_path=Path(sys.argv[1]); checksums=Path(sys.argv[2]); metadata=Path(sys.argv[3])
tag=sys.argv[4]; version=sys.argv[5]
manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
arts=[]; lines=[]
for runtime,path_text in manifest["artifacts"].items():
    p=Path(path_text)
    if not p.is_absolute(): p=Path.cwd()/p
    digest=hashlib.sha256(p.read_bytes()).hexdigest()
    arts.append({"runtime":runtime,"file":p.name,"sha256":digest})
    lines.append(f"{digest}  {p.name}")
checksums.write_text("\n".join(lines)+"\n",encoding="utf-8")
metadata.write_text(yaml.safe_dump({
    "name":"ArchiMate YAML EA GPT","version":version,"tag":tag,
    "source_of_version":"release_tag",
    "distribution_registry":"runtime/distribution-registry.yaml",
    "runtime_count":len(arts),"artifacts":arts,"checksums":checksums.name
},sort_keys=False,allow_unicode=True),encoding="utf-8")
PY
echo "PASS: release artifacts built for $TAG"
