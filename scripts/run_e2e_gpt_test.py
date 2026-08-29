#!/usr/bin/env python3
from pathlib import Path
import argparse,zipfile,shutil,yaml,json,hashlib,sys,importlib.util,tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
def lm(name,p):
    spec=importlib.util.spec_from_file_location(name,p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); sys.modules[name]=m; return m
asm=lm('assemble_project',ROOT/'scripts'/'assemble_project.py')
query=lm('query',ROOT/'scripts'/'query.py')
quality=lm('quality_check',ROOT/'scripts'/'quality_check.py')
temp=lm('validate_temporal',ROOT/'scripts'/'validate_temporal.py')
mi=lm('model_index',ROOT/'scripts'/'model_index.py')
loader=lm('model_loader',ROOT/'scripts'/'model_loader.py')
zv=lm('validate_project_zip',ROOT/'scripts'/'validate_project_zip.py')
pack=lm('pack_project',ROOT/'scripts'/'pack_project.py')
safe=lm('safe_unpack',ROOT/'scripts'/'safe_unpack.py')
val=lm('validate',ROOT/'scripts'/'validate.py')
pcmod=lm('project_control',ROOT/'scripts'/'project_control.py')
applym=lm('apply_changes',ROOT/'scripts'/'apply_changes.py')
migrate=lm('migrate_project',ROOT/'scripts'/'migrate_project.py')
identity=lm('identity',ROOT/'scripts'/'identity.py')
newp=lm('new_project',ROOT/'scripts'/'new_project.py')
upd=lm('update_project',ROOT/'scripts'/'update_project.py')
impact=lm('impact_analysis',ROOT/'scripts'/'impact_analysis.py')
mqr=lm('model_quality_report',ROOT/'scripts'/'model_quality_report.py')
compilev=lm('compile_view',ROOT/'scripts'/'compile_view.py')
exportd=lm('export_diagram',ROOT/'scripts'/'export_diagram.py')
grader=lm('grade_llm_eval',ROOT/'scripts'/'grade_llm_eval.py')
EX=ROOT/'examples'/'end-to-end'
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output-dir'); a=ap.parse_args()
    outdir=Path(a.output_dir) if a.output_dir else Path(tempfile.mkdtemp(prefix='ea-e2e-')); outdir.mkdir(parents=True,exist_ok=True); keep=bool(a.output_dir)
    results=[]
    try:
        initial=outdir/'project-initial.zip'; nr=newp.create_zip(yaml.safe_load((EX/'new-project.yaml').read_text()),initial); assert nr['validation_errors']==0 and initial.exists(); assert not zv.validate_zip(initial)[1]
        ih=hashlib.sha256(initial.read_bytes()).hexdigest(); results.append({'id':'E2E-001','status':'passed'})
        updated=outdir/'project-updated.zip'; ur=upd.do_update(initial,EX/'CHG-000001.yaml',updated); assert ur['status']=='updated',ur; assert ur['model_version_before']=='0.1.0' and ur['model_version_after']=='0.2.0'; assert {'STR-000001','APP-000001','REL-000001'}.issubset(set(ur['touched'])); assert hashlib.sha256(initial.read_bytes()).hexdigest()==ih; results.append({'id':'E2E-002','status':'passed','details':{'version_after':'0.2.0','input_immutable':True}})
        d=upd.do_update(updated,EX/'CHG-000002-duplicate.yaml',outdir/'duplicate-no.zip'); assert d['status']=='duplicate_candidates' and not (outdir/'duplicate-no.zip').exists(); results.append({'id':'E2E-003','status':'passed'})
        s=upd.do_update(updated,EX/'CHG-000003-stale.yaml',outdir/'stale-no.zip'); assert s['status']=='stale_change_set' and not (outdir/'stale-no.zip').exists(); results.append({'id':'E2E-004','status':'passed'})
        project=outdir/'project'; project.mkdir(exist_ok=True)
        with zipfile.ZipFile(updated) as z: z.extractall(project)
        logical,errs,_=loader.load_model(project); assert not errs,errs
        imp=impact.analyze(logical,['STR-000001'],direction='incoming',max_depth=3); it=impact.to_markdown(imp,'E2E impact'); assert 'APP-000001' in it and 'REL-000001' in it and 'do not by themselves prove real-world causal impact' in it; (outdir/'impact.md').write_text(it); results.append({'id':'E2E-005','status':'passed'})
        qr=mqr.result_for_project(project); qt=mqr.to_markdown(qr); assert 'Modellkvalitetsrapport' in qt and 'not an absolute architecture maturity rating' in qr['model_quality_result']['interpretation']; (outdir/'quality.md').write_text(qt); results.append({'id':'E2E-006','status':'passed'})
        viewp=ROOT/'views'/'standard'/'capability-realization.yaml'; viewdoc=yaml.safe_load(viewp.read_text()); compiled=compilev.compile_view(logical,viewdoc,viewp,project)['view_result']; dio=exportd.build_drawio(compiled,viewdoc); mmd=exportd.build_mermaid(compiled,viewdoc); assert 'APP-000001' in dio and 'STR-000001' in dio and 'APP_000001' in mmd and 'STR_000001' in mmd; (outdir/'view.drawio').write_text(dio); (outdir/'view.mmd').write_text(mmd); results.append({'id':'E2E-007','status':'passed'})
        assert not zv.validate_zip(updated)[1]
        with zipfile.ZipFile(updated) as z:
            names=set(z.namelist()); assert 'MODEL-INDEX.json' in names and 'PACKAGE-MANIFEST.yaml' in names
        results.append({'id':'E2E-008','status':'passed','details':{'sha256':hashlib.sha256(updated.read_bytes()).hexdigest()}})
        cat=yaml.safe_load((ROOT/'evals'/'catalog.yaml').read_text()); n=0
        for item in cat['cases']:
            case=yaml.safe_load((ROOT/item['file']).read_text()); response=(ROOT/'evals'/'grader-fixtures'/'passing'/f"{item['id']}.md").read_text(); g=grader.grade(case,response); assert g['status']=='passed',(item['id'],g); n+=1
        assert n==12; results.append({'id':'E2E-009','status':'passed','details':{'total':12,'passed':12,'failed':0}})
        result={'e2e_gpt_test':{'version':'0.1','status':'passed','summary':{'total':9,'passed':9,'failed':0},'results':results,'interpretation':'Deterministic project/toolchain E2E and observable LLM contract passed; no claim is made that a separate hosted Custom GPT session was executed.'}}
        (outdir/'e2e-result.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n'); print(json.dumps(result,indent=2,ensure_ascii=False)); return 0
    except Exception as e:
        print(json.dumps({'e2e_gpt_test':{'version':'0.1','status':'failed','error':str(e),'results':results}},indent=2,ensure_ascii=False)); return 1
    finally:
        if keep and (outdir/'project').exists(): shutil.rmtree(outdir/'project')
        if not keep: shutil.rmtree(outdir,ignore_errors=True)
if __name__=='__main__': raise SystemExit(main())
