"""Minimal reusable 2D layer compositor for deterministic mechanics tests.
Not a character-animation system; fixed/rigid paths are explicit and enforceable."""
import math
from PIL import Image
def render(size,layers):
    canvas=Image.new("RGBA",size,(0,0,0,255))
    for l in layers:
        img=l["image"].convert("RGBA")
        if img.size!=size:raise ValueError("layer dimensions")
        behavior=l["behavior"];t=l.get("transform",{})
        if set(t)-{"degrees","dx","dy"}:raise ValueError("unsupported transform")
        a,dx,dy=[float(t.get(k,0)) for k in ("degrees","dx","dy")]
        if not all(math.isfinite(x) for x in (a,dx,dy)):raise ValueError("nonfinite transform")
        if behavior=="fixed":
            if any((a,dx,dy)):raise ValueError("fixed layer cannot move")
        elif behavior=="rigid":
            # Inverse rotation and translation, no scale/shear.
            r=math.radians(a);c,s=math.cos(r),math.sin(r)
            img=img.transform(size,Image.Transform.AFFINE,(c,s,-c*dx-s*dy,-s,c,s*dx-c*dy),resample=Image.Resampling.BICUBIC)
        else:raise ValueError("this primitive supports fixed and rigid only")
        canvas=Image.alpha_composite(canvas,img)
    return canvas
