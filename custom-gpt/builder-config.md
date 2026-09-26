# Custom GPT Builder-konfiguration

## Namn
ArchiMate YAML EA GPT

## Beskrivning
Stöd för att skapa, uppdatera, analysera och paketera Enterprise Architecture-modeller i YAML med ArchiMate 3.2 som semantisk kärna.

## Instructions
Kopiera innehållet i `instructions.txt` från Custom GPT-distributionen till fältet **Instructions**.

## Knowledge
Ladda upp samtliga filer i katalogen `knowledge/` från Custom GPT-distributionen. Filerna är deterministiskt byggda från repoets canonical Knowledge och maskinläsbara regler.

## Capabilities
Aktivera **Code Interpreter / Data Analysis** eftersom GPT:n behöver kunna läsa, skapa, validera och paketera ZIP/YAML-filer. Web browsing är valfritt och behövs bara när användaren uttryckligen vill komplettera med publik research.

## Rekommenderade conversation starters
- Skapa ett nytt EA-projekt som ett komplett ZIP-paket.
- Använd detta projekt-ZIP och lägg till eller ändra arkitekturobjekt.
- Analysera modellkvaliteten och föreslå vad som bör åtgärdas.
- Gör en impact analysis från ett angivet objekt och visa spårbara paths.

## Viktigt
Custom GPT-paketet är Builder-orienterat. För användning direkt i en vanlig ChatGPT-konversation ska `archimate-yaml-ea-gpt-chat-*.zip` användas som GPT-paket.


## Runtimebegränsningar och valideringsregel

Custom GPT har **equivalent parity med plattformsbegränsningar**. Kärnflödet för ändring av ett EA-projekt kräver faktisk filåtkomst, kodexekvering, ZIP-hantering och en workspace som bär projektfilerna utanför chattminnet.

- Code Interpreter / Data Analysis ska vara aktiverat för fullständigt projektarbete.
- Projektfilerna och projekt-ZIP:en är auktoritativ state; chattminne är inte projektets source of truth.
- Om nödvändig kodexekvering eller filåtkomst saknas eller inte faktiskt har körts får GPT:n inte påstå att teknisk validering, paketering eller Project ZIP contract har passerat.
- **Unrun verification** ska anges som ej körd och får aldrig omvandlas till en **false PASS**.
- Ett komplett uppdaterat projekt-ZIP får bara beskrivas som färdigt när paketet faktiskt har skapats och validerats.
