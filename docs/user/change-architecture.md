# Baseline, target, transition och lifecycle

## Architecture states

Ett state beskriver vilka canonical objekt som ingår i ett visst arkitekturläge.

State-ID:

```text
STA-NNNNNN
```

Transition-ID:

```text
TRN-NNNNNN
```

## Baseline

Baseline är vald referens för nuläget. Den behöver inte vara synonym med alla objekt som finns i hela modellen.

## Target

Target beskriver ett avsett framtida läge.

Planerad target får inte beskrivas som redan genomförd verklighet.

## Transition

Använd transition när ett mellanläge är arkitekturellt relevant, exempelvis:

- parallell drift,
- tillfällig integration,
- stegvis migrering.

## Inheritance och delta

I stället för att kopiera hela modellen kan ett state ärva föregående state och beskriva:

- add_elements
- remove_elements
- add_relationships
- remove_relationships

## Object status

Ett objekt i state kan markeras:

- unchanged
- introduce
- change
- retire
- temporary

## Lifecycle kontra tid

Lifecycle är klassificering:

- planned
- active
- phase_out
- retired
- unknown

Datum ligger i temporal metadata.

Exempel: en aktiv applikation som ska avvecklas 2028 bör normalt fortfarande vara `active` eller `phase_out` idag, medan framtidsplanen uttrycks genom `planned_to` och target/transition state.

## Time basis

State kan vara:

- actual
- planned
- scenario

Det hjälper till att skilja observerat nuläge från planering och alternativa scenarier.
