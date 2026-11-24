"""Build a diagnostic contact sheet of existing assets; not reconstruction."""
import sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
root=Path(sys.argv[1]);out=Path(sys.argv[2])
# Focus on the notebook/writing region of the actual 720x1280 CP05 source.
crop=(220,855,710,1135)
entries=[("Source: writing region","source.png"),("Existing notebook layer","stationary_notebook.png"),("Existing writing limb","writing_limb.png"),("Existing clean plate","stationary_clean_plate.png")]
canvas=Image.new("RGB",(1040,690),(25,25,25));d=ImageDraw.Draw(canvas)
font=ImageFont.load_default(size=18);small=ImageFont.load_default(size=13)
d.text((20,12),"CP05 | Hidden surface inspection (existing assets only)",font=font,fill="white")
for i,(label,name) in enumerate(entries):
 x=20+(i%2)*510;y=58+(i//2)*310
 src=Image.open(root/name).convert("RGBA").crop(crop)
 bg=Image.new("RGBA",src.size,(50,50,50,255));bg.alpha_composite(src)
 canvas.paste(bg.convert("RGB"),(x,y+22));d.text((x,y),label,font=small,fill="white")
d.text((20,670),"No new paper reconstruction. Visual judgment required before animation.",font=small,fill=(225,190,120))
canvas.save(out)
