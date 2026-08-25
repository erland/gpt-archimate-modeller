# Project ZIP contract – steg 21

Project ZIP är den portabla arbets- och transportenheten för ett EA-projekt.

## Grundkrav

ZIP innehåller exakt en projektrot och ska kunna flyttas mellan sessioner utan extern state.

Obligatoriska canonical filer omfattar `project.yaml`, samtliga modellpartitioner,
relationer, sources/references, extensions/specializations, issues, identity counters,
change index, version history och `CHANGELOG.md`.

Obligatoriska kataloger omfattar även `queries/`, `reports/`, `views/` och `exports/`.
Tomma obligatoriska kataloger skrivs som explicita ZIP directory entries.

## Versionskompatibilitet

Contract 0.1 stödjer:

```yaml
format_version: "0.1"
package_layout_version: "0.1"
project:
  archimate_version: "3.2"
```

Nyare okänd version får inspekteras read-only men ska inte skrivas över automatiskt.

## Canonical och generated

Canonical:

- `project.yaml`
- `model/**`
- `sources/**`
- `extensions/**`
- `issues/**`
- `identity/**`
- `changes/**`
- `versioning/**`
- `queries/**`
- `reports/**`
- `views/**`
- `CHANGELOG.md`

Generated:

- `exports/**`

Generated artefakter får aldrig vara enda platsen där arkitekturfakta finns.

## PACKAGE-MANIFEST.yaml

Varje portabelt projekt-ZIP ska innehålla manifest med SHA-256 för alla filer utom manifestet självt.

## Path safety

Förbjudet:

- absoluta paths,
- `..`,
- path traversal,
- symlinks i ZIP.

`.DS_Store`, `Thumbs.db` och `__MACOSX` ska inte packas.

## Robusthetsregel

Korrupt eller partiellt `project.yaml` ska ge strukturerade valideringsfel och får aldrig krascha ZIP-validatorn.

## GPT-flöde

1. kontrollera ZIP-säkerhet,
2. kontrollera exakt en root,
3. läsa manifest/project.yaml,
4. verifiera versionstöd,
5. verifiera checksums,
6. packa upp,
7. köra projektvalidering,
8. först därefter ändra modellen.

Contract version: `0.1`.
