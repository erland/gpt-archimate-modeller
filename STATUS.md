# Development status

| Item | Status |
|---|---|
| Steps 1–44 | Complete |
| Step 45 – Real EA pilot | Complete |
| Step 46 – Revise format | Complete |
| Step 47 – Backward compatibility/migration | Complete |
| Step 48 – v1.0.0 | Complete |
| Stable version | 1.0.0 |
| Package version | 1.0.0 |
| Product plan | 48 / 48 |
| E2E scenarios | 9 / 9 passed |
| Observable LLM evals | 12 historical domain evals + 3 runtime-adherence evals |

## Product status

ArchiMate YAML EA GPT 1.0.0 är release-ready i källan. Publicering sker först efter merge,
grön CI/distributionsbuild på slutcommitten och tagg `v1.0.0`.

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

## Release sequence

1. final Step 48 commit passes CI,
2. final distribution build passes,
3. merge PR #5,
4. create tag `v1.0.0`,
5. tag-driven release workflow creates and validates all four distributions plus checksums/metadata.
