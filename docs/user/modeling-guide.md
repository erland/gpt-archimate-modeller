# Skapa och ändra modellen

## Lägg till ett objekt

Ge så konkret information som du känner till:

> Lägg till ApplicationComponent Ärendehantering. Owner är Team Ärende och lifecycle active.

GPT:n ska kontrollera om objektet redan kan finnas innan ett nytt ID skapas.

## Dubblettkontroll

Matchning sker ungefär i ordningen:

1. exakt stable ID,
2. alias,
3. exakt namn + kompatibel typ,
4. normaliserat namn,
5. externa ID:n,
6. semantisk likhet.

Vid tveksam identitet ska GPT:n inte auto-merga.

## Ändra ett objekt

Använd helst stable ID när du känner till det:

> Ändra beskrivningen på APP-000123.

Det minskar risken att fel objekt väljs.

## Ta bort eller avveckla

Fysisk borttagning och arkitekturell avveckling är olika saker.

Om objektet fortfarande är relevant historiskt eller i baseline/transition kan `lifecycle`, temporal metadata eller state membership vara bättre än deletion.

GPT:n ska inte radera objekt implicit.

## Relationer

Relationer ska använda tillåten ArchiMate-semantik.

Om önskad relation inte är giltig för käll-/måltyperna ska GPT:n föreslå korrekt modellering eller registrera frågan — inte tvinga in relationen.

## Properties

Organisationsegna properties måste vara deklarerade extensions. Okända properties får inte smygas in i modellen.

## Specializations

Specialization måste ha kompatibel ArchiMate-bastyp.

Exempel:

```yaml
type: Node
specialization: Platform
```

inte en påhittad ArchiMate-typ `Platform`.

## Förändringshistorik

Genomförda ändringar registreras via change sets och model version history. Stable IDs återanvänds aldrig för ett annat objekt.
