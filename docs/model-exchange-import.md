# Utvärdering av ArchiMate Model Exchange-import – steg 20

## Slutsats

Import bör stödjas, men som **kontrollerad interoperabilitetsimport** och inte som en lossless round-trip-mekanism.

Model Exchange XML kan återskapa:

- model identifier/name/version,
- standard-ArchiMate element,
- standard-ArchiMate relationer,
- source/target,
- namn,
- documentation,
- generiska properties,
- våra egna specializations om de exporterats som `ea.specialization`,
- aliases,
- evidence status/confidence i sammanfattad form.

Model Exchange XML kan däremot inte säkert återskapa hela YAML-projektets:

- source/reference-modell,
- evidence assertions,
- exakta provenance-länkar,
- issues,
- change history,
- version history,
- query/report/view-definitioner,
- extension-definitioner,
- specialization-definitioner,
- ID-counters,
- original filpartitionering.

## Rekommenderad importmodell

Import ska därför ge ett nytt eller staging-baserat EA-projekt där importerad information markeras:

```yaml
evidence:
  status: imported
  confidence: unknown
```

om inget rikare evidence-lager kan rekonstrueras.

## Import modes

Version 0.1 definierar:

### new_project

Skapar ett nytt projekt från XML.

### merge_candidate

Läser XML och producerar ett import-resultat/diagnostik som senare kan användas av GPT:n för att skapa ett change set mot ett befintligt projekt.

Direkt automatisk merge till befintlig modell införs inte i steg 20.

## Stable IDs

Om Model Exchange identifier följer våra interna ID-regler, exempel:

```text
APP-000001
```

bevaras det.

Om identifier inte följer vår ID-strategi:

1. nytt internt ID allokeras,
2. XML identifier bevaras som `external_id`,
3. source/provenance markeras som import.

I steg 20 implementeras första delen endast för kompatibla IDs. Icke-kompatibla IDs rapporteras som needing-allocation i import preview.

## Element mapping

```xml
<element identifier="APP-000001" xsi:type="ApplicationComponent">
```

blir:

```yaml
id: APP-000001
type: ApplicationComponent
```

## Relationship mapping

```xml
<relationship
  identifier="REL-000001"
  source="APP-000001"
  target="STR-000001"
  xsi:type="Realization"/>
```

blir motsvarande YAML-relation.

## Properties

Vanliga Model Exchange-properties importeras till:

```yaml
properties:
```

Följande reserverade properties behandlas särskilt:

- `ea.specialization`
- `ea.aliases`
- `ea.evidence.status`
- `ea.evidence.confidence`
- `ea.original_id`
- `ea.original_model_id`

## Specializations

`ea.specialization` återställs till:

```yaml
specialization: Platform
```

men importen kan inte veta om definitionen finns i den lokala specialization-profilen.

Därför skapas import-warning om specialization saknar definition.

## Evidence

Exporterade:

- `ea.evidence.status`
- `ea.evidence.confidence`

kan återställas som sammanfattning.

Detaljerade assertions är förlorade i Model Exchange och importen skapar därför inte fabricerade assertions.

## Extensions

Importerade properties vars definition saknas lokalt betraktas som **undeclared extension candidates**.

Importeraren får inte automatiskt skapa en permanent extension-definition utan att detta granskas.

## Views/diagrams

Model Exchange kan innehålla views, men import av dem skjuts upp.

Skäl:

- vårt view-format är medvetet separerat från model exchange,
- layout/notation kan skilja kraftigt mellan verktyg,
- vi har redan egen view/draw.io-pipeline.

## Import preview

CLI:

```bash
python scripts/import_model_exchange.py model.xml --preview
```

Output:

```yaml
import_preview:
  model:
    id: ...
  elements: 3
  relationships: 1
  warnings:
    - ...
  unsupported:
    - ...
```

## Import till staging-projekt

```bash
python scripts/import_model_exchange.py model.xml   --output-project staging-project
```

Version 0.1 skapar ett enkelt split-project med:

- project.yaml,
- model/elements/*.yaml,
- model/relationships.yaml,
- extensions/extensions.yaml,
- extensions/specializations.yaml,
- issues/issues.yaml,
- identity/id-counters.yaml.

Detta är ett staging-projekt för vidare GPT-granskning.

## Designprincip

Import är aldrig auktoritativ bara för att XML-filen är syntaktiskt giltig.

Importerad information ska kunna granskas innan den blandas in i en etablerad EA-modell.
