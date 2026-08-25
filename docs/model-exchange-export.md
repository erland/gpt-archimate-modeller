# ArchiMate Model Exchange-export – steg 19

## Syfte

Steg 19 exporterar den kanoniska YAML-modellen till The Open Group ArchiMate Model Exchange File Format.

Exporten är avsedd för interoperabilitet med ArchiMate-medvetna verktyg. Exchange-formatet är ett transportformat och ersätter inte projektets YAML som source of truth.

## ArchiMate-version

Projektets semantiska profil är ArchiMate 3.2.

The Open Group anger att samma Model Exchange File Format-standard används för ArchiMate 3.1 och 3.2.

Exporten använder:

```text
Namespace:
http://www.opengroup.org/xsd/archimate/3.0/

Schema:
https://www.opengroup.org/xsd/archimate/3.1/archimate3_Model.xsd
```

XSD-versionen är 3.1 även när modellen semantiskt använder ArchiMate 3.2.

## Scope i version 0.1

Exporteras:

- model identifier,
- model name,
- model version,
- model documentation,
- elements,
- element names,
- element descriptions/documentation,
- relationships,
- relationship names/documentation,
- source/target,
- ArchiMate types via `xsi:type`,
- organizationsspecifika properties,
- specialization som property,
- aliases som property,
- evidence-status/confidence som properties.

Exporteras inte ännu:

- sources/references som separata exchange-formatobjekt,
- views,
- diagram,
- organizations/folder trees,
- full provenance assertion graph,
- extensions som egen metamodelstruktur.

## Element

YAML:

```yaml
- id: APP-000001
  type: ApplicationComponent
  name: Ärendehanteringssystem
```

XML:

```xml
<element identifier="APP-000001" xsi:type="ApplicationComponent">
  <name xml:lang="sv">Ärendehanteringssystem</name>
</element>
```

## Relationship

YAML:

```yaml
- id: REL-000001
  type: Realization
  source: APP-000001
  target: STR-000001
```

XML:

```xml
<relationship
  identifier="REL-000001"
  source="APP-000001"
  target="STR-000001"
  xsi:type="Realization"/>
```

## Properties

ArchiMate exchange-formatet använder property definitions.

YAML:

```yaml
properties:
  lifecycle: active
  owner: Applikationsteam
```

ger konceptuellt:

```xml
<properties>
  <property propertyDefinitionRef="propdef-lifecycle">
    <value>active</value>
  </property>
</properties>

<propertyDefinitions>
  <propertyDefinition identifier="propdef-lifecycle" type="string">
    <name>lifecycle</name>
  </propertyDefinition>
</propertyDefinitions>
```

Alla organisationsspecifika properties exporteras som `string` i version 0.1 för maximal interoperabilitet.

## Specialization

Projektets egna specializations är inte nya ArchiMate-elementtyper.

Därför exporteras:

```yaml
type: Node
specialization: Platform
```

som:

- `xsi:type="Node"`
- property `ea.specialization=Platform`

Det bevarar korrekt ArchiMate-semantik.

## Evidence

För att inte tappa all spårbarhetsinformation exporteras ett minimalt sammanfattat lager:

- `ea.evidence.status`
- `ea.evidence.confidence`

Detaljerade assertion IDs, source refs och reference refs förblir i YAML-projektet.

## Identifierare

Stabila EA-ID:n bevaras när de redan är giltiga XML `xs:ID`.

Om en framtida identifierare inte är XML-kompatibel saneras den deterministiskt för exchange-filen. Originalvärdet läggs då som property `ea.original_id`.

## CLI

```bash
python scripts/export_model_exchange.py   examples/ea-project-split   --output exports/model-exchange.xml
```

## Validering

Intern validator:

```bash
python scripts/validate_model_exchange.py exports/model-exchange.xml
```

Den kontrollerar:

- XML well-formedness,
- rätt namespace,
- model identifier/name,
- unika IDs,
- relationship source/target,
- kända ArchiMate element- och relationstyper,
- propertyDefinitionRef.

Den är inte en ersättning för officiell XSD-validering i ett externt ArchiMate-verktyg.

## Designprincip

YAML förblir source of truth.

Model Exchange XML är en genererad interoperabilitetsartefakt.
