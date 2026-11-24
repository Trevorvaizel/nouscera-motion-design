"""MCI09-B/C experimental layered animation. Source-derived cutouts; no readiness promotion."""
from pathlib import Path
import cv2,numpy as np,math,json,hashlib
from PIL import Image,ImageDraw
home=Path.home()/"Documents/NOUSCERA";out=home/"reviews/MCI09_integrated_v01";out.mkdir(exist_ok=False)
assets=home/"harness-build/asset-gates/CP05-v01"
paperroot=Path.home()/"Documents/Krita MCP/NOUSCERA_Film001/MCI09A_Paper_v03"
sourcefile=home/"assets/NOUSCERA_Film001_CP05_ARTWORK_ONLY.png"
source=np.array(Image.open(sourcefile).convert("RGB"));h,w=source.shape[:2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(sourcefile)=="354c4d5d7bba985a9ad9f009d7a3f9ded58e161ca0a51f13362fe7f9373d11e5"
def load(p):return np.array(Image.open(p).convert("RGBA"))
arm=load(assets/"writing_limb.png");pen=load(assets/"rigid_pen.png");head=load(assets/"head.png")
paper=load(paperroot/"CP05_MCI09A_native_projection.png");patch=load(paperroot/"paper_reconstruction_patch.png")
assert sha(paperroot/"CP05_MCI09A_paper_v03.kra")=="c8b6878cf65bb716b8af3e1866707ccbc6a06219e383f41fa2661ffc883cbc9f"
Y,X=np.indices((h,w),dtype=np.float32)
def af(a):return a[:,:,3].astype(np.float32)/255
def smooth(a):a=np.clip(a,0,1);return a*a*(3-2*a)
def rgba(rgb,alpha):return np.dstack([np.uint8(np.clip(rgb+.5,0,255)),np.uint8(np.clip(alpha*255+.5,0,255))])
def blend(base,layer):
 a=af(layer)[:,:,None];return base*(1-a)+layer[:,:,:3]*a
def warp(a,mx,my):
 al=af(a);ma=cv2.remap(al,mx.astype(np.float32),my.astype(np.float32),cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
 pre=cv2.remap(a[:,:,:3].astype(np.float32)*al[:,:,None],mx.astype(np.float32),my.astype(np.float32),cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
 return rgba(pre/np.maximum(ma[:,:,None],1e-6),ma)
moving=np.maximum.reduce([af(arm),af(head),af(pen)])
hole=cv2.dilate(np.uint8(moving>.01),np.ones((3,3),np.uint8))
# Nearest clean source for narrow reveals, with local ink texture. Only edges are visible in this constrained motion.
_,labels=cv2.distanceTransformWithLabels(hole,cv2.DIST_L2,5,labelType=cv2.DIST_LABEL_PIXEL)
valid=np.where(hole==0)
lookup=np.zeros((int(labels.max())+1,3),np.uint8);lookup[labels[valid]]=source[valid]
near=lookup[labels]
plate=source.copy();plate[hole>0]=near[hole>0]
# Independently reconstruct shirt behind the visible upper pen fragment with adjacent same-garment texture.
shirt=(af(pen)>.01)&(Y<900)
sample=cv2.remap(source,(X+36).astype(np.float32),(Y-19).astype(np.float32),cv2.INTER_LINEAR)
plate[shirt]=sample[shirt]
# Native Krita notebook; replace only reconstructed region, not entire visible page.
paper_mask=af(paper)>0;repair=(af(patch)>0)&paper_mask
plate[repair|((hole>0)&paper_mask)]=paper[:,:,:3][repair|((hole>0)&paper_mask)]
Image.fromarray(plate).save(out/"stationary_plate.png")
# Preserve source-baked shadow as independent estimate, translated with hand.
base_lum=cv2.cvtColor(plate,cv2.COLOR_RGB2GRAY).astype(np.float32)
src_lum=cv2.cvtColor(source,cv2.COLOR_RGB2GRAY).astype(np.float32)
shadow0=np.clip((base_lum-src_lum)/np.maximum(base_lum,1),0,.78)
shadow0*=paper_mask*(1-moving)*smooth((Y-982)/10)*smooth((X-245)/15)*smooth((625-X)/15)
# Source reference manually sampled from nine actual decoded frames; truncate before tip leaves crop.
ref=np.array([[0,600,1007],[4,624,998],[8,618,1000],[12,601,1015],[16,600,1016],[20,588,1026],[24,573,1029],[28,565,1023]],np.float32)
# Limit reach to 62% of observed displacement; relative start aligned to protected illustration.
ref_delta=(ref[:,1:]-ref[0,1:])*.62
start=np.array([607.,1000.]);grip0=np.array([528.,936.]);wrist0=np.array([389.,951.]);elbow0=np.array([122.,956.]);shoulder=np.array([139.,505.])
def inverse(a,b,c,d):
 v=b-a;u=d-c;den=float(np.dot(u,u));co=float(np.dot(v,u))/den;si=float(u[0]*v[1]-u[1]*v[0])/den
 dx=X-c[0];dy=Y-c[1];return a[0]+co*dx-si*dy,a[1]+si*dx+co*dy
wh=smooth((X-315)/105)*smooth((Y-810)/75);wf=smooth((Y-795)/100)*(1-wh);wu=1-wh-wf
trace=[];records=[];frames=[]
for name in ["ink","shadow","head","pen","limb","source_lock","preview"]: (out/name).mkdir()
for i in range(48):
 # 8-frame still, 32-frame action, 8-frame hold.
 t=np.clip((i-7)/32,0,1);q=t*28
 delta=np.array([np.interp(q,ref[:,0],ref_delta[:,j]) for j in [0,1]],np.float32)
 tip=start+delta;angle=math.radians(1.5)*math.sin(t*math.pi*1.4)
 co,si=math.cos(angle),math.sin(angle);R=np.array([[co,-si],[si,co]])
 grip=tip+R@(grip0-start);wrist=wrist0+(grip-grip0)*.72;elbow=elbow0+delta*.07
 mx=np.zeros_like(X);my=np.zeros_like(Y)
 for a,b,c,d,weight in [(shoulder,elbow0,shoulder,elbow,wu),(elbow0,wrist0,elbow,wrist,wf),(wrist0,start,wrist,tip,wh)]:
  a1,b1=inverse(a,b,c,d);mx+=a1*weight;my+=b1*weight
 la=warp(arm,mx,my)
 dx=X-tip[0];dy=Y-tip[1];pa=warp(pen,start[0]+co*dx+si*dy,start[1]-si*dx+co*dy)
 # Restrained nod about chin support; gaze stays on notebook (not a validated gaze rig).
 ha=-math.radians(.5)*math.sin(math.pi*np.clip((i-4)/34,0,1));hc,hs=math.cos(ha),math.sin(ha);dx=X-520;dy=Y-482
 hea=warp(head,520+hc*dx+hs*dy,482-hs*dx+hc*dy)
 # Separate progressive ink deposited only during chosen contact period.
 ink=np.zeros((h,w),np.uint8)
 if 7<i<=39:trace.append(tip.tolist())
 if len(trace)>1:cv2.polylines(ink,[np.rint(np.array(trace)*16).astype(np.int32)],False,215,1,cv2.LINE_AA,shift=4)
 ink=np.uint8(ink*paper_mask);ia=rgba(np.full_like(source,12),ink.astype(np.float32)/255)
 # Keep existing contact-shadow shape separate; add gentle occlusion under moved fingers.
 sh=cv2.remap(shadow0,(X-delta[0]*.8).astype(np.float32),(Y-delta[1]*.8).astype(np.float32),cv2.INTER_LINEAR)
 occ=cv2.GaussianBlur(af(la),(0,0),4);occ=cv2.remap(occ,X,Y-4,cv2.INTER_LINEAR)
 zone=paper_mask*smooth((Y-986)/12)*smooth((X-248)/14)*smooth((623-X)/18)
 sh=np.maximum(sh,np.clip(occ*zone*.39,0,.45));sh*=paper_mask
 sa=rgba(np.zeros_like(source),sh)
 # Preserve exact source wherever no dynamic entity, paper repair or shadow may affect the image.
 support=(moving>0)|(af(hea)>0)|(af(pa)>0)|(af(la)>0)|(af(ia)>0)|(af(sa)>0)|repair
 lock=rgba(source,(~support).astype(np.float32))
 if i<=7:lock=rgba(source,np.ones((h,w),np.float32))
 composed=plate.astype(np.float32)
 for n,a in [("ink",ia),("shadow",sa),("head",hea),("pen",pa),("limb",la),("source_lock",lock)]:
  Image.fromarray(a).save(out/n/f"{i+1:04d}.png",compress_level=2)
  composed=blend(composed,a)
 f=np.uint8(np.clip(composed+.5,0,255));frames.append(f)
 Image.fromarray(f).save(out/"preview"/f"{i+1:04d}.png",compress_level=2)
 protected=~support
 records.append({"frame":i+1,"tip":tip.tolist(),"grip":grip.tolist(),"pen_angle":angle,"head_angle":ha,"protected_pixels":int(protected.sum()),"protected_changes":int(np.any(f[protected]!=source[protected],axis=1).sum()),"ink_pixels":int((ink>0).sum())})
# Evidence sheets for judgment, not automatic creative approval.
board=Image.new("RGB",(1200,550),(20,20,20));d=ImageDraw.Draw(board)
for j,k in enumerate([0,12,20,28,38,47]):
 im=Image.fromarray(frames[k]).resize((180,320));board.paste(im,(j*200+10,24));d.text((j*200+10,5),f"F{k+1:02d}",fill="white")
 im=Image.fromarray(frames[k]).crop((330,850,680,1090)).resize((190,130));board.paste(im,(j*200+5,375))
board.save(out/"integrated_contact.png")
# Compare plate reveal separately.
sheet=Image.new("RGB",(1080,600),(24,24,24));ds=ImageDraw.Draw(sheet)
for j,(a,label) in enumerate([(source,"Original"),(plate,"Experimental hidden-surface plate"),(frames[38],"Integrated sampled frame")]):
 im=Image.fromarray(a).resize((315,560));sheet.paste(im,(j*360+20,28));ds.text((j*360+20,5),label,fill="white")
sheet.save(out/"surface_reveal_review.png")
receipt={"scene":"CP05","experiment":"MCI09 integrated v01","source_sha256":sha(sourcefile),"paper_sha256":sha(paperroot/"CP05_MCI09A_native_projection.png"),"reference_video_sha256":sha(home/"reviews/B0311L_S09_CP05_STABILIZED_MASKED_720x1280_33f_v01.mp4"),"reference_manual_samples":ref.tolist(),"displacement_scale":.62,"frames":48,"fps":24,"first_frame_exact":bool(np.array_equal(frames[0],source)),"max_protected_changes":max(r["protected_changes"] for r in records),"tracks":records,"creative_approval":False,"readiness":"blocked; experimental preview only","limitations":["Manually sampled approximate nib path, scaled for constrained reveal; no automatic contact validation","Nearest-source edge extrapolation and approximate shirt sample, not full hidden-surface reconstruction","Independent estimated shadow and planar head nod; no validated gaze/cloth simulation","Source-lock initial still transitions to composed layers","Raster-generated per-frame layers, native Blender VSE composition to follow"]}
(out/"layer_receipt.json").write_text(json.dumps(receipt,indent=2));print("Layer sequences ready",len(frames),max(r["protected_changes"] for r in records),flush=True)
