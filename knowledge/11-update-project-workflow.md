# Update-project workflow

För befintligt projekt:

1. validera input-ZIP,
2. safe unpack,
3. compatibility/migration gate,
4. kontrollera current model version och change-set ID,
5. duplicate-candidate gate,
6. dry-run via samma `apply_changes`-motor,
7. real apply,
8. technical validation + quality + version history,
9. pack och final ZIP validation,
10. returnera komplett nytt ZIP.

Original-ZIP ändras aldrig.
Migration och duplicate override kräver explicit tillåtelse.
