import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const roles=Array.from({length:10},(_,i)=>`R${i+1}`);
const fail=(status,rc,detail='')=>({ok:false,status,rc,detail});
const pass=value=>({ok:true,status:'BATCH_VALID',rc:0,value});
const clone=x=>structuredClone(x);

export function rejectDuplicateJsonKeys(source){
  let i=0;const ws=()=>{while(/[\x20\t\r\n]/.test(source[i]??''))i++};
  const string=()=>{if(source[i++]!=='"')throw Error('string');const start=i-1;for(;i<source.length;i++){if(source[i]==='\\'){i++;continue}if(source[i]==='"'){i++;return JSON.parse(source.slice(start,i))}}throw Error('unterminated')};
  const value=()=>{ws();if(source[i]==='{'){i++;ws();const keys=new Set();if(source[i]==='}'){i++;return}for(;;){ws();const k=string();if(keys.has(k))throw Error(`duplicate:${k}`);keys.add(k);ws();if(source[i++]!==':')throw Error('colon');value();ws();if(source[i]==='}'){i++;return}if(source[i++]!==',')throw Error('comma')}}if(source[i]==='['){i++;ws();if(source[i]===']'){i++;return}for(;;){value();ws();if(source[i]===']'){i++;return}if(source[i++]!==',')throw Error('array comma')}}if(source[i]==='"'){string();return}const m=source.slice(i).match(/^(?:true|false|null|-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)/);if(!m)throw Error('value');i+=m[0].length};
  value();ws();if(i!==source.length)throw Error('trailing');return true;
}
export function parseRaw(raw){const s=Buffer.isBuffer(raw)?raw.toString('utf8'):String(raw);if(s.charCodeAt(0)===0xfeff||s.includes('\r')||s.includes('\0')||!s.endsWith('\n')||s.endsWith('\n\n'))throw Error('encoding');rejectDuplicateJsonKeys(s);return JSON.parse(s)}
const exactKeys=(obj,keys)=>obj&&typeof obj==='object'&&!Array.isArray(obj)&&Object.keys(obj).length===keys.length&&keys.every(k=>Object.hasOwn(obj,k));
function assessmentAdequate(x){return x&&x.assessment==='ADEQUATE'&&typeof x.reason==='string'&&x.reason.length>0}
export function validateRecord(obj,role,env){
  if(obj.schema_valid!==undefined||obj.go_semantics_valid!==undefined||obj.record_sha256!==undefined)return fail('STOP_CALLER_ASSERTED_VALIDITY',24);
  if(obj.reviewer_role!==role||obj.review_id!==`N8N-V2-${role}-${env.subject_envelope_sha256.slice(0,16)}`)return fail('STOP_ROLE_ID_MISMATCH',25);
  for(const k of ['plan_sha256','content_set_sha256','subject_envelope_sha256','manifest_sha256','validation_index_sha256'])if(obj[k]!==env[k])return fail(k==='manifest_sha256'?'STOP_MANIFEST_MISMATCH':'STOP_SUBJECT_MISMATCH',22,k);
  if(obj.plan_bytes!==env.plan_bytes)return fail('STOP_SUBJECT_MISMATCH',22,'plan_bytes');
  if(!exactKeys(obj.disposition_assessments,env.finding_ids)||!exactKeys(obj.cluster_assessments,env.cluster_ids)||!exactKeys(obj.xd_assessments,env.xd_ids)||!exactKeys(obj.audit_assessments,env.audit_ids))return fail('STOP_REVIEW_SCHEMA_INVALID',24,'exact-set');
  if(Object.values(obj.disposition_assessments).some(x=>!assessmentAdequate(x))||Object.values(obj.cluster_assessments).some(x=>!assessmentAdequate(x))||Object.values(obj.xd_assessments).some(x=>!assessmentAdequate(x)))return fail('STOP_REVIEW_SCHEMA_INVALID',24,'assessment');
  for(const id of env.audit_ids){const x=obj.audit_assessments[id];if(!x||x.audit_id!==id||x.source_item_sha256!==env.audit_hashes[id]||!['CLOSED','OPEN','BLOCKED'].includes(x.closure)||!['ADEQUATE','INADEQUATE','UNVERIFIABLE'].includes(x.assessment))return fail(x?.source_item_sha256!==env.audit_hashes[id]?'STOP_AUDIT_CLAIM_MISMATCH':'STOP_REVIEW_SCHEMA_INVALID',24,id)}
  if(!Array.isArray(obj.new_findings)||!Number.isInteger(obj.unresolved_design_conflicts)||!['GO','CHANGES_REQUIRED','STOP','BLOCKED'].includes(obj.verdict))return fail('STOP_REVIEW_SCHEMA_INVALID',24);
  const semanticGo=Object.values(obj.disposition_assessments).every(assessmentAdequate)&&Object.values(obj.cluster_assessments).every(assessmentAdequate)&&Object.values(obj.xd_assessments).every(assessmentAdequate)&&env.audit_ids.every(id=>obj.audit_assessments[id].closure==='CLOSED'&&obj.audit_assessments[id].assessment==='ADEQUATE'&&obj.audit_assessments[id].source_item_sha256===env.audit_hashes[id])&&obj.new_findings.length===0&&obj.unresolved_design_conflicts===0;
  if(obj.verdict==='GO'&&!semanticGo)return fail('STOP_CONTRADICTORY_GO',27);
  return pass({semantic_go:semanticGo,verdict:obj.verdict,new_findings:obj.new_findings});
}
export function validateBatch(rows,env,suppliedSummary=null){
  if(rows.length!==10||new Set(rows.map(r=>r.slot)).size!==10||roles.some(r=>!rows.find(x=>x.slot===r)))return fail('STOP_INVALID_REVIEW_SET',24);
  const hashes=rows.map(r=>sha(r.raw));if(new Set(hashes).size!==10)return fail('STOP_DUPLICATE_REVIEW_HASH',25);
  const ids=new Set(),valid=[];
  for(const role of roles){const row=rows.find(x=>x.slot===role);let obj;try{obj=parseRaw(row.raw)}catch(e){return fail(String(e).includes('duplicate')?'STOP_DUPLICATE_JSON_KEY':'STOP_REVIEW_SCHEMA_INVALID',24,String(e))}if(ids.has(obj.review_id))return fail('STOP_DUPLICATE_REVIEW_ID',25);ids.add(obj.review_id);const r=validateRecord(obj,role,env);if(!r.ok)return r;valid.push({role,obj,semantic_go:r.value.semantic_go,hash:sha(row.raw)})}
  const counts={go_count:valid.filter(x=>x.obj.verdict==='GO').length,stop_count:valid.filter(x=>x.obj.verdict==='STOP').length,blocked_count:valid.filter(x=>x.obj.verdict==='BLOCKED').length,changes_required_count:valid.filter(x=>x.obj.verdict==='CHANGES_REQUIRED').length,contradictory_go_count:valid.filter(x=>x.obj.verdict==='GO'&&!x.semantic_go).length};
  const allFindings=valid.flatMap(x=>x.obj.new_findings),p0=allFindings.filter(x=>x.severity==='P0').length,p1=new Map();for(const f of allFindings.filter(x=>x.severity==='P1')){const s=p1.get(f.canonical_new_finding_sha256)??new Set();s.add(f.reviewer_role);p1.set(f.canonical_new_finding_sha256,s)}const consensusP1=[...p1.values()].filter(s=>s.size>=2).length;
  Object.assign(counts,{validated_p0_count:p0,consensus_p1_count:consensusP1,valid_review_count:10});
  const verdict=counts.stop_count||counts.blocked_count||p0||consensusP1||counts.contradictory_go_count?'STOP':counts.go_count>=8?'GO':'CHANGES_REQUIRED';
  if(suppliedSummary){for(const [k,v] of Object.entries({...counts,verdict}))if(suppliedSummary[k]!==v)return fail('STOP_COUNTER_OR_VERDICT_CONTRADICTION',27,k)}
  if(verdict==='STOP')return fail(counts.blocked_count?'STOP_QUORUM_BLOCKED_PRESENT':counts.stop_count?'STOP_QUORUM_STOP_PRESENT':'STOP_QUORUM_POLICY',27,JSON.stringify(counts));
  if(verdict==='CHANGES_REQUIRED')return fail('QUORUM_CHANGES_REQUIRED',26,JSON.stringify(counts));
  return pass({counts,verdict,record_hashes:Object.fromEntries(valid.map(x=>[x.role,x.hash]))});
}
function sampleEnv(){
  const root=path.dirname(fileURLToPath(import.meta.url)),work=path.dirname(root),baseline=JSON.parse(fs.readFileSync(path.join(work,'00_FINDINGS_BASELINE.json'))),closure=JSON.parse(fs.readFileSync(path.join(root,'08_CONSENSUS_CLOSURE_V2.json'))),audit=JSON.parse(fs.readFileSync(path.join(root,'24_PROSPECTIVE_AUDIT_R2_BASELINE.json')));
  return{plan_bytes:1,plan_sha256:'1'.repeat(64),content_set_sha256:'2'.repeat(64),subject_envelope_sha256:'3'.repeat(64),manifest_sha256:'4'.repeat(64),validation_index_sha256:'5'.repeat(64),finding_ids:baseline.findings.map(x=>x.finding_id).sort(),cluster_ids:closure.clusters.map(x=>x.cluster_id).sort(),xd_ids:closure.cross_domain_decisions.decisions.map(x=>x.integration_decision_id).sort(),audit_ids:audit.required_ids,audit_hashes:Object.fromEntries(audit.required_ids.map(id=>[id,audit.items[id].source_item_sha256]))}
}
function sampleRecord(role,env){const assess=ids=>Object.fromEntries(ids.map(id=>[id,{assessment:'ADEQUATE',reason:`independent exact assessment ${id}`}])) ;return{review_id:`N8N-V2-${role}-${env.subject_envelope_sha256.slice(0,16)}`,reviewer_role:role,model:'independent-reviewer',reasoning_level:'xhigh',plan_bytes:env.plan_bytes,plan_sha256:env.plan_sha256,content_set_sha256:env.content_set_sha256,subject_envelope_sha256:env.subject_envelope_sha256,manifest_sha256:env.manifest_sha256,validation_index_sha256:env.validation_index_sha256,verdict:'GO',disposition_assessments:assess(env.finding_ids),cluster_assessments:assess(env.cluster_ids),xd_assessments:assess(env.xd_ids),audit_assessments:Object.fromEntries(env.audit_ids.map(id=>[id,{audit_id:id,source_item_sha256:env.audit_hashes[id],closure:'CLOSED',assessment:'ADEQUATE',plan_section_ids:['R2-C01'],acceptance_test_ids:['AT-XD-01'],negative_canary_ids:['NC-XD-01'],evidence_ids:['EV-XD-01'],rationale:`closed ${id}`}])) ,new_findings:[],unresolved_design_conflicts:0,independence_attestation:'reviewed without outputs of other reviewers',runtime_nonexecution_attestation:'no runtime execution'} }
const raw=o=>Buffer.from(JSON.stringify(o,null,2)+'\n');
function selfTest(){
  const env=sampleEnv(),base=roles.map(slot=>({slot,raw:raw(sampleRecord(slot,env))})),tests=[];
  const run=(id,mut,expected)=>{const rows=base.map(x=>({slot:x.slot,raw:Buffer.from(x.raw)})),summary=null,extra=mut(rows,env),r=validateBatch(rows,env,extra??summary);tests.push({canary_id:id,expected_status:expected,actual_status:r.status,rc:r.rc,result:!r.ok&&r.status===expected?'REJECTED':'FALSE_ACCEPT'});if(r.ok||r.status!==expected)throw Error(id)};
  run('FG-001',r=>{for(const x of r.slice(8)){const o=parseRaw(x.raw);o.verdict='BLOCKED';x.raw=raw(o)}},'STOP_QUORUM_BLOCKED_PRESENT');
  run('FG-002',r=>{const a=parseRaw(r[0].raw),b=parseRaw(r[1].raw);b.review_id=a.review_id;r[1].raw=raw(b)},'STOP_DUPLICATE_REVIEW_ID');
  run('FG-003',r=>{r[1].raw=Buffer.from(r[0].raw)},'STOP_DUPLICATE_REVIEW_HASH');
  run('FG-004',r=>{const o=parseRaw(r[1].raw);o.reviewer_role='R1';r[1].raw=raw(o)},'STOP_ROLE_ID_MISMATCH');
  run('FG-005',r=>{const o=parseRaw(r[0].raw);o.subject_envelope_sha256='9'.repeat(64);r[0].raw=raw(o)},'STOP_SUBJECT_MISMATCH');
  run('FG-006',r=>{const o=parseRaw(r[0].raw);o.manifest_sha256='9'.repeat(64);r[0].raw=raw(o)},'STOP_MANIFEST_MISMATCH');
  run('FG-007',(r,e)=>({go_count:9,stop_count:0,blocked_count:0,changes_required_count:0,contradictory_go_count:0,validated_p0_count:0,consensus_p1_count:0,valid_review_count:10,verdict:'GO'}),'STOP_COUNTER_OR_VERDICT_CONTRADICTION');
  run('FG-008',(r,e)=>({go_count:10,stop_count:0,blocked_count:0,changes_required_count:0,contradictory_go_count:0,validated_p0_count:0,consensus_p1_count:0,valid_review_count:10,verdict:'STOP'}),'STOP_COUNTER_OR_VERDICT_CONTRADICTION');
  run('FG-009',r=>{const o=parseRaw(r[0].raw);o.audit_assessments[Object.keys(o.audit_assessments)[0]].closure='OPEN';r[0].raw=raw(o)},'STOP_CONTRADICTORY_GO');
  run('FG-010',r=>{const o=parseRaw(r[0].raw);o.audit_assessments[Object.keys(o.audit_assessments)[0]].assessment='INADEQUATE';r[0].raw=raw(o)},'STOP_CONTRADICTORY_GO');
  run('FG-011',r=>{const o=parseRaw(r[0].raw);delete o.audit_assessments[Object.keys(o.audit_assessments)[0]];r[0].raw=raw(o)},'STOP_REVIEW_SCHEMA_INVALID');
  run('FG-012',r=>{const o=parseRaw(r[0].raw);o.audit_assessments.EXTRA={};r[0].raw=raw(o)},'STOP_REVIEW_SCHEMA_INVALID');
  run('FG-013',r=>{const o=parseRaw(r[0].raw);o.audit_assessments[Object.keys(o.audit_assessments)[0]].source_item_sha256='0'.repeat(64);r[0].raw=raw(o)},'STOP_AUDIT_CLAIM_MISMATCH');
  run('FG-014',r=>{const o=parseRaw(r[0].raw);delete o.disposition_assessments[Object.keys(o.disposition_assessments)[0]];r[0].raw=raw(o)},'STOP_REVIEW_SCHEMA_INVALID');
  run('FG-015',r=>{const o=parseRaw(r[0].raw);delete o.cluster_assessments[Object.keys(o.cluster_assessments)[0]];r[0].raw=raw(o)},'STOP_REVIEW_SCHEMA_INVALID');
  run('FG-016',r=>{const o=parseRaw(r[0].raw);delete o.xd_assessments[Object.keys(o.xd_assessments)[0]];r[0].raw=raw(o)},'STOP_REVIEW_SCHEMA_INVALID');
  const dup='{"review_id":"a","review_id":"b"}\n';let ds='';try{parseRaw(Buffer.from(dup))}catch(e){ds=String(e).includes('duplicate')?'STOP_DUPLICATE_JSON_KEY':'WRONG'}tests.push({canary_id:'FG-017',expected_status:'STOP_DUPLICATE_JSON_KEY',actual_status:ds,rc:24,result:ds==='STOP_DUPLICATE_JSON_KEY'?'REJECTED':'FALSE_ACCEPT'});if(ds!=='STOP_DUPLICATE_JSON_KEY')throw Error('FG-017');
  run('FG-018',r=>{const o=parseRaw(r[0].raw);o.schema_valid=true;r[0].raw=raw(o)},'STOP_CALLER_ASSERTED_VALIDITY');
  run('FG-019',r=>{const o=parseRaw(r[0].raw);o.verdict='STOP';r[0].raw=raw(o)},'STOP_QUORUM_STOP_PRESENT');
  run('FG-020',r=>{r.pop()},'STOP_INVALID_REVIEW_SET');
  const positive=validateBatch(base,env);if(!positive.ok||positive.value.verdict!=='GO')throw Error('positive');return{validator:'RAW-BATCH-NODE-A',result:'PASS',rc:0,positive_verdict:positive.value.verdict,canaries:tests};
}
if(import.meta.url===`file:///${process.argv[1].replace(/\\/g,'/')}`||process.argv[1]?.endsWith('25_RAW_REVIEW_BATCH_VALIDATOR_NODE.mjs')){try{console.log(JSON.stringify(selfTest()))}catch(e){console.error(e);process.exit(29)}}
