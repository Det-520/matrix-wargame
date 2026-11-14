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
    "turns": {"requests_per_turn": 3, "planning_requests": 4, "secret_coas": 2},
    "sides": {"red": "REDFOR", "blue": "BLUEFOR"},
    "map": {"svg": "map/source/map.svg", "name": "game_map", "tiles": 3},
    "schedule": {"start": "", "parley": 2, "flex_step": "", "flex_options": []},
    "block": [],
    "turn_step": [],
    "track": [],
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
    check(out)
    out["turns"]["total"] = sum(b.get("turns", 0) for b in out["block"])
    return out


def check(g):
    """Stop with a clear message if the run of show or the tracks can't work."""
    errs = []
    for i, b in enumerate(g["block"], 1):
        label = f"[[block]] {i} ({b.get('name', '?')})"
        for f in ("name", "short"):
            if not b.get(f):
                errs.append(f"{label}: needs `{f}`")
        if "turns" in b and b.get("step"):
            errs.append(f"{label}: has both `turns` and steps; split it in two")
        elif "turns" in b and not (isinstance(b["turns"], int) and b["turns"] > 0):
            errs.append(f"{label}: `turns` must be a whole number above 0")
        elif "turns" not in b and not b.get("step"):
            errs.append(f"{label}: needs `turns` or at least one [[block.step]]")
        if b.get("turns") and not g["turn_step"]:
            errs.append(f"{label}: has turns, so game.toml needs [[turn_step]] entries")
        for j, s in enumerate(b.get("step", []), 1):
            if not s.get("name") or not isinstance(s.get("min"), (int, float)) or s["min"] <= 0:
                errs.append(f"{label} step {j}: needs `name` and `min` above 0")
    for j, s in enumerate(g["turn_step"], 1):
        if not s.get("name") or not isinstance(s.get("min"), (int, float)) or s["min"] <= 0:
            errs.append(f"[[turn_step]] {j}: needs `name` and `min` above 0")
    flex = g["schedule"]["flex_step"]
    if flex and flex not in [s.get("id") for s in g["turn_step"]]:
        errs.append(f"[schedule] flex_step = {flex!r} names no [[turn_step]] id")
    for t in g["track"]:
        vals = track_values(t)
        if t.get("start") not in vals:
            errs.append(f"[[track]] {t.get('name', '?')}: `start` must be one of its values")
    if errs:
        sys.exit("game.toml:\n  " + "\n  ".join(errs))


def track_values(t):
    if "range" in t:
        lo, hi = t["range"]
        return list(range(lo, hi + 1))
    return list(t.get("values", []))


def fill(text, **kw):
    """Fill {turn}, {first}, {last}, {min} in a schedule text, leaving other braces alone."""
    for k, v in kw.items():
        text = text.replace("{" + k + "}", fmt_num(v))
    return text


def fmt_num(v):
    return str(int(v)) if isinstance(v, float) and v.is_integer() else str(v)


def run_of_show(g=None):
    """The schedule as a list of blocks, each with its steps and its start and end (minutes
    from the start of the game). A turns block keeps one entry, with a `turns` list of
    (turn number, start, end) and its turn length; `first` and `last` are its turn numbers."""
    g = g or GAME
    turn_len = sum(s["min"] for s in g["turn_step"])
    out, t, n = [], 0.0, 0
    for b in g["block"]:
        e = {k: v for k, v in b.items() if k != "step"}
        e["start"] = t
        if b.get("turns"):
            e["first"], e["last"] = n + 1, n + b["turns"]
            e["turn_len"] = turn_len
            e["turns"] = [(n + i + 1, t + i * turn_len, t + (i + 1) * turn_len) for i in range(b["turns"])]
            n += b["turns"]
            t += b["turns"] * turn_len
            e["steps"] = []
        else:
            steps, s0 = [], t
            for s in b["step"]:
                steps.append({**s, "start": s0, "end": s0 + s["min"]})
                s0 += s["min"]
            e["steps"] = steps
            t = s0
        e["end"] = t
        out.append(e)
    return out


def clock_time(minutes, g=None):
    """'1345' plus minutes as a 24-hour clock time, or elapsed 'h:mm' if no start is set."""
    g = g or GAME
    start = str(g["schedule"]["start"]).replace(":", "")
    total = round(minutes * 60)
    if start:
        base = int(start[:-2]) * 3600 + int(start[-2:]) * 60
        x = (base + total) % 86400
        return f"{x // 3600:02d}{x % 3600 // 60:02d}" + (f":{x % 60:02d}" if x % 60 else "")
    return f"{total // 3600}:{total % 3600 // 60:02d}" + (f":{total % 60:02d}" if total % 60 else "")


def clock_config(g=None):
    """The settings the timer program (tools/whitecell-clock.html) reads, as a dict for JSON."""
    g = g or GAME
    sch = g["schedule"]
    blocks = []
    for b in g["block"]:
        e = {k: b[k] for k in ("tag", "short", "name", "brief") if k in b}
        if b.get("turns"):
            e["turns"] = b["turns"]
        else:
            e["steps"] = [{k: s[k] for k in ("name", "min", "who", "side", "say", "brief") if k in s} for s in b["step"]]
        blocks.append(e)
    return {
        "name": g["game"]["name"],
        "start": str(sch["start"]),
        "parley": sch["parley"],
        "flex": {"step": sch["flex_step"], "options": sch["flex_options"]} if sch["flex_step"] else None,
        "blocks": blocks,
        "turn": [{k: s[k] for k in ("id", "name", "min", "who", "side", "say") if k in s} for s in g["turn_step"]],
        "tracks": [{k: t[k] for k in ("id", "name", "values", "range", "start", "ends", "triggers") if k in t}
                   for t in g["track"]],
    }


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
