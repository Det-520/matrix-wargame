#!/usr/bin/env python3
"""Read game.toml, the one file of scenario facts the tools need, and fill in the documents
that quote it.

    from game import GAME           # in a tool: the parsed config, with defaults filled in
    from game import render         # markdown (a Jinja2 template) -> markdown for this game
    python3 tools/game.py KEY.PATH  # print one value for a shell script (e.g. map.name)

The markdown in handouts/, scenario/, and the design documents is a Jinja2 template:
{{ requests }}, {{ mins(turn_min) }}, {% if rules == "full" %} ... {% endif %}. context()
lists every name a template can use. The run-of-show texts in game.toml (say, brief) are
templates too. Reading game.toml needs only the standard library (tomllib, Python 3.11 or
later); render() needs jinja2.
"""
import os
import re
import sys
import tomllib

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

DEFAULTS = {
    "game": {"name": "Operation Example", "designer": "", "event": "", "date": "", "date_short": "",
             "tables": 1, "rules_label": "Matrix Wargame", "rules_date": ""},
    "turns": {"requests_per_turn": 3, "planning_requests": 4, "secret_coas": 2, "game_days": 3},
    "rules": {"set": "full"},
    "side": [],
    "map": {"svg": "map/source/map.svg", "name": "game_map", "tiles": 3},
    "schedule": {"start": "", "parley": 2, "flex_step": "", "flex_options": []},
    "block": [],
    "turn_step": [],
    "track": [],
    "tq": [],
}


# A side's colour when game.toml gives none, in the order the sides are listed.
PALETTE = ["#0969da", "#cf222e", "#6e7781", "#1a7f37", "#bc4c00", "#8250df"]
LEGACY_STEP_SIDE = {"blue": "bluefor", "red": "redfor"}
RESERVED_IDS = {"common", "whitecell", "word", "assets", "intel", "design"}
RESERVED_PREFIXES = {"X", "S"}   # X- third-party counters, S- starting conditions


def sides_from(data):
    """The player teams, in briefing order, with every field filled in. An old game.toml's
    [sides] red/blue table (names only) gives the two default teams."""
    raw = data.get("side")
    if raw is None:
        old = data.get("sides", {})
        raw = [{"id": "bluefor", "label": "BLUEFOR", "nation": old.get("blue", "BLUEFOR"), "prefix": "B"},
               {"id": "redfor", "label": "REDFOR", "nation": old.get("red", "REDFOR"), "prefix": "R"}]
    out = []
    for i, s in enumerate(raw):
        sid = str(s.get("id", "")).strip()
        label = s.get("label") or sid.upper()
        cells = []
        for c in s.get("cell", []):
            cid = str(c.get("id", "")).strip()
            cells.append({"id": cid, "name": c.get("name") or cid, "short": c.get("short") or cid.upper()[:4],
                          "lead": c.get("lead", ""), "job": c.get("job", "")})
        out.append({"id": sid, "label": label, "nation": s.get("nation") or label,
                    "prefix": s.get("prefix") or label[:1].upper(), "color": s.get("color") or PALETTE[i % len(PALETTE)],
                    "cells": cells, "folder": f"{label} - 24H RELEASE"})
    return out


def load(path=os.path.join(ROOT, "game.toml")):
    with open(path, "rb") as f:
        data = tomllib.load(f)
    out = {}
    for key, default in DEFAULTS.items():
        if isinstance(default, dict):
            out[key] = {**default, **data.get(key, {})}
        else:
            out[key] = data.get(key, default)
    out["side"] = sides_from(data)
    for s in out["turn_step"] + [st for b in out["block"] for st in b.get("step", [])]:
        if s.get("side") in LEGACY_STEP_SIDE:  # side = "blue" / "red", from before [[side]]
            s["side"] = LEGACY_STEP_SIDE[s["side"]]
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
    if not isinstance(g["turns"]["game_days"], (int, float)) or g["turns"]["game_days"] <= 0:
        errs.append("[turns] game_days must be a number of days above 0 (0.5 = 12 hours)")
    if g["rules"]["set"] not in RULE_SETS:
        errs.append(f"[rules] set = {g['rules']['set']!r} must be one of: " + ", ".join(RULE_SETS))
    flex = g["schedule"]["flex_step"]
    if flex and flex not in [s.get("id") for s in g["turn_step"]]:
        errs.append(f"[schedule] flex_step = {flex!r} names no [[turn_step]] id")
    for t in g["track"]:
        vals = track_values(t)
        if t.get("start") not in vals:
            errs.append(f"[[track]] {t.get('name', '?')}: `start` must be one of its values")
    errs += check_sides(g)
    if errs:
        sys.exit("game.toml:\n  " + "\n  ".join(errs))


