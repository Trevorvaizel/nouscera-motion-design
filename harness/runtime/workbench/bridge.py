"""Local, allowlisted operations bridge for a visual workflow host. No arbitrary shell or file paths."""
import argparse,hashlib,html,json,os,re,secrets,shutil,subprocess,sys,time,urllib.parse,urllib.request,threading
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
HERE=Path(__file__).resolve().parent; RUNTIME=HERE.parent
sys.path.insert(0,str(RUNTIME));import runner,scene_gate
BUILD=Path(os.environ.get("NOUSCERA_BUILD_ROOT",str(HERE.parents[3]))).resolve()
WORK=BUILD/"wh002b";WORK.mkdir(exist_ok=True)
HOME=BUILD.parent;REG=BUILD/"runtime-registry-v01.json";PORT=8770;BASE=f"http://127.0.0.1:{PORT}"
KEY=WORK/"bridge.key"
if not KEY.exists():KEY.write_text(secrets.token_urlsafe(40),encoding="ascii")
TOKEN=KEY.read_text().strip(); BROWSER_TOKEN=secrets.token_urlsafe(32)
LOCK=threading.Lock()
OPS={"compare_candidates":"Compare actual prior motion candidates and recorded author feedback; no generation.","inspect_readiness":"Re-evaluate current CP05 asset manifest and reveal blocked preparation steps.","technical_replay":"Reproduce existing v02; explicit replay request required; no new creative work.","blocked":"Unsupported, ambiguous or new creative request; do not execute."}
def read(p):return json.loads(Path(p).read_text(encoding="utf-8-sig"))
def write(p,x):runner.atomic(p,x)
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest()
def packet():
 return {"state":runner.bootstrap()["state"],"current":read(RUNTIME/"observable/current.json"),"workflow":runner.contract(),"operations":OPS,"rules":["No new animation or creative approval.","Paper below hand requires intentional reconstruction in Krita and review; ComfyUI only where needed.","Fixed notebook, rigid pen, separate deformable arm, independent ink, protected source.","Use existing operations rather than improvise."]}
def artifacts():
 r=read(REG)["items"];a={}
 def add(k,label,p,kind):
  p=Path(p)
  if p.is_file():a[k]={"label":label,"path":p,"kind":kind}
 for k,label,kind in [("cp05_source","Protected CP05 artwork","image"),("kra_master","Krita master (inspection copy)","native"),("prepared_blender_master","Prepared Blender master (inspection copy)","native"),("baseline_video","Prepared scene v02","video")]:add(k,label,r[k]["path"],kind)
 for k,label,n in [("masked","Masked I2V experiment","B0311L_S09_CP05_STABILIZED_MASKED_720x1280_33f_v01.mp4"),("warp","Source-preserving warp v01","MCI07_CP05_source_warp_prototype_v01.mp4"),("rigid","Rigid pen / head / ink v02","MCI07_CP05_rigid_pen_head_ink_v02.mp4"),("prepared01","Prepared scene v01","CP05_prepared_scene_motion_v01.mp4")]:add(k,label,HOME/"reviews"/n,"video")
 for k,label,n in [("paper","Current approximate clean notebook","stationary_notebook.png"),("limb","Isolated writing limb","writing_limb.png"),("plate","Current approximate clean plate","stationary_clean_plate.png")]:add(k,label,BUILD/"asset-gates/CP05-v01"/n,"image")
 add("comfy_graph","Original Hunyuan API workflow",HOME/"tools/b0311l_s09_480_33f_api_graph.json","json")
 for q in (WORK/"requests").glob("*/receipt.json"):
  try:
   t=q.parent.name;receipt=read(q)
   if not re.fullmatch("[a-f0-9]{16}",t):continue
   add("receipt-"+t,"Operation receipt "+t,q,"json")
   if receipt["route"]=="technical_replay" and receipt["status"]=="complete":
    add("replay-"+t,"Verified replay "+t,BUILD/"runs"/("wb-"+t)/"scratch/reviews/CP05_prepared_scene_motion_v02.mp4","video")
  except (ValueError,OSError,KeyError):continue
 return a
