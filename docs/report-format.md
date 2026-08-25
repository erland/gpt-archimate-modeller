# Report-format – steg 15

## Syfte

Report-formatet beskriver **hur query-resultat ska presenteras**.

Separationen är:

- model = arkitekturkunskap,
- query = urval och traversal,
- report = presentation,
- view = visualisering.

## Grundstruktur

```yaml
report:
  id: application-overview
  title: Applikationsöversikt
  sections:
    - id: applications
      title: Applikationer
      source:
        query: queries/applications.yaml
      render:
        type: table
```

## Sections

En rapport består av en eller flera sektioner.

Varje sektion kan innehålla:

- rubrik,
- introduktionstext,
- query-källa,
- render-definition,
- tomresultatstext.

## Source

Version 0.1 använder sparade query-filer:

```yaml
source:
  query: queries/applications.yaml
```

Inline-query skjuts till senare version för att undvika duplicering.

## Render types

Version 0.1 stödjer:

- `table`
- `list`
- `summary`

### Table

```yaml
render:
  type: table
  columns:
    - field: id
      heading: ID
    - field: name
      heading: Namn
```

### List

```yaml
render:
  type: list
  item_fields:
    - name
    - description
```

### Summary

Används främst med aggregation:

```yaml
render:
  type: summary
```

## Columns

En tabellkolumn:

```yaml
- field: properties.lifecycle
  heading: Livscykel
```

Valfria attribut:

- `field`
- `heading`
- `default`
- `format`

## Format

Version 0.1 stöder:

- `text`
- `code`
- `boolean`
- `date`

## Grouping

Rapporten kan gruppera query-resultat efter ett returnerat fält:

```yaml
group_by:
  field: type
```

Gruppering sker i report-lagret, inte query-lagret.

## Sortering

Sortering bör i första hand göras i queryn eftersom den hör till urval/resultatordning.
Report får dock ange presentationssortering:

```yaml
presentation_sort:
  - field: name
    direction: asc
```

## Empty state

```yaml
empty_message: Inga objekt hittades.
```

## Intro och notes

```yaml
intro: >
  Rapporten visar aktuella applikationer.

notes:
  - Livscykelvärden kommer från organisationsspecifika extensions.
```

## Metadata

```yaml
metadata:
  audience:
    - enterprise_architect
  purpose: inventory
```

## Source references i rapport

Report-formatet får välja att visa evidence/source/references om queryn returnerar dessa fält.

Report-lagret ska inte själv slå upp nya fakta som queryn inte har efterfrågat.

## Output format

Steg 15 definierar report-formatet men inte full render-motor för Markdown/CSV.
Det kommer i steg 16.

## Designprinciper

- Report är deklarativ.
- Report ändrar aldrig modellen.
- Query-logik dupliceras inte i report.
- Samma query kan återanvändas i flera rapporter.
- Presentation ska kunna bytas utan att arkitektururvalet ändras.
