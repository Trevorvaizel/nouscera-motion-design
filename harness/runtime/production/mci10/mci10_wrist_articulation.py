"""MCI10 wrist correction: rigid distal forearm/hand; limited proximal cuff transition.
Diagnostic only. Existing rejected material plate is held fixed to isolate geometry.
"""
from pathlib import Path
import math,json,hashlib,io,zipfile,xml.etree.ElementTree as ET
import numpy as np,cv2
from PIL import Image,ImageDraw
home=Path.home()/"Documents/NOUSCERA"
base=home/"reviews/MCI10_material_v01";prev=home/"reviews/MCI09_integrated_v03"
out=home/"reviews/MCI10_wrist_v01";out.mkdir(exist_ok=False)
load=lambda p:np.array(Image.open(p).convert("RGBA"))
plate=load(base/"material_plate.png");arm=load(base/"forearm_cutout.png")
Y,X=np.indices(arm.shape[:2],dtype=np.float32)
tracks=json.loads((prev/"layer_receipt.json").read_text())["tracks"]
tips=np.array([r["tip"] for r in tracks]);ids=[1,int(np.argmax(tips[:,0]))+1,int(np.argmin(tips[:,0]))+1]
def smooth(a):a=np.clip(a,0,1);return a*a*(3-2*a)
def transform(t):
 tip=np.array(t["tip"]);theta=t["pen_angle"];co,si=math.cos(theta),math.sin(theta)
 dx=X-tip[0];dy=Y-tip[1]
 rx=607+co*dx+si*dy;ry=1000-si*dx+co*dy
 # Keep cuff at rest on proximal side. All wrist, hand and distal forearm
 # share the same rotation and translation as pen, without compensating curvature.
 weight=smooth((X-205)/105)
 mx=X+(rx-X)*weight;my=Y+(ry-Y)*weight
 al=arm[:,:,3].astype(np.float32)/255
 ma=cv2.remap(al,mx.astype(np.float32),my.astype(np.float32),cv2.INTER_LINEAR)
 pre=cv2.remap(arm[:,:,:3].astype(np.float32)*al[:,:,None],mx.astype(np.float32),my.astype(np.float32),cv2.INTER_LINEAR)
 a=np.dstack([np.uint8(np.clip(pre/np.maximum(ma[:,:,None],1e-6)+.5,0,255)),np.uint8(np.clip(ma*255+.5,0,255))])
 # Audit the exact rigid domain and check Jacobian for folding in transition.
 ax=np.gradient(mx,axis=1);ay=np.gradient(mx,axis=0);bx=np.gradient(my,axis=1);by=np.gradient(my,axis=0)
 det=ax*by-ay*bx
 region=(ma>.5)&(X>=310)
 transition=(ma>.5)&(X>205)&(X<310)
 return a,{"rigid_domain_max_jacobian_error":float(np.abs(det[region]-1).max()),"transition_min_jacobian":float(det[transition].min()),"transition_max_jacobian":float(det[transition].max()),"projected_area":float(ma.sum())}
def png(a):
 f=io.BytesIO();Image.fromarray(a).save(f,format="PNG");return f.getvalue()
board=Image.new("RGB",(1320,830),(24,24,24));d=ImageDraw.Draw(board)
records=[]
for j,k in enumerate(ids):
 a,r=transform(tracks[k-1])
 pen=load(prev/"pen"/f"{k:04d}.png");ink=load(prev/"ink"/f"{k:04d}.png");shadow=load(prev/"shadow"/f"{k:04d}.png")
 layers=[("05 Forearm and hand | rigid distal, proximal cuff transition",a),("04 Rigid pen",pen),("03 Independent contact shadow",shadow),("02 Inscription",ink),("01 Diagnostic material plate | rejected, unchanged",plate)]
 f=Image.fromarray(plate)
 for _,l in reversed(layers[:-1]):f.alpha_composite(Image.fromarray(l))
 f.save(out/f"pose_{k:04d}.png")
 Image.fromarray(a).save(out/f"arm_{k:04d}.png")
 x=j*440+10;crop=(100,820,675,1050)
 for row,im,label in [(0,Image.open(base/f"pose_{k:04d}.png"),"Previous area-preserving flow"),(1,f,"New rigid distal pose")]:
  y=20+row*230;d.text((x,y),f"F{k} | {label}",fill="white")
  board.paste(im.crop(crop).convert("RGB").resize((420,168)),(x,y+22))
 # Isolated arm on neutral ground, so hidden plate does not influence judgment.
 iso=Image.new("RGBA",(720,1280),(64,64,64,255));iso.alpha_composite(Image.fromarray(a))
 d.text((x,480),f"F{k} | isolated arm",fill="white");board.paste(iso.crop(crop).convert("RGB").resize((420,168)),(x,504))
 r.update({"reference_frame":k,"tip":tracks[k-1]["tip"],"rigid_start_x":310,"cuff_transition_x":[205,310]});records.append(r)
 xml=ET.Element("image",{"w":"720","h":"1280","name":f"MCI10 wrist test {k}","version":"0.0.3"});stack=ET.SubElement(xml,"stack")
 with zipfile.ZipFile(out/f"pose_{k:04d}.ora","w") as z:
  z.writestr("mimetype","image/openraster",compress_type=zipfile.ZIP_STORED)
  for i,(name,l) in enumerate(layers):
   path=f"data/layer{i}.png";z.writestr(path,png(l));ET.SubElement(stack,"layer",{"name":name,"src":path,"opacity":"1.0","visibility":"visible","composite-op":"svg:src-over","x":"0","y":"0"})
  z.writestr("stack.xml",ET.tostring(xml,encoding="utf-8",xml_declaration=True));z.writestr("mergedimage.png",png(np.array(f)))
d.text((10,720),"Distal forearm and hand move rigidly with pen. Deformation confined to proximal cuff transition.",fill="white")
d.text((10,745),"Existing rejected hidden-surface plate retained for comparison only. No animation or approval.",fill="white")
board.save(out/"wrist_comparison.png")
area=[r["projected_area"] for r in records]
receipt={"experiment":"MCI10 wrist geometry isolation","poses":records,"projected_area_range_pct":100*(max(area)-min(area))/area[0],"pen_ink_shadow_plate_unchanged":True,"source_overlay":False,"plate_status":"previously rejected; diagnostic use only","creative_approval":False,"motion_generated":False}
(out/"wrist_receipt.json").write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
