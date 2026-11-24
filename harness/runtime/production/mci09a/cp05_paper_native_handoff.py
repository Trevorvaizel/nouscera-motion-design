from pathlib import Path
import os,json,uuid,requests,hashlib,zipfile
root=Path.home()/"Documents/Krita MCP/NOUSCERA_Film001/MCI09A_Paper_v03"
config=json.loads((Path(os.environ["LOCALAPPDATA"])/"krita-codex-mcp/config.json").read_text())
def call(op,arguments):
 r=requests.post(f'http://127.0.0.1:{config["port"]}/v1/execute',headers={"Authorization":"Bearer "+config["token"]},json={"protocol_version":"1","request_id":str(uuid.uuid4()),"operation":op,"arguments":arguments},timeout=180)
 r.raise_for_status();x=r.json()
 if x.get("error"):raise RuntimeError(str(x["error"])[:500])
 return x["result"]
ora=root/"CP05_MCI09A_paper_v03.ora";kra=root/"CP05_MCI09A_paper_v03.kra"
assert ora.exists() and not kra.exists()
res=call("document",{"action":"open","path":str(ora)})
doc=res["affected_document_id"]
state=call("state",{"document_id":doc})
print("Native Krita document",state["document"],flush=True)
print("Layer fields",list(state["layers"][0]),flush=True)
for node in state["layers"]:
 print(node.get("name"),node.get("visible"),flush=True)
 if node["name"].startswith("05 Original"):
  call("layers",{"action":"set_properties","document_id":doc,"layer_id":node.get("id",node.get("layer_id")),"locked":True})
 if node["name"].startswith("02 Paper"):
  call("layers",{"action":"activate","document_id":doc,"layer_id":node.get("id",node.get("layer_id"))})
saved=call("save_export",{"document_id":doc,"kra_path":str(kra),"png_path":str(root/"CP05_MCI09A_native_projection.png")})
state=call("state",{"document_id":doc})
with zipfile.ZipFile(kra) as z:assert z.testzip() is None
out={"native_krita_save":True,"document_id":doc,"document":state["document"],"layers":state["layers"],"kra_sha256":hashlib.sha256(kra.read_bytes()).hexdigest(),"outputs":saved["outputs"],"creative_approval":False}
(root/"native_krita_receipt.json").write_text(json.dumps(out,indent=2))
print("Saved native KRA",kra.name,"SHA256",out["kra_sha256"],flush=True)
