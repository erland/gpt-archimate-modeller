#!/usr/bin/env python3
from pathlib import Path
import argparse, zipfile
ROOT=Path(__file__).resolve().parents[1]

def members(z): return [i.filename for i in z.infolist() if not i.is_dir()]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--version',required=True); ap.add_argument('--dist-dir',default='dist'); a=ap.parse_args()
    d=ROOT/a.dist_dir; version=a.version
    custom=d/f'archimate-yaml-ea-gpt-custom-gpt-v{version}.zip'; chat=d/f'archimate-yaml-ea-gpt-chat-v{version}.zip'; errors=[]
    for p in (custom,chat):
        if not p.exists(): errors.append(f'Missing {p.name}'); continue
        with zipfile.ZipFile(p) as z:
            if z.testzip(): errors.append(f'Corrupt {p.name}')
            names=members(z); roots={n.split('/')[0] for n in names}
            if len(roots)!=1: errors.append(f'{p.name}: expected one root')
            bad=[n for n in names if '__pycache__/' in n or n.endswith(('.pyc','.pyo'))]
            if bad: errors.append(f'{p.name}: cache files: {bad[:5]}')
    if custom.exists():
        with zipfile.ZipFile(custom) as z:
            n=members(z); root=n[0].split('/')[0]+'/'
            for req in ['README.md','builder-config.md','instructions.txt','knowledge/00-runtime-workflows.md','knowledge/06-archimate-reference.yaml']:
                if root+req not in n: errors.append(f'custom: missing {req}')
            inst=z.read(root+'instructions.txt').decode('utf-8')
            if len(inst)>8000: errors.append(f'custom instructions exceed 8000 chars: {len(inst)}')
            if any('/tests/' in '/'+x or '/evals/' in '/'+x for x in n): errors.append('custom: contains development test/eval files')
    if chat.exists():
        with zipfile.ZipFile(chat) as z:
            infos=[i for i in z.infolist() if not i.is_dir()]
            n=[i.filename for i in infos]; root=n[0].split('/')[0]+'/'
            for req in ['CHAT_PACKAGE.md','gpt/SYSTEM_INSTRUCTION.md','gpt/runtime-policy.yaml','scripts/new_project.py','scripts/update_project.py','schemas/ea-project.schema.json','templates/ea-project-split/project.yaml']:
                if root+req not in n: errors.append(f'chat: missing {req}')
            for forbidden in ['tests/','evals/','examples/','release/','docs/developer/']:
                if any(x.startswith(root+forbidden) for x in n): errors.append(f'chat: contains forbidden {forbidden}')
            for forbidden_script in ['build_distributions.py','build_custom_gpt_knowledge.py','run_tests.py','run_llm_evals.py','grade_llm_eval.py','generate_large_fixture.py','validate_distributions.py','validate_release_candidate.py','validate_developer_docs.py','validate_user_docs.py','validate_fixture_catalog.py','validate_reference_projects.py','validate_llm_evals.py','validate_gpt_instruction.py']:
                if root+'scripts/'+forbidden_script in n: errors.append(f'chat: contains development script {forbidden_script}')
            bootstrap=z.read(root+'CHAT_PACKAGE.md').decode('utf-8') if root+'CHAT_PACKAGE.md' in n else ''
            for marker in ['gpt/SYSTEM_INSTRUCTION.md','gpt/runtime-policy.yaml','knowledge/routing.yaml','Kärnflödet ska kunna starta']:
                if marker not in bootstrap: errors.append(f'chat: bootstrap missing marker {marker}')
            for info in infos:
                rel=info.filename[len(root):]
                if rel.startswith('scripts/') and Path(rel).suffix in {'.py','.sh'}:
                    mode=(info.external_attr>>16)&0o777
                    if mode != 0o755: errors.append(f'chat: runtime script is not executable: {rel} mode={oct(mode)}')
    if errors:
        print('FAILED'); [print('-',e) for e in errors]; return 1
    print('OK'); print(f'Custom GPT: {custom.name}'); print(f'Chat: {chat.name}'); return 0
if __name__=='__main__': raise SystemExit(main())
