"""Still-only ownership test: no source overlay, no head cutout, no sleeve patch."""
from pathlib import Path
import json,hashlib,math,io,zipfile,xml.etree.ElementTree as ET
import numpy as np,cv2
from PIL import Image,ImageDraw
home=Path.home()/"Documents/NOUSCERA";root=home/"reviews/MCI10_scene_ownership_v02"
prev=home/"reviews/MCI09_integrated_v03"
source=np.array(Image.open(home/"assets/NOUSCERA_Film001_CP05_ARTWORK_ONLY.png").convert("RGB"))
def load(p):return np.array(Image.open(p).convert("RGBA"))
plate=load(root/"clean_plate_candidate.png");arm=load(root/"forearm_cutout.png")
Y,X=np.indices(source.shape[:2],dtype=np.float32)
def smooth(x):x=np.clip(x,0,1);return x*x*(3-2*x)
def move(a,mx,my):
 al=a[:,:,3].astype(np.float32)/255
 ma=cv2.remap(al,mx.astype(np.float32),my.astype(np.float32),cv2.INTER_LINEAR)
 pre=cv2.remap(a[:,:,:3].astype(np.float32)*al[:,:,None],mx.astype(np.float32),my.astype(np.float32),cv2.INTER_LINEAR)
 return np.dstack([np.uint8(np.clip(pre/np.maximum(ma[:,:,None],1e-6)+.5,0,255)),np.uint8(np.clip(ma*255+.5,0,255))])
tracks=json.loads((prev/"layer_receipt.json").read_text())["tracks"]
tips=np.array([r["tip"] for r in tracks])
ids=[1,int(np.argmax(tips[:,0]))+1,int(np.argmin(tips[:,0]))+1]
results=[]
def png(a):
 s=io.BytesIO();Image.fromarray(a).save(s,format="PNG");return s.getvalue()
board=Image.new("RGB",(1260,820),(24,24,24));d=ImageDraw.Draw(board)
for j,k in enumerate(ids):
 t=tracks[k-1];tip=np.array(t["tip"]);angle=t["pen_angle"];co,si=math.cos(angle),math.sin(angle)
 start=np.array([607.,1000.]);dx=X-tip[0];dy=Y-tip[1]
 mx=start[0]+co*dx+si*dy;my=start[1]-si*dx+co*dy
 weight=smooth((X-242)/132)
 a=move(arm,X+(mx-X)*weight,Y+(my-Y)*weight)
 pen=load(prev/"pen"/f"{k:04d}.png");ink=load(prev/"ink"/f"{k:04d}.png");shadow=load(prev/"shadow"/f"{k:04d}.png")
 layers=[("05 Forearm and hand",a),("04 Rigid pen",pen),("03 Contact attenuation",shadow),("02 Inscription",ink),("01 Stationary body and environment",plate)]
 f=Image.fromarray(plate)
 for _,l in reversed(layers[:-1]):f.alpha_composite(Image.fromarray(l))
 f.save(root/f"pose_{k:04d}.png")
 d.text((j*420+10,8),f"Reference frame {k} | still test, no overlay",fill="white")
 board.paste(f.convert("RGB").resize((225,400)),(j*420+92,30))
 board.paste(f.crop((85,780,700,1100)).convert("RGB").resize((410,213)),(j*420+5,450))
 diff=np.abs(np.array(f.convert("RGB")).astype(float)-source)
 results.append({"reference_frame":k,"tip":t["tip"],"source_mae":float(diff.mean()),"forearm_area":float(a[:,:,3].sum()/255)})
 xml=ET.Element("image",{"w":"720","h":"1280","name":f"MCI10 ownership pose {k}","version":"0.0.3"})
 stack=ET.SubElement(xml,"stack")
 with zipfile.ZipFile(root/f"pose_{k:04d}.ora","w") as z:
  z.writestr("mimetype","image/openraster",compress_type=zipfile.ZIP_STORED)
  for i,(name,l) in enumerate(layers):
   path=f"data/layer{i}.png";z.writestr(path,png(l));ET.SubElement(stack,"layer",{"name":name,"src":path,"opacity":"1.0","visibility":"visible","composite-op":"svg:src-over","x":"0","y":"0"})
  z.writestr("stack.xml",ET.tostring(xml,encoding="utf-8",xml_declaration=True));z.writestr("mergedimage.png",png(np.array(f)))
d.text((10,700),"Stationary head / neck / support hand / upper sleeve. Distal forearm follows existing pen track.",fill="white")
d.text((10,725),"No full-image preservation matte or V12 seam overlay. Inpainted surfaces still approximate.",fill="white")
board.save(root/"pose_comparison.png")
(root/"pose_receipt.json").write_text(json.dumps({"poses":results,"no_source_overlay":True,"head_stationary":True,"status":"visual review required","creative_approval":False},indent=2))
print(json.dumps(results),flush=True)
