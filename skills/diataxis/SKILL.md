---
name: diataxis
description: This skill should be used when writing, reviewing, or restructuring documentation — when the user asks to "write the docs", "write a tutorial", "add a how-to guide", "document this feature/API", "improve the README", or says the documentation is confusing, incomplete, or hard to navigate. Also applies whenever a task produces or substantially edits documentation for any practitioner reader, human or agent — docs sites, guides, READMEs, manuals, runbooks, CLAUDE.md files, skills — even if the user never says "documentation".
---

# Diátaxis

Diátaxis (https://diataxis.fr, Daniele Procida) is a systematic approach to technical documentation. Its core claim: documentation serves practitioners of a craft, and a practitioner has exactly four kinds of need — so there are exactly four kinds of documentation, each written differently. Most documentation failures are one kind bleeding into another.

This file is a router, not the framework. The files in `references/` contain the actual diataxis.fr text, which is authoritative over any summary here. **Before writing, rewriting, or reviewing a document of a given kind, read the matching reference file in full** — the craft is in the detail, and the detail is deliberately not duplicated here.

## The four kinds

| | Tutorials | How-to guides | Reference | Explanation |
|---|---|---|---|---|
| answers | "Can you teach me to...?" | "How do I...?" | "What is...?" | "Why...?" |
| oriented to | learning | goals | information | understanding |
| serves the user | at study (acquiring skill) | at work (applying skill) | at work | at study |
| informs | action | action | cognition | cognition |
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

Apply the compass at any scale — a whole document, a section, a single sentence. Content whose two answers differ from its container's belongs somewhere else: move it (or link to it), don't leave it. If a planned document would serve two needs, that is two documents.

## Routing: read before writing

| Task | Read in full first |
|---|---|
| Write or revise a tutorial, getting-started, or onboarding lesson | `references/tutorials.md` |
| Write or revise a how-to guide, troubleshooting guide, or task recipe | `references/how-to-guides.md` |
| Write or revise reference material (API/CLI/config/schema description) | `references/reference.md` |
| Write or revise explanation (concepts, background, design discussion) | `references/explanation.md` |
| Audit, reorganise, or incrementally improve an existing docs corpus | `references/workflow.md` |
| Justify the framework, resolve a classification dispute, or reason about doc quality itself | `references/theory.md` |

Each per-kind file also contains the boundary discussion with the kind it is most often confused with (tutorials ↔ how-to guides; reference ↔ explanation), so one file is enough for one task. For a mixed task — e.g. documenting a new feature end to end — read each file at the point of writing that kind, not all four up front. The mode files matter most; summaries do not substitute for them.

## The discipline, compressed

- **Tutorials**: provide a learning experience, not knowledge transfer. Concrete steps, visible results early and often, a narrative of what to expect, perfect reliability. Ruthlessly minimise explanation and never offer choices or alternatives.
- **How-to guides**: address a real user goal, not a tool's operations ("how to integrate performance monitoring", never "using the monitoring API"). Assume competence. Action only — no teaching, no digression; link to reference and explanation instead of inlining them.
- **Reference**: neutral, austere, consistent description of the machinery, structured to mirror the machinery itself. Illustrate with examples, but never instruct, explain, or opine.
- **Explanation**: discursive treatment of a topic to deepen understanding — context, history, design reasons, alternatives, even opinion. Title it so an implicit "About ..." fits. Keep it bounded; no instructions or exhaustive description creeping in.

## Failure modes to actively resist

1. **Conflating tutorial and how-to guide** — the single most common error in software docs. A tutorial serves study (teacher responsible, contrived setting, single safe path); a how-to serves work (user responsible, real world, forks and edge cases). "Basic vs advanced" is *not* the distinction.
2. **Explanation creep in tutorials and how-to guides** — a sentence of why ("we use HTTPS because it's safer") plus a link is the maximum; a paragraph is a defect.
3. **Instruction or discussion creep in reference** — reference describes; it never walks through tasks or argues.
4. **Machinery-perspective how-to guides** — restating what buttons do is not guidance; guides answer to human projects.
5. **Creating four empty sections up front** — never scaffold `tutorials/ how-to/ reference/ explanation/` directories with nothing in them. Structure must emerge from improved content, not precede it.
6. **"Balancing" a document** — a page is not improved by giving it a bit of each kind; it is improved by becoming purely one kind and linking to the others.
7. **Assuming every product needs all four quadrants fully populated** — Diátaxis is a map for checking bearings, not a plan to complete.

## Working on existing documentation

For incremental improvement, follow `references/workflow.md`: pick one piece, assess it with the compass, make one improvement, complete it, repeat. Prefer many small published improvements over a grand reorganisation.

For a requested large-scale restructure: first classify the existing pages (per page or section: current kind, target kind, misplaced content and its destination), present that assessment and the proposed moves, and get confirmation before moving or rewriting anything. Moving documentation is destructive to inbound links, reader habits, and version control history; the analysis is cheap, the move is not.

## Scope

Diátaxis applies to documentation whose reader is a practitioner using a product or craft: docs sites, READMEs, user guides, API docs, runbooks, onboarding material. It does not govern code comments, commit messages, changelogs, marketing copy, academic papers, or internal planning documents — though the compass's *action/cognition* and *study/work* questions often still clarify what a confused document of any sort is trying to be.
