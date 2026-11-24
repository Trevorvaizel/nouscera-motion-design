"""Still poses with independent material plate and divergence-free pinned forearm transform."""
from pathlib import Path
import numpy as np,cv2,math,json,hashlib,zipfile,io,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw
home=Path.home()/"Documents/NOUSCERA";root=home/"reviews/MCI10_material_v01"
prev=home/"reviews/MCI09_integrated_v03"
load=lambda p:np.array(Image.open(p).convert("RGBA"))
plate=load(root/"material_conditioning.png");pred=load(root/"garment_native_crop.png")
mask=np.array(Image.open(root/"garment_mask.png").convert("L"))>0
c=plate[690:1202,120:632];c[mask[690:1202,120:632]]=pred[mask[690:1202,120:632]]
Image.fromarray(plate).save(root/"material_plate.png")
arm=load(root/"forearm_cutout.png")
Y,X=np.indices(arm.shape[:2],dtype=np.float32)
tracks=json.loads((prev/"layer_receipt.json").read_text())["tracks"]
tips=np.array([r["tip"] for r in tracks]);ids=[1,int(np.argmax(tips[:,0]))+1,int(np.argmin(tips[:,0]))+1]
def win(x):
 q=np.clip((x-242)/170,0,1);return q*q*(3-2*q),6*q*(1-q)/170
def integrate(x,y,field,dt,n=8):
 for _ in range(n):
  a,b=field(x,y);c,d=field(x+dt*a/2,y+dt*b/2);e,f=field(x+dt*c/2,y+dt*d/2);g,h=field(x+dt*e,y+dt*f)
  x=x+dt*(a+2*c+2*e+g)/6;y=y+dt*(b+2*d+2*f+h)/6
 return x,y
def transform(t):
 # Local area-preserving flow, pinned at cuff. Distal hand follows same rigid transform as pen.
 tip=np.array(t["tip"]);theta=t["pen_angle"];start=np.array([607.,1000.])
 center=np.array([440.,950.]);cs,sn=math.cos(theta),math.sin(theta);R=np.array([[cs,-sn],[sn,cs]])
 delta=tip+R@(center-start)-center;cx,cy=center+delta
 def rotate(x,y):
  w,dw=win(x);rx=x-cx;ry=y-cy
  return -theta*ry*w,theta*rx*w+.5*theta*(rx*rx+ry*ry)*dw
 def translate(x,y):
  w,dw=win(x);psi=delta[0]*(y-950)-delta[1]*(x-327)
  return w*delta[0],w*delta[1]-dw*psi
 mx,my=integrate(X,Y,rotate,-1/8);mx,my=integrate(mx,my,translate,-1/8)
 al=arm[:,:,3].astype(np.float32)/255
 ma=cv2.remap(al,mx.astype(np.float32),my.astype(np.float32),cv2.INTER_LINEAR)
 pre=cv2.remap(arm[:,:,:3].astype(np.float32)*al[:,:,None],mx.astype(np.float32),my.astype(np.float32),cv2.INTER_LINEAR)
 a=np.dstack([np.uint8(np.clip(pre/np.maximum(ma[:,:,None],1e-6)+.5,0,255)),np.uint8(np.clip(ma*255+.5,0,255))])
 return a
board=Image.new("RGB",(1260,770),(24,24,24));d=ImageDraw.Draw(board);records=[]
def png(a):
 s=io.BytesIO();Image.fromarray(a).save(s,format="PNG");return s.getvalue()
for j,k in enumerate(ids):
 a=transform(tracks[k-1]);pen=load(prev/"pen"/f"{k:04d}.png");ink=load(prev/"ink"/f"{k:04d}.png");shadow=load(prev/"shadow"/f"{k:04d}.png")
 layers=[("05 Forearm and hand | pinned area-preserving flow",a),("04 Rigid pen",pen),("03 Independent contact shadow",shadow),("02 Inscription",ink),("01 Material-separated stationary body and environment",plate)]
 f=Image.fromarray(plate)
 for _,l in reversed(layers[:-1]):f.alpha_composite(Image.fromarray(l))
 f.save(root/f"pose_{k:04d}.png")
 d.text((j*420+8,6),f"Reference frame {k} | static ownership test",fill="white")
 board.paste(f.convert("RGB").resize((225,400)),(j*420+94,25));board.paste(f.crop((85,780,700,1100)).convert("RGB").resize((410,213)),(j*420+5,440))
 records.append({"reference_frame":k,"alpha_area":float(a[:,:,3].sum()/255),"tip":tracks[k-1]["tip"]})
 xml=ET.Element("image",{"w":"720","h":"1280","name":f"MCI10 material pose {k}","version":"0.0.3"});stack=ET.SubElement(xml,"stack")
 with zipfile.ZipFile(root/f"pose_{k:04d}.ora","w") as z:
  z.writestr("mimetype","image/openraster",compress_type=zipfile.ZIP_STORED)
  for i,(name,l) in enumerate(layers):
   path=f"data/layer{i}.png";z.writestr(path,png(l));ET.SubElement(stack,"layer",{"name":name,"src":path,"opacity":"1.0","visibility":"visible","composite-op":"svg:src-over","x":"0","y":"0"})
  z.writestr("stack.xml",ET.tostring(xml,encoding="utf-8",xml_declaration=True));z.writestr("mergedimage.png",png(np.array(f)))
areas=np.array([r["alpha_area"] for r in records])
pct=float(100*np.ptp(areas)/areas[0])
d.text((10,690),f"Projected forearm alpha-area variation across three poses: {pct:.3f}% (2D proxy only). No source overlay.",fill="white")
board.save(root/"material_pose_comparison.png")
(root/"pose_receipt.json").write_text(json.dumps({"poses":records,"projected_area_peak_to_peak_pct":pct,"no_source_overlay":True,"head_stationary":True,"creative_approval":False,"motion_generated":False,"status":"still candidate only"},indent=2))
print(json.dumps({"poses":records,"area_variation_pct":pct}),flush=True)
