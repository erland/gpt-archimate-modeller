#!/usr/bin/env python3
from pathlib import Path
import argparse, json, shutil, tempfile, zipfile, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
CHAT_DIRS=['gpt','knowledge','metamodel','schemas','package','extensions','specializations','conflicts','quality','migrations','validation','versioning','impact','queries','reports','views','templates','scripts']
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

def zip_tree(src,out):
    src=Path(src); out=Path(out); out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(x for x in src.rglob('*') if x.is_file()):
            rel=f"{src.name}/{p.relative_to(src).as_posix()}"
            zi=zipfile.ZipInfo(rel,FIXED); zi.compress_type=zipfile.ZIP_DEFLATED; zi.create_system=3; zi.external_attr=(0o100644&0xffff)<<16
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
        (chatroot/'CHAT_PACKAGE.md').write_text(
            f'# Chat package v{version}\n\nDetta paket är avsett att laddas upp och användas som GPT-paket direkt i en ChatGPT-konversation.\n\nUtvecklingsmaterial som `tests/`, `evals/`, `examples/`, `docs/developer/` och releasehistorik är avsiktligt exkluderat. Canonical runtime-regler, scripts, schemas, templates och Knowledge finns kvar.\n',
            encoding='utf-8')
        zip_tree(chatroot,outdir/f'archimate-yaml-ea-gpt-chat-v{version}.zip')
    print(json.dumps({'version':version,'artifacts':[p.name for p in sorted(outdir.glob('*.zip'))]},indent=2))
    return 0
if __name__=='__main__': raise SystemExit(main())
