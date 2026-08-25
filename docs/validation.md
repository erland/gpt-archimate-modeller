# Grundvalidering – steg 10

## Gemensam validator

Från steg 10 används:

```bash
python scripts/validate.py <projektkatalog>
```

Den kör i en sammanhållen pipeline:

1. package/schema och referensintegritet,
2. kända ArchiMate-elementtyper,
3. kända ArchiMate-relationstyper,
4. ID/prefix,
5. source/reference,
6. evidence,
7. extensions,
8. specializations,
9. source–relationship–target-regler.

Resultatet klassificeras som `error` eller `warning` och kan även skrivas som JSON.

## Relationsmatris

Projektet har i steg 10 infört `metamodel/relationship-matrix.yaml`.

Den fullständiga tredjeparsmatris som används för korsgranskning finns i pyArchimate och är versionslåst till ett specifikt commit/blob. Den kopieras **inte** in i projektet, eftersom vi vill hålla vårt paket oberoende av tredjepartsimplementation och licens.

I stället byggs en portabel, egen regelprofil successivt. I steg 10 gäller:

- täckta par valideras strikt,
- otäckta par ger warning i normal mode,
- `--strict-relationships` gör otäckta par till error.

Detta är säkrare än att påstå full normativa täckning innan hela regelfilen har importerats och licens-/provenienshanterats uttryckligt.

## Upptäckt modellfel

Tidigare referensmodell använde:

```text
ApplicationComponent --Serving--> Capability
```

Korsgranskningen visade att den kombinationen inte är tillåten i den ArchiMate 3.2-kompatibla matrisen. Referensmodellen har därför korrigerats till:

```text
ApplicationComponent --Realization--> Capability
```

Detta är ett konkret exempel på varför relationsvalideringen behövs.

## Exit code

- `0`: inga errors
- `1`: minst ett error

Warnings blockerar inte normal validering.

## JSON-output

```bash
python scripts/validate.py examples/ea-project-split --json validation-result.json
```

## Strikt relationsläge

```bash
python scripts/validate.py examples/ea-project-split --strict-relationships
```

Detta kräver att varje source/target-typepar finns i den portabla matrisen.
