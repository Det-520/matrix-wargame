#!/usr/bin/env python3
"""Read game.toml, the one file of scenario facts the tools need.

    from game import GAME           # in a tool: the parsed config, with defaults filled in
    python3 tools/game.py KEY.PATH  # print one value for a shell script (e.g. map.name)

Standard library only (tomllib, Python 3.11 or later).
"""
import os
import sys
import tomllib

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

DEFAULTS = {
    "game": {"name": "Operation Example", "designer": "", "event": "", "date": "", "date_short": "",
             "tables": 1, "rules_label": "Matrix Wargame", "rules_date": ""},
    "turns": {"total": 7, "requests_per_turn": 3, "planning_requests": 4, "secret_coas": 2},
    "sides": {"red": "REDFOR", "blue": "BLUEFOR"},
    "map": {"svg": "map/source/map.svg", "name": "game_map", "tiles": 3},
    "tq": [],
}


def load(path=os.path.join(ROOT, "game.toml")):
    with open(path, "rb") as f:
        data = tomllib.load(f)
    out = {}
    for key, default in DEFAULTS.items():
        if isinstance(default, dict):
            out[key] = {**default, **data.get(key, {})}
        else:
            out[key] = data.get(key, default)
    return out


GAME = load()


def map_pdf(kind):
    """map/maps/<name>_full.pdf or _tiles_letter.pdf, relative to the project root."""
    return f"map/maps/{GAME['map']['name']}_{kind}.pdf"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    val = GAME
    for part in sys.argv[1].split("."):
        val = val[part]
    print(val)
