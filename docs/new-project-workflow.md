# New-project workflow – steg 26

Ett nytt EA-projekt skapas från den redan validerade canonical templaten
`templates/ea-project-split/`. Därmed använder nya och befintliga projekt samma fysiska kontrakt.

## Flöde

1. Läs init-spec.
2. Kopiera canonical template.
3. Sätt stabilt project id, namn och model version.
4. Töm modellinnehåll.
5. Lägg endast in explicit seed-data från användaren.
6. Initiera ID-counters.
7. Initiera version/change/migration histories.
8. Behåll standard extensions/specializations som default.
9. Kör technical validation.
10. Kör quality check.
11. Packa och validera ZIP om ZIP begärts.

## Minimal spec

```yaml
new_project:
  id: customs-enterprise-architecture
  name: Tullverkets enterprise architecture
```

Defaults: `model_version=0.1.0`, `language=sv`, `archimate_version=3.2`.

## Project ID

Lowercase kebab-case och stabilt över tid.

## Seed

Frivilligt:

```yaml
seed:
  elements: []
  relationships: []
  sources: []
  references: []
```

Seed måste själv följa samma evidence-, extension- och relationsregler som resten av modellen.
Generatorn försvagar inte valideringen för att acceptera ofullständig seed-data.

## Tom modell

Om inga fakta givits skapas inga element eller relationer, men alla canonical partitioner och filer finns.

## Standardprofiler

Standard extensions och specializations behålls som default. De kan stängas av i init-spec.

## Initial histories

`versioning/history.yaml` får initial model version.
`changes/index.yaml` och `migrations/history.yaml` initieras tomma.

## CLI

```bash
python scripts/new_project.py --spec examples/new-project/new-project.yaml --output-dir work
python scripts/new_project.py --spec examples/new-project/new-project.yaml --output-zip new-project.zip
```

Ett nytt projekt är färdigt först när technical validation och Project ZIP contract passerar.
