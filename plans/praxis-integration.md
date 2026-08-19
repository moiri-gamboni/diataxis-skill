# Integrating the diataxis skill with praxis

Status: Levels 1+2+3 implemented 2026-08-19, merged to praxis master and pushed (88f81d0 four hooks + a41a519 `/praxis:document`, v1.10.1, live on the roost install). The hooks: implementer step 8 + skill-audit range, ship State 2 docs check (the solo-path choke point; skipped when implementer already ran), design doc-task template, review documentation-unit briefing — with the inline-classification decision below applied as specified. Level 3 shipped as `/praxis:document` (parallel classification → assessment table + approval gate → per-kind writers → fresh-eyes kind-purity review; right-sized so single-document work loads the skill inline instead) — built ahead of the corpus-scale gate at Moïri's direction; first real corpus run should calibrate its briefs. This repo went public the same day (license position: whole repo CC BY-SA 4.0, attribution + modification notices in place), resolving the visibility mismatch with public praxis. This records how the diataxis plugin should hook into the praxis development pipeline (ideate → design → implement → review → ship), in increasing order of coupling. Written 2026-08-19 against praxis 1.8.1, from a full read of every praxis skill and agent file (all 13 SKILL.md + 4 supporting docs + 13 agents).

## Where praxis currently touches documentation (verified)

- **`agents/implementer.md` step 8** already mandates a docs pass per work unit: *"If documented behavior changed, update README.md and CLAUDE.md. If not, log 'no doc changes needed' explicitly — not silently."* It says nothing about *how* to write those updates.
- **`skills/review/SKILL.md`** already lists *"Documentation update — README, docs"* as a logical-unit type, so doc changes flow through the reviewer fleet — but no reviewer is briefed on documentation form; `praxis:comment-analyzer` covers code comments only.
- **`skills/implement/SKILL.md`** Phase 4 step 7 resolves *conflicting* doc edits from workers; decomposition (Phase 1) has no notion of a documentation unit.
- **`skills/ship/SKILL.md`** is state-driven with no generic checklist. State 1 (on main) is deliberately a single-message, no-questions fast path; States 2/3 (feature branch) verify tests and, in State 2, run `praxis:simplify`. There is no docs gate anywhere.
- **`agents/code-reviewer.md`** lists "doc completeness" under production readiness (for merge/PR) — so the reviewer fleet already asks *whether* docs exist, just not what form they should take.
- **`agents/trimmer.md`** already polices docs by subtraction: duplicated tables, sections restating code, docs asserting things false of the code, the fresh-maintainer test, and (plan mode) doc deliverables. Complementary, not overlapping: trimmer cuts doc bloat and staleness; diataxis governs kind and form. No conflict — a kind-pure doc is also easier to trim.
- **`skills/design/SKILL.md`** already classifies docs as non-behavioral deliverables (verification line instead of a test), and its Task Structure gives every task a **"Skills to activate"** header (e.g. `praxis:test-driven-development`) — an existing per-task mechanism a doc task could name `diataxis:diataxis` in. Nothing currently shapes doc content.
- **`skills/prototype/SKILL.md`**'s Phase 6 handoff doc was considered and excluded: it is a decision record for the next builder (decisions, tradeoffs, solid-vs-provisional), not practitioner documentation of a craft — forcing it into a Diátaxis kind would fight its purpose. Its "what it is + how to run" line is the one diataxis-shaped fragment, and it is fine as is.
- Praxis references components namespaced (`praxis:review`) with a name-resolution guard: unresolvable references are surfaced, never silently substituted. Cross-plugin references to `diataxis:diataxis` should reuse that pattern, with the surface message naming the fix (`/plugin marketplace add moiri-gamboni/diataxis-skill`).
- Praxis has documented machinery for absorbing an external plugin wholesale (`upstream.json` sources + `NOTICE` + `scripts/analyze-upstream.sh`) — the fallback if cross-plugin coupling proves brittle.

## Integration levels

### Level 0 — auto-activation (already live, no praxis change)

The diataxis skill's description triggers on documentation work in any session, including praxis workers: `praxis:implementer` lists `Skill` among its tools, and plugin skills are visible there. Passive; nothing guarantees the skill is loaded when implementer step 8 fires.

### Level 1 — one-line hooks at the two existing anchors (recommended next step)

Two minimal praxis-side edits, each grafting onto a step that already exists:

