# Change, migration och versionering

## Change set

Modellmutation ska ske genom explicit change set.

Viktiga egenskaper:

- stable change ID,
- expected model version,
- preconditions,
- operations,
- dry run,
- atomic apply,
- validation efter apply.

## Optimistic locking

`expected_model_version` förhindrar att stale change sets appliceras på nyare modell.

## Duplicate gate

`add_element` ska passera identity/duplicate checking innan nytt ID accepteras.

Ingen auto-merge.

## Migration

Migration förändrar **format**, inte verksamhetsarkitekturens semantik.

Migration ska:

- vara explicit,
- köras i staging,
- kunna previewas,
- dokumenteras i migration history,
- inte ändra input-ZIP in-place.

## Versionsnivåer

Model SemVer används ungefär så här:

- PATCH: informativ ändring
- MINOR: strukturell modelländring
- MAJOR: explicit breaking modelländring

Högsta relevanta impact styr.

## Changelog

Changelog ska beskriva observerbar modell-/paketförändring, inte implementation noise.

## Historik

Bevara:
- model version history,
- change-set archive/index,
- migration history.

History ska vara append-oriented och spårbar.
