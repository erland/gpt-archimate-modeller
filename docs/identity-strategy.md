# ID-strategi och objektidentitet – steg 5

## Beslut

Projektet använder **stabila, betydelselösa men läsbara ID:n med typfamiljsprefix och löpnummer**.

Exempel:

```yaml
id: APP-000001
type: ApplicationComponent
name: Ärendehanteringssystem
```

ID:t beskriver inte objektets namn eller organisatoriska placering. Därför kan objektet byta namn, flytta mellan filer eller få nya properties utan att ID:t behöver ändras.

## Varför inte namn som ID?

Namn är instabila och kan:

- ändras,
- stavas olika,
- förekomma på flera språk,
- vara duplicerade,
- innehålla organisationsspecifik terminologi.

Namn ska därför aldrig vara primär identitet.

## Varför inte enbart UUID?

UUID är tekniskt robust men mindre praktiskt för:

- manuell felsökning,
- dialog med GPT,
- rapportering,
- läsning av YAML,
- referenser i chatt.

Därför används korta stabila ID:n med typfamiljsprefix.

## Standardprefix

| Familj | Prefix |
|---|---|
| Motivation | MOT |
| Strategy | STR |
| Business | BUS |
| Application | APP |
| Technology | TEC |
| Physical | PHY |
| Implementation & Migration | IMP |
| Composite / Other | CMP |
| Relationship | REL |
| Source | SRC |
| Issue | ISS |

Prefixet anger endast grov familj. Det får inte användas som ersättning för `type`.

## Format

Element:

```text
PREFIX-NNNNNN
```

Relationer:

```text
REL-NNNNNN
```

Källor:

```text
SRC-NNNNNN
```

Issues:

```text
ISS-NNNNNN
```

Exempel:

```text
APP-000042
REL-000381
SRC-000017
ISS-000004
```

## Stabilitet

När ett objekt väl har fått ett ID gäller:

- ID ändras inte vid namnbyte,
- ID ändras inte vid ändrad beskrivning,
- ID ändras inte vid flytt mellan partitioner,
- ID ändras inte när en alias läggs till,
- ID återanvänds inte efter borttagning.

## Identifiering av befintligt objekt

Innan GPT:n skapar ett nytt objekt ska den söka i följande ordning:

1. exakt ID om användaren anger ID,
2. exakt alias,
3. exakt namn inom kompatibel typ,
4. normaliserat namn,
5. nära namnmatchning,
6. extern identifierare i properties,
7. semantisk likhet i namn + beskrivning + typ.

Vid osäkerhet ska GPT:n skapa eller uppdatera ett issue i stället för att skapa en sannolik dubblett.

## Alias

Ett element kan ha flera alias:

```yaml
aliases:
  - ÄHS
  - Case Management System
```

Alias är sekundära identitetsnycklar och får inte vara globala primärnycklar.

## External IDs

Externa identiteter lagras i properties eller senare specialiserad struktur, exempelvis:

```yaml
properties:
  cmdb_id: CI-93841
  portfolio_id: APP-217
```

Ett externt ID får användas som stark matchningssignal men ersätter inte projektets stabila interna ID.

## Dubblettkandidater

Två element ska flaggas som möjlig dubblett om flera av följande gäller:

- samma normaliserade namn,
- samma alias,
- samma externa ID,
- samma typ och mycket lik beskrivning,
- samma relationella kontext.

Dubbletter ska inte automatiskt slås ihop utan tillräckligt stöd.

## Merge-princip

Vid bekräftad merge:

1. välj ett kanoniskt element-ID,
2. flytta relevanta alias och properties,
3. flytta evidens och källreferenser,
4. peka om relationer,
5. markera det andra objektet som merged/retired via change log eller senare lifecycle-stöd,
6. återanvänd aldrig det borttagna ID:t.

## ID-allokering

Projektet innehåller en separat räknarfil:

```text
identity/id-counters.yaml
```

Exempel:

```yaml
counters:
  APP: 42
  REL: 381
```

Nästa ID genereras som nästa heltal för prefixet.

Detta gör genereringen deterministisk och enkel att validera.

## Kollisionsregel

Om räknaren ligger efter faktiskt innehåll ska validatorn:

- upptäcka detta,
- inte återanvända befintligt ID,
- kunna föreslå en korrigering av räknaren.

## Filflytt

Elementets partition styrs av dess ArchiMate-familj/type, inte av ID:t. Ett objekt kan därför flyttas mellan filer om klassificering eller format ändras, utan att identiteten bryts.

## Versionsprincip

ID-strategi versioneras separat:

```yaml
identity:
  strategy_version: "0.1"
```

Det möjliggör framtida migrering utan att nuvarande ID:n ändras.
