# Integrating the diataxis skill with praxis

Status: planned, not implemented. This records how the diataxis plugin should hook into the praxis development pipeline (ideate → design → implement → review → ship), in increasing order of coupling. Written 2026-08-19 against praxis 1.8.1, from a full read of the relevant skill and agent files (`skills/ship`, `skills/implement`, `skills/review`, `agents/implementer.md`, plus a docs-mention sweep across the rest).

## Where praxis currently touches documentation (verified)

- **`agents/implementer.md` step 8** already mandates a docs pass per work unit: *"If documented behavior changed, update README.md and CLAUDE.md. If not, log 'no doc changes needed' explicitly — not silently."* It says nothing about *how* to write those updates.
- **`skills/review/SKILL.md`** already lists *"Documentation update — README, docs"* as a logical-unit type, so doc changes flow through the reviewer fleet — but no reviewer is briefed on documentation form; `praxis:comment-analyzer` covers code comments only.
- **`skills/implement/SKILL.md`** Phase 4 step 7 resolves *conflicting* doc edits from workers; decomposition (Phase 1) has no notion of a documentation unit.
- **`skills/ship/SKILL.md`** is state-driven with no generic checklist. State 1 (on main) is deliberately a single-message, no-questions fast path; States 2/3 (feature branch) verify tests and, in State 2, run `praxis:simplify`. There is no docs gate anywhere.
- **`skills/design/SKILL.md`** already classifies docs as non-behavioral deliverables (verification line instead of a test) — so plans can carry docs tasks; nothing shapes their content.
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

### Level 2 — documentation units in `/praxis:implement` and doc-aware review briefings

- Phase 1 decomposition: a plan touching user-visible behaviour yields a documentation unit in `batch-plan.md` like any other unit (own deliverable, verification line instead of a test surface), depending on the interface-defining units so it dispatches late. The worker is a normal `praxis:implementer`, which with Level 1 already loads the skill.
- `/praxis:review` Step 4: when a logical unit is a documentation update, brief the dispatched reviewer to load `diataxis:diataxis` and review for kind-purity (the compass applied per section) in addition to accuracy.

Adopt only if Level 1 shows docs repeatedly arriving rushed or oversized at ship time; it moves the work earlier at the price of decomposition complexity.

### Level 3 — `/praxis:document` orchestration command

A praxis-side command for corpus-scale work, mirroring `/praxis:review`'s fleet shape: classify pages in parallel (per page: current kind / target kind / misplaced content and destination — the assessment table the diataxis SKILL.md already prescribes) → confirm the move plan with the user → per-kind writers, each loading only its `references/<kind>.md` → a kind-purity review pass. Build only when corpus-scale docs work is actually recurring; for single documents the plain skill suffices and an orchestrator is ceremony.

### Level 4 — incorporation into praxis (fallback, not a goal)

If cross-plugin resolution proves brittle, or praxis must work for users who won't install a second plugin: absorb via praxis's documented new-upstream procedure (add `moiri-gamboni/diataxis-skill` to `upstream.json`, copy `skills/diataxis/` in as `praxis:diataxis`, attribute in `NOTICE` — CC BY-SA 4.0 content coexisting with AGPL praxis the same way its MIT and Apache-2.0 material already does; generated files keep their attribution headers). Cost: a second copy to keep synced (mitigated by `analyze-upstream.sh`) and a concern praxis didn't have. Prefer the standalone plugin while both live on the same boxes.

## Decision points

- Adopt Level 1 after the skill has been exercised on a few real docs tasks, so the hook wording reflects observed use rather than a guess.
- Crux for Level 2: whether ship-time and step-8 docs updates turn out rushed, oversized, or kind-blurred under Level 1. Small correct diffs at ship → Level 1 is the resting state.
- Crux for Level 4: the cross-plugin guard firing more than rarely (praxis sessions without the diataxis plugin installed).
