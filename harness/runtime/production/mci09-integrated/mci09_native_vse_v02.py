"""Actual native Blender 5.3 sequence editor composite, editable strips."""
from pathlib import Path
import bpy,json,hashlib
p=Path.home()/"Documents/NOUSCERA"
root=p/"reviews/MCI09_integrated_v02"
receipt=json.loads((root/"layer_receipt.json").read_text())
assert receipt["frames"]==48
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.frame_start=1;s.frame_end=48;s.render.fps=24;s.render.fps_base=1
s.render.resolution_x=720;s.render.resolution_y=1280;s.render.resolution_percentage=100
s.view_settings.view_transform="Standard";s.view_settings.look="None";s.view_settings.exposure=0;s.view_settings.gamma=1
s.render.image_settings.file_format="PNG";s.render.image_settings.color_mode="RGB"
s.render.use_sequencer=True
ed=s.sequence_editor_create()
strip=ed.strips.new_image("01 Stationary reconstructed plate",str(root/"stationary_plate.png"),1,1)
strip.frame_final_duration=48;strip.blend_type="REPLACE"
for channel,folder,label in [(2,"ink","02 Progressive inscription"),(3,"shadow","03 Independent contact shadow"),(4,"head","04 Restrained head acting"),(5,"pen","05 Rigid pen"),(6,"limb","06 Deformed writing limb"),(7,"source_lock","07 Original preservation matte")]:
 paths=sorted((root/folder).glob("*.png"))
 assert len(paths)==48
 strip=ed.strips.new_image(label,str(paths[0]),channel,1)
 for path in paths[1:]:strip.elements.append(path.name)
 strip.frame_final_duration=48;strip.blend_type="ALPHA_OVER"
 assert strip.frame_final_duration==48
# All layer images are external sequence assets; keep this directory intact.
s["NOUSCERA_status"]="MCI09 integrated experiment; NOT approved; readiness remains blocked"
s["NOUSCERA_method"]="Native VSE alpha-over of independently generated raster layers, not a live 3D rig"
s["NOUSCERA_reference"]="First generative candidate pen path, manually sampled, 62% displacement"
s.frame_set(1)
master=root/"CP05_MCI09_integrated_v02.blend"
assert not master.exists()
render=root/"native_render";render.mkdir(exist_ok=False)
s.render.filepath=str(render/"frame_")
bpy.ops.wm.save_as_mainfile(filepath=str(master),relative_remap=True)
print("NATIVE VSE MASTER",master,[(x.name,x.channel,x.frame_final_duration) for x in ed.strips],flush=True)
bpy.ops.render.render(animation=True)
print("NATIVE RENDER COMPLETE",len(list(render.glob("*.png"))),flush=True)
