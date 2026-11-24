"""One local entry surface over the existing bridge and real n8n workflow."""
import sys,json,time,os,re,secrets,threading,subprocess,shutil,urllib.request,urllib.parse,zipfile,xml.etree.ElementTree as ET,mimetypes,hashlib
from pathlib import Path
from http.server import ThreadingHTTPServer
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
import bridge as b
ROOT=b.BUILD/"wh002c";RUNS=ROOT/"runs";RUNS.mkdir(parents=True,exist_ok=True)
STAGES=["source","krita","layers","board","gate","receipt"]
META={
"source":["Verify protected source","Python / SHA256","Preserve original artwork and master; confirm current manifest identity."],
"krita":["Inspect native Krita master","Krita archive reader","Read actual layered document structure, without editing the master."],
"layers":["Inspect semantic entities","Scene contract","Check fixed notebook, rigid pen, independent limb, head and ink dependencies."],
"board":["Build review evidence","Pillow diagnostic","Show existing hidden surface and writing layers at the same crop; no reconstruction."],
"gate":["Evaluate readiness","Existing scene_gate.py","Refuse progression if hidden surfaces lack bound visual review."],
"receipt":["Persist decision and handoff","Harness","Record actual findings, artifacts and next permitted preparation." ]}
N8N="http://127.0.0.1:5678/webhook/nouscera-preparation-audit-v1"
ID=re.compile(r"^[a-f0-9]{16}$")
LOCK=threading.RLock()
def read(p):return b.read(p)
def write(p,x):b.write(p,x)
def stamp():return time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())
def folder(t):
 if not isinstance(t,str) or not ID.fullmatch(t):raise ValueError("bad run id")
 p=RUNS/t
 if not p.is_dir():raise ValueError("unknown run")
 return p
def events(p):
 f=p/"events.jsonl"
 return [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l] if f.exists() else []
def log(p,stage,status,detail=None):
 with (p/"events.jsonl").open("a",encoding="utf-8") as f:
  f.write(json.dumps({"time":stamp(),"stage":stage,"status":status,"detail":detail or {}})+"\n");f.flush();os.fsync(f.fileno())
def sha(p):return b.runner.sha(p)
def init(origin):
 with LOCK:
  if any(read(p/"state.json")["status"] in ("queued","running") for p in RUNS.iterdir() if (p/"state.json").is_file()):raise ValueError("Another preparation audit is active; inspect it first.")
  t=secrets.token_hex(8);p=RUNS/t;p.mkdir()
  state={"run_id":t,"origin":origin,"objective":"Inspect existing CP05 preparation and expose the actual judgment gate","status":"queued","completed":[],"creative_approval":False,"created":stamp(),"workflow_sha256":sha(HERE/"preparation.n8n.json")}
  write(p/"state.json",state);log(p,"coordinator","delegated",{"actor":origin,"why":"Recover the actual readiness state before deciding the repair route. No new animation."})
  return t
def deliver(t):
 p=folder(t)
 try:
  q=urllib.request.Request(N8N,data=json.dumps({"run_id":t}).encode(),headers={"Content-Type":"application/json","X-Bridge-Key":b.TOKEN})
  with urllib.request.urlopen(q,timeout=180) as r:x=json.load(r)
  write(p/"n8n-response.json",x)
  if read(p/"state.json")["status"]!="complete":raise ValueError("native workflow returned without final receipt")
  log(p,"coordinator","received",{"actor":read(p/"state.json")["origin"],"status":"actual native workflow receipt available"})
 except Exception as e:
  with LOCK:
   s=read(p/"state.json")
   if s["status"]!="complete":s.update(status="failed",error=str(e)[:300]);write(p/"state.json",s)
   log(p,"coordinator","failed",{"error":str(e)[:300]})
def start(origin):
 t=init(origin);threading.Thread(target=deliver,args=(t,),daemon=True).start();return {"run_id":t,"status":"queued","creative_approval":False}
