# Interoperability

## draw.io och Mermaid

Views kan exporteras till:

- draw.io XML
- Mermaid

Stable element/relationship IDs bevaras i draw.io där möjligt.

## ArchiMate Model Exchange

YAML är fortsatt source of truth.

Export använder:

- namespace `http://www.opengroup.org/xsd/archimate/3.0/`
- Model Exchange schema version 3.1 för ArchiMate 3.2-semantik.

Export omfattar:

- elements
- relationships
- documentation
- properties

Organisationens specialization exporteras som property, inte ny `xsi:type`.

## Import

Model Exchange import är staging-import.

Kan återskapa:
- kärnelement,
- relationer,
- properties,
- specialization,
- sammanfattad evidence status/confidence.

Kan inte lossless återskapa:
- source/reference graph,
- evidence assertions,
- changes/history,
- queries/reports/views,
- extension definitions.

Direkt automatisk merge in i etablerad modell görs inte.
