from pathlib import Path
import hashlib,json,numpy as np,av
from PIL import Image
p=Path.home()/"Documents/NOUSCERA/reviews";a=p/"MCI09_integrated_v03";b=p/"MCI09_integrated_v04"
patch=np.array(Image.open(b/"sleeve_seam_repair.png").convert("RGBA"));mask=patch[:,:,3]>0
paths=sorted((b/"native_render").glob("*.png"));assert len(paths)==48
frames=[];outside=0;changed=0
for i,path in enumerate(paths,1):
 f=np.array(Image.open(path).convert("RGB"));prev=np.array(Image.open(a/"native_render"/f"frame_{i:04d}.png").convert("RGB"))
 diff=np.any(f!=prev,axis=2);outside+=int(diff[~mask].sum());changed+=int(diff[mask].sum())
 if i==1:assert np.array_equal(f,prev)
 frames.append(f)
assert outside==0 and changed>0,(outside,changed)
video=b/"CP05_MCI09_integrated_v04.mp4"
with av.open(str(video),"w") as c:
 st=c.add_stream("libx264",rate=24);st.width=720;st.height=1280;st.pix_fmt="yuv420p";st.options={"crf":"15"}
 for f in frames:
  for pkt in st.encode(av.VideoFrame.from_ndarray(f,format="rgb24")):c.mux(pkt)
 for pkt in st.encode():c.mux(pkt)
with av.open(str(video)) as c:assert sum(1 for f in c.decode(video=0))==48
sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
out={"experiment":"MCI09 V12 local sleeve seam repair","native_blender_render":True,"frames":48,"fps":24,"resolution":[720,1280],"video_sha256":sha(video),"blend_sha256":sha(b/"CP05_MCI09_integrated_v04.blend"),"changed_pixels_outside_patch_all_frames":outside,"changed_pixels_inside_patch_all_frames":changed,"patch_support_pixels":int(mask.sum()),"first_frame_exact_to_v11":True,"creative_approval":False,"gate":"blocked; author review pending","method":"Feathered original source texture anchored at sleeve seam; V11 layers unchanged. Not cloth simulation."}
(b/"native_render_receipt.json").write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
