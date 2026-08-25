# Arbeta med ett projekt-ZIP

## Projekt-ZIP är arbetsenheten

Ett projekt-ZIP innehåller hela EA-projektet och kan flyttas mellan konversationer och miljöer utan extern projektdatabas.

Typisk struktur:

```text
project.yaml
model/
sources/
extensions/
specializations/
issues/
architecture/
identity/
changes/
versioning/
queries/
reports/
views/
exports/
MODEL-INDEX.json
PACKAGE-MANIFEST.yaml
CHANGELOG.md
```

`MODEL-INDEX.json` är en cache. YAML-filerna är canonical.

## Öppna ett projekt

När du laddar upp ett projekt-ZIP ska GPT:n först:

1. kontrollera ZIP-säkerhet,
2. kontrollera manifest/checksums,
3. kontrollera formatkompatibilitet,
4. migrera endast när det är tillåtet och nödvändigt,
5. validera projektet.

Först därefter ska modellen ändras.

## Uppdatera ett projekt

En modelländring är en explicit förändring, inte en direkt filpatch.

Typiskt flöde:

```text
projekt-ZIP
→ change set
→ dry run
→ apply
→ teknisk validering
→ quality check
→ modellversion
→ nytt projekt-ZIP
```

## Modellversion

Modellversionen följer SemVer:

- PATCH – informations-/metadataändring utan strukturell betydelse
- MINOR – strukturell förändring
- MAJOR – explicit breaking change

GPT:n beräknar högsta relevanta förändringsnivå.

## Äldre projekt

Om projektformatet är äldre men migrerbart ska uppdatering normalt stoppas med `migration_required` tills migration tillåts.

Okänd framtida formatversion får inte skrivas över automatiskt.

## Stora projekt

Projekt-ZIP använder:

- checksummanifest,
- robust ZIP-validering,
- ett deriverat `MODEL-INDEX.json`.

Indexet används bara om fingerprint matchar YAML-källorna. Vid stale index används YAML automatiskt.

## CLI för avancerad användning

Skapa nytt:

```bash
python scripts/new_project.py --spec new-project.yaml --output-zip project.zip
```

Uppdatera:

```bash
python scripts/update_project.py project.zip changes/CHG-000123.yaml --output updated.zip
```

Validera ZIP:

```bash
python scripts/validate_project_zip.py project.zip
```
