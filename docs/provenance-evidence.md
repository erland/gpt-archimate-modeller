# Provenance- och evidensmodell – steg 6

## Syfte

Provenance- och evidensmodellen ska göra det möjligt att förstå:

- var information kommer ifrån,
- om informationen är explicit dokumenterad eller infererad,
- hur säker informationen bedöms vara,
- vilka källor som stödjer ett element eller en relation,
- om flera källor stödjer eller motsäger varandra,
- om ett påstående har skapats av användaren, import, dokumenttolkning eller GPT-slutsats.

Detta är centralt eftersom modellen ska kunna växa successivt genom dialog utan att verifierad information blandas ihop med antaganden.

## Separation mellan source och evidence

### Source

En `source` beskriver **underlaget**.

Exempel:

- dokument,
- webbsida,
- intervju,
- workshop,
- användaruppgift,
- systemexport.

### Evidence

`evidence` beskriver **hur ett specifikt modellelement eller en relation stöds av underlaget**.

Ett element kan därför ha flera evidensposter från flera olika källor.

## Ny modell i version 0.2

Tidigare format hade en enda förenklad evidence-post direkt på objektet.

Från och med formatets evidence-version 0.2 används:

```yaml
evidence:
  status: document_confirmed
  confidence: high
  assertions:
    - id: EV-000001
      kind: explicit
      source_refs:
        - SRC-000002
      supports:
        - existence
        - name
        - description
      note: Systemet finns explicit beskrivet i systemkatalogen.
```

## Evidence status

Objektnivån har en sammanvägd status.

Tillåtna värden:

- `user_confirmed`
- `document_confirmed`
- `imported`
- `inferred`
- `mixed`
- `unknown`

### mixed

`mixed` används när olika delar av objektinformationen har olika evidensgrund.

Exempel:

- existensen är dokumenterad,
- owner är användarbekräftad,
- relationen till en capability är infererad.

## Confidence

Tillåtna nivåer:

- `high`
- `medium`
- `low`
- `unknown`

Confidence beskriver tillförlitlighet i modellens aktuella tolkning och är inte samma sak som source quality.

## Evidence assertion

Varje assertion beskriver en konkret evidensgrund.

```yaml
- id: EV-000012
  kind: explicit
  source_refs:
    - SRC-000004
  supports:
    - existence
    - lifecycle
  confidence: high
```

### Assertion kind

- `explicit`
- `user_statement`
- `imported`
- `derived`
- `inferred`
- `contradicting`

## supports

`supports` anger vilka delar av objektet evidensen gäller.

Vanliga värden:

- `existence`
- `type`
- `name`
- `description`
- `relationship`
- `property:<property-name>`

Exempel:

```yaml
supports:
  - existence
  - property:lifecycle
```

## Inferens

Infererad information måste innehålla:

- `kind: inferred` eller `derived`,
- confidence,
- minst en source_ref om inferensen bygger på konkret underlag,
- en kort `reason`.

Exempel:

```yaml
- id: EV-000013
  kind: inferred
  source_refs:
    - SRC-000001
    - SRC-000002
  supports:
    - relationship
  confidence: medium
  reason: >
    Applikationen beskrivs som systemstöd för den aktuella förmågan,
    men relationen uttrycks inte explicit i källorna.
```

## Derived kontra inferred

### derived

Använd när information följer deterministiskt eller nästan deterministiskt från strukturerad information.

Exempel:

- en lifecycle-rapport klassificerar objektet som avvecklingskandidat utifrån ett explicit datum.

### inferred

Använd när GPT:n gör en semantisk slutsats.

Exempel:

- två beskrivningar antyder att applikationen realiserar en capability.

## Contradicting evidence

Motstridig information tas inte bort.

Exempel:

```yaml
- id: EV-000021
  kind: contradicting
  source_refs:
    - SRC-000010
  supports:
    - property:owner
  confidence: high
  note: Källan anger en annan ägare än nuvarande modellvärde.
```

Vid relevant konflikt ska ett issue kunna skapas.

## Evidence ID

Assertions använder stabila ID:n:

```text
EV-NNNNNN
```

Evidence-ID:n är lokala för projektet men globala inom projektpaketet.

En separat räknare `EV` läggs därför till i identity-strategin.

## Objektets sammanvägda status

GPT:n ska använda följande princip:

1. Om all viktig information är explicit dokumenterad → `document_confirmed`.
2. Om allt bygger på användarens uttryckliga uppgift → `user_confirmed`.
3. Om objektet kommer direkt från strukturerad import → `imported`.
4. Om objektets existens eller centrala semantik huvudsakligen är infererad → `inferred`.
5. Om flera former kombineras → `mixed`.
6. Om evidens saknas → `unknown`.

## Evidens för relationer

Relationer ska hanteras minst lika strikt som element.

Det är vanligt att element är väl dokumenterade medan relationen mellan dem bara är en slutsats.

Exempel:

```yaml
evidence:
  status: inferred
  confidence: medium
  assertions:
    - id: EV-000031
      kind: inferred
      supports:
        - relationship
      source_refs:
        - SRC-000004
        - SRC-000007
      reason: Båda källorna beskriver ett tydligt funktionellt beroende.
```

## Evidence coverage

Validatorn ska kunna flagga:

- objekt helt utan evidence,
- infererade assertions utan reason,
- source_refs som inte existerar,
- assertions utan `supports`,
- duplicerade EV-ID:n,
- evidence-status som inte är konsistent med assertions.

## Informationsbevarande

GPT:n får inte:

- skriva över explicit evidens med inferens,
- ta bort motstridiga assertions utan användarbeslut,
- höja confidence utan grund,
- ändra `inferred` till `document_confirmed` utan ny explicit källa.

## Kommande steg

Steg 7 fördjupar själva source- och referensmodellen.

Steg 11 kommer senare att använda evidence coverage som kvalitetsmått.
