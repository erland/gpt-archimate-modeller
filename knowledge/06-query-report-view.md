# Query, report and view

## Query

Query = urval och analyslogik.

Stöd:

- element/relationship select
- type filters
- specialization
- property filters
- evidence filters
- source/target filters
- traversal
- projection
- sort
- aggregation

Resultat är derivat och ska inte skrivas tillbaka till modellen.

## Report

Report = presentation av query-resultat.

Section types:

- table
- list
- summary

Stöd:

- columns
- grouping
- presentation sort
- intro
- notes
- empty state

Report ska inte läsa nya fakta utanför query-resultatet.

## View

View = visualiseringsdefinition.

Stöd:

- selected nodes
- selected relationships
- include/exclude
- grouping
- layout hints
- labels/properties
- edge display rules

View-resultat är derivat.

## Export

Report:
- Markdown
- CSV

View:
- draw.io/diagrams.net XML
- Mermaid


## Large-result runtime policy

Query-CLI/tool output begränsas som standard till 200 rows för att undvika onödigt stora
LLM-payloads. Resultatet anger `matched_count`, `returned_count` och `truncated`.
`--max-rows 0` tillåter explicit obegränsad CLI-output.

Report engine kör queryn utan denna runtime-cap eftersom rapporten är en avsiktlig artefakt;
query-definitionens eget `limit` gäller fortfarande.
