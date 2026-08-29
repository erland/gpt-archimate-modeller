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


## Always-use budget

För att runtime ska fungera robust även i mindre modeller ska `always_use` hållas litet.

Följande sju filer är kärnkontrakt och kan alltid användas:

- `01-runtime-contract.md`
- `02-archimate-core.md`
- `03-project-format.md`
- `04-identity-evidence.md`
- `05-change-versioning.md`
- `07-validation-quality.md`
- `09-project-package-migration.md`

Arbetsflödes- och analysfiler som new/update project, conflicts, baseline/target, impact, quality report, large ZIP och model index är task-specific och ska bara hämtas när uppgiften kräver dem.

Målet är att systeminstruktionen och core Knowledge ska räcka för att starta arbetet; routing ska sedan lägga till minsta relevanta fördjupning.
