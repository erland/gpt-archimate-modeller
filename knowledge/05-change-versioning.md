# Change workflow and versioning

## Change set

Befintligt projekt ändras via deklarativt change set.

Viktiga operationer:

- add_element
- update_element
- deprecate_element
- remove_element
- add_relationship
- update_relationship
- remove_relationship
- add_source
- add_reference
- add_issue
- resolve_issue

## Säkerhet

- type change på befintligt element är förbjudet.
- update_relationship får inte ändra source/target.
- remove_element med relationer ska stoppas.
- expected_model_version fungerar som optimistic lock.
- preconditions används när gammalt värde är viktigt.

## Modellversion

SemVer:

PATCH:
- text,
- properties,
- evidence,
- source/reference,
- metadata,
- issues.

MINOR:
- strukturella modellförändringar,
- add/remove element,
- add/remove relation,
- deprecate.

MAJOR:
- explicit större brytande omstrukturering.

Högsta impact bland operationerna gäller.
Användare får höja men inte sänka computed impact.

## Historik

- `changes/index.yaml`
- `versioning/history.yaml`
- `CHANGELOG.md`

är separata men ska hållas konsistenta.
