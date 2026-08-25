# EA project format

## Logisk modell

Top-level:

- `format_version`
- `project`
- `model`
- `sources`
- `references`
- `extensions`
- `specializations`
- `issues`

## Fysisk split-layout

Canonical struktur:

```text
project.yaml
model/elements/*.yaml
model/relationships.yaml
sources/sources.yaml
sources/references.yaml
extensions/extensions.yaml
extensions/specializations.yaml
issues/issues.yaml
identity/id-counters.yaml
changes/index.yaml
versioning/history.yaml
queries/
reports/
views/
exports/
CHANGELOG.md
```

## Partitioner

Element delas per domän/lager:

- motivation
- strategy
- business
- application
- technology
- physical
- implementation-migration
- composite

Relationer ligger globalt eftersom de ofta korsar lager.

## Projektmetadata

`project.yaml` skiljer bland annat mellan:

- format_version
- package_layout_version
- project.model_version
- project.archimate_version

Dessa är separata versionsdimensioner.
