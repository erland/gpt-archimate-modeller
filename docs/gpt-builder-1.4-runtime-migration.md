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
- **Steg 50 – Plattformneutrala runtime contracts** — genomfört; behavior/capability/artifact/workspace/tool finns i `runtime/runtime-contract.json` och separata schemas.
- **Steg 51 – Canonical ArchiMate tool contract** — genomfört; typad runtime-API-yta mappar canonical tools till utvalda Python-operationer.
- **Steg 52 – Claude Projects distribution** — genomfört; explicit reduced parity utan paketerade runtime-scripts.
- **Steg 53 – OpenCode distribution** — genomfört; root `AGENTS.md`, runtime snapshot och typade custom tools som projicerar canonical ArchiMate-tool-kontraktet.
- **Steg 54 – Registry-driven build och runtime-aware hygiene** — nästa steg.
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


## Steg 50 – Plattformneutrala runtime contracts

Steg 50 inför ett gemensamt kontraktslager som ligger mellan canonical ArchiMate-beteende
och runtime-specifika adaptrar.

### Kontrakt

- `behavior` — canonical instruktion och kritiska invariants.
- `capabilities` — krav på filåtkomst, exekvering, strukturerad data, persistent workspace och ZIP.
- `artifacts` — EA-projektpaket, validation evidence, change sets, reports, views och Model Exchange.
- `workspace_state` — projektfiler/projekt-ZIP är auktoritet; chat history är inte state.
- `tools` — abstrakta runtime-operationer, ännu utan runtime-specifik implementation.

### Viktig gräns

Steg 50 definierar endast den abstrakta tool-ytan. Kopplingen till konkreta Python-scripts
och typade argument görs i steg 51. Därmed undviks att dagens scripts råkar bli canonical
API bara för att de redan finns.

### Runtime compatibility

- Chat ZIP: implemented / equivalent
- Custom GPT: implemented / equivalent_with_platform_constraints
- Claude Projects: planned / reduced
- OpenCode: planned / equivalent
- OpenAI Plugin v1: not_planned / reduced


## Steg 51 – Canonical ArchiMate tool contract

Den abstrakta tool-ytan från steg 50 har nu konkretiserats i
`runtime/archimate-tool-contract.json`.

### Principer

- varje tool har stabil tool-id och typat input-schema,
- `projectRoot` är obligatoriskt och skiljer target workspace från runtime-paketet,
- endast utvalda runtime-scripts exponeras,
- development-, test- och release-scripts är inte del av API:t,
- path traversal är förbjuden,
- canonical mutation kräver approval=`ask`,
- outputgenerering som inte ändrar canonical model state kan vara approval=`allow`.

### Canonical runtime-API

Tool-kontraktet täcker:

- project/ZIP inspection,
- project/ZIP validation,
- new project,
- explicit project change,
- packaging,
- model query,
- impact analysis,
- model quality,
- report rendering,
- view export,
- Model Exchange export,
- Model Exchange staging preview.

Direkt Model Exchange merge exponeras inte som tool; import förblir staging/preview
i linje med canonical domänregler.

### Adapterregel

Runtime-adaptrar ska projicera detta kontrakt. De får inte betrakta generell shell-access
eller hela `scripts/` som canonical API.


## Steg 52 – Claude Projects distribution

Claude Projects är nu en byggbar distribution med **reduced parity**.

### Innehåll

Distributionen innehåller:

- `project-instructions.md` från canonical `gpt/SYSTEM_INSTRUCTION.md`,
- ett kuraterat Knowledge-set för modellering, format, evidence, change, validation och analys,
- snapshot av `runtime-contract.json`,
- snapshot av `archimate-tool-contract.json`,
- `compatibility.md`,
- README för installation/användning.

Den innehåller avsiktligt **inga Python runtime-scripts**. Tool-kontrakten är därför
transparens-/parityartefakter och får inte tolkas som att Claude Projects kan exekvera dem.

### Explicit reduced parity

Adaptern dokumenterar att den inte får anta:

- local command execution,
- deterministic project verification,
- workspace mutation,
- GitHub write actions.

Canonical behavior bevaras. EA-projektfiler/projekt-ZIP är workspace-file authority och
unrun verification måste förbli unrun; saknad exekvering får aldrig rapporteras som PASS.

### Release policy

Claude Projects är nu `implemented / reduced` i runtime compatibility. Full fyr-runtime
releasehantering införs först i migrationssteg 56.


## Steg 53 – OpenCode distribution

OpenCode är nu en byggbar peer runtime med target **equivalent**.

### Adapterstruktur

Distributionen innehåller:

- root `AGENTS.md` genererad från canonical systeminstruktion,
- `opencode.json` med explicit permission policy,
- `.opencode/runtime-contract.json`,
- `.opencode/tool-mapping.json`,
- `.opencode/tools/archimate.ts` med typade custom tools,
- runtime-implementation scripts under `runtime/scripts/`,
- runtime-relevant Knowledge.

OpenCode custom tools följer OpenCodes lokala TypeScript-toolmodell och använder
`tool.schema` för typade argument. Python-scripts anropas bakom wrappern; scriptsen
är implementation och blir inte själva implicit tool-yta.

### Workspace- och säkerhetsregler

- `projectRoot` är explicit på varje canonical tool.
- runtime-workspace och target EA-project är separata begrepp.
- path traversal utanför OpenCode-worktree blockeras av wrappern.
- direkt `bash`, `edit` och `write` är blockerade i adapterkonfigurationen.
- canonical mutation sker endast via deklarerade tools.
- `create_project` och `apply_project_change` kräver approval=`ask`.
- read/validate/query/analyze/present/export får köras utan mutationsapproval.

### Tool parity

Samtliga concrete tools från `runtime/archimate-tool-contract.json` projiceras till
OpenCode custom tools. Development-, test- och release-scripts exponeras inte.

OpenCode är därmed `implemented / equivalent` i runtime compatibility.
