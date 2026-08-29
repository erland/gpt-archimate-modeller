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
