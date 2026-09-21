#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

REQUIRED={
  'README.md','AGENTS.md','opencode.json',
  '.opencode/runtime-contract.json','.opencode/tool-mapping.json',
  '.opencode/tools/archimate.ts','runtime/scripts/project_control.py',
  'runtime/scripts/update_project.py','runtime/scripts/new_project.py',
  'runtime/scripts/query.py','runtime/scripts/impact_analysis.py',
  'runtime/scripts/model_quality_report.py','runtime/scripts/export_diagram.py',
  'runtime/scripts/export_model_exchange.py','runtime/scripts/import_model_exchange.py',
  'knowledge/01-runtime-contract.md','knowledge/02-archimate-core.md',
  'knowledge/03-project-format.md','knowledge/07-validation-quality.md'
}
MUTATING={'archimate_create_project','archimate_apply_project_change'}
EXPECTED={
 'archimate_inspect_project','archimate_inspect_project_zip','archimate_validate_project',
 'archimate_validate_project_zip','archimate_create_project','archimate_apply_project_change',
 'archimate_package_project','archimate_query_model','archimate_impact_analysis',
 'archimate_model_quality_report','archimate_render_report','archimate_export_view',
 'archimate_export_model_exchange','archimate_import_model_exchange_preview'
}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('zipfile'); a=ap.parse_args()
    errors=[]
    with zipfile.ZipFile(a.zipfile) as z:
        if z.testzip(): errors.append('corrupt OpenCode distribution')
        names=set(z.namelist())
        roots={n.split('/')[0] for n in names if n}
        if len(roots)!=1:
            errors.append('expected one distribution root')
            root=''
        else:
            root=next(iter(roots))+'/'
        relnames={n[len(root):] for n in names if n.startswith(root)}
        for req in sorted(REQUIRED):
            if req not in relnames: errors.append('missing '+req)
        if 'CLAUDE.md' in relnames: errors.append('CLAUDE.md must not be used for OpenCode')
        forbidden=[n for n in relnames if n.startswith('runtime/scripts/') and Path(n).name in {
            'build_distributions.py','validate_distributions.py','run_tests.py',
            'build_custom_gpt_knowledge.py','validate_llm_evals.py'
        }]
        if forbidden: errors.append('development scripts packaged: '+', '.join(sorted(forbidden)))

        agents=z.read(root+'AGENTS.md').decode('utf-8').casefold()
        for marker in ['yaml-projektet är source of truth','stable ids','change set','project zip contract']:
            if marker.casefold() not in agents: errors.append('AGENTS.md missing '+marker)

        cfg=json.loads(z.read(root+'opencode.json').decode('utf-8'))
        permissions=cfg.get('permission',{})
        for builtin in ['bash','edit','write']:
            if permissions.get(builtin)!='deny': errors.append(f'{builtin} must be denied')
        for tool in EXPECTED:
            expected='ask' if tool in MUTATING else 'allow'
            if permissions.get(tool)!=expected: errors.append(f'{tool} permission must be {expected}')

        snap=json.loads(z.read(root+'.opencode/runtime-contract.json').decode('utf-8'))
        if snap.get('runtime')!='opencode' or snap.get('compatibility')!='equivalent':
            errors.append('OpenCode runtime snapshot must be equivalent')
        pr=snap.get('project_root',{})
        if pr.get('explicit_argument')!='projectRoot' or pr.get('runtime_workspace_is_not_target_project') is not True:
            errors.append('projectRoot separation missing')
        if pr.get('path_traversal')!='forbidden': errors.append('path traversal policy missing')
        oc=snap.get('canonical_contract',{}).get('runtime_compatibility',{}).get('opencode',{})
        if oc.get('status')!='implemented' or oc.get('target')!='equivalent':
            errors.append('canonical OpenCode status must be implemented/equivalent')

        mapping=json.loads(z.read(root+'.opencode/tool-mapping.json').decode('utf-8')).get('tools',{})
        if {x['opencode_tool'] for x in mapping.values()}!=EXPECTED:
            errors.append('OpenCode tool mapping set mismatch')
        for entry in mapping.values():
            if entry.get('mutates_canonical_state') and entry.get('approval')!='ask':
                errors.append('mutating mapped tool must require approval')
            if not entry.get('input_schema',{}).get('properties',{}).get('projectRoot'):
                errors.append('mapped tool missing projectRoot schema')

        ts=z.read(root+'.opencode/tools/archimate.ts').decode('utf-8')
        if 'from "@opencode-ai/plugin"' not in ts: errors.append('typed OpenCode tool helper missing')
        if 'tool.schema' not in ts: errors.append('typed argument schemas missing')
        if 'Bun.spawn' not in ts: errors.append('Python runtime invocation missing')
        if 'Path escapes OpenCode worktree' not in ts: errors.append('runtime path guard missing')
        for name in EXPECTED:
            export=name.removeprefix('archimate_')
            if f'export const {export} = tool(' not in ts:
                errors.append('missing custom tool export '+export)

    if errors:
        print('FAILED')
        for e in errors: print('-',e)
        return 1
    print('OK')
    print('OpenCode distribution: typed canonical ArchiMate tools, explicit projectRoot, guarded mutations')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
