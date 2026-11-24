from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image,ImageDraw
p=Path.home()/"Documents/NOUSCERA/reviews"
a=p/"MCI09_integrated_v02";b=p/"MCI09_integrated_v03"
sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
assert sha(a/"stationary_plate.png")==sha(b/"stationary_plate.png")
for layer in ["ink","pen","head"]:
 assert all(sha(a/layer/f"{i:04d}.png")==sha(b/layer/f"{i:04d}.png") for i in range(1,49)),layer
def area(root):
 return np.array([np.array(Image.open(root/"limb"/f"{i:04d}.png"))[:,:,3].sum()/255 for i in range(1,49)])
x,y=area(a),area(b)
def stats(v):return {"minimum_change_pct":float(100*(v.min()/v[0]-1)),"maximum_change_pct":float(100*(v.max()/v[0]-1)),"peak_to_peak_pct":float(100*np.ptp(v)/v[0])}
r=json.loads((b/"layer_receipt.json").read_text());length=np.array([t["forearm_length"] for t in r["tracks"]])
o={"unchanged_layers":["stationary_plate","pen","ink","head"],"v10_projected_arm_alpha_area":stats(x),"v11_projected_arm_alpha_area":stats(y),"forearm_length_range_px":float(np.ptp(length)),"hand_transform_scale":1.0,"note":"2D alpha area is a proxy for apparent mass, not physical 3D volume. Cuff blend remains deformable. Shadow analytic approximation.","creative_approval":False}
(b/"v11_comparison_receipt.json").write_text(json.dumps(o,indent=2))
board=Image.new("RGB",(1040,720),(25,25,25));d=ImageDraw.Draw(board)
for row,root in enumerate([a,b]):
 for col,k in enumerate([13,29,48]):
  f=Image.open(root/"native_render"/f"frame_{k:04d}.png").convert("RGB").crop((225,845,700,1080)).resize((335,166))
  xx=10+col*345;yy=20+row*230;d.text((xx,yy),f"V{10+row} frame {k}",fill="white");board.paste(f,(xx,yy+20))
for col,k in enumerate([13,29,48]):
 f=Image.open(b/"shadow"/f"{k:04d}.png").getchannel("A").crop((225,845,700,1080)).resize((335,166));xx=10+col*345;d.text((xx,480),f"V11 shadow alpha frame {k}",fill="white");board.paste(f.convert("RGB"),(xx,500))
board.save(b/"v11_correction_comparison.png");print(json.dumps(o,indent=2))
