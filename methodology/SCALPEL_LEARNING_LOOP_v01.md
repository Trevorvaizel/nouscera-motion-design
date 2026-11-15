---
title: "Nouscera | Scalpel Learning Loop"
version: "0.1"
date: "2026-11-15"
status: "Prospective studio protocol; no prediction has been validated by new viewers"
applies_to:
  - "methodology/SEMANTIC_FIT_SCALPEL_MATRIX_v01.md"
  - "stories/001-human-at-the-door/B03.11D_COMPETING_AUDIOVISUAL_DESIGNS_v01.md"
---

# Scalpel Learning Loop v0.1

## Objective

The studio should become better at selecting meaningful audiovisual treatments **before generation** by accumulating evidence of where its interpretive force questions succeeded, failed, oversimplified or introduced their own distortions.

This does **not** imply that a force becomes a proven universal law because one short film appears effective. The goal is a **revisable operating method** with local, traceable changes to questions, scope and evidence.

## Three nested objects of learning

1. **Source fidelity:** Did we preserve the actual passage's qualifications, tensions and epistemic limits?
2. **Audiovisual decision:** Did the representation, timing, voice and sequence jointly enable the intended inference without importing an unwarranted one?
3. **Instrument performance:** Did a specific scalpel's *pre-generated prediction* help choose or reject the right candidate? Did it miss an important failure, or falsely reject an effective alternative?

**Critical separation:** The author approves intent and creative direction. Viewers supply observations about their interpretations. Models supply outputs with technical limitations. These are different evidence types and must not be blended into one success percentage.

## Protocol: predict -> produce -> observe -> revise -> retest

### Step 1 | Register the case before viewing any new candidate

- Case ID, source and exact passage.
- Intended viewer inference, and the *closest tempting wrong inference*.
- The specific force code and its **situated question**.
- Two or more genuinely different proposed representational mechanisms, when viable.
- **Prediction:** what a first-time viewer may infer from each, including a clear failure condition.
- What will be constant (source passage, audience brief, voice, duration where feasible), and what will vary.
- Source context that must not disappear.

### Step 2 | Make the smallest comparison that could disconfirm us

- Use low-fidelity stills, motion sketches, voice and black frames when enough.
- Track each asset, generator or editor, conditions, and changes.
- Don't mislabel a whole-treatment comparison of distinct scripts as a controlled, one-variable A/B.

### Step 3 | Gather actual interpretations, unprimed first

Neutral first:
- "What happened?"
- "What were the different choices or possibilities?"
- "What changed, and what remained open?"
- "Which detail led you to that reading?"

After that, probes about specific potential failures:
- "Did you think the actions had to occur in that order?"
- "Did you think a sale, validation, or result had already happened?"
- "Was any advice shown as intrinsically bad?"
- "What could the person do next, and how certain was that?"

Label audience background and viewing conditions if known. A small convenience group supports **qualitative diagnoses** only.

### Step 4 | Compare prediction with observation

For each force prediction mark one of:

- **Observed as predicted:** the specific warned interpretation occurred.
- **Predicted risk not observed in this test:** absence in a small sample does not prove safety.
- **Important failure missed:** viewers inferred something damaging the force question did not flag.
- **False veto candidate:** the force predicted a failure but viewers grasped the intended meaning and there is a defensible explanation.
- **Indeterminate:** unclear perception, insufficient exposure, conflicting viewers, or confounded treatment changes.

Also tag *whether* the failure came from source selection, narration, visual sign, scene, interval, sound, edit, or generative model. Don't credit a sign force for what was actually a script rewrite.

### Step 5 | Make the smallest instrument revision justified

Allowed revisions, all versioned with reasons:
- **Narrow a force's scope:** It worked for a static object, not a dialogue sequence.
- **Change the situated question:** "Does the picture match the noun?" becomes "Which action or relation can a viewer infer?"
- **Add a countercase:** Cases where a still works despite an action verb, or motion harms clarity.
- **Move a gate earlier:** Source-sequence audit belongs before image generation.
- **Add a competing scalpel:** Semantic spillover alone does not detect false causation from ordering.
- **Retain uncertainty:** Do not move a force from research candidate to universal standard without repeated cross-case evidence.

Keep the discarded wording and original predictions visible in Git history. Do not rewrite a prediction after seeing its result.

### Step 6 | Transfer-test on a different passage

Before calling the revision “better,” apply it to another piece of narration or another source with a different subject and visual form. Count both prevented problems and new false vetoes. Prefer a collection of well-documented case receipts to an opaque numeric score.

## Case record template

| Field | Entry |
|---|---|
| Case ID | EX-003A / EX-003B, or next identifier |
| Passage | Document, page span, excerpt/paraphrase and qualification |
| Intended inference | One clear audience recognition, not a style description |
| Candidate / difference | Named alternative mechanisms and which dimensions differ |
| Force and question | Exact Pxx-Fxx code with situated test |
| Pre-registered prediction | Expected reading and counter-reading **before generation** |
| Material | Script, images, edit timecode, voice, take and settings |
| Observation | Viewer paraphrase or visibly verified artifact behavior, with evidence class |
| Match | Observed / not observed / missed / false veto / indeterminate |
| Diagnosis | Source, script, object, action, interval, voice, technical, or mixed |
| Smallest revision | What changes and why, with version |
| Transfer case | Where a revised force will be used next |
| Limits | Small sample, confounds, absent footage, uncertain intent |

