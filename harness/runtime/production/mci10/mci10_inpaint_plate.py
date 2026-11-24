"""MCI10: reconstruct hidden writing-arm area using installed MAT model. Static head/upper body."""
from pathlib import Path
import sys, json,hashlib, numpy as np,cv2
from PIL import Image
import torch
from safetensors.torch import load_file
home=Path.home()/"Documents/NOUSCERA"
comfy=Path.home()/"Downloads/Compressed/ComfyUI_windows_portable_nvidia/ComfyUI_windows_portable/ComfyUI"
sys.path.insert(0,str(comfy/"custom_nodes/comfyui-inpaint-nodes"))
import mat
out=home/"reviews/MCI10_scene_ownership";out.mkdir(exist_ok=True)
src=home/"assets/NOUSCERA_Film001_CP05_ARTWORK_ONLY.png"
source=np.array(Image.open(src).convert("RGB"));assert hashlib.sha256(src.read_bytes()).hexdigest()=="354c4d5d7bba985a9ad9f009d7a3f9ded58e161ca0a51f13362fe7f9373d11e5"
a=home/"harness-build/asset-gates/CP05-v01"
arm=np.array(Image.open(a/"writing_limb.png").convert("RGBA"));pen=np.array(Image.open(a/"rigid_pen.png").convert("RGBA"))
Y,X=np.indices(source.shape[:2],dtype=np.float32)
# Keep head, supporting hand, shoulder and upper sleeve together. Moving foreground begins at lower cuff.
# The upper joining strip is stationary and will be held fixed in the pose transforms.
low=arm[:,:,3].copy();low[Y<846]=0
m=(low>2)|(pen[:,:,3]>2)
m=cv2.dilate(m.astype(np.uint8),np.ones((9,9),np.uint8))
m[Y<842]=0
# Upper pen can extend above lower cuff cutoff; restore its removal mask.
m=np.maximum(m,cv2.dilate((pen[:,:,3]>2).astype(np.uint8),np.ones((9,9),np.uint8)))
Image.fromarray(m*255).save(out/"removal_mask.png")
# 720x512 crop contains the entire masked area and adjacent shirt, paper and desk.
crop=(0,690,720,1202);x,y,x1,y1=crop
rgb=source[y:y1,x:x1];mask=m[y:y1,x:x1]
weights=comfy/"models/inpaint/MAT_Places512_G_fp16.safetensors"
np.random.seed(1010);torch.manual_seed(1010)
device="cuda" if torch.cuda.is_available() else "cpu"
model=mat.load(load_file(str(weights),device="cpu")).eval().to(device)
# The bundled MAT implementation stores z and label separately; move them with model.
model.z=model.z.to(device=device,dtype=torch.float32);model.label=model.label.to(device=device,dtype=torch.float32)
im=torch.from_numpy(cv2.resize(rgb,(512,512),interpolation=cv2.INTER_AREA)).permute(2,0,1)[None].float().to(device)/255
ms=torch.from_numpy(cv2.resize(mask,(512,512),interpolation=cv2.INTER_NEAREST))[None,None].float().to(device)
with torch.inference_mode(): result=model(im,ms)
pred=np.uint8(np.clip(result[0].permute(1,2,0).cpu().numpy()*255+.5,0,255))
pred=cv2.resize(pred,(720,512),interpolation=cv2.INTER_CUBIC)
plate=source.copy();part=plate[y:y1,x:x1];part[mask>0]=pred[mask>0]
# Reconstructed paper is explicit stationary entity, not model-generated background.
paperroot=Path.home()/"Documents/Krita MCP/NOUSCERA_Film001/MCI09A_Paper_v03"
paper=np.array(Image.open(paperroot/"CP05_MCI09A_native_projection.png").convert("RGBA"))
patch=np.array(Image.open(paperroot/"paper_reconstruction_patch.png").convert("RGBA"))
paperzone=(paper[:,:,3]>0)&((m>0)|(patch[:,:,3]>0))
plate[paperzone]=paper[:,:,:3][paperzone]
Image.fromarray(plate).save(out/"clean_plate_candidate.png")
Image.fromarray(pred).save(out/"mat_raw_crop.png")
receipt={"model":weights.name,"model_sha256":hashlib.sha256(weights.read_bytes()).hexdigest(),"device":device,"seed":1010,"crop":crop,"method":"installed ComfyUI MAT implementation directly; not a native ComfyUI graph","source_unchanged":True,"creative_approval":False,"status":"candidate, visual inspection required"}
(out/"mat_receipt.json").write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt),flush=True)
