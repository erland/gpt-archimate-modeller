# Modellkvalitet och impact analysis

## Modellkvalitet

Quality-checkern letar bland annat efter:

- isolerade element,
- capabilities utan realisering/support,
- saknad owner,
- svag/saknad evidence,
- otydliga source references,
- möjliga dubbletter,
- obalans mellan lager.

## Quality score

Score är en diagnostisk signal från aktiverade regler och deductions.

Den är **inte**:

- en EA-mognadsprocent,
- en revisionsrating,
- ett bevis på att arkitekturen är bra eller dålig.

## Dynamisk rapport

`model-quality-report` räknas fram från aktuell modell.

Den ska hållas separat från lagrade issues/observations.

## Impact analysis

Impact analysis traverserar modellerade relationer från startobjekt.

Stöd:

- incoming
- outgoing
- both
- max depth
- relationship filters
- paths
- certainty

## Direct och indirect

- direct = depth 1
- indirect = depth 2+

Det beskriver grafavstånd, inte säker verklig konsekvens.

## Certainty

Path certainty:

- strong
- moderate
- weak

Svag evidence på en relation gör hela vald path svagare.

## Viktig tolkningsregel

Att ett objekt är nåbart i grafen betyder modellerad beroendekontext. Det bevisar inte att en förändring definitivt kommer orsaka påverkan.

## Exempel

```bash
python scripts/impact_analysis.py project --seed APP-000123 --direction both --max-depth 3 --format markdown
```
