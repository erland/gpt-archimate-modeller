# {{GPT_NAME}} – OpenCode-distribution

Detta är ett OpenCode-workspace för ArchiMate YAML EA-modellering, inte ett GPT Byggaren-projekt.

## Kom igång

1. Packa upp ZIP-filen och öppna workspace-roten i OpenCode.
2. Läs `AGENTS.md` och de fyra Skills under `.opencode/skills/`.
3. Lägg ditt **ArchiMate YAML EA-projekt** i en separat katalog, exempelvis `project/`.
4. Kör relevanta Python-skript från respektive Skill mot den katalogen, förutsatt att Python och beroendena finns installerade.
5. Om den lokala runtime-miljön inte kan exekvera skripten kan den fristående **ArchiMate Engine ZIP** användas i en annan kompatibel Pythonmiljö.

## Beroenden

Python 3.10+, `PyYAML>=6,<7` och `jsonschema>=4,<5`. Installera från Engine ZIP:s `requirements.txt` eller i din egen Pythonmiljö.

## Begränsningar

Skills och skript innebär inte automatiskt att OpenCode har registrerat typade custom tools. Läs `.opencode/runtime-contract.json` för faktiska runtime-förutsättningar. Behåll alltid modellens YAML-filer som source of truth och leverera uppdaterade projekt som validerade ZIP-filer.

Version: {{VERSION}}
