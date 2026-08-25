# Release och kompatibilitet

## Inför en release

Minimikontroll:

1. `project.yaml` version/status uppdaterad.
2. `STATUS.md` uppdaterad.
3. `CHANGELOG.md` uppdaterad.
4. schemas valida.
5. reference projects passerar.
6. invalid fixtures ger förväntade fel.
7. automated test suite passerar.
8. LLM eval catalog validerar.
9. dokumentationsvalidatorer passerar.
10. release-ZIP integrity OK.

## Paketversion

GPT-/utvecklingspaketets version är separat från EA-projektens model version.

## Breaking changes

Breaking formatändring kräver:

- ny formatversion,
- migration,
- compatibility rule,
- fixtures,
- user/developer docs,
- regression.

## Unknown future versions

Får inte skrivas över automatiskt.

Read-only inspection kan tillåtas när säkert.

## Deprecated behavior

Om beteende ska fasas ut:

- dokumentera först,
- ge migration/alternativ,
- behåll backward compatibility under rimlig period,
- ta bort först i deklarerad breaking version.

## Release candidate

Steg 43 skapar första RC-paketet.
Steg 44 gör end-to-end GPT-test av RC:n.
