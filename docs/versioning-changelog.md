# Modellversionering och changelog – steg 13

## Versionsbegrepp
Projektet skiljer på paketversion, formatversion, package-layout-version och EA-modellens `model_version`.

## SemVer för model_version
- PATCH: description, evidence, sources/references, aliases, metadata, properties och issues.
- MINOR: add/remove element, add/remove relation och deprecate element.
- MAJOR: större brytande omstrukturering; kräver explicit begäran eller migration.

Varje change-set-operation har en impact. Change setets impact är den högsta bland operationerna.
`requested_impact` får höja men aldrig sänka den beräknade impacten.

## Historik
- `changes/index.yaml` indexerar applicerade change sets.
- `versioning/history.yaml` spårar modellversioner.
- samma `CHG-NNNNNN` får inte appliceras två gånger.

## ID-counter-konsistens
När ett explicit nytt ID läggs till via change set uppdateras motsvarande counter i samma transaktion innan valideringen körs. Detta säkerställer att exempelvis `STR-000002` också ger minst `STR: 2` i `identity/id-counters.yaml`.

Versionshistoriken är repository-agnostisk och fungerar utan Git.
