# Arkitekturöversikt

## Huvudlager

Paketet består av fem tydliga lager:

```text
Canonical EA data
    ↓
Assembly + validation
    ↓
Change/query/report/view/analysis engines
    ↓
Packaging/interoperability
    ↓
GPT runtime + Knowledge
```

## Canonical source of truth

YAML i projektet är canonical.

Det gäller framför allt:

- `project.yaml`
- `model/**`
- `sources/**`
- `extensions/**`
- `specializations/**`
- `issues/**`
- `architecture/**`
- `identity/**`
- `changes/**`
- `versioning/**`

Generated/derived data får aldrig bli enda platsen för arkitekturfakta.

## Derived data

Exempel:

- `MODEL-INDEX.json`
- exports
- rendered reports
- compiled views

Derived data måste kunna byggas om från canonical data.

## Modellseparation

Fyra koncept hålls strikt isär:

```text
model
query
report
view
```

Queries, reports och views får inte mutera modellen.

## Identity

Stable IDs är globalt stabila inom ett projekt och återanvänds aldrig för annan identitet.

Namnbyte är inte identitetsbyte.

## Evidence

Evidence är first-class metadata och används både på element och relationer.

Fakta, inferred/derived information och unknown state ska förbli explicit separerade.

## Change architecture

Baseline/target/transition ligger ovanpå samma canonical element-ID:n.

State-lagret duplicerar inte hela modellen.

## Runtimeprincip

GPT-runtime ska använda samma maskinläsbara regler som scripts och validators.

Narrativ dokumentation får aldrig vara den enda normativa definitionen av formatet.
