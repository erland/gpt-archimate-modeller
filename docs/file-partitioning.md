# Filindelning för EA-projektpaket – beslut i steg 4

## Beslut

Projektet använder en **hybridindelning**.

Det innebär:

- `project.yaml` är ett litet manifest och innehåller projektmetadata samt pekare till projektets datafiler.
- ArchiMate-element delas upp i ett begränsat antal filer efter domän/lager.
- Relationer hålls i en gemensam fil i första versionen.
- Sources, extensions, specializations och issues ligger i separata filer.
- Queries, reports och views ligger i egna kataloger när de införs.
- En assembler kan läsa alla delar och skapa samma logiska modell som det monolitiska formatet från steg 3.

## Standardstruktur

```text
ea-project/
├── project.yaml
├── model/
│   ├── elements/
│   │   ├── motivation.yaml
│   │   ├── strategy.yaml
│   │   ├── business.yaml
│   │   ├── application.yaml
│   │   ├── technology.yaml
│   │   ├── physical.yaml
│   │   ├── implementation-migration.yaml
│   │   └── composite.yaml
│   └── relationships.yaml
├── sources/
│   └── sources.yaml
├── extensions/
│   ├── extensions.yaml
│   └── specializations.yaml
├── issues/
│   └── issues.yaml
├── queries/
├── reports/
├── views/
├── exports/
└── CHANGELOG.md
```

## Varför inte en enda YAML-fil?

En enda fil är enkel i mycket små modeller, men blir sämre när modellen växer:

- LLM:n måste läsa och skriva om större mängder irrelevant information.
- små ändringar skapar stora diffar,
- människor får svårare att navigera,
- risken ökar att orelaterade delar förändras av misstag.

## Varför inte en fil per objekt?

En fil per objekt ger motsatt problem:

- mycket stort antal små filer,
- dyr kataloginventering,
- fler filoperationer,
- sämre överblick,
- relationer och närliggande objekt blir fragmenterade.

## Varför dela element per domän/lager?

Det ger en bra balans:

- filerna är semantiskt sammanhållna,
- ett typiskt ändringsarbete behöver bara läsa ett fåtal filer,
- det är lätt att hitta rätt område,
- filantalet förblir litet,
- formatet kan senare sharda en enskild domän om modeller blir mycket stora.

## Varför hålls relationer samlade initialt?

Relationer går ofta tvärs över lager. Om de delas per lager uppstår snabbt frågor om vilken fil en tvärgående relation tillhör.

Därför används:

```text
model/relationships.yaml
```

som standard i v1.

Om skalbarhetstest senare visar att relationsfilen blir för stor kan den delas enligt en separat, explicit shardingstrategi. Det ska inte göras i förtid.

## Logiskt format kontra fysisk paketering

Det finns två separata nivåer:

### Logiskt modellformat

`schemas/ea-project.schema.json`

Det beskriver hur den **sammansatta modellen** ser ut:

```yaml
model:
  elements: [...]
  relationships: [...]
```

### Fysisk paketering

`schemas/ea-package.schema.json`

Det beskriver var modellens delar ligger i ZIP-paketet.

Det gör att rapportmotor, queries och analyser kan arbeta mot en enhetlig logisk modell även om den lagras i flera filer.

## Standardpartitioner

Följande partitioner används:

| Partition | Innehåll |
|---|---|
| motivation | Motivation-element |
| strategy | Strategy-element |
| business | Business-lager |
| application | Application-lager |
| technology | Technology-lager |
| physical | Physical-element |
| implementation-migration | Implementation & Migration |
| composite | Grouping, Location och andra composite/other-element |

## Filformat

Varje elementfil har formen:

```yaml
elements:
  - id: APP-001
    type: ApplicationComponent
    name: Exempel
```

Relationsfil:

```yaml
relationships:
  - id: REL-001
    type: Serving
    source: APP-001
    target: CAP-001
```

Sources:

```yaml
sources: []
```

Extensions:

```yaml
extensions: {}
```

Specializations:

```yaml
specializations: {}
```

Issues:

```yaml
issues: []
```

## Manifest

`project.yaml` anger uttryckligen vilka filer som är del av modellen.

Exempel:

```yaml
format_version: "0.1"
package_layout_version: "0.1"

project:
  id: example
  name: Exempel
  model_version: "0.1.0"
  archimate_version: "3.2"

files:
  element_partitions:
    - id: application
      path: model/elements/application.yaml
  relationships: model/relationships.yaml
  sources: sources/sources.yaml
  extensions: extensions/extensions.yaml
  specializations: extensions/specializations.yaml
  issues: issues/issues.yaml
```

## Skalbarhetsregel

I v1 gäller:

- använd standardpartitionerna,
- skapa inte spontant nya partitioner,
- sharda inte relationer utan en formatändring,
- lägg inte ett element i flera filer,
- manifestet är auktoritativt för vilka filer som ingår.

## LLM-arbetsprincip

Vid en lokal ändring bör GPT:n i första hand läsa:

1. `project.yaml`,
2. relevant elementpartition,
3. `model/relationships.yaml` om relationer påverkas,
4. relevanta source/extension-filer.

Hela modellen behöver inte läsas om ändringen kan genomföras säkert lokalt.

## Kompatibilitet

Det monolitiska exempelprojektet från steg 3 behålls som ett test av det logiska formatet.

Från steg 4 är den rekommenderade **projektpaketeringen** den uppdelade strukturen.
