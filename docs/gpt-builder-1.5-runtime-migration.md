# GPT Byggaren 1.5.0 – migreringsplan

Projekt: **ArchiMate YAML EA GPT**  
Utgångsläge: stabil produktversion **1.0.0**, produktplan **48/48**, genomförd GPT Byggaren 1.4-runtime-migrering.

## Mål

Migrera runtime-/projektmodellen till GPT Byggaren 1.5.0 utan att förändra projektets canonical ArchiMate-beteende, projektformat eller stabila produktversion.

## Preserve-first

Följande ska bevaras:

- `gpt/SYSTEM_INSTRUCTION.md` som canonical behavior.
- ArchiMate 3.2 som semantisk kärna.
- YAML som source of truth.
- Stable IDs.
- Evidence/provenance/confidence.
- Explicit change-set workflow.
- Teknisk validering före och efter mutation.
- Komplett validerat projekt-ZIP efter modelländring.
- Query/report/view-separation.
- Model Exchange som interoperabilitet, inte canonical källa.
- `runtime/runtime-contract.json` och `runtime/archimate-tool-contract.json` som etablerade kontraktslager.
- Registry-driven build/release.
- Befintlig produktplan och releasehistorik.

## Runtime-målbild

Aktiva runtimes:

1. Chat ZIP
2. Custom GPT
3. Claude Projects
4. OpenCode

OpenAI Plugin ska bedömas explicit i 1.5.0 men inte aktiveras som full runtime om kärnkraven för filesystem write, code execution, persistent workspace, archive I/O, mutation och deterministisk validering inte kan uppfyllas.

## Steg

### 1. Inför separat 1.5.0-migrationsstatus
Lägg till separat plan/status för 1.5.0 utan att ändra produktplan 48/48 eller runtime-set.

### 2. Normalisera kontrakten mot GPT Byggaren 1.5.0
Mappa befintliga behavior-, capability-, artifact-, workspace/state- och tool-kontrakt till 1.5.0-modellen och lägg till validering.

### 3. Normalisera registry och build metadata
Gör distribution-registryt uttryckligen kompatibelt med 1.5.0 och behåll registry-driven build.

### 4. Verifiera Chat ZIP
Verifiera canonical instruction, runtime scripts, workspace authority, project ZIP contract och artifact parity.

### 5. Verifiera Custom GPT
Verifiera compiled instruction, Knowledge, plattformsbegränsningar och no-false-PASS.

### 6. Verifiera Claude Projects och OpenCode
Behåll Claude som reduced parity och OpenCode som equivalent med typade ArchiMate-tools och explicit projectRoot.

### 7. OpenAI Plugin compatibility assessment
Dokumentera om Plugin är not_planned eller reduced/advisory. Ingen falsk tool/workspace parity.

### 8. Generalisera CI/release/readiness
Säkerställ att registry, parity, evals och release assets följer 1.5.0-modellen.

### 9. Slutlig release-readiness
Synka README/PROJECT/STATUS och verifiera att migreringen är mergeklar.
