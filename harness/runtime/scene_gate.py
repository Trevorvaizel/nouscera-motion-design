"""Fail-closed, scene-independent readiness gate. No creative approval or tool execution."""
import argparse,hashlib,json,math,struct,sys
from pathlib import Path
REQUIRED={"environment":"fixed","notebook":"fixed","limb":"deformable","pen":"rigid","head":"articulated","ink":"progressive"}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dimensions(p):
    with Path(p).open("rb") as f:b=f.read(24)
    if b[:8]!=b"\x89PNG\r\n\x1a\n" or b[12:16]!=b"IHDR":raise ValueError("expected PNG")
    return list(struct.unpack(">II",b[16:24]))
def asset(root,a,size):
    p=(root/a["file"]).resolve()
    if not p.is_relative_to(root.resolve()):raise ValueError("asset escapes root")
    if sha(p)!=a["sha256"]:raise ValueError("asset identity mismatch")
    if dimensions(p)!=size:raise ValueError("dimensions mismatch")
    return p
def inspect(m,root):
    errors=[];blocked=[]
    if m.get("schema_version")!=1:errors.append("unsupported schema")
    size=m.get("size",[])
    if len(size)!=2 or any(not isinstance(n,int) or n<=0 for n in size):errors.append("invalid size")
    entities=m.get("entities",{});roles=m.get("required_roles",{})
    # Roles are scene-specific; no assumption that every scene depicts a writer.
    if not roles:errors.append("missing required roles")
    for role,behavior in roles.items():
        if role not in entities or entities[role].get("behavior")!=behavior:errors.append("missing/wrong role: "+role)
    for role,e in entities.items():
        try:
            if e["behavior"] not in ("fixed","rigid","deformable","articulated","progressive"):raise ValueError("invalid behavior")
            for dep in e.get("depends_on",[]):
                if dep not in entities or dep==role:raise ValueError("unresolved dependency")
            if e["behavior"]=="fixed" and e.get("motion")!="identity":raise ValueError("fixed entity must have identity transform")
            if e["behavior"]=="rigid" and e.get("motion")!="rotation_translation_only":raise ValueError("rigid entity cannot be warped or scaled")
            if e.get("asset"):asset(root,e["asset"],size)
            elif e["behavior"]!="progressive":raise ValueError("missing asset")
        except (KeyError,ValueError,OSError) as exc:errors.append(role+": "+str(exc))
    # Check dependency cycles rather than silently resolving a contradictory hierarchy.
    def walk(k,trail):
        if k in trail:raise ValueError("dependency cycle: "+k)
        for dep in entities[k].get("depends_on",[]):
            if dep in entities:walk(dep,trail|{k})
    try:
        for k in entities:walk(k,set())
    except ValueError as exc:errors.append(str(exc))
    hs=m.get("hidden_surfaces",[])
    if not hs and m.get("occlusion_possible",True):blocked.append("hidden surfaces not assessed")
    for h in hs:
        # A review must identify the actual artifact; approval is not inferred from file existence.
        if h.get("status")!="reviewed_pass" or not h.get("review_receipt"):blocked.append("hidden surface not reviewed: "+h.get("id","unknown"));continue
        try:
            p=asset(root,h["asset"],size)
            rev=(root/h["review_receipt"]).resolve()
            if not rev.is_relative_to(root.resolve()):raise ValueError("review escapes root")
            record=json.loads(rev.read_text(encoding="utf-8"))
            if record.get("artifact_sha256")!=sha(p) or record.get("verdict")!="pass" or not record.get("reviewer") or record.get("review_scope")!="hidden_surface_visual":raise ValueError("unbound review")
        except (KeyError,ValueError,OSError) as exc:errors.append(h.get("id","hidden")+": "+str(exc))
    if m.get("scene_id")=="CP05" and roles!=REQUIRED:errors.append("CP05 requires all six roles")
    if m.get("source"):
        try:asset(root,m["source"],size)
        except (KeyError,ValueError,OSError) as exc:errors.append("source: "+str(exc))
    else:errors.append("source missing")
    return {"scene_id":m.get("scene_id"),"status":"invalid" if errors else "blocked" if blocked else "asset_contract_pass","errors":errors,"blockers":blocked,"creative_approval":False,"scope":"metadata, artifact integrity and explicit review receipt; cannot judge artistic quality by itself"}
def main():
    p=argparse.ArgumentParser();p.add_argument("manifest");p.add_argument("--out",required=True);a=p.parse_args();m=Path(a.manifest)
    report=inspect(json.loads(m.read_text(encoding="utf-8")),m.parent)
    dest=Path(a.out)
    with dest.open("x",encoding="utf-8") as f:json.dump(report,f,indent=2)
    print(json.dumps(report,indent=2))
    if report["status"]!="asset_contract_pass":raise SystemExit(2)
if __name__=="__main__":main()
