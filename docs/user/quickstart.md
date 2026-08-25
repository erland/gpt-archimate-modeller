# Snabbstart

## 1. Skapa ett nytt projekt

Be GPT:n exempelvis:

> Skapa ett nytt EA-projekt med id `myndighet-ea` och namnet `Myndighetens enterprise architecture`.

Om du inte anger några arkitekturfakta skapas ett tomt, giltigt projekt. GPT:n ska inte hitta på innehåll för att fylla modellen.

Du får tillbaka ett komplett projekt-ZIP.

## 2. Fortsätt arbeta

Ladda upp senaste projekt-ZIP i en ny eller befintlig konversation och be om en förändring, exempelvis:

> Lägg till applikationen Ärendehantering. Den ägs av Team Ärende och är aktiv.

GPT:n ska:

1. validera ZIP:en,
2. kontrollera format/version,
3. identifiera befintliga objekt och möjliga dubbletter,
4. göra förändringen genom ett change set,
5. validera modellen,
6. ge tillbaka ett nytt komplett ZIP.

Original-ZIP ändras inte.

## 3. Analysera utan att ändra

Exempel:

> Visa vilka capabilities som saknar realisering.

> Gör en impact analysis från APP-000123, max tre relationer.

> Skapa modellkvalitetsrapporten.

Queries, rapporter, views och analyser är read-only om du inte uttryckligen ber om en modelländring.

## 4. Visualisera

Exempel:

> Exportera standardvyn application-landscape till draw.io.

> Skapa en Mermaid-vy över capability-realiseringen.

## 5. Beskriv framtida arkitektur

Exempel:

> Skapa en target architecture för 2028 där APP-000123 ska avvecklas och APP-000456 introduceras.

Baseline/target/transition återanvänder samma stabila objekt-ID:n och beskriver state/delta. Hela modellen ska inte kopieras med nya ID:n.

## Det viktigaste att komma ihåg

- YAML är source of truth.
- Stable IDs ska återanvändas.
- Fakta, inferenser och planerad framtid hålls isär.
- Evidence ska stödja viktiga påståenden.
- Vid osäker identitet eller konflikt ska GPT:n stoppa och synliggöra problemet i stället för att gissa.
- Efter en förändring ska du alltid få ett komplett nytt projekt-ZIP.
