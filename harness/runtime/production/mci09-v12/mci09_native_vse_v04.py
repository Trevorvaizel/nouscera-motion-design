from pathlib import Path
import bpy
p=Path.home()/"Documents/NOUSCERA/reviews"
base=p/"MCI09_integrated_v03";out=p/"MCI09_integrated_v04"
bpy.ops.wm.open_mainfile(filepath=str(base/"CP05_MCI09_integrated_v03.blend"))
s=bpy.context.scene;ed=s.sequence_editor
assert len(ed.strips)==7
# Resolve old relative assets before changing the master directory.
for strip in ed.strips:
 if hasattr(strip,"directory"):strip.directory=bpy.path.abspath(strip.directory)
strip=ed.strips.new_image("08 Local stationary sleeve seam repair",str(out/"sleeve_seam_repair.png"),8,1)
strip.frame_final_duration=48;strip.blend_type="ALPHA_OVER"
s["NOUSCERA_status"]="V12 localized seam correction; author review pending"
s.frame_set(1)
render=out/"native_render";render.mkdir(exist_ok=False)
s.render.filepath=str(render/"frame_")
master=out/"CP05_MCI09_integrated_v04.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(master),relative_remap=True)
bpy.ops.render.render(animation=True)
assert len(list(render.glob("*.png")))==48
print("NATIVE RENDER COMPLETE 48",flush=True)
