# Användningsfall – version 1

## UC-01 – Skapa nytt EA-projekt

**Aktör:** Användare

**Mål:** Skapa ett nytt tomt eller initialt ifyllt EA-projekt.

**Flöde:**
1. Användaren beskriver organisationen eller modellens syfte.
2. GPT:n skapar grundläggande projektmetadata.
3. GPT:n skapar nödvändiga standardfiler och kataloger.
4. Initial information läggs in om sådan finns.
5. Projektet valideras.
6. En komplett ZIP returneras.

**Resultat:** Ett giltigt projekt som kan användas som input i en ny konversation.

---

## UC-02 – Öppna befintlig projekt-ZIP

**Aktör:** Användare

**Mål:** Fortsätta arbeta med en existerande arkitekturmodell.

**Flöde:**
1. Användaren laddar upp projekt-ZIP.
2. GPT:n identifierar projektformat och modellversion.
3. Projektets struktur och innehåll valideras.
4. GPT:n sammanfattar projektets status när det är relevant.
5. Projektet blir aktuell arbetsmodell.

**Resultat:** Modellen är redo för analys eller förändring.

---

## UC-03 – Lägg till element

**Aktör:** Användare

**Mål:** Lägga till ett nytt arkitekturobjekt.

**Flöde:**
1. Användaren beskriver objektet.
2. GPT:n söker efter befintligt eller liknande objekt.
3. Om inget lämpligt objekt finns väljs korrekt ArchiMate-typ.
4. Stabilt ID skapas.
5. Käll- och evidensmetadata läggs till när möjligt.
6. Modellen valideras.

**Resultat:** Ett nytt korrekt modellerat element.

---

## UC-04 – Ändra befintligt element

**Aktör:** Användare

**Mål:** Uppdatera information utan att förlora objektidentitet.

**Flöde:**
1. GPT:n identifierar rätt befintligt objekt.
2. Begärda attribut ändras.
3. ID bevaras.
4. Evidens och uppdateringsmetadata justeras vid behov.
5. Changelog uppdateras.

**Resultat:** Uppdaterat element med bibehållen historisk identitet.

---

## UC-05 – Ta bort eller avveckla element

**Aktör:** Användare

**Mål:** Hantera element som inte längre ska vara aktiva.

**Flöde:**
1. GPT:n avgör om användaren menar faktisk borttagning eller livscykelförändring.
2. Beroenden analyseras.
3. Objektet markeras för avveckling eller tas bort enligt vald regel.
4. Påverkade relationer hanteras.
5. Modellen valideras.

**Resultat:** Kontrollerad förändring utan brutna referenser.

---

## UC-06 – Skapa relation

**Aktör:** Användare

**Mål:** Beskriva relation mellan två existerande element.

**Flöde:**
1. Source och target identifieras.
2. GPT:n väljer eller kontrollerar relationstyp.
3. Relationens tillåtlighet mot ArchiMate-metamodellen verifieras.
4. Relation skapas med stabilt ID.
5. Evidensmetadata läggs till när relevant.

**Resultat:** En validerad relation.

---

## UC-07 – Återanvänd befintliga objekt

**Aktör:** GPT

**Mål:** Motverka duplicering.

**Flöde:**
1. Vid varje nytt objektförslag söks namn, alias, typ och relevanta metadata.
2. Sannolika kandidater jämförs.
3. Befintligt objekt används när det är samma koncept.
4. Osäkra fall flaggas i stället för att automatiskt dupliceras.

**Resultat:** Högre modellkvalitet och stabilare identitet.

---

## UC-08 – Importera ostrukturerad information

**Aktör:** Användare

**Mål:** Omvandla text, dokument eller listor till strukturerad arkitekturinformation.

**Flöde:**
1. GPT:n analyserar underlaget.
2. Kandidater till element och relationer identifieras.
3. Befintlig modell matchas.
4. Nya objekt skapas bara när det behövs.
5. Infererad information märks tydligt.
6. Källreferenser sparas.
7. Projektet valideras.

**Resultat:** Underlag har införlivats utan att förväxlas med verifierade fakta.

---

## UC-09 – Analysera beroenden

**Aktör:** Användare

**Mål:** Förstå hur arkitekturelement hänger samman.

**Exempelfrågor:**
- Vad påverkas om Oracle avvecklas?
- Vilka applikationer använder plattform X?
- Vilka förmågor saknar realiserande applikationer?

**Resultat:** Spårbar analys baserad på modellens relationer.

---

## UC-10 – Generera rapport

**Aktör:** Användare

**Mål:** Skapa en strukturerad rapport från modellen.

**Flöde:**
1. Rapportdefinition väljs.
2. Underliggande query körs.
3. Resultat filtreras, sorteras och grupperas.
4. Rapporten genereras i stödda format.

**Första format:** Markdown och CSV.

**Resultat:** Reproducerbar rapport utifrån aktuell modell.

---

## UC-11 – Generera vy

**Aktör:** Användare

**Mål:** Visualisera en vald del av modellen.

**Flöde:**
1. En view-definition används eller skapas.
2. Relevanta element och relationer hämtas.
3. Layoutinformation tillämpas där sådan finns.
4. Ett stödd visualiseringsformat genereras.

**Resultat:** Visualisering som är en projektion av modellen, inte en separat sanningskälla.

---

## UC-12 – Validera projekt

**Aktör:** Användare eller GPT

**Mål:** Säkerställa teknisk och semantisk kvalitet.

**Kontroller i v1:**
- giltig YAML,
- obligatoriska fält,
- unika ID:n,
- giltiga referenser,
- giltiga elementtyper,
- giltiga relationstyper,
- tillåtna relationer,
- giltiga enum-värden,
- kvalitetsvarningar.

**Resultat:** Tydliga fel och varningar med tillräcklig information för korrigering.

---

## UC-13 – Returnera uppdaterad projekt-ZIP

**Aktör:** GPT

**Mål:** Göra resultatet portabelt mellan konversationer.

**Flöde:**
1. Alla förändringar är genomförda.
2. Projektet valideras.
3. Modellmetadata uppdateras.
4. Changelog uppdateras.
5. Komplett projektstruktur paketeras.
6. Ny ZIP returneras.

**Resultat:** ZIP-filen ensam räcker för att fortsätta arbetet i en ny konversation.

---

# Tvärgående kvalitetskrav

Alla användningsfall ska följa följande:

- befintlig information får inte tappas tyst,
- stabila ID:n ska bevaras,
- inferenser får inte presenteras som bekräftade fakta,
- oklarheter ska kunna sparas som öppna frågor i framtida format,
- projektet ska förbli validerbart efter varje förändring,
- GPT:n ska inte kräva kunskap om extern repository- eller versionshantering.
