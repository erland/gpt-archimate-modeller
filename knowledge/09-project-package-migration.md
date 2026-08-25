# Project ZIP, control and migration

## Project ZIP contract

ZIP innehåller exakt en projektrot.

Obligatoriska canonical filer och kataloger definieras i:
- `package/project-zip-contract.yaml`

`PACKAGE-MANIFEST.yaml` innehåller SHA-256 för projektets filer.

Path traversal och symlinks är förbjudna.

## Project control

Gemensam CLI:

- inspect-zip
- unpack
- inspect-project
- validate-project
- pack
- roundtrip

Unpack och pack ska vara atomiska.

`.project-control.yaml` är workspace metadata och ska inte packas.

## Migration

Migration är explicit.

CLI stödjer:

- compatibility
- plan
- preview
- apply

Registry:
- `migrations/registry.yaml`

History:
- `migrations/history.yaml`

Unknown future format = read-only.
