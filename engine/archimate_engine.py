#!/usr/bin/env python3
"""Portable CLI for the canonical ArchiMate YAML EA Python implementation."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMANDS = {
    "new-project": "new_project.py",
    "validate": "validate.py",
    "apply-changes": "apply_changes.py",
    "pack-project": "pack_project.py",
    "validate-project-zip": "validate_project_zip.py",
    "query": "query.py",
    "impact-analysis": "impact_analysis.py",
    "render-report": "render_report.py",
    "compile-view": "compile_view.py",
    "export-diagram": "export_diagram.py",
    "export-model-exchange": "export_model_exchange.py",
    "import-model-exchange": "import_model_exchange.py",
    "migrate-project": "migrate_project.py",
    "model-quality-report": "model_quality_report.py",
}

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print("Usage: python archimate_engine.py <command> [script arguments...]")
        print("Commands: " + ", ".join(sorted(COMMANDS)) + ", selftest")
        return 0 if len(sys.argv) > 1 else 2
    cmd = sys.argv[1]
    if cmd == "selftest":
        return subprocess.call([sys.executable, str(ROOT / "selftest.py"), *sys.argv[2:]])
    if cmd not in COMMANDS:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        return 2
    script = ROOT / "scripts" / COMMANDS[cmd]
    if not script.is_file():
        print(f"Missing engine script: {script.name}", file=sys.stderr)
        return 2
    return subprocess.call([sys.executable, str(script), *sys.argv[2:]])

if __name__ == "__main__":
    raise SystemExit(main())
