# Query-format – steg 14

## Syfte

Query-formatet beskriver **vad som ska väljas och hur modellen ska traverseras**.
Presentation hör senare hemma i report-format och visualisering i view-format.

## Grundstruktur

```yaml
query:
  id: applications
  select: elements
  where:
    type_in:
      - ApplicationComponent
  return:
    fields:
      - id
      - type
      - name
```

## select

- `elements`
- `relationships`

## where

Stödda filter i version 0.1:

- `type`
- `type_in`
- `specialization`
- `id_in`
- `name_contains`
- `property_equals`
- `property_in`
- `evidence_status_in`
- `confidence_in`
- för relationship-query: `source_in`, `target_in`

Filter i samma `where` kombineras med AND.

## Traverse

Traversal gäller elementqueries:

```yaml
traverse:
  direction: incoming
  relationship_types:
    - Realization
  target_types:
    - ApplicationComponent
  depth: 1
  include_start: false
```

Direction:

- `incoming`
- `outgoing`
- `both`

Depth: 1–10.

## Return

```yaml
return:
  fields:
    - id
    - name
    - properties.lifecycle
    - evidence.status
```

Om `return` saknas returneras hela objekt.

## Sortering och limit

```yaml
sort:
  - field: name
    direction: asc

limit: 100
```

## Aggregation

Version 0.1 stöder count och group-by:

```yaml
aggregate:
  count: true
  group_by: type
```

## Resultat

```yaml
query_result:
  query_id: applications
  count: 2
  rows: [...]
```

Vid aggregation kompletteras resultatet med exempelvis:

```yaml
groups:
  ApplicationComponent: 2
```

## Designprinciper

- Query är read-only.
- Stable IDs används som identitet.
- Traversal deduplicerar element.
- Query-resultat är derivat och aldrig source of truth.
- Query, report och view hålls separata.
