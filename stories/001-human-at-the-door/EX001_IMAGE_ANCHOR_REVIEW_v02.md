# EX-001 | Look Study 02 | Shared-frame and inter-frame design review

**Date:** 2026-11-11
**Status:** Three related key-state images generated and extracted; **not validated motion-ready production anchors**, **no video test run**
**Context:** A05 EX-001 v0.1 and EX001_IMAGE_ANCHOR_REVIEW_v01.md

## Question

Can we repair the previous mismatched viewport and start designing **the interval between images** as its own creative material rather than asking AI to bridge unrelated stills?

## What was generated

Two sequential image-generation attempts produced explanatory multi-panel **engraved transformation boards**, not single-frame 9:16 illustrations. Generation references:

- Board 1: `f6892d5a-f9f3-4d75-a290-be6c3546a8ae`.
- Board 2: `e8afd03d-10c7-4a67-ac67-0d65ce9431a3`.

The second board contained three related key-state panels:
1. **Start:** human with notebook at desk inside personal study.
2. **Proposed intermediate state:** same figure and notebook with flowing contour bands while study walls begin acquiring café/environmental identity.
3. **Target:** same figure and notebook in a social/customer-conversation environment.

The panels were precisely extracted into **three separate 1080×1920 portrait files** by proportional scaling and adding black vertical negative space. This is a **presentation conversion** of existing art, not original native 9:16 frame generation. The processed local files are:

- `EX001_v02_start_portrait.png`
- `EX001_v02_between_portrait.png`
- `EX001_v02_possible_conversation_portrait.png`
- `EX001_v02_three_key_states.png` (side-by-side comparison)

**Public repository boundary:** These generated assets exist in the conversation's working runtime and are **not** uploaded into the public GitHub repository. Paths above are session-local asset references, not guaranteed future cloud paths.

## What improved over Look Study 01

- Camera framing, person, pose, hand, notebook, mug and work-surface alignment are **far more similar** across the three generated panels.
- The *environment*, rather than only an illustration projected into a stable room, visibly begins changing identity.
- The intermediate key-state illustrates possible continuity: study linework becomes flowing contours and the world of a customer conversation emerges.

These observations are an editorial look review, not a measured frame-correspondence test.

## Remaining mismatches and story hazards

1. **Native composition remains landscape in the generator output**: we extracted panels and padded to portrait, but the images were not re-composed for the height of a full 9:16 cinematic frame. Do not call them final production anchors.
2. **Generated intermediate is a concept key-state**: a three-panel image does not define timing, velocity, holds, shape correspondence for every frame, or a usable generative video trajectory.
3. **Customer activity is visible in the target background**, risking a reading that the protagonist is already having validated conversations; the person is still at a notebook, so this is ambiguous. A subsequent target should preserve **possible encounter** rather than actual success.
4. **The original desk edge does not convert as unmistakably as specified**; room-to-world change reads well at a broad level but needs stronger local correspondence.
5. **The ending may read as relocation rather than metamorphosis** if an actual video simply crossfades from study to café.
6. **Fine white engraving stability** in actual AI motion remains untested.
7. **Character and notebook identity** are more consistent but not pixel-identical. Any downstream motion may amplify subtle drift.
8. **A compelling board is not yet a finished A05 result**.

## The role of P07/P08/P09 in the 'space between'

The studio's prior cartography distinguished:
- **P07 Animation:** Authorship of timing, spacing, holds, acceleration, motion identity and change *between drawings*.
- **P08 Motion Design and Metamorphosis:** Authorship of what identity/relation survives a morph, and whether it wrongly implies causal succession or equivalence.
- **P09 Editing:** Authorship of what an audience retains across an interval, including where a pause or cut is truer than seamless movement.

Thus two beautiful anchors are **constraints and endpoints**, not a motion design. The creative work is to specify the path by which the desk becomes another world, which forms maintain their identity, where the spectator should notice change, and how long the old and new meanings overlap.

## Next decision and experiment

**Concentrate on one correspondence**, such as the **desk edge to conversation table edge**, with the human/notebook relation protected. Produce a new, truly vertically composed pair using the locked figure/camera reference and intentionally keep the opposite place unoccupied. Then create and compare a short AI-generated motion against a semantic interval contract, preserving the full provider/model settings and rejected takes.

**Status:** This iteration is useful design progress, but not evidence that the actual moving interval works. EX-001 remains open; no animated sequence has been run.
