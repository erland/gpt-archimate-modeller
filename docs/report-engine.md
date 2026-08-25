# Report engine – steg 16

## Syfte

Steg 16 gör report-formatet exekverbart.

Flödet är:

```text
EA model
  ↓
query
  ↓
query_result
  ↓
report definition
  ↓
report engine
  ↓
Markdown / CSV
```

## Markdown

Markdown är primärt format för människoläsbara rapporter.

Stöd i version 0.1:

- rapporttitel,
- description,
- sektioner,
- intro,
- table,
- list,
- summary,
- grouping,
- notes,
- empty state.

## CSV

CSV används för tabulära sektioner.

Regel i version 0.1:

- en CSV-fil per table-sektion,
- summary/list exporteras inte automatiskt till CSV,
- rapport med flera tabellsektioner ger flera CSV-filer.

Filnamn:

```text
<report-id>--<section-id>.csv
```

## Markdown table

Report-definition:

```yaml
render:
  type: table
  columns:
    - field: id
      heading: ID
      format: code
```

Output:

```markdown
| ID | Namn |
|---|---|
| `APP-000001` | Ärendehanteringssystem |
```

## List

```yaml
render:
  type: list
  item_fields:
    - name
    - description
```

Output:

```markdown
- **Ärendehanteringssystem** — Systemstöd ...
```

Första item field används som primär text.

## Summary

För aggregate-query:

```yaml
render:
  type: summary
```

Exempel:

```markdown
Totalt: **3**

| Grupp | Antal |
|---|---:|
| ApplicationComponent | 1 |
| Capability | 1 |
| Node | 1 |
```

## Grouping

Om report-sektionen anger:

```yaml
group_by:
  field: type
```

skapas underrubriker:

```markdown
### ApplicationComponent
...
### Node
...
```

## Format

### text

Renderas som vanlig text.

### code

Markdown: backticks.

CSV: rått värde.

### boolean

Markdown:

- `Ja`
- `Nej`

CSV:

- `true`
- `false`

### date

Renderas som ISO-datum i version 0.1.

## Escaping

Markdown-tabeller escape:ar:

- `|`
- radbrytningar.

CSV använder Python CSV writer med standard quoting.

## Proveniens

Report engine får endast använda data som query-resultatet innehåller.

Den ska inte själv läsa model fields utanför query-resultatet för att fylla tabeller.

Detta bevarar separationen mellan query och report.

## CLI

Markdown:

```bash
python scripts/render_report.py   examples/ea-project-split   reports/application-overview.yaml   --format markdown   --output exports/application-overview.md
```

CSV:

```bash
python scripts/render_report.py   examples/ea-project-split   reports/application-overview.yaml   --format csv   --output-dir exports
```

## Determinism

Samma:

- modell,
- query,
- report definition,

ska ge samma output.

Ingen tidsstämpel läggs automatiskt in i renderingen.

## Kommande steg

Steg 30 kan bygga ett större standardbibliotek av reports ovanpå denna motor.
