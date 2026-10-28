# {{GPT_NAME}} – Chat ZIP

Detta paket innehåller instruktioner, fyra Skills, resurser och Python-skript för ArchiMate YAML EA-modellering.

## Användning i ChatGPT

1. Bifoga Chat ZIP och ett separat YAML-projekt (eller begär att ett nytt projekt skapas).
2. Använd Skills för projektflöde, modellering, analys och interoperabilitet.
3. När Python-exekvering och ett skrivbart filsystem finns kan de medföljande skripten användas.
4. Om Skill-skripten inte går att köra direkt, bifoga den separata **ArchiMate Engine ZIP** och kör dess `archimate_engine.py` från en kompatibel Pythonmiljö.

Engine ZIP innehåller beroendelista (`PyYAML>=6,<7`, `jsonschema>=4,<5`), CLI och selftest. Att bifoga en ZIP aktiverar inte automatiskt skript som ChatGPT-verktyg.

## Viktiga filer

- `assistant/instructions.md` – genererade runtimeinstruktioner
- `assistant/skills/` – Skills och skript
- `assistant/runtime-contract.json` – runtimeförutsättningar
- `knowledge/` – kunskap

Version: {{VERSION}}
