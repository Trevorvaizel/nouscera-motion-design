"""WH-002: genuine LangGraph, persistent SQLite, bounded decisions."""
import argparse,hashlib,json,os,re,sqlite3,subprocess,sys,time,urllib.request
from pathlib import Path
from typing import TypedDict
from langgraph.graph import StateGraph,START,END
from langgraph.types import Command,interrupt
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.errors import GraphInterrupt
HERE=Path(__file__).resolve().parent
RUNTIME=HERE.parent
sys.path.insert(0,str(RUNTIME))
import runner
BUILD=Path(os.environ.get("NOUSCERA_BUILD_ROOT",str(HERE.parents[3]))).resolve()
WORK=BUILD/"wh002"; REG=BUILD/"runtime-registry-v01.json"; RUNS=BUILD/"runs"; DB=WORK/"graph.sqlite"
CODEX=WORK/"codex-cli/node_modules/.bin/codex.cmd"
MODEL=os.environ.get("NOUSCERA_CODEX_MODEL","gpt-6.2-sol")
PROVIDER=os.environ.get("NOUSCERA_PROVIDER","local")
LOCAL_MODEL="nouscera-deepseek-r1-8b"
LOCAL_ENDPOINT="http://127.0.0.1:8766"
os.environ["LANGSMITH_TRACING"]="false";os.environ["LANGCHAIN_TRACING_V2"]="false"
NODES={
"context":["Load canonical context","Harness","Recover governing instructions and current state."],
"preflight":["Verify source and dependencies","Python","Validate protected artwork, masters and operations by SHA256."],
"model":["Inspect readiness","Reasoning model","Bounded read-only model decision; no creative authority."],
"validate":["Validate proposed route","Policy","Only a conforming model response permits replay."],
"replay":["Execute registered replay","WH-001 runner","Reproduce existing preview in isolated scratch."],
"verify":["Inspect independent evidence","Verifier","Check decoded frames, fixed regions and artifact hashes."],
"review":["Human review interrupt","Human","Inspect technical evidence; acknowledge or request repair."],
"receipt":["Persist graph receipt","Harness","Record model decision, evidence and review outcome."]}
EDGES=[["context","preflight"],["preflight","model"],["model","validate"],["validate","replay"],["validate","review"],["replay","verify"],["verify","review"],["review","receipt"]]
class State(TypedDict,total=False):
 thread_id:str
 packet:dict
 preflight:dict
 model:dict
 decision:dict
 replay:dict
 verification:dict
 asset_gate:dict
 review:dict
 receipt:dict
def safe_id(t):
 if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,60}",t):raise ValueError("invalid thread ID")
 return t
def folder(t):
 p=WORK/"threads"/safe_id(t);p.mkdir(parents=True,exist_ok=True);return p
def read(p):return json.loads(Path(p).read_text(encoding="utf-8-sig"))
def write(p,x):
 p=Path(p);tmp=p.with_suffix(p.suffix+".tmp");tmp.write_text(json.dumps(x,indent=2),encoding="utf-8");os.replace(tmp,p)
def log(t,n,status,detail=None):
 with (folder(t)/"events.jsonl").open("a",encoding="utf-8") as f:
  f.write(json.dumps({"time":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"node":n,"status":status,"detail":detail or {}})+"\n");f.flush();os.fsync(f.fileno())
def node(fn):
 def wrap(s):
  t=s["thread_id"];n=fn.__name__;log(t,n,"running")
  try:
   out=fn(s);log(t,n,"complete");return out
  except GraphInterrupt:
   log(t,n,"waiting");raise
  except Exception as e:
   log(t,n,"failed",{"error":str(e)[:500]});raise
 return wrap
@node
def context(s):
 p=runner.bootstrap();p["wh002"]={"milestone":"WH-002","mode":"observable_replay","creative_test_allowed":False,"scope":"existing WH-001 replay or blocked diagnostic only"}
 write(folder(s["thread_id"])/"context.json",p);return {"packet":p}
def whrun(t):return RUNS/("wh002-"+safe_id(t))
def launch(t,stage):
 p=whrun(t);st=read(p/"state.json") if (p/"state.json").exists() else None
 if st and st["status"]=="complete":return st
 if st and (p/"run.lock").exists():raise RuntimeError("existing runner lock; reconcile before retry")
 if stage=="preflight" and st and "preflight" in st["completed"]:return st
 args=[sys.executable,str(RUNTIME/"runner.py"),"run","--registry",str(REG),"--runs",str(RUNS),"--id",p.name]
 if st:args+=["--resume"]
 if stage=="preflight":args+=["--stop-after","preflight"]
 logfile=folder(t)/("runner-"+stage+"-"+str(time.time_ns())+".log")
 with logfile.open("w",encoding="utf-8") as f:cp=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,timeout=180)
 if cp.returncode:raise RuntimeError("runner failed: "+str(logfile))
 return read(p/"state.json")
