# GitHub release och distributionspaket

Repo-roten är katalogen där `README.md` ligger. När den checkas in i GitHub kan två distributionspaket byggas automatiskt.

## Artefakter

En release med taggen exempelvis `v1.0.0-rc.3` skapar:

- `archimate-yaml-ea-gpt-custom-gpt-v1.0.0-rc.3.zip` — för registrering i Custom GPT Builder.
- `archimate-yaml-ea-gpt-chat-v1.0.0-rc.3.zip` — för uppladdning direkt i en vanlig ChatGPT-konversation.

## Custom GPT-paket

Innehåller endast Builder Instructions, Builder-konfiguration och ett kompakt, deterministiskt Knowledge-paket.

## Chat-paket

Innehåller runtime Knowledge, scripts, schemas, templates och konfigurationsfiler som behövs för ZIP→ZIP-arbetsflödet. Testsvit, fixtures och utvecklardokumentation följer inte med.

## GitHub Actions

- `ci.yml` kör regression, dokumentations-/evalvalidering och bygger distributionspaketen på push/PR.
- `build-distributions.yml` bygger paket på push/PR/workflow_dispatch och bifogar båda ZIP:arna till en publicerad GitHub Release.
- `release.yml` bygger och validerar båda paketen samt skapar/uppdaterar GitHub Release direkt när en SemVer-tagg `v*.*.*` pushas. Detta är avsiktligt självständigt eftersom GitHub normalt inte kedjar nya workflow-körningar från events skapade med `GITHUB_TOKEN`.

## Lokal kontroll

```bash
python scripts/build_distributions.py --version 1.0.0-rc.3
python scripts/validate_distributions.py --version 1.0.0-rc.3
```
