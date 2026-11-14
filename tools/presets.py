#!/usr/bin/env python3
"""Browse the presets in presets/ and add them to the scenario (presets/README.md).

    python3 tools/presets.py list teams|cells|assets|tracks [--category C] [--service S] [--search TEXT]
    python3 tools/presets.py show KEY                  one preset in full (team, cell, asset, or track)
    python3 tools/presets.py add-cell SIDE [CELL ...]  split a team into cells; no CELL = a checklist to tick
    python3 tools/presets.py add-team TEAM [--id ID] [--label L] [--nation N] [--prefix P] [--color #rrggbb]
                                           [--cells a,b] [--no-assets]
    python3 tools/presets.py add-asset SIDE ASSET [ASSET ...] [--zone Z6] [--availability start|home|rff]
                                           [--visibility visible|hidden] [--cell CELL] [--arrives N+1] [--approval TEXT]
    python3 tools/presets.py add-track TRACK [TRACK ...]
    python3 tools/presets.py reference [--write]       the asset reference (presets/asset-reference.md)

SIDE is a team's id or label (redfor, REDFOR). Every command that changes game.toml checks the
result with tools/game.py first and leaves the file alone if it would not load. Files that already
exist are never overwritten. Needs only the standard library.
"""
import argparse
import csv
import json
import os
import re
import string
import sys
import tempfile
import tomllib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import game  # noqa: E402

ROOT = game.ROOT
PRESETS = os.path.join(ROOT, "presets")
TEMPLATES = os.path.join(PRESETS, "templates")
GAME_TOML = os.path.join(ROOT, "game.toml")
ASSETS_CSV = os.path.join(ROOT, "scenario", "data", "assets.csv")
CATALOG_CSV = os.path.join(PRESETS, "assets.csv")
REFERENCE_MD = os.path.join(PRESETS, "asset-reference.md")
AVAIL = ("start", "home", "rff")


# ---------------------------------------------------------------- catalogs

def toml_list(name, key):
    with open(os.path.join(PRESETS, name), "rb") as f:
        return {x["key"]: x for x in tomllib.load(f).get(key, [])}


def teams():
    return toml_list("teams.toml", "team")


def cells():
    return game.cell_presets()


def tracks():
    return toml_list("tracks.toml", "track")


def assets():
    with open(CATALOG_CSV, newline="", encoding="utf-8") as f:
        return {r["key"]: r for r in csv.DictReader(f)}


CATEGORIES = {
    "fighter": "Fighters and attack aircraft", "bomber": "Bombers and air-delivered mines", "ew": "Electronic warfare",
    "tanker": "Tankers", "airlift": "Airlift", "logistics": "Logistics and sealift", "c2": "Command and control",
    "isr": "Intelligence, surveillance, and reconnaissance", "space": "Space", "cyber": "Cyber",
    "air-defense": "Air and missile defense", "fires": "Long-range fires and coastal defense", "naval": "Naval forces",
    "ground": "Ground forces", "base": "Basing and Agile Combat Employment", "sof": "Special operations",
    "info": "Information and civil affairs", "authority": "Authorities and packages (RFF items, not map counters)",
}


def die(msg):
    sys.exit(f"presets: {msg}")


def find_side(name, g=None):
    g = g or game.GAME
    for s in g["side"]:
        if name in (s["id"], s["label"]):
            return s
    die(f"no team {name!r} in game.toml (teams: {', '.join(s['id'] for s in g['side'])})")


# ---------------------------------------------------------------- listing

def table(rows, cols):
    widths = [max(len(c), *(len(str(r.get(c, ""))) for r in rows)) if rows else len(c) for c in cols]
    widths = [min(w, 60) for w in widths]
    line = lambda vals: "  ".join(str(v)[:w].ljust(w) for v, w in zip(vals, widths))  # noqa: E731
    print(line(cols))
    print(line(["-" * w for w in widths]))
    for r in rows:
        print(line([r.get(c, "") for c in cols]))


