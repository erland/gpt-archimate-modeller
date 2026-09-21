# GitHub release och distributionspaket

Repo-roten är katalogen där `README.md` ligger. Distributionerna byggs från det gemensamma registret `runtime/distribution-registry.yaml`.

## Runtime-artefakter

Den stabila releasen `v1.0.0` skapar fyra ZIP-distributioner:

- `archimate-yaml-ea-gpt-chat-v1.0.0.zip` — Chat ZIP, target **equivalent**.
- `archimate-yaml-ea-gpt-custom-gpt-v1.0.0.zip` — Custom GPT, **equivalent_with_platform_constraints**.
- `archimate-yaml-ea-gpt-claude-projects-v1.0.0.zip` — Claude Projects, **reduced** parity.
- `archimate-yaml-ea-gpt-opencode-v1.0.0.zip` — OpenCode, target **equivalent**.

Releasepaketet innehåller dessutom:

- `distribution-build-manifest.json`
- `SHA256SUMS.txt`
- `release-metadata.yaml`

OpenAI Plugin v1 är bedömd men inte aktiverad och publiceras inte.

## Build och validering

Registry-driven lokal build:

```bash
VERSION="$(tr -d '[:space:]' < VERSION)"
python scripts/build_all_distributions.py --version "$VERSION" --output-dir dist
python scripts/validate_all_distributions.py --manifest dist/distribution-build-manifest.json
```

Ordinarie CI kör dessutom instruction adherence och runtime parity över behavior, capability, artifact, workspace_state och tool.

## Release från tagg

`.github/workflows/release.yml` triggas av SemVer-taggar `v*.*.*` och kan även startas manuellt med en explicit tagg. Workflowet anropar `scripts/build_release.sh`.

Release-buildern:

1. kör regression och canonical validators,
2. validerar registry och repository hygiene,
3. bygger samtliga fyra runtimes,
4. validerar build-manifestet,
5. kör instruction adherence för alla fyra,
6. kör femdimensionell runtime parity,
7. skapar checksummor och release metadata.

Git-taggen styr releasebygget och måste matcha repo-filen `VERSION`. En release stoppas om
exempelvis taggen `v1.0.0` inte matchar `VERSION=1.0.0`.

## GitHub Actions

- `ci.yml` — regression, contracts, registry, hygiene, release-workflow validation, registry-build, instruction adherence och parity.
- `build-distributions.yml` — bygger registry-distributioner på push/PR/workflow_dispatch och laddar upp de fyra ZIP:arna plus build-manifest som workflow artifact. Vid `release`-event kan artefakterna också laddas upp till den publicerade releasen.
- `release.yml` — självständigt taggdrivet releaseflöde som bygger releaseartefakterna och skapar/uppdaterar GitHub Release.


## Stable v1.0.0

Efter Step 48 ska PR:n först mergas med gröna slutgrindar. Därefter skapas taggen
`v1.0.0`. Tag-workflowet kör hela release-buildern på nytt och publicerar först därefter
GitHub Release-artefakterna.
