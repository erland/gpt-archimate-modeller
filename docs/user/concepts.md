# Begrepp och mental modell

## Element

Arkitekturobjekt enligt ArchiMate, exempelvis Capability, BusinessProcess, ApplicationComponent eller Node.

## Relationship

En ArchiMate-relation mellan två objekt. Relationens riktning och typ har semantik och valideras.

## Stable ID

Objekt behåller samma ID över tid. Namn får ändras utan att identiteten byts.

Exempel:

```text
APP-000123
STR-000045
REL-000910
```

## Specialization

Organisationens precisering av en ArchiMate-typ.

Exempel: `Platform` kan vara en specialization av `Node`.

Kärntypen ligger kvar i `type`; specialization ersätter inte ArchiMate-semantiken.

## Extension

Deklarerat organisationsspecifikt attribut, exempelvis:

- owner
- lifecycle
- criticality
- information_classification

## Evidence

Beskriver varför ett påstående finns i modellen och med vilken säkerhet.

## Source och Reference

- Source = dokument, webbsida, intervju eller annan källa.
- Reference = exakt locator i källan, exempelvis sida, rubrik eller radintervall.

## Issue och Observation

- Issue = något som behöver hanteras eller beslutas.
- Observation = noterad iakttagelse som inte nödvändigtvis kräver åtgärd.

De är inte samma sak som canonical arkitekturfakta.

## Query

Read-only urval/analys av modellen.

## Report

Presentation av query-resultat.

## View

Visuell projektion av modellen.

## Baseline / Target / Transition

Architecture states ovanpå samma modell-ID:n:

- baseline = vald nulägesreferens,
- target = avsett framtida läge,
- transition = legitimt mellanläge.

## Temporal metadata

Skiljer faktisk giltighet från planering.

Exempel:

- `valid_from`
- `valid_to`
- `planned_from`
- `planned_to`
- `retired_on`

## Model index

`MODEL-INDEX.json` är ett deriverat prestandaindex. Det kan alltid byggas om från YAML och är aldrig source of truth.
