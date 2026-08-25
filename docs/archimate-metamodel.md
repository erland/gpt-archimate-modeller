# ArchiMate 3.2 – maskinläsbar metamodelldefinition

## Beslut

Projektet använder ArchiMate 3.2 som första metamodelprofil.

Metamodellen är uppdelad i flera YAML-filer för att hålla:
- elementtyper,
- relationstyper,
- lager,
- aspekter,
- relationship connectors,
- generella relationsregler,
- källmetadata

separerade men maskinellt sammanlänkade via `metamodel/index.yaml`.

## Varför inte bädda in hela specifikationen?

The Open Groups specifikation är licensierad dokumentation. Projektet återger därför inte specifikationstexten. Metamodellen representerar typnamn, klassificering och egen kortfattad struktur som behövs för maskinell bearbetning.

## Relationsvalidering i steg 2

Två nivåer finns nu:

1. kontroll att element- och relationstyper existerar,
2. grov semantisk kandidatkontroll baserad på aspekter/domäner.

Den fullständiga normativa källtyp–relation–måltyp-matrisen från Appendix B reproduceras inte i detta steg. Den planerade grundvalideringen i steg 10 ska använda en explicit, versionsmärkt exakt matris från en rättsligt och tekniskt lämplig maskinläsbar källa.

Det är ett medvetet designval: steg 2 beskriver språkets maskinläsbara begreppsmodell; steg 10 bygger den strikta validatorn.

## Antal typer i denna profil

- 60 vanliga elementtyper
- 11 relationstyper
- 1 connector-koncept med AND/OR-varianter

## Versionsstrategi

Framtida profiler ska kunna ligga parallellt, exempelvis:

```text
metamodel/
  3.2/
  4.x/
```

I nuvarande tidiga projektstruktur ligger 3.2-filerna direkt i `metamodel/`. En katalogmigrering görs först om en andra profil faktiskt behöver stödjas.
