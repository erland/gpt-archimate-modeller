# {{GPT_NAME}} – OpenAI Plugin

Version: {{VERSION}}

Skills-first plugin för ArchiMate 3.2-modellering med YAML-projekt.

## Innehåll

- `plugin.json`, `runtime-contract.json`, `MANIFEST.json`
- Fyra Skills med kanoniska instruktioner, Python-skript och nödvändiga dataresurser

## Skills

{{SKILLS}}

## Exekvering och beroenden

Medföljande skript är resurser, **inte automatiskt registrerade ChatGPT-verktyg**. De kan användas när hosten ger kompatibel Python-exekvering, skrivbart filsystem och beroenden `PyYAML>=6,<7` och `jsonschema>=4,<5`. Pluginpaketet registrerar ingen MCP-server.

När skript inte kan köras direkt i ChatGPT, använd den separat distribuerade **ArchiMate Engine ZIP** i en kompatibel Pythonmiljö. Engine ZIP har ett gemensamt CLI och ett selftest, och kräver inte plugininstallation.

## Säkerhet och portabilitet

Kontrollera ändringsförslag med dry-run före apply. Validera alltid projekt och projekt-ZIP efter ändringar. YAML är source of truth. Den faktiska runtime-funktionaliteten beror på värdens tillgängliga verktyg och behörigheter.
