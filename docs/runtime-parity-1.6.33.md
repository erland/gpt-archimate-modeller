# Runtimeparitet – GPT Byggaren 1.6.33 (PR #8)

## Verifieringsgrund

Kanonisk modell: `canonical/core.md` och fyra Skills. Projektets primära ArchiMate-version är 3.2. Fem aktiva peer-distributioner byggs med originalmotorn 1.6.33. Historisk Custom GPT är avaktiverad.

### Verifiering per mål

| Runtime | Arkiv byggt och originalvaliderat | Skill-resurser | Körbar projektlivscykel | Värdmiljötest |
| --- | --- | --- | --- | --- |
| Chat ZIP | PASS | PASS, fyra paketerade referens-Skills | PASS, direkt Python i isolerad testmiljö | Ej verifierat i Chat-host |
| Claude Project | PASS | Instruktioner och kontrakt verifierade i arkivet | Ej körbart Skill-hosttest; portabla referenser | Ej verifierat i Claude |
| Claude Skills | PASS | PASS, fyra Skills | PASS, direkt Python i isolerad testmiljö | Ej verifierat i Claude |
| OpenCode | PASS | PASS, fyra Skills | PASS, direkt Python i isolerad testmiljö | Ej verifierat i OpenCode |
| OpenAI Plugin | PASS | PASS, fyra Skills | PASS, direkt Python i isolerad testmiljö | Ej verifierat i Plugin-host |

PASS för projektlivscykel innebär att ett uppackat Skill kan skapa ett projekt, köra validering, paketera en ZIP och validera ZIP:en med Python och nödvändiga installerade paket. Detta bevisar **inte** att en runtime-host tillåter filskrivning, har rätt Python-beroenden, aktiverar Skills automatiskt eller hanterar bilagor.

## Verifierade kontrakt

- Samma canonical beteendekälla används för de fem distributionerna.
- Lokala statiska Python-importkedjor kontrolleras för varje Skill.
- Deklarerade skript, tillgångar och referenser granskas i byggda arkiv.
- Paketerade schema- och metamodelluppslag smoketestas i fyra Skill-baserade mål (16 kontroller).
- Projektgenerering, validering och ZIP-kontroll smoketestas i dessa fyra mål.
- Originalmotorns linter har noll fel och tre GP210-varningar om duplicerade fixture-Markdownfiler.

## Begränsningar som blockerar release-ready

1. Riktiga värdmiljötester för Chat, Claude, OpenCode och Plugin saknas. Claude Project kräver egen text-/bilageverifiering.
2. Dynamiska importer, externa verktyg, värdberoenden och all dataresursåtkomst är inte fullständigt verifierade.
3. Modellens verkliga analys-, ändrings- och import/exportfunktioner har inte funktionstestats i samtliga hosts.
4. Källprojektets historiska 1.5-release- och byggflöden måste granskas innan övergång till 1.6.33; migrationens CI-jobb är ännu separerat.
5. Releasehygien, fullständig projektlint och ändringsparitet måste vägas samman i ett slutligt releasebeslut.

## Slutsats

Det finns **paketeringsparitet för fem mål** och **isolera­de Python-projektflödestester för fyra mål**, inte belagd funktionell paritet i faktiska värdmiljöer. Migrationen är inte releaseklar och PR #8 ska inte mergas med hänvisning till den här rapporten.
