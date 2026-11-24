"""MCI09-A: source-derived stationary paper candidate. No animation; editable native handoff."""
from pathlib import Path
import cv2,numpy as np,hashlib,json,zipfile,io,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw
home=Path.home()/"Documents/NOUSCERA"
root=Path.home()/"Documents/Krita MCP/NOUSCERA_Film001/MCI09A_Paper_v02"
root.mkdir(parents=True,exist_ok=True)
src=home/"assets/NOUSCERA_Film001_CP05_ARTWORK_ONLY.png"
source=np.array(Image.open(src).convert("RGB"));h,w=source.shape[:2]
assert hashlib.sha256(src.read_bytes()).hexdigest()=="354c4d5d7bba985a9ad9f009d7a3f9ded58e161ca0a51f13362fe7f9373d11e5"
assets=home/"harness-build/asset-gates/CP05-v01"
limb=np.array(Image.open(assets/"writing_limb.png").convert("RGBA"))
pen=np.array(Image.open(assets/"rigid_pen.png").convert("RGBA"))
old=np.array(Image.open(assets/"stationary_notebook.png").convert("RGBA"))
Y,X=np.indices((h,w),dtype=np.float32)
def polygon(points):
 m=np.zeros((h,w),np.uint8);cv2.fillPoly(m,[np.array(points,np.int32)],255);return m
# Inferred rear edge and traced visible book perimeter. Preserve the visible front page stack.
book=polygon([(246,1016),(311,1001),(405,979),(503,958),(578,958),(659,957),(679,965),(719,978),(719,1091),(700,1104),(668,1113),(609,1125),(548,1141),(478,1155),(438,1153),(389,1125),(340,1095),(291,1067),(236,1031)])
# Reuse the previously traced perimeter outside the rear edge; remove extra transparent non-book pixels.
original_alpha=old[:,:,3]
# Outer book lower silhouette is based on previous asset; new polygon only changes back/top edge.
rear=polygon([(245,1016),(312,1000),(405,979),(503,958),(578,958),(659,957),(679,965),(719,978),(719,1015),(245,1040)])
alpha=np.where(Y<1020, np.maximum(book*0, np.minimum(book,np.maximum(rear,original_alpha))),original_alpha).astype(np.uint8)
# Patch the obscured hand/pen area and the source-baked contact shadow. Keep existing written marks.
occluded=cv2.dilate(np.maximum(limb[:,:,3],pen[:,:,3]),np.ones((5,5),np.uint8))
shadow=polygon([(246,1017),(303,1008),(366,1000),(425,1000),(493,991),(541,986),(575,994),(609,1001),(594,1007),(552,1015),(509,1024),(456,1030),(398,1037),(335,1039),(283,1033),(246,1028)])
region=np.maximum(occluded,shadow)
# Remove all moving-object pixels within the inferred page, and fade the shadow repair into adjacent paper.
region=np.maximum(region,polygon([(247,1016),(312,1000),(405,979),(503,958),(579,958),(590,982),(609,1001),(573,1015),(505,1028),(424,1034),(333,1039),(280,1033),(247,1026)]))
soft=cv2.GaussianBlur(region,(0,0),5.0).astype(np.float32)/255
soft=np.maximum(soft,(occluded>20).astype(np.float32));soft*=alpha.astype(np.float32)/255
# Sample actual blank lower-left page, maintaining local perspective and hatch scale.
# No generative replacement, no blur of the entire illustration.
# Reflect source texture at its native pixel scale within wholly visible paper samples.
def reflected(t,lo,hi):
 n=hi-lo
 return (lo+n-np.abs(np.mod(t-lo,2*n)-n)).astype(np.float32)
lx=reflected(X+31,395,542)
ly=reflected(Y+78,1045,1074)
left=cv2.remap(source,lx,ly,cv2.INTER_LINEAR)
rx=reflected(X+17,620,646)
ry=reflected(Y+31,963,981)
right=cv2.remap(source,rx,ry,cv2.INTER_LINEAR)
def detail(rgb):
 g=cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY).astype(np.float32)
 return g-cv2.GaussianBlur(g,(0,0),5)
