# Kodstruktur och modulgränser

## Centrala script

### `assemble_project.py`

Ansvar:
- läser fysisk projektstruktur,
- bygger logical model,
- gör ingen modellmutation.

Ska hållas så deterministisk som möjligt.

### `validate.py`

Unified technical validation.

Samlar flera specialvalidatorer men ska inte duplicera deras semantik.

### `apply_changes.py`

Canonical change engine.

All faktisk modellmutation ska gå genom explicit operation-/change-set-semantik.

### `update_project.py`

Orchestrator för ZIP → staging → change → validation → ZIP.

Ska återanvända change engine, inte implementera alternativ mutationslogik.

### `query.py`

Read-only query engine.

Ska inte ändra modell eller persistenta arbetsobjekt.

### `render_report.py`

Renderer ovanpå query-resultat.

### `compile_view.py` / `export_diagram.py`

Kompilerar deklarativa views och exporterar draw.io/Mermaid.

### `architecture_states.py`

Validerar och resolverar baseline/target/transition membership.

### `impact_analysis.py`

Read-only grafanalys.

Resultat beskriver modellerad reachability, inte säker kausalitet.

### `quality_check.py`

Canonical dynamisk quality-motor.

### `model_quality_report.py`

Rapportering ovanpå exakt samma quality engine.

### `model_index.py` / `model_loader.py`

Derived read cache.

Måste alltid kunna falla tillbaka till YAML.

### `pack_project.py` / `validate_project_zip.py`

Deterministisk paketering och säker ZIP-validering.

## Designregel

Om två script behöver samma affärsregel:
1. lägg regeln i gemensam modul,
2. återanvänd den,
3. duplicera inte reglerna.

Det minskar risken för drift mellan CLI, GPT-runtime och tester.
