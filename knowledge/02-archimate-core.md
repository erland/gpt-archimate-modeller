# ArchiMate core

## Semantisk kärna

Projektet använder ArchiMate 3.2 som semantisk kärna.

`type` ska alltid vara en standard-ArchiMate-typ.

Organisationens egna begrepp uttrycks med:
- `specialization` för semantisk underkategori,
- extension/property för klassificering, status och metadata.

## Element

Paketet innehåller 60 standardelement och Junction.

Elementmetadata finns i:

- `metamodel/elements.yaml`
- `metamodel/connectors.yaml`
- `metamodel/layers.yaml`
- `metamodel/aspects.yaml`

## Relationer

Relationstyper:

- Composition
- Aggregation
- Assignment
- Realization
- Serving
- Access
- Influence
- Association
- Triggering
- Flow
- Specialization

Definitioner:
- `metamodel/relationships.yaml`

Exakt pair coverage finns stegvis i:
- `metamodel/relationship-matrix.yaml`

Om ett pair saknas där ska GPT:n inte låtsas att paketet har full normativ coverage.

## Specialization

Exempel:

```yaml
type: Node
specialization: Platform
```

Specialization får inte ersätta ArchiMate `type`.

## Extensions

Status och klassificering ska normalt vara properties, exempel:

- lifecycle
- owner
- criticality
- information_classification
- strategic_fit
- technical_debt