def cmd_list(a):
    if a.kind == "teams":
        table([dict(t, cells=",".join(t["cells"])) for t in teams().values()],
              ["key", "label", "prefix", "archetype", "cells"])
    elif a.kind == "cells":
        table(list(cells().values()), ["key", "short", "name", "job"])
    elif a.kind == "tracks":
        table([dict(t, scale=" / ".join(map(str, t["values"])) if "values" in t else f"{t['range'][0]} to {t['range'][1]}")
               for t in tracks().values()], ["key", "name", "scale", "fits"])
    else:
        rows = [r for r in assets().values()
                if (not a.category or r["category"] == a.category)
                and (not a.service or r["service"].lower() == a.service.lower())
                and (not a.cell or r["cell"] == a.cell)
                and (not a.search or a.search.lower() in " ".join(r.values()).lower())]
        table(rows, ["key", "category", "service", "asset", "limitation"])
        if not a.category:
            print("\ncategories: " + ", ".join(CATEGORIES))


def cmd_show(a):
    for kind, cat in (("team", teams()), ("cell", cells()), ("asset", assets()), ("track", tracks())):
        if a.key in cat:
            print(f"# {kind} preset: {a.key}")
            for k, v in cat[a.key].items():
                if v not in ("", [], None):
                    print(f"{k:>12}: {'; '.join(map(str, v)) if isinstance(v, list) and not isinstance(v[0], dict) else v}")
            return
    die(f"no preset {a.key!r}: try `list teams`, `list cells`, `list assets`, `list tracks`")


# ---------------------------------------------------------------- game.toml editing

HEADER = re.compile(r"^\s*\[\[?([A-Za-z0-9_.-]+)\]\]?\s*(#.*)?$")


def headers(lines):
    """(line index, table name) for every live table header in game.toml."""
    return [(i, m.group(1)) for i, ln in enumerate(lines) if (m := HEADER.match(ln))]


def content_end(lines, start, stop):
    """The index just after the last line of real content in lines[start:stop] (skips trailing
    blanks and comments, so an insertion lands before a commented-out example)."""
    i = stop
    while i > start + 1 and (not lines[i - 1].strip() or lines[i - 1].lstrip().startswith("#")):
        i -= 1
    return i


def entry_span(lines, name, k, nested=()):
    """Start and end of the k-th [[name]] entry; the entry runs to the next header that isn't one
    of its own nested tables (side.cell for side)."""
    hs = headers(lines)
    own = [i for i, n in hs if n == name]
    if k >= len(own):
        die(f"game.toml has {len(own)} [[{name}]] entries, expected at least {k + 1}")
    start = own[k]
    stop = next((i for i, n in hs if i > start and n not in nested), len(lines))
    return start, stop


def tval(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return game.fmt_num(v)
    if isinstance(v, str):
        return json.dumps(v, ensure_ascii=False)
    if isinstance(v, dict):
        return "{ " + ", ".join(f"{k} = {tval(x)}" for k, x in v.items()) + " }"
    if isinstance(v, list) and any(isinstance(x, dict) for x in v):
        return "[\n" + "".join(f"  {tval(x)},\n" for x in v) + "]"
    return "[" + ", ".join(tval(x) for x in v) + "]"


def splice(lines, at, new):
    """Insert lines at `at`, with a blank line after them if the next line isn't one."""
    if at < len(lines) and lines[at].strip():
        new = new + [""]
    lines[at:at] = new


def toml_entry(name, d, indent=""):
    return [f"{indent}[[{name}]]"] + [f"{indent}{k} = {tval(v)}" for k, v in d.items()]


def save_toml(lines, what):
    """Write game.toml if the new text loads; otherwise stop and leave it alone."""
    text = "\n".join(lines).rstrip("\n") + "\n"
    fd, tmp = tempfile.mkstemp(suffix=".toml")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        try:
            new = game.load(tmp)
        except SystemExit as e:
            die(f"{what} would break game.toml, so nothing was changed:\n{e}")
        except tomllib.TOMLDecodeError as e:
            die(f"{what} would make game.toml invalid TOML ({e}), so nothing was changed")
    finally:
        os.unlink(tmp)
    with open(GAME_TOML, "w", encoding="utf-8") as f:
        f.write(text)
    return new


def read_lines():
    with open(GAME_TOML, encoding="utf-8") as f:
        return f.read().split("\n")


def write_new(path, text):
    """Write a file that doesn't exist yet; report a skip if it does."""
    rel = os.path.relpath(path, ROOT)
    if os.path.exists(path):
        print(f"  kept   {rel} (already exists)")
        return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"  wrote  {rel}")
    return True


