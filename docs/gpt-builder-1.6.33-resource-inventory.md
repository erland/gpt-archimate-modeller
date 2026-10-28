# Resurs- och CI-inventering inför GPT Byggaren 1.6.33

Datum: 2026-10-28. Status: riktad granskning av kända huvudscripts genomförd; fullständig transitive dependency closure återstår.

## Verifierade källor
- scripts/project_control.py, scripts/update_project.py, scripts/query.py, scripts/impact_analysis.py
- scripts/export_model_exchange.py, scripts/import_model_exchange.py
- scripts/build_distributions.py, scripts/validate_distributions.py, scripts/build_release.sh
- .github/workflows/ci.yml, .github/workflows/release.yml
- docs/developer/testing.md, docs/developer/modules.md
- runtime/runtime-contract.json, runtime/archimate-tool-contract.json

## Skill-ankare och observerade beroenden

| Skill | Verifierade entrypoints | Direkt observerade beroenden |
| --- | --- | --- |
| project-workflow | project_control.py, update_project.py | validate_project_zip, safe_unpack, pack_project, validate, quality_check, assemble_project, migrate_project, identity, apply_changes |
| archimate-modeling | update_project.py (mutationsorchestrering), apply_changes.py (enligt modulbeskrivning) | identity, assemble_project; projektflödets validering och ZIP krävs vid mutation |
| architecture-analysis | query.py, impact_analysis.py | model_loader; rapporter och views använder render_report.py, compile_view.py och export_diagram.py enligt dokumenterade modulgränser |
| interoperability | import_model_exchange.py, export_model_exchange.py | export_model_exchange använder assemble_project; XML och staging är domänspecifikt |

Detta är startmängder, inte färdiga explicit resource lists. Samma script får behövas av flera Skills; behåll en kanonisk implementation.

## Resurskategorier att verifiera

- **references**: kunskapsmaterial under knowledge/, metamodel/, schemas/ och relevanta format-/policyfiler – mappa till aktuellt arbetsflöde efter innehåll och importberoenden.
- **scripts**: räkna inte alla scripts som runtimeverktyg. Mappa deklarerade tool entrypoints i runtime/archimate-tool-contract.json till faktiska scripts, transitiva imports och nödvändiga datafiler.
- **assets**: identifiera scheman, metamodel/matris, project templates och exportmallar; håll isär läsresurser och genererade utdata.
- **workspace/state**: EA project ZIP och project files fortsätter vara auktoritativa. Resurser i plugin-distributionen är inte en skrivbar projektarbetsyta.

## CI, tester och release

- CI: .github/workflows/ci.yml kör scripts/run_tests.py, validate_llm_evals.py, dokumentations-/fixture-/kontraktskontroller, 1.5-specifika validatorer, build_all_distributions.py och runtime-adherence.
- Release: scripts/build_release.sh kör domän- och 1.5-kontroller samt build_all_distributions.py och validate_all_distributions.py.
- .github/workflows/release.yml använder validate_release_assets_1_5.py.
- scripts/build_distributions.py och scripts/validate_distributions.py kodar äldre fem mål inklusive Custom GPT. Nytt mål ska ha Claude Skills i stället för aktiv Custom GPT.
- Tester enligt docs/developer/testing.md: enhet/subsystem, referensprojekt, negativa fixtures, E2E, automatiserad suite och LLM-evals. Ingen suite har körts i detta inventeringssteg.

## Risker, gates och nästa avgränsade steg

1. Utför fullständig file-tree-inventering och importgraf över scripts innan skills.resource_policy: explicit aktiveras. Enbart de lästa entrypoints ovan räcker inte.
2. Jämför konkreta tool-kontrakt mot samtliga scripts och identifiera odeklarerade runtimekommandon, templates och schemas.
3. Bevara legacy build/test tills originalmotorns ersättning passerar jämförbara funktionstester och CI.
4. Skapa projektspecifik gpt-project.yaml och modulär canonical layout först när resursmatrisen är fullständig. De fem nya distributionerna kräver separat verifiering.
5. Ingen ändring av produktversion, ArchiMate 3.2, format 0.2 eller canonical modellbeteende.

Inventeringsresultatet är källgranskat men inte exekverat eller fullständigt dependenciesäkrat.
