# Project migration – steg 23

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

## Reference migration

Steg 23 innehåller en testmigration:

```text
format 0.0 -> 0.1
```

Legacy-fixturen bygger på en semantiskt komplett modell men saknar strukturer som införts senare,
exempelvis `changes/index.yaml`, `versioning/history.yaml`, vissa tomma partitioner och
migrationshistorik.

Migrationen skapar dessa utan att ändra modellens arkitekturfakta.

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
