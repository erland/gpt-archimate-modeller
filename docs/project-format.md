# EA-projektets YAML-metamodell – format 0.1

## Syfte

Detta dokument definierar det första konkreta formatet för ett EA-projekt. Formatet är avsiktligt enkelt men tillräckligt strikt för att bli maskinellt validerbart.

## Top-level struktur

```yaml
format_version: "0.1"

project:
  id: example-ea
  name: Exempelarkitektur
  model_version: "0.1.0"
  archimate_version: "3.2"

model:
  elements: []
  relationships: []

sources: []
extensions: {}
specializations: {}
issues: []
```

## Principer

- ArchiMate-objekt ligger i `model`.
- Projektmetadata ligger i `project`.
- Källor ligger i `sources`.
- Organisationsspecifika properties deklareras i `extensions`.
- Specialiseringar deklareras i `specializations`.
- Öppna osäkerheter kan lagras i `issues`.
- GPT-specifik evidens lagras separat från ArchiMate-konceptet.

## Element

Minsta form:

```yaml
- id: APP-000001
  type: ApplicationComponent
  name: Ärendehanteringssystem
```

Rekommenderad form:

```yaml
- id: APP-000001
  type: ApplicationComponent
  name: Ärendehanteringssystem
  description: Systemstöd för handläggning.
  properties:
    lifecycle: active
    owner: Verksamhetsområde X
  evidence:
    status: document_confirmed
    confidence: high
    source_refs:
      - SRC-000001
  metadata:
    created: 2026-08-25
    updated: 2026-08-25
  aliases:
    - ÄHS
```

## Relationer

```yaml
- id: REL-000001
  type: Serving
  source: APP-000001
  target: STR-000001
```

`source` och `target` refererar alltid till stabila element-ID:n.

## Evidence

Evidence är inte ArchiMate utan projektmetadata.

Tillåtna statusvärden i format 0.1:

- `user_confirmed`
- `document_confirmed`
- `imported`
- `inferred`
- `unknown`

Confidence:

- `high`
- `medium`
- `low`
- `unknown`

## Sources

```yaml
sources:
  - id: SRC-000001
    type: document
    title: Plattformskatalog
    locator: avsnitt 4.2
```

I kommande steg fördjupas reglerna för källor och referenser.

## Extensions

Properties får användas fritt i element och relationer, men organisationsspecifika standardfält bör deklareras.

```yaml
extensions:
  lifecycle:
    description: Livscykelstatus
    value_type: enum
    allowed_values:
      - planned
      - active
      - phase_out
      - retired
    applies_to:
      - element
```

Detta gör att en validator senare kan kontrollera värden.

## Specializations

```yaml
specializations:
  Platform:
    base_type: Node
    description: Organisationsspecifik plattform
    allowed_relationships_inherit: true
```

Specialiserade element använder:

```yaml
specialization: Platform
```

men behåller en giltig ArchiMate-typ i `type`.

## Issues

Issues ger projektet möjlighet att bevara osäkerhet utan att tvinga fram ett felaktigt beslut.

```yaml
issues:
  - id: ISSUE-001
    type: possible_duplicate
    status: open
    element_refs:
      - APP-000001
      - APP-014
```

## Avgränsning i steg 3

Detta steg definierar formatets struktur men inte ännu:

- exakt ID-strategi,
- full provenance-modell,
- full source-modell,
- extension-regler,
- specialiseringsregler,
- exakt ArchiMate-relationsmatris,
- filindelning för stora projekt.

De kommer i efterföljande steg.

## Schema

Maskinläsbar definition finns i:

`schemas/ea-project.schema.json`
