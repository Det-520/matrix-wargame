#!/usr/bin/env bash
# Build the printable map from the master SVG named in game.toml [map] (see map/README.md):
#   map/maps/<name>.png               2x raster
#   map/maps/<name>_full.pdf          one page at the scale of the assembled tiles
#   map/maps/<name>_tiles_letter.pdf  N x N letter tiles to trim and tape
#   handouts/assets/game-map.png      the image the Scenario Brief embeds
# Needs pdftoppm (poppler-utils) and Chromium. The Inter fonts in map/fonts/
# (tools/fetch_third_party.py) are used if the SVG names them.
# On NixOS this pulls the Python packages with nix-shell. Elsewhere, install playwright.
set -euo pipefail
cd "$(dirname "$0")/.."
SVG=$(python3 -I tools/game.py map.svg)
NAME=$(python3 -I tools/game.py map.name)
TILES=$(python3 -I tools/game.py map.tiles)
if [ -z "${CHROMIUM_PATH:-}" ]; then
  CHROMIUM_PATH=$(command -v chromium || ls -d /nix/store/*-chromium-*/bin/chromium 2>/dev/null | head -1 || true)
  export CHROMIUM_PATH
fi
export FONTCONFIG_FILE=$PWD/map/fonts/fonts.conf
mkdir -p map/maps handouts/assets
STEPS="python3 -I map/source/render_png.py $SVG map/maps/$NAME.png 2
python3 -I map/source/build_pdfs.py $SVG map/maps $NAME $TILES"
PY='python3.withPackages (ps: with ps; [playwright])'
if command -v nix-shell >/dev/null; then
  nix-shell -p "$PY" --run "set -e; $STEPS"
else
  bash -ec "$STEPS"
fi
pdftoppm -q -png -scale-to-x 4200 -scale-to-y -1 -singlefile "map/maps/${NAME}_full.pdf" handouts/assets/game-map
echo "wrote map/maps/$NAME*, handouts/assets/game-map.png"
