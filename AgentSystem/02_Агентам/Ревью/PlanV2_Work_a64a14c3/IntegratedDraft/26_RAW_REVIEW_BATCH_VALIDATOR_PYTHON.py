import copy, hashlib, json, pathlib, sys

ROLES=[f'R{i}' for i in range(1,11)]
def sha(b): return hashlib.sha256(b).hexdigest()
def bad(status,rc,detail=''): return {'ok':False,'status':status,'rc':rc,'detail':detail}
def good(value): return {'ok':True,'status':'BATCH_VALID','rc':0,'value':value}
def no_dups(pairs):
 d={}
 for k,v in pairs:
  if k in d: raise ValueError('duplicate:'+k)
  d[k]=v
 return d
def parse_raw(raw):
 if raw.startswith(b'\xef\xbb\xbf') or b'\r' in raw or b'\x00' in raw or not raw.endswith(b'\n') or raw.endswith(b'\n\n'): raise ValueError('encoding')
 return json.loads(raw.decode('utf-8'),object_pairs_hook=no_dups)
def exact(obj,keys): return isinstance(obj,dict) and len(obj)==len(keys) and set(obj)==set(keys)
def adequate(x): return isinstance(x,dict) and x.get('assessment')=='ADEQUATE' and isinstance(x.get('reason'),str) and len(x['reason'])>0
def validate_record(o,role,e):
 if any(k in o for k in ('schema_valid','go_semantics_valid','record_sha256')): return bad('STOP_CALLER_ASSERTED_VALIDITY',24)
 if o.get('reviewer_role')!=role or o.get('review_id')!=f"N8N-V2-{role}-{e['subject_envelope_sha256'][:16]}": return bad('STOP_ROLE_ID_MISMATCH',25)
 for k in ('plan_sha256','content_set_sha256','subject_envelope_sha256','manifest_sha256','validation_index_sha256'):
  if o.get(k)!=e[k]: return bad('STOP_MANIFEST_MISMATCH' if k=='manifest_sha256' else 'STOP_SUBJECT_MISMATCH',22,k)
 if o.get('plan_bytes')!=e['plan_bytes']: return bad('STOP_SUBJECT_MISMATCH',22,'plan_bytes')
 if not exact(o.get('disposition_assessments'),e['finding_ids']) or not exact(o.get('cluster_assessments'),e['cluster_ids']) or not exact(o.get('xd_assessments'),e['xd_ids']) or not exact(o.get('audit_assessments'),e['audit_ids']): return bad('STOP_REVIEW_SCHEMA_INVALID',24,'exact-set')
 if any(not adequate(x) for m in ('disposition_assessments','cluster_assessments','xd_assessments') for x in o[m].values()): return bad('STOP_REVIEW_SCHEMA_INVALID',24,'assessment')
 for aid in e['audit_ids']:
  x=o['audit_assessments'][aid]
  if x.get('source_item_sha256')!=e['audit_hashes'][aid]: return bad('STOP_AUDIT_CLAIM_MISMATCH',24,aid)
  if x.get('audit_id')!=aid or x.get('closure') not in ('CLOSED','OPEN','BLOCKED') or x.get('assessment') not in ('ADEQUATE','INADEQUATE','UNVERIFIABLE'): return bad('STOP_REVIEW_SCHEMA_INVALID',24,aid)
 if not isinstance(o.get('new_findings'),list) or not isinstance(o.get('unresolved_design_conflicts'),int) or o.get('verdict') not in ('GO','CHANGES_REQUIRED','STOP','BLOCKED'): return bad('STOP_REVIEW_SCHEMA_INVALID',24)
 sem=all(adequate(x) for m in ('disposition_assessments','cluster_assessments','xd_assessments') for x in o[m].values()) and all(o['audit_assessments'][aid]['closure']=='CLOSED' and o['audit_assessments'][aid]['assessment']=='ADEQUATE' for aid in e['audit_ids']) and not o['new_findings'] and o['unresolved_design_conflicts']==0
 if o['verdict']=='GO' and not sem: return bad('STOP_CONTRADICTORY_GO',27)
 return good({'semantic_go':sem,'verdict':o['verdict'],'new_findings':o['new_findings']})
