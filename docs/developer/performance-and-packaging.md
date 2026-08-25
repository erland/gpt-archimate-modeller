# Prestanda, ZIP och model index

## ZIP

`pack_project.py` ska ge deterministiskt ZIP-resultat för identiskt projektinnehåll.

Viktiga egenskaper:

- sorterade entries,
- fast timestamp,
- normaliserade permissions,
- required empty directories,
- manifest med SHA-256 + size.

## ZIP-säkerhet

Validatorn blockerar:

- duplicate entries,
- case collisions,
- path traversal,
- absolute/backslash paths,
- symlinks,
- special files,
- size/entry limits,
- extrem compression ratio.

Validering måste ske före extraction.

## Model index

`MODEL-INDEX.json` är en derived read cache.

Den innehåller logical model + fingerprint över canonical källor.

Användning:

```text
valid fingerprint → använd index
stale/missing/invalid → assemble YAML
```

## Prestandabeslut

Steg 40 visade att YAML-assemblering var flaskhalsen på stora modeller medan read-operations efter assembly var snabba.

Därför optimeras loading, inte canonical format.

## Regel

Optimera först efter mätning.

Persistent/derived acceleration får inte göra canonical YAML mindre korrekt eller svårare att migrera.
