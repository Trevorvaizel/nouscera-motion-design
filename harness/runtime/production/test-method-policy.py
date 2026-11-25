"""Native n8n decision gate acceptance; no creative writes."""
from pathlib import Path
import json,requests,time,hashlib,sqlite3
r=Path(__file__).resolve().parent; b=r.parents[3]; p=b/"production-integration"
policy=json.loads((r/"method-policy.v1.json").read_text())
source=policy["reference"]["source_sha256"]
base={"scene":"CP05","source_sha256":source}
h={"X-Bridge-Key":(b/"wh002b/bridge.key").read_text().strip()}
url="http://127.0.0.1:5678/webhook/nouscera-method-decision-v1"
for _ in range(90):
 try:
  raw=(p/"method-policy-server.log").read_bytes()
  log=raw.decode("utf-16" if raw.startswith(b"\xff\xfe") else "utf-8",errors="replace")
  if "NousceraMethodDecision01" in log and "Editor is now accessible" in log and requests.get("http://127.0.0.1:5678/healthz",timeout=3).ok:break
 except Exception:pass
 time.sleep(2)
else:raise RuntimeError("Native n8n decision workflow not available")
cases=[]
for m in policy["methods"]:
 body={**base,"objective":m["objective"],"fault":m["fault"]}
 if m["id"]=="transfer_validation":body={**body,"scene":"synthetic-transfer-check","source_sha256":"a"*64}
 res=requests.post(url,json=body,headers=h,timeout=30);res.raise_for_status();x=res.json()
 assert x["method"]==m["id"] and x["disposition"]==m["status"],x
 assert not any(x[k] for k in ["execution_authorized","creative_approval_granted","readiness_promoted"])
 assert x["evidence"]==m["evidence"] and x["required_checks"]==m["requires"]
 if m["id"]=="transfer_validation":assert x["approval_reference"] is None
 cases.append({"case":m["id"],"http":res.status_code,"result":x});print("PASS",m["id"],x["n8n_execution_id"],flush=True)
valid={**base,"objective":"prepare_motion","fault":"wrist_or_cuff_distortion"}
for name,body in [
 ("retired_mat",{**valid,"requested_method":"MCI10-native-MAT-v01"}),
 ("retired_overlay",{**valid,"requested_method":"stationary_sleeve_concealment"}),
 ("wrong_method",{**valid,"requested_method":"independent_light"}),
 ("unknown_problem",{**valid,"fault":"arbitrary"}),
 ("wrong_source",{**valid,"source_sha256":"0"*64}),
 ("unfamiliar_scene",{**valid,"scene":"other"}),
 ("self_approval",{**valid,"creative_approval":True})]:
 res=requests.post(url,json=body,headers=h,timeout=30)
 assert res.status_code>=400,(name,res.status_code)
 cases.append({"case":name,"http":res.status_code,"rejected":True});print("PASS rejection",name,res.status_code,flush=True)
res=requests.post(url,json=valid,timeout=20);assert res.status_code in (401,403)
cases.append({"case":"unauthenticated","http":res.status_code,"rejected":True})
for path in ["nouscera-mci10-native-inpaint-v1","nouscera-mci10-garment-v1"]:
 res=requests.post("http://127.0.0.1:5678/webhook/"+path,json={},headers=h,timeout=20)
 assert res.status_code==404,(path,res.status_code)
 cases.append({"case":"retired_webhook_"+path,"http":res.status_code})
with sqlite3.connect(b/"wh002b/n8n-data/.n8n/database.sqlite") as db:
 workflows=dict(db.execute("SELECT id,active FROM workflow_entity").fetchall())
 assert workflows["NousceraMethodDecision01"]==1
 assert workflows["NousceraNativeMAT01"]==workflows["NousceraMaterialMAT01"]==0
 assert all(workflows[x]==1 for x in ["NousceraWorkbench01","NousceraPrepAudit01","NousceraKitsuAudit01"])
approval=json.loads((r/"mci11/author-approval.json").read_text())
for name,digest in approval["dependency_manifest"].items():assert hashlib.sha256((b.parent/name).read_bytes()).hexdigest()==digest,name
receipt={"policy_version":policy["version"],"policy_sha256":hashlib.sha256((r/"method-policy.v1.json").read_bytes()).hexdigest(),"native_workflow":"NousceraMethodDecision01","cases":cases,"test_count":len(cases),"approved_dependency_count":len(approval["dependency_manifest"]),"historical_workflows_retired":True,"other_native_workflows_active":True,"creative_writes":False,"scope":"Deterministic structured method decision; coordinator still verifies scene evidence and dispatches methods. No autonomous tool selection or execution claim."}
(r/"method-policy-test-receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
print("ALL NATIVE POLICY TESTS PASSED",len(cases),flush=True)
