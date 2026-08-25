# Specialiseringar – steg 9

## Syfte

Specialiseringar gör det möjligt att använda organisationsspecifika semantiska begrepp utan att ändra ArchiMate-kärnan.

```yaml
specializations:
  Platform:
    base_type: Node
```

Ett element använder fortfarande en giltig ArchiMate-typ:

```yaml
- id: TEC-000001
  type: Node
  specialization: Platform
  name: Containerplattform
```

## Grundprinciper

- `type` är alltid en giltig ArchiMate-typ.
- `specialization` är valfri men måste vara deklarerad.
- Specialisering påverkar inte stabilt objekt-ID.
- Status och egenskaper ska normalt modelleras som extensions, inte specialiseringar.
- Specialiseringar får ärva från andra specialiseringar.
- Arv får inte bilda cykler.
- I modellversion 0.2 måste barn och förälder ha samma `base_type`.
- Relationer valideras i v1 enligt specializationens `base_type`.

## Definition

```yaml
Platform:
  label: Platform
  base_type: Node
  description: Organisationsspecifik teknisk plattform.
  inherits_relationships: true
  governance:
    status: active
    owner: EA
```

Barnspecialisering:

```yaml
IntegrationPlatform:
  base_type: Node
  parent_specialization: Platform
```

## Governance

Status:

- `active`
- `deprecated`
- `experimental`

Deprecated specialisering bevaras på befintliga objekt men ska inte användas för nya objekt.

## Standardprofil

- `Platform` → `Node`
- `IntegrationPlatform` → `Node`, parent `Platform`
- `BusinessApplication` → `ApplicationComponent`
- `SharedApplicationService` → `ApplicationService`

## Specialization kontra extension

Använd specialization för:

> Vad är detta för slags arkitekturobjekt i vår organisation?

Använd extension för:

> Vilken egenskap eller status har objektet?

Exempel:

```yaml
type: Node
specialization: Platform
properties:
  lifecycle: active
  criticality: high
```