def link(k):return BASE+"/artifact?id="+urllib.parse.quote(k)
def plan(objective):
 if not isinstance(objective,str) or not 1<=len(objective.strip())<=2000:raise ValueError("objective required")
 t=secrets.token_hex(8);p=WORK/"requests"/t;p.mkdir(parents=True)
 ctx=packet()
 # Task-specific context: historical creative restriction is not a ban on inspection.
 task_context={"scene":"CP05","current_question":"Hidden notebook paper requires reconstruction and visual review before animation.","approved_animation":False,"creative_release":"blocked","permitted_now":OPS,"source_rules":ctx["rules"]}
 prompt="""You route requests in NOUSCERA. Inspection and comparison of EXISTING material are explicitly authorized now, even though NEW creative production is blocked. Choose precisely one available workflow. A user may request inspection of readiness without authorizing animation. Do not treat those words as a request to animate.
Examples: 'show previous versions' -> compare_candidates; 'is the paper ready?' -> inspect_readiness; 'replay the existing verified operation' -> technical_replay; 'make a new animation' -> blocked. Technical replay requires explicit replay request. Return JSON route and short reason. Do not grant creative approval.
""" + json.dumps(task_context)+"\nUser objective: "+objective
 schema={"type":"object","properties":{"route":{"type":"string","enum":list(OPS)},"reason":{"type":"string"}},"required":["route","reason"],"additionalProperties":False}
 body={"model":"nouscera-deepseek-r1-8b","messages":[{"role":"user","content":prompt}],"temperature":0.1,"max_tokens":768,"response_format":{"type":"json_schema","json_schema":{"name":"operation","schema":schema}}}
 write(p/"request.json",{"objective":objective,"context":ctx,"prompt":prompt,"model_request":body})
 try:
  key=(BUILD/"wh002/local-inference.key").read_text().strip()
  req=urllib.request.Request("http://127.0.0.1:8766/v1/chat/completions",data=json.dumps(body).encode(),headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"})
  with urllib.request.urlopen(req,timeout=150) as f:res=json.load(f)
  if res.get("model")!="nouscera-deepseek-r1-8b":raise ValueError("model identity mismatch")
  raw=res["choices"][0]["message"]["content"];ans=json.loads(raw)
  if set(ans)!={"route","reason"} or ans["route"] not in OPS or not isinstance(ans["reason"],str):raise ValueError("invalid route")
  route=ans["route"];reason=ans["reason"][:500]
  if route=="technical_replay" and not re.search(r"\breplay\b",objective,re.I):route="blocked";reason="Replay needs an explicit request."
  status="responded"
  write(p/"model.json",{"model":res["model"],"answer":ans,"usage":res.get("usage"),"finish_reason":res["choices"][0].get("finish_reason")})
 except Exception as e:route="blocked";reason="Model invocation failed: "+str(e)[:250];status="invocation_failed"
 x={"request_id":t,"objective":objective,"route":route,"reason":reason,"model_status":status,"context_sha256":digest(ctx),"creative_approval":False};write(p/"plan.json",x);return x
def execute(t,expected):
 if not isinstance(t,str) or not re.fullmatch("[a-f0-9]{16}",t):raise ValueError("unknown request")
 p=WORK/"requests"/t
 with LOCK:
  x=read(p/"plan.json")
  if expected!=x["route"] or digest(packet())!=x["context_sha256"]:raise ValueError("route or context changed")
  if (p/"receipt.json").exists():return read(p/"receipt.json")
  route=x["route"];items=[];details={};summary=""
  if route=="compare_candidates":
   items=["cp05_source","masked","warp","rigid","prepared01","baseline_video","kra_master","prepared_blender_master","comfy_graph"]
   summary="Compare existing candidates. Broad warps moved the pen and notebook incorrectly; the prepared scene improved texture and motion, but hidden paper reconstruction remains inadequate. No animation approved."
  elif route=="inspect_readiness":
   root=BUILD/"asset-gates/CP05-v01";details=scene_gate.inspect(read(root/"scene_manifest.json"),root)
   items=["cp05_source","paper","plate","limb","kra_master","prepared_blender_master"]
   summary="Readiness: "+details["status"]+". "+ "; ".join(details["blockers"])+". Inspect the reconstructed paper before any animation."
  elif route=="technical_replay":
   rid="wb-"+t;dest=BUILD/"runs"/rid
   if dest.exists():raise ValueError("existing interrupted run; reconcile rather than duplicate")
   with (p/"runner.log").open("w") as f:cp=subprocess.run([sys.executable,str(RUNTIME/"runner.py"),"run","--registry",str(REG),"--runs",str(BUILD/"runs"),"--id",rid],stdout=f,stderr=subprocess.STDOUT,timeout=180)
   if cp.returncode:raise RuntimeError("registered replay failed; see receipt directory")
   details=read(dest/"verification.json");summary="Technical replay completed. "+str(details["frame_count"])+" frames; verification "+details["status"]+". No new creative work."
   items=["baseline_video","prepared_blender_master"]
  else:summary="Stopped: "+x["reason"]+". No creative work was executed."
  a=artifacts();links=[{"label":a[k]["label"],"url":link(k)} for k in items if k in a]
  output="**"+route.replace("_"," ").capitalize()+"**\n\n"+summary+"\n\n**Why this route:** "+x["reason"]+"\n\n"+"\n".join("["+v["label"]+"]("+v["url"]+")" for v in links)+"\n\n[Compare existing motion versions]("+BASE+"/compare)\n\n[Technical evidence](http://127.0.0.1:8765/)"
  if route=="technical_replay":
   links.append({"label":"Actual verified replay output","url":link("replay-"+t)})
   output+="\n\n[Actual verified replay output]("+link("replay-"+t)+")"
  output+="\n\n[Operation evidence]("+link("receipt-"+t)+")"
  r={**x,"status":"blocked" if route=="blocked" else "complete","details":details,"artifacts":links,"output":output};write(p/"receipt.json",r);return r
def page(title,body):
 return ("<!doctype html><meta charset=utf-8><title>"+html.escape(title)+"</title><style>body{background:#151515;color:#eee;font:16px system-ui;margin:30px;max-width:1500px}a{color:#c8dfca}video,img{max-width:100%;max-height:70vh;display:block;margin:12px auto}button{padding:12px;font:inherit;cursor:pointer}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}article{border:1px solid #444;padding:12px}p{max-width:800px}</style><h1>"+html.escape(title)+"</h1>"+body).encode()
class H(BaseHTTPRequestHandler):
 def send(self,b,typ="application/json",code=200):
  self.send_response(code);self.send_header("Content-Type",typ);self.send_header("Content-Length",str(len(b)));self.send_header("Cache-Control","no-store");self.send_header("X-Content-Type-Options","nosniff");self.send_header("Content-Security-Policy","default-src 'self'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; frame-ancestors 'none'");self.end_headers();self.wfile.write(b)
 def js(self,x,c=200):self.send(json.dumps(x).encode(),code=c)
 def host(self):return self.headers.get("Host") in [f"127.0.0.1:{PORT}",f"localhost:{PORT}"]
 def do_GET(self):
  if not self.host():return self.js({"error":"local only"},403)
  u=urllib.parse.urlparse(self.path);k=urllib.parse.parse_qs(u.query).get("id",[""])[0];a=artifacts()
  if u.path=="/compare":
   cards="".join("<article><b>"+html.escape(a[k]["label"])+"</b><video controls preload=metadata src='/media?id="+k+"'></video></article>" for k in ["masked","warp","rigid","prepared01","baseline_video"] if k in a)
   return self.send(page("CP05 | Compare actual attempts","<p>Author feedback: texture and movement improved; notebook reconstruction remains unresolved. None approved.</p><section>"+cards+"</section>"),"text/html")
  if k not in a:return self.js({"error":"unknown artifact"},404)
  v=a[k];kind=v["kind"]
  if u.path=="/media" and kind in ("image","video","json"):
   if v["path"].stat().st_size>50*1024*1024:return self.js({"error":"preview too large"},413)
   return self.send(v["path"].read_bytes(),{"image":"image/png","video":"video/mp4","json":"application/json"}[kind])
  if u.path!="/artifact":return self.js({"error":"not found"},404)
  if kind=="native":
   body="<p>Opens a versioned inspection copy in the registered native application; original stays untouched.</p><button id='open'>Open native file</button><p id='result'></p><script>document.getElementById('open').onclick=async()=>{let r=await fetch('/open',{method:'POST',headers:{'Content-Type':'application/json','X-Local-Token':'"+BROWSER_TOKEN+"'},body:JSON.stringify({id:'"+k+"'})});document.getElementById('result').textContent=JSON.stringify(await r.json())}</script>"
  elif kind=="video":body="<video controls autoplay muted src='/media?id="+k+"'></video>"
  elif kind=="image":body="<img src='/media?id="+k+"'>"
  else:body="<a href='/media?id="+k+"'>Inspect workflow JSON</a><p><a href='http://127.0.0.1:8188/'>Open ComfyUI canvas</a> (workflow import is not automated).</p>"
  return self.send(page(v["label"],body),"text/html")
 def do_POST(self):
  if not self.host():return self.js({"error":"local only"},403)
  try:
   n=int(self.headers.get("Content-Length","0"));assert 0<n<16384
   x=json.loads(self.rfile.read(n))
   if self.path=="/open":
    if self.headers.get("Origin")!=BASE or not secrets.compare_digest(self.headers.get("X-Local-Token",""),BROWSER_TOKEN):return self.js({"error":"local authorization required"},403)
    a=artifacts().get(x.get("id"))
    if not a or a["kind"]!="native":return self.js({"error":"not an allowed native artifact"},404)
    dest=WORK/"inspection-copies"/(str(time.time_ns())+"-"+a["path"].name);dest.parent.mkdir(exist_ok=True);shutil.copy2(a["path"],dest)
    if runner.sha(dest)!=runner.sha(a["path"]):raise ValueError("copy mismatch")
    app=Path(read(REG)["blender"]) if dest.suffix.lower()==".blend" else Path(os.environ.get("ProgramFiles",r"C:\Program Files"))/"Krita (x64)/bin/krita.exe"
    if not app.is_file():raise ValueError("native application unavailable")
    proc=subprocess.Popen([str(app),str(dest)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    return self.js({"status":"launch requested","file":dest.name,"application":app.name,"pid":proc.pid})
   if not secrets.compare_digest(self.headers.get("X-Bridge-Key",""),TOKEN):return self.js({"error":"unauthorized"},403)
   if self.path=="/plan":return self.js(plan(x["objective"]))
   if self.path=="/execute":return self.js(execute(x["request_id"],x["route"]))
   return self.js({"error":"not found"},404)
  except Exception as e:return self.js({"error":str(e)[:350]},400)
 def log_message(self,*a):pass
if __name__=="__main__":print("Workbench bridge "+BASE,flush=True);ThreadingHTTPServer(("127.0.0.1",PORT),H).serve_forever()
