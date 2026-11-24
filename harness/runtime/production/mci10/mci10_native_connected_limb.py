"""Native Blender 5.3 two-link planar armature diagnostic. Three stills, no approved plate."""
from pathlib import Path
import bpy, math,json,hashlib
from mathutils import Vector,Matrix
home=Path.home()/"Documents/NOUSCERA";root=home/"reviews/MCI10_connected_limb_v01";root.mkdir(exist_ok=False)
assets=home/"harness-build/asset-gates/CP05-v01"
ref=json.loads((home/"reviews/MCI09_integrated_v03/layer_receipt.json").read_text())["tracks"]
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.render.engine="CYCLES";s.cycles.samples=4;s.cycles.use_denoising=False
s.render.resolution_x=720;s.render.resolution_y=1280;s.render.resolution_percentage=100
s.render.film_transparent=True;s.render.image_settings.file_format="PNG";s.render.image_settings.color_mode="RGBA"
s.view_settings.view_transform="Standard";s.view_settings.look="None";s.view_settings.exposure=0;s.view_settings.gamma=1
s.world=bpy.data.worlds.new("Neutral void");s.world.color=(0,0,0)
def W(p,z=0):return Vector(((p[0]-360)/100,(640-p[1])/100,z))
def material(name,path):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();l=m.node_tree.links
 im=n.new("ShaderNodeTexImage");im.image=bpy.data.images.load(str(path),check_existing=True);im.image.pack();im.interpolation="Linear";im.extension="CLIP"
 e=n.new("ShaderNodeEmission");tr=n.new("ShaderNodeBsdfTransparent");mix=n.new("ShaderNodeMixShader");o=n.new("ShaderNodeOutputMaterial")
 l.new(im.outputs["Color"],e.inputs["Color"]);l.new(im.outputs["Alpha"],mix.inputs[0]);l.new(tr.outputs[0],mix.inputs[1]);l.new(e.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],o.inputs[0]);return m
def mesh(name,path,bounds,step,z):
 x0,y0,x1,y1=bounds;xs=list(range(x0,x1,step))+[x1];ys=list(range(y0,y1,step))+[y1]
 pos=[(x,y) for y in ys for x in xs];nx=len(xs);faces=[(j*nx+i,j*nx+i+1,(j+1)*nx+i+1,(j+1)*nx+i) for j in range(len(ys)-1) for i in range(len(xs)-1)]
 me=bpy.data.meshes.new(name);me.from_pydata([W(p,z) for p in pos],[],faces);me.update();uv=me.uv_layers.new()
 for loop in me.loops:
  x,y=pos[loop.vertex_index];uv.data[loop.index].uv=(x/720,1-y/1280)
 ob=bpy.data.objects.new(name,me);s.collection.objects.link(ob);me.materials.append(material(name,path));return ob,pos
A=Vector((139,505));B=Vector((122,956));C=Vector((607,1000))
# A shoulder, B elbow and C nib are approximate projected landmarks. Pen and hand belong to distal bone.
L1=(B-A).length;L2=(C-B).length
arm=bpy.data.armatures.new("Connected planar writing anatomy");rig=bpy.data.objects.new("CP05 | connected limb rig",arm);s.collection.objects.link(rig)
bpy.context.view_layer.objects.active=rig;rig.select_set(True);rig.show_in_front=True
bpy.ops.object.mode_set(mode="EDIT")
u=arm.edit_bones.new("upper_sleeve");u.head=W(A);u.tail=W(B)
f=arm.edit_bones.new("forearm_hand_pen");f.head=W(B);f.tail=W(C);f.parent=u;f.use_connect=True
bpy.ops.object.mode_set(mode="OBJECT")
limb,pos=mesh("Continuous sleeve forearm hand",assets/"writing_limb.png",(16,405,620,1055),5,.08)
pen,ppos=mesh("Rigid pen fragments",assets/"rigid_pen.png",(400,760,650,1040),8,.06)
def smooth(v):v=min(1,max(0,v));return v*v*(3-2*v)
for ob,coords,ispen in [(limb,pos,False),(pen,ppos,True)]:
 vg1=ob.vertex_groups.new(name="upper_sleeve");vg2=ob.vertex_groups.new(name="forearm_hand_pen")
 for i,(x,y) in enumerate(coords):
  # Transition constrained to elbow/sleeve, not wrist. Distal skin and pen are rigid.
  w=1 if ispen else max(smooth((y-830)/120),smooth((x-175)/125)*smooth((y-815)/70))
  if w<1:vg1.add([i],1-w,"REPLACE")
  if w>0:vg2.add([i],w,"REPLACE")
 mod=ob.modifiers.new("Native armature deformation","ARMATURE");mod.object=rig;mod.use_deform_preserve_volume=True
