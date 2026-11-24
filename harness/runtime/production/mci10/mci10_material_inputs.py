"""Material-specific preparation: bounded garment mask, independent desk and notebook."""
from pathlib import Path
import hashlib,json,cv2,numpy as np
from PIL import Image,ImageDraw
home=Path.home()/"Documents/NOUSCERA"
out=home/"reviews/MCI10_material_v01";out.mkdir(exist_ok=False)
inp=Path.home()/"Downloads/Compressed/ComfyUI_windows_portable_nvidia/ComfyUI_windows_portable/ComfyUI/input/NOUSCERA"
src=home/"assets/NOUSCERA_Film001_CP05_ARTWORK_ONLY.png"
assert hashlib.sha256(src.read_bytes()).hexdigest()=="354c4d5d7bba985a9ad9f009d7a3f9ded58e161ca0a51f13362fe7f9373d11e5"
source=np.array(Image.open(src).convert("RGB"));h,w=source.shape[:2];Y,X=np.indices((h,w),dtype=np.float32)
load=lambda p:np.array(Image.open(p).convert("RGBA"))
prior=home/"reviews/MCI10_scene_ownership_v02"
arm=load(prior/"forearm_cutout.png");pen=load(home/"harness-build/asset-gates/CP05-v01/rigid_pen.png")
paperroot=Path.home()/"Documents/Krita MCP/NOUSCERA_Film001/MCI09A_Paper_v03"
paper=load(paperroot/"CP05_MCI09A_native_projection.png");patch=load(paperroot/"paper_reconstruction_patch.png")
rem=np.array(Image.open(prior/"removal_mask.png").convert("L"))>0
# Inferred tabletop back edge extends the visible boundary at right; paper ownership takes precedence.
edge=1030-.14*(X-40)
paperzone=(paper[:,:,3]>0)&(rem|(patch[:,:,3]>0))
desk=rem&~paperzone&(Y>=edge)
shirt=rem&~paperzone&~desk
# Remove garment and desk skin traces from conditioning canvas. Only shirt is presented to MAT as missing.
# Desk sampling uses visible wood grain parallel to projected tabletop lines.
sx=(640+np.mod(X-640,63)).astype(np.float32)
sy=(944+np.mod(Y-edge,11)).astype(np.float32)
wood=cv2.remap(source,sx,sy,cv2.INTER_LINEAR)
plate=source.copy();plate[desk]=wood[desk];plate[paperzone]=paper[:,:,:3][paperzone]
# Replace old foreground color in mask, so model cannot condition on original skin inside mask.
plate[shirt]=0
crop=(120,690,632,1202)
assert np.where(shirt)[1].min()>=120 and np.where(shirt)[1].max()<632
Image.fromarray(plate).save(out/"material_conditioning.png")
Image.fromarray(plate).crop(crop).save(inp/"MCI10_material_garment_source_v01.png")
Image.fromarray(shirt.astype(np.uint8)*255).crop(crop).save(inp/"MCI10_material_garment_mask_v01.png")
for n,m in [("garment",shirt),("desk",desk),("paper",paperzone),("moving_footprint",rem)]:
 Image.fromarray(m.astype(np.uint8)*255).save(out/(n+"_mask.png"))
Image.fromarray(arm).save(out/"forearm_cutout.png")
overlay=source.copy()
for m,c in [(shirt,(145,90,210)),(desk,(40,160,230)),(paperzone,(230,190,60))]:overlay[m]=(overlay[m].astype(float)*.3+np.array(c)*.7).astype(np.uint8)
Image.fromarray(overlay).save(out/"material_ownership_map.png")
files=[inp/"MCI10_material_garment_source_v01.png",inp/"MCI10_material_garment_mask_v01.png"]
r={"crop":crop,"source_sha256":hashlib.sha256(src.read_bytes()).hexdigest(),"input_sha256":{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files},"garment_pixels":int(shirt.sum()),"desk_pixels":int(desk.sum()),"paper_pixels":int(paperzone.sum()),"overlap_pixels":int(((shirt.astype(int)+desk+paperzone)>1).sum()),"unassigned_removal_pixels":int((rem&~(shirt|desk|paperzone)).sum()),"tabletop_edge":"inferred from visible right edge; approximate","desk_method":"source wood-grain samples, not generative","paper_method":"native Krita MCI09A v03"}
(out/"material_inputs_receipt.json").write_text(json.dumps(r,indent=2));print(json.dumps(r),flush=True)
