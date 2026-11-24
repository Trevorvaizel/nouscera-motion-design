"""Local-only WH-002 read/technical-review console. No arbitrary path or shell API."""
import argparse,json,mimetypes,secrets,threading,urllib.parse,os,time
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import graph_runtime as g
HERE=Path(__file__).resolve().parent
TOKEN=secrets.token_urlsafe(32)
PORT=8765
THREAD="local-demo-01"
START_LOCK=threading.Lock()
def known_threads():
 root=g.WORK/"threads"
 return sorted([x.name for x in root.iterdir() if x.is_dir() and (x/"events.jsonl").is_file()]) if root.is_dir() else []
def chosen(t):
 t=g.safe_id(t)
 if t not in known_threads():raise ValueError("unknown thread")
 return t
def artifacts(t):
 p=g.folder(t);w=g.whrun(t);reg=g.read(g.REG)
 a={}
 def add(key,label,path,kind,parents=(),digest=None):
  path=Path(path)
  if path.is_file():a[key]={"label":label,"path":str(path),"kind":kind,"bytes":path.stat().st_size,"parents":list(parents),"sha256":digest}
 for key,label,kind in [("cp05_source","CP05 protected artwork","image"),("kra_master","Original layered Krita master","native"),("tracks_v02","Frozen motion tracks","json"),("prepared_scene_code","Frozen prepared scene operation","text"),("prepared_blender_master","Prepared Blender master (native parity unverified)","native"),("baseline_video","Prior prepared-scene preview","video")]:
  x=reg["items"][key];add(key,label,x["path"],kind,(),x["sha256"])
 add("context","Canonical context packet",p/"context.json","json")
 add("request","Actual model instruction packet",p/"model-request.txt","text",["context"])
 add("answer","Actual model answer",p/"model-answer.txt","text",["request"])
 add("model_receipt","Provider invocation receipt",p/"model.json","json",["request","answer"])
 add("preflight","Input integrity receipt",w/"preflight.json","json",["cp05_source","kra_master","prepared_scene_code","tracks_v02"])
 add("run_state","WH-001 execution state",w/"state.json","json",["preflight"])
 add("replay_video","Isolated replay video",w/"scratch/reviews/CP05_prepared_scene_motion_v02.mp4","video",["cp05_source","tracks_v02","prepared_scene_code","preflight"])
 add("verification","Independent frame verification",w/"verification.json","json",["replay_video","baseline_video"])
 add("replay_receipt","Replay receipt",w/"receipt.json","json",["verification"])
 add("asset_gate","Actual CP05 asset readiness gate",g.BUILD/"asset-gates/CP05-v01/gate.json","json")
 add("graph_receipt","Graph execution and review receipt",p/"graph-receipt.json","json",["model_receipt","replay_receipt","asset_gate"])
 return a
def events(t):
 p=g.folder(t)/"events.jsonl";out=[]
 if p.is_file():
  for line in p.read_text(encoding="utf-8").splitlines():
   try:out.append(json.loads(line))
   except ValueError:pass
 return out
def status(t):
 snap=g.snapshot(t);a=artifacts(t);ev=events(t)
 return {"thread":t,"nodes":g.NODES,"edges":g.EDGES,"snapshot":snap,"events":ev,"artifacts":a,"asset_gate":g.read(g.BUILD/"asset-gates/CP05-v01/gate.json"),"active_lock":(g.folder(t)/"graph.lock").exists(),"engine":"LangGraph + SQLite","creative_test_allowed":False,"scope":"Technical replay only"}
