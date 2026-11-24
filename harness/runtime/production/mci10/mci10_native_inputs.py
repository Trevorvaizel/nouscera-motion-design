from pathlib import Path
import hashlib,json
from PIL import Image
home=Path.home()/"Documents/NOUSCERA"
comfy=Path.home()/"Downloads/Compressed/ComfyUI_windows_portable_nvidia/ComfyUI_windows_portable/ComfyUI"
out=comfy/"input/NOUSCERA";out.mkdir(exist_ok=True)
src=home/"assets/NOUSCERA_Film001_CP05_ARTWORK_ONLY.png"
assert hashlib.sha256(src.read_bytes()).hexdigest()=="354c4d5d7bba985a9ad9f009d7a3f9ded58e161ca0a51f13362fe7f9373d11e5"
crop=(120,690,632,1202)
mask=Image.open(home/"reviews/MCI10_scene_ownership_v02/removal_mask.png").convert("L")
assert mask.getbbox()[0]>=120 and mask.getbbox()[2]<=632,mask.getbbox()
Image.open(src).convert("RGB").crop(crop).save(out/"MCI10_native_source_crop.png")
mask.crop(crop).save(out/"MCI10_native_removal_mask.png")
print("Prepared exact 512px square from protected source; mask bounding box",mask.getbbox())
