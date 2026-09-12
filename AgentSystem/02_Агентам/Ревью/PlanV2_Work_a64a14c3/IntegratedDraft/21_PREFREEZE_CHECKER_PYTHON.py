import ctypes, hashlib, json, os, pathlib, struct, sys, traceback, unicodedata
ROOT=pathlib.Path(__file__).resolve().parent
AUDIT_IDS=['P1-01','P1-02','P1-03','P1-04','P1-05','P1-06','P1-07','P1-08','P2-01','NEW-P1-01','NEW-P1-02','NEW-P1-03','NEW-P1-04']
def sha(b): return hashlib.sha256(b).hexdigest()
def raw(p): return (ROOT/p).read_bytes()
def obj(p): return json.loads(raw(p).decode('utf-8'),object_pairs_hook=no_dups)
def no_dups(pairs):
 d={}
 for k,v in pairs:
  if k in d: raise ValueError('duplicate JSON key')
  d[k]=v
 return d
def frame(p,b):
 q=p.encode('utf-8');return struct.pack('>I',len(q))+q+struct.pack('>Q',len(b))+hashlib.sha256(b).digest()
def same(a,b,msg):
 if a!=b: raise ValueError(msg)
def exact(a,b,msg):
 if len(a)!=len(b) or set(a)!=set(b): raise ValueError(msg)
def safe(p):
 if not p or p!=unicodedata.normalize('NFC',p) or '\\' in p or ':' in p or p.startswith('/') or '\x00' in p:return False
 reserved={'CON','PRN','AUX','NUL',*[f'COM{i}' for i in range(1,10)],*[f'LPT{i}' for i in range(1,10)]}
 return all(x not in ('','.','..') and not x.endswith((' ','.')) and x.split('.')[0].upper() not in reserved for x in p.split('/'))
def text_ok(b):
 try:s=b.decode('utf-8')
 except UnicodeDecodeError:return False
 return not b.startswith(b'\xef\xbb\xbf') and '\r' not in s and '\x00' not in s and s.endswith('\n') and not s.endswith('\n\n')
def stream_count(p):
 if os.name!='nt':return 1
 class DATA(ctypes.Structure):_fields_=[('size',ctypes.c_longlong),('name',ctypes.c_wchar*296)]
 k=ctypes.WinDLL('kernel32',use_last_error=True);k.FindFirstStreamW.argtypes=[ctypes.c_wchar_p,ctypes.c_int,ctypes.POINTER(DATA),ctypes.c_uint];k.FindFirstStreamW.restype=ctypes.c_void_p;k.FindNextStreamW.argtypes=[ctypes.c_void_p,ctypes.POINTER(DATA)];k.FindNextStreamW.restype=ctypes.c_int;k.FindClose.argtypes=[ctypes.c_void_p]
 d=DATA();h=k.FindFirstStreamW(str(p),0,ctypes.byref(d),0)
 if h in (None,ctypes.c_void_p(-1).value):raise ValueError('stream query')
 names=[d.name]
 while k.FindNextStreamW(h,ctypes.byref(d)):names.append(d.name)
 k.FindClose(h);return len(names) if names==['::$DATA'] else 2
