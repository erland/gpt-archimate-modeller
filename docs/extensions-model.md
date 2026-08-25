# Extensions och organisationsspecifik information – steg 8

## Syfte

Extensions används för information som är viktig i praktiskt EA-arbete men som inte är en del av ArchiMate-kärnan.

Exempel:

- lifecycle,
- owner,
- criticality,
- information classification,
- strategic fit,
- technical debt,
- platform type.

ArchiMate-elementets `type` ska fortsatt beskriva det semantiska ArchiMate-konceptet. Extensions kompletterar objektet utan att ändra dess ArchiMate-identitet.

## Grundprincip

GPT:n får inte spontant skapa nya standardfält i `properties`.

Ett organisationsspecifikt property ska först vara deklarerat i:

```text
extensions/extensions.yaml
```

Exempel:

```yaml
extensions:
  lifecycle:
    description: Livscykelstatus
    value_type: enum
    allowed_values:
      - planned
      - active
      - phase_out
      - retired
    applies_to:
      kinds:
        - element
    required: false
```

Därefter kan ett objekt använda:

```yaml
properties:
  lifecycle: active
```

## Namnregler

Extension-ID:n:

- används som property-nyckel,
- ska vara `snake_case`,
- ska vara stabila,
- ska inte ändras bara för att visningsnamnet ändras.

Exempel:

```text
information_classification
technical_debt
strategic_fit
```

## Value types

Stödda typer i extension model 0.2:

- `string`
- `integer`
- `number`
- `boolean`
- `date`
- `enum`
- `list`
- `reference`

## Enum

```yaml
criticality:
  value_type: enum
  allowed_values:
    - low
    - medium
    - high
    - critical
```

## List

```yaml
supported_regions:
  value_type: list
  item_type: string
```

## Reference

Reference-property används när värdet ska peka på ett annat definierat objekt eller externt register, men inte är en ArchiMate-relation.

Exempel:

```yaml
service_owner:
  value_type: reference
  reference_kind: external
```

Det ska användas restriktivt. Om semantiken kan uttryckas som en ArchiMate-relation är relation normalt bättre.

## Applies to

Extensions kan begränsas.

Exempel:

```yaml
applies_to:
  kinds:
    - element
  archimate_types:
    - ApplicationComponent
    - Node
```

Tillåtna kinds:

- `element`
- `relationship`
- `project`

Om `archimate_types` saknas gäller extensionen alla objekt av vald kind.

## Required

```yaml
required: true
```

ska senare kunna användas av kvalitetsvalidatorn.

Ett required property betyder inte att gammal modell omedelbart måste bli ogiltig på syntaxnivå. Det kan i stället ge kvalitetsfel beroende på vald validation profile.

## Default value

```yaml
default: unknown
```

Default används endast vid uttrycklig projektpolicy. GPT:n ska inte tyst fylla default och presentera det som känd fakta.

## Evidence på properties

Extension-definitionen kan ange:

```yaml
evidence_required: true
```

Det betyder att ett satt property-värde bör ha en evidence assertion som stödjer:

```text
property:<extension-id>
```

Exempel:

```yaml
supports:
  - property:lifecycle
```

## Governance metadata

En extension kan innehålla:

```yaml
governance:
  status: active
  owner: EA
  introduced_in: "0.8.0"
```

Det gör det möjligt att styra vilka extensions som är officiella i projektet.

## Deprecated extensions

En extension kan markeras:

```yaml
governance:
  status: deprecated
  replaced_by: lifecycle_state
```

GPT:n ska då:

- inte använda den för nya objekt,
- inte automatiskt radera gamla värden,
- kunna migrera dem i framtida migreringssteg.

## Standard extensions i referensprofilen

Steg 8 introducerar följande generella exempelprofil:

- `lifecycle`
- `owner`
- `criticality`
- `information_classification`
- `strategic_fit`
- `technical_debt`

Dessa är exempel på projektprofil och inte nya ArchiMate-koncept.

## Separation från specializations

Extensions beskriver properties.

Specializations beskriver semantiska undertyper av ArchiMate-koncept.

Exempel:

```yaml
properties:
  lifecycle: active
```

är extension.

```yaml
specialization: Platform
type: Node
```

är specialization.

Dessa mekanismer ska inte blandas ihop.

## Validatorregler

Validatorn ska kontrollera:

- att property är deklarerad,
- korrekt value_type,
- enum-värden,
- applies_to,
- unknown properties,
- deprecated extension,
- list item type,
- evidence requirement där relevant.

## Strict och permissive mode

Två framtida valideringslägen definieras redan nu:

### strict

Okända properties ger fel.

### permissive

Okända properties ger varning.

Standard för GPT-redigering ska vara strict när projektformatet är fullt etablerat.

I steg 8 implementeras strict validation för referensprojekten.

## Designprincip

ArchiMate-kärnan ska förbli portabel även om organisationens extensionprofil förändras.
