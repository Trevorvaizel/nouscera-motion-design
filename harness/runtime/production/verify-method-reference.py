"""Read-only integrity check for the approved CP05 reference and method registry."""
from pathlib import Path
import argparse,hashlib,json

def check(workspace: Path):
    root=Path(__file__).resolve().parent
    policy=json.loads((root/"method-policy.v1.json").read_text(encoding="utf-8"))
    approval=json.loads((root/policy["reference"]["approval"]).read_text(encoding="utf-8"))
    assert approval["revision"]==policy["reference"]["revision"]
    assert approval["preview_id"]==policy["reference"]["preview_id"]
    assert approval["creative_approval"] is True
    def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
    workspace=workspace.resolve()
    for name,expected in approval["dependency_manifest"].items():
        p=(workspace/name).resolve()
        if not p.is_relative_to(workspace) or not p.is_file() or digest(p)!=expected:
            raise ValueError("Missing or altered approved dependency: "+name)
    source=workspace/"assets/NOUSCERA_Film001_CP05_ARTWORK_ONLY.png"
    assert digest(source)==policy["reference"]["source_sha256"],"Protected source changed"
    for method in policy["methods"]:
        for relative in method["evidence"]:
            evidence=(root/relative).resolve()
            assert evidence.is_relative_to(root) and evidence.is_file(),relative
    wf=json.loads((root/"method-decision.n8n.json").read_text(encoding="utf-8"))
    code=next(n["parameters"]["jsCode"] for n in wf["nodes"] if n["name"]=="Resolve method from evidence")
    embedded=json.loads(code.split("const registry=",1)[1].split(";\n",1)[0])
    assert embedded==policy,"Policy and published definition drift"
    return {"reference_revision":approval["revision"],"verified_dependencies":len(approval["dependency_manifest"]),"protected_source_verified":True,"policy_sha256":digest(root/"method-policy.v1.json"),"definition_registry_match":True,"creative_approval_granted":False,"readiness_promoted":False}

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("workspace",type=Path,help="Authorized NOUSCERA workspace containing assets and reviews")
    print(json.dumps(check(p.parse_args().workspace),indent=2))
