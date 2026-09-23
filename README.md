# diataxis-skill

A Claude Code plugin that teaches Claude the [Diátaxis](https://diataxis.fr) documentation framework. Claude uses it when a session writes, reviews or restructures user-facing documentation, and you can invoke it directly as `/diataxis:diataxis`.

## Installation

```bash
/plugin marketplace add moiri-gamboni/diataxis-skill
/plugin install diataxis@diataxis-skill
```

## Design

Many Diátaxis skills paraphrase the framework. This one carries **the actual diataxis.fr text** and adds routing on top. Fidelity is the point: Procida's prose is precise about distinctions (tutorial vs how-to guide, reference vs explanation) that paraphrases reliably blur.

Claude reads it in three levels:

1. **`skills/diataxis/SKILL.md`**: the hand-written router. The four kinds, the compass, each kind's discipline in compressed form, the common failure modes, and a table saying which reference file to read in full for which task.
2. **`skills/diataxis/references/*.md`**: the diataxis.fr pages as Markdown, grouped per task so that one read covers one job: `tutorials.md`, `how-to-guides.md`, `reference.md` and `explanation.md` (each includes the essay separating its kind from the one it is most often confused with), `workflow.md` (improving existing documentation, and the compass), `theory.md` (foundations, the map, quality).
3. **`upstream/`**: the verbatim `.rst` source, its license and citation file, pinned to the commit in `upstream/COMMIT`.

## Maintenance

- `references/*.md` are generated, never edited by hand. `scripts/build-references.py` converts `upstream/source/*.rst` with pandoc plus deterministic cleanups (images dropped, sidebars turned into blockquotes, the tutorial/how-to comparison grid turned into a two-column table); change the script or the upstream copy, then rerun it.
- `scripts/refresh-upstream.sh` pulls the latest diataxis.fr source and rebuilds. Review the diff, including whether SKILL.md's summary has to change with it, before committing.
- After cloning, install the version-bump hook: `ln -sf ../../scripts/pre-commit-version-bump .git/hooks/pre-commit`. Installed plugins pick up new content only when the version changes.

## License and attribution

The Diátaxis text is by **Daniele Procida**, from [diataxis.fr](https://diataxis.fr) ([source repository](https://github.com/evildmp/diataxis-documentation-framework)), used under [CC BY-SA 4.0](LICENSE). Modifications to it are limited to format conversion (reStructuredText to Markdown, images and site navigation removed) and per-task concatenation, as implemented in `scripts/build-references.py`; the verbatim source is preserved under `upstream/`. To cite Diátaxis itself, see `upstream/CITATION.cff`.

Everything else in this repository (the SKILL.md router, scripts, this README) is also released under [CC BY-SA 4.0](LICENSE), so the whole repository shares one license.
