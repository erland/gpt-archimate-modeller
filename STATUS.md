# Development status

| Item | Status |
|---|---|
| Steps 1–48 | Complete |
| Stable version | 1.0.0 |
| Package version | 1.0.0 |
| Product plan | 48 / 48 |
| GPT Builder 1.5 migration | 9 / 9 complete |
| Active runtimes | 4 |
| OpenAI Plugin | not_active / reduced / advisory only |
| E2E scenarios | 9 / 9 passed |
| Observable LLM evals | 12 historical domain evals + 3 runtime-adherence evals |

## Product status

ArchiMate YAML EA GPT **1.0.0** är stabil produktversion. GPT Byggaren 1.5.0-migreringen är beteendebevarande och ändrar inte produktformatet eller releasehistoriken.

## v1.0 scope

- ArchiMate 3.2 semantic core.
- YAML project format 0.2.
- Explicit format 0.1 → 0.2 migration via `MIG-000002`.
- Stable IDs, evidence/provenance and controlled change workflow.
- Queries, reports, views, impact analysis and model quality report.
- ArchiMate Model Exchange export and staging import.
- Deterministic project ZIP contract and derived model index.
- Chat ZIP, Custom GPT, Claude Projects and OpenCode runtime distributions.
- Registry-driven build/release, instruction adherence and five-dimensional runtime parity.

## GPT Byggaren 1.5.0

Följande är slutligt verifierat:

- Chat ZIP: equivalent parity.
- Custom GPT: equivalent parity med plattformsbegränsningar och no-false-PASS.
- Claude Projects: reduced parity med explicita begränsningar.
- OpenCode: equivalent parity med typade ArchiMate-tools, explicit `projectRoot`, path guard och approval på mutation.
- OpenAI Plugin: inte aktiv distribution; reduced/advisory only.
- CI och release använder samma 1.5-kontrakt.
- Release-assets härleds exakt från `runtime/distribution-registry.yaml`.
- Wildcard-publicering av runtime-assets används inte.

## Release sequence

1. slutcommitten ska passera ordinarie CI,
2. Build GPT distributions ska vara grön,
3. migrations-PR:n kan mergas,
4. framtida release skapas med semantisk GitHub Release-tagg,
5. taggdriven release bygger och validerar exakt de aktiva registry-distributionerna plus checksummor/metadata.

Maskinläsbar migrationsstatus finns i `migration-status-1.5.yaml`.
