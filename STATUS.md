# Development status

| Item | Status |
|---|---|
| Steps 1–48 | Complete |
| Stable version | 1.0.0 |
| Package version | 1.0.0 |
| Product plan | 48 / 48 |
| GPT Builder 1.5 migration | 9 / 9 complete |
| Active runtimes | 5 |
| OpenAI Plugin | equivalent_runtime_dependent |
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
- Chat ZIP, Custom GPT, Claude Projects, OpenCode and OpenAI Plugin runtime distributions.
- Registry-driven build/release, instruction adherence and five-dimensional runtime parity.

## GPT Byggaren 1.5.0

Följande är slutligt verifierat:

- Chat ZIP: equivalent parity.
- Custom GPT: equivalent parity med plattformsbegränsningar och no-false-PASS.
- Claude Projects: reduced parity med explicita begränsningar.
- OpenCode: equivalent parity med typade ArchiMate-tools, explicit `projectRoot`, path guard och approval på mutation.
- OpenAI Plugin: active `equivalent_runtime_dependent` skills-first runtime med required filesystem/persistent-state/Python execution för canonical project work.
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

## Pågående migration till GPT Byggaren 1.6.33 (PR #8)

Detta är en separat migration och **ersätter ännu inte** den stabila 1.5-releasekedjan som dokumenteras ovan. Produktversionen förblir 1.0.0 och YAML/ArchiMate-kontrakten ändras inte av distributionsmigreringen.

- Fem peer-distributioner och ett projektarkiv har byggts och originalvaliderats med 1.6.33 i migrations-CI.
- De fyra paketerade Skill-runtimernas Python-projektlivscykel har smoketestats från uppackade arkiv.
- Claude Projects och riktiga Chat-/Plugin-/Claude-/OpenCode-värdmiljöer är ännu inte funktionellt verifierade.
- Ordinarie `build-distributions.yml` och taggdriven `release.yml` använder fortfarande 1.5-baserade skript och validatorer; **de är inte bevis på en genomförd 1.6.33-release**.
- Se `docs/runtime-parity-1.6.33.md` och `migration-status-1.6.33.yaml` för verifieringsomfattning och återstående blockerare.

Release får inte kallas 1.6.33-klar förrän den ordinarie taggdrivna byggkedjan använder den nya motorn, levererar rätt fem runtimearkiv, har motsvarande release-asset-kontroll samt återstående värdtester bedömts. Ingen merge eller release har genomförts här.
