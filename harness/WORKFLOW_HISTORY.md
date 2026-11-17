# Workflow evolution ledger

This file records **changes to how the studio works**, not changes to a particular story. The Git history captures line changes; this ledger preserves the causal reasons.

## W-001 | 2026-11-11 | Research-first cartography

**From:** Starting with visual generation or tool presets.  
**To:** Map 13 independent knowledge provinces, their accumulated mistakes, competing mechanisms and diagnostic conditions before choosing the production workflow.  
**Reason:** Tool proficiency alone cannot explain why a film communicates successfully.  
**Evidence:** Volume 00, 13 working province manuscripts, Volume 14.  
**Status:** Research-first approach accepted, research forces provisional.  
**Failure guard:** Do not turn research prose into automatic laws.

## W-002 | 2026-11-11 | Two-track studio architecture

**From:** A linear path from a theme to attractive illustrations to AI-generated motion.  
**To:** Parallel Meaning and Cinematic Language tracks, joining at a treatment-selection gate.  
**Reason:** Beautiful visual treatments can silently redefine the story.  
**Evidence:** Stage 02 desk synthesis; proposed Stage 03 methodology.  
**Status:** Working methodological proposal, pending review in practice.  
**Failure guard:** A polished image is not approval for the underlying claim.

## W-003 | 2026-11-11 | Six decision-bearing artifacts

**From:** Separate department output documents without enforced handoff criteria.  
**To:** Thought Receipt -> Treatment Comparison -> Recognition Score -> Look/Motion Bible -> Shot/Transition Contracts -> Selection and Evidence Receipt.  
**Reason:** Keep authorial intention, motion design, AI execution and viewer response inspectably connected.  
**Status:** The author accepted the **six artifact types**, not every field or populated instance.  
**Failure guard:** Artifacts must reduce decision uncertainty, not become administrative ritual.

## W-004 | 2026-11-11 | GitHub as a living harness

**From:** Downloadable monolithic research bundles and conversation-located decisions.  
**To:** Editable manuscripts, current status, issue-linked bricks, decisions, corrections, original candidates and explicitly versioned workflows in one repository.  
**Reason:** Maintain continuity as the studio's methodology evolves and the first film emerges.  
**Status:** Infrastructure implemented.  
**Failure guard:** A document count is not an indicator of creative maturity. Every new file must have a clear operational role.

## Future workflow-change template

**W-### | date | trigger | previous practice | new practice | why | evidence/countercases | author status | affected documents | experiment or review required | retirement condition**

Do not overwrite the previous workflow rationale when a new one supersedes it.


## W-005 | 2026-11-11 | Adaptation-source preflight

**Trigger:** The supplied source for the first experiment is a 50-page essay, while the previous Thought Receipt had been built from a one-line assistant-proposed example.

**From:** Begin A01 with an attractive concept line and ask the user for its personal origin.

**To:** For an existing source work, first register the work, map its argument and movements, and choose a self-contained adaptation unit. Only then derive a source-anchored A01 Thought Receipt.

**Why:** A slogan can flatten a longer essay and manufacture a claim the source did not make.

**Status:** Adopted for the Film 001 preparation phase. This conditional **Source Map** is not a seventh compulsory artifact; the six agreed artifact types remain.

**Evidence and limits:** User-uploaded _The Human at the Door_ (50 pages), film source now confirmed. No short-film passage selected. Full text deliberately excluded from public GitHub.


## W-006 | 2026-11-15 | Visible Film 001 control map and AI-first production ownership

**Trigger:** The author approved a single orienting artifact, source/force derivation trails, a full shot and brick ledger, checklists and a six-image continuity specification after repeated disconnected microtests and repeated delegation of routine production decisions.

**From:** A growing collection of experimental receipts, partially obsolete STATUS handoffs and chat-local choices, with no single film-wide current/next index; isolated shot prompts were sometimes posed as author choices. A physical-recording proposal was explicitly rejected.

