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

## Release från publicerad GitHub Release

Normalflödet är att användaren först skapar och publicerar en GitHub Release med en SemVer-tagg,
till exempel `v1.0.0`. Händelsen `release: published` startar därefter
`.github/workflows/release.yml`.

Workflowet checkoutar exakt release-taggen och anropar `scripts/build_release.sh`.
En manuell `workflow_dispatch` finns kvar för omkörning mot en redan existerande release.

Release-buildern:

1. kör regression och canonical validators,
2. validerar registry och repository hygiene,
3. bygger samtliga fyra runtimes,
4. validerar build-manifestet,
5. kör instruction adherence för alla fyra,
6. kör femdimensionell runtime parity,
7. skapar checksummor och release metadata.

**GitHub Release-taggen är release-versionens source of truth.** Prefixet `v` tas bort och
resten används direkt som distributionsversion. Exempel: `v1.2.3` ger
`archimate-yaml-ea-gpt-chat-v1.2.3.zip`.

Repo-filen `VERSION` används för vanliga push/PR-builds och beskriver källans basversion,
men styr inte versionsnumret i en publicerad release.

## GitHub Actions

- `ci.yml` — regression, contracts, registry, hygiene, release-workflow validation, registry-build, instruction adherence och parity.
- `build-distributions.yml` — bygger registry-distributioner på push/PR/workflow_dispatch och laddar upp de fyra ZIP:arna plus build-manifest som workflow artifact.
- `release.yml` — triggas när en GitHub Release publiceras, bygger releaseartefakterna från release-taggen och laddar upp dem till den redan skapade releasen.


## Stable v1.0.0

Efter Step 48 ska PR:n först mergas med gröna slutgrindar. Därefter skapar och publicerar
du GitHub Release, exempelvis med taggen `v1.0.0`. Publiceringen startar release-workflowet,
som bygger och laddar upp de fyra distributionspaketen, manifest, checksummor och metadata.
