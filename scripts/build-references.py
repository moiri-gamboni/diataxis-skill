#!/usr/bin/env python3
"""Regenerate skills/diataxis/references/*.md from upstream/source/*.rst.

Each output file concatenates the diataxis.fr pages relevant to one task, so a
reader loads one file and gets everything that matters for that task. The text
is Daniele Procida's, converted mechanically (rst -> GitHub markdown via pandoc,
then the cleanups below); no sentences are rewritten.

Cleanups applied after pandoc:
- images and Sphinx layout wrappers (cssclass, figure) dropped
- sidebar divs become blockquotes
- the grid-item comparison layout (tutorials-how-to) becomes a two-column table
- `Title <target>` cross-reference stubs become italic text
"""

import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "upstream" / "source"
OUT = ROOT / "skills" / "diataxis" / "references"

# output file -> ordered upstream pages. The pairwise contrast pages are
# deliberately duplicated into both files they contrast: whichever single file
# is loaded, the reader gets the distinction that guards against the most
# common conflations.
FILES = {
    "tutorials.md": ["tutorials.rst", "tutorials-how-to.rst"],
    "how-to-guides.md": ["how-to-guides.rst", "tutorials-how-to.rst"],
    "reference.md": ["reference.rst", "reference-explanation.rst"],
    "explanation.md": ["explanation.rst", "reference-explanation.rst"],
    "workflow.md": ["how-to-use-diataxis.rst", "compass.rst"],
    "theory.md": ["theory.rst", "foundations.rst", "map.rst", "quality.rst"],
}


def pandoc(rst_path: Path) -> str:
    rst = rst_path.read_text()
    # A rubric is a keynote sentence; pandoc renders it as a bold line, which
    # breaks when the sentence itself contains bold. Turn it into a plain
    # paragraph (directive marker dropped, continuation lines dedented).
    rst = re.sub(
        r"^\.\.\s+rubric:: ([^\n]*(?:\n[ \t]+[^\n]+)*)",
        lambda m: re.sub(r"\n[ \t]+", " ", m.group(1)),
        rst, flags=re.M,
    )
    return subprocess.run(
        ["pandoc", "-f", "rst", "-t", "gfm", "--wrap=none"],
        input=rst, check=True, capture_output=True, text=True,
    ).stdout


def convert_grids(lines: list[str]) -> list[str]:
    """Pair up grid-item blocks into a two-column Tutorial/How-to table."""
    out, i = [], 0
    while i < len(lines):
        if lines[i].startswith('<div class="grid"'):
            depth, cells, cell = 1, [], None
            i += 1
            while i < len(lines) and depth > 0:
                line = lines[i]
                if line.startswith("<div"):
                    depth += 1
                    if 'class="grid-item"' in line:
                        cell = []
                elif line.startswith("</div>"):
                    depth -= 1
                    if cell is not None and depth == 1:
                        cells.append(" ".join(x for x in cell if x.strip()))
                        cell = None
                elif cell is not None:
                    cell.append(line.strip())
                elif re.fullmatch(r"[\d ]+", line.strip()) or not line.strip():
                    pass  # column-spec line like "1 2 2 2", or padding
                i += 1
            out.append("| Tutorials | How-to guides |")
            out.append("|---|---|")
            for a, b in zip(cells[0::2], cells[1::2]):
                out.append(f"| {a} | {b} |")
            out.append("")
        else:
            out.append(lines[i])
            i += 1
    return out


def convert_sidebars(lines: list[str]) -> list[str]:
    out, i = [], 0
    while i < len(lines):
        if lines[i].startswith('<div class="sidebar"'):
            depth, body = 1, []
            i += 1
            while i < len(lines) and depth > 0:
                if lines[i].startswith("<div"):
                    depth += 1
                elif lines[i].startswith("</div>"):
                    depth -= 1
                    if depth == 0:
                        break
                body.append(lines[i])
                i += 1
            i += 1  # past closing </div>
            while body and not body[0].strip():
                body.pop(0)
            while body and not body[-1].strip():
                body.pop()
            out.append("")
            for b in body:
                out.append(f"> {b}".rstrip())
            out.append("")
        else:
            out.append(lines[i])
            i += 1
    return out


def clean(md: str) -> str:
    lines = md.splitlines()
    lines = [l for l in lines if not l.lstrip().startswith("<img ")
             and not re.fullmatch(r"!\[[^\]]*\]\([^)]*\)", l.strip())]
    lines = convert_grids(lines)
    lines = convert_sidebars(lines)

    out, skip_depth, in_figure = [], 0, False
    for line in lines:
        # figures carry only images and photo credits; drop them whole
        if line.startswith("<figure"):
            in_figure = True
            continue
        if line.startswith("</figure>"):
            in_figure = False
            continue
        if in_figure:
            continue
        # drop remaining wrapper divs (cssclass etc.) and their one-word bodies
        if line.startswith("<div"):
            skip_depth += 1
            continue
        if line.startswith("</div>"):
            skip_depth = max(0, skip_depth - 1)
            continue
        if skip_depth and line.strip() in ("lined", ""):
            continue
        out.append(line)

    text = "\n".join(out)
    # `Title <target>` cross-reference stubs -> italic title
    text = re.sub(r"`([^`<>]+?) <[\w./-]+>`", r"*\1*", text)
    # <span class="title-ref">x</span> leftovers, if any
    text = re.sub(r'<span class="title-ref">([^<]*)</span>', r"*\1*", text)
    # rst lines wrapped after a spaced hyphen rejoin as "word -word"; restore the space
    text = re.sub(r"(\w) -(\w)", r"\1 - \2", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def main() -> None:
    commit = (ROOT / "upstream" / "COMMIT").read_text().strip()
    OUT.mkdir(parents=True, exist_ok=True)
    for name, sources in FILES.items():
        parts = [
            f"<!-- Generated by scripts/build-references.py on {date.today()} — do not edit by hand.\n"
            f"     Text by Daniele Procida, from https://diataxis.fr (CC BY-SA 4.0),\n"
            f"     source pages {', '.join(sources)} @ {commit[:12]}.\n"
            f"     Modifications: format conversion and concatenation only (see script docstring). -->\n"
        ]
        for src in sources:
            parts.append(clean(pandoc(SRC / src)))
        (OUT / name).write_text("\n\n".join(parts))
        print(f"wrote {OUT / name}", file=sys.stderr)


if __name__ == "__main__":
    main()
