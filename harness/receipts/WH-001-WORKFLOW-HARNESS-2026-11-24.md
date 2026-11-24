# WH-001 | Workflow harness engineering receipt | 2026-11-24

**Status:** Executable foundation verified for one existing scene replay. Overall reliability milestone remains open; creative gate remains blocked. This is not a motion or film approval.

## Evidence and inventory
- Audited 74 local operations, 7 actual ComfyUI workflows, 49 review-evidence files and 3 Blender masters. Registered 9 critical dependencies by SHA256; froze 52 curated operations in the private local registry/snapshot. The original CP05 source and layered Krita master hash checks passed. No private paths, artwork, model weights, credentials or raw user conversations are published.
- Five previously pending HunyuanVideo jobs completed technically; no artistic approval follows.
- The active state, workflow contract, catalogue, instruction bootstrap, runner, independent verifier, scene gate, fixed/rigid layer primitive, handoff checker and test suite are in harness/runtime. The repository now explicitly distinguishes old instructions from the active WH-001 handoff.
- Replay wh001-replay-01 paused at preflight, resumed in a separate process and completed all four stages. Independent verification: 72 frames at 24 fps; exact equality of all decoded frames against the prior prepared-scene v02 video; source first frame, dimensions/count, finite tracks and reported metrics passed. Four independently selected static ROIs (20,125 pixels total) had zero changes before encoding. Duplicate completed-run resume was refused. Original source hashes checked again before receipt.
- Replay verification SHA256 b4e0595cb7de524241340d6610b13e0179be3f9ef87db8340effa031c42cea79; replay output SHA256 bd1a852ed7986e4897622a49e30ac79d6a475613f02a70a20f673839b4119ce1.
- Scene gate ran against actual CP05 prepared assets and returned blocked (no schema/integrity errors): paper under hand, shirt behind pen, head/sleeve reveals lack bound visual review. The independent synthetic fixed/rigid fixture passed, with 12 distinct frames, fixed ROI equality and two forbidden transform rejections. Synthetic transfer is not a second actual creative scene.
- Ten local unit tests passed, including tamper rejection, context and authority, state persistence, entity behavior/dependency rules and handoff failure cases. CI is configured to run public contract tests without private assets.
- Cold independent model entry: Claude failed with expired OAuth; Codex rejected two configured/catalogued model selections for the current account. No model answer was produced. Handoff checker correctly records invocation failure; successful fixture answers are unit-test evidence only. The canonical packet and reusable response checker exist; actual independent model comprehension and model substitution as a creative worker remain unverified.

## Decisions and limits
- Keep n8n and additional model downloads deferred. Technical reproduction of a prior flawed visual is deliberately not artistic validation. Native Blender parity, purposefully prepared Krita/ComfyUI hidden surfaces, actual second-scene transfer, interruption during a running subprocess (as opposed to a controlled checkpoint pause), off-device private backup, and provider-independent creative execution remain unverified.
- The runner has a narrowly scoped, frozen CP05 replay adapter. It is not a general scene-authoring engine. Scene gate verifies artifact identity, declared behavior and review receipts, not artistic truth. The handoff checker validates a bounded orientation answer only; providers must be authenticated/selected separately.
- Do not start the next creative test. Resolve a successful fresh independent model handoff and review the infrastructure branch, then prepare and explicitly validate hidden surfaces before animating. Preserve original source and earlier draft PRs.

## Re-entry
Run `python harness/runtime/runner.py bootstrap`, then read `harness/runtime/README.md` and `harness/runtime/SCENE_READINESS.md`. Local runtime files and full logs remain on TREVOR; private registry required for replay. Public repository records the reusable implementation and sanitized evidence, not local media.