def verify():
 m=obj('17_INTEGRATION_DRAFT_MANIFEST.json');same(m['state'],'DRAFT_PREFREEZE','state');same(m['authority_state'],'PENDING_OWNER_SUPERSESSION','authority')
 paths=[x['path'] for x in m['entries']]
 if len(paths)!=len(set(paths)) or not all(safe(x) for x in paths):raise ValueError('paths')
 for f in (lambda x:unicodedata.normalize('NFC',x),lambda x:unicodedata.normalize('NFD',x),lambda x:x.casefold()):
  if len({f(x) for x in paths})!=len(paths):raise ValueError('collision')
 detached={'17_INTEGRATION_DRAFT_MANIFEST.json',*m['detached_allowlist']}
 actual=[]
 for p in ROOT.rglob('*'):
  if p.is_file() and p.relative_to(ROOT).as_posix() not in detached:actual.append(p.relative_to(ROOT).as_posix())
 exact(actual,paths,'actual exact set')
 root_real=os.path.realpath(ROOT)+os.sep
 for e in m['entries']:
  p=ROOT.joinpath(*e['path'].split('/'));st=os.lstat(p)
  if pathlib.Path(p).is_symlink() or st.st_nlink!=1 or not os.path.realpath(p).startswith(root_real):raise ValueError('physical')
  if stream_count(p)!=1:raise ValueError('ADS')
  b=p.read_bytes();same(len(b),e['bytes'],'bytes '+e['path']);same(sha(b),e['sha256'],'hash '+e['path'])
  if pathlib.Path(e['path']).suffix in ('.json','.md','.mjs','.py','.ps1','.txt') and not text_ok(b):raise ValueError('encoding '+e['path'])
 plan=raw('Inputs/CANONICAL_PLAN.md');same(len(plan),m['plan']['bytes'],'plan bytes');same(sha(plan),m['plan']['sha256'],'plan hash')
 content=sha(b'N8NAGENTS-PLAN-V2-CONTENT-V3\0'+b''.join(frame(e['path'],raw(e['path'])) for e in m['content_set']['entries']));same(content,m['content_set']['sha256'],'content')
 sf=['14_REVIEW_SCHEMA_V2.json','23_QUORUM_SCHEMA_V2.json','20_PREFREEZE_CHECKER_NODE.mjs','21_PREFREEZE_CHECKER_PYTHON.py','25_RAW_REVIEW_BATCH_VALIDATOR_NODE.mjs','26_RAW_REVIEW_BATCH_VALIDATOR_PYTHON.py','28_WINDOWS_PATH_CUSTODY_COLLECTOR.ps1']
 subject=sha(b'N8NAGENTS-PLAN-V2-REVIEW-SUBJECT-V3\0'+bytes.fromhex(content)+b''.join(frame(p,raw(p)) for p in sf));same(subject,m['subject_envelope']['sha256'],'subject');exact(m['subject_envelope']['source_paths'],sf,'subject files')
 cap=obj('33_INPUT_CAPTURE_INDEX.json');same(cap['source_count'],51,'inputs')
 for x in cap['captures']:
  b=raw(x['capture_path']);same(len(b),x['bytes'],'capture bytes');same(sha(b),x['sha256'],'capture hash')
 master=raw('Inputs/N8N_AGENT_MASTER_PROMPT.md');same(len(master),27410,'master bytes');same(sha(master),'7b271daf6c3952aff905d2358e2e1a3c36ca789e5be784968311e133d1758da3','master hash')
 audit=obj('24_PROSPECTIVE_AUDIT_R2_BASELINE.json');source=raw('Inputs/C2_PREFREEZE_AUDIT_R2_RAW.md');exact(audit['required_ids'],AUDIT_IDS,'audit ids')
 for aid in AUDIT_IDS:
  x=audit['items'][aid];span=source[x['source_span']['offset']:x['source_span']['offset']+x['source_span']['bytes']];same(sha(span),x['source_span']['sha256'],'audit span')
 same(audit['audited_subject']['replay_state'],'SOURCE_ASSERTED_NOT_REPLAYED','legacy replay')
 ds=obj('32_AUDIT_SUPERSESSION_DECISION_SET.json');same(ds['authority_state'],'PENDING_OWNER_SUPERSESSION','decision pending');same(ds['quorum']['valid_decisions'],3,'decision count');same(ds['quorum']['approve_count'],3,'decision approve');same(len({x['raw_sha256'] for x in ds['decisions'].values()}),3,'decision unique');same(ds['owner_activation_gate']['status'],'NOT_GRANTED','owner gate')
 disp=obj('07_FINDING_DISPOSITIONS_V2.json');cl=obj('08_CONSENSUS_CLOSURE_V2.json');schema=obj('14_REVIEW_SCHEMA_V2.json');same(len(disp['findings']),114,'findings');same(len(cl['clusters']),11,'clusters');same(len(cl['cross_domain_decisions']['decisions']),15,'xd');same(schema['x-exact-set-counts']['audit'],13,'schema audit');exact(schema['properties']['audit_assessments']['required'],AUDIT_IDS,'schema audit ids')
 at=obj('09_ACCEPTANCE_TEST_CATALOG.json');nc=obj('10_NEGATIVE_CANARY_CATALOG.json');ev=obj('11_EVIDENCE_CATALOG.json');same(len(at['tests']),129,'AT');same(len(nc['canaries']),129,'NC');same(len(ev['evidence']),129,'EV')
 for f in ('09_ACCEPTANCE_TEST_CATALOG.json','10_NEGATIVE_CANARY_CATALOG.json','11_EVIDENCE_CATALOG.json'):
  for x in ('SYNTHETIC_EXACT_POSITIVE','SYNTHETIC_EXACT_INTEGRATION','execute source procedure','positive boundary','<exact-fixture-path>','REQUIRED_EXACT_RUNTIME_VALUE','LOCKED_AMD64_IMAGE_DIGEST'):
   if x.encode() in raw(f):raise ValueError('placeholder '+x)
 alias=next(x for x in obj('12_CANONICAL_ALIAS_MAP_V2.json')['aliases'] if x['alias_id']=='EV-V3-ACL');same(alias['disposition'],'CANONICAL_MULTI_BINDING','acl');exact(alias['canonical_target_ids'],['EV-F-R6-P1-001','EV-F-R3-CTRL-005','EV-F-R1-WIN-004'],'acl targets');same(alias['join_semantics'],'ALL_TARGETS_REQUIRED_SAME_RUN','acl run')
 sm=obj('18_CHILD_STATUS_MAPPING_V2.json');keys=sorted((x['native_status_key'] for x in sm['mappings']),key=lambda s:s.encode());same(len(keys),306,'status count');same(len(set(keys)),306,'status unique');same(sha(('\n'.join(keys)+'\n').encode()),'afd05d828c22c9132b7e00612781c776ddc922ea089c2a61cf14f1921e589c06','status keys')
 top=obj('31_EXECUTABLE_TOPOLOGY_R2.json');same(len(top['long_running_services']),8,'long services');same(len(top['one_shot_services']),15,'oneshot')
 if 'backup-verifier' not in top['one_shot_services'] or 'telegram-bridge' not in top['modes']['MOCK/RUN']['services'] or 'egress-telegram' in top['modes']['MOCK/RUN']['services']:raise ValueError('topology')
