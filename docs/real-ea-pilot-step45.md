# Step 45 – Real EA pilot

## Syfte

Step 45 prövar ArchiMate YAML EA GPT mot ett verkligt större EA-underlag och samlar
konkreta input till Step 46. Piloten ska inte dölja formatproblem genom att ändra schema
under själva pilotsteget.

## Pilotunderlag

Pilotfil: `it-formagemodell-standard-archimate-v1.11.0.zip`.

Filen kommer från tidigare verkligt EA-modelleringsarbete och är inte incheckad i detta repo.
Piloten kördes med den Chat ZIP som byggdes från `main` för `1.0.0-rc.5`.

### Storlek

- ZIP entries: 81
- filer: 65
- okomprimerad storlek: 12,502,193 byte
- element: 462
- relationer: 1,104
- sources: 21
- change sets: 14

Elementprofil:

- 330 Grouping
- 92 TechnologyService
- 13 Capability
- 11 Assessment
- 10 ApplicationComponent
- 6 Driver

Relationsprofil:

- 708 Association
- 293 Influence
- 103 Serving

Det ger ett realistiskt underlag med capabilities, IT-stöd, plattform-/produktgruppering,
tekniktjänster, drivkrafter, extern styrning och beroenden.

## Resultat

### ZIP contract

`validate_project_zip.py` accepterade original-ZIP:en utan fel eller varningar:

- status: valid
- 81 entries
- 65 filer

### Full project validation

Full unpack/project validation hittade ett blockerande formatgap:

`files.impact_themes` förekommer i pilotens `project.yaml`, men dagens project schema
tillåter inte fältet.

Detta är **inte** ändrat i Step 45. För att kunna fortsätta övriga pilotoperationer togs
endast filreferensen temporärt bort i en lokal pilotkopia. Själva pilotartefakten ändrades
inte och normaliseringen är inte en rekommenderad migration.

Efter denna temporära normalisering passerade technical validation med 0 errors men
1,040 warnings, samtliga `ARCH-REL-PAIR-UNCOVERED`.

### Relationship coverage

Den portabla exakta relationsmatrisen täcker inte stora delar av pilotens legitima
real-world-mönster, särskilt Association mellan TechnologyService, Capability och Grouping.
Warnings är icke-blockerande men volymen gör signalen svår att använda.

**Input till Step 46:** utvärdera hur relation-pair coverage kan breddas utan att göra
validatorn normativt överdriven.

### Quality report

Quality report kördes på den temporärt normaliserade kopian:

- score: 0.0
- findings: 442
- warnings: 128
- info: 314
- Q-CAP-001: 13
- Q-OWNER-001: 115
- Q-SRC-001: 314

Resultatet visar att kvalitetsprofilen är för hårt kalibrerad för importerade/verkliga
portföljmodeller där owner och source/evidence inte finns på varje objekt.

**Input till Step 46:** skilj bättre mellan modellkvalitet, metadata completeness och
evidence coverage så att ett verkligt importerat projekt inte kollapsar till score 0 trots
tekniskt giltig struktur.

### Queries

Standardqueries fungerade på modellen.

`capabilities-applications-platforms.yaml` returnerade 23 objekt:
13 Capability och 10 ApplicationComponent.

`count-by-type.yaml` fungerade men gav cirka 1.3 MB JSON för denna modell.

**Input till Step 46:** stora query-resultat behöver tydligare default summary/limit eller
ett workflow som undviker onödigt stora LLM-payloads.

### Reports

`standard/model-overview.yaml` renderades till cirka 121 KB Markdown.

`standard/capability-realization.yaml` kördes tekniskt korrekt men gav "Inga resultat",
trots att pilotmodellen innehåller capability/TechnologyService-samband. Standardrapporten
är för snäv för den semantik som används i verkliga IT-plattformsmodeller.

**Input till Step 46:** capability realization behöver stödja eller tydligt skilja flera
realiseringsmönster, inte anta en enda ApplicationComponent-baserad variant.

### Impact analysis

Piloten hittade ett implementationfel när två lika långa paths nådde samma objekt:

`'<' not supported between instances of 'dict' and 'dict'`

Orsaken var att `impact_analysis.py` jämförde två lists of dicts som tie-breaker.
Step 45 fixar detta med en deterministisk scalar path key och lägger till regressionstest.

Efter fixen gav analys från `STR-000012` på depth 2:

- impacted objects: 180
- direct: 27
- indirect: 153
- strong certainty: 165
- weak certainty: 15

### Model Exchange

ArchiMate Model Exchange-export lyckades och skapade cirka 5.26 MB XML.

Det bekräftar att den stora modellen kan exporteras genom den ordinarie runtime-toolchainen.

## Bedömning mot Step 45

### Vad ArchiMate uttrycker bra

- capabilities och strategiska drivers,
- TechnologyService-baserade plattformstjänster,
- IT-stöd som ApplicationComponent,
- externa styrsignaler som motivation/Assessment-specialisering,
- beroenden och påverkan,
- interoperabilitet via Model Exchange.

### Extensions/specializations som behövs

Pilotens specialiseringar fungerar för ITCapability, ITSupport och governance-liknande
koncept. Däremot visar `impact_themes` behov av ett kontrollerat, modellnära klassificerings-
koncept som dagens project schema inte har en tydlig plats för.

### Rapporter som saknas eller är för snäva

- capability realization för TechnologyService-/Association-baserade modeller,
- kompakt portfölj-/typöversikt för stora projekt,
- quality/evidence completeness med separat scoring.

### Var runtime/GPT-flödet gör fel

- ZIP contract kan vara valid samtidigt som full unpack/project validation blockerar på ett
  project-schemafält; statusen behöver vara lättare att förstå.
- impact analysis hade en riktig equal-depth path bug; fixad i Step 45.
- hög warning-volym från relation-pair coverage riskerar att dölja viktigare fynd.

### Arbetsflöden som är för tunga

- fulla query-resultat på stora modeller blir snabbt stora payloads,
- model-overview Markdown blir mycket omfattande,
- quality report behöver mer profil-/scope-styrning för importerade portföljmodeller.

## Slutsats och Step 46 backlog

Step 45 är genomfört med verkligt material och har gett konkreta format- och
användbarhetsfynd. Step 46 bör i första hand utvärdera:

1. canonical representation av controlled impact themes,
2. relation-pair coverage och warning strategy,
3. quality score decomposition för owner/source/evidence completeness,
4. capability-realization report semantics,
5. large-result defaults för query/report.

Inga av dessa formatfrågor ändras tyst i Step 45.