def validate_batch(rows,e,summary=None):
 if len(rows)!=10 or {x['slot'] for x in rows}!=set(ROLES): return bad('STOP_INVALID_REVIEW_SET',24)
 hashes=[sha(x['raw']) for x in rows]
 if len(set(hashes))!=10: return bad('STOP_DUPLICATE_REVIEW_HASH',25)
 ids=set();valid=[]
 for role in ROLES:
  row=next(x for x in rows if x['slot']==role)
  try:o=parse_raw(row['raw'])
  except Exception as ex:return bad('STOP_DUPLICATE_JSON_KEY' if 'duplicate:' in str(ex) else 'STOP_REVIEW_SCHEMA_INVALID',24,str(ex))
  if o.get('review_id') in ids:return bad('STOP_DUPLICATE_REVIEW_ID',25)
  ids.add(o.get('review_id'));r=validate_record(o,role,e)
  if not r['ok']:return r
  valid.append((role,o,r['value']['semantic_go'],sha(row['raw'])))
 counts={'go_count':sum(o['verdict']=='GO' for _,o,_,_ in valid),'stop_count':sum(o['verdict']=='STOP' for _,o,_,_ in valid),'blocked_count':sum(o['verdict']=='BLOCKED' for _,o,_,_ in valid),'changes_required_count':sum(o['verdict']=='CHANGES_REQUIRED' for _,o,_,_ in valid),'contradictory_go_count':sum(o['verdict']=='GO' and not sem for _,o,sem,_ in valid)}
 findings=[f for _,o,_,_ in valid for f in o['new_findings']];p0=sum(f.get('severity')=='P0' for f in findings);p1={}
 for f in [x for x in findings if x.get('severity')=='P1']:p1.setdefault(f.get('canonical_new_finding_sha256'),set()).add(f.get('reviewer_role'))
 counts.update(validated_p0_count=p0,consensus_p1_count=sum(len(x)>=2 for x in p1.values()),valid_review_count=10)
 verdict='STOP' if counts['stop_count'] or counts['blocked_count'] or counts['validated_p0_count'] or counts['consensus_p1_count'] or counts['contradictory_go_count'] else ('GO' if counts['go_count']>=8 else 'CHANGES_REQUIRED')
 if summary is not None:
  for k,v in {**counts,'verdict':verdict}.items():
   if summary.get(k)!=v:return bad('STOP_COUNTER_OR_VERDICT_CONTRADICTION',27,k)
 if verdict=='STOP':return bad('STOP_QUORUM_BLOCKED_PRESENT' if counts['blocked_count'] else ('STOP_QUORUM_STOP_PRESENT' if counts['stop_count'] else 'STOP_QUORUM_POLICY'),27,json.dumps(counts,separators=(',',':')))
 if verdict=='CHANGES_REQUIRED':return bad('QUORUM_CHANGES_REQUIRED',26,json.dumps(counts,separators=(',',':')))
 return good({'counts':counts,'verdict':verdict,'record_hashes':{role:h for role,_,_,h in valid}})
def env():
 root=pathlib.Path(__file__).resolve().parent;work=root.parent
 baseline=json.loads((work/'00_FINDINGS_BASELINE.json').read_text(encoding='utf-8'));closure=json.loads((root/'08_CONSENSUS_CLOSURE_V2.json').read_text(encoding='utf-8'));audit=json.loads((root/'24_PROSPECTIVE_AUDIT_R2_BASELINE.json').read_text(encoding='utf-8'))
 return {'plan_bytes':1,'plan_sha256':'1'*64,'content_set_sha256':'2'*64,'subject_envelope_sha256':'3'*64,'manifest_sha256':'4'*64,'validation_index_sha256':'5'*64,'finding_ids':sorted(x['finding_id'] for x in baseline['findings']),'cluster_ids':sorted(x['cluster_id'] for x in closure['clusters']),'xd_ids':sorted(x['integration_decision_id'] for x in closure['cross_domain_decisions']['decisions']),'audit_ids':audit['required_ids'],'audit_hashes':{x:audit['items'][x]['source_item_sha256'] for x in audit['required_ids']}}
