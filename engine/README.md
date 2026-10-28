# ArchiMate Modeller Engine

Standalone Python CLI distribution for ArchiMate Modeller. This ZIP is a **runtime engine**, not GPT Byggaren's build engine, and it requires no installed ChatGPT plugin or MCP server.

## Start

Extract the ZIP into a writable directory. Python 3.10+ is required.

```bash
python -m pip install -r requirements.txt
python archimate_engine.py selftest
python archimate_engine.py --help
```

Examples (paths relative to your working directory):

```bash
python archimate_engine.py new-project --id demo --name Demo --output-dir .
python archimate_engine.py validate demo
python archimate_engine.py query demo query.yaml --json
python archimate_engine.py export-model-exchange demo --output model.xml
python archimate_engine.py pack-project demo demo.zip
```

All commands forward their remaining arguments to the canonical script in `scripts/`. Use `python archimate_engine.py <command> --help` for command-specific options.

## ChatGPT Chat fallback

When a ChatGPT conversation can execute Python and install dependencies, attach the Engine ZIP, extract it and run `selftest`. Use the CLI for model changes, analysis, validation, XML import/export and ZIP packaging. A ChatGPT host without Python execution or filesystem write cannot run this ZIP; in that case use a compatible execution environment. Do not claim that merely attaching this ZIP automatically activates its commands.

This archive includes the model schemas, metamodel, quality/version policies and serialized project templates required by the canonical scripts. Project data remains in separate YAML project directories/ZIPs.

## Release och versionsmatchning

Hämta alltid Engine ZIP från samma GitHub Release som den Chat-, Plugin-, Claude- eller OpenCode-distribution du använder. Filnamnet är `archimate-modeller-engine-<version>.zip` och publiceras som en release-tillgång vid publicering. Se https://github.com/erland/gpt-archimate-modeller/releases .
