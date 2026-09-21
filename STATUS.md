# Development status

| Item | Status |
|---|---|
| Steps 1–43 | Complete |
| Step 44 – End-to-end GPT test | Complete |
| Step 45 – Real EA pilot | Not started |
| Release candidate | 1.0.0-rc.4 |
| Package version | 0.44.2 |
| E2E scenarios | 9 / 9 passed |
| Observable LLM evals | 12 historical domain evals + 3 runtime-adherence evals |
| Integration defects found/fixed | 2 |

## Completed plan step
`44 / 48`

## RC maintenance

- Safe cleanup complete: Python cache and generated E2E result files removed.
- GitHub Actions release packaging added.
- Two release distributions: Custom GPT and Chat package.
- Development plan remains at Step 44; Step 45 still requires a real EA pilot.

- RC.4: fixed query CLI model-loader integration; regression covered by T-QRV-002.

## Luna/runtime hardening

- Chat bootstrap precedence clarified.
- Chat runtime package slimmed to runtime-relevant scripts.
- Knowledge `always_use` reduced to seven core files; task-specific routing enforced.
- EVAL-013–015 add bootstrap, multi-turn retention and Knowledge-routing coverage.
- Runtime scripts are packaged with deterministic executable permissions.


## GPT Byggaren 1.4 runtime migration

Detta är ett separat migrationsspår och ändrar **inte** produktplanens status
`44 / 48`. Steg 45 – Real EA pilot är fortfarande inte genomfört.

| Migration item | Status |
|---|---|
| Step 49 – Runtime assessment | Complete |
| Step 50 – Platform-neutral runtime contracts | Complete |
| Step 51 – Canonical ArchiMate tool contract | Complete |
| Step 52 – Claude Projects distribution | Next |
| Target runtimes | Chat ZIP, Custom GPT, Claude Projects, OpenCode |
| OpenAI Plugin v1 | Assessed, not planned |
| Main baseline CI | PASS |
| Main baseline distribution build | PASS |

Se `docs/gpt-builder-1.4-runtime-migration.md`.