def fill(path, **kw):
    with open(path, encoding="utf-8") as f:
        return string.Template(f.read()).safe_substitute(**kw)


def bullets(items):
    return "\n".join(f"- {x}" for x in items) if items else "- [Add your own.]"


# ---------------------------------------------------------------- cells

def pick_cells(side, catalog):
    have = {c["preset"] or c["id"] for c in side["cells"]}
    keys = list(catalog)
    print(f"Cells for {side['label']}. Tick the ones you want: type their numbers or keys, separated by spaces.")
    print("Most teams want none, or two to four (RULES.md §9.4).\n")
    for n, k in enumerate(keys, 1):
        c = catalog[k]
        print(f"  {n:>2}. [{'x' if k in have else ' '}] {k:<9} {c['name']} — {c['job']}")
        print(f"          {'':<9} Fits: {c.get('fits', '')}")
    try:
        ans = input("\nAdd which? ").replace(",", " ").split()
    except EOFError:
        ans = []
    out = []
    for x in ans:
        k = keys[int(x) - 1] if x.isdigit() and 0 < int(x) <= len(keys) else x
        if k not in catalog:
            die(f"{x!r} is not a cell number or key")
        out.append(k)
    return out


def brief_text(key, c, catalog):
    return fill(os.path.join(TEMPLATES, "cell-brief.md.tmpl"), key=key,
                phase1=c.get("phase1", ""), prepare=c.get("prepare", ""), cons=c.get("cons", ""),
                concern=c.get("concern", ""), rfis=bullets(c.get("rfis", [])), coas=bullets(c.get("coas", [])),
                pros=bullets(c.get("pros", [])),
                works_with=", ".join(catalog[w]["name"] for w in c.get("works_with", []) if w in catalog) or "the commander")


def add_cells(side_name, keys, brief=True, lines=None, g=None, quiet=False):
    """Add cell presets to a team in game.toml and write a brief for each. Returns the new game."""
    catalog = cells()
    g = g or game.GAME
    side = find_side(side_name, g)
    if not keys:
        if not sys.stdin.isatty():
            die("name the cells to add (`python3 tools/presets.py list cells`), or run this in a terminal to pick")
        keys = pick_cells(side, catalog)
    have = {c["id"] for c in side["cells"]}
    keys = [k for k in dict.fromkeys(keys) if k not in have]
    for k in keys:
        if k not in catalog:
            die(f"no cell preset {k!r} (`python3 tools/presets.py list cells`)")
    if not keys:
        print(f"{side['label']}: nothing to add.")
        return g
    lines = lines or read_lines()
    k = [s["id"] for s in g["side"]].index(side["id"])
    start, stop = entry_span(lines, "side", k, nested=("side.cell",))
    at = content_end(lines, start, stop)
    new = []
    for key in keys:
        new += [""] + toml_entry("side.cell", {"preset": key}, "  ")
    splice(lines, at, new)
    g = save_toml(lines, f"adding cells {', '.join(keys)} to {side['label']}")
    print(f"game.toml: {side['label']} now has cells " + ", ".join(c["id"] for c in find_side(side["id"], g)["cells"]))
    if brief:
        for key in keys:
            write_new(os.path.join(ROOT, "handouts", side["id"], "cells", f"{key}.md"), brief_text(key, catalog[key], catalog))
    if not quiet:
        print(f"""
Next:
  - Give each cell its counters: set the `cell` column in scenario/data/assets.csv to the cell's id
    (or `python3 tools/presets.py add-asset {side['id']} KEY --cell {keys[0]}`).
  - Rewrite each brief in handouts/{side['id']}/cells/ for the scenario (its FORMAT NOTE says what to change).
  - Rebuild: the briefs go into the {side['label']} release and the site, and the counters show each cell's short name.""")
    return g


