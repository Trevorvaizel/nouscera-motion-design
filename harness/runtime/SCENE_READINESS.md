# Scene readiness: reusable gate, not creative automation
The workflow can be replayed now. The next scene authoring operation is intentionally blocked until independently prepared assets meet their contract.

## Required operations
1. Read active state and requested shot intent. Lock source/version and authorize only the task at hand.
2. Map entities, behaviors, dependencies, visibility/occlusion and permitted movement. Assign each entity a distinct semantic asset where required. Static page remains fixed; pen is a rigid transform, never a cloth warp.
3. Krita: duplicate the protected master; isolate layers; produce a clean plate and full hidden surface for the planned movement envelope. Use ComfyUI selectively for masked reconstruction with exact source, graph version, mask and model identity, retaining outside-mask source pixels. Do not claim this step from generic inpainting or a pixel preservation test. Evaluate the reconstructed paper itself at full scale.
4. Register prepared PNG layers and content hashes; record hidden-surface review against the actual artifact hash. Run scene_gate.py. An unreviewed asset fails closed.
5. Blender: separate fixed, rigid and deformable objects; independent ink and contact effects; render test and inspect occlusion, rigidity and contact. Do not present the external raster preview as a native Blender render.
6. Verify static areas independently, inspect complete action in motion, document unresolved defects. Author reviews intent and artistic quality, not merely a successful export.
7. Register new workflow versions and receipts before transferring. Preserve rejected attempts and known failures.

The gate accepts a scene-specific manifest, not a general assertion of readiness. For CP05, six roles are required. Other scenes define their own roles and physical rules. The local CP05 manifest remains blocked because clean paper is not yet validated. The generic fixed/rigid compositor has a synthetic transfer test; it does not prove whole-scene transfer or replace the prepared-scene adapter.
