# Development status

| Item | Status |
|---|---|
| Steps 1–43 | Complete |
| Step 44 – End-to-end GPT test | Complete |
| Step 45 – Real EA pilot | Complete |
| Release candidate | 1.0.0-rc.6 |
| Package version | 0.45.0 |
| E2E scenarios | 9 / 9 passed |
| Observable LLM evals | 12 historical domain evals + 3 runtime-adherence evals |
| Integration defects found/fixed | 2 |

## Completed plan step
`45 / 48`

## RC maintenance

- Safe cleanup complete: Python cache and generated E2E result files removed.
- GitHub Actions release packaging added.
- Four runtime distributions: Chat ZIP, Custom GPT, Claude Projects and OpenCode.
- Development plan remains at Step 44; Step 45 still requires a real EA pilot.
- RC.4: fixed query CLI model-loader integration; regression covered by T-QRV-002.

## Luna/runtime hardening

- Chat bootstrap precedence clarified.
- Chat runtime package slimmed to runtime-relevant scripts.
- Knowledge `always_use` reduced to seven core files; task-specific routing enforced.
- EVAL-013–015 add bootstrap, multi-turn retention and Knowledge-routing coverage.
- Runtime scripts are packaged with deterministic executable permissions.

## GPT Byggaren 1.4 runtime migration

Det separata runtime-migrationsspåret är nu komplett och ändrar **inte** produktplanens status
`44 / 48`. Steg 45 – Real EA pilot är genomfört; nästa ordinarie steg är Step 46 – Revise format.

| Migration item | Status |
|---|---|
| Step 49 – Runtime assessment | Complete |
| Step 50 – Platform-neutral runtime contracts | Complete |
| Step 51 – Canonical ArchiMate tool contract | Complete |
| Step 52 – Claude Projects distribution | Complete |
| Step 53 – OpenCode distribution | Complete |
| Step 54 – Registry-driven build and runtime-aware hygiene | Complete |
| Step 55 – Four-runtime instruction adherence and parity | Complete |
| Step 56 – Four-runtime CI, release and documentation | Complete |
| Step 57 – Full regression and new release candidate | Complete |
| Target runtimes | Chat ZIP, Custom GPT, Claude Projects, OpenCode |
| OpenAI Plugin v1 | Assessed, not planned |
| Main baseline CI | PASS |
| Main baseline distribution build | PASS |

Se `docs/gpt-builder-1.4-runtime-migration.md`.

## RC.5 runtime migration readiness

- Runtime migration steps 49–57 complete.
- Four runtime targets: Chat ZIP, Custom GPT, Claude Projects and OpenCode.
- OpenAI Plugin v1 remains assessed/not planned.
- Product plan is now 45/48; Step 45 Real EA pilot is complete.
- Step 45 findings are documented in `docs/real-ea-pilot-step45.md`.

## Step 45 – Real EA pilot

- Pilot: `it-formagemodell-standard-archimate-v1.11.0.zip`.
- 462 elements, 1,104 relationships, 21 sources and 14 change sets.
- Query/report and Model Exchange export worked on the normalized pilot copy.
- Impact analysis exposed a deterministic equal-depth path comparison defect; fixed and regression-covered.
- Format/report/quality findings are carried into Step 46 rather than silently changing the schema in Step 45.
