# Queries, rapporter, views och export

## Query

Query är read-only och används för att välja eller traversera modellinformation.

Exempel:

> Lista alla ApplicationComponent med lifecycle phase_out.

## Standardrapporter

Biblioteket innehåller bland annat rapporter för:

- modellöversikt,
- applikationer/plattformar,
- capability-realisering,
- evidence/spårbarhet,
- issues/observations,
- modellkvalitet,
- lifecycle/tid.

Rapporter kan normalt renderas till Markdown och tabellsektioner till CSV.

## Standardvyer

Sex standardvyer finns:

- architecture-layers
- standard-capability-realization
- application-platform-context
- application-landscape
- technology-platform-landscape
- implementation-roadmap-context

## Diagramformat

Standardvyer kan exporteras till:

- draw.io / diagrams.net XML
- Mermaid

Stable modell-ID:n bevaras i draw.io-exporten.

## Model Exchange

ArchiMate Model Exchange kan exporteras för interoperabilitet.

Import är en staging-process. Importerad XML skrivs inte direkt över canonical YAML-modell.

## Separation

Viktigt:

```text
model ≠ query ≠ report ≠ view
```

Att skapa en rapport eller vy ska inte ändra modellen.

## Exempel

```bash
python scripts/render_report.py project reports/standard/lifecycle-overview.yaml --format markdown
```

```bash
python scripts/export_diagram.py project views/standard/application-landscape.yaml --format drawio --output application-landscape.drawio
```
