from pathlib import Path
import numpy as np,json
from PIL import Image,ImageDraw
p=Path.home()/"Documents/NOUSCERA"
b=p/"reviews/MCI09_integrated_v03";v=p/"reviews/MCI09_integrated_v04";a=p/"harness-build/asset-gates/CP05-v01"
out=p/"reviews/MCI09_composite_diagnosis";out.mkdir(exist_ok=True)
def load(f):return Image.open(f).convert("RGBA")
def panel(img,crop):
 im=img.crop(crop);bg=Image.new("RGBA",im.size,(55,55,55,255));bg.alpha_composite(im);return bg.convert("RGB")
source=load(p/"assets/NOUSCERA_Film001_CP05_ARTWORK_ONLY.png")
plate=load(b/"stationary_plate.png")
for name,crop,entity,frame in [("head",(280,95,660,640),"head",24),("sleeve",(30,420,325,1030),"limb",48),("hand",(285,790,700,1100),"limb",48)]:
 original=load(a/("head.png" if entity=="head" else "writing_limb.png"))
 moved=load(b/entity/f"{frame:04d}.png")
 lock=load(b/"source_lock"/f"{frame:04d}.png")
 result=load(b/"native_render"/f"frame_{frame:04d}.png")
 new=load(v/"native_render"/f"frame_{frame:04d}.png")
 origalpha=np.array(original)[:,:,3]
 movealpha=np.array(moved)[:,:,3]
 reveal=(origalpha>127)&(movealpha<127)
 rev=source.copy();red=np.zeros_like(np.array(source));red[:,:,:3]=(255,40,40);red[:,:,3]=reveal.astype(np.uint8)*200
 rev.alpha_composite(Image.fromarray(red))
 items=[("Original",source),("Stationary plate alone",plate),("Original cutout",original),("Moved cutout",moved),("Original-source preservation matte",lock),("Revealed original footprint",rev),("V11 composite",result),("V12 composite",new)]
 board=Image.new("RGB",(1200,900),(24,24,24));d=ImageDraw.Draw(board)
 for i,(label,img) in enumerate(items):
  x=(i%4)*300;y=(i//4)*450
  z=panel(img,crop);z.thumbnail((290,420));board.paste(z,(x+(300-z.width)//2,y+22));d.text((x+5,y+5),label,fill="white")
 board.save(out/(name+".jpg"),quality=94)
print("Diagnostic layer boards created; no source edits")
