from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image,ImageDraw
home=Path.home()/"Documents/NOUSCERA";root=home/"reviews/MCI10_connected_limb_v01"
r=json.loads((root/"rig_receipt.json").read_text())
board=Image.new("RGB",(1290,850),(24,24,24));d=ImageDraw.Draw(board)
for j,p in enumerate(r["poses"]):
 k=p["reference_frame"];im=Image.open(root/f"pose_{k:04d}.png").convert("RGBA")
 bg=Image.new("RGBA",im.size,(65,65,65,255));bg.alpha_composite(im)
 x=j*430+8;d.text((x,8),f"Native rig pose {k} | elbow shift {p['elbow_displacement_px']:.1f}px",fill="white")
 board.paste(bg.crop((20,420,650,1060)).convert("RGB").resize((399,405)),(x,30))
 board.paste(bg.crop((100,810,650,1060)).convert("RGB").resize((414,188)),(x,460))
 prev=Image.open(home/"reviews/MCI10_material_v01"/f"pose_{k:04d}.png").convert("RGB")
 board.paste(prev.crop((100,810,650,1060)).resize((414,188)),(x,655))
 p["render_sha256"]=hashlib.sha256((root/f"pose_{k:04d}.png").read_bytes()).hexdigest()
 p["isolated_render_alpha_area"]=float(np.array(im.getchannel("A")).sum()/255)
d.text((8,440),"Isolated articulated cuff and wrist | no background hiding the geometry",fill="white")
d.text((8,638),"Previous curved wrist reference (includes rejected background)",fill="white")
board.save(root/"connected_limb_review.png")
(root/"rig_receipt.json").write_text(json.dumps(r,indent=2))
print(json.dumps(r,indent=2))