## Initial prospective records, still all OPEN

| Case | Force prediction, registered now | What would support the diagnosis? | What would count against it? |
|---|---|---|---|
| A: Competing Counsel | **P02-F03** warns the audible order "ask, observe, build, wait" can be mistaken for a necessary sequence even after separate cuts | Unprimed viewers describe "first do X, then Y, then Z" as the film's instruction | Viewers consistently describe incompatible proposals without a prescribed order |
| A: Scene-to-action correspondence | **P07-F07 / P01-F04** predict a short active prototype event may reveal *making something provisional* better than the static tiny house | Viewers describe construction/trying, while explicitly not assuming a completed product | They only notice the specific object, infer a particular industry, or cannot explain why it was provisional |
| B: Context spillover | **P01-F02/F03** warn contextual details may invent a biographical hardship story | Viewers confidently report a specific debt, job or family event never established | Viewers report conditional pressures without claiming the hypothetical was the character's actual biography |
| B: Pressure versus agency | **P02-F06 / P04-F03** warn pressure imagery may imply the person is helpless or that delay is always correct | Viewers conclude "never build" is the film's prescriptive solution | Viewers explain that which action is useful depends on context and real next contact |
| Both: Placement endpoint | **P01-F04 / P03-F01** warn a neat relational graphic can make placement seem algorithmic | Viewers believe the film selected the one correct customer/contact or guarantees a next move | Viewers articulate a question the person can now ask, alongside unresolved uncertainty |
| Both: Artistic rhythm | **P09-F04** predicts black and selective imagery can help clarify contrasting meanings, but can also be read as dead air | Unprimed viewers describe abrupt emptiness that loses the question | Viewers describe a purposeful contrast or space to register the distinction |

**Status:** These are **registered expectations**, not observed results. Do not fill the observation column until actual variants exist and are seen.

## Update policy for the force matrix

- Each new receipt records **whether the force helped before generation**, not whether an assistant could explain the failure afterward.
- Prefer a **local decision note** after one test, a **candidate question revision** after several independent cases, and broader methodology promotion only with cross-case confirmation.
- Maintain a simple **force use log** showing the cases in which a force was applied, its predicted risk, actual interpretation, misses, false vetoes and revised scope.
- Never silently replace original source claims, approved authorial intent or the current A01 meaning contract to rescue a favored technique.
- When model limitations prevent producing a designed scene, tag it as **production feasibility** rather than reclassifying the thought as impossible to communicate.

## Next gate

Before generating either competing passage-wide rough animatic:
1. Author/director reviews the full spoken-and-seen design hypotheses.
2. Freeze each candidate's provisional script and protected source claims as a *test version*, not final narration.
3. Decide whether to first compare complete rough story treatments or one nested **same-voice** passage slice to isolate a representation mechanism.
4. Then produce, inspect and log results in A06 with the prediction status above.

**There are no reception results for EX-003A/B yet.** The studio's methodology can become better only if failed predictions, unexpected readings and unglamorous false alarms are retained along with successes.


## Author reaction update | B03.11F | 2026-11-15

**Do not alter the pre-registered prediction table above.** This is a subsequent observation entry, clearly separated from the original hypotheses.

**Observer:** author/creative director, already aware of intended narrative, **not blind**.

**Verbatim gist:** The contrast between two situations in B made “the same advice means something else in another context” memorable. The author did **not** feel or recognize the human pressures shown, and judged the smaller-question ending unsuccessful in **both** roughs. Full words captured in [B03.11F scene contract receipt](../stories/001-human-at-the-door/B03.11F_AUTHOR_RECEPTION_SCENE_CONTRACTS_v01.md).

**Narrow conclusions:** B's contextual contrast was **author-recognized** as meaningful. Visual depiction of stakes and placement was **author-rejected** as insufficient. This supplies a concrete next revision target, **not population comprehension**, nor a numeric score proving the force matrix's accuracy.

**Observed/missed risk ledger:**
- **P01-F02/P03 B biography warning:** Author did **not** report inferred specific biography. Mark **not assessed**, not cleared.
- **P02-F06/P04-F03 pressure depiction:** Author reported inability to feel pressure or recognize the scene. Mark **author-observed failure of visual embodiment**, but actual audience generalization indeterminate.
- **P01-F04/P03-F01 placement endpoint:** Author reported ending did not work. Mark **author-observed failed recognitional landing**; the exact viewer misreading (algorithmic selection vs no perceptual change) remains **unresolved**.
- **P02-F03 A recipe reading:** Not explicitly tested by this feedback; remain **unknown**.
- **P09-F04 black holds:** Not explicitly evaluated; remain **unknown**.
- **B4 context contrast:** Positive author perception, which can inform candidate design but is **not** a post-hoc force-prediction success.

**Next prospective test:** Pressure P1 vs P2 and Recognition R1 vs R2, keeping the working B4 conditional contrast where possible. The scene contract document specifies what would falsify each design before generation.
