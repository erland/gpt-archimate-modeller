# Projektmodell för GPT Byggaren 1.6.33

Status: förslag, ej aktivt runtime-kontrakt. Ursprunglig canonical instruktion och befintligt registry gäller tills migrationen är verifierad.

## Projektidentitet
- id: archimate-yaml-ea-gpt
- produktversion: 1.0.0
- builder: 1.6.33
- ArchiMate: 3.2
- YAML-projektformat: 0.2

## Målstruktur
- gpt-project.yaml: projektunik konfiguration, skapas först efter avstämd motormodell.
- canonical/core.md: gemensamma beteenderegler.
- canonical/skills/project-workflow/behavior.md
- canonical/skills/archimate-modeling/behavior.md
- canonical/skills/architecture-analysis/behavior.md
- canonical/skills/interoperability/behavior.md

## Skill-avgränsning
project-workflow: projektpaket, migration, change sets, modellversion och validering.
archimate-modeling: element, relationer, identitet, evidens och extensions.
architecture-analysis: queries, impact, kvalitet, rapporter och views.
interoperability: ArchiMate Model Exchange import/export och staging.

## Fem planerade runtime-mål
chat, plugin, claude_project, claude_skills, opencode.
Custom GPT är historiskt stöd och ingår inte bland de fem aktiva.

## Kontrakt att bevara
- runtime/runtime-contract.json och runtime/archimate-tool-contract.json är underlag för capabilities, state, artifacts och verktyg.
- gpt/SYSTEM_INSTRUCTION.md är oförändrad referens för beteendeparitet.
- projectRoot och path safety, no-false-PASS, approved mutation och Project ZIP contract är obligatoriska.
- Gemensamma Python-moduler kan delas, men varje Skill måste deklarera sina riktiga runtime-resurser.

## Aktiveringskrav
1. Fullständig kartläggning av transitive Python- och övriga resurser.
2. Generera och validera explicit resource_policy för varje Skill.
3. Kör kanonisk GPT Byggaren 1.6.33-installation och distributionsvalidering.
4. Jämför beteendet mot ursprunglig systeminstruktion och projektets tester.
5. Synkronisera registry, GitHub Actions, README och migrationsstatus först när resultatet är godkänt.

En grön gammal CI innebär inte att den nya 1.6.33-projektmodellen är aktiverad.
