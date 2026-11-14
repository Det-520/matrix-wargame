#!/usr/bin/env bash
# Generate and build the white cell site with mdbook (site/, see tools/build_site.py).
#   tools/build_site.sh          # pages + mdbook build  -> site/book/
#   tools/build_site.sh serve    # pages + mdbook serve  -> http://localhost:3000
# Run tools/build_handouts.sh first if the PDFs changed: the site copies build/.
# Needs mdbook 0.5 or later; on NixOS without it installed, the script uses nix-shell.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -I tools/schedule.py --write
python3 -I tools/build_site.py
TITLE="$(python3 -I tools/game.py game.name) — White Cell Site"
CMD="build"
[ "${1:-build}" = serve ] && CMD="serve --open"
if command -v mdbook >/dev/null; then
  MDBOOK_BOOK__TITLE="$TITLE" mdbook $CMD site
elif command -v nix-shell >/dev/null; then
  MDBOOK_BOOK__TITLE="$TITLE" nix-shell -p mdbook --run "mdbook $CMD site"
else
  echo "mdbook not found: install it (https://rust-lang.github.io/mdBook/guide/installation.html)" >&2
  exit 1
fi
