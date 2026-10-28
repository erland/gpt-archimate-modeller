# Migrering till GPT Byggaren 1.6.33

Projekt: ArchiMate YAML EA GPT
Bas: GPT Byggaren 1.5.0, produktversion 1.0.0, ArchiMate 3.2, YAML format 0.2.
Status: inventering påbörjad; ingen funktionell migrering är ännu verifierad.

## Bevarandevillkor

- Bevara gpt/SYSTEM_INSTRUCTION.md, ArchiMate 3.2, YAML som källa, stabila ID, evidence/provenance/confidence samt explicit ändrings- och valideringsflöde.
- Bevara produktplan 48/48 och befintlig produktversion; migreringen ändrar enbart GPT Byggaren-integration.
- Behåll befintliga ArchiMate-specifika tester och plattformsbegränsningar. Inga falska PASS.
- Använd enbart den kanoniska GPT Byggaren 1.6.33-motorn som bygg- och valideringsmotor.

## Sex steg och kontrollpunkter

1. **Inventering** – jämför befintliga instruktioner, scripts, kontrakt, distributionsregistry, CI, release, tester och dokumentation. Identifiera förlorade beteenden och beroenden.
2. **Projektmodell** – inför projektunik gpt-project.yaml; föreslå och granska Skill-indelning innan eventuell modularisering, upprätta spårbarhetsmatris; mappa capability/artifact/workspace-state/tool-kontrakt.
3. **Motor** – installera versionslåst original av GPT Byggaren 1.6.33; verifiera integritet och självtest, uppdatera byggkommandon utan att ersätta projektspecifika verktyg i förtid.
4. **Fem distributioner** – Chat ZIP, OpenAI Plugin, Claude Projects, Claude Skills och OpenCode. Custom GPT är historiskt stöd, inte aktiv sjätte distribution. Verifiera plattformsparitet.
5. **Dokumentation och filhygien** – synkronisera README, PROJECT/STATUS, plan, registry, CI/release; inventera gamla 1.5-skript och ta bort enbart när funktionell ersättning och noll referenser verifierats.
6. **Slutverifiering** – kör projektets domäntester, kanoniskt lint/build/distributionsvalidering, runtime-kontroller och release-readiness. Markera klar först efter godkända resultat.

## Inventeringsfynd

- README anger migrering till GPT Byggaren 1.5.0 och produktversion 1.0.0.
- migration-status-1.5.yaml anger 9/9 steg genomförda; detta är historisk status och får bevaras.
- runtime/distribution-registry.yaml anger fem äldre mål inklusive custom_gpt, men saknar claude_skills.
- gpt-project.yaml och PROJECT.md saknas i repositoryroten.
- .github/workflows/release.yml använder scripts/validate_release_assets_1_5.py.
- GPT Byggaren 1.6.33 Engine ZIP har självtestats separat med godkänt resultat; projektets egna runtimebyggen är ännu inte verifierade.

## Nästa konkreta åtgärd

Fullständig inventering av kanonisk instruktion, domänskript, projektstruktur och befintliga CI-filer; därefter presentera en föreslagen Skill-arkitektur med beteendespårbarhet innan projektmodellen ändras.
