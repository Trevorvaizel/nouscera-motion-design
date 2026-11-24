"""Independent comparison of frozen baseline and replay, using lossless checkpoints."""
import hashlib,json,sys
from pathlib import Path
import av,numpy as np
from PIL import Image
def read(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def video(p):
    with av.open(str(p)) as c:
        stream=c.streams.video[0]
        return [f.to_ndarray(format="rgb24") for f in c.decode(video=0)],float(stream.average_rate)
def main():
    run=Path(sys.argv[1]);r=read(sys.argv[2]);c=read(sys.argv[3]);a=c["acceptance"];scratch=run/"scratch"
    source=np.array(Image.open(r["items"]["cp05_source"]["frozen_path"]).convert("RGB"))
    paths=sorted((scratch/"lossless").glob("*.png"));raw=[np.array(Image.open(p).convert("RGB")) for p in paths]
    baseline,bfps=video(r["items"]["baseline_video"]["path"])
    replay,fps=video(scratch/"reviews/CP05_prepared_scene_motion_v02.mp4")
    checks={}
    checks["dimensions_and_count"]=len(raw)==len(replay)==len(baseline)==a["expected_frames"] and all(f.shape==(a["height"],a["width"],3) for f in raw+replay+baseline) and fps==bfps==a["fps"]
    checks["first_frame_source"]=bool(np.array_equal(raw[0],source))
    checks["decoded_replay_exact"]=len(baseline)==len(replay) and all(np.array_equal(x,y) for x,y in zip(baseline,replay))
    rois={}
    for roi in a["protected_rois"]:
        x,y,X,Y=roi["xyxy"];q=source[y:Y,x:X];changes=[int(np.count_nonzero(np.any(f[y:Y,x:X]!=q,axis=2))) for f in raw];rois[roi["name"]]={"pixels":int(q.shape[0]*q.shape[1]),"max_changed":max(changes)}
    checks["independent_static_rois"]=all(x["max_changed"]==0 for x in rois.values())
    m=read(scratch/"reviews/CP05_prepared_scene_metrics_v02.json");orig=read(r["items"]["baseline_metrics"]["frozen_path"])
    checks["reported_metrics_match"]=m==orig
    tracks=read(scratch/"reviews/CP05_prepared_scene_tracks_v02.json")
    # Track invariants are not pixel-level proof of pen rigidity or contact.
    checks["finite_tracks"]=len(tracks)==a["expected_frames"] and all(np.isfinite(np.array(t["pen_tip"])).all() for t in tracks)
    out={"status":"pass" if all(checks.values()) else "fail","checks":checks,"static_rois":rois,"frame_count":len(replay),"fps":fps,"limitations":["exact replay does not prove artistic quality","fixed ROI audit excludes possible occlusions","no claim of native Blender parity, correct hidden surfaces or physical acting","no creative approval"]}
    (run/"verification.json").write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
    if out["status"]!="pass":raise SystemExit(1)
if __name__=="__main__":main()
