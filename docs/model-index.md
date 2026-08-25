# Model index – steg 40

## Beslut

Benchmark på 10 000 element / 9 999 relationer visade:

- query och impact är redan snabba när modellen är laddad,
- quality-check är acceptabel,
- YAML-assemblering är flaskhalsen.

Därför införs ett **deriverat läsindex**, inte ett nytt canonical format.

## MODEL-INDEX.json

Vid `pack_project.py` skapas automatiskt:

```text
MODEL-INDEX.json
```

Indexet innehåller:

- index-version,
- SHA-256 source fingerprint,
- antal source-filer,
- assemblerad logical model.

## Source of truth

Indexet är uttryckligen:

- derived,
- rebuildable,
- non-canonical,
- aldrig auktoritativt framför YAML.

Om fingerprint inte matchar ignoreras indexet och systemet faller tillbaka till YAML-assemblering.

## Fingerprint

Fingerprint beräknas deterministiskt över projektets YAML/JSON-källfiler med path + bytes.

`MODEL-INDEX.json` och `PACKAGE-MANIFEST.yaml` ingår inte i fingerprint.

## Pack

Varje packning bygger om indexet innan ZIP skapas.

Ett gammalt index i uppackad projektkatalog återanvänds aldrig av packern.

## Läsning

`model_loader.py` används av read-heavy operationer:

- query CLI,
- reports,
- views,
- impact analysis,
- model quality report,
- quality CLI.

## Säkerhet

Indexet används bara om source fingerprint fortfarande är giltigt.

Det betyder att man kan ändra YAML manuellt; nästa läsning upptäcker stale index och använder YAML.

## Tradeoff

Första packningen av en stor modell blir dyrare eftersom assemblering krävs för indexbygget.
Efter uppackning kan flera read-operationer däremot återanvända det förassemblerade JSON-indexet.

Det är rätt tradeoff för chat/ZIP-workflow där samma projekt ofta analyseras flera gånger efter uppladdning.
