# B03.11B | EX-002 | Speech-to-Sign Micro-Animatic Comparison

**Date:** 2026-11-15  
**Status:** Two actual controlled rough video variants generated; no author review or cold-viewer evidence  
**Film source:** _The Human at the Door_, "The fog", PDF pp. 7–11, source PDF remains outside public repository  
**Project decisions:** D-014, D-018, D-019, D-020, D-021  
**Instruments:** A03 [Speech-to-Sign Audit v0.1](A03_SPEECH_TO_SIGN_AUDIT_v01.md), A04 graphic grammar, A05 scoped production comparison, A06 preliminary evidence  

## The one question

When the spoken instructions are **the same**, does showing detailed, concrete signs in deliberate isolation help an audience distinguish the *kinds of action* each instruction suggests better than a simple label display, without adding an unwarranted success claim or narrowing their meaning too much?

This is a **speech-to-sign** experiment. It does **not** test room-to-world EX-001 metamorphosis or the full film's placement revelation.

## Exact audio inherited from the first rough animatic

The existing Film 001 `B2.wav` temporary voice track was reused **unchanged** in both variants. It says:

> So the advice arrives. Validate first. Talk to customers. Build the smallest version.

The wording and voice come from the already-existing temporary Rhythm A narration, not a new quotation from the essay. The essay itself offers comparable sensible instructions, including talk to customers and building the smallest possible version.

**Silence boundaries detected in the original B2 track** (approximate seconds):
- First clause ends 1.636, silence to 2.109.
- "Validate first" ends 3.264, silence to 3.779.
- "Talk to customers" ends 5.093, silence to 5.564.
- "Build the smallest version" ends 7.395, silence to 7.881.

These positions controlled the visual changes. Each film extends with black to **9.000 seconds**; the audio is identical in both.

## Actual produced outputs

**Version A: Text-only control.** A simple uppercase text label for each instruction on black. This approximates the prior sparse text-box logic without reproducing the full first animatic's visual timeline.

**Version B: Isolated engraved objects.** Three independent monochrome illustrations, each shown without a continuous environment: an unfilled validation/checklist notebook and pen, an unoccupied chair beside a table and water glass, and a pair of hands assembling an unfinished small cardboard model. Each emerges from black via a short line-preserving reveal, holds, then retracts into darkness. No automatic morph joins the objects.

**Companion comparison:** Split-screen A/B playback, sharing audio from A, to make the differences inspectable.

**Media files** (in conversation runtime, intentionally **not** copied into public GitHub):

| Asset | Technical properties | SHA-256 |
|---|---|---|
| `EX002_A_Typography_Control_WithTempVoice.mp4` | 540×960, 18fps, 9 sec | `6645ec09f19053bc9e098bf34804d60cac13e57e349435f84281c18c1b09d7b3` |
| `EX002_B_Isolated_Engraved_Objects_WithTempVoice.mp4` | 540×960, 18fps, 9 sec | `28dd73b6df29fc2a9e6385a3ef0e76e137da1f81de67b74fdd599c4d0f52006f` |
| `EX002_AB_Side_by_Side_Comparison.mp4` | 1080×960, 18fps, 9 sec | `65417d94cc5f818bd0a27815a25c50d780063d436ce6064c26e65abd69e3952e` |
| `EX002_Control_vs_Isolated_Objects_ContactSheet.jpg` | A/B five-times visual reference | `fea49cf9ba61d451dd9c4f4619cf188365479584f5411983630d2c2392c478d6` |

**Build method:** Engraved object art from ImageGen; original rendered source output delivered as a six-frame GIF, then its two-row, three-column component panels were assembled into three static object studies. PIL/Numpy compositing authored short directed reveals and black holds; ffmpeg encoded synchronized H.264/AAC video. Build script: `build_ex002.py` in working runtime; source script is not yet committed.

**Production scope:** Actual animations exist, but these are rough motion-design tests. No final music, sound design, AI video model, full cinematic scene or final human character was produced.

## Immediate quality observations, not viewer results

**Present:**
- A and B have the same audio and total duration.
- B is not a continuous AI movie. Detailed physical objects appear independently on black.
- The three sign types differ in form and implied action.
- Separate black holds prevent automatic causal links between the instructions.
- The illustration family is consistent and recognizably white-on-black engraved.

**Known design risks:**
1. A checklist can mislead viewers into treating "validation" as completing a form rather than learning from evidence.
2. The empty chair may suggest social contact but does not by itself show a customer, customer behavior or listening.
3. The cardboard prototype resembles a miniature building, potentially narrowing "build the smallest version" to an architectural or construction product. This is **not** a claim the essay supports.
4. Objects standing alone can still miss the founder's lived pressure and original question. EX-002 is intentionally *only the advice event*, not a test of the full argument.
5. Animation is a directed simple reveal, not a proof of fluent AI motion or a room converting into another world.
6. We do not know whether viewers infer the intended action distinction. No neutral participant has watched or reported their interpretation.

## Preliminary adjudication

**Production:** Passed the basic equal-audio, timed A/B preparation gate.  
**Representation:** More semantically distinctive sign candidates exist, but their actual comprehensibility is **unverified**.  
**Source protection:** No one is shown completing validation, holding a customer meeting or obtaining a successful prototype outcome. Risk of implied meanings still needs review.  
**Outcome:** **Ready for author inspection and a few unprimed interpretations**, not approved for inclusion in Film 001.

## How to review without priming

First show A or B without telling the viewer what we meant by each object. Then ask:
- What distinct actions or possibilities did you perceive?
- What did you think the three illustrations had in common?
- Did any object suggest that something had already succeeded?
- What, if anything, did you infer about the person facing these choices?

Then reveal the spoken content and compare whether the images helped or redirected understanding. With a small, informal study, do not claim generalized audience results.

## Next brick

Make an **author selection or revision** among specific signs, not a generic approval of 'visual objects'. In particular, challenge the prototype's unwanted product specificity and whether the 'validate' image represents actual evidence. Then use the learned correspondence rules on the **placement question** in the later A03 speech events S10–S12. Only once both are legible should we revise the full 49-second Rhythm A animatic to v0.2.

**No decision about the user's preferred illustration has been inferred here.**
