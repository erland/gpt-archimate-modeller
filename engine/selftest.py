#!/usr/bin/env python3
"""End-to-end verification from an unpacked standalone engine ZIP."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def run(*args):
    result = subprocess.run([sys.executable, str(ROOT / "archimate_engine.py"), *map(str, args)],
                            text=True, capture_output=True, cwd=ROOT)
    if result.returncode:
        raise RuntimeError(f"{' '.join(map(str,args))}: {result.stdout}\n{result.stderr}")
    return result.stdout

def main():
    import yaml
    with tempfile.TemporaryDirectory(prefix="archimate-engine-selftest-") as tmp:
        tmp = Path(tmp)
        run("new-project", "--id", "engine-test", "--name", "Engine Test",
            "--output-dir", tmp)
        project = tmp / "engine-test"
        assert (project / "project.yaml").is_file()
        run("validate", project)
        query = tmp / "query.yaml"
        query.write_text(yaml.safe_dump({"query":{"id":"all","select":"elements"}}), encoding="utf-8")
        output = json.loads(run("query", project, query, "--json"))
        assert output["query_result"]["count"] == 0
        change = tmp / "change.yaml"
        change.write_text(yaml.safe_dump({"change_set":{
            "id":"CHG-000001","title":"Add application","created":"2026-10-28",
            "expected_model_version":"0.1.0",
            "operations":[{"op":"add_element","element":{
                "id":"APP-000001","type":"ApplicationComponent","name":"Engine Test Application"}}]
        }}), encoding="utf-8")
        run("apply-changes", project, change, "--dry-run")
        run("apply-changes", project, change)
        run("validate", project)
        output = json.loads(run("query", project, query, "--json"))
        assert output["query_result"]["count"] == 1
        xml = tmp / "model.xml"
        run("export-model-exchange", project, "--output", xml)
        assert xml.is_file()
        result = json.loads(run("import-model-exchange", xml, "--preview", "--json"))
        assert result["import_preview"]["element_count"] == 1
        archive = tmp / "project.zip"
        run("pack-project", project, archive)
        run("validate-project-zip", archive)
        print("PASS: standalone engine new-project, validate, query, dry-run/apply, export/import, ZIP")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
