# EX-001 | Initial Anchor Image Review v0.1

**Date:** 2026-11-11  
**Status:** Two generated stills are **exploratory look studies**, NOT matched production anchors, NOT a motion test  
**Contract:** [A05 EX-001](A05_EX001_SHOT_TRANSITION_CONTRACT_v01.md)

## What was generated

Two independent black-and-white engraving-style illustrations were generated during the conversation:

- **EX-001-S-candidate-01**, start: seated person in a late-night study, with notebook and desk. Image generation record: `36ce1220-6162-4812-828d-d5c9b0df452f`.
- **EX-001-E-candidate-01**, target: seated person and notebook at a possible customer-conversation table, with an unoccupied opposite chair. Image generation record: `5976bc11-e0ee-447c-b868-f029e508eb70`.

**Assets:** Returned in the private conversation; the binary images have **not** been uploaded to this public GitHub repository. Their current storage is not a permanent repo-linked asset system.

## Observed visual properties (editorial inspection only)

**Positive candidates:** High-contrast black/white engraved vocabulary and recognizable human/notebook relationships. The end-state environment can imply a possible encounter rather than a transaction that has occurred.

**Blocking issues for the intended controlled morph:**

1. **Viewpoint mismatch:** Start image uses side/three-quarter face-and-desk composition; end image uses a much closer over-the-shoulder viewpoint. This defeats easy source-target identity matching.
2. **Topological correspondence missing:** Desk and table geometry, near edges and their orientation differ too much for the specified edge-to-edge invariant.
3. **Human character continuity unproven:** Both show a human, but the angle/crop, apparent identity and pose do not reliably establish the same actor moving through one world.
4. **Canvas mismatch:** Generated files present as landscape (~16:9), while the working platform test canvas in A04/A05 is vertical 9:16.
5. **Background transition uncontrolled:** Without matched anchor framing, a video model could generate an attractive dissolve or unrelated replacement rather than the room itself becoming the new world.

These are **observations of the still pair**, not results from a video model, not cold-viewer evidence and not a failure of the selected cinematic idea.

## Adjudication

- **Do not label EX-001 completed or passed.**
- Preserve these as **Look Study 01, unpaired**.
- **Next still-making target:** A matched **portrait 9:16** pair, same viewpoint, same human identity and notebook pose, a deliberately shared desk/table edge path, but a visibly changed environment.
- The customer chair must remain empty to protect the difference between a *possible* contact and completed validation.
- Keep the new pair simple enough that the user can see the relationship on a phone; reduce decorative hatching as required before attempting to animate.
- Once the pair passes a static comparison, use the A05 experimental contract to choose an actual start/end-frame-capable model and perform a controlled morph test. Do not infer model capabilities in advance.

## Evidence limits

No prompt/settings/seed/model-version log beyond generated IDs is available from the image-generation record. Any later repeatability claim must be qualified. No raw generation binary was copied to the public repo and no copyright/license conclusion about publication has been drawn.

**The first learning is a production-design issue:** a visual *style match* is not the same as a **motion-ready correspondence**.
