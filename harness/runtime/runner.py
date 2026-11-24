"""Versioned local replay harness; no network/model calls or creative authorization."""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, time
from pathlib import Path
HERE=Path(__file__).resolve().parent
STAGES=("preflight","replay","verify","receipt")
def read(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def sha(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()
def atomic(p,obj):
    p=Path(p);tmp=p.with_name(p.name+".tmp")
    tmp.write_text(json.dumps(obj,indent=2),encoding="utf-8");os.replace(tmp,p)
def now():return time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())
def contract():
    c=read(HERE/"workflows/scene-readiness.v01.json")
    if c["schema_version"]!=1 or c["mode"]!="replay_only" or tuple(s["id"] for s in c["stages"])!=STAGES or c["acceptance"]["author_approval"] is not False:raise ValueError("unsupported or unsafe contract")
    return c
def bootstrap():
    state=read(HERE/"current.json");c=contract()
    if state["active_workflow"]!=c["id"]+"@"+c["version"] or state["approved_animation"] is not False or state["active_mode"]!="harness_reliability":raise ValueError("state/contract mismatch")
    return {"context_version":1,"state":state,"contract":c,"catalog":read(HERE/"catalog.json"),"authority":"Author controls creative approval. Replay cannot grant it. Stop on conflict or absent evidence."}
def fingerprint(reg):
    return {"registry":sha(reg),"contract":sha(HERE/"workflows/scene-readiness.v01.json"),"state":sha(HERE/"current.json"),"catalog":sha(HERE/"catalog.json"),"runner":sha(__file__),"verifier":sha(HERE/"verify_replay.py")}
def validate_registry(reg,c):
    r=read(reg)
    if r["schema_version"]!=1:raise ValueError("registry schema")
    for x in c["inputs"]:
        i=r["items"][x["id"]]
        for k in ("path","frozen_path"):
            if k in i and sha(i[k])!=i["sha256"]:raise ValueError("hash mismatch: "+x["id"]+"/"+k)
    if not Path(r["python"]).is_file():raise ValueError("runtime missing")
    return r
def safe_id(s):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}",s):raise ValueError("invalid run id")
    return s
def checked_process(argv,log,env=None):
    with open(log,"w",encoding="utf-8") as f:
        result=subprocess.run(argv,stdout=f,stderr=subprocess.STDOUT,env=env,check=False)
    if result.returncode:raise RuntimeError("process failed; see "+str(log))
def stage_replay(run,r):
    scratch=run/"scratch"
    if scratch.exists():
        quarantine=run/("interrupted-scratch-"+str(time.time_ns()))
        scratch.rename(quarantine)
    for d in ("assets","reviews","tools","blender","lossless"):(scratch/d).mkdir(parents=True,exist_ok=True)
    for id,rel in [("cp05_source","assets/NOUSCERA_Film001_CP05_ARTWORK_ONLY.png"),("tracks_v02","reviews/MCI07_CP05_joint_tracks_v02.json")]:
        shutil.copyfile(r["items"][id]["frozen_path"],scratch/rel)
    frozen=Path(r["items"]["prepared_scene_code"]["frozen_path"])
    code=frozen.read_text(encoding="utf-8")
    # Explicit adapter: one root substitution and lossless diagnostic frame capture. Original code immutable.
    lines=code.splitlines();matches=[i for i,l in enumerate(lines) if l.startswith("home=Path(r")]
    if len(matches)!=1:raise ValueError("unexpected adapter root")
    lines[matches[0]]='home=Path(__import__("os").environ["NOUSCERA_RUN_ROOT"])'
    capture=[i for i,l in enumerate(lines) if l.strip()=="frames.append(f)"]
    if len(capture)!=1:raise ValueError("unexpected frame capture point")
    i=capture[0];lines.insert(i+1,' Image.fromarray(f).save(home/"lossless"/f"{fi:03d}.png")')
    script=scratch/"tools/replay_adapter.py";script.write_text("\n".join(lines)+"\n",encoding="utf-8")
    env=dict(os.environ,NOUSCERA_RUN_ROOT=str(scratch))
    checked_process([r["python"],str(script)],run/"replay.log",env)
    atomic(run/"replay-adapter.json",{"source_script_sha256":sha(frozen),"adapter_sha256":sha(script),"changes":["isolated root","lossless frame capture"]})
