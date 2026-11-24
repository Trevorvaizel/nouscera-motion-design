"""MCI10 diagnostic: rigid forearm with physically occluding cuff opening."""
from pathlib import Path
import json,math,io,zipfile,xml.etree.ElementTree as ET,hashlib
import numpy as np,cv2
from PIL import Image,ImageDraw
home=Path.home()/"Documents/NOUSCERA";base=home/"reviews/MCI10_material_v01";prev=home/"reviews/MCI09_integrated_v03"
out=home/"reviews/MCI10_wrist_v02";out.mkdir(exist_ok=False)
load=lambda p:np.array(Image.open(p).convert("RGBA"))
source=load(home/"assets/NOUSCERA_Film001_CP05_ARTWORK_ONLY.png")
plate=load(base/"material_plate.png");arm=load(base/"forearm_cutout.png")
Y,X=np.indices(arm.shape[:2],dtype=np.float32)
# Trace skin's upper boundary from source grid. Remove the stray cuff spike.
top=np.interp(X,[0,145,160,180,200,225,245,275,310,350,380,400],[925,925,916,905,898,896,898,900,901,901,893,880])
clean=(X<385)&(Y<top-1)
arm[clean,3]=0
# Extend proximal skin only beneath actual cuff opening, using nearby source skin.
# This provides overlap for the 22px slide without stretching wrist anatomy.
extend=(X>=104)&(X<185)&(Y>=932)&(Y<=1002)
sample=cv2.remap(arm,(X+70).astype(np.float32),Y,cv2.INTER_LINEAR)
ext=np.where(extend,sample[:,:,3],0).astype(np.uint8)
take=ext>arm[:,:,3]
arm[take]=sample[take];arm[take,3]=ext[take]
# Stationary cuff has its own ownership, explicitly removed from the base where opaque.
# Trace actual cloth/skin border, not a full-image repair matte.
edge=np.interp(Y,[845,870,888,895,905,920,940,960,980,1000,1015,1030],[254,258,249,230,198,177,163,153,148,149,163,183])
roi=(Y>=845)&(Y<=1030)&(X>=65)&(X<=edge)
alpha=np.uint8(np.clip((edge-X+0.5)*255,0,255))*roi
cuff=np.dstack([source[:,:,:3],alpha])
plate[alpha==255,3]=0
# Transparent hole is owned by cuff, which remains above rigid forearm in compositing.
Image.fromarray(arm).save(out/"rigid_forearm_asset.png")
Image.fromarray(cuff).save(out/"stationary_cuff_asset.png")
Image.fromarray(plate).save(out/"diagnostic_plate_without_cuff.png")
tracks=json.loads((prev/"layer_receipt.json").read_text())["tracks"]
tips=np.array([r["tip"] for r in tracks]);ids=[1,int(np.argmax(tips[:,0]))+1,int(np.argmin(tips[:,0]))+1]
def warp(a,mx,my):
 al=a[:,:,3].astype(np.float32)/255
 ma=cv2.remap(al,mx.astype(np.float32),my.astype(np.float32),cv2.INTER_LINEAR)
 pre=cv2.remap(a[:,:,:3].astype(np.float32)*al[:,:,None],mx.astype(np.float32),my.astype(np.float32),cv2.INTER_LINEAR)
 return np.dstack([np.uint8(np.clip(pre/np.maximum(ma[:,:,None],1e-6)+.5,0,255)),np.uint8(np.clip(ma*255+.5,0,255))])
def png(a):
 f=io.BytesIO();Image.fromarray(a).save(f,format="PNG");return f.getvalue()
board=Image.new("RGB",(1320,800),(24,24,24));d=ImageDraw.Draw(board);records=[]
for j,k in enumerate(ids):
 t=tracks[k-1];tip=np.array(t["tip"]);theta=t["pen_angle"];co,si=math.cos(theta),math.sin(theta)
 dx=X-tip[0];dy=Y-tip[1];a=warp(arm,607+co*dx+si*dy,1000-si*dx+co*dy)
 pen=load(prev/"pen"/f"{k:04d}.png");ink=load(prev/"ink"/f"{k:04d}.png");shadow=load(prev/"shadow"/f"{k:04d}.png")
 layers=[("06 Stationary cuff | actual occluder",cuff),("05 Rigid forearm and hand",a),("04 Rigid pen",pen),("03 Independent contact shadow",shadow),("02 Inscription",ink),("01 Diagnostic plate | rejected, cuff ownership removed",plate)]
 f=Image.fromarray(plate)
 for _,l in reversed(layers[:-1]):f.alpha_composite(Image.fromarray(l))
 f.save(out/f"pose_{k:04d}.png")
 x=j*440+10;crop=(100,820,675,1050)
 for row,im,label in [(0,Image.open(base/f"pose_{k:04d}.png"),"Previous curved wrist"),(1,f,"Rigid arm under stationary cuff")]:
  y=20+row*230;d.text((x,y),f"F{k} | {label}",fill="white");board.paste(im.crop(crop).convert("RGB").resize((420,168)),(x,y+22))
 iso=Image.new("RGBA",(720,1280),(64,64,64,255));iso.alpha_composite(Image.fromarray(a));iso.alpha_composite(Image.fromarray(cuff))
 d.text((x,480),f"F{k} | isolated cuff + arm",fill="white");board.paste(iso.crop(crop).convert("RGB").resize((420,168)),(x,504))
 records.append({"reference_frame":k,"underlying_arm_alpha_area":float(a[:,:,3].sum()/255),"visible_arm_alpha_area":float((a[:,:,3].astype(float)/255*(1-alpha.astype(float)/255)).sum()),"tip":t["tip"],"rigid_scale":1.0})
 xml=ET.Element("image",{"w":"720","h":"1280","name":f"MCI10 rigid cuff pose {k}","version":"0.0.3"});stack=ET.SubElement(xml,"stack")
 with zipfile.ZipFile(out/f"pose_{k:04d}.ora","w") as z:
  z.writestr("mimetype","image/openraster",compress_type=zipfile.ZIP_STORED)
  for i,(name,l) in enumerate(layers):
   path=f"data/layer{i}.png";z.writestr(path,png(l));ET.SubElement(stack,"layer",{"name":name,"src":path,"opacity":"1.0","visibility":"visible","composite-op":"svg:src-over","x":"0","y":"0"})
  z.writestr("stack.xml",ET.tostring(xml,encoding="utf-8",xml_declaration=True));z.writestr("mergedimage.png",png(np.array(f)))
a=[r["underlying_arm_alpha_area"] for r in records];v=[r["visible_arm_alpha_area"] for r in records]
r={"poses":records,"underlying_rigid_area_range_pct":100*(max(a)-min(a))/a[0],"visible_area_range_pct":100*(max(v)-min(v))/v[0],"creative_approval":False,"motion_generated":False,"limitations":["Cuff boundary traced from visible source; proximal skin extension sampled, not recovered","Previous rejected garment plate retained; no new plate approval","Rigid planar slide is a diagnostic approximation, not an articulated 3D arm"]}
d.text((10,720),"Rigid hand and forearm share pen transform; cuff is a separate physical occluder, not a repair overlay.",fill="white")
d.text((10,745),"Original rejected plate retained for geometry test only. No animation.",fill="white")
board.save(out/"wrist_cuff_comparison.png");(out/"wrist_receipt.json").write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
