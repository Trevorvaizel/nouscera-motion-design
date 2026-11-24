from pathlib import Path
import json,hashlib,zipfile
import numpy as np
from PIL import Image
home=Path.home()/"Documents/NOUSCERA"
root=Path.home()/"Documents/Krita MCP/NOUSCERA_Film001/MCI09A_Paper_v03"
candidate=np.array(Image.open(root/"stationary_notebook_candidate.png").convert("RGBA"))
projection=np.array(Image.open(root/"CP05_MCI09A_native_projection.png").convert("RGBA"))
assert candidate.shape==projection.shape
visible=candidate[:,:,3]==255
delta=np.abs(candidate.astype(np.int16)-projection.astype(np.int16))
source=home/"assets/NOUSCERA_Film001_CP05_ARTWORK_ONLY.png"
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(source)=="354c4d5d7bba985a9ad9f009d7a3f9ded58e161ca0a51f13362fe7f9373d11e5"
native=json.loads((root/"native_krita_receipt.json").read_text())
assert len(native["layers"])==5
assert any(n["locked"] and not n["visible"] and n["name"].startswith("05 Original") for n in native["layers"])
receipt={"source_unchanged":True,"native_document":True,"layer_count":5,"locked_original":True,"native_opaque_pixels":int(visible.sum()),"native_projection_max_abs_delta_opaque":int(delta[visible].max()),"native_projection_mean_abs_delta_opaque":float(delta[visible].mean()),"kra_sha256":native["kra_sha256"],"review_status":"pending author review","creative_approval":False}
(root/"native_projection_verification.json").write_text(json.dumps(receipt,indent=2))
print(json.dumps(receipt,indent=2))
