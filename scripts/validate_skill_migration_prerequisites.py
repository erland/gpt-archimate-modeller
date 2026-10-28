#!/usr/bin/env python3
"""Fail-fast, read-only prerequisite check for the planned modular Skills.

Not a substitute for transitive resource auditing or canonical engine lint.
"""
from pathlib import Path
import argparse
import json

REQUIRED = {
    "canonical_behavior": ["gpt/SYSTEM_INSTRUCTION.md"],
    "contracts": [
        "runtime/runtime-contract.json",
        "runtime/archimate-tool-contract.json",
        "runtime/distribution-registry.yaml",
    ],
    "project_workflow": [
        "scripts/project_control.py", "scripts/update_project.py",
        "scripts/new_project.py", "scripts/pack_project.py",
        "scripts/validate_project_zip.py", "scripts/safe_unpack.py",
    ],
    "modeling": [
        "scripts/apply_changes.py", "scripts/identity.py",
        "scripts/assemble_project.py", "scripts/validate.py",
        "schemas/ea-project.schema.json", "schemas/ea-package.schema.json",
    ],
    "analysis": [
        "scripts/query.py", "scripts/impact_analysis.py",
        "scripts/model_loader.py", "scripts/render_report.py",
        "scripts/compile_view.py", "scripts/export_diagram.py",
    ],
    "interoperability": [
        "scripts/import_model_exchange.py",
        "scripts/export_model_exchange.py",
        "scripts/assemble_project.py",
    ],
    "verification": [
        "scripts/run_tests.py", "scripts/validate_llm_evals.py",
        "tests/fixtures/fixture-catalog.yaml",
    ],
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--output")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    groups = {
        group: {
            "present": [p for p in paths if (root / p).is_file()],
            "missing": [p for p in paths if not (root / p).is_file()],
        }
        for group, paths in REQUIRED.items()
    }
    missing = [p for group in groups.values() for p in group["missing"]]
    report = {
        "schema_version": 1,
        "status": "pass" if not missing else "fail",
        "scope": "known critical files only",
        "groups": groups,
        "limitations": [
            "does not validate file contents",
            "does not resolve transitive schema, YAML, template or dynamic Python dependencies",
            "does not verify modular resource isolation or runtime parity",
        ],
    }
    payload = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 1 if missing else 0

if __name__ == "__main__":
    raise SystemExit(main())