**To:** [Film 001 Master Experiment Map](../stories/001-human-at-the-door/MASTER_EXPERIMENT_MAP_v01.md) as the film's **READ FIRST** control surface, backed by [Continuity Pack v0.1](../stories/001-human-at-the-door/CONTINUITY_PACK_SPEC_v01.md), 13-shot spine, source/force traceability, status/checklist gate tracking and a named next production brick. Update AGENTS and root README to prevent older instructions from overruling it. Studio conducts AI-first image and motion production; author reviews meaningful artistic and source decisions.

**Why:** Avoid a creative-process black box while **still making the film**, rather than accumulating unlinked documents or constantly asking the author to choose next tasks.

**Evidence:** Author explicit agreement, approved A01/TR-002, D-018/D-019/D-020/D-021, B03.11F author reception, D-028 full-spine workflow, D-029 control-system authorization, and [B03.11J receipt](receipts/B03.11J-MASTER-MAP-AND-CONTINUITY-SPEC.md).

**Limits:** This controls source, decisions and experiment history; it does **not** prove the 13 proposed shots, six pending reference images or AI motion are successful. Force questions remain revisable hypotheses, not universal law.

**Status:** Adopted operating orientation. The two artifacts are created; B03.11K image generation remains to be executed. Earlier W-005 historical statement “no passage selected” is **now obsolete**, not a current source decision.

**Failure guard:** If the map and STATUS disagree, reconcile and cite the actual latest decision. Do not close a brick merely because a specification was written when its deliverable is actual visual output. Keep an author-visible film, asset and source lineage alongside its documentation.


## W-007 | 2026-11-17 | Layer-preserving local AI edits replace broad re-rendering

**From:** New-image prompts tried to preserve a specific approved face, workspace, engraved texture, props and camera angle simultaneously. The model often returned visual imitations instead.
**To:** Maintain an immutable selected CP-05 source layer, protected composites, small masks and independent graphical inserts. Use Krita layers and ComfyUI for constrained generation, then verify the exact changed pixels and record what the model actually changed.
**Evidence:** Local FLUX.2 4B FP8 inference successful; masked trial changed 63 accepted pixels inside a 36 x 25 region and none outside. A separate deterministic trial changed 77 pixels. Original engraving remained exact in protected regions.
**Limit:** These results demonstrate local controlled compositing, not successful scene-wide identity preservation or human motion.
**Status:** Adopted working production method for continuity-sensitive film shots.

## W-008 | 2026-11-17 | Separate enacted gesture from expressive semantic typography

**From:** Try to communicate a smaller question using near-invisible ink on a perspective-distorted notebook page. CP-06 lettering oriented toward the viewer rather than the character.
**To:** Let a believable scribble or hesitation carry physical action while separately controlled typography carries readable meaning in negative black space, or use an actual perspective insert if appropriate.
**Reason:** Semantic clarity and physical plausibility need not be forced into one 36 x 25 region.
**Author status:** Scribble plus typography selected as visual direction. The exact proposed wording and animation remain working.
**Failure guard:** Pure type or camera motion cannot be passed off as actual actor performance.

## W-009 | 2026-11-17 | Continuous editable master plus versioned tests and repository continuity

**From:** Each generated alternative risked becoming an isolated new “master” and leaving old repository handoffs stale.
**To:** Preserve an immutable approved CP-05 source in one native layered Krita master, maintain distinct typography/scribble/effects layers, preserve experimental versions and keep repository status, decisions, receipts and asset lineage reconciled.
**Evidence:** Native KRA master and preview generated locally and verified for pixel-exact preservation of its source; [working master manifest](../stories/001-human-at-the-door/LOCAL_WORKING_MASTER_MANIFEST_v01.md).
**Boundary:** The working master's existence is not evidence of completed actor motion, CP-06 final approval or externally archived media.