def check_sides(g):
    errs, seen = [], {"id": set(), "label": set(), "prefix": set()}
    if len(g["side"]) < 2:
        errs.append("[[side]]: a game needs at least two player teams")
    for s in g["side"]:
        at = f"[[side]] {s['id'] or '?'}"
        if not re.fullmatch(r"[a-z][a-z0-9-]*", s["id"]) or s["id"] in RESERVED_IDS:
            errs.append(f"{at}: `id` must be lowercase letters, digits, or hyphens (it names a folder), "
                        f"and not one of {', '.join(sorted(RESERVED_IDS))}")
        if not re.fullmatch(r"[A-Z]", s["prefix"]) or s["prefix"] in RESERVED_PREFIXES:
            errs.append(f"{at}: `prefix` must be one capital letter other than X (third parties) and S (starting conditions)")
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", s["color"]):
            errs.append(f"{at}: `color` must be #rrggbb")
        for k in seen:
            if s[k] in seen[k]:
                errs.append(f"{at}: another side has the same `{k}` ({s[k]})")
            seen[k].add(s[k])
        cids = [c["id"] for c in s["cells"]]
        for c in s["cells"]:
            if not re.fullmatch(r"[a-z][a-z0-9-]*", c["id"]):
                errs.append(f"{at} cell {c['id'] or '?'}: `id` must be lowercase letters, digits, or hyphens")
            if cids.count(c["id"]) > 1:
                errs.append(f"{at}: two cells have the id {c['id']}")
    ids = {s["id"] for s in g["side"]}
    for st in g["turn_step"] + [x for b in g["block"] for x in b.get("step", [])]:
        if st.get("side") and st["side"] not in ids:
            errs.append(f"step {st.get('name', '?')}: side = {st['side']!r} names no [[side]] id")
    return errs


def warnings(g=None):
    """Advice, not errors: things Mouat's Practical Advice on Matrix Games warns against."""
    g = g or GAME
    out = []
    if g["turns"]["total"] < 6:
        out.append(f"the run of show has {g['turns']['total']} turns; Mouat recommends at least 6, so each team "
                   "lives with the consequences of its moves through two cycles of action, reaction, and counteraction")
    if len(g["side"]) > 2 and len(g["side"]) % 2:
        out.append(f"{len(g['side'])} player teams: Mouat finds an even number of actors plays best, since the insight "
                   "comes from action and counteraction; give the odd team objectives that conflict with every other team")
    turn_sides = {st.get("side") for st in g["turn_step"]}
    for s in g["side"]:
        if g["turn_step"] and s["id"] not in turn_sides:
            out.append(f"no [[turn_step]] has side = \"{s['id']}\", so {s['label']} has no COA or Cons slot in a turn")
    return out


# ---------------------------------------------------------------- templates

RULE_SETS = ("full", "basic")   # [rules] set; a template asks {% if rules == "full" %}
WORDS = ["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
         "eleven", "twelve"]


def clock_len(m):
    """Minutes as m:ss (5 -> 5:00, 0.5 -> 0:30)."""
    sec = round(m * 60)
    return f"{sec // 60}:{sec % 60:02d}"


def mins(m):
    """5 -> '5 minutes', 1 -> '1 minute', 0.5 -> '30 seconds'."""
    if m < 1:
        return f"{round(m * 60)} seconds"
    return f"{fmt_num(m)} minute{'' if m == 1 else 's'}"


def word(n):
    """4 -> 'four' (up to twelve; larger numbers stay digits)."""
    return WORDS[n] if isinstance(n, int) and 0 <= n < len(WORDS) else fmt_num(n)