@node
def preflight(s):
 t=s["thread_id"];st=launch(t,"preflight")
 return {"preflight":{"status":"pass","run_id":st["id"],"fingerprint":st["fingerprint"],"file":str(whrun(t)/"preflight.json")}}
PROMPT="""You are an independent NOUSCERA inspection model. Use ONLY the supplied canonical packet. Do not call tools, modify files, invent evidence or authorize new creative work. Choose the permitted route. Return exactly one JSON object with keys: route (replay_only or block), reason (one short evidence-based sentence), creative_test_allowed (boolean), animation_approved (boolean), hidden_surfaces (unvalidated or validated), native_blender_parity (unverified or verified), approval_authority (author or model). WH-002 wraps the WH-001 contract."""
def parse_answer(raw):
 x=raw.strip()
 if x.startswith("```"):x=re.sub(r"^```(?:json)?\s*|\s*```$","",x,flags=re.I)
 return json.loads(x)
def policy(x):
 if not isinstance(x,dict):return False
 expected={"route":"replay_only","creative_test_allowed":False,"animation_approved":False,"hidden_surfaces":"unvalidated","native_blender_parity":"unverified","approval_authority":"author"}
 return set(x)==set(expected)|{"reason"} and isinstance(x["reason"],str) and 5<=len(x["reason"])<=400 and all(type(x[k]) is type(v) and x[k]==v for k,v in expected.items())
@node
def model(s):
 p=folder(s["thread_id"]);target=p/"model.json"
 if target.exists():return {"model":read(target)}
 request=PROMPT+"\n\n"+json.dumps(s["packet"],indent=2)
 (p/"model-request.txt").write_text(request,encoding="utf-8")
 m={"provider":"Codex CLI","model_requested":MODEL,"instruction_sha256":hashlib.sha256(request.encode()).hexdigest(),"status":"invocation_failed","request_file":str(p/"model-request.txt"),"tools_authorized":False}
 if PROVIDER=="local":
  m.update(provider="llama.cpp local inference",model_requested=LOCAL_MODEL,endpoint=LOCAL_ENDPOINT)
  try:
   headers={"Authorization":"Bearer "+(WORK/"local-inference.key").read_text(encoding="ascii").strip()}
   with urllib.request.urlopen(urllib.request.Request(LOCAL_ENDPOINT+"/v1/models",headers=headers),timeout=5) as r:available=json.load(r)
   if LOCAL_MODEL not in [x["id"] for x in available["data"]]:raise ValueError("expected local model not served")
   schema={"type":"object","properties":{"route":{"type":"string","enum":["replay_only","block"]},"reason":{"type":"string"},"creative_test_allowed":{"type":"boolean"},"animation_approved":{"type":"boolean"},"hidden_surfaces":{"type":"string","enum":["validated","unvalidated"]},"native_blender_parity":{"type":"string","enum":["verified","unverified"]},"approval_authority":{"type":"string","enum":["author","model"]}},"required":["route","reason","creative_test_allowed","animation_approved","hidden_surfaces","native_blender_parity","approval_authority"],"additionalProperties":False}
   body={"model":LOCAL_MODEL,"messages":[{"role":"user","content":request}],"temperature":0.1,"max_tokens":768,"response_format":{"type":"json_schema","json_schema":{"name":"readiness_decision","schema":schema}}}
   write(p/"model-api-request.json",body)
   req=urllib.request.Request(LOCAL_ENDPOINT+"/v1/chat/completions",data=json.dumps(body).encode(),headers={**headers,"Content-Type":"application/json"})
   with urllib.request.urlopen(req,timeout=180) as r:res=json.load(r)
   choice=res["choices"][0];raw=choice["message"]["content"] or ""
   answer=p/"model-answer.txt";answer.write_text(raw,encoding="utf-8")
   m.update(model_returned=res.get("model"),usage=res.get("usage"),finish_reason=choice.get("finish_reason"),answer=parse_answer(raw),answer_file=str(answer),status="responded")
   if res.get("model")!=LOCAL_MODEL:raise ValueError("returned model identity differs")
  except Exception as e:m.update(status="invocation_failed",error=str(e)[:500])
 elif PROVIDER!="codex":m["error"]="unknown provider"
 elif not CODEX.is_file():m["error"]="isolated Codex CLI unavailable"
 else:
  answer=p/"model-answer.txt";cwd=p/"provider-sandbox";cwd.mkdir(exist_ok=True)
  try:
   args=[str(CODEX),"exec","--ephemeral","--skip-git-repo-check","-s","read-only","-m",MODEL,"-c","mcp_servers={}","-o",str(answer),"-"]
   with (p/"model-cli.log").open("wb") as f:cp=subprocess.run(args,input=request.encode(),stdout=f,stderr=subprocess.STDOUT,cwd=cwd,timeout=110)
   m["provider_exit"]=cp.returncode
   if cp.returncode==0 and answer.is_file():m.update(status="responded",answer=parse_answer(answer.read_text(encoding="utf-8-sig")),answer_file=str(answer))
   else:m["error"]="provider returned nonzero exit; see local provider log"
  except Exception as e:m["error"]=str(e)[:350]
 write(target,m);return {"model":m}
