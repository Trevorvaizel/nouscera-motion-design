from pathlib import Path
import json,hashlib,numpy as np,av
from PIL import Image,ImageDraw
home=Path.home()/"Documents/NOUSCERA";root=home/"reviews/MCI11_integrated_v01"
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
paths=sorted((root/"native_render").glob("*.png"));assert len(paths)==48
video=root/"CP05_MCI11_integrated_connected_limb_v01.mp4";assert not video.exists()
with av.open(str(video),"w") as c:
 st=c.add_stream("libx264",rate=24);st.width=720;st.height=1280;st.pix_fmt="yuv420p";st.options={"crf":"15"}
 for path in paths:
  f=np.array(Image.open(path).convert("RGB"));assert f.shape==(1280,720,3)
  for pkt in st.encode(av.VideoFrame.from_ndarray(f,format="rgb24")):c.mux(pkt)
 for pkt in st.encode():c.mux(pkt)
with av.open(str(video)) as c:assert sum(1 for f in c.decode(video=0))==48
board=Image.new("RGB",(1200,660),(24,24,24));d=ImageDraw.Draw(board)
for j,k in enumerate([1,13,21,29,40,48]):
 im=Image.open(paths[k-1]).convert("RGB");d.text((j*200+8,6),f"Native frame {k}",fill="white");board.paste(im.resize((185,329)),(j*200+8,28))
 board.paste(im.crop((60,800,650,1060)).resize((190,84)),(j*200+5,395))
board.save(root/"motion_review.png")
tracks=json.loads((root/"rig_tracks.json").read_text())
r={"experiment":"MCI11 integrated native connected armature","frames":48,"fps":24,"resolution":[720,1280],"video_sha256":sha(video),"master_sha256":sha(root/"CP05_MCI11_integrated_connected_limb.blend"),"rig_master_sha256":sha(root/"CP05_MCI11_connected_animated.blend"),"maximum_nib_target_error_px":max(x["tip_error_px"] for x in tracks),"maximum_joint_gap_px":max(x["joint_gap_px"] for x in tracks),"plate":json.loads((root/"plate_receipt.json").read_text()),"creative_approval":False,"readiness":"blocked; integrated experimental preview","limitations":["Sampled stills show softer moving engraving, visible narrow shoulder boundary and bright desk sliver below elbow. Hidden surfaces approximate.","Pen angle follows connected rig; no independent head motion. Existing ink and shadow sequences reused.","No source overlay or corrective sleeve patch. Native rig render is a separate scene retained in integrated master, VSE uses rendered foreground; rerender after rig edits. External sequences must be retained.","No native ComfyUI invocation in this pass; bounded source sampling used for temporary reveal plate; native Krita paper from MCI09A reused, unapproved.","Nib target error verifies projected rig landmark, not physical contact. Full playback author review pending."]}
(root/"animation_receipt.json").write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2),flush=True)