1. **`agents/implementer.md` step 8**: before updating docs, load `diataxis:diataxis` (name-resolution guard as usual) and follow its routing — so the already-mandated docs pass writes kind-pure updates instead of ad-hoc prose.
2. **`skills/ship/SKILL.md` State 2** (feature branch, no PR — the path solo work converges on, since the solo workflow never passes through the implementer agent): alongside the existing simplify step, ask whether the diff changes user-visible behaviour with no corresponding doc change; if so, update the docs (loading `diataxis:diataxis`) or state in the PR body that docs are deferred and why. Leave State 1's no-questions fast path untouched — that asymmetry is deliberate in ship's design.

Cost: two short diffs; converts stale-docs from silent omission into explicit decision on both the orchestrated and solo paths.

### Level 2 — documentation tasks named in plans, doc-aware review briefings

- `/praxis:design` Phase 3: a doc-deliverable task lists `diataxis:diataxis` in its existing **"Skills to activate"** header, exactly as behavioral tasks list `praxis:test-driven-development` — the per-task activation mechanism already exists, so this is a template change, not new machinery. `/praxis:implement` decomposition inherits it for free when the plan carries such a task (the unit dispatches after the interface-defining units it documents).
- `/praxis:review` Step 4: when a logical unit is a documentation update, brief the dispatched reviewer to load `diataxis:diataxis` and review for kind-purity (the compass applied per section) in addition to the accuracy and completeness checks code-reviewer already runs.

Adopt only if Level 1 shows docs repeatedly arriving rushed or oversized at ship time; it moves the work earlier at the price of decomposition complexity.

### Level 3 — `/praxis:document` orchestration command

A praxis-side command for corpus-scale work, mirroring `/praxis:review`'s fleet shape: classify pages in parallel (per page: current kind / target kind / misplaced content and destination — the assessment table the diataxis SKILL.md already prescribes) → confirm the move plan with the user → per-kind writers, each loading only its `references/<kind>.md` → a kind-purity review pass. Build only when corpus-scale docs work is actually recurring; for single documents the plain skill suffices and an orchestrator is ceremony.

### Level 4 — incorporation into praxis (fallback, not a goal)

If cross-plugin resolution proves brittle, or praxis must work for users who won't install a second plugin: absorb via praxis's documented new-upstream procedure (add `moiri-gamboni/diataxis-skill` to `upstream.json`, copy `skills/diataxis/` in as `praxis:diataxis`, attribute in `NOTICE` — CC BY-SA 4.0 content coexisting with AGPL praxis the same way its MIT and Apache-2.0 material already does; generated files keep their attribution headers). Cost: a second copy to keep synced (mitigated by `analyze-upstream.sh`) and a concern praxis didn't have. Prefer the standalone plugin while both live on the same boxes.

## Inline shape guidance in praxis: classification yes, rules no

Decided 2026-08-19 (raised by Moïri: should praxis agents/skills themselves recommend specific doc shapes?). Praxis's own TDD integration is the template: inline the *classification gate*, defer all *rules* to the skill loaded fresh at the point of work ("Skills are tool calls, not vibes"). Duplicating compressed shape rules into praxis would recreate the paraphrase-drift problem this skill exists to avoid.

What praxis should carry inline, when Levels 1-2 land:

- **`implementer` step 8**: its current "update README.md and CLAUDE.md" is already an implicit — and wrong — shape policy (everything → README). Replace with kind-aware phrasing: load `diataxis:diataxis`, identify which kinds the change touches, update those docs where the project keeps them.
- **`design` Phase 3 doc tasks**: one line in the task template — name the kind(s) the deliverable serves — so tasks read "update the reference for X", never "update docs".
- **One stable prior, stated once**: feature work almost always touches how-to and reference, sometimes explanation, almost never tutorial. Derives from the framework's structure, so it won't drift; prevents tutorial-voiced READMEs.

Nothing else. Every rule about what a kind looks like stays in the skill.

## Decision points

- Direction (Moïri, 2026-08-19): target is "probably Level 2 + 3" rather than resting at Level 1. Level 1's two hooks are subsumed by Level 2 work (the step-8 rewording above is part of it); Level 3 still gates on a real corpus-scale task to shape the command against.
- Adopt the praxis-side edits after the skill has been exercised on a few real docs tasks, so the hook wording reflects observed use rather than a guess.
- Crux for Level 2: whether ship-time and step-8 docs updates turn out rushed, oversized, or kind-blurred under Level 1. Small correct diffs at ship → Level 1 is the resting state.
- Crux for Level 4: the cross-plugin guard firing more than rarely (praxis sessions without the diataxis plugin installed).