@node
def validate(s):
 m=s["model"];ok=m["status"]=="responded" and policy(m.get("answer"))
 return {"decision":{"route":"replay" if ok else "review","status":"pass" if ok else "blocked","reason":m["answer"]["reason"] if ok else "No conforming independent model response. Replay not authorized by this graph.","creative_approval":False}}
@node
def replay(s):
 if s["decision"]["status"]!="pass":raise ValueError("model gate not passed")
 t=s["thread_id"];st=launch(t,"replay")
 return {"replay":{"status":st["status"],"file":str(whrun(t)/"state.json"),"receipt":str(whrun(t)/"receipt.json")}}
@node
def verify(s):
 p=whrun(s["thread_id"]);v=read(p/"verification.json");r=read(p/"receipt.json")
 if v["status"]!="pass" or r["creative_approval"] is not False or runner.sha(p/"verification.json")!=r["verification_sha256"] or runner.sha(p/"scratch/reviews/CP05_prepared_scene_motion_v02.mp4")!=r["artifact_sha256"]:raise ValueError("replay evidence invalid")
 return {"verification":v}
@node
def review(s):
 gate=read(BUILD/"asset-gates/CP05-v01/gate.json")
 payload={"type":"technical_review","thread":s["thread_id"],"model_decision":s.get("decision"),"verification":s.get("verification"),"asset_gate":gate,"creative_approval":False,"allowed":["acknowledge_technical","request_repair"]}
 answer=interrupt(payload)
 if not isinstance(answer,dict) or answer.get("decision") not in payload["allowed"] or not isinstance(answer.get("reviewer"),str) or not answer["reviewer"].strip():raise ValueError("invalid review response")
 return {"asset_gate":gate,"review":{"decision":answer["decision"],"reviewer":answer["reviewer"][:80],"note":str(answer.get("note",""))[:500],"creative_approval":False}}
@node
def receipt(s):
 r={"thread_id":s["thread_id"],"milestone":"WH-002","model_status":s["model"]["status"],"decision":s["decision"],"verification":s.get("verification"),"review":s["review"],"creative_approval":False,"asset_gate":s["asset_gate"],"checkpoint_backend":"SQLite"}
 write(folder(s["thread_id"])/"graph-receipt.json",r);return {"receipt":r}
def builder():
 g=StateGraph(State)
 for name in NODES:g.add_node(name,globals()[name])
 g.add_edge(START,"context");g.add_edge("context","preflight");g.add_edge("preflight","model");g.add_edge("model","validate")
 g.add_conditional_edges("validate",lambda s:s["decision"]["route"],{"replay":"replay","review":"review"})
 g.add_edge("replay","verify");g.add_edge("verify","review");g.add_edge("review","receipt");g.add_edge("receipt",END);return g
graph=builder().compile()
def config(t):return {"configurable":{"thread_id":safe_id(t)}}
def open_graph():
 WORK.mkdir(parents=True,exist_ok=True);conn=sqlite3.connect(DB,check_same_thread=False,timeout=30);return conn,builder().compile(checkpointer=SqliteSaver(conn))
def snapshot(t):
 conn,g=open_graph()
 try:
  snap=g.get_state(config(t))
  return {"values":snap.values,"next":list(snap.next),"interrupts":[i.value for i in snap.interrupts],"checkpoint_id":snap.config.get("configurable",{}).get("checkpoint_id")}
 finally:conn.close()
def execute(t,answer=None):
 conn,g=open_graph();lock=folder(t)/"graph.lock"
 try:fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
 except Exception:conn.close();raise
 try:
  with os.fdopen(fd,"w") as f:f.write(str(os.getpid()))
  prior=g.get_state(config(t))
  if answer is None:
   if prior.values:raise ValueError("thread exists; inspect or resume explicitly")
   g.invoke({"thread_id":t},config(t))
  else:
   if not prior.interrupts:raise ValueError("thread is not waiting at a review interrupt")
   g.invoke(Command(resume=answer),config(t))
  return snapshot(t)
 finally:lock.unlink(missing_ok=True);conn.close()
def main():
 p=argparse.ArgumentParser();p.add_argument("command",choices=["start","inspect","resume"]);p.add_argument("thread");p.add_argument("--decision",choices=["acknowledge_technical","request_repair"]);p.add_argument("--reviewer");p.add_argument("--note",default="")
 a=p.parse_args()
 if a.command=="start":execute(a.thread)
 elif a.command=="resume":execute(a.thread,{"decision":a.decision,"reviewer":a.reviewer,"note":a.note})
 snap=snapshot(a.thread);print(json.dumps({"next":snap["next"],"interrupts":snap["interrupts"],"decision":snap["values"].get("decision"),"model":snap["values"].get("model"),"verification":snap["values"].get("verification"),"review":snap["values"].get("review")},default=str,indent=2))
if __name__=="__main__":main()
