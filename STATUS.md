# Development status

| Item | Status |
|---|---|
| Steps 1–44 | Complete |
| Step 45 – Real EA pilot | Complete |
| Step 46 – Revise format | Complete |
| Step 47 – Backward compatibility/migration | Next |
| Release candidate | 1.0.0-rc.7 |
| Package version | 0.46.0 |
| E2E scenarios | 9 / 9 passed |
| Observable LLM evals | 12 historical domain evals + 3 runtime-adherence evals |

## Completed plan step
`46 / 48`

## Step 45 – Real EA pilot

Pilotrapport: `docs/real-ea-pilot-step45.md`.

Piloten prövade 462 element, 1,104 relationer, 21 sources och 14 change sets och gav
konkreta input till formatrevisionen.

## Step 46 – Format revision

Format 0.2 är nu målformat för nya projekt. 0.1 kan fortfarande läsas.

Pilotfynden har omsatts i:

- optional controlled `impact_themes` registry,
- aggregerade unknown relationship-pair findings,
- normaliserade quality-dimensioner för architecture/ownership/evidence,
- bredare capability-realization query/report,
- bounded query CLI/tool output med `matched_count`, `returned_count` och `truncated`.

Step 47 ska nu implementera och verifiera explicit 0.1 → 0.2 migration samt
bakåtkompatibilitet för äldre pilotprojekt.

## Runtime distributions

Chat ZIP, Custom GPT, Claude Projects och OpenCode byggs registry-drivet. Runtime-migreringen
49–57 är fortsatt komplett och oberoende av produktplanens 46/48.
