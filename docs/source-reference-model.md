# Käll- och referensmodell – steg 7

## Syfte

Källmodellen ska göra det möjligt att spåra arkitekturinformation till ett konkret underlag och, när möjligt, till en konkret plats i underlaget.

Det räcker inte att veta att ett element stöds av ett dokument. GPT:n bör också kunna ange exempelvis:

- sida 12,
- avsnitt 4.2,
- tabell 3,
- rad 120–145,
- rubrik "Teknisk plattform",
- workshop 2026-08-20, beslutspunkt 4.

## Separation mellan Source och Reference

### Source

En `source` beskriver själva informationskällan.

Exempel:

```yaml
- id: SRC-000002
  type: document
  title: Systemkatalog
  date: 2026-08-25
  origin:
    kind: file
    path: sources/files/systemkatalog.pdf
```

### Reference

En `reference` beskriver en specifik plats eller del av en source.

Exempel:

```yaml
- id: REF-000003
  source_ref: SRC-000002
  locator:
    kind: page
    value: "12"
  label: Systembeskrivning
```

Evidence assertions ska i första hand peka på `reference_refs` när exakt lokalisering finns, annars direkt på `source_refs`.

## Source types

Format 0.2 stödjer följande source types:

- `document`
- `web`
- `interview`
- `workshop`
- `system_export`
- `user_statement`
- `email`
- `presentation`
- `spreadsheet`
- `repository`
- `other`

## Source origin

En source kan ha en origin.

### File

```yaml
origin:
  kind: file
  path: sources/files/systemkatalog.pdf
```

### URL

```yaml
origin:
  kind: url
  uri: https://example.org/architecture
```

### Conversation

För användaruppgifter eller workshopanteckningar:

```yaml
origin:
  kind: conversation
  conversation_ref: current
```

### External system

```yaml
origin:
  kind: external_system
  system: CMDB
  external_id: export-2026-08-25
```

## Reference locator

Locator är strukturerad.

Tillåtna `kind`:

- `page`
- `section`
- `heading`
- `line_range`
- `paragraph`
- `table`
- `figure`
- `cell_range`
- `timestamp`
- `record`
- `anchor`
- `custom`

Exempel:

```yaml
locator:
  kind: line_range
  start: 120
  end: 145
```

eller:

```yaml
locator:
  kind: section
  value: "4.2"
```

## Flera referenser i samma source

Samma source kan ha flera reference-objekt.

```yaml
references:
  - id: REF-000001
    source_ref: SRC-000002
    locator:
      kind: page
      value: "12"

  - id: REF-000002
    source_ref: SRC-000002
    locator:
      kind: page
      value: "18"
```

## Reference ID

Referenser använder:

```text
REF-NNNNNN
```

och får egen räknare i identity-strategin.

## Evidence assertion

Evidence assertions kan nu använda:

```yaml
source_refs:
  - SRC-000002

reference_refs:
  - REF-000003
```

Regel:

- `reference_refs` är starkare och mer precisa,
- `source_refs` får användas när exakt locator saknas,
- båda får förekomma samtidigt.

## Source quality metadata

En source kan ha:

```yaml
quality:
  authority: high
  freshness: medium
  completeness: high
```

Tillåtna värden:

- `high`
- `medium`
- `low`
- `unknown`

Dessa beskriver källan, inte modellens confidence.

## Authorship och ownership

Valfria metadata:

```yaml
authors:
  - Tullverket

publisher: Tullverket
owner: Arkitekturfunktionen
```

## Dates

En source kan ha:

- `published_date`
- `retrieved_date`
- `effective_date`
- `expires_date`

Det gör det möjligt att senare bedöma aktualitet.

## Content fingerprint

För filer eller importer kan ett fingerprint sparas:

```yaml
fingerprint:
  algorithm: sha256
  value: ...
```

Detta hjälper att avgöra om två source-poster avser samma underlag.

## Källor i projekt-ZIP

Projektet använder:

```text
sources/
├── sources.yaml
└── references.yaml
```

Själva originalfilerna kan senare ligga under exempelvis:

```text
sources/files/
```

men det är inte obligatoriskt att bädda in källfilen i projekt-ZIP.

## Informationsbevarande

GPT:n ska:

- återanvända source-ID om samma källa redan finns,
- återanvända reference-ID om samma locator redan finns,
- inte skapa ny source enbart för en ny sida i samma dokument,
- inte skriva över source metadata utan grund,
- kunna behålla gamla references även om modellen ändras.

## Kommande användning

Denna modell blir grund för:

- exakta källhänvisningar i rapporter,
- evidence coverage,
- kvalitetskontroll,
- konfliktanalys,
- framtida importflöden.