def days(n, adj=False):
    """Game time in the unit a planner would use: 0.5 -> '12 hours', 3 -> '3 days',
    7 -> '1 week', 21 -> '3 weeks', 30 -> '1 month', 90 -> '3 months'. adj=True gives '3-day' (a 3-day window)."""
    if n < 1:
        q, unit = round(n * 24), "hour"
    elif n >= 60 or n % 30 == 0:
        q, unit = round(n / 30), "month"
    elif n % 7 == 0:
        q, unit = int(n // 7), "week"
    else:
        q, unit = n, "day"
    q = fmt_num(q)
    return f"{q}-{unit}" if adj else f"{q} {unit}{'' if q == '1' else 's'}"


def join(items, conj="and"):
    """['A', 'B', 'C'] -> 'A, B, and C'; two items take no comma."""
    items = list(items)
    if len(items) < 3:
        return f" {conj} ".join(items)
    return ", ".join(items[:-1]) + f", {conj} " + items[-1]


def team_rows(row, g=None):
    """One table row per team. `row` is the cells between the outer pipes, with {label}, {prefix},
    {nation}, and {id} filled in for each team. Write the line as | {{ team_rows("{label} | {prefix}1") }} |
    so the markdown stays one valid table row."""
    g = g or GAME
    return " |\n| ".join(row.format(**x) for x in g["side"])


def span(a, b):
    return f"{a}–{b}" if a != b else f"{a}"


def ticks(first=1, mark="☐"):
    """One tick-grid cell a turn, as table cells: '☐ | ☐ | ...'. Turns before `first` get '—'."""
    return " | ".join("—" if t < first else mark for t in range(1, GAME["turns"]["total"] + 1))


def turn_columns():
    """The tick grid's turn headings: 'T1 | T2 | ...'."""
    return " | ".join(f"T{t}" for t in range(1, GAME["turns"]["total"] + 1))


def turn_rule():
    """The tick grid's separator cells under turn_columns()."""
    return " | ".join("---" for _ in range(GAME["turns"]["total"]))


def context(g=None, rule_set=None):
    """Every name a template can use. Numbers stay numbers, so templates can do sums
    ({{ days(game_days * turns) }}); mins(), clock(), word(), Word(), and days() format them."""
    g = g or GAME
    t = g["turns"]
    turn_len = sum(s["min"] for s in g["turn_step"])
    slips = t["planning_requests"] + t["total"] * t["requests_per_turn"]
    c = {
        "rules": rule_set or g["rules"]["set"],
        "game": g["game"],
        "sides": g["side"],                         # the player teams, in briefing order
        "side": {x["id"]: x for x in g["side"]},    # side.redfor.label, .nation, .prefix, .cells
        "teams": join([x["label"] for x in g["side"]]),            # "BLUEFOR and REDFOR"
        "teams_or": join([x["label"] for x in g["side"]], "or"),   # "BLUEFOR or REDFOR"
        "team_boxes": " ".join("☐ " + x["label"] for x in g["side"]),  # a form's tick boxes
        "team_slash": "/".join(x["label"] for x in g["side"]),     # "BLUEFOR/REDFOR"
        "first_team": g["side"][0]["label"],
        "team_order": ", ".join(x["label"] for x in g["side"][:-1]) + ", then " + g["side"][-1]["label"],  # "BLUEFOR, then REDFOR"
        "cells": any(x["cells"] for x in g["side"]),   # some team works in cells (RULES.md §9.4)
        "turn_min": turn_len,                       # minutes in one turn
        "turns": t["total"],                        # turns in the game
        "game_days": t["game_days"],                # days of game time a turn stands for
        "requests": t["requests_per_turn"], "planning_requests": t["planning_requests"],
        "secret_coas": t["secret_coas"], "parley": g["schedule"]["parley"],
        "slips": slips, "slip_pages": -(-slips // 3),
        "mins": mins, "clock": clock_len, "word": word, "Word": lambda n: word(n).capitalize(), "days": days,
        "ticks": ticks, "turn_columns": turn_columns, "turn_rule": turn_rule, "team_rows": team_rows,
    }
    flex = next((s for s in g["turn_step"] if s.get("id") and s["id"] == g["schedule"]["flex_step"]), None)
    c["flex"] = ", then ".join(clock_len(m) for m in g["schedule"]["flex_options"] if flex and m < flex["min"])
    steps, at = {}, 0.0
    for s in g["turn_step"]:   # steps.ID.start / end / min (minutes into the turn), .span ('5:00–7:00')
        if s.get("id"):
            steps[s["id"]] = dict(name=s["name"], start=at, end=at + s["min"], min=s["min"],
                                 span=f"{clock_len(at)}–{clock_len(at + s['min'])}")
        at += s["min"]
    blocks = {}
    for b in run_of_show(g):   # blocks.TAG.start / end (clock times), .span, .min, and .first / .last / .turns
        if not b.get("tag"):
            continue
        e = dict(name=b["name"], start=clock_time(b["start"], g), end=clock_time(b["end"], g), min=b["end"] - b["start"])
        e["span"] = f"{e['start']}–{e['end']}"
        if b.get("turns"):
            e.update(first=b["first"], last=b["last"], turns=span(b["first"], b["last"]))
        blocks[b["tag"]] = e
        for s in b["steps"]:
            if s.get("requests_due"):  # the planning step that ends when its requests are due
                c["request_deadline"] = s["end"] - b["start"]
                c["request_deadline_at"] = clock_time(s["end"], g)
    c["steps"], c["blocks"] = steps, blocks
    return _whole(c)


def _whole(v):
    """12.0 -> 12, all the way down, so a template prints '12', not '12.0'."""
    if isinstance(v, dict):
        return {k: _whole(x) for k, x in v.items()}
    return int(v) if isinstance(v, float) and v.is_integer() else v


def values(g=None):
    """context() without the functions: the numbers and texts, for tools and for listing."""
    return {k: v for k, v in context(g).items() if not callable(v)}


CODE = re.compile(r"^```.*?^```|`[^`\n]+`", re.M | re.S)
_ENV = None


def outside_code(fn, text):
    """fn applied to the markdown with its code spans and blocks held back, so an example
    quoted in backticks (`{{ requests }}`) is printed as written."""
    held = []

    def hold(m):
        held.append(m.group(0))
        return f"\x00{len(held) - 1}\x00"
    out = fn(CODE.sub(hold, text))
    return re.sub(r"\x00(\d+)\x00", lambda m: held[int(m.group(1))], out)


def render(text, where="markdown", rule_set=None, extra=None):
    """A template (markdown, or a game.toml text) filled in for this game. Stops with the
    file and line if it names something that doesn't exist."""
    global _ENV
    import jinja2
    if _ENV is None:
        _ENV = jinja2.Environment(undefined=jinja2.StrictUndefined, keep_trailing_newline=True,
                                  trim_blocks=True, lstrip_blocks=True, autoescape=False)
    ctx = context(rule_set=rule_set)
    if extra is not None:
        ctx.update(extra)
    elif "_table(" in text:
        from schedule import tables  # the generated tables: {{ schedule_table() }}, {{ turn_clock_table() }}
        ctx.update(tables(rule_set))

    def one(t):
        # A block tag alone on its line vanishes with its line (trim_blocks, lstrip_blocks); one that
        # ends a line of text keeps the line break ({% endif +%}), so paragraphs don't run together.
        t = re.sub(r"(?m)^(.*\S.*?)\{%([^%]*?)(?<![+-])%\}$",
                   lambda m: m.group(0) if m.group(1).strip().startswith("{%") and m.group(1).strip().endswith("%}")
                   else f"{m.group(1)}{{%{m.group(2)}+%}}", t)
        try:
            return _ENV.from_string(t).render(ctx)
        except jinja2.TemplateError as e:
            line = getattr(e, "lineno", None)
            sys.exit(f"{where}{':' + str(line) if line else ''}: {e.__class__.__name__}: {e.message}")
    return outside_code(one, text)


def game_texts(g=None, rule_set=None):
    """game.toml with its run-of-show texts (name, brief, say) filled in. {turn}, {first},
    {last}, and {min} stay for fill() and the timer program."""
    import copy
    g = copy.deepcopy(g or GAME)
    for s in g["turn_step"] + g["block"] + [st for b in g["block"] for st in b.get("step", [])]:
        for k in ("name", "brief", "say"):
            if isinstance(s.get(k), str) and ("{{" in s[k] or "{%" in s[k]):
                s[k] = render(s[k], where=f"game.toml ({s.get('name', '?')} {k})", rule_set=rule_set, extra={})
    return g


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
    g = game_texts(g)
    sch = g["schedule"]
    blocks = []
    for b in g["block"]:
        e = {k: b[k] for k in ("tag", "short", "name", "brief") if k in b}
        if b.get("turns"):
            e["turns"] = b["turns"]
        else:
            e["steps"] = [{k: s[k] for k in ("name", "min", "who", "side", "say", "brief", "requests_due") if k in s} for s in b["step"]]
        blocks.append(e)
    return {
        "name": g["game"]["name"],
        "rules": g["rules"]["set"],
        "start": str(sch["start"]),
        "parley": sch["parley"],
        "flex": {"step": sch["flex_step"], "options": sch["flex_options"]} if sch["flex_step"] else None,
        "sides": [{"id": x["id"], "label": x["label"], "color": x["color"]} for x in g["side"]],
        "blocks": blocks,
        "turn": [{k: s[k] for k in ("id", "name", "min", "who", "side", "say", "brief") if k in s} for s in g["turn_step"]],
        "tracks": [{k: t[k] for k in ("id", "name", "values", "range", "start", "ends", "triggers") if k in t}
                   for t in g["track"]],
    }


GAME = load()


def side_of(label_or_id):
    """The side whose id, label, or ID prefix this is (redfor, REDFOR, R), or None."""
    for x in GAME["side"]:
        if label_or_id in (x["id"], x["label"], x["prefix"]):
            return x
    return None


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
