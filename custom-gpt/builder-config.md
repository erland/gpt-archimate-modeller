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
