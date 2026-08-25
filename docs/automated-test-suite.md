# Automated test suite – steg 37

Kör hela sviten med `python scripts/run_tests.py` eller `sh scripts/test.sh`.

Suites: core_validation, reference_projects, invalid_fixtures, queries_reports_views, project_workflows, interoperability, change_architecture, analysis_quality.

Output: text, JSON, YAML. Exit codes: 0 pass, 1 test failure, 2 runner/config error.

Sviten är deterministisk, nätverksoberoende och återanvänder fixtures/reference projects från steg 36.
