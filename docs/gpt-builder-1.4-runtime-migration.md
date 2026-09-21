# GPT Byggaren 1.4.0 – runtime migration

## Syfte

Detta dokument beskriver ett separat runtime-migrationsspår för ArchiMate YAML EA GPT.
Den ursprungliga produktplanen **45–48** bevaras oförändrad; migrationsspåret får inte
användas för att påstå att Real EA pilot eller övriga produktsteg är genomförda.

Migreringen ska bevara projektets canonical domänbeteende:

- ArchiMate 3.2 som semantisk kärna,
- YAML som source of truth,
- stable IDs,
- evidence/provenance/confidence,
- change-set workflow för befintliga projekt,
- technical validation före write/package,
- komplett validerat projekt-ZIP efter modelländring,
- query/report/view-separation,
- Model Exchange som interoperabilitet, inte canonical källa.

## Steg 49 – Runtime assessment

### Nuvarande läge

Projektet har två produktionsnära distributioner:

1. **Chat package**
2. **Custom GPT**

Båda byggs deterministiskt från repo-källor och valideras i CI. Nuvarande
`main` hade vid assessment grön CI och grön distributionsbuild.

Canonical runtimebeteende finns huvudsakligen i:

- `gpt/SYSTEM_INSTRUCTION.md`
- `gpt/runtime-policy.yaml`
- maskinläsbara schemas/policies under projektets domänkataloger

Custom GPT använder en kondenserad instruktion och deterministiskt Knowledge-paket.

### Gap mot GPT Byggaren 1.4.0

Projektet saknar ännu ett explicit plattformsneutralt lager för:

- behavior contract,
- capability contract,
- artifact contract,
- workspace/state contract,
- tool contract,
- runtime compatibility/parity.

Nuvarande Chat- och Custom GPT-builders är runtime-specifika direkt från
repo-strukturen snarare än peer adapters från samma explicita runtime contracts.

Projektet saknar även:

- Claude Projects-adapter,
- OpenCode-adapter,
- fyr-runtime parity,
- registry-driven build/release för alla aktiverade runtimes.

## Runtimebedömning

| Runtime | Mål | Aktivera | Motivering |
| --- | --- | --- | --- |
| Chat ZIP | equivalent | Ja | Befintlig huvudruntime med komplett ZIP/toolchain. |
| Custom GPT | equivalent_with_platform_constraints | Ja | Befintlig och validerad; Code Interpreter/Data Analysis täcker kärnflödet inom plattformens gränser. |
| Claude Projects | reduced | Ja | Analys, modellering och filbaserat arbete är användbart, men lokal Python-exekvering, deterministisk validering, workspace-mutation och GitHub-write får inte antas. |
| OpenCode | equivalent | Ja | Mycket stark matchning mot projektets lokala Python-toolchain och portabla EA-workspace. |
| OpenAI Plugin v1 | reduced / not_planned | Nej | Projektets kritiska ZIP/workspace/tool-flöden kräver starkare lokal exekvering och persistent arbetsyta än vad som ska antas för Plugin v1. |

## Beslutad målbild

Aktiverade runtime-distributioner:

1. Chat ZIP
2. Custom GPT
3. Claude Projects
4. OpenCode

OpenAI Plugin v1 finns kvar i compatibility-bedömningen men byggs inte eller
publiceras så länge kritisk tool/workspace parity saknas.

## Särskilt beslut för OpenCode

ArchiMate-projektet har redan många konkreta runtime-operationer. OpenCode ska
därför **inte** bara få generell tillgång till hela `scripts/`.

Nästa tool-contract ska identifiera en kontrollerad runtime-API-yta, exempelvis:

- project inspect/read,
- new project,
- update/apply change set,
- validate project/package,
- query,
- render report,
- compile/export view,
- impact analysis,
- model quality report,
- Model Exchange import/export,
- package project.

Tools ska:

- härledas från canonical tool contract,
- ha typade argument,
- använda explicit `projectRoot`/workspace,
- bara exponera operations som behövs,
- kräva approval för mutation,
- inte ge modellen implicit åtkomst till development-/release-scripts.

## Parity-principer

Parity ska bedömas över fem dimensioner:

1. behavior
2. capability
3. artifact
4. workspace_state
5. tool

Claude Projects får vara **reduced** om begränsningarna är explicita och
canonical behavior, state authority och no-false-PASS bevaras.

## Fortsatt migrationsplan

Detta är ett separat runtime-spår. Den ursprungliga produktplanen 45–48
fortsätter att vara ofullbordad tills den faktiskt genomförs.

- **Steg 49 – Runtime assessment** — genomfört i denna ändring.
- **Steg 50 – Plattformneutrala runtime contracts** — behavior/capability/artifact/workspace/tool.
- **Steg 51 – Canonical ArchiMate tool contract** — normalisera runtime-API och tool boundaries.
- **Steg 52 – Claude Projects distribution** — explicit reduced parity.
- **Steg 53 – OpenCode distribution** — root `AGENTS.md`, runtime contract och typad tool projection.
- **Steg 54 – Registry-driven build och runtime-aware hygiene**.
- **Steg 55 – Fyr-runtime instruction adherence och parity**.
- **Steg 56 – Fyr-runtime CI, release och dokumentation**.
- **Steg 57 – Full regression och ny release candidate**.

## Klart-kriterier för steg 49

Steg 49 är klart när:

- nuläget är inventerat,
- befintlig canonical domänlogik är markerad som preserve-first,
- runtime-målbild är beslutad,
- OpenAI Plugin-beslutet är explicit,
- OpenCode tool-strategin är explicit,
- 50–57 är planerade utan att ändra status för produktsteg 45–48.