def solve(target):
 q=target-A;dist=q.length;unit=q.normalized()
 along=(L1*L1-L2*L2+dist*dist)/(2*dist);h=math.sqrt(max(0,L1*L1-along*along))
 perp=Vector((-unit.y,unit.x));opts=[A+along*unit+h*perp,A+along*unit-h*perp]
 return min(opts,key=lambda b:(b-B).length)
def angle(v):return math.atan2(v.y,v.x)
def M(a,b,theta):
 return Matrix.Translation(W(b))@Matrix.Rotation(-theta,4,"Z")@Matrix.Translation(-W(a))
bpy.ops.object.camera_add(location=(0,0,10));cam=bpy.context.object;cam.data.type="ORTHO";cam.data.ortho_scale=12.8;s.camera=cam
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=="VIEW_3D":area.spaces.active.region_3d.view_perspective="CAMERA"
ids=[1,max(range(1,49),key=lambda i:ref[i-1]["tip"][0]),min(range(1,49),key=lambda i:ref[i-1]["tip"][0])]
records=[]
for k in ids:
 target=Vector(ref[k-1]["tip"]);elbow=solve(target)
 th1=angle(elbow-A)-angle(B-A);th2=angle(target-elbow)-angle(C-B)
 pb1=rig.pose.bones["upper_sleeve"];pb2=rig.pose.bones["forearm_hand_pen"]
 pb1.matrix=M(A,A,th1)@pb1.bone.matrix_local;bpy.context.view_layer.update()
 pb2.matrix=M(B,elbow,th2)@pb2.bone.matrix_local;bpy.context.view_layer.update()
 # Validate actual evaluated pose, not just analytic solution.
 err=(pb2.tail-W(target)).length*100;join=(pb2.head-pb1.tail).length*100
 assert err<.01 and join<.01,(err,join)
 s.render.filepath=str(root/f"pose_{k:04d}.png");bpy.ops.render.render(write_still=True)
 records.append({"reference_frame":k,"target_tip":list(target),"elbow":list(elbow),"elbow_displacement_px":(elbow-B).length,"upper_rotation_deg":math.degrees(th1),"forearm_rotation_deg":math.degrees(th2),"tip_error_px":err,"joint_gap_px":join,"bone_lengths_px":[L1,L2]})
 print("POSE",records[-1],flush=True)
s["NOUSCERA_status"]="MCI10 native connected-limb diagnostic; no approval; no background plate"
s["NOUSCERA_note"]="Two-link planar solve; pen follows distal arm orientation, not prior independent pen angle. Packed textures. Still poses only."
bpy.context.view_layer.objects.active=rig;rig.select_set(True)
master=root/"CP05_MCI10_connected_limb.blend";bpy.ops.wm.save_as_mainfile(filepath=str(master))
receipt={"native_blender_armature":True,"poses":records,"master_sha256":hashlib.sha256(master.read_bytes()).hexdigest(),"creative_approval":False,"motion_generated":False,"limitations":["Approximate planar shoulder/elbow/nib landmarks, not validated 3D anatomy","Original cutout edge contamination remains","No clean background or ink/contact shadow test; isolated rig only","Pen orientation is derived from coupled distal transform, not identical to V11"]}
(root/"rig_receipt.json").write_text(json.dumps(receipt,indent=2));print("NATIVE RIG STILL TEST COMPLETE",flush=True)
