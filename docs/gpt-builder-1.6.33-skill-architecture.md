# Föreslagen Skill-arkitektur för 1.6.33

Status: inventering av instruktion och kontrakt genomförd; implementering återstår.

## Källor
- gpt/SYSTEM_INSTRUCTION.md
- runtime/runtime-contract.json
- runtime/archimate-tool-contract.json
- runtime/gpt-builder-1.5-contract.yaml
- scripts/build_distributions.py
- runtime/distribution-registry.yaml
- docs/user/index.md och docs/developer/index.md

## Gemensam kärna
canonical/core.md: YAML som sanningskälla, ArchiMate 3.2, stable ID, evidence och confidence, inga tysta ändringar eller påhittade uppgifter, pre- och postvalidering, separata query/report/view, projektfiler som state och komplett validerat ZIP efter modelländring.

## Fyra Skills
1. project-workflow: projekt-ZIP, säker inläsning, migration, change sets, SemVer, historik, validering och paketering.
2. archimate-modeling: element, relationer, stable-ID-matchning, extensions, specializations, evidence, issues, tolkning av ostrukturerad information.
3. architecture-analysis: query, traversal, impact, modellkvalitet, report, view, Mermaid och draw.io.
4. interoperability: ArchiMate Model Exchange export och staging-import, round-trip och informationsförlust.

## Spårbarhet från original
- Roll, Grundprinciper, Kommunikation, Förbjudet beteende, Slutregel -> core.
- När användaren lämnar ett projekt-ZIP; När migration krävs; Change workflow; Versionsregler -> project-workflow.
- ArchiMate-modellering; Elementidentitet; Relationer; Evidence och provenance; Confidence; Extensions; Specializations; Issues; När användaren ger ostrukturerad information -> archimate-modeling.
- Query; Report; View; Diagram; Quality; När användaren ber om analys; När användaren ber om rapport eller vy -> architecture-analysis (globala kvalitetsgränser i core).
- Model Exchange -> interoperability.
- Export och output -> core samt relevant Skill.

## Gränser och verifiering
En Skill får inte duplicera en annan Skills specialbeteende. Projektskapande och ändring kräver project-workflow även om begäran börjar i modellering eller import. En analys eller vy får inte skapa nya modellfakta.

Nästa genomförandesteg: kartlägg samtliga scripts, resurser, tests och CI-anrop; verifiera explicit resursbehov för varje Skill innan gpt-project.yaml och modular_skills införs. Den gamla distributionsbyggaren och Custom GPT-adaptern ska inte raderas innan verifierad ersättning. Detta dokument är ett förslag, inte godkänd runtime-paritet.
