# Förändringsflöde och säker modellredigering – steg 12

## Syfte

GPT:n ska inte redigera YAML-filer ad hoc.

Varje förändring ska följa ett kontrollerat flöde:

1. läs projekt,
2. validera nuläge,
3. identifiera berörda objekt,
4. sök efter befintliga objekt och dubblettkandidater,
5. skapa ett change set,
6. applicera change set,
7. validera resultat,
8. kör kvalitetskontroll,
9. uppdatera projektmetadata,
10. uppdatera changelog,
11. returnera komplett projekt-ZIP.

## Change set

Ett change set är en maskinläsbar beskrivning av avsedd förändring.

Exempel:

```yaml
change_set:
  id: CHG-000001
  title: Lägg till containerplattform
  created: 2026-08-25
  operations:
    - op: add_element
      element:
        id: TEC-000002
        type: Node
        specialization: Platform
        name: OpenShift

    - op: update_element
      id: TEC-000001
      set:
        properties.lifecycle: phase_out
```

## Varför change set?

Det ger:

- tydlig skillnad mellan avsikt och resultat,
- möjlighet att validera före applicering,
- möjlighet att testa idempotens,
- spårbarhet,
- enklare rollback i framtiden,
- enklare GPT-arbetsprocess.

## Operationer i version 0.1

### add_element

Lägger till ett nytt element.

Regler:

- ID måste vara nytt.
- Typ måste vara giltig.
- relevant partition avgörs av type.
- dubblettkontroll ska göras före applicering.

### update_element

Uppdaterar ett befintligt element.

Stabilt ID bevaras.

Tillåtna ändringar kan exempelvis vara:

- name
- description
- aliases
- properties
- evidence
- metadata
- specialization

### deprecate_element

Markerar ett element för avveckling genom extension/property när sådan finns.

Detta är inte samma sak som fysisk delete.

### remove_element

Fysisk borttagning.

Får endast ske när:

- användaren uttryckligen begär borttagning,
- inga kvarvarande relationer blir brutna,
- change set anger explicit `reason`.

### add_relationship

Skapar ny relation.

Source och target måste finnas.

### update_relationship

Ändrar relationsegenskaper/evidence men inte implicit source/target utan uttrycklig operation.

### remove_relationship

Tar bort relation.

### add_source

Skapar ny source.

### add_reference

Skapar en exact reference.

### add_issue

Skapar öppet issue för osäkerhet eller konflikt.

### resolve_issue

Markerar issue resolved.

## Inga tysta destruktiva ändringar

GPT:n får inte:

- skriva över ID,
- byta elementtyp utan explicit operation,
- radera evidence,
- radera sources/references som fortfarande används,
- merge:a element automatiskt,
- ta bort relationer som bieffekt av rename,
- ersätta infererad information med bekräftad utan ny evidens.

## Rename

Rename är `update_element`.

ID ändras inte.

Alias kan vid behov kompletteras med tidigare namn.

## Type change

Ändring av ArchiMate-typ är semantiskt stor.

I version 0.1 förbjuds vanlig `update_element` att ändra `type`.

En framtida explicit operation `retype_element` kan införas om behov uppstår.

## Dubblettkontroll före add

Före `add_element` ska GPT:n kontrollera:

1. exact ID,
2. exact alias,
3. exact name + compatible type,
4. normalized name,
5. external identifier,
6. semantic similarity.

Vid stark kandidat ska add stoppas eller issue skapas.

## Preconditions

Operation kan ange preconditions.

Exempel:

```yaml
preconditions:
  - path: properties.lifecycle
    equals: active
```

Om nuläget inte matchar ska operationen inte appliceras.

Det skyddar mot att ett change set appliceras mot fel projektversion.

## Expected model version

Change set ska kunna ange:

```yaml
expected_model_version: "0.4.0"
```

Om projektets modellversion avviker stoppas applicering.

## Dry-run

`apply_changes.py` ska stödja dry-run.

Dry-run:

- läser,
- verifierar,
- simulerar,
- validerar,
- skriver inte projektfiler.

## Transactionell princip

Om någon operation misslyckas ska ingen delvis modifierad projektmodell lämnas som godkänt resultat.

Scriptet arbetar därför mot en temporär kopia och skriver först tillbaka efter godkänd validering.

## Changelog

Varje applicerat change set ska generera en post som minst anger:

- change set ID,
- titel,
- datum,
- operations,
- berörda IDs.

## Change history

Projektet får:

```text
changes/
├── CHG-000001.yaml
└── CHG-000002.yaml
```

Detta är projektets egen ändringshistorik och har inget beroende till Git.

## Säker standard

GPT:n ska normalt:

- föredra update framför add om objekt redan finns,
- föredra deprecate framför delete,
- skapa issue vid osäkerhet,
- inte applicera ett change set som gör teknisk validering sämre,
- rapportera nya kvalitetsvarningar som uppstår.

## Modellversion

Efter lyckad förändring uppdateras `model_version`.

I steg 12 används enkel semver-hjälpfunktion:

- add/remove semantic object: minor bump
- metadata/property/evidence-only change: patch bump

Detta kan finjusteras i steg 13.
