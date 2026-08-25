# Impact analysis – steg 34

## Syfte

Impact analysis identifierar objekt som är nåbara från ett eller flera startobjekt via modellerade relationer.

Resultatet är **förklarbart graph reachability**, inte automatiskt bevis på verklig kausal påverkan.

## Input

Direkt:

```bash
python scripts/impact_analysis.py project   --seed STR-000001   --direction incoming   --max-depth 3
```

Från change set:

```bash
--change-set changes/CHG-000120.yaml
```

Från skillnaden mellan två architecture states:

```bash
--from-state STA-000001 --to-state STA-000003
```

## Riktning

- `outgoing` följer relationship source → target.
- `incoming` följer target → source.
- `both` ger neutral connected context.

Rätt riktning beror på frågan och relationens semantik.

Exempel: om en Capability är target för Realization kan `incoming` vara relevant för att hitta realiserande komponenter.

## Djup

- depth 1 = direct
- depth 2+ = indirect

Max depth är 10.

## Certainty

Path-certainty är konservativ och bestäms av den svagaste relationen på vald path:

- strong
- moderate
- weak

`inferred` eller `unknown` evidence gör path weak även om grafkopplingen finns.

## Paths

Varje impact kan visa relationerna som ledde dit, vilket gör analysen spårbar.

## Filter

Stöd finns för:

- relationship types
- excluded relationship types
- stop types
- include/exclude seeds

## Change set

Change-set-seeds utgår från explicit berörda modell-ID:n i operationerna.

Det innebär inte att alla förändringar har samma påverkan; analysen visar den modellerade beroendekontexten runt de ändrade objekten.

## State delta

State-delta använder symmetrisk skillnad i element/relation membership mellan två states som startmängd.

## Interpretation

Särskilt viktigt:

- `direct` betyder en grafkant bort, inte "säker verksamhetspåverkan".
- `indirect` betyder flera grafkanter bort.
- certainty avser evidence för path, inte sannolikheten att en förändring faktiskt orsakar en incident eller kostnad.

## Designprincip

Impact analysis ska vara deterministisk, spårbar och försiktig i sina påståenden.
