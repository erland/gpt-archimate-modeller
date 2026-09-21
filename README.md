# ArchiMate YAML EA GPT

Ett ZIP-baserat verktygs- och GPT-paket för att skapa, underhålla, analysera och exportera Enterprise Architecture-modeller med **ArchiMate 3.2** som semantisk kärna och **YAML som source of truth**.

## För användare

Börja här:

- [Användardokumentation](docs/user/index.md)
- [Snabbstart](docs/user/quickstart.md)
- [Felsökning](docs/user/troubleshooting.md)

Normal arbetsmodell:

```text
projekt-ZIP
→ GPT analyserar/ändrar
→ validering
→ komplett nytt projekt-ZIP
```

Du behöver normalt inte köra Python-skripten själv.

## Viktiga principer

- ArchiMate är semantisk kärna.
- YAML är canonical arbetsformat.
- Stable IDs bevarar objektidentitet över tid.
- Evidence, provenance och confidence hålls explicit.
- Fakta, inferenser och planerad framtid hålls isär.
- Modell, query, report och view är separata.
- Konflikter och dubbletter löses explicit; ingen tyst merge.
- Baseline/target/transition återanvänder samma objekt-ID:n.
- `MODEL-INDEX.json` är endast en deriverad cache.
- Ett ändrat projekt levereras som ett komplett validerat ZIP.

## Funktioner

Paketet stödjer bland annat:

- full grundläggande ArchiMate-modellering,
- organisationsegna extensions och specializations,
- evidence/source/reference,
- safe change sets och versionshistorik,
- queries och rapporter,
- draw.io och Mermaid views,
- ArchiMate Model Exchange export och staging-import,
- issues/observations,
- baseline/target/transition,
- time/lifecycle,
- impact analysis,
- model quality report,
- robust/deterministisk ZIP-hantering,
- derived model index för stora projekt,
- automatiserade tester och LLM-evals.

## För utvecklare

Börja med [utvecklardokumentationen](docs/developer/index.md).

Tekniska contracts finns därefter under `schemas/`, `scripts/`, `tests/`, `package/`, `metamodel/` och `knowledge/`.

Aktuell utvecklingsstatus: [STATUS.md](STATUS.md)

Ändringshistorik: [CHANGELOG.md](CHANGELOG.md)

## Paketversion

`0.46.0`

Genomförd utvecklingsplan: **46 / 48 steg**.

Nästa steg: **Steg 47 – Säkerställ bakåtkompatibilitet och migrering**.

## Release candidate

Första release candidate är **1.0.0-rc.7**. Se `release/RC-NOTES.md` och `release/RC-CHECKLIST.md`.

## GitHub release och distributionspaket

Repo-roten är katalogen där denna `README.md` ligger. GitHub Actions bygger fyra runtime-distributioner från samma canonical kontrakt:

- **Chat ZIP** — för uppladdning direkt i en ChatGPT-konversation.
- **Custom GPT** — för registrering i GPT Builder.
- **Claude Projects** — reduced parity med canonical behavior men utan antagen lokal tool-exekvering.
- **OpenCode** — equivalent peer runtime med typade ArchiMate-tools och explicit `projectRoot`.

Se [`docs/release-and-ci.md`](docs/release-and-ci.md).

`runtime/distribution-registry.yaml` är source of truth för aktiva runtimes och releaseartefakternas namn. Taggen styr versionsnumret; releasebygget skapar även `SHA256SUMS.txt`, `release-metadata.yaml` och `distribution-build-manifest.json`.

## GPT Byggaren 1.4 runtime migration

Ett separat runtime-migrationsspår har startats utan att ändra den ursprungliga produktplanens status 44/48. Målbilden är Chat ZIP, Custom GPT, Claude Projects och OpenCode från gemensamma plattformsneutrala contracts. Se [`docs/gpt-builder-1.4-runtime-migration.md`](docs/gpt-builder-1.4-runtime-migration.md).

## RC.5 runtime migration

GPT Byggaren 1.4-migreringen är genomförd för Chat ZIP, Custom GPT, Claude Projects och OpenCode. Full regression, fyr-runtime instruction adherence/parity och registry-driven release är del av RC.5.

## Real EA pilot

Step 45 har genomförts mot en verklig större EA-modell. Pilotresultat och identifierade
format-/rapportproblem finns i [`docs/real-ea-pilot-step45.md`](docs/real-ea-pilot-step45.md).

## Format 0.2

Step 46 har reviderat projektformatet utifrån real-EA-piloten. Nya projekt skapas som
format 0.2; format 0.1 kan fortfarande läsas. Viktiga ändringar är controlled impact themes,
normaliserad quality scoring, aggregerade relationship-coverage warnings, bredare
capability-realization och bounded query tool output.

Se [`docs/format-revision-step46.md`](docs/format-revision-step46.md).
