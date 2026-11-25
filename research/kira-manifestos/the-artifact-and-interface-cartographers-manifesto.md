---
title: "The Artifact and Interface Cartographer's Manifesto"
type: manifesto
domain:
  - artifacts-and-interfaces
  - domain-cartography
tags:
  - type/manifesto
  - domain/artifacts-and-interfaces
  - layer/invisible
aliases:
  - The Artifact and Interface Cartographer's Manifesto
  - Design of Artifacts and Interfaces
created: 2026-08-04
revised: 2026-08-05
version: 4
status: candidate-canon
author: Trevor + Claude (K2M Cartographic Engine)
source-manifesto: "[[the-domain-cartographers-manifesto]]"
adversarial-review: in-progress 2026-08-05
revision_note: "v4 — rebuilt in the native K2M mastery-map house form. Supersedes v1 (academic-lite) and v2/v3 (wrong register)."
---

# THE ARTIFACT AND INTERFACE CARTOGRAPHER'S MANIFESTO
## A Map of the Action Field Beneath the Screen — and What the Designer Cannot See

---

> The map is not the territory.
>
> But an interface is not the surface — it is a field of action that decides what a person can intend, do, understand, recover, and author.
>
> Every interface presents itself as a screen to make easy. The master sees the loop from intention to authored consequence.
>
> This document maps that field.

---

## PREAMBLE: THE DOMINANT MISUNDERSTANDING

You believe interface design makes things easy.

Arrange the screen, cut the clicks, clarify the labels, and eventually the interface disappears into effortless use. The best interface is invisible; friction is failure; and if the user struggles, the design was not simple enough.

This is what the surface teaches, because the surface *is* the screen — the clean layout, the satisfying tap, the frictionless flow.

But an interface configures a *field of action*. It helps a person translate intention into operation, perceive state, interpret feedback, anticipate consequence, recover from error, coordinate across artifacts, and return to unfinished work — distributing effort and authority as it goes. The best interface does not always disappear; sometimes it must become unmistakably visible — when money moves, medication is delivered, a model changes, or a generated proposal is about to become an action.

**Mastery is NOT:**
- Believing the best interface always disappears
- Treating all friction as bad and "frictionless" as a virtue everywhere
- Mistaking an affordance for a visual cue, or feedback for recovery
- Treating "user error" as the explanation
- Confusing a fast assisted artifact with learning, or an editable label with authorship

**Mastery IS:**
- Asking whether *this* receptor can form an intention, find a handle, understand the state, see what changed, recover in proportion to consequence, and remain an author
- Classifying recovery: reversible, compensable, reviewable, irreversible
- Scaling the safety envelope to consequence, not importing "frictionless"
- Reading workarounds as evidence about the plan, not user resistance
- Keeping the person's correction consequential downstream

The governing question is the receptor's whole loop, from intention to authored consequence.

---

## PART I: THE FOUR LAYERS OF THE ACTION FIELD

### Layer 1: The Visible
Screens, labels, buttons, forms, handles, prompts, diagrams, alerts, generated text.
**What lives here:** the rendered surface people call "the design."
**The trap:** appearance mistaken for the field of action it configures.

### Layer 2: The Mechanics
Mappings, modes, constraints, defaults, feedback, latency, permissions, reversibility, persistence.
**What lives here:** the relation between action and state.
**The trap:** mechanics without dynamics produce designers who add confirmations without classifying recovery.

### Layer 3: The Dynamics
Mental models, workarounds, information search, handoffs, external representations, roles, assistive technologies, histories.
**What lives here:** how the same interface behaves across bodies, tasks, and institutions.
**The trap:** dynamics without invisible forces produce analysts who see use vary and cannot name why.

### Layer 4: The Invisible
Whose goal defines "ease," who absorbs failure, which body counts as ordinary, what becomes durable, what stays contestable, and where a suggestion becomes an institutional or physical act.
**What lives here:** the native forces of Part III.
More exacting than the surface, because it must explain a "usable" interface that harms.

---

## PART II: THE PROVINCE MAP

### Domain Boundary
The design and critique of artifacts and interfaces as fields of action — physical controls, documents, forms, workflows, software, collaborative records, safety systems, and generative surfaces.