def stage(t,name):
 p=folder(t)
 with LOCK:
  s=read(p/"state.json")
  if s["workflow_sha256"]!=sha(HERE/"preparation.n8n.json"):raise ValueError("workflow changed; new run required")
  if name not in STAGES:raise ValueError("unknown stage")
  if name in s["completed"]:return {"run_id":t,"stage":name,"result":read(p/(name+".json"))}
  if s["status"] not in ("queued","running") or s.get("active") or name!=STAGES[len(s["completed"])]:raise ValueError("out of order or failed run")
  s.update(status="running",active=name);write(p/"state.json",s);log(p,name,"running")
 try:
  reg=read(b.REG);root=b.BUILD/"asset-gates/CP05-v01";m=read(root/"scene_manifest.json")
  if name=="source":
   data={}
   for k in ["cp05_source","kra_master","prepared_blender_master"]:
    v=reg["items"][k];actual=sha(v["path"])
    if actual!=v["sha256"]:raise ValueError("protected asset changed: "+k)
    data[k]={"sha256":actual,"bytes":Path(v["path"]).stat().st_size}
   if sha(root/m["source"]["file"])!=m["source"]["sha256"] or m["source"]["sha256"]!=data["cp05_source"]["sha256"]:raise ValueError("prepared source mismatch")
   data["manifest_sha256"]=sha(root/"scene_manifest.json")
   data["artifacts"]=["cp05_source","kra_master","gate_manifest"]
  elif name=="krita":
   f=Path(reg["items"]["kra_master"]["path"])
   if sha(f)!=reg["items"]["kra_master"]["sha256"]:raise ValueError("Krita master changed")
   with zipfile.ZipFile(f) as z:
    tree=ET.fromstring(z.read("maindoc.xml"))
    layers=[{"name":e.attrib.get("name",""),"type":e.attrib.get("nodetype",""),"visible":e.attrib.get("visible","")} for e in tree.iter() if e.tag.split("}")[-1]=="layer"]
    data={"archive_integrity":"pass" if z.testzip() is None else "fail","layers":layers,"scope":"read-only archive structure; not a live Krita edit","artifacts":["kra_master"]}
    if data["archive_integrity"]!="pass":raise ValueError("damaged archive")
  elif name=="layers":
   if sha(root/"scene_manifest.json")!=read(p/"source.json")["manifest_sha256"]:raise ValueError("manifest changed mid-run")
   data={"entities":[],"artifacts":["plate","paper","limb","pen","head","gate_manifest"]}
   for k,v in m["entities"].items():
    item={"role":k,"behavior":v["behavior"],"motion":v["motion"],"depends_on":v.get("depends_on",[])}
    if v.get("asset"):
     a=v["asset"];f=root/a["file"]
     if sha(f)!=a["sha256"]:raise ValueError("layer changed: "+k)
     item.update(sha256=a["sha256"],dimensions=b.scene_gate.dimensions(f))
    data["entities"].append(item)
  elif name=="board":
   board=p/"review-board.png"
   cp=subprocess.run([reg["python"],str(HERE/"review_board.py"),str(root),str(board)],capture_output=True,timeout=45)
   if cp.returncode or not board.is_file():raise ValueError("diagnostic board failed: "+cp.stderr.decode(errors="replace")[-250:])
   data={"sha256":sha(board),"scope":"new diagnostic board from existing layers, not new artwork","artifacts":["board-"+t,"paper","limb"]}
  elif name=="gate":
   if sha(root/"scene_manifest.json")!=read(p/"source.json")["manifest_sha256"]:raise ValueError("manifest changed mid-run")
   data=b.scene_gate.inspect(m,root);data["artifacts"]=["board-"+t,"gate_manifest"]
   if data["status"]=="invalid":raise ValueError("invalid scene manifest: "+str(data["errors"]))
  else:
   g=read(p/"gate.json")
   for k,v in read(p/"source.json").items():
    if k in reg["items"] and sha(reg["items"][k]["path"])!=v["sha256"]:raise ValueError("source changed during run")
   data={"status":"complete","readiness":g["status"],"blockers":g["blockers"],"creative_approval":False,"next":"Prepare complete hidden surfaces in Krita, selectively ComfyUI, then bind actual visual review before animation.","evidence":{k:sha(p/(k+".json")) for k in STAGES[:-1]},"artifacts":["board-"+t,"runreceipt-"+t,"paper","kra_master"]}
  with LOCK:
   write(p/(name+".json"),data);s["completed"].append(name);s.update(active=None,status="complete" if name=="receipt" else "running");write(p/"state.json",s);log(p,name,"blocked" if name=="gate" and data["status"]=="blocked" else "complete",{"artifacts":data.get("artifacts",[])})
  return {"run_id":t,"stage":name,"result":data}
 except Exception as e:
  with LOCK:s.update(status="failed",error=str(e)[:300]);write(p/"state.json",s);log(p,name,"failed",{"error":str(e)[:300]})
  raise
