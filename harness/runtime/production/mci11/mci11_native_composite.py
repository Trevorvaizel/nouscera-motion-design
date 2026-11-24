from pathlib import Path
import bpy
p=Path.home()/"Documents/NOUSCERA";out=p/"reviews/MCI11_integrated_v01";prev=p/"reviews/MCI09_integrated_v03"
# Preserve the keyframed native rig in this integrated master.
bpy.ops.wm.open_mainfile(filepath=str(out/"CP05_MCI11_connected_animated.blend"))
rigscene=bpy.context.scene;rigscene.name="CP05 connected armature | rendered foreground"
s=bpy.data.scenes.new("CP05 MCI11 | integrated review")
bpy.context.window.scene=s
s.frame_start=1;s.frame_end=48;s.render.fps=24;s.render.resolution_x=720;s.render.resolution_y=1280;s.render.resolution_percentage=100
s.view_settings.view_transform="Standard";s.view_settings.look="None";s.render.image_settings.file_format="PNG";s.render.image_settings.color_mode="RGB";s.render.use_sequencer=True
ed=s.sequence_editor_create()
strip=ed.strips.new_image("01 Material-separated stationary plate",str(out/"stationary_plate.png"),1,1)
strip.frame_final_duration=48;strip.blend_type="REPLACE"
for ch,folder,label in [(2,prev/"ink","02 Progressive ink"),(3,prev/"shadow","03 Independent contact shadow"),(4,out/"rig_frames","04 Native connected rig render")]:
 paths=sorted(folder.glob("*.png"));assert len(paths)==48
 strip=ed.strips.new_image(label,str(paths[0]),ch,1)
 for path in paths[1:]:strip.elements.append(path.name)
 strip.frame_final_duration=48;strip.blend_type="ALPHA_OVER"
s["NOUSCERA_status"]="MCI11 experimental review; no creative approval, no readiness promotion"
s["NOUSCERA_method"]="Integrated VSE using native keyframed connected armature renders, no full source overlay. Rig scene retained; rerender foreground after rig edits."
s.frame_set(1);render=out/"native_render";render.mkdir(exist_ok=False);s.render.filepath=str(render/"frame_")
bpy.ops.wm.save_as_mainfile(filepath=str(out/"CP05_MCI11_integrated_connected_limb.blend"),relative_remap=True)
bpy.ops.render.render(animation=True)
assert len(list(render.glob("*.png")))==48
print("MCI11 NATIVE COMPOSITE COMPLETE",flush=True)