def run_command(a):
    c=contract();packet=bootstrap();reg=Path(a.registry).resolve();fp=fingerprint(reg)
    root=Path(a.runs).resolve();root.mkdir(parents=True,exist_ok=True)
    run=root/safe_id(a.id);statefile=run/"state.json"
    if run.exists():
        if not a.resume:raise ValueError("run exists; use --resume")
        state=read(statefile)
        if state["fingerprint"]!=fp:raise ValueError("version/registry changed; new run required")
        if state["status"]=="complete":raise ValueError("run already complete; inspect receipt")
    else:
        if a.resume:raise ValueError("no run to resume")
        run.mkdir();state={"id":a.id,"status":"new","completed":[],"fingerprint":fp,"attempts":[]}
        atomic(statefile,state);atomic(run/"context.json",packet)
    lock=run/"run.lock"
    fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    with os.fdopen(fd,"w") as f:f.write(str(os.getpid()))
    try:
        r=validate_registry(reg,c)
        for stage in STAGES:
            if stage in state["completed"]:continue
            state.update(status="running",active_stage=stage);state["attempts"].append({"stage":stage,"started":now()});atomic(statefile,state)
            if stage=="preflight":atomic(run/"preflight.json",{"status":"pass","input_ids":[i["id"] for i in c["inputs"]],"fingerprint":fp,"time":now()})
            elif stage=="replay":stage_replay(run,r)
            elif stage=="verify":
                checked_process([r["python"],str(HERE/"verify_replay.py"),str(run),str(reg),str(HERE/"workflows/scene-readiness.v01.json")],run/"verify.log")
                if read(run/"verification.json")["status"]!="pass":raise RuntimeError("verification failed")
            elif stage=="receipt":
                validate_registry(reg,c)
                atomic(run/"receipt.json",{"run_id":a.id,"workflow":c["id"]+"@"+c["version"],"technical_status":"verified_replay","creative_approval":False,"fingerprint":fp,"verification_sha256":sha(run/"verification.json"),"artifact_sha256":sha(run/"scratch/reviews/CP05_prepared_scene_motion_v02.mp4"),"time":now(),"limitations":c["non_goals"]})
            state["completed"].append(stage);state["attempts"][-1]["finished"]=now();state.update(status="paused",active_stage=None);atomic(statefile,state)
            if a.stop_after==stage and stage!="receipt":print(json.dumps(state));return
        state.update(status="complete",active_stage=None);atomic(statefile,state);print(json.dumps(state))
    except Exception as e:
        state.update(status="failed",error=str(e));atomic(statefile,state);raise
    finally:lock.unlink(missing_ok=True)
def main():
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest="cmd",required=True)
    sub.add_parser("bootstrap");sub.add_parser("plan")
    q=sub.add_parser("run");q.add_argument("--registry",required=True);q.add_argument("--runs",required=True);q.add_argument("--id",required=True);q.add_argument("--resume",action="store_true");q.add_argument("--stop-after",choices=STAGES)
    q=sub.add_parser("status");q.add_argument("--runs",required=True);q.add_argument("--id",required=True)
    a=p.parse_args()
    if a.cmd=="bootstrap":print(json.dumps(bootstrap(),indent=2))
    elif a.cmd=="plan":print(json.dumps(contract(),indent=2))
    elif a.cmd=="status":print(json.dumps(read(Path(a.runs)/safe_id(a.id)/"state.json"),indent=2))
    else:run_command(a)
if __name__=="__main__":main()