### In-Scope Provinces
1. **Cognitive engineering** — gulfs of execution and evaluation.
2. **Direct manipulation** — persistent representation, visible consequence.
3. **Situated action** — plans as resources, not determinants.
4. **Distributed cognition** — thought across people, artifacts, time.
5. **Affordances & signifiers** — action possibility vs. perceptible cue.
6. **Information architecture & foraging** — scent, disclosure, findability.
7. **Boundary objects & standards** — shared artifacts across groups.
8. **History-enriched objects** — temporal continuity and its surveillance risk.
9. **Deceptive design** — constraint gradients that capture consent.
10. **Safety-critical & generative systems** — envelopes, probabilistic agency.

### Omission Ledger

| Province | Why omitted | Risk created | Return priority |
|---|---|---|---|
| Visual & graphic design craft | Aesthetics is adjacent, not the field | Under-serves surface makers | Medium |
| Software engineering | Implementation is its own domain | Treats the artifact, not the codebase | Medium |
| Product economics & business model | Who benefits is touched, not mapped | Under-treats incentive design | High |
| Hardware & industrial ergonomics | Physical-device design needs its own province | Keeps forces mostly digital | Medium |

---

## PART III: THE ELEVEN NATIVE FORCES

### FORCE I: Translation Distance
**Surface Pattern:** a person knows what they want but cannot locate, specify, or evaluate the operation.
**Invisible Mechanism:** intention and system action/state use mismatched vocabularies; the gulfs of execution and evaluation widen (Norman's "Cognitive Engineering").
**Second-Order Force:** people memorize rituals, avoid features, or blame themselves.
**Application:** trace goal → available action → state transition → perceptible evidence → interpretation.
**Changes Diagnosis:** when a feature goes unused, measure the translation distance before adding a tooltip.
**Transplant Test:** "make it intuitive" is a slogan; the specific mechanism — the *gulfs of execution and evaluation* between intention and system state — is native to cognitive engineering.
**Failure Mode:** one-click execution that shortens one gulf while hiding consequence and recovery.

### FORCE II: State Legibility
**Surface Pattern:** actors cannot distinguish draft/final, local/shared, test/live, proposal/commitment.
**Invisible Mechanism:** consequential state is hidden, transient, or scattered; direct manipulation works by joining persistent representation to visible consequence (Shneiderman).
**Second-Order Force:** people repeat actions, build shadow records, and over-trust tone.
**Application:** define the smallest persistent state vocabulary, its audience, and transition evidence.
**Changes Diagnosis:** when actions are repeated or trust is lost, check whether state is legible.
**Transplant Test:** "show status" is generic; the specific mechanism — *consequential system state* made continuously legible to action — is native to direct-manipulation design.
**Failure Mode:** exposing every variable as noise, or hiding the mode that changes meaning.

### FORCE III: Consequence Coupling
**Surface Pattern:** action feels controllable when its effect is quick and near; uncertain when delayed, displaced, or delegated.
**Invisible Mechanism:** temporal, spatial, or causal distance separates operation from consequence.
**Second-Order Force:** loose coupling invites duplicate action, automation surprise, and false attribution.
**Application:** show diagnostic effect near action; preview and label remote and delayed consequences.
**Changes Diagnosis:** when users act blindly, measure the distance from action to visible effect.
**Transplant Test:** "give feedback" is generic; the specific mechanism — *action–consequence coupling distance* in a manipulable system — is native to interaction design.
**Failure Mode:** immediate response rewarding a proxy while long-horizon consequences stay hidden.

### FORCE IV: Recovery Horizon
**Surface Pattern:** some mistakes invite play; others create anxiety because correction is obscure, costly, public, or impossible.
**Invisible Mechanism:** reversibility changes with operation, elapsed time, affected parties, and repair authority.
**Second-Order Force:** narrow recovery creates caution, rehearsal, and covert workarounds.
**Application:** classify actions as reversible, compensable, reviewable, or irreversible; design checkpoints accordingly.
**Changes Diagnosis:** when users freeze, locate the recovery horizon.
**Transplant Test:** "add undo" is generic; the specific mechanism — a *recovery horizon* that "undo" cannot cross once an effect enters another person or system — is native to interaction/safety design.
**Failure Mode:** "undo" that lies after an effect crossed into another person, institution, or model state.

### FORCE V: Constraint Gradient
**Surface Pattern:** paths differ in effort, visibility, default status, and consequence.
**Invisible Mechanism:** constraints, defaults, and friction redistribute probability and labor before a choice appears (FTC dark-patterns; the Amazon "Iliad" case).
**Second-Order Force:** gradients can scaffold safety or capture consent and institutional interest.
**Application:** map effort in both directions, the result of inaction, who benefits, and whether refusal stays meaningful.
**Changes Diagnosis:** when a flow "converts," ask whose goal the gradient serves.
**Transplant Test:** "defaults matter" is broad; the specific mechanism — an *interface constraint gradient* redistributing probability and labor, protectively or coercively — is native to interaction design and deceptive-design research.
**Failure Mode:** ease evaluated without asking whose goal it serves.

### FORCE VI: Affordance–Receptor Fit
**Surface Pattern:** an action is obvious to one actor and absent, unsafe, or impossible to another.
**Invisible Mechanism:** action possibility, signifier, bodily capacity, convention, and assistive technology do or do not align (Gaver; Norman's "Affordances, Conventions, and Design").
**Second-Order Force:** repeated mismatch becomes exclusion, dependence, or presumed incompetence.
**Application:** separate actual action, cue, mapping, required technique, and equivalent operation; test with plural bodies.
**Changes Diagnosis:** when someone "can't," locate the misfit, not the deficit.
**Transplant Test:** "design for accessibility" is a slogan; the specific mechanism — an *affordance* as a relation between action possibility and a particular receptor — is native to interaction design and disability studies.
**Failure Mode:** a visual cue mistaken for access; a "universal" solution erasing incompatible needs.

### FORCE VII: Cognitive Distribution
**Surface Pattern:** performance changes when tools, layout, collaborators, or records change, even if the individual does not.
**Invisible Mechanism:** cognitive work is carried and transformed across people, artifacts, spaces, and time (Hollan/Hutchins/Kirsh).
**Second-Order Force:** good representations compound coordination; bad ones create invisible maintenance and brittle dependence.
**Application:** trace where information originates, changes form, waits, moves, becomes authoritative, and can be corrected.
**Changes Diagnosis:** when a team's output shifts, look at the distributed representations, not just the people.
**Transplant Test:** "context matters" is generic; the specific mechanism — cognition *distributed and transformed across an artifact ecology* — is native to distributed-cognition HCI.
**Failure Mode:** offloading that becomes dumping, adminware, or surveillance.

### FORCE VIII: Situated Drift
**Surface Pattern:** real use departs from the designed sequence through interruption, shortcut, workaround, and repair.
**Invisible Mechanism:** plans under-specify unfolding circumstances; actors recruit locally available resources (Suchman).
**Second-Order Force:** drift can create resilience or normalize unsafe, unpaid, invisible labor.
**Application:** compare official flow with observed conduct; treat workaround clusters as diagnostic.
**Changes Diagnosis:** when users deviate, read the plan's blindness before the user's error.
**Transplant Test:** "reality differs from the plan" is generic; the specific mechanism — a *plan as a resource for situated action*, reworked at the point of use — is native to situated-action HCI.
**Failure Mode:** romanticizing workarounds, or forcing compliance by removing adaptive capacity.

### FORCE IX: Temporal Continuity
**Surface Pattern:** the artifact shows what exists now but not how it arrived, what changed, or which earlier state governed a decision.
**Invisible Mechanism:** digital surfaces strip or hide history although work unfolds across interruptions, actors, and versions (Hill & Hollan's Edit Wear / Read Wear).
**Second-Order Force:** selected trace supports re-entry and attribution; total trace creates surveillance and frozen identity.
**Application:** preserve selected versions, transitions, authorship, and rollback under explicit retention and access rules.
**Changes Diagnosis:** when re-entry or attribution fails, check what history the surface discarded.
**Transplant Test:** "keep a log" is generic; the specific mechanism — *interaction history* made visible to support re-entry while risking surveillance — is native to history-enriched-object design.
**Failure Mode:** version history that cannot reconstruct meaning, or every interaction as a performance metric.

### FORCE X: Safety Envelope
**Surface Pattern:** the same usability feature behaves differently as consequence, uncertainty, and reversibility rise.
**Invisible Mechanism:** risk emerges from the interaction of user, interface, device, environment, training, organization, and downstream system (Leveson & Turner's Therac-25; Three Mile Island).
**Second-Order Force:** consumer heuristics migrate into high-stakes settings; warnings replace design.
**Application:** identify critical tasks, hazard paths, alarm priority, mode transitions, checks, and worst credible recovery.
**Changes Diagnosis:** when consequence is high, ask whether the design has an envelope or just a warning.
**Transplant Test:** "make it safe" is a slogan; the specific mechanism — a *sociotechnical safety envelope* where the unit is user+interface+organization+downstream — is native to safety-critical HCI.
**Failure Mode:** importing "frictionless" into a high-stakes setting, or a warning label substituting for hazard control.

### FORCE XI: Probabilistic Agency Gap
**Surface Pattern:** fluent systems appear to understand, remember, and act consistently while output varies and language may trigger tools.
**Invisible Mechanism:** inference, updates, personalization, and uncertain environment state separate conversation from deterministic action.
**Second-Order Force:** people overgeneralize competence, inherit machine framing, or lose track of what became durable and external.
**Application:** separate generation, evidence, saved state, recommendation, decision, permission, external effect, and stop route.
**Changes Diagnosis:** when a generative interface acts, locate where the sentence became a durable or external act.
**Transplant Test:** "AI is unpredictable" is generic; the specific mechanism — a *probabilistic, drifting agent* whose conversation can cross into deterministic external action — is native to generative-interface design.
**Failure Mode:** anthropomorphic certainty, invisible memory, broad permissions, and no recovery after tool action.

---

## PART IV: THE STAGES OF THE ARTIFACT-AND-INTERFACE CARTOGRAPHER

### Stage 1: Surface → Action Field
**Inner voice:** "It's about how it looks."
Stops equating appearance with design; sees goals, actions, mappings, gulfs. **Trap:** believing the designed path predicts use. **Move:** trace one real intention through the loop.

### Stage 2: Action → State & Consequence
**Inner voice:** "A control needs interpretable state."
Classifies recovery rather than adding confirmations. **Trap:** feedback volume as a good. **Move:** classify actions by recovery horizon.

### Stage 3: Flow → Situated Conduct
**Inner voice:** "Journeys are hypotheses."
Studies interruption, workarounds, repair. **Trap:** "user error" as closure. **Move:** compare official flow with observed conduct.

### ⬇ THE SAFETY & POWER VALLEY — most designers plateau here.
The valley is comfortable because the flow *tests well* and users are happy. Nothing signals that a default is capturing consent, that a "small" action is irreversible for someone, or that consumer "frictionless" is migrating toward a high-stakes context. Crossing it means scaling requirements to consequence and asking whose goal the ease serves.

### Stage 4: Individual → Cognitive Ecology
**Inner voice:** "Cognition spans artifacts, people, histories."
Sees externalization as coordination, not storage. **Trap:** celebrating extension while ignoring dependency. **Move:** trace the distributed representation.

### Stage 5: Average User → Plural Receptor
**Inner voice:** "Separate affordance from signifier; test equivalent operations."
Recognizes disabled people as design knowers. **Trap:** standards as a ceiling. **Move:** test with plural bodies.

### Stage 6: Ease → Power & Safety
**Inner voice:** "Defaults and friction distribute labor and authority."
Scales requirements to consequence and recovery. **Trap:** treating ease as neutral. **Move:** build a safety envelope.

### Stage 7: Artifact → Temporal & Probabilistic Governance
**Inner voice:** "Design evolving systems with memory, ownership, and uncertain behavior."
Preserves inspectability, correction, access, and human authority — not disappearance.

---

## PART V: THE TOOLKIT

**Tool 1 — Action-Loop Trace.** Goal → action → state → evidence → interpretation → recovery → authorship.
**Tool 2 — State Vocabulary.** Smallest persistent state, its audience, and transition evidence.
**Tool 3 — Recovery Classifier.** Reversible | compensable | reviewable | irreversible.
**Tool 4 — Constraint-Gradient Map.** Effort both directions, result of inaction, who benefits, whether refusal is meaningful.
**Tool 5 — Affordance/Signifier Split.** Actual action, cue, mapping, required technique, equivalent operation.
**Tool 6 — Distributed-Representation Trace.** Where information originates, changes, waits, becomes authoritative, and can be corrected.
**Tool 7 — Workaround Study.** Observed conduct vs. official flow; clusters as evidence.
**Tool 8 — History & Retention Rule.** Selected versions, transitions, authorship, rollback, access.
**Tool 9 — Safety Envelope.** Critical tasks, hazards, alarms, modes, checks, worst credible recovery.
**Tool 10 — Generative-Legibility Card.** Generation, evidence, saved state, recommendation, decision, permission, external effect, stop.

---

## PART VI: DIAGNOSTICS

1. Can this receptor form the intention and find the handle?
2. Is the consequential state legible, and is the mode obvious?
3. How far is action from visible consequence?
4. Is this action reversible, compensable, reviewable, or irreversible?
5. Whose goal does the constraint gradient serve?
6. Is this a real affordance for this body, or a cue mistaken for access?
7. Where does information become authoritative, and who can correct it?
8. Do workarounds signal resilience or normalized unsafe labor?
9. As consequence rises, is there an envelope — or only a warning?

---

## PART VII: CASE TRACES

**VisiCalc (Shneiderman)** — direct manipulation joined persistent representation, incremental action, and visible consequence; not merely pointing instead of typing. **Forces:** State Legibility (II), Consequence Coupling (III).

**Suchman's Xerox copier** — plans and scripted dialogue did not determine situated conduct; local trouble, talk, and repair organized action. **Forces:** Situated Drift (VIII).

**Ship navigation (Hutchins)** — cognition across crew, charts, instruments, procedure, and space. **Forces:** Cognitive Distribution (VII).

**Edit Wear / Read Wear (Hill & Hollan)** — visible interaction history supported re-entry while raising ownership and surveillance problems. **Forces:** Temporal Continuity (IX).

**Therac-25 (Leveson & Turner)** — overdoses emerged from software, interface behavior, engineering assumptions, and regulation; "operator error" cannot carry it. **Forces:** Safety Envelope (X), Recovery Horizon (IV).

**Three Mile Island** — abundant alarms did not guarantee interpretable state; more feedback was not the missing law. **Forces:** State Legibility (II), Safety Envelope (X).

**Mars Climate Orbiter** — a unit mismatch became a failed organizational handoff; a boundary artifact must preserve semantics and tests. **Forces:** Cognitive Distribution (VII), boundary handoff.

**Hawai'i false ballistic-missile alert** — test/live mode, situated interpretation, high-consequence action, and slow correction formed one safety problem. **Forces:** Safety Envelope (X), State Legibility (II).

**Amazon "Iliad" flow (FTC)** — asymmetrical enrollment and cancellation; ease evaluated against whose goal the interface serves. **Forces:** Constraint Gradient (V).

---

## PART VIII: RESEARCH SPINE

### Foundational / Durable

| Source | Posture | Supports | Bias / Caution |
|---|---|---|---|
| Norman, "Cognitive Engineering" | academic / HCI | Translation Distance (I) | Foundational; linear-use critique needed. |
| Shneiderman, "Direct Manipulation" | academic / HCI | State Legibility (II), Consequence Coupling (III) | Pre-web examples. |
| Suchman, *Plans and Situated Actions* | academic / work practice | Situated Drift (VIII) | Specific settings. |
| Hollan, Hutchins & Kirsh, "Distributed Cognition" | academic / HCI | Cognitive Distribution (VII) | Programmatic. |
| Gaver, "Technology Affordances" | academic / HCI | Affordance–Receptor Fit (VI) | Affordance debate is live. |
| Norman, "Affordances, Conventions, and Design" | academic / HCI | Affordance–Receptor Fit (VI) | Clarifies signifier vs. affordance. |
| Pirolli & Card, "Information Foraging" | academic / HCI | disclosure, scent | Bounded to search/IA. |
| Star & Griesemer, "Boundary Objects" | academic / sociology | boundary plasticity | Often over-extended. |
| Hill & Hollan, "History-Enriched Digital Objects" | academic / HCI | Temporal Continuity (IX) | Prototype-era; governance open. |
| Leveson & Turner, "Therac-25 Accidents" | academic / safety | Safety Envelope (X) | Foundational accident analysis. |
| FTC dark-patterns report & Amazon complaint | official / regulator | Constraint Gradient (V) | Jurisdictional; dated case. |

### Current Source Pointers
- Norman, "Cognitive Engineering": https://ics.uci.edu/~dfredmil/inf233-FQ07/oldpapers/Norman1986ch3.pdf · Shneiderman, "Direct Manipulation": https://www.cs.umd.edu/~ben/papers/Shneiderman1983Direct.pdf · Suchman: https://www.cambridge.org/core/books/abs/humanmachine-reconfigurations/plans/486980BE0B03AE3DF9C2181D74F26E64 · Hollan/Hutchins/Kirsh: https://escholarship.org/uc/item/8sb9s5rm
- Gaver: https://www.lri.fr/~mbl/Stanford/CS477/papers/Gaver-CHI1991.pdf · Norman, "Affordances…": https://cs.uwaterloo.ca/~jianzhao/cs449-649/files/affordance-norman99.pdf · Pirolli & Card: https://citeseerx.ist.psu.edu/document?doi=59f1e446fab201399d84ae48156ea7bd05c4439b&repid=rep1&type=pdf · Hill & Hollan: https://hci.ucsd.edu/hollan/Pubs/JH1993-1.pdf · Leveson & Turner: https://web.mit.edu/6.033/2004/wwwdocs/papers/Therac_1.html
- FTC dark patterns: https://www.ftc.gov/reports/bringing-dark-patterns-light · FTC v. Amazon: https://www.ftc.gov/system/files/ftc_gov/pdf/2023-09-20-067-AmendedComplaint%28redacted%29.pdf · WCAG 2.2: https://www.w3.org/TR/WCAG22/ · Hamraie, "Designing Collective Access": https://dsq-sds.org/article/ojs_id/3871/ · NRC Three Mile Island: https://ww2.nrc.gov/reading-rm/doc-collections/fact-sheets/3mile-isle · NASA Mars Climate Orbiter: https://llis.nasa.gov/llis_lib/pdf/1009464main1_0641-mr.pdf · Hawai'i EMA: https://dod.hawaii.gov/wp-content/uploads/2018/01/report2018-01-29-181149.pdf · NIST AI RMF 1.0: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf

### Case Evidence

| Case | Source | Forces |
|---|---|---|
| VisiCalc / direct manipulation | Shneiderman | II, III |
| Xerox copier | Suchman | VIII |
| Ship navigation | Hutchins | VII |
| Edit Wear / Read Wear | Hill & Hollan | IX |
| Therac-25 | Leveson & Turner | X, IV |
| Three Mile Island | NRC | II, X |
| Mars Climate Orbiter | NASA | VII |
| Hawai'i false alert | Hawai'i EMA | X, II |
| Amazon "Iliad" | FTC | V |

### Source-Bias Risks & Unresolved
- Foundational sources give durable mechanisms and named cases, not universal laws; regulator/standards sources are jurisdictional floors; platform-operator sources (Microsoft/IBM guidelines) carry incentives.
- **Unresolved:** whether Boundary Plasticity is a distinct force here or covered elsewhere; how the Probabilistic Agency Gap evolves as agents gain persistent memory and tools; where the "scent gradient" belongs (folded into Affordance–Receptor Fit, Situated Drift, and disclosure).

---

## PART IX: THE PRESSURE-REPRESENTATION CROSSING

> K2M synthesis — directional design inferences.

Under pressure, preserve the goal/action distinction and offer one bounded handle without taking the decision (Translation Distance). Mark the current edge, what changed, who can see it, and what remains undecided (State Legibility). Do not let immediate recognition masquerade as durable change — name the later return test (Consequence Coupling). Keep interpretation drafts reversible and require authored confirmation before durable or external claims (Recovery Horizon). Protect deliberate choice without making correction, refusal, or deletion harder than compliance (Constraint Gradient). Match the representation grammar to the present receptor without declaring one compressed form humane for everyone (Affordance–Receptor Fit). Give load a place, then ask who owns and can challenge it (Cognitive Distribution). Evaluate the artifact in the next live pressure scene, not the calm workshop (Situated Drift). Build correction trails and re-entry objects, not permanent dossiers (Temporal Continuity). As consequence rises, separate orientation aid from diagnosis, authority, and executable decision (Safety Envelope). And preserve the line among the person's model, the generated proposal, the durable record, and the authorized action (Probabilistic Agency Gap).

---

## CREED: THE ARTIFACT-AND-INTERFACE CARTOGRAPHER'S OATH

I will not mistake the screen for the field of action.

I will not treat every disappearance as mastery or every friction as failure.

I will separate affordance from cue, and feedback from recovery.

I will classify recovery before I ship the action.

I will ask whose goal the ease serves.

I will read the workaround as evidence about my plan.

I will scale the safety envelope to the consequence, not import "frictionless."

I will keep the person's correction consequential downstream.

I will preserve the line between a generated sentence and an authorized act.

No artifact is validated by the calm clarity of its presentation. Return it to the body, the workflow, the interruption, and the consequence for which it was made.