def artifacts():
 a=b.artifacts();root=b.BUILD/"asset-gates/CP05-v01"
 def add(k,label,path,kind):
  path=Path(path)
  if path.is_file():a[k]={"label":label,"path":path,"kind":kind}
 for k,label,name,kind in [("pen","Rigid pen layer","rigid_pen.png","image"),("head","Head layer","head.png","image"),("gate_manifest","Scene asset manifest","scene_manifest.json","json"),("gate_report","Previous readiness result","gate.json","json")]:add(k,label,root/name,kind)
 for k,label,name,kind in [("atlas","Semantic decomposition atlas","CP05_prepared_scene_atlas_v02.png","image"),("author_review","Recorded author review","MCI07_author_review_2026-11-24.md","text"),("vae_metrics","VAE reconstruction evidence","MCI01_VAE_reconstruction_metrics.json","json"),("steps_metrics","22 vs 50 step evidence","MCI03_22_vs_50_metrics_v01.json","json")]:add(k,label,b.HOME/"reviews"/name,kind)
 for p in RUNS.iterdir():
  if p.is_dir() and ID.fullmatch(p.name):
   add("board-"+p.name,"Current hidden-surface inspection board",p/"review-board.png","image")
   add("runreceipt-"+p.name,"Preparation audit receipt",p/"receipt.json","json")
 return a
def agent_summary():
 out=[]
 for p in sorted((b.WORK/"requests").glob("*"),key=lambda p:p.stat().st_mtime,reverse=True)[:30]:
  if not ID.fullmatch(p.name) or not (p/"request.json").is_file():continue
  try:
   req=read(p/"request.json");plan=read(p/"plan.json") if (p/"plan.json").is_file() else {};receipt=read(p/"receipt.json") if (p/"receipt.json").is_file() else {}
   out.append({"id":p.name,"objective":req["objective"],"route":plan.get("route"),"reason":plan.get("reason"),"status":receipt.get("status","executing" if plan else "model pending"),"model_status":plan.get("model_status"),"artifacts":receipt.get("artifacts",[])})
  except (ValueError,OSError,KeyError):continue
 return out
def agent_detail(t):
 if not ID.fullmatch(t):raise ValueError("unknown agent request")
 p=b.WORK/"requests"/t
 if not (p/"request.json").is_file():raise ValueError("unknown agent request")
 out={k:read(p/(k+".json")) for k in ["request","model","plan","receipt"] if (p/(k+".json")).is_file()}
 replay=b.BUILD/"runs"/("wb-"+t)/"state.json"
 if replay.is_file():out["actual_runner_state"]=read(replay)
 return out
