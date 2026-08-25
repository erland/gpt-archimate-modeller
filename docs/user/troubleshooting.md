# Felsökning och felmeddelanden

## `migration_required`

Projektet använder ett äldre, migrerbart format.

Åtgärd: tillåt migration i staging-kopian och skapa därefter ett nytt ZIP.

## `stale_change_set`

`expected_model_version` matchar inte aktuell modellversion.

Åtgärd: skapa om eller revidera change set mot aktuell version. Applicera inte det gamla change set:et ändå.

## Duplicate candidate / possible duplicate

Det nya objektet kan vara samma som ett befintligt.

Åtgärd: avgör om det ska:

- återanvända befintligt ID,
- merge:as genom explicit resolution/change,
- behållas separat.

## Relationship not allowed

Relationstypen är inte tillåten för aktuella ArchiMate-typer.

Åtgärd: kontrollera relationens semantik och source/target-riktning.

## Missing evidence / unsupported property

En uppgift saknar tillräckligt underlag.

Åtgärd: lägg till user confirmation, source/reference eller lämna uppgiften okänd.

## Unknown extension

En property är inte deklarerad i extension-profilen.

Åtgärd: använd befintligt attribut eller definiera extension explicit.

## Invalid specialization

Specializationens bastyp matchar inte elementets ArchiMate-typ.

Åtgärd: korrigera `type` eller specialization-definitionen.

## Temporal error

Exempel:

- `valid_from` efter `valid_to`,
- `planned_start` efter `planned_end`.

Åtgärd: korrigera tidsintervallet. Skilj planerade från faktiska datum.

## State inheritance cycle

Architecture states ärver cirkulärt.

Åtgärd: skapa en riktad state-kedja utan cykel.

## ZIP validation failed

Möjliga orsaker:

- checksum mismatch,
- duplicate/case-collision path,
- path traversal,
- symlink,
- för stor fil,
- extrem compression ratio,
- saknad canonical fil/katalog.

Åtgärd: använd senaste giltiga projekt-ZIP eller packa om projektet med `pack_project.py`.

## `MODEL-INDEX.json` stale

Detta är normalt efter manuell YAML-ändring.

Indexet ignoreras automatiskt och YAML används. Nästa packning bygger om indexet.

## Quality warning

Quality warnings blockerar normalt inte uppdatering.

Bedöm om warning ska:
- accepteras,
- åtgärdas,
- registreras som issue/observation.

## När du är osäker

Be GPT:n:

> Inspektera projektet utan att ändra det och förklara vilka validerings- eller kvalitetsproblem som finns.

Det är ett read-only arbetssätt.
