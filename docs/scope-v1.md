# Scope – v1 och senare

## Ingår i v1

### Modellkärna

- ArchiMate-baserade element.
- ArchiMate-baserade relationer.
- Maskinellt validerbara relationer.
- Stabil objektidentitet.
- YAML som kanoniskt arbetsformat.
- Projektmetadata.
- Modellversion.
- Formatversion.

### Informationskvalitet

- Källor.
- Evidens.
- Confidence.
- Skillnad mellan bekräftad och infererad information.
- Grundläggande kvalitetskontroller.
- Möjlighet att upptäcka dubblettkandidater.

### Projektpaketering

- Komplett projektstruktur.
- ZIP som transport- och arbetsenhet.
- Validering vid inläsning och export.
- Changelog.
- Grund för framtida migrering mellan formatversioner.

### Analys

- Query-definitioner.
- Relationstraversering.
- Grundläggande beroendeanalys.
- Modellkvalitetsanalys.

### Rapportering

- Deklarativa rapportdefinitioner.
- Markdown-export.
- CSV-export.
- Ett standardbibliotek av centrala EA-rapporter.

### Views

- Deklarativa view-definitioner.
- Minst ett enkelt visualiseringsformat.
- Views ska alltid kunna återskapas från modellen.

### GPT-arbetsflöde

- skapa projekt,
- öppna projekt,
- uppdatera projekt,
- lägga till element,
- ändra element,
- skapa relationer,
- validera,
- generera rapporter,
- generera views,
- returnera komplett ZIP.

### Interoperabilitet

Målet är stöd för ArchiMate Model Exchange-export i eller senast i anslutning till v1, under förutsättning att det kan implementeras och verifieras robust.

---

## Kan vänta till efter v1

- avancerad automatisk diagramlayout,
- komplett roundtrip av all layout mellan olika EA-verktyg,
- fleranvändarredigering,
- låsning och samtidighetskontroll,
- central modellserver,
- relationsdatabas,
- grafdatabas,
- webbgränssnitt,
- realtidsintegrationer,
- automatisk synk mot CMDB,
- automatisk synk mot ITSM,
- Git-integration,
- GitHub-integration,
- pull requests,
- automatiska commits,
- repository-specifika workflows,
- central autentisering,
- rollbaserad åtkomstkontroll i själva projektformatet.

---

## Explicita icke-mål

Följande är inte syftet med projektet:

### Inte ett nytt Git-system

Projektet ska inte kräva:

- commits,
- branches,
- pull requests,
- GitHub,
- GitLab.

Git kan användas externt av användaren men är inte en runtime-förutsättning.

### Inte ett nytt komplett kommersiellt EA-repository

Projektet ska inte initialt försöka ersätta hela funktionaliteten i etablerade enterprise architecture-plattformar.

### Inte en diagramgenerator med modellen som biprodukt

Diagram är en projektion av modellen. Den maskinläsbara modellen är den primära sanningskällan.

### Inte fri schemalös YAML

Formatet ska vara strikt definierat och validerbart.

### Inte autonom arkitekturdesign utan spårbarhet

GPT:n får göra inferenser och rekommendationer, men dessa ska kunna skiljas från verifierad modellinformation.

---

# Beslut för steg 1

Följande beslut fastställs som utgångspunkt för kommande steg:

1. Projektformatet är ZIP-first och repository-agnostic.
2. YAML blir det primära arbetsformatet.
3. ArchiMate används som semantisk kärna.
4. Projektformat och modellversion hanteras separat.
5. GPT-paketet och EA-projektpaketet är separata artefakter.
6. Reports, queries och views är separata lager ovanpå modellen.
7. Proveniens och evidens designas in från början.
8. Git/GitHub hålls helt utanför projektets kärnmodell och runtime.
