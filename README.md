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

`0.44.1`

Genomförd utvecklingsplan: **44 / 48 steg**.

Nästa steg: **Steg 45 – Real EA pilot**.


## Release candidate

Första release candidate är **1.0.0-rc.3**. Se `release/RC-NOTES.md` och `release/RC-CHECKLIST.md`.


## GitHub release och distributionspaket

Repo-roten är katalogen där denna `README.md` ligger. GitHub Actions bygger två releaseartefakter:

- **Custom GPT** — för registrering i GPT Builder.
- **Chat package** — för uppladdning direkt i en ChatGPT-konversation.

Se [`docs/release-and-ci.md`](docs/release-and-ci.md).
