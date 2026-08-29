#!/usr/bin/env python3
from pathlib import Path
import argparse, shutil, yaml
ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); a=ap.parse_args()
    out=Path(a.output); shutil.rmtree(out,ignore_errors=True); out.mkdir(parents=True)
    cfg=yaml.safe_load((ROOT/'custom-gpt'/'knowledge-map.yaml').read_text(encoding='utf-8'))
    for bundle in cfg['bundles']:
        parts=[f"# {bundle['file'].removesuffix('.md').replace('-', ' ').title()}\n"]
        for rel in bundle['sources']:
            p=ROOT/rel
            parts.extend([f"\n---\n\n## Källa: `{rel}`\n\n",p.read_text(encoding='utf-8').strip(),"\n"])
        (out/bundle['file']).write_text(''.join(parts),encoding='utf-8')
    refs={
      '06-archimate-reference.yaml':['metamodel/elements.yaml','metamodel/relationships.yaml','metamodel/relationship-rules.yaml','metamodel/relationship-matrix.yaml'],
      '07-organization-profiles.yaml':['extensions/standard-extensions.yaml','specializations/standard-specializations.yaml','conflicts/policy.yaml'],
      '08-runtime-contracts.yaml':['gpt/runtime-policy.yaml','package/project-zip-contract.yaml','package/zip-robustness.yaml','versioning/policy.yaml'],
    }
    for name,sources in refs.items():
        doc={'generated_knowledge_version':'0.1','sources':[]}
        for rel in sources:
            p=ROOT/rel
            doc['sources'].append({'path':rel,'content':yaml.safe_load(p.read_text(encoding='utf-8'))})
        (out/name).write_text(yaml.safe_dump(doc,sort_keys=False,allow_unicode=True,width=120),encoding='utf-8')
    print(f'OK: {out}')
    return 0
if __name__=='__main__': raise SystemExit(main())
