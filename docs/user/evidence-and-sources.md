# Evidence, källor och osäkerhet

## Varför evidence finns

Modellen ska kunna skilja mellan:

- verifierade fakta,
- användarbekräftade uppgifter,
- importerad information,
- härledda slutsatser,
- inferenser,
- okänd/osäker information.

## Confidence

Typiska nivåer:

- high
- medium
- low
- unknown

Confidence beskriver underlagets styrka, inte objektets viktighet.

## Stöd för egenskaper

Viktiga egenskaper kan kräva explicit stöd, exempelvis:

```text
property:owner
property:lifecycle
```

Om du anger owner i prompten kan ett `user_statement`-assertion stödja uppgiften.

## Källor

När information kommer från ett dokument bör Source beskriva dokumentet.

När det går bör Reference ange exakt plats:

- page,
- section,
- heading,
- line range,
- table,
- anchor.

## Inferens

GPT:n får göra inferenser när det är relevant, men inferensen ska:

- vara markerad som inferens,
- ha reason,
- inte presenteras som verifierat faktum.

## Saknad information

Om information saknas ska modellen kunna lämna värdet okänt och vid behov skapa issue/observation.

Målet är inte maximal ifyllnadsgrad utan korrekt och spårbar modell.
