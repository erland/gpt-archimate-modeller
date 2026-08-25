# Conflict/duplicate handling – steg 28

## Syfte

Steg 28 formaliserar hur möjliga dubbletter och motstridiga uppgifter ska identifieras och lösas utan att GPT:n gör tysta merges eller väljer fakta godtyckligt.

## Konfliktklasser

Version 0.1 använder:

- `possible_duplicate`
- `identity_conflict`
- `type_conflict`
- `property_conflict`
- `evidence_conflict`
- `relationship_conflict`

### possible_duplicate

Två objekt kan representera samma verkliga koncept.

### identity_conflict

Samma stable ID används för inkompatibla objekt.

### type_conflict

Samma sannolika objekt har olika ArchiMate `type`.

### property_conflict

Samma objekt har olika värden för en property.

### evidence_conflict

Källor/assertions stödjer motsägande påståenden.

### relationship_conflict

Två relationer beskriver inkompatibel semantik för samma source/target-kontext.

## Resolution actions

Tillåtna beslut:

- `merge`
- `keep_separate`
- `prefer_existing`
- `prefer_incoming`
- `defer`
- `reject_incoming`

## Merge-regel

Merge får endast ske explicit.

Vid merge:

1. ett canonical stable ID väljs,
2. andra identifierare bevaras som aliases/external IDs när relevant,
3. relationer repointas explicit,
4. evidence från båda objekten bevaras,
5. konflikter i type/property/evidence måste lösas separat,
6. pensionerat ID återanvänds aldrig.

## Type conflict

Type får inte bytas via vanlig `update_element`.

Om samma verkliga koncept har modellerats med olika ArchiMate-typer måste resolutionen vara explicit:

- keep separate,
- reject incoming,
- eller skapa en strukturell migration/change sequence.

## Property conflict

Resolution måste ange värdestrategi:

```yaml
resolution:
  action: prefer_existing
```

eller:

```yaml
resolution:
  action: prefer_incoming
```

`defer` skapar/behåller issue och ändrar inte modellen.

## Evidence conflict

Motsägande evidence ska inte raderas bara för att ett värde väljs.

Konflikten bevaras genom:

- contradicting assertion,
- issue,
- resolution note.

## Duplicate candidates

Detektionssignaler kan vara:

- samma stable ID,
- samma normaliserade namn,
- samma namn + kompatibel typ,
- delade aliases,
- samma external ID,
- hög semantisk likhet.

En kandidat är inte samma sak som bekräftad dubblett.

## Resolution file

```yaml
resolution:
  id: RES-000001
  conflict_type: possible_duplicate
  existing_id: APP-000001
  incoming_id: APP-000002
  action: keep_separate
  reason: ...
```

## Stable resolution IDs

Format:

```text
RES-NNNNNN
```

RES är separat från CHG/ISS och beskriver beslut, inte modelländringen i sig.

## Workflow

1. detect,
2. classify,
3. propose resolution,
4. validate resolution,
5. translate resolution to change-set changes/issues,
6. apply through normal update workflow.

## Automatic behavior

Automatiskt tillåtet:

- detektera,
- klassificera,
- föreslå.

Inte automatiskt tillåtet:

- merge,
- delete,
- retype,
- discard evidence.

## Designprincip

Osäkerhet ska bli explicit modellstyrning, inte döljas i GPT:ns resonemang.
