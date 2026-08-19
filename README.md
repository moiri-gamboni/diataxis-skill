# diataxis-skill

A Claude Code plugin that teaches Claude the [Diátaxis](https://diataxis.fr) documentation framework. It activates when a session writes, reviews, or restructures user-facing documentation, and can be invoked directly as `/diataxis:diataxis`.

## Design

Unlike the many existing Diátaxis skills that paraphrase the framework, this one carries **the actual diataxis.fr text** and layers routing on top. Fidelity is the point: Procida's prose is precise about distinctions (tutorial vs how-to, reference vs explanation) that paraphrases reliably blur.

Three levels of disclosure:

1. **`skills/diataxis/SKILL.md`** — hand-written router: the four kinds, the compass, per-kind discipline in compressed form, failure modes, and a table saying which reference file to read in full for which task.
2. **`skills/diataxis/references/*.md`** — the diataxis.fr pages, converted to markdown and concatenated per task, so one Read covers one job: `tutorials.md`, `how-to-guides.md`, `reference.md`, `explanation.md` (each per-kind file includes the boundary essay for the kind it is most often confused with), `workflow.md` (improving existing docs + the compass), `theory.md` (foundations, the map, quality).
3. **`upstream/`** — the verbatim `.rst` source, license, and citation file, pinned to a commit.

The references are generated, not edited: `scripts/build-references.py` converts `upstream/source/*.rst` with pandoc plus deterministic cleanups (images dropped, sidebars → blockquotes, the tutorial/how-to comparison grid → a two-column table). `scripts/refresh-upstream.sh` re-vendors the source and rebuilds.

## Installation

```bash
/plugin marketplace add moiri-gamboni/diataxis-skill
/plugin install diataxis@diataxis-skill
```

## Maintenance

- Never edit `references/*.md` by hand — change the build script or the upstream copy, then rebuild.
- `scripts/refresh-upstream.sh` pulls the latest diataxis.fr source; review the diff (and whether SKILL.md's summary needs to move with it) before committing.
- Install the version-bump hook after cloning: `ln -sf ../../scripts/pre-commit-version-bump .git/hooks/pre-commit`. Installed plugins only pick up new content when the version changes.

## License and attribution

The Diátaxis text is by **Daniele Procida**, from [diataxis.fr](https://diataxis.fr) ([source repository](https://github.com/evildmp/diataxis-documentation-framework)), used under [CC BY-SA 4.0](LICENSE). Modifications to it are limited to format conversion (reStructuredText → Markdown, images and site navigation removed) and per-task concatenation, as implemented in `scripts/build-references.py`; the verbatim source is preserved under `upstream/`. To cite Diátaxis itself, see `upstream/CITATION.cff`.

Everything else in this repository (the SKILL.md router, scripts, this README) is also released under [CC BY-SA 4.0](LICENSE), so the whole repository shares one license.
