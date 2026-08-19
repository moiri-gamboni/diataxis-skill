# CLAUDE.md

Claude Code plugin carrying the Diátaxis documentation framework as a skill. The content *is* the product; there is no build beyond regenerating markdown from the vendored source.

## Layout

- `skills/diataxis/SKILL.md` — the hand-written router (summary + compass + routing table). The only prose in this repo we author; keep it a router, not a paraphrase of the framework.
- `skills/diataxis/references/*.md` — **generated**. Never edit by hand; run `python3 scripts/build-references.py` after changing the script or `upstream/`. Concatenation map (which upstream pages feed which file) lives in the script's `FILES` dict.
- `upstream/` — verbatim diataxis.fr `.rst` source + LICENSE + CITATION, pinned by `upstream/COMMIT`. Refresh with `scripts/refresh-upstream.sh` (watch the diff: an upstream content change may also warrant a SKILL.md update).
- `plans/` — design and integration plans (praxis integration lives here).

## Conventions

- Versioning: patch auto-bumped by the pre-commit hook (`ln -sf ../../scripts/pre-commit-version-bump .git/hooks/pre-commit` after cloning — same mechanism as the praxis repo). Claude Code detects plugin updates by version string; an unbumped commit never reaches installed copies. Bump MINOR for new reference files or routing changes, MAJOR for renamed/removed skills.
- License: whole repo CC BY-SA 4.0 (forced by ShareAlike on the Diátaxis text; simplest to keep one license). Preserve the attribution header the build script writes into each generated file.
- SKILL.md style: description frontmatter states WHEN to activate (trigger conditions), not what the workflow is; body in imperative form; keep it lean — detail belongs to the verbatim references, which are authoritative over the summary.

## Deployment (roost)

Installed box-wide on the roost server via `claude plugin marketplace add` + `install`, wired in the server repo's private `files/private/claude-plugins.sh` (roost-private repo) with autoUpdate=true — a push here goes live on the next marketplace refresh, but only if the version was bumped.