def record(role,e):
 assess=lambda ids:{x:{'assessment':'ADEQUATE','reason':f'independent exact assessment {x}'} for x in ids}
 return {'review_id':f"N8N-V2-{role}-{e['subject_envelope_sha256'][:16]}",'reviewer_role':role,'model':'independent-reviewer','reasoning_level':'xhigh','plan_bytes':e['plan_bytes'],'plan_sha256':e['plan_sha256'],'content_set_sha256':e['content_set_sha256'],'subject_envelope_sha256':e['subject_envelope_sha256'],'manifest_sha256':e['manifest_sha256'],'validation_index_sha256':e['validation_index_sha256'],'verdict':'GO','disposition_assessments':assess(e['finding_ids']),'cluster_assessments':assess(e['cluster_ids']),'xd_assessments':assess(e['xd_ids']),'audit_assessments':{x:{'audit_id':x,'source_item_sha256':e['audit_hashes'][x],'closure':'CLOSED','assessment':'ADEQUATE','plan_section_ids':['R2-C01'],'acceptance_test_ids':['AT-XD-01'],'negative_canary_ids':['NC-XD-01'],'evidence_ids':['EV-XD-01'],'rationale':f'closed {x}'} for x in e['audit_ids']},'new_findings':[],'unresolved_design_conflicts':0,'independence_attestation':'reviewed without outputs of other reviewers','runtime_nonexecution_attestation':'no runtime execution'}
