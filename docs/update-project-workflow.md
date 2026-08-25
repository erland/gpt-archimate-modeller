# Update-project workflow – steg 27

## Syfte

Steg 27 samlar hela förändringsflödet för ett befintligt EA-projekt i en kontrollerad ZIP→ZIP-pipeline.

## Flöde

```text
input ZIP
 → ZIP-contract + checksum
 → safe unpack
 → compatibility/migration gate
 → current project inspection
 → change-set ID/version gate
 → duplicate-candidate gate
 → dry-run via apply_changes.py
 → real apply via apply_changes.py
 → technical validation + quality + version history
 → atomic pack
 → final ZIP-contract validation
```

## Input

```bash
python scripts/update_project.py   project.zip   changes/CHG-000123.yaml   --output updated-project.zip
```

## Optimistic locking

Change set bör ange:

```yaml
expected_model_version: "0.3.0"
```

Mismatch stoppar uppdateringen innan apply.

## Migration

Migrerbart äldre projekt stoppas default med `migration_required`.

För att tillåta migration i staging-kopian:

```bash
--allow-migration
```

Migrationen sker fortfarande aldrig mot original-ZIP.

Unknown future format stoppas.

## Duplicate candidates

`add_element` kontrolleras mot befintlig modell.

Default är att stoppa vid kandidat och rapportera den.

```bash
--allow-duplicate-candidates
```

får endast användas när användaren uttryckligen har beslutat att det är ett separat objekt.

Ingen automatisk merge görs.

## Dry run

Samma etablerade change-set-motor används för både dry run och real apply:

```text
apply_changes.apply(..., dry_run=True)
apply_changes.apply(..., dry_run=False)
```

Update workflow duplicerar inte change-operationernas semantik.

## Post-validation

Efter apply krävs:

- technical validation utan errors,
- konsistent version history,
- final ZIP contract utan errors.

Quality warnings är non-blocking men returneras.

## Output

```yaml
update_project_result:
  status: updated
  project_id: ...
  change_set_id: CHG-000123
  model_version_before: "0.3.0"
  model_version_after: "0.3.1"
  computed_impact: patch
  validation:
    errors: 0
  quality:
    score: 94.0
  output_zip: updated-project.zip
```

## Failure safety

- input ZIP ändras aldrig,
- output publiceras först efter full validering,
- temporär workspace tas bort vid fel,
- felsteg rapporteras.

## Designprincip

`update_project.py` är en orchestrator ovanpå existerande, redan testade byggblock.
