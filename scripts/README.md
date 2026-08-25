# scripts

## Steg 2

`validate_metamodel.py` verifierar den interna konsistensen i den maskinläsbara ArchiMate-profilen.

Kör:

```bash
python scripts/validate_metamodel.py
```

Scriptet kräver Python och PyYAML.


## Steg 3

`validate_project.py` validerar ett EA-projekt mot `schemas/ea-project.schema.json` och kontrollerar även:

- unika element-ID:n,
- unika relations-ID:n,
- source/target-referenser,
- source_refs i evidence.

Exempel:

```bash
python scripts/validate_project.py examples/ea-project-minimal.yaml
```

Om paketet `jsonschema` finns installerat används full JSON Schema-validering. Annars körs en enklare fallback plus referenskontroller.


## Steg 4

### assemble_project.py

Läser ett uppdelat projektpaket och bygger den logiska modellrepresentationen från steg 3.

```bash
python scripts/assemble_project.py examples/ea-project-split /tmp/assembled.yaml
```

### validate_package.py

Validerar manifest, filstruktur, sammansatt schema och referensintegritet.

```bash
python scripts/validate_package.py examples/ea-project-split
```


## Steg 5

### identity.py

Gemensamma funktioner för:

- normalisering av namn,
- typfamilj → prefix,
- ID-generering.

### allocate_id.py

Allokerar nästa stabila ID från projektets räknarfil.

```bash
python scripts/allocate_id.py path/to/id-counters.yaml APP
```

### find_duplicate_candidates.py

Identifierar starka dubblettkandidater utifrån normaliserat namn och delade alias.

```bash
python scripts/find_duplicate_candidates.py examples/ea-project-split
```


## Steg 6

### validate_evidence.py

Validerar provenance/evidence-regler som går utöver JSON Schema:

- unika EV-ID:n,
- source references,
- inferred/derived måste ha reason,
- document_confirmed måste ha explicit assertion,
- user_confirmed måste ha user_statement assertion.

```bash
python scripts/validate_evidence.py examples/ea-project-split
```


## Steg 7

### validate_sources.py

Validerar source- och reference-specifika regler:

- origin-krav,
- reference → source-integritet,
- line_range,
- dubbletter av source+locator.

```bash
python scripts/validate_sources.py examples/ea-project-split
```


## Steg 8

### validate_extensions.py

Validerar organisationsspecifika properties mot deklarerad extensionprofil.

```bash
python scripts/validate_extensions.py examples/ea-project-split strict
```

Kontrollerar bland annat:

- okända properties,
- value types,
- enum-värden,
- applies_to,
- evidence_required,
- required fields,
- deprecated extensions.


## Steg 10 – gemensam validator

Använd i första hand:

```bash
python scripts/validate.py examples/ea-project-split
```

För fullständigt täckningskrav på den portabla relationsmatrisen:

```bash
python scripts/validate.py examples/ea-project-split --strict-relationships
```

De äldre specialvalidatorerna finns kvar som diagnostiska verktyg.


## Steg 11

```bash
python scripts/quality_check.py examples/ea-project-split
python scripts/check_project.py examples/ea-project-split
```

`quality_check.py` analyserar semantisk kvalitet. `check_project.py` kör både teknisk och semantisk kontroll.


## Steg 12 – säkra förändringar

```bash
python scripts/apply_changes.py <projektkatalog> <change-set.yaml> --dry-run
python scripts/apply_changes.py <projektkatalog> <change-set.yaml>
```

Change set valideras mot projektets nuläge och appliceras transactionellt på en temporär kopia innan resultatet skrivs tillbaka.


## Steg 14 – query engine

```bash
python scripts/validate_query.py queries/applications.yaml
python scripts/query.py examples/ea-project-split queries/applications.yaml
```


## Steg 15 – report-format

Validera report:

```bash
python scripts/validate_report.py reports/application-overview.yaml
```

Förhandsgranska reportens query-resultat:

```bash
python scripts/report_preview.py examples/ea-project-split reports/application-overview.yaml
```

Full Markdown/CSV-rendering kommer i steg 16.


## Steg 16 – report engine

Markdown:

```bash
python scripts/render_report.py examples/ea-project-split reports/application-overview.yaml   --format markdown --output exports/application-overview.md
```

CSV:

```bash
python scripts/render_report.py examples/ea-project-split reports/application-overview.yaml   --format csv --output-dir exports
```


## Steg 17 – view-format

Validera:

```bash
python scripts/validate_view.py views/capability-realization.yaml
```

Kompilera till ett neutralt view-resultat:

```bash
python scripts/compile_view.py examples/ea-project-split views/capability-realization.yaml
```

Steg 18 använder view-resultatet för första diagram/exportformatet.


## Steg 18 – diagram-export

draw.io:

```bash
python scripts/export_diagram.py   examples/ea-project-split   views/capability-realization.yaml   --format drawio   --output exports/capability-realization.drawio
```

Mermaid:

```bash
python scripts/export_diagram.py   examples/ea-project-split   views/capability-realization.yaml   --format mermaid   --output exports/capability-realization.mmd
```


## Steg 19 – ArchiMate Model Exchange

Export:

```bash
python scripts/export_model_exchange.py   examples/ea-project-split   --output exports/model-exchange.xml
```

Intern strukturell validering:

```bash
python scripts/validate_model_exchange.py exports/model-exchange.xml
```


## Steg 20 – Model Exchange import

Preview:

```bash
python scripts/import_model_exchange.py   examples/model-exchange/example-enterprise-architecture.xml   --preview
```

Skapa staging-projekt:

