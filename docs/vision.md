# Vision – ArchiMate-baserad EA GPT med portabel YAML-projektmodell

## Syfte

Projektets mål är att skapa en GPT-baserad arbetsmiljö för enterprise architecture där ArchiMate används som semantisk kärna och YAML används som det primära, LLM-vänliga arbets- och lagringsformatet.

Lösningen ska göra det möjligt att arbeta successivt med en arkitekturmodell genom vanlig dialog. Ett arkitekturprojekt ska kunna paketeras som en självständig ZIP-fil, laddas upp i en ny konversation, ändras av GPT:n och returneras som en ny komplett ZIP.

Den övergripande principen är:

> **ZIP-first, repository-agnostic. Projektpaketet är den portabla sanningskällan.**

GPT:n ska inte vara beroende av Git, GitHub, GitLab, SharePoint eller någon annan specifik lagrings- eller versionshanteringslösning. Användaren kan själv välja att lagra eller versionshantera det uppackade projektet i valfritt system.

## Problem som lösningen ska adressera

Traditionellt EA-arbete har ofta flera parallella representationsformer:

- modeller i EA-verktyg,
- diagram,
- kalkylblad,
- dokument,
- presentationer,
- manuellt sammanställda kataloger,
- muntlig kunskap.

Det gör informationen svår att hålla synkroniserad och återanvända.

Projektet ska i stället skapa en maskinläsbar arkitekturmodell som kan användas för:

- dialogbaserad modellering,
- sökning,
- analys,
- beroendeanalys,
- kvalitetskontroll,
- rapportering,
- visualisering,
- interoperabilitet med externa EA-verktyg.

## Målbild

Användaren ska kunna arbeta ungefär så här:

```text
ea-project-v0.3.zip
        ↓
      ChatGPT
        ↓
"Lägg till dessa plattformar"
"Koppla dem till befintliga applikationer"
"Markera Jenkins för avveckling"
"Vilka förmågor påverkas?"
"Skapa teknikberoenderapporten"
        ↓
ea-project-v0.4.zip
```

Den nya ZIP-filen ska innehålla hela projektet och vara tillräcklig för att fortsätta arbetet i en helt ny konversation.

## Två separata artefakter

### GPT-paketet

GPT-paketet innehåller verktyget och dess regler:

- instruktioner,
- ArchiMate-metamodell,
- schema,
- valideringsregler,
- rapportdefinitioner,
- vydefinitioner,
- scripts,
- dokumentation,
- tester.

### EA-projektpaketet

EA-projektet innehåller den faktiska arkitekturmodellen:

- projektmetadata,
- element,
- relationer,
- källor,
- evidens,
- queries,
- rapporter,
- views,
- changelog,
- eventuella exporter.

GPT-paketets version och ett EA-projekts modellversion är två olika saker.

## Grundprinciper

1. ArchiMate är den semantiska kärnan.
2. YAML är det kanoniska arbetsformatet för GPT:n.
3. Modell, query, report och view hålls separerade.
4. Alla objekt får stabila identifierare.
5. Proveniens och evidens är förstaklassinformation.
6. GPT:n ska skilja mellan fakta, importerad information och inferenser.
7. Projektformatets version skiljs från modellens version.
8. Efter en förändring returneras normalt ett komplett projektpaket.
9. Lagrings- och versionshanteringssystem är externa val.
10. Formatet ska utformas för långsiktig maskinell validering och migrering.

## Målgrupp

Primära användare:

- enterprise architects,
- lösningsarkitekter,
- verksamhetsarkitekter,
- IT-arkitekter,
- plattformsarkitekter,
- andra personer som underhåller eller analyserar strukturerad arkitekturinformation.

Sekundära användare:

- verksamhetsutvecklare,
- produktansvariga,
- tekniska ledare,
- förvaltning,
- styrning och portföljfunktioner.

## Framgångskriterier för v1

Version 1.0 ska betraktas som framgångsrik när det går att:

1. skapa ett nytt EA-projekt,
2. paketera det som ZIP,
3. läsa projektet i en ny konversation,
4. lägga till och ändra ArchiMate-element och relationer,
5. bevara stabila ID:n,
6. skilja säker information från inferenser,
7. validera strukturella fel,
8. köra definierade queries,
9. generera definierade rapporter,
10. skapa grundläggande views,
11. returnera en ny komplett ZIP utan informationsförlust.

## Designmål utanför själva användarupplevelsen

Lösningen ska dessutom vara:

- textbaserad,
- diffvänlig,
- portabel,
- verifierbar,
- möjlig att testa automatiskt,
- möjlig att migrera mellan formatversioner,
- möjlig att integrera med externa verktyg senare.

## Arkitekturprincip

Lösningen ska inte optimeras för att bli en ny generell EA-plattform eller webbapplikation. Kärnan ska vara ett portabelt modellformat och ett robust LLM-arbetsflöde ovanpå detta format.
