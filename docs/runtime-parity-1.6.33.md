# Runtimeparitet – GPT Byggaren 1.6.33 (PR #8)

## Verifieringsgrund

Kanonisk modell: `canonical/core.md` och fyra Skills. Projektets primära ArchiMate-version är 3.2. Fem aktiva peer-distributioner byggs med originalmotorn 1.6.33. Historisk Custom GPT är avaktiverad.

### Verifiering per mål

| Runtime | Arkiv byggt och originalvaliderat | Skill-resurser | Körbar projektlivscykel | Värdmiljötest |
| --- | --- | --- | --- | --- |
| Chat ZIP | PASS | PASS, fyra paketerade referens-Skills | PASS, direkt Python i isolerad testmiljö | Ej verifierat i Chat-host |
| Claude Project | PASS | Instruktioner och kontrakt verifierade i arkivet | Ej körbart Skill-hosttest; portabla referenser | Ej verifierat i Claude |
| Claude Skills | PASS | PASS, fyra Skills | PASS, direkt Python i isolerad testmiljö | Ej verifierat i Claude |
| OpenCode | PASS | PASS, fyra Skills | PASS, direkt Python i isolerad testmiljö | Ej verifierat i OpenCode |
| OpenAI Plugin | PASS | PASS, fyra Skills | PASS, direkt Python i isolerad testmiljö | Ej verifierat i Plugin-host |

PASS för projektlivscykel innebär att ett uppackat Skill kan skapa ett projekt, köra validering, paketera en ZIP och validera ZIP:en med Python och nödvändiga installerade paket. Detta bevisar **inte** att en runtime-host tillåter filskrivning, har rätt Python-beroenden, aktiverar Skills automatiskt eller hanterar bilagor.

## Verifierade kontrakt

- Samma canonical beteendekälla används för de fem distributionerna.
- Lokala statiska Python-importkedjor kontrolleras för varje Skill.
- Deklarerade skript, tillgångar och referenser granskas i byggda arkiv.
- Paketerade schema- och metamodelluppslag smoketestas i fyra Skill-baserade mål (16 kontroller).
- Projektgenerering, validering och ZIP-kontroll smoketestas i dessa fyra mål.
- Originalmotorns linter har noll fel och tre GP210-varningar om duplicerade fixture-Markdownfiler.

## Begränsningar som blockerar release-ready

1. Riktiga värdmiljötester för Chat, Claude, OpenCode och Plugin saknas. Claude Project kräver egen text-/bilageverifiering.
2. Dynamiska importer, externa verktyg, värdberoenden och all dataresursåtkomst är inte fullständigt verifierade.
3. Analysfråga och ArchiMate Model Exchange export/import har funktionstestats i fyra uppackade Skills-runtimer (CI 40680562341). Modelländring har därefter också verifierats i fyra uppackade Skill-arkiv; beteende i faktiska hosts återstår.
4. Ordinarie distributionsbygge och taggdriven releasekonfiguration har migrerats till 1.6.33. Torrkörning av release-artefakter är godkänd, men en verklig taggdriven release och uppladdning har inte körts.
5. Slutlig värdmiljöparitet och ändrings-/analys-/importexportbeteende är inte styrkt för varje host. Releasebeslutet är därför fortsatt BLOCKERAT.

## Slutsats

Det finns **paketeringsparitet för fem mål** och **isolera­de Python-projektflödestester för fyra mål**, inte belagd funktionell paritet i faktiska värdmiljöer. Migrationen är inte releaseklar och PR #8 ska inte mergas med hänvisning till den här rapporten.

## Slutbedömning 2026-10-28

Beslut: **NO-GO för release och merge just nu**. Godkända GitHub Actions på commit `984b224`: ordinarie CI `40675810402`, distributionsbygge `40675810408` och migrationsvalidering `40675810401`.

Det finns ingen evidens för ett faktiskt publicerat 1.6.33-taggreleaseflöde eller värdmiljökörning av alla fem mål. Ett enhetligt ja-beslut skulle överdriva testtäckningen. Nästa verifieringspaket bör omfatta värdmiljötest för varje stödjande runtime, särskild granskning av Claude Project samt representativa tester för modelländring, analys och import/export. Först därefter prövas merge/release.

## Utökad beteendeverifiering 2026-10-28

Körning `40680562341` verifierar samma projektflöde i Chat ZIP, Claude Skills, OpenCode och OpenAI Plugin som uppackade ZIP-arkiv: skapa projekt, exekvera elementfråga, exportera ArchiMate Model Exchange XML och importera XML till förhandsgranskning. Ordinarie CI och distributionsbygge på motsvarande commit är också godkända. Testerna styrker skriptbeteende i isolerad Pythonmiljö, inte native host-integration eller ändringshantering. Releasebeslut: **villkorat NO-GO** tills resterande värdtester och kontrollerat taggdrivet releaseflöde bedömts.

## Mergebedömning 2026-10-28 – efter utökade tester

**GO för merge av migrations-PR #8 som utvecklingssteg, men NO-GO för publicerad release.** Bedömningen ersätter ovanstående historiska NO-GO för merge, inte releasebegränsningarna.

De senaste kontrollerade körningarna på commit `bddf4a6` är godkända: ordinarie CI `40686039202`, distributionsbygge `40686039186` och migrationsvalidering `40686039203`. I de fyra uppackade Skill-runtimerna verifieras projektgenerering, ZIP-kontroll, modelländring med dry-run och apply, analysfråga samt Model Exchange-export/import. Claude Project är ett separat textbaserat distributionsmål och saknar motsvarande Python-hosttest.

Merge innebär att projektet kan fortsätta med verifiering av de byggda distributionerna; det innebär **inte** att plattformsspecifik funktion, dynamiska beroenden eller en riktig GitHub Release har verifierats. Behåll `release_ready: false`; publicera ingen release före separat kontroll och beslut.

## Fristående ArchiMate Engine ZIP

Utöver de fem peer-runtimepaketen och det genererade projektpaketet byggs nu en separat `archimate-modeller-engine-<version>.zip`. Den innehåller kanoniska Python-skript, CLI, `requirements.txt`, YAML-schema/metamodell, policyfiler och den serialiserade projektmallen. Byggkedjan verifierar Engine efter uppackning i en isolerad temporär katalog genom `python archimate_engine.py selftest` (skapa, validera, ändra, analysera, exportera/importera, paketera).

Chat ZIP, Plugin, Claude Skills och OpenCode innehåller dessutom `requirements.txt` med deklarerade Pythonberoenden. Deras instruktioner förklarar att skript är runtime-resurser och inte garanterat registrerade verktyg. **Engine är en lokal Python-runtime, inte en MCP-server.** Ett värdsystem utan Python, filskrivning eller möjlighet att installera beroenden kan inte exekvera Engine ZIP direkt. Faktisk värdmiljöparitet kräver fortsatt separat acceptanstest. `release_ready: false` gäller fortfarande till publiceringsbeslut.
