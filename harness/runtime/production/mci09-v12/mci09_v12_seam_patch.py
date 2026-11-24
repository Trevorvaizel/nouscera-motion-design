"""Local stationary garment seam repair. Preserve V11 primary layers."""
from pathlib import Path
import hashlib,json,numpy as np
from PIL import Image,ImageDraw
home=Path.home()/"Documents/NOUSCERA"
base=home/"reviews/MCI09_integrated_v03";out=home/"reviews/MCI09_integrated_v04";out.mkdir(exist_ok=False)
src=home/"assets/NOUSCERA_Film001_CP05_ARTWORK_ONLY.png"
assert hashlib.sha256(src.read_bytes()).hexdigest()=="354c4d5d7bba985a9ad9f009d7a3f9ded58e161ca0a51f13362fe7f9373d11e5"
im=np.array(Image.open(src).convert("RGB"));Y,X=np.indices(im.shape[:2],dtype=np.float32)
def smooth(x):x=np.clip(x,0,1);return x*x*(3-2*x)
# The red-marked original seam is ~x165-240, y570-820 on the 720x1280 source.
# Retain original texture in the exposed seam only; feather into the existing sleeve/torso.
alpha=smooth((X-170)/25)*smooth((260-X)/22)*smooth((Y-552)/35)*smooth((850-Y)/30)
patch=np.dstack([im,np.uint8(np.round(alpha*255))]);Image.fromarray(patch).save(out/"sleeve_seam_repair.png")
# Compare three exact native frames with the proposed local patch before Blender render.
board=Image.new("RGB",(1000,700),(24,24,24));d=ImageDraw.Draw(board)
for col,k in enumerate([13,29,48]):
 f=Image.open(base/"native_render"/f"frame_{k:04d}.png").convert("RGBA")
 fixed=Image.alpha_composite(f,Image.fromarray(patch))
 for row,a in enumerate([f,fixed]):
  x=col*330+8;y=row*340+10;d.text((x,y),f"V{11+row} frame {k}",fill="white")
  board.paste(a.crop((120,500,300,865)).resize((155,315)).convert("RGB"),(x+80,y+20))
board.save(out/"seam_preflight.png")
print("Local patch ready; source only, no synthesized texture",flush=True)
