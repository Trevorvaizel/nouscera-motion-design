from pathlib import Path
import json,requests,hashlib,time
p=Path(__file__).parent;b=p.parent;home=b.parent
out=home/"reviews/MCI10_material_v01"
inp=Path.home()/"Downloads/Compressed/ComfyUI_windows_portable_nvidia/ComfyUI_windows_portable/ComfyUI/input/NOUSCERA"
r=json.loads((out/"material_inputs_receipt.json").read_text())
def verify():
 for n,h in r["input_sha256"].items():assert hashlib.sha256((inp/n).read_bytes()).hexdigest()==h
verify()
for _ in range(100):
 try:
  raw=(p/"material-n8n-server.log").read_bytes();log=raw.decode("utf-16" if raw.startswith(b"\xff\xfe") else "utf-8",errors="replace")
  if "NousceraMaterialMAT01" in log and "Editor is now accessible" in log and requests.get("http://127.0.0.1:5678/healthz",timeout=3).ok:break
 except Exception:pass
 time.sleep(2)
else:raise RuntimeError("Native workflow not ready")
url="http://127.0.0.1:5678/webhook/nouscera-mci10-garment-v1"
headers={"X-Bridge-Key":(b/"wh002b/bridge.key").read_text().strip()}
f=out/"native_submission.json"
if f.exists():q=json.loads(f.read_text())
else:
 res=requests.post(url,headers=headers,json={"objective":"reconstruct_hidden_garment","scene":"CP05","method":"MCI10-garment-MAT-v01"},timeout=60)
 res.raise_for_status();q=res.json();assert q["state"]=="queued_not_validated";f.write_text(json.dumps(q,indent=2))
print("Submitted",q,flush=True)
pid=q["prompt_id"];base="http://127.0.0.1:8188"
for _ in range(120):
 h=requests.get(base+"/history/"+pid,timeout=10).json().get(pid)
 if h and h.get("status",{}).get("status_str")=="error":raise RuntimeError(str(h["status"])[:1800])
 if h and h.get("status",{}).get("completed"):break
 time.sleep(2)
else:raise RuntimeError("No completed native output")
assert h["status"]["status_str"]=="success"
im=h["outputs"]["5"]["images"][0];res=requests.get(base+"/view",params=im,timeout=20);res.raise_for_status();verify()
(out/"garment_native_crop.png").write_bytes(res.content)
receipt={"submission":q,"native_status":"success","output":im,"output_sha256":hashlib.sha256(res.content).hexdigest(),"input_hashes_verified_before_and_after":True,"input_sha256":r["input_sha256"],"creative_approval":False}
(out/"native_method_receipt.json").write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt),flush=True)
