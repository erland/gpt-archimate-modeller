# Development status

| Item | Status |
|---|---|
| Steps 1–44 | Complete |
| Step 45 – Real EA pilot | Complete |
| Step 46 – Revise format | Complete |
| Step 47 – Backward compatibility/migration | Complete |
| Step 48 – v1.0.0 | Next |
| Release candidate | 1.0.0-rc.8 |
| Package version | 0.47.0 |
| E2E scenarios | 9 / 9 passed |
| Observable LLM evals | 12 historical domain evals + 3 runtime-adherence evals |

## Completed plan step
`47 / 48`

## Step 45 – Real EA pilot

Pilotrapport: `docs/real-ea-pilot-step45.md`.

## Step 46 – Format revision

Format 0.2 är målformat. Nya projekt skapas som 0.2 medan 0.1 fortsatt kan läsas.

## Step 47 – Backward compatibility/migration

Explicit `MIG-000002` migrerar format 0.1 → 0.2.

Migrationen:

- körs via befintligt preview/plan/apply-flöde,
- bevarar befintlig `files.impact_themes`-path,
- bevarar alla befintliga impact-theme-poster,
- skapar en tom controlled registry om projektet saknar impact themes,
- uppgraderar registry-metadata till format 0.2,
- registrerar migrationen separat i `migrations/history.yaml`,
- tar bort stale derived `PACKAGE-MANIFEST.yaml` och `MODEL-INDEX.json`,
- bygger och validerar nya transportartefakter vid nästa pack,
- gör ingen automatisk downgrade.

Regressionstest verifierar preview, apply, preservation, idempotens och valid repack.

Nästa steg är **Step 48 – v1.0.0**.

## Runtime distributions

Chat ZIP, Custom GPT, Claude Projects och OpenCode byggs fortsatt registry-drivet.