def cmd_add_cell(a):
    add_cells(a.side, a.cells, brief=not a.no_brief)


# ---------------------------------------------------------------- assets

def scenario_rows():
    with open(ASSETS_CSV, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        return r.fieldnames, list(r)


def next_id(prefix, rows, rff):
    lo, hi = (30, 49) if rff else (1, 29)
    used = {int(m.group(1)) for r in rows if (m := re.fullmatch(re.escape(prefix) + r"-(\d+)", r["id"]))}
    n = max([u for u in used if lo <= u <= hi], default=lo - 1) + 1
    while n in used:
        n += 1
    if n > hi:
        die(f"no free {prefix}- number between {lo} and {hi}; give one with --id")
    return f"{prefix}-{n:02d}"


def md_row(cells):
    """A markdown table row, with an empty cell as `| |` (markdownlint's compact style)."""
    return "|" + "|".join(f" {c} " if str(c).strip() else " " for c in cells) + "|"


def owner_of(side):
    label = side["label"]
    return label[:-3] if label.endswith("FOR") and len(label) > 3 else label


def packet_cells(header, r, side):
    """A packet table row for this asset, matched to the table's own columns."""
    vis = "Hidden" if r["visibility"] == "hidden" else "Visible"
    core = r["core_function"].replace(";", ", ") if r["core_function"] else ("Joint" if r["service"] not in ("USAF", "USSF") else "")
    out = []
    for h in header:
        h = h.lower()
        out.append(r["id"] if h == "id" else f"**{r['asset']}**" if h == "asset" else owner_of(side) if h == "owner"
                   else r["zone"].replace(";", ", ") if h == "zone" else vis if h.startswith("vis")
                   else core if h.startswith("core") else r["arrives"] if h.startswith("arriv")
                   else r["approval"] if h.startswith("approval") else r["limitation"] if "limit" in h
                   else r["role"] if "does" in h or h == "role" else "")
    return md_row(out)


SECTION = {"start": ("at start",), "home": ("from home", "at start"), "rff": ("rff pool",)}


def insert_packet_row(side, r):
    """Add the asset's row to the right force table in scenario/<id>-packet.md, if there is one."""
    path = os.path.join(ROOT, "scenario", f"{side['id']}-packet.md")
    if not os.path.exists(path):
        return False
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    for want in SECTION[r["availability"]]:
        for i, ln in enumerate(lines):
            if ln.startswith("#") and want in ln.lower():
                j = i + 1
                while j < len(lines) and not lines[j].startswith("|") and not lines[j].startswith("#"):
                    j += 1
                if j >= len(lines) or not lines[j].startswith("|"):
                    continue
                header = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                end = j
                while end < len(lines) and lines[end].startswith("|"):
                    end += 1
                lines.insert(end, packet_cells(header, r, side))
                with open(path, "w", encoding="utf-8") as f:
                    f.write("\n".join(lines))
                return True
    return False


def oob_row(r):
    ids = r["id"]
    if r["parts"]:
        ids = ", ".join(f"{r['id']}{chr(97 + i)}" for i in range(int(r["parts"])))
    bold = (lambda x: f"**{x}**") if r["visibility"] == "hidden" else (lambda x: x)
    if r["availability"] == "rff":
        return md_row([ids, r["asset"], r["arrives"], r["approval"]])
    asset = r["asset"] + (" (hidden)" if r["visibility"] == "hidden" else "")
    return md_row([bold(x) for x in (ids, asset, r["zone"].replace(";", ", ") or "[Zx]", r["role"], r["limitation"])])


def add_assets(side, keys, zone="", availability=None, visibility=None, cell=None, arrives=None, approval=None,
               asset_id=None, quiet=False):
    """Copy catalog assets into scenario/data/assets.csv and the team's packet. Returns the new rows."""
    catalog = assets()
    fields, rows = scenario_rows()
    cell_ids = {c["id"] for c in side["cells"]}
    if cell and cell not in cell_ids:
        die(f"{side['label']} has no cell {cell!r} (cells: {', '.join(cell_ids) or 'none'})")
    added = []
    for key in keys:
        key, _, avail = key.partition("@")
        if key not in catalog:
            die(f"no asset preset {key!r} (`python3 tools/presets.py list assets --search ...`)")
        c = catalog[key]
        avail = availability or avail or "start"
        if avail not in AVAIL:
            die(f"availability must be one of {', '.join(AVAIL)}, not {avail!r}")
        z = zone
        if c["parts"] and z and len(z.split(";")) != int(c["parts"]):
            die(f"{key} has {c['parts']} parts: give {c['parts']} zones as Z1;Z2;Z3, or no zone")
        rid = asset_id if asset_id and len(keys) == 1 else next_id(side["prefix"], rows, avail == "rff")
        if any(x["id"] == rid for x in rows):
            die(f"{rid} is already in scenario/data/assets.csv")
        r = {f: "" for f in fields}
        r.update(id=rid, side=side["label"], owner=owner_of(side), asset=c["asset"], service=c["service"],
                 availability=avail, zone=z, parts=c["parts"], part_asset=c["part_asset"],
                 visibility=visibility or c["visibility"] or "visible",
                 core_function=c["core_function"], role=c["role"], limitation=c["limitation"],
                 cell=cell if cell else (c["cell"] if c["cell"] in cell_ids else ""),
                 arrives=(arrives or c["arrives"] or "N+1") if avail == "rff" else "",
                 approval=(approval or c["approval"] or "Routine") if avail == "rff" else "")
        rows.append(r)
        added.append(r)
    with open(ASSETS_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    for r in added:
        where = "packet" if insert_packet_row(side, r) else "CSV only: add its row to the packet by hand"
        print(f"  added  {r['id']}  {r['asset']}  ({r['availability']}{', cell ' + r['cell'] if r['cell'] else ''}; {where})")
    if not quiet:
        print("\nOrder of battle rows to paste (handouts/%s/order-of-battle.md):" % side["id"])
        for r in added:
            print("  " + oob_row(r))
        print("\nNext: set each zone (`zone` in the CSV and the packet), rewrite role and limitation for the scenario,\n"
              "then `python3 tools/check_assets.py && python3 tools/make_counters.py`.")
    return added


def cmd_add_asset(a):
    side = find_side(a.side)
    add_assets(side, a.assets, zone=a.zone, availability=a.availability, visibility=a.visibility, cell=a.cell,
               arrives=a.arrives, approval=a.approval, asset_id=a.id)


# ---------------------------------------------------------------- teams

def cmd_add_team(a):
    presets = teams()
    if a.team not in presets:
        die(f"no team preset {a.team!r} (`python3 tools/presets.py list teams`)")
    t = presets[a.team]
    g = game.GAME
    sid = a.id or t["key"]
    label, prefix = a.label or t["label"], a.prefix or t["prefix"]
    nation, color = a.nation or t["nation"], a.color or t["color"]
    for s in g["side"]:
        if sid == s["id"] or label == s["label"] or prefix == s["prefix"]:
            die(f"{s['label']} already uses that id, label, or prefix: pick another with --id, --label, or --prefix")
    if os.path.exists(os.path.join(ROOT, "handouts", sid)):
        die(f"handouts/{sid}/ already exists")
    lines = read_lines()

    # [[turn_step]]: the COA step after the last COA step, the Cons step after the last Cons step,
    # and a minute more for the white cell (RULES.md §2.2, §2.6).
    steps = g["turn_step"]
    own = {s["id"]: [i for i, st in enumerate(steps) if st.get("side") == s["id"]] for s in g["side"]}
    last_coa = max(v[0] for v in own.values())
    last_cons = max(v[1] for v in own.values())
    coa = {"id": f"{sid}-coa", "name": f"{label} COA + Pros", "min": 2, "who": label, "side": sid,
           "say": f"“{label}, your COA.” No interruptions. {label} may react to earlier COAs but not negate them.",
           "brief": "Brief aloud: action, measurable effect, up to 3 reasons. Post the same COA in the group channel before the step ends."}
    cons = {"id": f"{sid}-cons", "name": f"{label} Cons", "min": 1, "who": label, "side": sid,
            "say": f"“{label}, your Cons, against any of the other teams' COAs.”",
            "brief": "Up to 3 Cons in total, against any of the other teams' COAs: name the COA each one is against. "
                     "Post them in the group channel before the step ends."}
    hs = [i for i, n in headers(lines) if n == "turn_step"]
    _, cons_stop = entry_span(lines, "turn_step", last_cons)
    cons_at = content_end(lines, hs[last_cons], cons_stop)
    coa_at = hs[last_coa + 1]
    res = next((i for i, st in enumerate(steps) if st.get("id") == "res"), None)
    bumped = ""
    if res is not None:
        r0, r1 = entry_span(lines, "turn_step", res)
        for i in range(r0, r1):
            m = re.match(r"^(min\s*=\s*)([\d.]+)(.*)$", lines[i])
            if m:
                old = float(m.group(2))
                lines[i] = f"{m.group(1)}{game.fmt_num(old + 1)}{m.group(3)}"
                bumped = f"resolve step {game.fmt_num(old)} → {game.fmt_num(old + 1)} minutes"
                break
    for at, entry in sorted([(cons_at, [""] + toml_entry("turn_step", cons)),
                             (coa_at, toml_entry("turn_step", coa) + [""])], key=lambda x: -x[0]):
        lines[at:at] = entry

    # [[side]], after the last team (before any commented-out example)
    hs = headers(lines)
    sides = [i for i, n in hs if n == "side"]
    stop = next((i for i, n in hs if i > sides[-1] and n not in ("side", "side.cell")), len(lines))
    at = content_end(lines, sides[-1], stop)
    side_lines = [""] + toml_entry("side", {"id": sid, "label": label, "nation": nation, "prefix": prefix, "color": color})
    splice(lines, at, side_lines)
    g = save_toml(lines, f"adding {label}")
    side = find_side(sid, g)
    print(f"game.toml: added {label} ({nation}, prefix {prefix}) with its COA and Cons steps"
          + (f"; {bumped}" if bumped else "; no step with id \"res\", so give the white cell about a minute more yourself"))

    if a.cells:
        g = add_cells(sid, [c.strip() for c in a.cells.split(",") if c.strip()], g=g, quiet=True)
        side = find_side(sid, g)

    # the team's files
    kw = dict(key=t["key"], label=label, label_title=label.title(), label_upper_forces=f"{label} FORCES", nation=nation,
              nation_upper=nation.strip("[]").upper(), prefix=prefix, id=sid, archetype=t["archetype"],
              archetype_lower=t["archetype"][0].lower() + t["archetype"][1:], summary=t["summary"], pulls=t["pulls"],
              caution=t.get("caution", ""), wants=bullets(t["wants"]), levers=bullets(t["levers"]))
    print("Files:")
    write_new(os.path.join(ROOT, "scenario", f"{sid}-packet.md"), fill(os.path.join(TEMPLATES, "team", "packet.md.tmpl"), **kw))
    added = [] if a.no_assets else add_assets(side, t["assets"], quiet=True)
    kw["oob_start"] = "\n".join(oob_row(r) for r in added if r["availability"] != "rff") or "| [ID] | [Asset] | [Zone] | | |"
    kw["oob_rff"] = "\n".join(oob_row(r) for r in added if r["availability"] == "rff") or "| [ID] | [Asset] | N+1 | |"
    h = os.path.join(ROOT, "handouts", sid)
    for src, dst in (("team-packet.md.tmpl", "team-packet.md"), ("order-of-battle.md.tmpl", "order-of-battle.md"),
                     ("commanders-letter.md.tmpl", "commanders-letter.md"),
                     ("intel/00-read-me-first.md.tmpl", "intel/00-read-me-first.md"),
                     ("intel/product.md.tmpl", f"intel/{prefix}I-01-diplomatic-cable.md")):
        write_new(os.path.join(h, dst), fill(os.path.join(TEMPLATES, "team", src), **kw))
    print(f"""
{label} is in the game. The tools follow game.toml from here: the turn clock, the timer, the counters, the
release folder "{side['folder']}", the Print Packet, and the site. What only you can write
(DESIGN-GUIDE.md §2.1, step 4):
  - its actor entry, starting conditions (S-{prefix}1 ...), and directives in scenario/00-overview.md and the Scenario Brief,
    and its starting conditions in handouts/common/starting-conditions.md;
  - its rows in scenario/whitecell-ground-truth.md, White Cell Intelligence and Injects, the Master Asset List,
    the Likely Plans, Table Setup Guide §4–5, White Cell Handbook §7.2 and §8, and its placement form in White Cell Forms §4;
  - its objectives ({prefix}1–{prefix}3) and forces in scenario/{sid}-packet.md, and the files in handouts/{sid}/;
  - a [[tq]] entry in game.toml if its commander's letter is built in Word;
  - the `who` texts in game.toml that say "Both teams", and the other teams' documents that name only one enemy.
Then: python3 tools/schedule.py --write (the timer's settings) && python3 tools/check_assets.py && python3 tools/schedule.py --check""")
    for w in game.warnings(g):
        print(f"\nNote: {w}.")


# ---------------------------------------------------------------- tracks

def cmd_add_track(a):
    catalog = tracks()
    g = game.GAME
    have = {t.get("id") for t in g["track"]}
    lines = read_lines()
    hs = headers(lines)
    tr = [i for i, n in hs if n == "track"]
    if tr:
        stop = next((i for i, n in hs if i > tr[-1] and n != "track"), len(lines))
        at = content_end(lines, tr[-1], stop)
    else:
        at = len(lines)
    new = []
    for key in a.tracks:
        if key not in catalog:
            die(f"no track preset {key!r} (`python3 tools/presets.py list tracks`)")
        t = {k: v for k, v in catalog[key].items() if k not in ("key", "fits", "moved_by")}
        if t["id"] in have:
            die(f"game.toml already has a track with id {t['id']!r}")
        have.add(t["id"])
        new += [""] + toml_entry("track", t)
    splice(lines, at, new)
    save_toml(lines, "adding tracks")
    print(f"game.toml: added {', '.join(a.tracks)}. Rewrite their names and triggers for the scenario "
          "([TEAM], [NATION]), describe them in scenario/00-overview.md §5.1 and Scenario Brief §5, and run "
          "`python3 tools/schedule.py --write` so the timer shows them.")


# ---------------------------------------------------------------- reference

def reference_markdown():
    cat = assets()
    cl = cells()
    out = ["# Asset Reference", "",
           "**Audience:** designer and white cell. Generated from `presets/assets.csv` by "
           "`python3 tools/presets.py reference --write`: edit the CSV, not this page.", "",
           f"A catalog of {len(cat)} real U.S. systems, forces, and authorities to build a scenario's forces from "
           "(`DESIGN-GUIDE.md` §2.6, `presets/README.md` §3). Capabilities are unclassified, approximate, and simplified "
           "for play, and every entry has a limitation another team can use as a Con. Copy one into a team with "
           "`python3 tools/presets.py add-asset SIDE KEY`.", "",
           "**Columns.** *Core fn* is the AFDP 3-0 core function, given for Air Force assets: AS = Air Superiority, "
           "GPA = Global Precision Attack, RGM = Rapid Global Mobility, GISR = Global ISR, C2 = Command and Control. "
           "*Cell* is the cell preset that usually owns it (`presets/cells.toml`). *RFF* is a typical arrival and "
           "approval when the asset is in an RFF pool. *Hidden* marks an asset that makes a good hidden counter.", ""]
    for c, title in CATEGORIES.items():
        rows = [r for r in cat.values() if r["category"] == c]
        if not rows:
            continue
        out += [f"## {title}", "", "| Key | Asset | Service | Core fn | What it does | Key limitation | Cell | RFF |",
                "| --- | --- | --- | --- | --- | --- | --- | --- |"]
        for r in rows:
            name = r["asset"] + (" *(hidden)*" if r["visibility"] == "hidden" else "")
            if r["parts"]:
                name += f" *({r['parts']} counters)*"
            rff = f"{r['arrives']}, {r['approval'].lower()}" if r["arrives"] else "—"
            out.append(f"| `{r['key']}` | {name} | {r['service']} | {r['core_function'].replace(';', ', ') or '—'} | "
                       f"{r['role']} | {r['limitation']} | {cl.get(r['cell'], {}).get('short', '—')} | {rff} |")
        notes = [f"- `{r['key']}`: {r['notes']}" for r in rows if r["notes"]]
        out += [""] + (["**Notes.**", ""] + notes + [""] if notes else [])
    return "\n".join(out).rstrip() + "\n"


def cmd_reference(a):
    text = reference_markdown()
    if a.write:
        with open(REFERENCE_MD, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"wrote {os.path.relpath(REFERENCE_MD, ROOT)}")
    elif a.check:
        with open(REFERENCE_MD, encoding="utf-8") as f:
            if f.read() != text:
                die("presets/asset-reference.md is out of date: run `python3 tools/presets.py reference --write`")
        print("OK: presets/asset-reference.md matches presets/assets.csv")
    else:
        print(text)


# ---------------------------------------------------------------- main

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("list", help="list presets")
    s.add_argument("kind", choices=["teams", "cells", "assets", "tracks"])
    s.add_argument("--category", choices=list(CATEGORIES))
    s.add_argument("--service")
    s.add_argument("--cell")
    s.add_argument("--search")
    s.set_defaults(fn=cmd_list)
    s = sub.add_parser("show", help="one preset in full")
    s.add_argument("key")
    s.set_defaults(fn=cmd_show)
    s = sub.add_parser("add-cell", help="split a team into cells")
    s.add_argument("side")
    s.add_argument("cells", nargs="*")
    s.add_argument("--no-brief", action="store_true", help="don't write handouts/<side>/cells/<cell>.md")
    s.set_defaults(fn=cmd_add_cell)
    s = sub.add_parser("add-team", help="add a player team from a preset")
    s.add_argument("team")
    for f in ("id", "label", "nation", "prefix", "color", "cells"):
        s.add_argument(f"--{f}")
    s.add_argument("--no-assets", action="store_true", help="don't add the preset's starter assets")
    s.set_defaults(fn=cmd_add_team)
    s = sub.add_parser("add-asset", help="copy catalog assets into a team")
    s.add_argument("side")
    s.add_argument("assets", nargs="+", help="asset keys; key@rff sets the availability for one")
    s.add_argument("--zone", default="")
    s.add_argument("--availability", choices=AVAIL)
    s.add_argument("--visibility", choices=["visible", "hidden"])
    s.add_argument("--cell")
    s.add_argument("--arrives")
    s.add_argument("--approval")
    s.add_argument("--id", help="the asset ID, for a single asset (default: the next free number)")
    s.set_defaults(fn=cmd_add_asset)
    s = sub.add_parser("add-track", help="copy track presets into game.toml")
    s.add_argument("tracks", nargs="+")
    s.set_defaults(fn=cmd_add_track)
    s = sub.add_parser("reference", help="the asset reference page")
    s.add_argument("--write", action="store_true")
    s.add_argument("--check", action="store_true")
    s.set_defaults(fn=cmd_reference)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
