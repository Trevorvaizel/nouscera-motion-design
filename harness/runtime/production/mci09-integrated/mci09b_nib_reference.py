from pathlib import Path
import cv2
from PIL import Image,ImageDraw
p=Path.home()/"Documents/NOUSCERA"
c=cv2.VideoCapture(str(p/"reviews/B0311L_S09_CP05_STABILIZED_MASKED_720x1280_33f_v01.mp4"))
frames=[]
while True:
 ok,f=c.read()
 if not ok:break
 frames.append(f)
c.release()
indices=[0,4,8,12,16,20,24,28,32]
board=Image.new("RGB",(1080,690),(20,20,20));d=ImageDraw.Draw(board)
for i,k in enumerate(indices):
 im=Image.fromarray(cv2.cvtColor(frames[k],cv2.COLOR_BGR2RGB)).crop((540,940,680,1030)).resize((336,216))
 dr=ImageDraw.Draw(im)
 for x in range(550,680,10):
  a=(x-540)*2.4;dr.line((a,0,a,216),fill=(45,100,70));dr.text((a+1,1),str(x),fill="yellow")
 for y in range(950,1030,10):
  a=(y-940)*2.4;dr.line((0,a,336,a),fill=(45,100,70));dr.text((0,a+1),str(y),fill="yellow")
 x=(i%3)*360;y=(i//3)*230
 board.paste(im,(x,y+14));d.text((x,y),f"Frame {k}",fill="white")
board.save(p/"reviews/MCI09B_reference_nib_grid.png")