```bash
python scripts/import_model_exchange.py   examples/model-exchange/example-enterprise-architecture.xml   --output-project imported-project
```

Direkt merge till ett befintligt EA-projekt stöds inte i version 0.1.


## Steg 21 – Project ZIP contract

```bash
python scripts/generate_package_manifest.py examples/ea-project-split
python scripts/pack_project.py examples/ea-project-split example-project.zip
python scripts/validate_project_zip.py example-project.zip
```


## Steg 22 – project control

Gemensam CLI:

```bash
python scripts/project_control.py inspect-zip project.zip
python scripts/project_control.py unpack project.zip --output-dir workspace
python scripts/project_control.py inspect-project workspace/project
python scripts/project_control.py validate-project workspace/project
python scripts/project_control.py pack workspace/project --output project-updated.zip
python scripts/project_control.py roundtrip project.zip
```

`safe_unpack.py` används för explicit path-safe extraction.


## Steg 23 – project migration

```bash
python scripts/migrate_project.py <project> --compatibility
python scripts/migrate_project.py <project> --plan
python scripts/migrate_project.py <project> --preview
python scripts/migrate_project.py <project> --apply
```


## Steg 24 – GPT system instruction

Validera instruktionerna:

```bash
python scripts/validate_gpt_instruction.py
```

Filer:

- `gpt/SYSTEM_INSTRUCTION.md`
- `gpt/CUSTOM_GPT_INSTRUCTION.txt`
- `gpt/runtime-policy.yaml`


## Steg 25 – GPT Knowledge structure

Validera Knowledge:

```bash
python scripts/validate_knowledge.py
```

Index:

- `knowledge/knowledge-index.yaml`
- `knowledge/routing.yaml`


## Steg 26 – new-project workflow

```bash
python scripts/new_project.py --spec examples/new-project/new-project.yaml --output-dir work
python scripts/new_project.py --spec examples/new-project/new-project.yaml --output-zip new-project.zip
```


## Steg 27 – update-project workflow

```bash
python scripts/update_project.py   project.zip   changes/CHG-000123.yaml   --output updated-project.zip
```

Valfria explicita overrides:

- `--allow-migration`
- `--allow-duplicate-candidates`


## Steg 28 – conflict/duplicate handling

Detektera:

```bash
python scripts/detect_conflicts.py <project>
python scripts/detect_conflicts.py <project> --incoming incoming.yaml
```

Validera/översätt resolution:

```bash
python scripts/resolve_conflict.py examples/conflicts/keep-separate.yaml
```


## Steg 29 – issues/observations

```bash
python scripts/validate_issues.py issues/issues.yaml --project-dir .
python scripts/promote_observation.py issues/issues.yaml OBS-000001 ISS-000020
```


## Steg 30 – standard report library

`reports/standard-library.yaml` och `reports/standard/*.yaml`.

```bash
python scripts/validate_report_library.py
```


## Steg 31 – standard views

`views/standard-library.yaml`, `views/standard/*.yaml`.

```bash
python scripts/validate_view_library.py
```


## Steg 32 – baseline/target/transition

```bash
python scripts/architecture_states.py <project> --validate
python scripts/architecture_states.py <project> --resolve STA-000003
```


## Steg 33 – time/lifecycle

```bash
python scripts/validate_temporal.py <project>
```

Standardrapport: `reports/standard/lifecycle-overview.yaml`.


## Steg 34 – impact analysis

```bash
python scripts/impact_analysis.py examples/ea-project-split   --seed STR-000001   --direction incoming   --max-depth 3   --format markdown
```

Kan även seedas från `--change-set` eller `--from-state/--to-state`.


## Steg 35 – model quality report

```bash
python scripts/model_quality_report.py examples/ea-project-split --format markdown
python scripts/model_quality_report.py examples/ea-project-split --format csv
```

Dynamisk rapportdefinition:

```text
reports/dynamic/model-quality-report.yaml
```


## Steg 36 – fixtures/reference projects

```bash
python scripts/validate_reference_projects.py
python scripts/validate_fixture_catalog.py
```


## Steg 37 – automated test suite

```bash
python scripts/run_tests.py
python scripts/run_tests.py --format json --output test-result.json
```


## Steg 38 – LLM evals

```bash
python scripts/validate_llm_evals.py
python scripts/run_llm_evals.py --responses-dir evals/grader-fixtures/passing
```


## Steg 39 – large ZIP robustness

```bash
python scripts/generate_large_fixture.py /tmp/large-project --elements 5000 --relationships 4999
python scripts/pack_project.py /tmp/large-project /tmp/large.zip
python scripts/validate_project_zip.py /tmp/large.zip
```


## Steg 40 – model index

Bygg/checka index:

```bash
python scripts/model_index.py <project>
python scripts/model_index.py <project> --check
```

`pack_project.py` lägger automatiskt ett färskt `MODEL-INDEX.json` i projekt-ZIP.


## Steg 41 – user docs

Validera användardokumentationen:

```bash
python scripts/validate_user_docs.py
```

Ingång:

```text
docs/user/index.md
```


## Steg 42 – developer docs

```bash
python scripts/validate_developer_docs.py
```

Ingång:

```text
docs/developer/index.md
```


## Steg 43 – first RC package

```bash
python scripts/validate_release_candidate.py
```

RC-filer:
- `release/RC-NOTES.md`
- `release/RC-CHECKLIST.md`
- `release/RC-MANIFEST.yaml`


## Steg 44 – end-to-end GPT test

```bash
python scripts/run_e2e_gpt_test.py --output-dir /tmp/e2e
```
