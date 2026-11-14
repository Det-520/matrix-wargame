#!/usr/bin/env bash
# Build everything in build/ from the markdown (see tools/build_handouts.py).
#   tools/build_handouts.sh              # schedule tables and timer settings (game.toml), counters,
#                                        # Tongue and Quill documents, then every release PDF
#   tools/build_handouts.sh --only Brief # pass options through to build_handouts.py
# On NixOS this pulls the Python packages with nix-shell (tools/pyenv.sh). Elsewhere, install
# jinja2, markdown-it-py, mdit-py-plugins, pypdf, and playwright.
# SKIP_TQ=1 uses the Tongue and Quill files already in handouts/word/ (CI has no WordCraft).
set -euo pipefail
cd "$(dirname "$0")/.."
. tools/pyenv.sh
if [ -z "${CHROMIUM_PATH:-}" ]; then
  CHROMIUM_PATH=$(command -v chromium || ls -d /nix/store/*-chromium-*/bin/chromium 2>/dev/null | head -1 || true)
  export CHROMIUM_PATH
fi
py tools/schedule.py --write
python3 -I tools/check_assets.py
python3 -I tools/make_counters.py
[ -n "${SKIP_TQ:-}" ] || python3 -I tools/tq/build_tq.py
py tools/build_handouts.py "$@"
