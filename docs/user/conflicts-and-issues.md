# Konflikter, dubbletter, issues och observations

## Dubblett

Om ett nytt objekt liknar ett befintligt ska GPT:n identifiera `possible_duplicate`.

Standardbeteendet är att stoppa automatisk add/merge tills identiteten är avgjord.

## Konflikt

Exempel:

- samma ID men inkompatibel typ,
- olika owner med stark evidence,
- motsägande källor,
- konkurrerande relationships.

GPT:n kan klassificera och föreslå lösning men får inte automatiskt:

- merge:a,
- radera,
- retype:a,
- kasta evidence.

## Resolution actions

Stödda beslut omfattar:

- merge
- keep_separate
- prefer_existing
- prefer_incoming
- defer
- reject_incoming

Ett merge-beslut måste fortfarande materialiseras som explicita change operations.

## Issue

Använd när något kräver uppföljning, exempelvis:

- missing information,
- conflicting information,
- missing evidence,
- modeling question,
- unresolved duplicate.

## Observation

Använd för en noterad finding som inte nödvändigtvis kräver åtgärd.

## Quality findings

Dynamiska quality findings skapar inte automatiskt issues.

Om ett finding ska följas över tid behöver det först omvandlas till explicit issue/observation via change workflow.
