# GPT Knowledge structure – steg 25

## Mål

Systeminstruktionen ska vara stabil och beteendestyrande.
Knowledge ska bära domän- och formatdetaljer.

## Struktur

`knowledge/` innehåller nio tematiska kärnfiler plus:

- `knowledge-index.yaml`
- `routing.yaml`

## Prioritet

Priority 1:
- runtime,
- ArchiMate core,
- project format,
- identity/evidence,
- change/versioning,
- validation,
- package/migration.

Priority 2:
- query/report/view,
- interoperability.

## Machine-readable authority

När en sammanfattande Markdown-fil och en maskinläsbar definition skiljer sig ska den maskinläsbara definitionen ses som auktoritativ för exakta regler.

Exempel:
- elementlista → `metamodel/elements.yaml`
- relationstyper → `metamodel/relationships.yaml`
- schema → `schemas/*.json`
- ZIP-contract → `package/project-zip-contract.yaml`

## Runtime routing

`knowledge/routing.yaml` mappar arbetsintentioner till relevanta knowledge-filer.

Detta minskar behovet att läsa all referensdokumentation för varje uppgift.
