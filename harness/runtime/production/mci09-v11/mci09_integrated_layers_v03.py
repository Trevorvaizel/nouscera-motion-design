"""MCI09-B/C experimental layered animation. Source-derived cutouts; no readiness promotion."""
from pathlib import Path
import cv2,numpy as np,math,json,hashlib
from PIL import Image,ImageDraw
home=Path.home()/"Documents/NOUSCERA";out=home/"reviews/MCI09_integrated_v03";out.mkdir(exist_ok=False)
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
# Reconstruct the narrow shirt reveal behind the hand with nearby real garment texture.
# Sample above the old silhouette, not along its edge; avoid the old rigid pen and other cutouts.
garment=(hole>0)&(X>=225)&(Y>=840)&(Y<1010)&(af(paper)==0)
sx=X.copy();sy=Y-100
# Preserve dark shirt identity near the pen; sample from an adjacent column.
sx=np.where((X>420)&(X<515),X+52,X)
sy=np.where((X>420)&(X<515),Y-120,sy)
tex=cv2.remap(source,sx.astype(np.float32),sy.astype(np.float32),cv2.INTER_LINEAR)
# If a sampled pixel belongs to a moving entity, substitute a safe dark shirt swatch.
invalid=cv2.remap(hole,sx.astype(np.float32),sy.astype(np.float32),cv2.INTER_NEAREST)>0
fallback=cv2.remap(source,(355+np.mod(X,65)).astype(np.float32),(700+np.mod(Y,75)).astype(np.float32),cv2.INTER_LINEAR)
tex[invalid]=fallback[invalid]
plate[garment]=tex[garment]
# Native Krita notebook; replace only reconstructed region, not entire visible page.
paper_mask=af(paper)>0;repair=(af(patch)>0)&paper_mask
plate[repair|((hole>0)&paper_mask)]=paper[:,:,:3][repair|((hole>0)&paper_mask)]
Image.fromarray(plate).save(out/"stationary_plate.png")
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
 # Rigid hand follows the existing pen transform exactly. Forearm length is preserved by
 # letting the elbow slide along the forearm axis, then rotating the fixed-length segment.
 grip=tip+R@(grip0-start)
 wrist=tip+R@(wrist0-start)
 v=wrist-elbow0
 length=float(np.linalg.norm(wrist0-elbow0))
 elbow=wrist-v/np.linalg.norm(v)*length
 def rigid_inv(a,b,c,d):
  v=b-a;u=d-c
  theta=math.atan2(u[1],u[0])-math.atan2(v[1],v[0])
  cc,ss=math.cos(theta),math.sin(theta)
  dx=X-c[0];dy=Y-c[1]
  return a[0]+cc*dx+ss*dy,a[1]-ss*dx+cc*dy
 # Blend only in the cuff and wrist transition. Hand and most forearm use rigid transforms.
 hand_w=smooth((X-350)/65)*smooth((Y-810)/70)
 fore_w=smooth((Y-790)/105)*(1-hand_w)
 upper_w=1-hand_w-fore_w
 hm=(start[0]+co*(X-tip[0])+si*(Y-tip[1]),start[1]-si*(X-tip[0])+co*(Y-tip[1]))
 fm=rigid_inv(elbow0,wrist0,elbow,wrist)
 um=rigid_inv(shoulder,elbow0,shoulder,elbow)
 mx=hm[0]*hand_w+fm[0]*fore_w+um[0]*upper_w
 my=hm[1]*hand_w+fm[1]*fore_w+um[1]*upper_w
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
 # Analytic soft contact occlusion. No image-derived shadow or displaced page texture.
 # The stationary paper clips the light attenuation; only opacity changes.
 def ellipse(cx,cy,sx,sy,opacity):
  return opacity*np.exp(-.5*((X-cx)/sx)**2-.5*((Y-cy)/sy)**2)
 shift=grip-grip0
 sh=ellipse(370+shift[0]*.7,1018+shift[1]*.7,89,7.5,.24)
 sh+=ellipse(478+shift[0],1014+shift[1],48,5.5,.24)
 sh+=ellipse(554+shift[0],1007+shift[1],32,8,.10)
 sh=np.clip(sh,0,.42)
 sh*=smooth((X-240)/24)*smooth((628-X)/28)*paper_mask
 sh[sh<.004]=0
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
 records.append({"frame":i+1,"tip":tip.tolist(),"grip":grip.tolist(),"pen_angle":angle,"head_angle":ha,"protected_pixels":int(protected.sum()),"protected_changes":int(np.any(f[protected]!=source[protected],axis=1).sum()),"ink_pixels":int((ink>0).sum()),"arm_alpha_area":float(af(la).sum()),"forearm_length":float(np.linalg.norm(wrist-elbow)),"hand_rigid_scale":1.0})
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
receipt={"scene":"CP05","experiment":"MCI09 integrated v03","source_sha256":sha(sourcefile),"paper_sha256":sha(paperroot/"CP05_MCI09A_native_projection.png"),"reference_video_sha256":sha(home/"reviews/B0311L_S09_CP05_STABILIZED_MASKED_720x1280_33f_v01.mp4"),"reference_manual_samples":ref.tolist(),"displacement_scale":.62,"frames":48,"fps":24,"first_frame_exact":bool(np.array_equal(frames[0],source)),"max_protected_changes":max(r["protected_changes"] for r in records),"tracks":records,"creative_approval":False,"readiness":"blocked; experimental preview only","limitations":["Manually sampled approximate nib path, scaled for constrained reveal; no automatic contact validation","Nearby source garment texture and nearest-source edge extrapolation, not full hidden-surface reconstruction","Analytic soft contact shadow and rigid hand/forearm with blended sleeve transition; planar head nod; no validated gaze/cloth simulation","Source-lock initial still transitions to composed layers","Raster-generated per-frame layers, native Blender VSE composition to follow"]}
(out/"layer_receipt.json").write_text(json.dumps(receipt,indent=2));print("Layer sequences ready",len(frames),max(r["protected_changes"] for r in records),flush=True)
