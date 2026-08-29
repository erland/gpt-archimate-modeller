# Knowledge overview

Detta är GPT:ns strukturerade kunskapsunderlag.

## Syfte

Systeminstruktionen ska styra beteendet.
Knowledge-filerna ska bära detaljer som behövs för korrekt modellering, validering, projektarbete och export.

## Runtime-laddning

Kärnmaterialet definieras av `loading_guidance.always_use` i `knowledge-index.yaml`.

Läs inte hela Knowledge-basen som standard. Börja med kärnmaterialet och använd därefter `routing.yaml` för att hämta minsta relevanta task-specifika fördjupning för den aktuella uppgiften.

## Grundprincip

Knowledge är referensmaterial.
Den får inte motsäga systeminstruktionen.
Om två Knowledge-filer verkar krocka ska mer specifik fil och senaste format/version i `knowledge-index.yaml` gälla.
