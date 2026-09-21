#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import tempfile
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FIXED=(1980,1,1,0,0,0)

RUNTIME_SCRIPTS={
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

KNOWLEDGE_FILES=[
    '00-overview.md','01-runtime-contract.md','02-archimate-core.md','03-project-format.md',
    '04-identity-evidence.md','05-change-versioning.md','06-query-report-view.md',
    '07-validation-quality.md','08-interoperability.md','09-project-package-migration.md',
    '10-new-project-workflow.md','11-update-project-workflow.md',
    '12-conflict-duplicate-handling.md','13-issues-observations.md',
    '14-standard-report-library.md','15-standard-views.md','16-baseline-target-transition.md',
    '17-time-lifecycle.md','18-impact-analysis.md','19-model-quality-report.md',
    '23-large-zip-robustness.md','24-model-index.md','25-user-docs.md',
    'knowledge-index.yaml','routing.yaml'
]

TOOLS_TS=r'''import { tool } from "@opencode-ai/plugin"
import path from "node:path"

function safePath(worktree: string, raw: string): string {
  const root = path.resolve(worktree)
  const resolved = path.resolve(root, raw)
  if (resolved !== root && !resolved.startsWith(root + path.sep)) {
    throw new Error("Path escapes OpenCode worktree: " + raw)
  }
  return resolved
}

async function runPython(script: string, argv: string[], context: any): Promise<string> {
  const scriptPath = path.join(context.worktree, "runtime", "scripts", script)
  const proc = Bun.spawn(["python3", scriptPath, ...argv], {
    cwd: context.worktree,
    stdout: "pipe",
    stderr: "pipe",
  })
  const [stdout, stderr, code] = await Promise.all([
    new Response(proc.stdout).text(),
    new Response(proc.stderr).text(),
    proc.exited,
  ])
  if (code !== 0) {
    throw new Error((stderr || stdout || ("Tool failed with exit code " + code)).trim())
  }
  return stdout.trim()
}

export const inspect_project = tool({
  description: "Inspect an unpacked EA project without mutation.",
  args: { projectRoot: tool.schema.string() },
  async execute(args, context) {
    return runPython("project_control.py", ["inspect-project", safePath(context.worktree,args.projectRoot), "--json"], context)
  },
})

export const inspect_project_zip = tool({
  description: "Inspect and validate an EA project ZIP.",
  args: { projectRoot: tool.schema.string(), zipFile: tool.schema.string() },
  async execute(args, context) {
    safePath(context.worktree,args.projectRoot)
    return runPython("project_control.py", ["inspect-zip", safePath(context.worktree,args.zipFile), "--json"], context)
  },
})

export const validate_project = tool({
  description: "Run technical, history and quality validation for an unpacked EA project.",
  args: { projectRoot: tool.schema.string() },
  async execute(args, context) {
    return runPython("project_control.py", ["validate-project", safePath(context.worktree,args.projectRoot), "--json"], context)
  },
})

export const validate_project_zip = tool({
  description: "Validate a complete EA project ZIP against the package contract.",
  args: { projectRoot: tool.schema.string(), zipFile: tool.schema.string() },
  async execute(args, context) {
    safePath(context.worktree,args.projectRoot)
    return runPython("validate_project_zip.py", [safePath(context.worktree,args.zipFile)], context)
  },
})

export const create_project = tool({
  description: "Create a new EA project from a structured specification. Canonical mutation; requires approval.",
  args: {
    projectRoot: tool.schema.string(),
    specFile: tool.schema.string(),
    outputDir: tool.schema.string(),
    outputZip: tool.schema.string(),
  },
  async execute(args, context) {
    safePath(context.worktree,args.projectRoot)
    return runPython("new_project.py", [
      "--spec", safePath(context.worktree,args.specFile),
      "--output-dir", safePath(context.worktree,args.outputDir),
      "--output-zip", safePath(context.worktree,args.outputZip),
      "--json",
    ], context)
  },
})

export const apply_project_change = tool({
  description: "Apply an explicit change set to an existing project ZIP. Canonical mutation; requires approval.",
  args: {
    projectRoot: tool.schema.string(),
    inputZip: tool.schema.string(),
    changeSet: tool.schema.string(),
    outputZip: tool.schema.string(),
    allowMigration: tool.schema.boolean().optional(),
    allowDuplicateCandidates: tool.schema.boolean().optional(),
  },
  async execute(args, context) {
    safePath(context.worktree,args.projectRoot)
    const argv=[safePath(context.worktree,args.inputZip),safePath(context.worktree,args.changeSet),"--output",safePath(context.worktree,args.outputZip),"--json"]
    if (args.allowMigration) argv.push("--allow-migration")
    if (args.allowDuplicateCandidates) argv.push("--allow-duplicate-candidates")
    return runPython("update_project.py", argv, context)
  },
})

export const package_project = tool({
  description: "Package and validate the current EA workspace as a complete project ZIP.",
  args: { projectRoot: tool.schema.string(), outputZip: tool.schema.string() },
  async execute(args, context) {
    return runPython("project_control.py", ["pack",safePath(context.worktree,args.projectRoot),"--output",safePath(context.worktree,args.outputZip)], context)
  },
})

export const query_model = tool({
  description: "Execute a canonical model query.",
  args: {
    projectRoot: tool.schema.string(),
    queryFile: tool.schema.string(),
    output: tool.schema.string().optional(),
  },
  async execute(args, context) {
    const argv=[safePath(context.worktree,args.projectRoot),safePath(context.worktree,args.queryFile),"--json"]
    if (args.output) argv.push("--output",safePath(context.worktree,args.output))
    return runPython("query.py",argv,context)
  },
})

export const impact_analysis = tool({
  description: "Analyze dependency impact from model seeds, state transition or a change set.",
  args: {
    projectRoot: tool.schema.string(),
    seeds: tool.schema.array(tool.schema.string()).optional(),
    changeSet: tool.schema.string().optional(),
    fromState: tool.schema.string().optional(),
    toState: tool.schema.string().optional(),
    direction: tool.schema.enum(["outgoing","incoming","both"]).optional(),
    maxDepth: tool.schema.number().int().min(1).max(20).optional(),
    relationshipTypes: tool.schema.array(tool.schema.string()).optional(),
    excludeRelationshipTypes: tool.schema.array(tool.schema.string()).optional(),
    includeSeeds: tool.schema.boolean().optional(),
    stopTypes: tool.schema.array(tool.schema.string()).optional(),
    includePaths: tool.schema.boolean().optional(),
    format: tool.schema.enum(["yaml","json","markdown"]).optional(),
    output: tool.schema.string().optional(),
  },
  async execute(args, context) {
    const argv=[safePath(context.worktree,args.projectRoot)]
    for (const x of args.seeds ?? []) argv.push("--seed",x)
    if (args.changeSet) argv.push("--change-set",safePath(context.worktree,args.changeSet))
    if (args.fromState) argv.push("--from-state",args.fromState)
    if (args.toState) argv.push("--to-state",args.toState)
    argv.push("--direction",args.direction ?? "both")
    argv.push("--max-depth",String(args.maxDepth ?? 3))
    for (const x of args.relationshipTypes ?? []) argv.push("--relationship-type",x)
    for (const x of args.excludeRelationshipTypes ?? []) argv.push("--exclude-relationship-type",x)
    if (args.includeSeeds) argv.push("--include-seeds")
    for (const x of args.stopTypes ?? []) argv.push("--stop-type",x)
    if (args.includePaths === false) argv.push("--no-paths")
    argv.push("--format",args.format ?? "yaml")
    if (args.output) argv.push("--output",safePath(context.worktree,args.output))
    return runPython("impact_analysis.py",argv,context)
  },
})

export const model_quality_report = tool({
  description: "Generate a model quality report.",
  args: {
    projectRoot: tool.schema.string(),
    profile: tool.schema.string().optional(),
    format: tool.schema.enum(["markdown","csv","json","yaml"]).optional(),
    output: tool.schema.string().optional(),
  },
  async execute(args, context) {
    const argv=[safePath(context.worktree,args.projectRoot),"--format",args.format ?? "markdown"]
    if (args.profile) argv.push("--profile",safePath(context.worktree,args.profile))
    if (args.output) argv.push("--output",safePath(context.worktree,args.output))
    return runPython("model_quality_report.py",argv,context)
  },
})

export const render_report = tool({
  description: "Render a report definition against the current EA project.",
  args: {
    projectRoot: tool.schema.string(),
    reportFile: tool.schema.string(),
    format: tool.schema.enum(["markdown","csv"]).optional(),
    output: tool.schema.string().optional(),
    outputDir: tool.schema.string().optional(),
  },
  async execute(args, context) {
    const argv=[safePath(context.worktree,args.projectRoot),safePath(context.worktree,args.reportFile),"--format",args.format ?? "markdown"]
    if (args.output) argv.push("--output",safePath(context.worktree,args.output))
    if (args.outputDir) argv.push("--output-dir",safePath(context.worktree,args.outputDir))
    return runPython("render_report.py",argv,context)
  },
})

export const export_view = tool({
  description: "Compile and export a view as draw.io or Mermaid.",
  args: {
    projectRoot: tool.schema.string(),
    viewFile: tool.schema.string(),
    format: tool.schema.enum(["drawio","mermaid"]),
    output: tool.schema.string(),
  },
  async execute(args, context) {
    return runPython("export_diagram.py",[
      safePath(context.worktree,args.projectRoot),
      safePath(context.worktree,args.viewFile),
      "--format",args.format,
      "--output",safePath(context.worktree,args.output),
    ],context)
  },
})

export const export_model_exchange = tool({
  description: "Export canonical YAML model to ArchiMate Model Exchange XML.",
  args: { projectRoot: tool.schema.string(), outputXml: tool.schema.string() },
  async execute(args, context) {
    return runPython("export_model_exchange.py",[
      safePath(context.worktree,args.projectRoot),"--output",safePath(context.worktree,args.outputXml)
    ],context)
  },
})

export const import_model_exchange_preview = tool({
  description: "Parse Model Exchange XML as staging preview without merging into canonical model.",
  args: { projectRoot: tool.schema.string(), xmlFile: tool.schema.string() },
  async execute(args, context) {
    safePath(context.worktree,args.projectRoot)
    return runPython("import_model_exchange.py",[safePath(context.worktree,args.xmlFile),"--preview","--json"],context)
  },
})
'''

def zip_tree(src: Path, out: Path):
    out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(x for x in src.rglob('*') if x.is_file()):
            rel=p.relative_to(src).as_posix()
            zi=zipfile.ZipInfo(rel,FIXED); zi.compress_type=zipfile.ZIP_DEFLATED; zi.create_system=3
            mode=0o100755 if rel.startswith('runtime/scripts/') and p.suffix=='.py' else 0o100644
            zi.external_attr=(mode&0xffff)<<16
            z.writestr(zi,p.read_bytes())

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--version',required=True)
    ap.add_argument('--output',required=True)
    a=ap.parse_args()
    version=a.version.strip()
    output=Path(a.output)

    contract=json.loads((ROOT/'runtime/runtime-contract.json').read_text(encoding='utf-8'))
    tools=json.loads((ROOT/'runtime/archimate-tool-contract.json').read_text(encoding='utf-8'))
    cfg=contract['runtime_compatibility']['opencode']
    if cfg.get('status')!='implemented' or cfg.get('target')!='equivalent':
        raise ValueError('OpenCode runtime must be implemented/equivalent before build')

    with tempfile.TemporaryDirectory(prefix='archimate-opencode-') as td:
        root=Path(td)
        shutil.copy2(ROOT/'gpt/SYSTEM_INSTRUCTION.md',root/'AGENTS.md')
        (root/'.opencode/tools').mkdir(parents=True)
        (root/'runtime/scripts').mkdir(parents=True)
        (root/'knowledge').mkdir(parents=True)

        for name in sorted(RUNTIME_SCRIPTS):
            src=ROOT/'scripts'/name
            if not src.is_file(): raise FileNotFoundError(f'Missing runtime script: {name}')
            shutil.copy2(src,root/'runtime/scripts'/name)
        for name in KNOWLEDGE_FILES:
            shutil.copy2(ROOT/'knowledge'/name,root/'knowledge'/name)

        mapping={}
        for t in tools['tools']:
            mapping[t['id']]={
                'opencode_tool':'archimate_'+t['id'].replace('-','_'),
                'abstract_tool':t['abstract_tool'],
                'canonical_script':t['implementation']['script'],
                'packaged_script':'runtime/scripts/'+Path(t['implementation']['script']).name,
                'mutates_canonical_state':t['mutates_canonical_state'],
                'approval':t['approval'],
                'input_schema':t['input_schema'],
            }

        snapshot={
            'schema_version':1,
            'runtime':'opencode',
            'role':'peer_distribution',
            'compatibility':'equivalent',
            'canonical_source':{
                'instructions':'gpt/SYSTEM_INSTRUCTION.md',
                'runtime_contract':'runtime/runtime-contract.json',
                'tool_contract':'runtime/archimate-tool-contract.json',
            },
            'generated_projection':{
                'instructions':'AGENTS.md',
                'runtime_contract':'.opencode/runtime-contract.json',
                'tool_mapping':'.opencode/tool-mapping.json',
                'tool_definitions':'.opencode/tools/archimate.ts',
                'runtime_scripts':'runtime/scripts/',
            },
            'project_root':{
                'explicit_argument':'projectRoot',
                'default':'.',
                'runtime_workspace_is_not_target_project':True,
                'path_traversal':'forbidden',
            },
            'canonical_contract':contract,
        }
        (root/'.opencode/runtime-contract.json').write_text(json.dumps(snapshot,indent=2)+'\n',encoding='utf-8')
        (root/'.opencode/tool-mapping.json').write_text(json.dumps({'schema_version':1,'tools':mapping},indent=2)+'\n',encoding='utf-8')
        (root/'.opencode/tools/archimate.ts').write_text(TOOLS_TS,encoding='utf-8')

        permissions={
            'read':'allow','glob':'allow','grep':'allow',
            'bash':'deny','edit':'deny','write':'deny',
        }
        for t in tools['tools']:
            permissions['archimate_'+t['id'].replace('-','_')]='ask' if t['mutates_canonical_state'] else 'allow'
        config={'$schema':'https://opencode.ai/config.json','permission':permissions}
        (root/'opencode.json').write_text(json.dumps(config,indent=2)+'\n',encoding='utf-8')

        (root/'README.md').write_text(f'''# ArchiMate YAML EA GPT — OpenCode v{version}

Extract this ZIP into a dedicated OpenCode workspace and open that workspace in OpenCode.

- Root `AGENTS.md` is generated from the canonical system instruction.
- The EA project/workspace is separate from this runtime distribution and is always supplied through explicit `projectRoot`.
- Canonical ArchiMate operations are exposed as typed custom tools from `.opencode/tools/archimate.ts`.
- The custom tools call only packaged runtime Python scripts under `runtime/scripts/`.
- Direct `bash`, `edit` and `write` are denied so canonical model mutation cannot bypass the declared change-set tools.
- Mutating canonical tools require approval.
- `.opencode/runtime-contract.json` and `.opencode/tool-mapping.json` are generated projections, not canonical sources.
''',encoding='utf-8')

        zip_tree(root,output)
    print(output)
    return 0

if __name__=='__main__':
    raise SystemExit(main())
