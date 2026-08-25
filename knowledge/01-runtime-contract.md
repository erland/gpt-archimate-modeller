# Runtime contract

## Source of truth

YAML-projektet är source of truth.

Generated artefakter är derivat.

## När ett ZIP öppnas

1. validera ZIP-contract,
2. kontrollera path safety,
3. verifiera manifest/checksums,
4. kontrollera versioner,
5. migrera explicit om det behövs,
6. packa upp atomiskt,
7. teknisk validering,
8. quality check,
9. kontrollera versionshistorik,
10. först därefter write.

## Vid projektändring

Ändra via change set och returnera komplett projekt-ZIP.

Projektet är klart först när slut-ZIP validerar.

## Blocking

Blockera write vid:
- ZIP contract error,
- technical validation error,
- unsupported future format,
- failed migration.

Quality warnings är normalt inte blockerande.