def raw(o):return (json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
def self_test():
 e=env();base=[{'slot':r,'raw':raw(record(r,e))} for r in ROLES];tests=[]
 def run(cid,mut,expected):
  rows=copy.deepcopy(base);summary=mut(rows,e);r=validate_batch(rows,e,summary);tests.append({'canary_id':cid,'expected_status':expected,'actual_status':r['status'],'rc':r['rc'],'result':'REJECTED' if not r['ok'] and r['status']==expected else 'FALSE_ACCEPT'});assert not r['ok'] and r['status']==expected,cid
 run('FG-001',lambda r,e:[x.update(raw=raw({**parse_raw(x['raw']),'verdict':'BLOCKED'})) for x in r[8:]] and None,'STOP_QUORUM_BLOCKED_PRESENT')
 run('FG-002',lambda r,e:r[1].update(raw=raw({**parse_raw(r[1]['raw']),'review_id':parse_raw(r[0]['raw'])['review_id']})),'STOP_DUPLICATE_REVIEW_ID')
 run('FG-003',lambda r,e:r[1].update(raw=r[0]['raw']),'STOP_DUPLICATE_REVIEW_HASH')
 run('FG-004',lambda r,e:r[1].update(raw=raw({**parse_raw(r[1]['raw']),'reviewer_role':'R1'})),'STOP_ROLE_ID_MISMATCH')
 run('FG-005',lambda r,e:r[0].update(raw=raw({**parse_raw(r[0]['raw']),'subject_envelope_sha256':'9'*64})),'STOP_SUBJECT_MISMATCH')
 run('FG-006',lambda r,e:r[0].update(raw=raw({**parse_raw(r[0]['raw']),'manifest_sha256':'9'*64})),'STOP_MANIFEST_MISMATCH')
 wrong={'go_count':9,'stop_count':0,'blocked_count':0,'changes_required_count':0,'contradictory_go_count':0,'validated_p0_count':0,'consensus_p1_count':0,'valid_review_count':10,'verdict':'GO'}
 run('FG-007',lambda r,e:wrong,'STOP_COUNTER_OR_VERDICT_CONTRADICTION');run('FG-008',lambda r,e:{**wrong,'go_count':10,'verdict':'STOP'},'STOP_COUNTER_OR_VERDICT_CONTRADICTION')
 def audit_mut(rows,k,v):o=parse_raw(rows[0]['raw']);o['audit_assessments'][e['audit_ids'][0]][k]=v;rows[0]['raw']=raw(o)
 run('FG-009',lambda r,e:audit_mut(r,'closure','OPEN'),'STOP_CONTRADICTORY_GO');run('FG-010',lambda r,e:audit_mut(r,'assessment','INADEQUATE'),'STOP_CONTRADICTORY_GO')
 run('FG-011',lambda r,e:(lambda o:(o['audit_assessments'].pop(e['audit_ids'][0]),r[0].update(raw=raw(o))))(parse_raw(r[0]['raw'])),'STOP_REVIEW_SCHEMA_INVALID')
 run('FG-012',lambda r,e:(lambda o:(o['audit_assessments'].__setitem__('EXTRA',{}),r[0].update(raw=raw(o))))(parse_raw(r[0]['raw'])),'STOP_REVIEW_SCHEMA_INVALID')
 run('FG-013',lambda r,e:audit_mut(r,'source_item_sha256','0'*64),'STOP_AUDIT_CLAIM_MISMATCH')
 run('FG-014',lambda r,e:(lambda o:(o['disposition_assessments'].pop(next(iter(o['disposition_assessments']))),r[0].update(raw=raw(o))))(parse_raw(r[0]['raw'])),'STOP_REVIEW_SCHEMA_INVALID')
 run('FG-015',lambda r,e:(lambda o:(o['cluster_assessments'].pop(next(iter(o['cluster_assessments']))),r[0].update(raw=raw(o))))(parse_raw(r[0]['raw'])),'STOP_REVIEW_SCHEMA_INVALID')
 run('FG-016',lambda r,e:(lambda o:(o['xd_assessments'].pop(next(iter(o['xd_assessments']))),r[0].update(raw=raw(o))))(parse_raw(r[0]['raw'])),'STOP_REVIEW_SCHEMA_INVALID')
 try:parse_raw(b'{"review_id":"a","review_id":"b"}\n');ds='FALSE_ACCEPT'
 except Exception as ex:ds='STOP_DUPLICATE_JSON_KEY' if 'duplicate:' in str(ex) else 'WRONG'
 tests.append({'canary_id':'FG-017','expected_status':'STOP_DUPLICATE_JSON_KEY','actual_status':ds,'rc':24,'result':'REJECTED' if ds=='STOP_DUPLICATE_JSON_KEY' else 'FALSE_ACCEPT'});assert ds=='STOP_DUPLICATE_JSON_KEY'
 run('FG-018',lambda r,e:(lambda o:(o.__setitem__('schema_valid',True),r[0].update(raw=raw(o))))(parse_raw(r[0]['raw'])),'STOP_CALLER_ASSERTED_VALIDITY')
 run('FG-019',lambda r,e:r[0].update(raw=raw({**parse_raw(r[0]['raw']),'verdict':'STOP'})),'STOP_QUORUM_STOP_PRESENT')
 run('FG-020',lambda r,e:r.pop(),'STOP_INVALID_REVIEW_SET')
 positive=validate_batch(base,e);assert positive['ok'] and positive['value']['verdict']=='GO';return {'validator':'RAW-BATCH-PYTHON-B','result':'PASS','rc':0,'positive_verdict':'GO','canaries':tests}
if __name__=='__main__':
 try:print(json.dumps(self_test(),ensure_ascii=False,separators=(',',':')))
 except Exception as ex:print(json.dumps({'validator':'RAW-BATCH-PYTHON-B','result':'FAIL','rc':29,'error':str(ex)},separators=(',',':')));sys.exit(29)
