#!/bin/bash
# Refresh upstream/ from the diataxis source repo and rebuild the references.
# Review the resulting diff before committing — a content change upstream may
# also warrant an update to the hand-written SKILL.md summary.
set -euo pipefail

REPO="https://github.com/evildmp/diataxis-documentation-framework"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

git clone --depth 1 "$REPO" "$TMP/src"
rm -f "$ROOT"/upstream/source/*.rst
cp "$TMP"/src/source/*.rst "$ROOT/upstream/source/"
cp "$TMP"/src/LICENSE.rst "$TMP"/src/CITATION.cff "$ROOT/upstream/"
git -C "$TMP/src" rev-parse HEAD > "$ROOT/upstream/COMMIT"

python3 "$ROOT/scripts/build-references.py"
echo "upstream now at $(cat "$ROOT/upstream/COMMIT")"
git -C "$ROOT" status --short