def native_open(t,k,actor):
 p=folder(t);a=artifacts().get(k)
 if not a or k not in ("kra_master","prepared_blender_master") or a["kind"]!="native":raise ValueError("not an allowed native artifact")
 with LOCK:log(p,"native","running",{"actor":actor,"why":"Inspect registered native master without modifying original.","artifacts":[k]})
 try:
  reg=read(b.REG);source=a["path"]
  if sha(source)!=reg["items"][k]["sha256"]:raise ValueError("protected master changed")
  dest=b.WORK/"inspection-copies"/(str(time.time_ns())+"-"+source.name);dest.parent.mkdir(exist_ok=True);shutil.copy2(source,dest)
  if sha(dest)!=sha(source):raise ValueError("copy mismatch")
  app=Path(reg["blender"]) if k=="prepared_blender_master" else Path(os.environ.get("ProgramFiles",r"C:\Program Files"))/"Krita (x64)/bin/krita.exe"
  if not app.is_file():raise ValueError("native app unavailable")
  proc=subprocess.Popen([str(app),str(dest)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  result={"status":"launch requested","application":app.name,"pid":proc.pid,"inspection_copy":dest.name,"source_sha256":sha(source),"artifacts":[k],"actor":actor,"scope":"process spawned; GUI file load not independently confirmed"}
  with LOCK:log(p,"native","launch requested",result)
  return result
 except Exception as e:
  with LOCK:log(p,"native","failed",{"error":str(e)[:300]})
  raise
def overview():
 with LOCK:
  runs=[]
  for p in sorted(RUNS.iterdir(),key=lambda p:p.stat().st_mtime,reverse=True):
   if (p/"state.json").is_file():
    s=read(p/"state.json");s["events"]=events(p);s["results"]={k:read(p/(k+".json")) for k in STAGES if (p/(k+".json")).is_file()};runs.append(s)
  a=artifacts()
  return {"history":read(HERE/"history.json"),"stages":META,"runs":runs,"agent_requests":agent_summary(),"artifacts":{k:{"label":v["label"],"kind":v["kind"],"bytes":v["path"].stat().st_size,"filename":v["path"].name} for k,v in a.items()},"creative_approval":False,"scope":"Preparation audit, not hidden-surface reconstruction"}
class Handler(b.H):
 def do_GET(self):
  if not self.host():return self.js({"error":"local only"},403)
  u=urllib.parse.urlparse(self.path);q=urllib.parse.parse_qs(u.query);k=q.get("id",[""])[0]
  try:
   if u.path in ("/","/surface","/compare","/artifact"):
    return self.send((HERE/"index.html").read_text(encoding="utf-8").replace("__TOKEN__",b.BROWSER_TOKEN).encode(),"text/html; charset=utf-8")
   if u.path=="/api/surface":return self.js(overview())
   if u.path=="/api/agent":return self.js(agent_detail(k))
   if u.path=="/media":
    v=artifacts().get(k)
    if not v or v["kind"]=="native":return self.js({"error":"not previewable"},404)
    if v["path"].stat().st_size>50*1024*1024:return self.js({"error":"preview too large"},413)
    return self.send(v["path"].read_bytes(),{"video":"video/mp4","image":"image/png","json":"application/json","text":"text/plain; charset=utf-8"}[v["kind"]])
   return super().do_GET()
  except Exception as e:return self.js({"error":str(e)[:300]},400)
 def do_POST(self):
  if self.path not in ("/api/start","/api/stage","/api/note","/api/ask","/api/native"):return super().do_POST()
  if not self.host():return self.js({"error":"local only"},403)
  key=secrets.compare_digest(self.headers.get("X-Bridge-Key",""),b.TOKEN)
  browser=self.headers.get("Origin")==b.BASE and secrets.compare_digest(self.headers.get("X-Local-Token",""),b.BROWSER_TOKEN)
  if not key and not browser:return self.js({"error":"unauthorized"},403)
  try:
   n=int(self.headers.get("Content-Length","0"))
   if not 0<n<4096:raise ValueError("bad request size")
   x=json.loads(self.rfile.read(n))
   if self.path=="/api/stage":
    if not key:return self.js({"error":"workflow credential required"},403)
    return self.js(stage(x["run_id"],x["stage"]))
   if self.path=="/api/start":
    if x!={"operation":"preparation_audit"}:raise ValueError("only preparation audit authorized")
    return self.js(start("ChatGPT via Desktop Commander" if key else "local workbench user"),202)
   if self.path=="/api/native":return self.js(native_open(x["run_id"],x["id"],"ChatGPT via Desktop Commander" if key else "local workbench user"))
   if self.path=="/api/ask":
    if not browser:raise ValueError("local user action required")
    objective=x.get("objective","").strip()
    if not 1<=len(objective)<=2000:raise ValueError("objective required")
    q=urllib.request.Request("http://127.0.0.1:5678/webhook/nouscera-creative-workbench/chat",data=json.dumps({"action":"sendMessage","sessionId":secrets.token_hex(16),"chatInput":objective}).encode(),headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(q,timeout=230) as r:return self.js(json.load(r))
   p=folder(x["run_id"])
   if not browser:raise ValueError("local user action required")
   note=x.get("note","").strip()
   if not 1<=len(note)<=1000:raise ValueError("note required")
   with LOCK:log(p,"judgment","recorded",{"note":note,"scope":"local user note; not creative approval or automatic instruction to ChatGPT"})
   return self.js({"status":"recorded","creative_approval":False})
  except Exception as e:return self.js({"error":str(e)[:300]},400)
if __name__=="__main__":print("NOUSCERA shared workbench "+b.BASE,flush=True);ThreadingHTTPServer(("127.0.0.1",b.PORT),Handler).serve_forever()
