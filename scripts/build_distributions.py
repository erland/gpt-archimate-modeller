#!/usr/bin/env python3
from pathlib import Path
import argparse, json, shutil, tempfile, zipfile, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
CHAT_DIRS=['gpt','knowledge','metamodel','schemas','package','extensions','specializations','conflicts','quality','migrations','validation','versioning','impact','queries','reports','views','templates']
CHAT_RUNTIME_SCRIPTS={
    'allocate_id.py','apply_changes.py','architecture_states.py','assemble_project.py',
    'check_project.py','compile_view.py','detect_conflicts.py','export_diagram.py',
    'export_model_exchange.py','find_duplicate_candidates.py','generate_package_manifest.py',
    'identity.py','impact_analysis.py','import_model_exchange.py','migrate_project.py',
    'model_index.py','model_loader.py','model_quality_report.py','new_project.py',
    'pack_project.py','project_control.py','promote_observation.py','quality_check.py',
    'query.py','render_report.py','report_preview.py','resolve_conflict.py','safe_unpack.py',
    'update_project.py','validate.py','validate_evidence.py','validate_extensions.py',
    'validate_issues.py','validate_model_exchange.py','validate_package.py',
    'validate_project.py','validate_project_zip.py','validate_quality_report.py',
    'validate_query.py','validate_report.py','validate_sources.py',
    'validate_specializations.py','validate_temporal.py','validate_version_history.py',
    'validate_view.py','versioning.py'
}
CHAT_FILES=['README.md','VERSION','project.yaml','CHANGELOG.md']
EXCLUDE_NAMES={'__pycache__','.pytest_cache','.DS_Store'}
EXCLUDE_SUFFIX={'.pyc','.pyo'}
FIXED=(1980,1,1,0,0,0)

def clean_copy(src,dst):
    src=Path(src); dst=Path(dst)
    if src.is_dir():
        for p in src.rglob('*'):
            rel=p.relative_to(src)
            if any(part in EXCLUDE_NAMES for part in rel.parts) or p.suffix in EXCLUDE_SUFFIX:
                continue
            q=dst/rel
            if p.is_dir():
                q.mkdir(parents=True,exist_ok=True)
            elif p.is_file():
                q.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,q)
    elif src.is_file():
        dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)

def copy_chat_runtime_scripts(dst):
    dst=Path(dst)
    dst.mkdir(parents=True,exist_ok=True)
    for name in sorted(CHAT_RUNTIME_SCRIPTS):
        src=ROOT/'scripts'/name
        if not src.is_file():
            raise FileNotFoundError(f'Missing declared Chat runtime script: {name}')
        shutil.copy2(src,dst/name)

