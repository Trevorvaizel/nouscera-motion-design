"""Exercise fixed-surface and rigid-prop mechanism on a different synthetic scene."""
import argparse,json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw
from layer_engine import render
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True);a=p.parse_args();out=Path(a.out);out.mkdir(exist_ok=False,parents=True)
    size=(160,100);paper=Image.new("RGBA",size,(20,20,20,255));d=ImageDraw.Draw(paper);d.rectangle((10,38,149,94),fill=(235,235,235,255))
    for y in range(46,95,8):d.line((15,y,144,y),fill=(100,100,100,255))
    prop=Image.new("RGBA",size);d=ImageDraw.Draw(prop);d.rectangle((25,15,65,21),fill="white")
    frames=[render(size,[{"image":paper,"behavior":"fixed"},{"image":prop,"behavior":"rigid","transform":{"dx":i*3,"dy":20,"degrees":0}}]) for i in range(12)]
    roi=(10,65,149,94);same=all(f.crop(roi).tobytes()==paper.crop(roi).tobytes() for f in frames)
    distinct=len({hashlib.sha256(f.tobytes()).hexdigest() for f in frames})==12
    denied=0
    for bad in [{"behavior":"fixed","transform":{"dx":1}},{"behavior":"rigid","transform":{"scale":1.2}}]:
        try:render(size,[{"image":paper,**bad}])
        except ValueError:denied+=1
    frames[0].save(out/"synthetic_transfer.gif",save_all=True,append_images=frames[1:],duration=100,loop=0)
    report={"status":"pass" if same and distinct and denied==2 else "fail","static_roi_equal":same,"distinct_frames":distinct,"forbidden_transforms_rejected":denied,"scope":"synthetic fixture, not a second creative scene"}
    (out/"receipt.json").write_text(json.dumps(report,indent=2));print(json.dumps(report));assert report["status"]=="pass"
if __name__=="__main__":main()
