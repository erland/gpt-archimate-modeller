# Pack/unpack/project control – steg 22

## Syfte

Steg 22 samlar projektets paket- och kontrollfunktioner i ett tydligt arbetsflöde.

Målet är att GPT:n ska kunna hantera ett EA-projekt med samma deterministiska ordning varje gång:

1. inspect ZIP,
2. validate ZIP contract,
3. unpack säkert,
4. validate project,
5. inspect project status,
6. arbeta med modellen,
7. validate igen,
8. repack med nytt manifest.

## Project control CLI

Ny gemensam ingång:

```bash
python scripts/project_control.py <command> ...
```

Kommandon:

- `inspect-zip`
- `unpack`
- `inspect-project`
- `validate-project`
- `pack`
- `roundtrip`

## inspect-zip

```bash
python scripts/project_control.py inspect-zip project.zip
```

Visar:

- contract status,
- project id,
- model version,
- root,
- errors/warnings,
- file count.

Ingen unpack görs.

## unpack

```bash
python scripts/project_control.py unpack project.zip --output-dir work
```

Flöde:

1. ZIP-contract valideras,
2. path safety kontrolleras,
3. paketet extraheras till temporär katalog,
4. projektets tekniska validator körs,
5. versionshistorik kontrolleras,
6. först därefter flyttas projektet till requested output directory.

En misslyckad unpack lämnar inte ett halvt extraherat projekt.

## inspect-project

```bash
python scripts/project_control.py inspect-project work/my-project
```

Resultat innehåller bland annat:

- project id/name,
- model version,
- format/layout version,
- ArchiMate-version,
- antal element/relationer,
- antal sources/references/issues,
- antal change sets,
- query/report/view counts,
- quality score,
- validation error/warning counts.

## validate-project

```bash
python scripts/project_control.py validate-project work/my-project
```

Kör:

- teknisk validator,
- semantic quality checker,
- version history validator.

Exit code blir non-zero vid tekniska fel eller inkonsistent versionshistorik.

Quality warnings blockerar inte som standard.

## pack

```bash
python scripts/project_control.py pack work/my-project --output project.zip
```

Före packning:

1. teknisk validering,
2. versionshistorikvalidering,
3. nytt `PACKAGE-MANIFEST.yaml`,
4. ZIP skapas,
5. den skapade ZIP-filen valideras igen.

Det gör pack till en release-gate för det portabla projektpaketet.

## roundtrip

```bash
python scripts/project_control.py roundtrip project.zip
```

Testar:

```text
ZIP
 → validate
 → unpack temp
 → validate project
 → repack temp
 → validate new ZIP
```

Originalfilen ändras inte.

Detta är ett viktigt regressionstest för project ZIP-contract.

## Safe extraction

`safe_unpack.py` använder explicit extraction i stället för `extractall()`.

Varje member:

- normaliseras,
- kontrolleras för absoluta paths,
- kontrolleras för `..`,
- symlink avvisas,
- destination måste ligga under extraction root.

## Workspace marker

Efter lyckad unpack skapas:

```text
.project-control.yaml
```

Exempel:

```yaml
project_control:
  contract_version: "0.1"
  source_package: project.zip
  verified: true
```

Marker-filen är **workspace metadata** och ska inte packas in i projekt-ZIP.

Packern ignorerar därför `.project-control.yaml`.

## Generated workspace state

Workspace-filer:

- `.project-control.yaml`

är inte canonical EA-data.

De ska aldrig läggas i `PACKAGE-MANIFEST.yaml`.

## Atomic pack

Pack sker först till temporär ZIP.

Den temporära ZIP-filen valideras.

Endast om den är giltig ersätts requested output.

## Atomic unpack

Unpack sker till temporär katalog.

Endast ett validerat projekt flyttas till requested output.

## Designprincip

Project control är orkestrering.

Den ska återanvända befintliga:

- ZIP validator,
- package manifest generator,
- project validator,
- quality checker,
- version history validator,

i stället för att duplicera deras semantik.