def zip_tree(src,out):
    src=Path(src); out=Path(out); out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(x for x in src.rglob('*') if x.is_file()):
            rel=f"{src.name}/{p.relative_to(src).as_posix()}"
            zi=zipfile.ZipInfo(rel,FIXED); zi.compress_type=zipfile.ZIP_DEFLATED; zi.create_system=3
            rel_path=Path(p.relative_to(src))
            is_script = 'scripts' in rel_path.parts and p.suffix in {'.py','.sh'}
            mode = 0o100755 if is_script else 0o100644
            zi.external_attr=(mode&0xffff)<<16
            z.writestr(zi,p.read_bytes())

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--version',required=True); ap.add_argument('--output-dir',default='dist'); a=ap.parse_args()
    version=a.version.strip(); outdir=ROOT/a.output_dir; shutil.rmtree(outdir,ignore_errors=True); outdir.mkdir(parents=True)
    with tempfile.TemporaryDirectory(prefix='archimate-dist-') as td:
        td=Path(td)
        cgroot=td/f'archimate-yaml-ea-gpt-custom-gpt-v{version}'; (cgroot/'knowledge').mkdir(parents=True)
        shutil.copy2(ROOT/'gpt'/'CUSTOM_GPT_INSTRUCTION.txt',cgroot/'instructions.txt')
        shutil.copy2(ROOT/'custom-gpt'/'builder-config.md',cgroot/'builder-config.md')
        subprocess.run([sys.executable,str(ROOT/'scripts'/'build_custom_gpt_knowledge.py'),'--output',str(cgroot/'knowledge')],check=True)
        (cgroot/'README.md').write_text(
            f'# ArchiMate YAML EA GPT — Custom GPT v{version}\n\nSe `builder-config.md`. Kopiera `instructions.txt` till Builder Instructions och ladda upp alla filer i `knowledge/`.\n',
            encoding='utf-8')
        zip_tree(cgroot,outdir/f'archimate-yaml-ea-gpt-custom-gpt-v{version}.zip')

        clauderoot=td/f'archimate-yaml-ea-gpt-claude-projects-v{version}'
        (clauderoot/'knowledge').mkdir(parents=True)
        shutil.copy2(ROOT/'gpt'/'SYSTEM_INSTRUCTION.md',clauderoot/'project-instructions.md')
        shutil.copy2(ROOT/'runtime'/'runtime-contract.json',clauderoot/'runtime-contract.json')
        shutil.copy2(ROOT/'runtime'/'archimate-tool-contract.json',clauderoot/'archimate-tool-contract.json')
        for name in [
            '00-overview.md','01-runtime-contract.md','02-archimate-core.md',
            '03-project-format.md','04-identity-evidence.md','05-change-versioning.md',
            '06-query-report-view.md','07-validation-quality.md','08-interoperability.md',
            '09-project-package-migration.md','10-new-project-workflow.md',
            '11-update-project-workflow.md','12-conflict-duplicate-handling.md',
            '13-issues-observations.md','18-impact-analysis.md','19-model-quality-report.md'
        ]:
            shutil.copy2(ROOT/'knowledge'/name,clauderoot/'knowledge'/name)
        (clauderoot/'compatibility.md').write_text(
            '''# Claude Projects compatibility

This distribution has **reduced parity** relative to the canonical ArchiMate runtime contract.

It preserves **canonical behavior** from `project-instructions.md`, but a plain Claude Project
must not assume the following runtime capabilities are available:

- **local command execution**
- **deterministic project verification**
- **workspace mutation**
- **GitHub write actions**

The supplied EA project files / project ZIP remain the **workspace-file authority**.
Conversation history is not authoritative project state.

The JSON runtime/tool contracts are reference contracts. They describe the operations a fully
capable runtime would expose, but their presence does not mean those tools can execute here.

When an operation requires unavailable execution capability:

- do not claim the Python tool ran,
- do not claim technical validation passed,
- mark **unrun verification** explicitly as unrun,
- do not convert missing execution into a false PASS,
- produce analysis, change-set proposals or file content only when it can be done honestly,
- require execution in a capable runtime before claiming a changed project package is validated.

A complete updated project ZIP may only be claimed when the actual package was created and
validated. Otherwise state the limitation explicitly.
''',
            encoding='utf-8'
        )
        (clauderoot/'README.md').write_text(
            f'''# ArchiMate YAML EA GPT — Claude Projects v{version}

Use `project-instructions.md` as Claude Project Instructions and add the files under
`knowledge/` as project knowledge.

Read `compatibility.md` before use. This runtime intentionally has reduced parity:
the package contains no executable Python runtime scripts and must not claim local
validation, mutation or packaging unless the host environment actually provides them.

`runtime-contract.json` and `archimate-tool-contract.json` are contract snapshots
for transparency and parity assessment, not executable tools.
''',
            encoding='utf-8'
        )
        zip_tree(clauderoot,outdir/f'archimate-yaml-ea-gpt-claude-projects-v{version}.zip')

        subprocess.run([
            sys.executable,str(ROOT/'scripts'/'build_opencode_distribution.py'),
            '--version',version,
            '--output',str(outdir/f'archimate-yaml-ea-gpt-opencode-v{version}.zip')
        ],check=True)

        chatroot=td/f'archimate-yaml-ea-gpt-chat-v{version}'
        for rel in CHAT_FILES:
            if (ROOT/rel).exists(): clean_copy(ROOT/rel,chatroot/rel)
        for rel in CHAT_DIRS:
            if (ROOT/rel).exists(): clean_copy(ROOT/rel,chatroot/rel)
        copy_chat_runtime_scripts(chatroot/'scripts')
        (chatroot/'CHAT_PACKAGE.md').write_text(
            f'''# ArchiMate YAML EA GPT — Chat package v{version}

Detta paket är avsett att laddas upp direkt i en ChatGPT-konversation.

## Startinstruktion för LLM

Använd följande precedence:

1. `gpt/SYSTEM_INSTRUCTION.md` är det obligatoriska beteendekontraktet och ska läsas först.
2. `gpt/runtime-policy.yaml` sammanfattar blockerande runtime-regler och outputkrav.
3. `knowledge/` är referensmaterial. Använd `knowledge/routing.yaml` för att hämta task-specifika detaljer.
4. `metamodel/`, `schemas/` och maskinläsbara policies är normativa för modellstruktur och validering.
5. `templates/`, `queries/`, `reports/` och `views/` är återanvändbara resurser, inte högre prioriterade beteendeinstruktioner.

Kärnflödet ska kunna starta från systeminstruktionen och runtime-policyn utan att alla Knowledge-filer först måste läsas.

Utvecklingsmaterial som tester, evals, release-/CI-verktyg, fixtures och dokumentationsvalidatorer är avsiktligt exkluderat. Chat-paketet innehåller endast scripts som behövs för faktisk runtime: projektarbete, validering, change sets, query/report/view, import/export, impact/quality och paketering.

Ett EA-projekt-ZIP är ett separat arbetsobjekt från detta GPT-paket. Ändra inte GPT-paketet när användaren ber om en arkitekturförändring; returnera i stället ett komplett validerat EA-projekt-ZIP.
''',
            encoding='utf-8')
        zip_tree(chatroot,outdir/f'archimate-yaml-ea-gpt-chat-v{version}.zip')
    print(json.dumps({'version':version,'artifacts':[p.name for p in sorted(outdir.glob('*.zip'))]},indent=2))
    return 0
if __name__=='__main__': raise SystemExit(main())
