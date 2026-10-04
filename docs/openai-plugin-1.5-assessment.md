# OpenAI Plugin compatibility assessment – GPT Byggaren 1.5.0

## Beslut

OpenAI Plugin är en **aktiv peer runtime** för ArchiMate YAML EA GPT.

Compatibility är `equivalent_runtime_dependent`.

Det betyder att canonical ArchiMate-beteende, projektstate, mutation, validering och paketering kan bevaras när hosten erbjuder de required capabilities som projektet redan deklarerar. Pluginpaketet provisionerar inte själv workspace eller Python-runtime.

## Required host capabilities

Full canonical körning kräver:

1. filesystem read,
2. filesystem write,
3. code execution,
4. structured data,
5. persistent workspace,
6. archive I/O.

Därutöver krävs verklig exekvering av canonical toolchain, teknisk validering före och efter mutation samt komplett Project ZIP contract-verifiering.

## Packaged runtime tools

Pluginen återanvänder den etablerade runtime-script-allowlisten från Chat-distributionen. Den innehåller bland annat:

- `new_project.py`
- `update_project.py`
- `validate_project_zip.py`
- `project_control.py`
- `query.py`
- `impact_analysis.py`
- `model_quality_report.py`
- `render_report.py`
- `export_diagram.py`
- `export_model_exchange.py`
- `import_model_exchange.py`

samt deras supportverktyg.

Skillen paketerar även runtime-relevanta schemas, metamodel, package contracts, migrations, validation policies, queries, reports, views och templates så verktygen kan köras med samma relativa runtime-layout som i Chat ZIP.

Scripts är resources och behöver inte MCP-wrapper enbart för att användas. Hostens kompatibla Python code execution kan köra dem direkt.

## Mutation och approval

Canonical mutation kräver fortsatt explicit approval enligt tool-contractet.

Pluginen får inte:

- mutera canonical projektstate utan approval,
- hoppa över pre-validation eller post-validation,
- hävda att validation har passerat om den inte faktiskt körts,
- behandla chat history som project state,
- hävda att ett komplett projekt-ZIP finns om det inte faktiskt skapats och validerats.

No-false-PASS gäller alltid.

## Runtime-dependent parity

`equivalent_runtime_dependent` är korrekt eftersom parity beror på hosten.

Om filesystem write, code execution, persistent workspace eller archive I/O saknas kan pluginen fortfarande ge rådgivande ArchiMate-stöd, men den får inte hävda att det canonical ZIP-first change/validate/package-flödet genomförts.

## Project ZIP contract

Det kompletta EA project ZIP är den portabla auktoriteten. Efter en projektändring ska ett komplett validerat ZIP produceras enligt Project ZIP contract.

## Release

Plugin-distributionen byggs och valideras som:

`archimate-yaml-ea-gpt-plugin-v<version>.zip`

Den ingår i registry-driven build, runtime parity, checksums, release metadata och exact release asset set.
