from pathlib import Path
import bpy, math,json,hashlib
from mathutils import Vector,Matrix
home=Path.home()/"Documents/NOUSCERA";out=home/"reviews/MCI11_integrated_v01";out.mkdir(exist_ok=False)
base=home/"reviews/MCI10_connected_limb_v01/CP05_MCI10_connected_limb.blend"
bpy.ops.wm.open_mainfile(filepath=str(base))
s=bpy.context.scene;rig=bpy.data.objects["CP05 | connected limb rig"]
ref=json.loads((home/"reviews/MCI09_integrated_v03/layer_receipt.json").read_text())["tracks"]
assert len(ref)==48
A=Vector((139,505));B=Vector((122,956));C=Vector((607,1000))
L1=(B-A).length;L2=(C-B).length
def W(p):return Vector(((p[0]-360)/100,(640-p[1])/100,0))
def angle(v):return math.atan2(v.y,v.x)
def M(a,b,t):return Matrix.Translation(W(b))@Matrix.Rotation(-t,4,"Z")@Matrix.Translation(-W(a))
def solve(target):
 q=target-A;dist=q.length;unit=q.normalized();along=(L1*L1-L2*L2+dist*dist)/(2*dist)
 h=math.sqrt(max(0,L1*L1-along*along));perp=Vector((-unit.y,unit.x))
 return min([A+along*unit+h*perp,A+along*unit-h*perp],key=lambda b:(b-B).length)
s.frame_start=1;s.frame_end=48;s.render.fps=24
pb1=rig.pose.bones["upper_sleeve"];pb2=rig.pose.bones["forearm_hand_pen"]
rig.animation_data_clear()
records=[]
for i,t in enumerate(ref,1):
 s.frame_set(i);target=Vector(t["tip"]);elbow=solve(target)
 th1=angle(elbow-A)-angle(B-A);th2=angle(target-elbow)-angle(C-B)
 pb1.matrix=M(A,A,th1)@pb1.bone.matrix_local;bpy.context.view_layer.update()
 pb2.matrix=M(B,elbow,th2)@pb2.bone.matrix_local;bpy.context.view_layer.update()
 err=(pb2.tail-W(target)).length*100;gap=(pb2.head-pb1.tail).length*100
 assert max(err,gap)<.01
 for pb in [pb1,pb2]:
  pb.keyframe_insert("location",frame=i);pb.keyframe_insert("rotation_quaternion",frame=i);pb.keyframe_insert("scale",frame=i)
 records.append({"frame":i,"tip":list(target),"elbow":list(elbow),"tip_error_px":err,"joint_gap_px":gap,"distal_angle_deg":math.degrees(th2)})
# Verify actual animated evaluation after key insertion.
for i,r in enumerate(records,1):
 s.frame_set(i);bpy.context.view_layer.update()
 assert (pb2.tail-W(r["tip"])).length*100<.02
s.frame_set(1);s.render.engine="BLENDER_EEVEE";s.render.film_transparent=True
s.render.image_settings.file_format="PNG";s.render.image_settings.color_mode="RGBA"
s.render.resolution_x=720;s.render.resolution_y=1280;s.render.resolution_percentage=100
s.render.filepath=str(out/"rig_frames"/"frame_");(out/"rig_frames").mkdir()
s["NOUSCERA_status"]="MCI11 animated connected rig, unapproved experimental preview"
master=out/"CP05_MCI11_connected_animated.blend";bpy.ops.wm.save_as_mainfile(filepath=str(master))
(out/"rig_tracks.json").write_text(json.dumps(records,indent=2))
print("48 KEYFRAMED POSES VERIFIED",flush=True)
bpy.ops.render.render(animation=True)
assert len(list((out/"rig_frames").glob("*.png")))==48
print("RIG RENDER COMPLETE 48",flush=True)