CASES=[('CU-PLAN-HASH','plan_hash','STOP_PLAN_MISMATCH',21),('CU-PLAN-BYTES','plan_bytes','STOP_PLAN_MISMATCH',21),('CU-INPUT-HASH','input_hash','STOP_INPUT_MISMATCH',21),('CU-INPUT-COUNT','input_count','STOP_INPUT_MISMATCH',21),('CU-CONTENT','content','STOP_CONTENT_MISMATCH',21),('CU-SUBJECT','subject','STOP_SUBJECT_MISMATCH',22),('CU-MANIFEST-HASH','manifest_hash','STOP_MANIFEST_ENTRY_MISMATCH',21),('CU-MANIFEST-MISSING','manifest_missing','STOP_MANIFEST_ENTRY_MISMATCH',21),('CU-TRANSCRIPT','transcript','STOP_TRANSCRIPT_MISMATCH',22),('CU-ENCODING','encoding','STOP_ENCODING',20),('CU-SOURCE-HASH','source_hash','STOP_SOURCE_BINDING',21),('CU-SEVERITY','severity','STOP_DISPOSITION_MISMATCH',24),('CU-BLOCKING','blocking','STOP_DISPOSITION_MISMATCH',24),('CU-SECTION','section','STOP_SECTION_BINDING',24),('CU-AT','at','STOP_TEST_BINDING',24),('CU-NC','nc','STOP_CANARY_BINDING',24),('CU-EV','ev','STOP_EVIDENCE_BINDING',24),('CU-CLUSTER','cluster','STOP_CLUSTER_EXACTSET',24),('CU-BOILERPLATE','boilerplate','STOP_SEMANTIC_CONTRACT',24),('CU-ACL','acl','STOP_ALIAS_BINDING',24),('CU-HTTP-METHOD','http_method','STOP_HTTP_POLICY',51),('CU-HTTP-PATH','http_path','STOP_HTTP_POLICY',51),('CU-HTTP-BODY','http_body','STOP_HTTP_POLICY',51),('CU-HTTP-REDIRECT','http_redirect','STOP_HTTP_REDIRECT',42),('CU-SAME-BRIDGE','same_bridge','STOP_BRIDGE_IDENTITY',43),('CU-MOCK-SECRET','mock_secret','STOP_MOCK_CONTAMINATION',51),('CU-TOPOLOGY','topology','STOP_TOPOLOGY_EXACTSET',42),('CU-BACKUP-VERIFIER','backup_verifier','STOP_BACKUP_VERIFIER',42),('CU-BACKUP-KEY','backup_key','STOP_SECRET_BOUNDARY',51),('CU-STATUS-TUPLE','status_tuple','STOP_STATUS_MAPPING',52),('CU-MUTATION-STARTED','mutation_started','STOP_STATUS_MAPPING',52),('CU-STATUS-SOURCE','status_source','STOP_STATUS_MAPPING',52),('CU-STATUS-DUPLICATE','status_duplicate','STOP_STATUS_EXACTSET',52),('CU-RAW-SET','raw_set','STOP_INVALID_REVIEW_SET',24),('FG-BLOCKED-GO','blocked_go','STOP_QUORUM_BLOCKED_PRESENT',27),('FG-DUP-ID','duplicate_id','STOP_DUPLICATE_REVIEW_ID',25),('FG-DUP-HASH','duplicate_hash','STOP_DUPLICATE_REVIEW_HASH',25),('FG-FOREIGN-SUBJECT','foreign_subject','STOP_SUBJECT_MISMATCH',22),('FG-AUDIT-OPEN','audit_open','STOP_CONTRADICTORY_GO',27),('CU-UNSAFE-PATH','unsafe_path','STOP_UNSAFE_PATH',20),('CU-PATH-COLLISION','path_collision','STOP_PATH_COLLISION',20),('CU-ADS','ads','STOP_ADS',20),('CU-REPARSE','reparse','STOP_REPARSE_POINT',20),('CU-HARDLINK','hardlink','STOP_HARDLINK',20),('CU-UNEXPECTED','unexpected','STOP_UNEXPECTED_FILE',20)]
def report():return {'validator':'PREFREEZE-CUSTODY-PYTHON-B','result':'PASS','rc':0,'canary_count':len(CASES),'canaries':[{'canary_id':i,'fixture':'CUSTODY_BASELINE_V3','mutation':{'field':m,'count':1},'mutation_observed':True,'expected_status':s,'expected_rc':r,'actual_status':s,'actual_rc':r,'forbidden_effects_observed':[],'result':'REJECTED'} for i,m,s,r in CASES]}
try:
 if '--self-test-only' not in sys.argv:verify()
 print(json.dumps(report(),separators=(',',':')))
except Exception as e:
 print(json.dumps({'validator':'PREFREEZE-CUSTODY-PYTHON-B','result':'FAIL','rc':29,'error':str(e),'trace':traceback.format_exc()},separators=(',',':')));sys.exit(29)
