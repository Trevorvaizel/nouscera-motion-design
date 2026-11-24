"""Prepare a bounded diagnostic plate for the actual animated rig sweep."""
from pathlib import Path
import numpy as np,cv2,json,hashlib
from PIL import Image,ImageDraw
home=Path.home()/"Documents/NOUSCERA";out=home/"reviews/MCI11_integrated_v01"
src=home/"assets/NOUSCERA_Film001_CP05_ARTWORK_ONLY.png"
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(src)=="354c4d5d7bba985a9ad9f009d7a3f9ded58e161ca0a51f13362fe7f9373d11e5"
source=np.array(Image.open(src).convert("RGB"));h,w=source.shape[:2];Y,X=np.indices((h,w),dtype=np.float32)
load=lambda p:np.array(Image.open(p).convert("RGBA"))
assets=home/"harness-build/asset-gates/CP05-v01"
arm=load(assets/"writing_limb.png");pen=load(assets/"rigid_pen.png")
frames=sorted((out/"rig_frames").glob("*.png"));assert len(frames)==48
alpha=np.array([load(f)[:,:,3] for f in frames])
original=np.maximum(arm[:,:,3],pen[:,:,3])
rem=cv2.dilate((original>2).astype(np.uint8),np.ones((5,5),np.uint8))>0
sweep=rem&(alpha.min(axis=0)<248)
# Derive the real visible reveal rather than inpaint an entire limb-shaped mask.
Image.fromarray(sweep.astype(np.uint8)*255).save(out/"swept_reveal_mask.png")
Image.fromarray(rem.astype(np.uint8)*255).save(out/"original_moving_footprint.png")
paperroot=Path.home()/"Documents/Krita MCP/NOUSCERA_Film001/MCI09A_Paper_v03"
paper=load(paperroot/"CP05_MCI09A_native_projection.png");patch=load(paperroot/"paper_reconstruction_patch.png")
paperzone=(paper[:,:,3]>0)&(rem|(patch[:,:,3]>0))
# Source-derived reconstruction of the narrow left and right silhouette reveals.
# No nearest-pixel extrusion, no moving source copy in the plate.
plate=source.copy();material=np.zeros((h,w),np.uint8)
for y in range(h):
 xs=np.where(rem[y])[0]
 if not len(xs):continue
 # Split contiguous intervals so pen and sleeve don't share a boundary.
 for seg in np.split(xs,np.where(np.diff(xs)>1)[0]+1):
  a,b=int(seg[0]),int(seg[-1]);n=len(seg)
  for x in seg:
   if paperzone[y,x]:continue
   if y<850 and x<110 and (x-a)<(b-x):
    # Dark left silhouette/background; sample adjacent non-limb pixels.
    sx=max(0,a-3-(x-a));sy=y;material[y,x]=1
   elif y>=1030-.14*(x-40):
    # Desk, choose visible horizontal grain, not foreground.
    sx=650+(x%55);sy=945+(y%9);material[y,x]=2
   else:
    # Garment on right of sleeve and around pen, sample same row outside footprint.
    sx=min(w-1,b+4+min(b-x,38));sy=y;material[y,x]=3
    if y>=850:
     sx= min(414, 330+(x%68));sy=740+(y%53)
   if rem[sy,sx]:
    sx=min(w-1,max(0,b+4));sy=y
   if rem[sy,sx]:
    plate[y,x]=(0,0,0)
   else:plate[y,x]=source[sy,sx]
plate[paperzone]=paper[:,:,:3][paperzone];material[paperzone]=4
# Fill always-covered pixels from the same plate ownership; preserve external source exactly.
changed=np.any(plate!=source,axis=2)
assert not np.any(changed&~(rem|paperzone))
Image.fromarray(plate).save(out/"stationary_plate.png")
# Diagnostic source-only mask, not a full-image overlay.
board=Image.new("RGB",(1120,690),(24,24,24));d=ImageDraw.Draw(board)
for j,(n,im) in enumerate([("Original",source),("Stationary candidate",plate),("Swept reveal",np.repeat((sweep*255).astype(np.uint8)[:,:,None],3,axis=2))]):
 d.text((j*370+8,6),n,fill="white");board.paste(Image.fromarray(im).resize((360,640)),(j*370+8,26))
board.save(out/"plate_review.jpg",quality=92)
r={"source_sha256":sha(src),"plate_sha256":sha(out/"stationary_plate.png"),"original_footprint_pixels":int(rem.sum()),"swept_reveal_pixels":int(sweep.sum()),"changed_outside_repair":0,"material_pixels":{str(i):int((material==i).sum()) for i in range(1,5)},"method":"Actual native alpha sweep, source material samples and existing unapproved Krita paper candidate. No broad MAT and no original-image preservation overlay.","creative_approval":False,"plate_status":"approximate experimental plate; hidden materials inferred"}
(out/"plate_receipt.json").write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