# The central crease continues diagonally from beneath the hand.
crease_y=980+(X-522)*.55
mix=np.clip((crease_y-Y+3)/12,0,1)
mix*=np.clip((X-510)/37,0,1)
left_tone=203+10*np.clip((X-280)/280,0,1)
right_tone=233
tone=np.clip((left_tone+detail(left))*(1-mix)+(right_tone+detail(right))*mix,0,255)
# Add a restrained narrow crease only inside reconstructed region; source crease preserved beyond it.
tone-=7*np.exp(-((Y-crease_y)/2.4)**2)*np.clip((X-520)/30,0,1)
fill=np.repeat(np.uint8(np.clip(tone,0,255))[:,:,None],3,axis=2)
patch=np.dstack([fill,np.uint8(np.round(soft*255))])
book_base=np.dstack([source,alpha])
def over(bottom,top):
 b=Image.fromarray(bottom,"RGBA");t=Image.fromarray(top,"RGBA");return np.array(Image.alpha_composite(b,t))
clean=over(book_base,patch)
# Force exact notebook alpha; the patch is clipped to its object extent.
clean[:,:,3]=alpha
# No hidden paper is claimed outside reconstructed notebook alpha.
reference=np.dstack([source,np.full((h,w),255,np.uint8)])
for n,a in [("notebook_visible_source",book_base),("paper_reconstruction_patch",patch),("stationary_notebook_candidate",clean),("writing_limb_reference",limb),("rigid_pen_reference",pen),("original_reference",reference)]:
 Image.fromarray(a).save(root/(n+".png"))
# OpenRaster editable layers. The original and moving components are initially hidden.
layers=[("05 Original artwork | protected reference",reference,False),("04 Writing limb | prior approximate mask",limb,False),("03 Rigid pen | prior approximate mask",pen,False),("02 Paper reconstruction | editable",patch,True),("01 Notebook | source pixels",book_base,True)]
def png(a):
 s=io.BytesIO();Image.fromarray(a).save(s,format="PNG");return s.getvalue()
ora=root/"CP05_MCI09A_paper_v02.ora"
xml=ET.Element("image",{"w":str(w),"h":str(h),"name":"CP05 | Paper reconstruction candidate","version":"0.0.3"})
stack=ET.SubElement(xml,"stack")
with zipfile.ZipFile(ora,"w") as z:
 z.writestr("mimetype","image/openraster",compress_type=zipfile.ZIP_STORED)
 for i,(name,a,visible) in enumerate(layers):
  f=f"data/layer{i}.png";z.writestr(f,png(a));ET.SubElement(stack,"layer",{"name":name,"src":f,"opacity":"1.0","visibility":"visible" if visible else "hidden","composite-op":"svg:src-over","x":"0","y":"0"})
 z.writestr("stack.xml",ET.tostring(xml,encoding="utf-8",xml_declaration=True));z.writestr("mergedimage.png",png(clean))
# Visual comparison: original, old notebook, candidate; identical scale.
crop=(220,850,720,1155);board=Image.new("RGB",(1040,700),(24,24,24));d=ImageDraw.Draw(board)
d.text((16,10),"MCI09-A | Notebook reconstruction | candidate, not approved",fill="white")
def panel(a,x,y,label):
 d.text((x,y),label,fill="white")
 im=Image.fromarray(a).convert("RGBA").crop(crop);bg=Image.new("RGBA",im.size,(50,50,50,255));bg.alpha_composite(im);board.paste(bg.convert("RGB"),(x,y+20))
panel(reference,16,35,"Original writing region")
panel(old,524,35,"Previous isolated notebook")
panel(clean,16,370,"Reconstructed stationary notebook")
panel(over(over(clean,pen),limb),524,370,"Prior limb and pen on reconstructed paper (shadow not reapplied)")
board.save(root/"MCI09A_paper_review_v02.png")
changed=np.any(clean[:,:,:3]!=source,axis=2)
receipt={"source_sha256":hashlib.sha256(src.read_bytes()).hexdigest(),"method":"Local source texture sampling and bounded patch; native layered document handoff","candidate_sha256":hashlib.sha256((root/"stationary_notebook_candidate.png").read_bytes()).hexdigest(),"changed_visible_notebook_pixels":int((changed&(alpha>0)).sum()),"changed_outside_patch_inside_book":int((changed&(alpha>0)&(patch[:,:,3]==0)).sum()),"candidate_only":True,"creative_approval":False,"hidden_surface_review":"pending","limitations":["Rear edge inferred behind hand, previous limb and pen masks approximate","Contact shadow removed from paper and not yet modeled separately","Other hidden surfaces untouched","Not a generative reconstruction or motion test"]}
(root/"paper_receipt.json").write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
