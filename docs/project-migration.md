# Project migration

## Syfte

Projektformat och ZIP-layout kommer att utvecklas över tid. Migration ska därför vara explicit,
deterministisk och validerad.

## Flöde

1. läs `format_version` och `package_layout_version`,
2. kontrollera compatibility,
3. bygg migration plan,
4. kör preview på temporär kopia,
5. applicera migrationsstegen,
6. skapa/uppdatera nya obligatoriska stödstrukturer,
7. validera det migrerade projektet,
8. skriv `migrations/history.yaml`,
9. ersätt arbetskopian atomiskt.

## Kommandon

```bash
python scripts/migrate_project.py <project> --compatibility
python scripts/migrate_project.py <project> --plan
python scripts/migrate_project.py <project> --preview
python scripts/migrate_project.py <project> --apply
```

## Migration registry

```text
migrations/registry.yaml
```

Varje migration har stabilt `MIG-NNNNNN`.

## Migration history

Formatmigrationer sparas separat från EA-modellens versionshistorik:

```text
migrations/history.yaml
```

## Registrerade migrationer

```text
MIG-000001: format 0.0 -> 0.1
MIG-000002: format 0.1 -> 0.2
```

### MIG-000002

0.1 → 0.2 är den produktionsmigration som infördes efter real-EA-piloten.

Den:

- ändrar `project.yaml.format_version` till `0.2`,
- bevarar en befintlig `files.impact_themes`-path,
- uppgraderar den befintliga impact-theme-filens metadata till `format_version: '0.2'`,
- bevarar samtliga befintliga theme-poster oförändrade,
- skapar `extensions/impact-themes.yaml` med tom lista om registry saknas,
- invalidaterar stale `PACKAGE-MANIFEST.yaml` och `MODEL-INDEX.json` i workspacet.

Derived manifest/index regenereras vid pack. Migrationen ändrar inga ArchiMate-element,
relationer, sources eller evidence.

## Idempotens

En migration körs aldrig två gånger. När projektet redan är på target-version returneras `no_change`.

## Future version

En okänd högre formatversion klassas som `unsupported_future`.
Read-only inspection är tillåten men write/migration stoppas.

## Designprinciper

- migration är explicit,
- migration körs på temporär kopia,
- migration fabricerar inte arkitekturfakta,
- migration valideras innan publicering,
- downgrade görs inte automatiskt.


## Step 47 compatibility contract

- läsbart: format 0.1 och 0.2,
- write target: 0.2,
- 0.1 write/update kräver explicit migration,
- preview får inte mutera source,
- apply är atomisk,
- migrationshistorik är separat från modellens versionshistorik,
- downgrade 0.2 → 0.1 stöds inte,
- unknown future format är read-only.
