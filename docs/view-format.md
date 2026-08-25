# View-format – steg 17

## Syfte

View-formatet beskriver **vilket modellurval som ska visualiseras och vilka presentationshintar som gäller**.

Separation:

- model = arkitekturkunskap,
- query = urval/traversal,
- report = text/tabellpresentation,
- view = diagram-/visualiseringsdefinition.

## Grundstruktur

```yaml
view:
  id: capability-realization
  title: Capability realization
  source:
    query: queries/capability-realization-view.yaml
  include_relationships: between_selected
  layout:
    direction: left_to_right
```

## Source

Version 0.1 använder sparad query:

```yaml
source:
  query: queries/...
```

Queryn ska returnera element som ska ingå i vyn.

## Relationer

`include_relationships`:

- `between_selected`
- `all_touching_selected`
- `none`

### between_selected

Endast relationer där både source och target ingår i valda element.

### all_touching_selected

Relationer där minst ena ändpunkten ingår.

När relationen drar in ett nytt element ska det elementet inte automatiskt läggas till i vyn i version 0.1; relationen filtreras därför i praktiken bort om ena ändpunkten saknas.

## Explicit elements

View kan komplettera query-resultatet:

```yaml
include_elements:
  - STR-000001
```

## Exclude

```yaml
exclude_elements:
  - APP-000999

exclude_relationships:
  - REL-000123
```

## Layout hints

Version 0.1 stödjer:

```yaml
layout:
  direction: left_to_right
  algorithm: layered
  rank_by: type
```

### direction

- `left_to_right`
- `top_to_bottom`
- `right_to_left`
- `bottom_to_top`

### algorithm

- `layered`
- `grid`
- `manual`
- `auto`

Detta är hints. Exportören i steg 18 avgör hur de översätts.

## Grouping

```yaml
groups:
  - id: strategy
    title: Strategi
    match:
      types:
        - Capability
```

Match kan använda:

- `types`
- `specializations`
- `ids`

Grupper påverkar presentation, inte modellsemantik.

## Node display

```yaml
nodes:
  label:
    primary: name
    secondary:
      - type
      - specialization
  show_properties:
    - lifecycle
    - owner
```

## Edge display

```yaml
edges:
  show_type: true
  show_name: false
  show_confidence: true
```

## Styling hints

Version 0.1 tillåter semantiska stilnycklar men inte hårdkodade grafiska färger.

```yaml
style:
  theme: archimate_default
  emphasize:
    - capabilities
```

Konkreta färger och shapes hanteras i exporter eller templates.

## View result

Ett kompilerat view-resultat:

```yaml
view_result:
  view_id: capability-realization
  nodes:
    - id: APP-000001
      type: ApplicationComponent
      name: Ärendehanteringssystem
  edges:
    - id: REL-000001
      type: Realization
      source: APP-000001
      target: STR-000001
```

## Designprinciper

- View är read-only.
- View innehåller inga nya arkitekturfakta.
- View-resultat är derivat.
- Stable IDs används.
- Grupper/layout är presentation, inte semantik.
- Query-logik ska inte dupliceras i view.
