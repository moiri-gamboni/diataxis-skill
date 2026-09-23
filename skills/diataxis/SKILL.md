---
name: diataxis
description: This skill should be used when writing, reviewing, or restructuring documentation — when the user asks to "write the docs", "write a tutorial", "add a how-to guide", "document this feature/API", "improve the README", or says the documentation is confusing, incomplete, or hard to navigate. Also applies whenever a task produces or substantially edits documentation for any practitioner reader, human or agent — docs sites, guides, READMEs, manuals, runbooks, CLAUDE.md files, skills — even if the user never says "documentation".
---

# Diátaxis

Diátaxis (https://diataxis.fr, Daniele Procida) holds that documentation serves practitioners of a craft, who have exactly four kinds of need, so there are exactly four kinds of documentation, each written differently. Most documentation failures are one kind bleeding into another.

This file is a router. The files in `references/` are the diataxis.fr text itself and are authoritative over any summary here. **Before writing, rewriting, or reviewing a document of a given kind, read the matching reference file in full**: the craft is in the detail, which is deliberately not duplicated here.

## The four kinds

| | Tutorials | How-to guides | Reference | Explanation |
|---|---|---|---|---|
| answers | "Can you teach me to...?" | "How do I...?" | "What is...?" | "Why...?" |
| oriented to | learning | goals | information | understanding |
| form | a lesson | a series of steps | dry description | discursive discussion |
| analogy | teaching a child to cook | a recipe | the label on a food packet | an article on culinary history |

## Classify first: the compass

Before writing anything, and whenever a piece of writing feels off, ask two questions:

1. Does this content inform **action** (practical steps, doing) or **cognition** (facts, thinking)?
2. Does it serve the **acquisition** of skill (study) or the **application** of skill (work)?

| informs | serves | → it belongs to |
|---|---|---|
| action | acquisition | a tutorial |
| action | application | a how-to guide |
| cognition | application | reference |
| cognition | acquisition | explanation |

Apply the compass at any scale: a whole document, a section, a sentence. Content whose answers differ from its container's belongs elsewhere: move it or link to it. A planned document that would serve two needs is two documents.

## Routing: read before writing

| Task | Read in full first |
|---|---|
| Write or revise a tutorial, getting-started, or onboarding lesson | `references/tutorials.md` |
| Write or revise a how-to guide, troubleshooting guide, or task recipe | `references/how-to-guides.md` |
| Write or revise reference material (API/CLI/config/schema description) | `references/reference.md` |
| Write or revise explanation (concepts, background, design discussion) | `references/explanation.md` |
| Audit, reorganise, or incrementally improve an existing docs corpus | `references/workflow.md` |
| Justify the framework, resolve a classification dispute, or reason about doc quality itself | `references/theory.md` |

Each per-kind file includes the boundary discussion with the kind it is most often confused with (tutorials ↔ how-to guides, reference ↔ explanation), so one file covers one task. For a mixed task, such as documenting a new feature end to end, read each file when you reach that kind, not all four up front.

## The discipline, compressed

- **Tutorials**: a learning experience, not knowledge transfer. Concrete steps, visible results early and often, a narrative of what to expect, perfect reliability. Minimise explanation ruthlessly; never offer choices or alternatives.
- **How-to guides**: address a real user goal, not a tool's operations ("how to integrate performance monitoring", never "using the monitoring API"). Assume competence. Action only: no teaching, no digression.
- **Reference**: neutral, austere, consistent description of the machinery, structured like the machinery itself. Illustrate with examples; never instruct, explain, or opine.
- **Explanation**: discursive treatment of a topic to deepen understanding: context, history, design reasons, alternatives, even opinion. Title it so an implicit "About ..." fits. Keep it bounded, with no instructions or exhaustive description creeping in.

In a tutorial or how-to guide, one sentence of why plus a link is the most explanation allowed; a paragraph is a defect. Link to reference and explanation rather than inlining them.

## Failure modes to resist

1. **Conflating tutorial and how-to guide**, the most common error in software docs. A tutorial serves study (teacher responsible, contrived setting, single safe path); a how-to serves work (user responsible, real world, forks and edge cases). "Basic vs advanced" is *not* the distinction.
2. **Scaffolding four empty sections up front.** Never create empty `tutorials/ how-to/ reference/ explanation/` directories; structure emerges from improved content.
3. **"Balancing" a document.** A page improves by becoming purely one kind and linking to the others, not by getting a bit of each.
4. **Assuming every product needs all four kinds fully populated.** Diátaxis is a map for checking bearings, not a plan to complete.

## Working on existing documentation

For incremental improvement, follow `references/workflow.md`: pick one piece, assess it with the compass, make one improvement, complete it, repeat. Many small published improvements beat a grand reorganisation.

For a requested large-scale restructure, first classify the existing pages (per page or section: current kind, target kind, misplaced content and its destination), present that assessment and the proposed moves, and get confirmation before moving or rewriting anything: moving documentation breaks inbound links, reader habits and version history, so the analysis is cheap and the move is not.

## Scope

Diátaxis governs documentation whose reader is a practitioner using a product or craft: docs sites, READMEs, user guides, API docs, runbooks, onboarding material. It does not govern code comments, commit messages, changelogs, marketing copy, academic papers, or internal planning documents, though the compass's two questions often clarify what a confused document of any sort is trying to be.
