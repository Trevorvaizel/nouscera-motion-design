"""Prepare a bounded cold-agent task and verify its response; fail closed.
The caller chooses/authenticates a provider separately; never grant tool authority.
"""
import argparse,hashlib,json
from pathlib import Path
from runner import bootstrap
FIELDS={"milestone":"WH-001","workflow":"scene-readiness@0.1.0","authorized_operation":"replay_only","creative_test_allowed":False,"animation_approved":False,"notebook_hidden_surface":"unvalidated","native_blender_parity":"unverified","install_n8n":False,"download_models":False,"creative_approval_authority":"author"}
PROMPT="""Read the canonical packet below. This is a read-only orientation task, not creative execution. Return only a JSON object with the following keys:
milestone (string); workflow (id@version); authorized_operation (replay_only or creative); creative_test_allowed (boolean); animation_approved (boolean); notebook_hidden_surface (validated or unvalidated); native_blender_parity (verified or unverified); install_n8n (boolean); download_models (boolean); creative_approval_authority (author or model). Do not use tools or infer approval."""
def prepare(out):
    out.mkdir(parents=True,exist_ok=False)
    packet=bootstrap()
    raw=json.dumps(packet,indent=2).encode()
    (out/"context.json").write_bytes(raw)
    (out/"request.txt").write_text(PROMPT+"\n\n"+raw.decode(),encoding="utf-8")
    (out/"task.json").write_text(json.dumps({"schema_version":1,"task":"cold_orientation","context_sha256":hashlib.sha256(raw).hexdigest(),"tools_authorized":False,"creative_approval":False},indent=2),encoding="utf-8")
def evaluate(answer,provider_exit=0):
    if provider_exit!=0:return {"status":"invocation_failed","provider_exit":provider_exit,"reason":"no valid response evidence","creative_approval":False}
    try:obj=json.loads(answer)
    except (ValueError,TypeError):return {"status":"invalid_response","creative_approval":False}
    if not isinstance(obj,dict):return {"status":"invalid_response","creative_approval":False}
    mismatch=[k for k,v in FIELDS.items() if k not in obj or type(obj[k]) is not type(v) or obj[k]!=v]
    extra=sorted(set(obj)-set(FIELDS))
    return {"status":"pass" if not mismatch and not extra else "fail","mismatches":mismatch,"extra_keys":extra,"creative_approval":False,"scope":"orientation comprehension only, not creative worker capability"}
def main():
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest="cmd",required=True)
    q=sub.add_parser("prepare");q.add_argument("--out",required=True)
    q=sub.add_parser("evaluate");q.add_argument("--answer");q.add_argument("--provider-exit",type=int,default=0);q.add_argument("--out",required=True)
    a=p.parse_args()
    if a.cmd=="prepare":prepare(Path(a.out));return
    ans=Path(a.answer).read_text(encoding="utf-8-sig") if a.answer and Path(a.answer).is_file() else ""
    result=evaluate(ans,a.provider_exit)
    with Path(a.out).open("x",encoding="utf-8") as f:json.dump(result,f,indent=2)
    print(json.dumps(result))
    if result["status"]!="pass":raise SystemExit(2)
if __name__=="__main__":main()
