# Scheman och formatutveckling

## Schemafiler

Maskinläsbara contracts finns främst i:

```text
schemas/
metamodel/
package/
extensions/
specializations/
```

## Formatversion kontra modellversion

Håll isär:

- project/package format version,
- model version,
- GPT package version.

De beskriver olika saker och ska inte kopplas implicit.

## Backward compatibility

Vid en formatändring:

1. klassificera om den är backward-compatible,
2. uppdatera schema,
3. uppdatera assembler/validator,
4. uppdatera template/reference projects,
5. lägg migration om befintliga projekt annars bryts,
6. lägg fixtures,
7. uppdatera docs/Knowledge,
8. kör hela regressionen.

## Schemaförändringar

Undvik att göra ett befintligt optional field required utan migration.

Undvik att byta semantik för ett existerande field-name.

Vid större semantisk ändring är ny formatversion bättre än dold reinterpretation.

## Extensions

Organisationsegna properties måste deklareras.

Undvik:
- fria ad hoc-properties,
- att använda extensions för att ersätta ArchiMate core semantics.

## Specializations

Specialization ska alltid ha kompatibel ArchiMate-bastyp.

Kärntypen i `type` ska vara kvar.

## Stable IDs

Ny objekttyp/prefix kräver:
- prefix-regel,
- counter,
- schema,
- validation,
- fixtures,
- migration vid behov.

## Derived formats

`MODEL-INDEX.json` och exports ska inte driva formatutvecklingen för canonical YAML.
