#!/usr/bin/env python3
from pathlib import Path
import argparse,datetime as dt,importlib.util,json,sys,tempfile,time,traceback,subprocess,shutil,xml.etree.ElementTree as ET,yaml
ROOT=Path(__file__).resolve().parents[1]; SCRIPTS=ROOT/'scripts'; sys.path.insert(0,str(SCRIPTS))
def lm(name,p):
    spec=importlib.util.spec_from_file_location(name,p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
assemble=lm('assemble_project',SCRIPTS/'assemble_project.py'); sys.modules['assemble_project']=assemble
query=lm('query',SCRIPTS/'query.py'); sys.modules['query']=query
quality=lm('quality_check',SCRIPTS/'quality_check.py'); sys.modules['quality_check']=quality
temporal=lm('validate_temporal',SCRIPTS/'validate_temporal.py'); sys.modules['validate_temporal']=temporal
states=lm('architecture_states',SCRIPTS/'architecture_states.py'); sys.modules['architecture_states']=states
compile_view=lm('compile_view',SCRIPTS/'compile_view.py'); sys.modules['compile_view']=compile_view
export_diagram=lm('export_diagram',SCRIPTS/'export_diagram.py'); sys.modules['export_diagram']=export_diagram
validate=lm('validate',SCRIPTS/'validate.py'); issues=lm('validate_issues',SCRIPTS/'validate_issues.py')
new_project=lm('new_project',SCRIPTS/'new_project.py'); pack_project=lm('pack_project',SCRIPTS/'pack_project.py'); zipval=lm('validate_project_zip',SCRIPTS/'validate_project_zip.py')
impact=lm('impact_analysis',SCRIPTS/'impact_analysis.py'); mqr=lm('model_quality_report',SCRIPTS/'model_quality_report.py'); render=lm('render_report',SCRIPTS/'render_report.py')
migrate=lm('migrate_project',SCRIPTS/'migrate_project.py')
export_mx=lm('export_model_exchange',SCRIPTS/'export_model_exchange.py'); import_mx=lm('import_model_exchange',SCRIPTS/'import_model_exchange.py')
class R:
    def __init__(self,sel=None,ff=False): self.sel=set(sel or []); self.ff=ff; self.stop=False; self.tests=[]
    def run(self,id,suite,fn):
        if self.stop:return
        if self.sel and suite not in self.sel: self.tests.append({'id':id,'suite':suite,'status':'skipped','duration_ms':0,'message':'suite not selected'}); return
        t=time.perf_counter()
        try:
            d=fn(); rec={'id':id,'suite':suite,'status':'passed','duration_ms':int((time.perf_counter()-t)*1000)}
            if d is not None: rec['details']=d
            self.tests.append(rec)
        except Exception as e:
            self.tests.append({'id':id,'suite':suite,'status':'failed','duration_ms':int((time.perf_counter()-t)*1000),'message':str(e),'details':{'traceback':traceback.format_exc(limit=5)}})
            if self.ff:self.stop=True
    def result(self,start,dur):
        p=sum(x['status']=='passed' for x in self.tests); f=sum(x['status']=='failed' for x in self.tests); s=sum(x['status']=='skipped' for x in self.tests)
        return {'test_run':{'version':'0.1','status':'failed' if f else 'passed','started_at':start,'duration_ms':dur,'summary':{'total':len(self.tests),'passed':p,'failed':f,'skipped':s},'tests':self.tests}}
def noerr(f):
    e=[x for x in f if x['severity']=='error']; assert not e,e

def build_tests(r):
    ref=ROOT/'examples'/'ea-project-split'; cat=yaml.safe_load((ROOT/'tests'/'fixtures'/'fixture-catalog.yaml').read_text())
    def core():
        l,f=validate.validate(ref); noerr(f); return {'elements':len(l['model']['elements']),'relationships':len(l['model']['relationships'])}
    r.run('T-CORE-001','core_validation',core)
    r.run('T-CORE-002','core_validation',lambda: ({'issue_errors':0} if not issues.validate_file(ref/'issues'/'issues.yaml',ref) else (_ for _ in ()).throw(AssertionError('issue validation failed'))))
    r.run('T-CORE-003','core_validation',lambda: ({'warnings':len(temporal.validate_temporal(ref)[1])} if not temporal.validate_temporal(ref)[0] else (_ for _ in ()).throw(AssertionError(temporal.validate_temporal(ref)[0]))))
    def format02_controls():
        logical={'model':{
            'elements':[
                {'id':'TEC-000001','type':'TechnologyService','name':'Service'},
                {'id':'STR-000001','type':'Capability','name':'Capability'},
            ],
            'relationships':[
                {'id':'REL-000001','type':'Association','source':'TEC-000001','target':'STR-000001','properties':{'impact_themes':'privacy'}},
                {'id':'REL-000002','type':'Association','source':'TEC-000001','target':'STR-000001'},
            ],
        },'impact_themes':[{'id':'privacy','label':'Privacy'}]}
        findings=[]; validate.check_impact_themes(logical,findings); assert not findings,findings
        logical['model']['relationships'][0]['properties']['impact_themes']='unknown_theme'
        findings=[]; validate.check_impact_themes(logical,findings)
        assert len(findings)==1 and findings[0]['code']=='IMPACT-THEME-UNKNOWN',findings
        rel_findings=[]; validate.check_relationship_pairs(logical,rel_findings,False)
        uncovered=[x for x in rel_findings if x['code']=='ARCH-REL-PAIR-UNCOVERED']
        assert len(uncovered)==1,uncovered
        return {'impact_theme_validation':'controlled','aggregated_uncovered_pair_findings':len(uncovered)}
    r.run('T-CORE-004','core_validation',format02_controls)
    def refs():
        ids=[]
        for x in cat['reference_projects']:
            p=ROOT/x['path']; _,f=validate.validate(p); noerr(f); assert not issues.validate_file(p/'issues'/'issues.yaml',p); assert not temporal.validate_temporal(p)[0]; assert not states.validate_states(p); ids.append(x['id'])
        return {'validated':ids}
    r.run('T-REF-001','reference_projects',refs)
    def msgs(root,sub):
        if sub in ('technical_validation','relationship_validation','evidence','extensions','specializations'):
            _,f=validate.validate(root); return [f"{x.get('code','')}: {x.get('message','')}" for x in f if x['severity']=='error']
        if sub=='temporal':return temporal.validate_temporal(root)[0]
        if sub=='architecture_states':return states.validate_states(root)
        if sub=='issues_observations':return issues.validate_file(root/'issues'/'issues.yaml',root)
        return []
    def invalid():
        ok=[]
        for x in cat['invalid_fixtures']:
            m=msgs(ROOT/x['path'],x['subsystem']); assert m; assert x['expected_fragment'].lower() in '\n'.join(m).lower(),(x,m); ok.append(x['id'])
        return {'matched':ok}
    r.run('T-FIX-001','invalid_fixtures',invalid)
    def qrv():
        logical,e=assemble.assemble(ref); assert not e,e; qc=rc=vc=0
        for p in sorted((ROOT/'queries').glob('*.yaml')): query.execute(logical,yaml.safe_load(p.read_text())); qc+=1
        for p in list(sorted((ROOT/'reports').glob('*.yaml')))+list(sorted((ROOT/'reports'/'standard').glob('*.yaml'))):
            d=yaml.safe_load(p.read_text());
            if isinstance(d,dict) and 'report' in d: render.render_markdown(ref,p); rc+=1
        for p in list(sorted((ROOT/'views').glob('*.yaml')))+list(sorted((ROOT/'views'/'standard').glob('*.yaml'))):
            if p.name=='standard-library.yaml': continue
            d=yaml.safe_load(p.read_text());
            if not (isinstance(d,dict) and 'view' in d): continue
            vr=compile_view.compile_view(logical,d,p,ref)['view_result']; ET.fromstring(export_diagram.build_drawio(vr,d)); assert export_diagram.build_mermaid(vr,d).startswith('flowchart '); vc+=1
        return {'queries':qc,'reports':rc,'views':vc}
    r.run('T-QRV-001','queries_reports_views',qrv)
    def query_cli():
        p=subprocess.run(
            [sys.executable,str(SCRIPTS/'query.py'),str(ref),str(ROOT/'queries'/'all-elements.yaml'),'--json'],
            cwd=ROOT,capture_output=True,text=True
        )
        assert p.returncode==0,(p.stdout,p.stderr)
        payload=json.loads(p.stdout)
        assert payload['query_result']['query_id']=='all-elements',payload
        assert payload['query_result']['count']>=1,payload
        big={'project':{'id':'BIG','model_version':'1.0.0'},'model':{
            'elements':[{'id':f'APP-{i:06d}','type':'ApplicationComponent','name':f'App {i}'} for i in range(1,251)],
            'relationships':[]}}
        qr=query.execute(big,{'query':{'id':'big','select':'elements','return':{'fields':['id']}}},max_rows=200)['query_result']
        assert qr['matched_count']==250 and qr['returned_count']==200 and qr['truncated'] is True,qr
        return {'query_id':payload['query_result']['query_id'],'count':payload['query_result']['count'],'bounded_rows':qr['returned_count']}
    r.run('T-QRV-002','queries_reports_views',query_cli)
    def wf():
        spec=yaml.safe_load((ROOT/'examples'/'new-project'/'new-project.yaml').read_text())
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/spec['new_project']['id']; res=new_project.create(root,spec); assert res['validation_errors']==0
            descriptor=yaml.safe_load((root/'project.yaml').read_text(encoding='utf-8'))
            assert descriptor['format_version']=='0.2',descriptor
            assert descriptor['files']['impact_themes']=='extensions/impact-themes.yaml',descriptor
            assert (root/'extensions'/'impact-themes.yaml').exists()
            z=Path(td)/'p.zip'; pack_project.pack(root,z); rr,ee,ww=zipval.validate_zip(z); assert not ee,ee
            return {'zip_status':rr['status'],'warnings':len(ww),'format_version':descriptor['format_version']}
    r.run('T-WF-001','project_workflows',wf)
    def migration_01_02():
        src=ROOT/'tests'/'reference-projects'/'RP-002-layered-example'
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/'legacy'
            shutil.copytree(src,root)
            descriptor=yaml.safe_load((root/'project.yaml').read_text(encoding='utf-8'))
            assert descriptor['format_version']=='0.1',descriptor
            descriptor.setdefault('files',{})['impact_themes']='extensions/impact-themes.yaml'
            (root/'project.yaml').write_text(yaml.safe_dump(descriptor,sort_keys=False,allow_unicode=True,width=120),encoding='utf-8')
            themes={'format_version':'0.1','impact_themes':[{'id':'privacy','label':'Privacy'}]}
            (root/'extensions'/'impact-themes.yaml').write_text(yaml.safe_dump(themes,sort_keys=False,allow_unicode=True),encoding='utf-8')
            before=(root/'extensions'/'impact-themes.yaml').read_text(encoding='utf-8')
            comp=migrate.compatibility(root)
            assert comp['status']=='migration_available' and comp['steps']==['MIG-000002'],comp
            temp,preview_root,steps=migrate.apply_to_copy(root)
            try:
                pd=yaml.safe_load((preview_root/'project.yaml').read_text(encoding='utf-8'))
                pt=yaml.safe_load((preview_root/'extensions'/'impact-themes.yaml').read_text(encoding='utf-8'))
                assert pd['format_version']=='0.2',pd
                assert pt['format_version']=='0.2' and pt['impact_themes'][0]['id']=='privacy',pt
                assert (root/'project.yaml').read_text(encoding='utf-8').find("format_version: '0.1'")>=0
            finally:
                shutil.rmtree(temp,ignore_errors=True)
            applied=migrate.apply(root)
            assert applied['status']=='migrated' and applied['steps']==['MIG-000002'],applied
            assert migrate.compatibility(root)['status']=='current'
            hist=yaml.safe_load((root/'migrations'/'history.yaml').read_text(encoding='utf-8'))
            assert hist['history'][-1]['id']=='MIG-000002',hist
            after=yaml.safe_load((root/'extensions'/'impact-themes.yaml').read_text(encoding='utf-8'))
            assert after['impact_themes']==themes['impact_themes'],after
            assert not (root/'PACKAGE-MANIFEST.yaml').exists()
            out=Path(td)/'migrated.zip'
            pack_project.pack(root,out)
            rr,ee,ww=zipval.validate_zip(out); assert not ee,ee
            return {'migration':applied['steps'][0],'themes_preserved':len(after['impact_themes']),'zip_status':rr['status']}
    r.run('T-WF-002','project_workflows',migration_01_02)
    def interop():
        with tempfile.TemporaryDirectory() as td:
            xml=Path(td)/'m.xml'; logical,errs=assemble.assemble(ref); assert not errs,errs; xml.write_text(export_mx.build_exchange(logical),encoding='utf-8'); assert xml.exists(); preview=import_mx.parse(xml); return {'elements':len(preview['elements']),'relationships':len(preview['relationships'])}
    r.run('T-INT-001','interoperability',interop)
    def st():
        p=ROOT/'tests'/'fixtures'/'architecture-states-example'; assert not states.validate_states(p); x=states.resolve_state(p,'STA-000003'); return {'elements':len(x['elements']),'relationships':len(x['relationships'])}
    r.run('T-STATE-001','change_architecture',st)
    def aq():
        logical,e=assemble.assemble(ref); assert not e
        imp=impact.analyze(logical,['STR-000001'],direction='incoming',max_depth=3)
        assert any(x['id']=='APP-000001' for x in imp['impacts'])
        tie_logical={'model':{
            'elements':[
                {'id':'A','type':'Capability','name':'A'},
                {'id':'B','type':'Capability','name':'B'},
                {'id':'C','type':'Capability','name':'C'},
                {'id':'D','type':'Capability','name':'D'},
            ],
            'relationships':[
                {'id':'R1','type':'Association','source':'A','target':'B'},
                {'id':'R2','type':'Association','source':'A','target':'C'},
                {'id':'R3','type':'Association','source':'B','target':'D'},
                {'id':'R4','type':'Association','source':'C','target':'D'},
            ],
        }}
        tie=impact.analyze(tie_logical,['A'],direction='outgoing',max_depth=2)
        assert any(x['id']=='D' and x['depth']==2 for x in tie['impacts'])
        q=mqr.result_for_project(ref)['model_quality_result']
        assert 0.0 <= q['summary']['score'] <= 100.0,q['summary']
        assert set(q['summary']['dimensions'])=={'architecture','ownership','evidence'},q['summary']
        return {'impact_count':imp['impacted_count'],'tie_path_count':tie['impacted_count'],'quality_score':q['summary']['score'],'quality_dimensions':q['summary']['dimensions']}
    r.run('T-AQ-001','analysis_quality',aq)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--suite',action='append'); ap.add_argument('--fail-fast',action='store_true'); ap.add_argument('--format',choices=['text','json','yaml'],default='text'); ap.add_argument('--output'); a=ap.parse_args()
    start=dt.datetime.now(dt.timezone.utc).isoformat(); t=time.perf_counter()
    try:
        r=R(a.suite,a.fail_fast); build_tests(r); result=r.result(start,int((time.perf_counter()-t)*1000))
        if a.format=='json': text=json.dumps(result,indent=2,ensure_ascii=False)+'\n'
        elif a.format=='yaml': text=yaml.safe_dump(result,sort_keys=False,allow_unicode=True,width=120)
        else:
            s=result['test_run']['summary']; lines=[f"Status: {result['test_run']['status']}",f"Total: {s['total']}  Passed: {s['passed']}  Failed: {s['failed']}  Skipped: {s['skipped']}"]+[f"[{x['status'].upper()}] {x['id']} ({x['suite']}) {x.get('message','')}".rstrip() for x in result['test_run']['tests']]; text='\n'.join(lines)+'\n'
        if a.output: Path(a.output).write_text(text,encoding='utf-8')
        else: print(text,end='')
        return 0 if result['test_run']['status']=='passed' else 1
    except Exception as e:
        print('TEST RUNNER ERROR'); print(e); return 2
if __name__=='__main__': raise SystemExit(main())