class Handler(BaseHTTPRequestHandler):
 def send(self,data,typ="application/json",code=200):
  self.send_response(code);self.send_header("Content-Type",typ);self.send_header("Content-Length",str(len(data)));self.send_header("Cache-Control","no-store");self.send_header("X-Content-Type-Options","nosniff");self.send_header("Referrer-Policy","no-referrer");self.send_header("Content-Security-Policy","default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; media-src 'self'; object-src 'none'; frame-ancestors 'none'");self.end_headers();self.wfile.write(data)
 def js(self,x,code=200):self.send(json.dumps(x,default=str).encode(),"application/json; charset=utf-8",code)
 def allowed_host(self):return self.headers.get("Host","") in [f"127.0.0.1:{PORT}",f"localhost:{PORT}"]
 def do_GET(self):
  if not self.allowed_host():return self.js({"error":"local host only"},403)
  u=urllib.parse.urlparse(self.path);q=urllib.parse.parse_qs(u.query)
  try:
   if u.path=="/":return self.send((HERE/"console.html").read_text(encoding="utf-8").replace("__LOCAL_TOKEN__",TOKEN).encode(),"text/html; charset=utf-8")
   if u.path=="/api/threads":return self.js({"threads":known_threads(),"default":THREAD})
   if u.path=="/api/state":return self.js(status(chosen(q.get("thread",[THREAD])[0])))
   if u.path=="/api/artifact":
    key=q.get("id",[""])[0];a=artifacts(chosen(q.get("thread",[THREAD])[0])).get(key)
    if not a or a["kind"]=="native":return self.js({"error":"not available for browser preview; use displayed local path"},404)
    p=Path(a["path"]);typ={"image":"image/png","video":"video/mp4","json":"application/json; charset=utf-8","text":"text/plain; charset=utf-8"}[a["kind"]]
    if p.stat().st_size>50*1024*1024:return self.js({"error":"preview exceeds local limit"},413)
    return self.send(p.read_bytes(),typ)
   return self.js({"error":"not found"},404)
  except Exception as e:return self.js({"error":str(e)[:400]},500)
 def do_POST(self):
  if not self.allowed_host() or self.headers.get("Origin") not in [f"http://127.0.0.1:{PORT}",f"http://localhost:{PORT}"] or not secrets.compare_digest(self.headers.get("X-Local-Token",""),TOKEN):return self.js({"error":"local authorization required"},403)
  try:
   if self.path not in ["/api/review","/api/start"]:return self.js({"error":"not found"},404)
   length=int(self.headers.get("Content-Length","0"))
   if not 1<=length<=4096:return self.js({"error":"invalid request"},400)
   a=json.loads(self.rfile.read(length))
   if self.path=="/api/start":
    if a!={"operation":"technical_replay_only"}:return self.js({"error":"explicit technical replay request required"},400)
    with START_LOCK:
     if any((g.folder(t)/"graph.lock").exists() for t in known_threads()):return self.js({"error":"another graph is running"},409)
     t="local-"+time.strftime("%Y%m%d-%H%M%S")+"-"+secrets.token_hex(3)
     g.log(t,"context","queued",{"scope":"technical replay only"})
     def worker():
      try:g.execute(t)
      except Exception as e:g.log(t,"context","failed",{"error":str(e)[:350]})
     threading.Thread(target=worker,daemon=True).start()
    return self.js({"thread":t,"status":"started","creative_approval":False},202)
   t=chosen(a.pop("thread",THREAD));snap=g.snapshot(t)
   if not snap["interrupts"] or (g.folder(t)/"graph.lock").exists():return self.js({"error":"no available review interrupt"},409)
   if a.get("decision") not in ["acknowledge_technical","request_repair"] or not str(a.get("reviewer","")).strip():return self.js({"error":"reviewer and explicit decision required"},400)
   g.execute(t,a);return self.js({"status":"recorded","creative_approval":False})
  except Exception as e:return self.js({"error":str(e)[:400]},500)
 def log_message(self,*args):pass
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--thread",default="local-demo-01");p.add_argument("--port",type=int,default=8765);a=p.parse_args();THREAD=g.safe_id(a.thread);PORT=a.port
 print(f"NOUSCERA console: http://127.0.0.1:{PORT}/ thread {THREAD}",flush=True)
 ThreadingHTTPServer(("127.0.0.1",PORT),Handler).serve_forever()
