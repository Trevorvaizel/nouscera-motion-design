from pathlib import Path
import json,hashlib,numpy as np,av
from PIL import Image,ImageDraw
p=Path.home()/"Documents/NOUSCERA";root=p/"reviews/MCI09_integrated_v03"
src=np.array(Image.open(p/"assets/NOUSCERA_Film001_CP05_ARTWORK_ONLY.png").convert("RGB"))
paths=sorted((root/"native_render").glob("*.png"))
assert len(paths)==48
frames=[];metrics=[]
for i,path in enumerate(paths):
 f=np.array(Image.open(path).convert("RGB"));assert f.shape==src.shape
 ref=np.array(Image.open(root/"preview"/f"{i+1:04d}.png").convert("RGB"))
 lock=np.array(Image.open(root/"source_lock"/f"{i+1:04d}.png").convert("RGBA"))[:,:,3]==255
 diff=np.abs(f.astype(np.int16)-src.astype(np.int16))
 err=np.abs(f.astype(np.int16)-ref.astype(np.int16))
 metrics.append({"frame":i+1,"locked_pixels":int(lock.sum()),"locked_max":int(diff[lock].max()),"locked_changed":int(np.any(diff[lock]!=0,axis=1).sum()),"composite_mad":float(err.mean()),"composite_max":int(err.max())})
 frames.append(f)
video=root/"CP05_MCI09_integrated_v03.mp4"
assert not video.exists()
with av.open(str(video),"w") as c:
 st=c.add_stream("libx264",rate=24);st.width=720;st.height=1280;st.pix_fmt="yuv420p";st.options={"crf":"15"}
 for f in frames:
  for pkt in st.encode(av.VideoFrame.from_ndarray(f,format="rgb24")):c.mux(pkt)
 for pkt in st.encode():c.mux(pkt)
with av.open(str(video)) as c: decoded=sum(1 for f in c.decode(video=0))
assert decoded==48
sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
board=Image.new("RGB",(1200,550),(20,20,20));d=ImageDraw.Draw(board)
for j,k in enumerate([0,12,20,28,38,47]):
 board.paste(Image.fromarray(frames[k]).resize((180,320)),(j*200+10,24))
 d.text((j*200+10,5),f"Blender native F{k+1:02d}",fill="white")
 board.paste(Image.fromarray(frames[k]).crop((330,850,680,1090)).resize((190,130)),(j*200+5,375))
board.save(root/"native_contact.png")
out={"native_blender_render":True,"frames":decoded,"fps":24,"resolution":[720,1280],"duration_seconds":2,"video_sha256":sha(video),"blend_sha256":sha(root/"CP05_MCI09_integrated_v03.blend"),"native_first_frame_exact":bool(np.array_equal(frames[0],src)),"native_max_locked_pixel_delta":max(r["locked_max"] for r in metrics),"native_max_locked_changed_pixels":max(r["locked_changed"] for r in metrics),"native_max_composite_mad":max(r["composite_mad"] for r in metrics),"metrics":metrics,"creative_approval":False,"gate":"blocked; isolated experimental review"}
(root/"native_render_receipt.json").write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k!="metrics"},indent=2))
