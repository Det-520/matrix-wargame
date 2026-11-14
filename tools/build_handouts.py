#!/usr/bin/env python3
"""Build the release PDFs in build/ from the handout markdown.

    tools/build_handouts.sh            # the usual way (sets up Python and Chromium on NixOS)
    python3 tools/build_handouts.py [--only NAME ...] [--html-only]

Needs: markdown-it-py, mdit-py-plugins, pypdf, playwright (with Chromium 131 or later,
for CSS page-margin boxes).

What it does:
- Renders each handout in RELEASES from markdown to HTML (CommonMark plus
  tables and task lists) and prints it to PDF in Chromium. The look follows the
  "Repo" theme at markdown.style (GitHub's markdown style) with one accent colour
  per audience: green public, purple white cell, and each team its game.toml colour.
  The running header (short name | // MARKING // | date) and the page numbers
  sit in CSS page-margin boxes, inside the page margins, so nothing is lost
  when a printer trims the edge.
- Takes the Tongue and Quill documents (the [[tq]] entries in game.toml) from
  handouts/word/, built by tools/tq/build_tq.py. Run that first after changing
  one of them. An intelligence product with a Word version (handouts/word/RI-07 ...)
  uses it in place of its markdown.
- Splices each team's intelligence products into one "Full Intel" PDF, each
  product starting on a new page.
- Makes one release folder per team ([[side]] in game.toml), from the files in
  handouts/<side id>/ that exist: commander's letter, team packet, order of battle,
  intelligence, counters, and a brief for each cell (cells/<cell id>.md).
- Copies the counters, the map (game.toml [map]), and the white cell clock into place
  (tools/build_handouts.sh first runs tools/schedule.py --write, which sets up the clock
  from game.toml's run of show).
- Assembles the white cell's Print Packet (PACKET): everything one table
  prints to run the game, with the right number of copies, behind a cover
  sheet that lists it. A second version (REF_PACKET_NAME) holds one copy of
  each player form per side, as a reference to copy from, and no spares.
- Pads every built handout, and every item in the Print Packet, to an even
  page count with blank pages, so each prints double-sided on its own sheets.
  The game pieces in the packet (GAME_PIECES) get a blank back behind every page.

Names, dates, turn counts, and the map come from game.toml (tools/game.py).

The markdown is the source, and a Jinja2 template: values from game.toml
({{ requests }}), the rule set ({% if rules == "full" %}), and generated tables are
filled in first (tools/game.py render()). Audience lines and FORMAT NOTE blocks stay out of
the PDFs (the running header carries the audience). `render_markdown()` is
shared with tools/build_site.py.

Layout hooks in the markdown are HTML comments, so the files stay valid for
markdownlint (no inline HTML):
- `<!-- mw:NAME [NAME ...] -->` on the line before a table gives it those
  classes: `form` (labels left, room to write right; add `med` or `tall` for
  bigger boxes), `log` (rows to fill in), `checkgrid` (a step-by-turn tick grid), `compact`
  (a dense reference table).
- `<!-- mw:begin cards -->` ... `<!-- mw:end -->` turns each `###` section in
  between into a cut-out card. `mw:begin slips` cuts the block into slips at
  each `---`, with a dashed cut line between them. Any other name just wraps
  the block.
- `<!-- pagebreak -->` starts a new page.
"""
import argparse
import glob
import html
import os
import re
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from game import GAME, map_pdf, render, values  # noqa: E402

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
H = os.path.join(ROOT, "handouts")
FIN = os.path.join(ROOT, "build")
FONTS = os.path.join(ROOT, "tools", "fonts")

ASAP, WEEK = "Common Matrix - ASAP RELEASE", "Common Scenario - 1WK RELEASE"
WC = "White Cell"
SIDES = GAME["side"]   # the player teams, in briefing order: id, label, prefix, color, cells, folder

G = GAME["game"]
MATRIX = (G["rules_label"], "// PUBLIC //", G["rules_date"])
PUBLIC = (G["name"], "// PUBLIC //", G["date_short"])
WC_ONLY = (G["name"], "// WHITE CELL ONLY //", G["date_short"])


def only(side):
    """The running header for one team's documents."""
    return (G["name"], f"// {side['label']} ONLY //", G["date_short"])


def tint(hexcolor, keep=0.12):
    """A light tint of a colour: mostly white."""
    rgb = [int(hexcolor[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join("%02x" % round(255 - (255 - c) * keep) for c in rgb)


# Accent and tint for each marking.
THEMES = {
    "PUBLIC": ("#1a7f37", "#dafbe1"),
    "WHITE CELL": ("#8250df", "#fbefff"),
    **{f"{s['label']} ONLY": (s["color"], tint(s["color"])) for s in SIDES},
}


def theme(header):
    mark = header[1] if header else "PUBLIC"
    for k, v in THEMES.items():
        if f"// {k} //" == mark or (k in ("PUBLIC", "WHITE CELL") and k in mark):
            return v
    return THEMES["PUBLIC"]


INTEL_ID = re.compile(r"^[%s]I-\d\d" % "".join(s["prefix"] for s in SIDES))


def intel(side_id):
    side = next(s for s in SIDES if s["id"] == side_id)
    return sorted(glob.glob(os.path.join(H, side_id, "intel", f"{side['prefix']}I-*.md")))


def side_releases(side):
    """One team's release folder, from the files in handouts/<side id>/ that exist."""
    sid, label, hdr, rel = side["id"], side["label"], only(side), side["folder"]
    has = lambda f: os.path.exists(os.path.join(H, sid, f))  # noqa: E731
    out = []
    letter = f"{sid}/commanders-letter.md"
    tq = next((d["key"] for d in GAME["tq"] if d["src"] == f"handouts/{letter}"), None)
    if tq:
        out.append((rel, f"{tq}.pdf", None, [("word", tq)]))
    elif has("commanders-letter.md"):
        out.append((rel, f"{label} - Commander's Letter.pdf", hdr, [letter]))
    if has("team-packet.md"):
        out.append((rel, f"{label} Team Packet.pdf", hdr, [f"{sid}/team-packet.md"]))
    for c in side["cells"]:
        if has(f"cells/{c['id']}.md"):
            out.append((rel, f"{label} Cell Brief - {c['name']}.pdf", hdr, [f"{sid}/cells/{c['id']}.md"]))
    if has("order-of-battle.md"):
        out.append((rel, f"{label} Order of Battle.pdf", hdr, [f"{sid}/order-of-battle.md"]))
    if has("intel/00-read-me-first.md"):
        out.append((rel, f"{label} Intel - Read Me First.pdf", hdr, [f"{sid}/intel/00-read-me-first.md"]))
    if intel(sid):
        out.append((rel, f"{label} Full Intel.pdf", hdr, f"intel:{sid}"))
    out.append((rel, "counters.pdf", None, [("copy", f"handouts/{sid}/counters.pdf")]))
    return out


PACKET_NAME = "Print Packet - One Table.pdf"
REF_PACKET_NAME = "Print Packet - One Table, Reference Forms.pdf"

# (folder, file name, header, sources). A source is a markdown path, or
# ("word", name) for a PDF from handouts/word/, or ("copy", path).
# "packet" builds the Print Packet from the files above it, so it comes last;
# "packet:reference" builds the version with one copy of each player form.
# The basic rule set (game.toml [rules] set = "basic") gives players the Basic Rules
# in place of the Player Rules Handbook.
BASIC = GAME["rules"]["set"] == "basic"
RELEASES = [
    *([] if BASIC else [(ASAP, "Player Rules Handbook.pdf", MATRIX, ["common/rules-handbook.md"])]),
    (ASAP, "Basic Rules.pdf", MATRIX, ["common/basic-rules.md"]),
    (ASAP, "Player Forms and Templates.pdf", MATRIX, ["common/player-forms.md"]),
    (WEEK, "Scenario Brief.pdf", PUBLIC, ["common/scenario-brief.md"]),
    (WEEK, "Scenario Schedule.pdf", PUBLIC, ["common/scenario-schedule.md"]),
    (WEEK, "Starting Conditions.pdf", PUBLIC, ["common/starting-conditions.md"]),
    (WEEK, "map-full.pdf", None, [("copy", map_pdf("full"))]),
    (WEEK, "map-tiles.pdf", None, [("copy", map_pdf("tiles_letter"))]),
    *[r for side in SIDES for r in side_releases(side)],
    (WC, "White Cell Handbook.pdf", WC_ONLY, ["whitecell/handbook.md"]),
    (WC, "White Cell Checklist.pdf", WC_ONLY, ["whitecell/checklist.md"]),
    (WC, "White Cell Table Setup Guide.pdf", WC_ONLY, ["whitecell/table-setup.md"]),
    (WC, "White Cell Likely Plans.pdf", WC_ONLY, ["whitecell/likely-plans.md"]),
    (WC, "White Cell Intelligence and Injects.pdf", WC_ONLY, ["whitecell/intel-and-injects.md"]),
    (WC, "Master Asset List.pdf", WC_ONLY, ["whitecell/master-asset-list.md"]),
    (WC, "White Cell Forms.pdf", WC_ONLY, ["whitecell/forms.md"]),
    (WC, "counters.pdf", None, [("copy", "handouts/whitecell/counters.pdf")]),
    (WC, "whitecell-clock.html", None, [("copy", "tools/whitecell-clock.html")]),
    (WC, PACKET_NAME, WC_ONLY, "packet"),
    (WC, REF_PACKET_NAME, WC_ONLY, "packet:reference"),
]

# Paper the players need per side, from game.toml [turns]: one worksheet a turn,
# request slips for every request (3 slips to a page), one secret COA slip a phase
# (none with the basic rules).
T = GAME["turns"]
TURNS = T["total"]
SLIPS, SLIP_PAGES = values()["slips"], values()["slip_pages"]  # the Player Forms quote the same numbers
SECRET = 0 if BASIC else T["secret_coas"]  # the basic rules have no secret COAs

# What one table prints to run the game. (label, release file, section heading
# (its start, as printed) or None for the whole file, copies, note). Copies are per table; the packet
# holds them all, in this order.
PACKET = [
    ("White Cell Checklist", (WC, "White Cell Checklist.pdf"), None, 1, "Lead adjudicator. Tick it off through the event."),
    ("Table Setup Guide", (WC, "White Cell Table Setup Guide.pdf"), None, 1, "Devices, table layout, and where every counter starts. Set up before Phase I."),
    ("White Cell Forms", (WC, "White Cell Forms.pdf"), None, 1, "Score sheet, ongoing-effects sheet, objective status card, a placement form for each team. The ongoing-effects sheet goes beside the map; the rest stays face down with the loggers."),
    ("Starting conditions: reference and cue cards", (WEEK, "Starting Conditions.pdf"), None, 1, "Cut the cue cards apart and stand them face up beside the map."),
    ("Counters, every team", (WC, "counters.pdf"), None, 1, "Print at 100% (not \"fit to page\"), in colour, on card stock if you can. Shows hidden assets: white cell only."),
    ("Map, letter tiles", (WEEK, "map-tiles.pdf"), None, 1, "Portrait, like the rest of the packet (the map is turned on the page). Trim and tape. For one large sheet, print map-full.pdf on a plotter instead."),
]
# Each team's player forms, then spares for whichever team runs short. The player forms have a team box, so one stack serves all.
for _side in [s["label"] for s in SIDES]:
    PACKET += [
        (f"{_side}: OPORD/FRAGO format", (ASAP, "Player Forms and Templates.pdf"), "1. Five-Paragraph", 1, "For reference; the brief doesn't have to follow it"),
        (f"{_side}: COA worksheets", (ASAP, "Player Forms and Templates.pdf"), "2. COA Worksheet", TURNS, "One per turn"),
        (f"{_side}: Cons worksheets", (ASAP, "Player Forms and Templates.pdf"), "3. Cons Worksheet", TURNS, "One per turn"),
        (f"{_side}: request slips (3 per page)", (ASAP, "Player Forms and Templates.pdf"), "4. Request Slips", SLIP_PAGES,
         f"{SLIP_PAGES * 3} slips: {T['planning_requests']} in Phase I, {T['requests_per_turn']} a turn after"),
        (f"{_side}: secret COA slips", (ASAP, "Player Forms and Templates.pdf"), "6. Secret COA Slip", SECRET, "One per phase"),
    ]
PACKET += [
    ("Spare: request slips (3 per page)", (ASAP, "Player Forms and Templates.pdf"), "4. Request Slips", 3, "9 slips, any team"),
    ("Spare: COA worksheets", (ASAP, "Player Forms and Templates.pdf"), "2. COA Worksheet", 2, "Any team"),
    ("Spare: Cons worksheets", (ASAP, "Player Forms and Templates.pdf"), "3. Cons Worksheet", 2, "Any team"),
    ("Spare: secret COA slips", (ASAP, "Player Forms and Templates.pdf"), "6. Secret COA Slip", 2 if SECRET else 0, "Any team"),
    *[(f"Spare: {s['label']} placement form", (WC, "White Cell Forms.pdf"), f"{s['label']} placement form", 1,
       "If the first fills up with crossings-out") for s in SIDES],
]


PLAYER_FORMS = (ASAP, "Player Forms and Templates.pdf")

# The packet prints double-sided. Each document copy is padded to an even page
# count so the next one starts on a new sheet. Pieces that are cut apart or
# taped together get a blank back behind every page instead.
GAME_PIECES = {(WEEK, "Starting Conditions.pdf"), (WC, "counters.pdf"), (WEEK, "map-tiles.pdf")}


def sheets(pages, f):
    """Sheets of paper one copy uses, printed double-sided."""
    return pages if f in GAME_PIECES else (pages + 1) // 2


def packet_items(variant="full"):
    """PACKET as printed. "reference" keeps one copy of each player form per side and drops the spares.
    An item with no copies (secret COA slips under the basic rules) is left out."""
    items = [item for item in PACKET if item[3] > 0]
    if variant == "full":
        return items
    return [(label, f, h, 1, "Reference copy" if f == PLAYER_FORMS else note)
            for label, f, h, _copies, note in items if not label.startswith("Spare: ")]


def word_name(md_path):
    """The handouts/word/ PDF that replaces this intel product, if there is one."""
    code = os.path.basename(md_path)[:5]
    hits = glob.glob(os.path.join(H, "word", code + " *.pdf"))
    return os.path.splitext(os.path.basename(hits[0]))[0] if hits else None


def expand(sources):
    if isinstance(sources, str) and sources.startswith("intel:"):
        out = []
        for md in intel(sources.split(":")[1]):
            w = word_name(md)
            out.append(("word", w) if w else os.path.relpath(md, H))
        return out
    return sources


# ---------------------------------------------------------------- markdown

FRONT = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def front_matter(text):
    m = FRONT.match(text)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip().strip('"')
        text = text[m.end():]
    return meta, text


def clean(text, is_intel=False, where="markdown"):
    """The markdown filled in for this game (a Jinja2 template, tools/game.py render()),
    without what stays in the markdown only: audience lines and FORMAT NOTEs."""
    text = render(text, where=where)
    paras = re.split(r"(\n\s*\n)", text)
    out = []
    for p in paras:
        s = p.strip()
        if s.startswith("> **FORMAT NOTE"):
            continue
        if s.startswith("**Audience:**"):
            continue
        # the audience marking ("**REDFOR EYES ONLY.**", "**WHITE CELL ONLY.**"), not any bold REDFOR text
        m = MARKING.match(s)
        if m:
            rest = s[m.end():].strip()
            if is_intel or not rest.startswith("*") or rest.startswith("**"):
                continue
            p = rest
        out.append(p)
    text = "".join(out)
    if is_intel:  # the rule under the audience line
        text = re.sub(r"\A(\s*# [^\n]*\n)\s*---\s*\n", r"\1", text)
    return text


MARKING = re.compile(r"^\*\*(?:(?:%s) EYES ONLY|WHITE CELL ONLY)\.\*\*\s*(\*\*Never show[^*]*\*\*\s*)?"
                     % "|".join(re.escape(s["label"]) for s in SIDES))


def side_class(heading_html):
    """mw-side-<id> for a card or slip whose heading names a team (S-R1, R-30, REDFOR ...)."""
    t = re.sub(r"<[^>]+>", "", heading_html)
    for side in SIDES:
        if re.match(r"\s*(S-)?%s-?\d|.*\b%s\b" % (side["prefix"], re.escape(side["label"])), t):
            return " mw-side-" + side["id"]
    return ""


def _wrap_blocks(out):
    """<!-- mw:begin NAME --> ... <!-- mw:end --> -> <div class="mw-NAME">; cards and slips split at <h3>."""
    def block(m):
        name, inner = m.group(1), m.group(2)
        if name == "cards":
            parts = re.split(r"(?=<h3)", inner)
            inner = parts[0] + "".join('<div class="mw-card%s">%s</div>' % (side_class(p[:200]), p) for p in parts[1:])
        elif name == "slips":
            inner = "".join('<div class="mw-slip">%s</div>' % p for p in re.split(r"<hr\s*/?>", inner))
        return '<div class="mw-%s">%s</div>' % (name, inner)
    return re.sub(r"<!-- mw:begin (\w[\w-]*) -->\s*(.*?)<!-- mw:end -->", block, out, flags=re.S)


def render_markdown(text, base_dir, image_url=None):
    """Markdown (as the handouts use it) -> HTML."""
    from markdown_it import MarkdownIt
    from mdit_py_plugins.tasklists import tasklists_plugin

    text = re.sub(r"\)\{width=[^}]*\}", ")", text)
    text = text.replace("<!-- pagebreak -->", '<div class="pagebreak"></div>')
    md = MarkdownIt("commonmark", {"html": True, "typographer": False}).enable("table").enable("strikethrough")
    md.use(tasklists_plugin)
    out = md.render(text)

    # table classes from <!-- mw:a b --> on the line before
    out = re.sub(r"<!-- mw:((?!begin|end)[\w -]+?) -->\s*<table>",
                 lambda m: '<table class="%s">' % " ".join("mw-" + c for c in m.group(1).split()), out)
    out = _wrap_blocks(out)
    # a header row with no text (key-value tables in the intel products) is dropped
    out = re.sub(r"<table( class=\"[^\"]*\")?>\s*<thead>\s*<tr>\s*(?:<th[^>]*>\s*</th>\s*)+</tr>\s*</thead>",
                 lambda m: '<table class="mw-kv%s">' % (" " + m.group(1)[8:-1] if m.group(1) else ""), out)
    # a header cell followed by empty ones spans them (form titles)
    def span(m):
        n = 1 + len(re.findall(r"<th[^>]*>\s*</th>", m.group(2)))
        return '<th colspan="%d"%s</th></tr>' % (n, m.group(1)) if n > 1 else m.group(0)
    out = re.sub(r"<th(?: [^>]*)?(>(?:(?!</th>).)*\S(?:(?!</th>).)*)</th>((?:\s*<th[^>]*>\s*</th>)+)\s*</tr>", span, out)
    # an all-capitals heading is an issuing office's masthead (intel products), not a headline
    out = re.sub(r"<h2>([^<a-z]+)</h2>", r'<h2 class="mw-masthead">\1</h2>', out)
    # a paragraph that is only bold text is a label (headings stop at h3): keep it with what follows
    out = re.sub(r"<p><strong>((?:(?!</?p>).)*?)</strong></p>", r'<p class="mw-label"><strong>\1</strong></p>', out)
    # ☐ prints as a drawn box, the same size everywhere; a box and its label don't split
    out = re.sub(r"☐ ?([^☐<|/]*?[^☐<|/\s])(?=\s*(?:☐|/|<|$))",
                 lambda m: '<span class="mw-opt"><span class="mw-box" aria-hidden="true">☐</span>%s</span>' % m.group(1)
                 if len(m.group(1)) <= 14 else m.group(0), out)
    out = out.replace("☐", '<span class="mw-box" aria-hidden="true">☐</span>')
    out = re.sub(r"<td>((?:\s*<span class=\"mw-opt\">(?:(?!</span></span>).)*</span></span>)+\s*)</td>",
                 r'<td class="mw-opts">\1</td>', out)

    def img(m):
        src = m.group(1)
        if re.match(r"^[a-z]+:", src):
            return m.group(0)
        path = os.path.normpath(os.path.join(base_dir, src))
        return 'src="%s"' % (image_url(path) if image_url else "file://" + path)
    return re.sub(r'src="([^"]+)"', img, out)


# ---------------------------------------------------------------- style

FONT_FACES = "".join(
    '@font-face { font-family: "JetBrains Mono"; src: url("file://%s/JetBrainsMono-%s.ttf"); font-weight: %s; font-style: %s; }\n'
    % (FONTS, f, w, s) for f, w, s in (("Regular", 400, "normal"), ("Bold", 700, "normal"), ("Italic", 400, "italic")))

# The Repo theme (markdown.style), set for paper: system sans, JetBrains Mono for
# code, rules under the top two heading levels, zebra-striped tables.
CSS = """
:root {
  --fg: #1f2328; --muted: #59636e; --line: #d1d9e0; --soft: #f6f8fa; --link: #0969da;
  --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
  --mono: "JetBrains Mono", ui-monospace, "DejaVu Sans Mono", "Liberation Mono", monospace;
}
html { font-family: var(--sans); font-size: 10pt; color: var(--fg); -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; line-height: 1.45; }
a { color: var(--link); text-decoration: none; }
h1, h2, h3, h4, h5, h6 { font-weight: 600; line-height: 1.25; margin: 1.3em 0 0.5em; break-after: avoid; color: var(--fg); }
h1 { font-size: 18pt; padding-bottom: 0.25em; border-bottom: 1px solid var(--line); }
h2 { font-size: 14pt; padding-bottom: 0.25em; border-bottom: 1px solid var(--line); }
h3 { font-size: 11.5pt; }
h4 { font-size: 10pt; }
h5, h6 { font-size: 9.5pt; color: var(--muted); }
h2 + *, h3 + *, h4 + * { break-before: avoid; }
p.mw-label { margin: 1.1em 0 0.4em; break-after: avoid; }
p.mw-label + * { break-before: avoid; }
p { margin: 0 0 0.65em; orphans: 3; widows: 3; }
strong { font-weight: 600; }
ul, ol { margin: 0 0 0.65em; padding-left: 1.7em; } li { margin: 0.2em 0; } li > p { margin: 0.2em 0; }
blockquote { margin: 0.4em 0 0.8em; padding: 0.15em 0.9em; color: var(--muted); border-left: 0.25em solid var(--accent); }
blockquote p { margin: 0.35em 0; } blockquote strong { color: var(--fg); }
code { font-family: var(--mono); font-size: 0.86em; background: var(--soft); padding: 0.1em 0.3em; border-radius: 4px; }
pre { font-family: var(--mono); font-size: 8.5pt; line-height: 1.45; white-space: pre-wrap;
      border: 1px solid var(--line); border-radius: 6px; padding: 9pt 11pt; break-inside: avoid; }
pre code { background: none; padding: 0; font-size: inherit; }
hr { border: 0; height: 0.25em; background: var(--line); margin: 1.2em 0; }
img { max-width: 100%; }

table { border-collapse: collapse; width: 100%; margin: 0.4em 0 1em; font-size: 9pt; line-height: 1.35; break-inside: auto; }
tr { break-inside: avoid; }
th, td { border: 1px solid var(--line); padding: 4pt 6pt; vertical-align: top; text-align: left; }
thead th { font-weight: 600; border-bottom: 1.5pt solid var(--accent); }
td:empty { height: 1.3em; }

/* the title block made from the front matter */
.doc-head { margin: 0 0 1.4em; padding: 0 0 0.8em; border-bottom: 2pt solid var(--accent); }
.doc-kicker { font-size: 8.5pt; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--accent); margin: 0 0 0.3em; }
.doc-head h1 { font-size: 24pt; border: 0; padding: 0; margin: 0 0 0.2em; }
.doc-subtitle { color: var(--muted); font-size: 11pt; margin: 0; }

/* intelligence products */
.product > h1:first-child { margin-top: 0; border-bottom: 2pt solid var(--accent); }
h2.mw-masthead { font-size: 10pt; letter-spacing: 0.06em; color: var(--muted); border: 0; padding: 0; margin: 1em 0 0.5em; }

/* checkboxes */
.mw-box { display: inline-block; width: 0.8em; height: 0.8em; border: 1.1pt solid var(--fg); border-radius: 2px;
          color: transparent; overflow: hidden; line-height: 0.8em; vertical-align: -0.08em; margin: 0 0.3em 0 0.35em; }
.mw-box:first-child { margin-left: 0; }
ul.contains-task-list { list-style: none; padding-left: 1.4em; }
.task-list-item-checkbox { appearance: none; -webkit-appearance: none; width: 0.85em; height: 0.85em; border: 1.1pt solid var(--fg);
          border-radius: 2px; margin: 0 0.55em 0 -1.4em; vertical-align: -0.1em; }

/* forms: label column on the left, room to write on the right */
table.mw-form { font-size: 10pt; }
table.mw-form thead th { color: var(--fg); border-top: 2pt solid var(--accent); border-bottom: 1.5pt solid var(--fg); font-size: 11pt; letter-spacing: 0.04em; }
table.mw-form td:first-child { width: 31%; font-weight: 600; }
table.mw-form td { height: 0.42in; vertical-align: middle; box-sizing: border-box; }
table.mw-form.mw-tall td { height: 0.9in; vertical-align: top; }
table.mw-form.mw-med td { height: 0.6in; vertical-align: top; }
table.mw-form.mw-tall td:first-child, table.mw-form.mw-med td:first-child { vertical-align: top; }
.mw-opt { white-space: nowrap; margin-right: 0.35em; }
td.mw-opts { white-space: nowrap; width: 1%; }
table.mw-log td:empty, table.mw-log td { height: 0.3in; padding-top: 1pt; padding-bottom: 1pt; vertical-align: middle; box-sizing: border-box; }
table.mw-kv td:first-child { width: 28%; font-weight: 600; }

table.mw-checkgrid { font-size: 8.5pt; }
table.mw-checkgrid th:nth-child(n+3), table.mw-checkgrid td:nth-child(n+3) { text-align: center; width: 5.2%; padding: 3pt 2pt; }
table.mw-checkgrid td { height: 0.27in; vertical-align: middle; }
table.mw-checkgrid td:first-child { width: 10%; white-space: nowrap; color: var(--muted); font-family: var(--mono); font-size: 7.5pt; }

/* cut-out cards and slips */
.mw-card { border: 1.2pt dashed var(--muted); border-radius: 6px; padding: 0.16in 0.22in; height: 2.88in; box-sizing: border-box;
           margin: 0 0 0.14in; break-inside: avoid; overflow: hidden; position: relative; font-size: 12.5pt; line-height: 1.4; }
.mw-card h3 { margin: -0.16in -0.22in 0.12in; padding: 0.1in 0.22in; font-size: 15pt; color: #fff; background: var(--card); border-radius: 5px 5px 0 0; }
.mw-card p { margin: 0 0 0.45em; }
.mw-card { --card: var(--accent); }
%(side_cards)s
.mw-slip { border-bottom: 1.2pt dashed var(--muted); padding: 0 0 0.12in; margin: 0 0 0.16in; break-inside: avoid; }
.mw-slip:last-child { border-bottom: 0; }
table.mw-compact { font-size: 8pt; table-layout: fixed; line-height: 1.3; }
table.mw-compact td { padding: 3pt 5pt; }
table.mw-compact th:first-child { width: 6%; } table.mw-compact th:nth-child(2) { width: 16%; }
table.mw-compact th:nth-child(3) { width: 50%; }
.mw-slip table.mw-form td { height: 0.36in; }
.mw-slip table { margin-bottom: 0; }

.pagebreak { break-after: page; height: 0; }
.product { break-before: page; } .product:first-child { break-before: auto; }
""".replace("%(side_cards)s", " ".join(".mw-card.mw-side-%s { --card: %s; }" % (x["id"], x["color"]) for x in SIDES))

# Page frame. The header and footer sit in the margin boxes, inside the page margins.
PAGE = """
@page {
  size: Letter; margin: 0.9in 0.75in 0.8in 0.75in;
  @top-left { content: "%(left)s"; font: 8pt var(--sans); color: #59636e; vertical-align: bottom; padding-bottom: 0.14in; border-bottom: 0.75pt solid #d1d9e0; }
  @top-center { content: "%(mid)s"; font: 700 8pt var(--sans); letter-spacing: 0.06em; color: %(accent)s; vertical-align: bottom; padding-bottom: 0.14in; border-bottom: 0.75pt solid #d1d9e0; }
  @top-right { content: "%(right)s"; font: 8pt var(--sans); color: #59636e; vertical-align: bottom; padding-bottom: 0.14in; border-bottom: 0.75pt solid #d1d9e0; }
  @bottom-left { content: "%(title)s"; font: 7.5pt var(--sans); color: #59636e; vertical-align: top; padding-top: 0.14in; }
  @bottom-right { content: "Page " counter(page) " of " counter(pages); font: 7.5pt var(--sans); color: #59636e; vertical-align: top; padding-top: 0.14in; }
}
:root { --accent: %(accent)s; --tint: %(tint)s; }
"""


def css_str(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def title_block(meta):
    """The front matter's title and subtitle as a title block. "Operation Example — X" puts the first part above."""
    title = meta.get("title", "")
    kicker, _, main = title.partition(" — ")
    if not main:
        kicker, main = "", title
    sub = '<p class="doc-subtitle">%s</p>' % html.escape(meta["subtitle"]) if meta.get("subtitle") else ""
    kick = '<p class="doc-kicker">%s</p>' % html.escape(kicker) if kicker else ""
    return '<header class="doc-head">%s<h1>%s</h1>%s</header>' % (kick, html.escape(main), sub)


def page_html(md_paths, header=WC_ONLY, doc_title=""):
    """One HTML document for one or more markdown files (several = intel products)."""
    bodies = []
    many = any(INTEL_ID.match(os.path.basename(p)) for p in md_paths)
    for rel in md_paths:
        path = rel if os.path.isabs(rel) else os.path.join(H, rel)
        meta, text = front_matter(open(path, encoding="utf-8").read())
        is_product = bool(INTEL_ID.match(os.path.basename(path)))
        text = clean(text, is_intel=is_product, where=os.path.relpath(path, ROOT))
        body = render_markdown(text, os.path.dirname(path))
        if meta.get("title"):
            body = title_block(meta) + body
            doc_title = doc_title or meta.get("short", "")
        bodies.append('<section class="product">%s</section>' % body if many else body)
    accent, tint = theme(header)
    left, mid, right = header or ("", "", "")
    page = PAGE % dict(left=css_str(left), mid=css_str(mid), right=css_str(right), title=css_str(doc_title),
                       accent=accent, tint=tint)
    return ('<!doctype html><html><head><meta charset="utf-8"><style>%s%s%s</style></head><body>%s</body></html>'
            % (FONT_FACES, CSS, page, "".join(bodies)))


# ---------------------------------------------------------------- PDF

def print_pdf(browser, page_doc, out_path):
    src = out_path[:-4] + ".html"  # a file:// page may load file:// images and fonts; set_content may not
    with open(src, "w", encoding="utf-8") as f:
        f.write(page_doc)
    page = browser.new_page()
    page.goto("file://" + src, wait_until="load")
    page.evaluate("document.fonts.ready")
    page.pdf(path=out_path, print_background=True, prefer_css_page_size=True, display_header_footer=False)
    page.close()


def pad_even(w, start=0):
    """Add a blank page if the pages written since `start` are odd, so the next item starts on a new sheet when printed double-sided."""
    if (len(w.pages) - start) % 2:
        box = w.pages[-1].mediabox
        w.add_blank_page(width=box.width, height=box.height)


def write_pdf(pdfs_or_pages, name, dst, even=False):
    """Join PDFs, or (path, [page indexes], mode) pieces, into one. `even` pads the whole file to an even page count.
    A piece's mode is "even" (pad the piece to an even count) or "backs" (a blank back behind every page)."""
    from pypdf import PdfReader, PdfWriter
    w = PdfWriter()
    for item in pdfs_or_pages:
        if isinstance(item, str):
            w.append(item)
            continue
        path, pages, mode = item
        r = PdfReader(path)
        start = len(w.pages)
        for i in pages:
            w.add_page(r.pages[i])
            if mode == "backs":
                pad_even(w, start)
        pad_even(w, start)
    if even:
        pad_even(w)
    w.add_metadata({"/Title": os.path.splitext(name)[0], "/Author": G["designer"], "/Creator": "tools/build_handouts.py"})
    with open(dst, "wb") as f:
        w.write(f)


def build_one(browser, folder, name, header, sources, work):
    dst = os.path.join(FIN, folder, name)
    if isinstance(sources, str) and sources.startswith("packet"):
        return build_packet(browser, header, dst, work, sources.partition(":")[2] or "full")
    sources = expand(sources)
    if len(sources) == 1 and isinstance(sources[0], tuple) and sources[0][0] == "copy":
        shutil.copyfile(os.path.join(ROOT, sources[0][1]), dst)
        return dst
    # group consecutive markdown files so each run prints as one PDF
    parts, run = [], []
    for s in sources:
        if isinstance(s, tuple):
            if run:
                parts.append(("md", run))
                run = []
            parts.append(s)
        else:
            run.append(s)
    if run:
        parts.append(("md", run))
    short = os.path.splitext(name)[0]
    pdfs = []
    for i, (kind, val) in enumerate(parts):
        if kind == "md":
            p = os.path.join(work, f"{len(os.listdir(work))}-{i}.pdf")
            print_pdf(browser, page_html(val, header, short), p)
            pdfs.append(p)
        elif kind == "word":
            p = os.path.join(H, "word", val + ".pdf")
            if not os.path.exists(p):
                # No Word version yet (WordCraft not run): print the markdown it is made from instead.
                src = next((d["src"] for d in GAME["tq"] if d["key"] == val), None)
                if not src:
                    sys.exit(f"missing {os.path.relpath(p, ROOT)}: run tools/tq/build_tq.py first")
                print(f"  note: no {os.path.relpath(p, ROOT)}; using {src} (run tools/tq/build_tq.py for the Word version)")
                p = os.path.join(work, f"{len(os.listdir(work))}-{i}.pdf")
                side = header or next((only(x) for x in SIDES if f"/{x['id']}/" in src), WC_ONLY)
                print_pdf(browser, page_html([os.path.join(ROOT, src)], side, short), p)
            pdfs.append(p)
    write_pdf(pdfs, name, dst, even=True)
    return dst


# ---------------------------------------------------------------- print packet

def section_pages(pdf, heading):
    """Page indexes of the section that starts with the heading `heading`, up to where the next one starts."""
    from pypdf import PdfReader
    pages = PdfReader(pdf).pages
    others = {h for _l, f, h, _c, _n in PACKET if h and os.path.join(FIN, *f) == pdf}
    starts = {}
    for i, pg in enumerate(pages):
        text = pg.extract_text() or ""
        for h in others:
            if re.search(r"^\s*(?:\d+(?:\.\d+)*\.?\s+)?" + re.escape(h), text, re.M):
                starts.setdefault(h, i)
    if heading not in starts:
        sys.exit(f"{os.path.relpath(pdf, ROOT)}: no section {heading!r}"
                 + (" (each team in game.toml [[side]] needs its own placement form in the White Cell Forms §4)"
                    if heading.endswith("placement form") else ""))
    later = sorted(v for v in starts.values() if v > starts[heading])
    return list(range(starts[heading], later[0] if later else len(pages)))


def packet_rows(variant="full"):
    """[(label, file, pages per copy, copies, note)] with the page counts read from the built PDFs."""
    from pypdf import PdfReader
    rows = []
    for label, (folder, fname), heading, copies, note in packet_items(variant):
        pdf = os.path.join(FIN, folder, fname)
        if not os.path.exists(pdf):
            sys.exit(f"missing {os.path.relpath(pdf, ROOT)}: build it before the print packet")
        pages = section_pages(pdf, heading) if heading else list(range(len(PdfReader(pdf).pages)))
        pages = [i for i in pages if "/Contents" in PdfReader(pdf).pages[i]]  # drop the release file's blank pad pages
        rows.append((label, pdf, pages, copies, note, (folder, fname)))
    return rows


def packet_markdown(rows=None, variant="full"):
    """The cover sheet, as markdown. Also used for the site page (rows=None reads the counts without page numbers)."""
    ref = variant == "reference"
    lines = [
        "---",
        'title: "%s — Print Packet%s"' % (G["name"], ", Reference Forms" if ref else ""),
        'subtitle: "%s · print one packet per table (%d %s)"' % (
            "Everything one table prints, with one copy of each player form per side" if ref
            else "Everything one table prints to run the game", G["tables"], "table" if G["tables"] == 1 else "tables"),
        'short: "Print Packet"',
        "---",
        "",
        "**WHITE CELL ONLY.** This packet holds **every team's** hidden counters and the white cell forms. "
        "Print it, split it into the stacks below, and keep it away from the players until each piece is handed out.",
        "",
    ]
    if ref:
        lines += [
            "This version holds **one copy of each player form and slip for each team**, as a reference, and no spares. "
            f"Photocopy more from it as needed, or print `{PACKET_NAME}` for the full count.",
            "",
        ]
    lines += [
        "## Contents (one table)",
        "",
        "| Printed | Item | Copies | Sheets | Notes |",
        "| --- | --- | --- | --- | --- |",
    ]
    total = 0
    spares = False
    for label, _pdf, pages, copies, note, f in rows or [(r[0], None, [], r[3], r[4], r[1]) for r in packet_items(variant)]:
        n = sheets(len(pages), f) * copies
        total += n
        if label.startswith("Spare: ") and not spares:
            spares = True
            lines.append("| | **Spares, at the back.** Keep them with the white cell and hand them out as needed. | | | |")
        label = label.removeprefix("Spare: ")
        lines.append("| ☐ | %s | %d | %s | %s |" % (label, copies, n or "", note))
    lines += [
        "",
        f"Packet total: **{total} sheets** after this cover, in the order listed." if rows else "",
        "",
        "## Printing",
        "",
        "- Print **double-sided** (flip on the long edge) **at 100% scale** (\"actual size\", not \"fit to page\"). Every page keeps its content inside a 0.75 in margin.",
        "- Every item starts on a new sheet: blank pages fill out any item with an odd page count. "
        "The counters, map tiles, and starting conditions have a blank back behind every page, so they can be cut apart and taped.",
        "- **Colour** for the game pieces: the counters, map tiles, and cue cards use colour for teams. "
        "Everything else (the forms, worksheets, and slips) is black and white, so print it in greyscale to save ink.",
        "- **Card stock** for the counters and cue cards, if you have it.",
        "- Cut the counters along the grey lines, and the cue cards and request slips along the dashed lines.",
        "",
        "## Also needed at each table",
        "",
        "- [ ] The room's TV or projector. Use the room computer connected to it if there is one; otherwise bring the lead adjudicator's laptop and its cable",
        "- [ ] The timer and dice program (`whitecell-clock.html`) on that screen, where every team can see it. Its tracker keeps the tracks; there is no paper track board.",
        "- [ ] Each logger's laptop with the white cell site and Slack, screen turned away from the players (Table Setup Guide §1)",
        "- [ ] An envelope for the hidden counters",
        "- [ ] Pens for each team and each logger",
        "",
    ]
    return "\n".join(lines)


def build_packet(browser, header, dst, work, variant="full"):
    rows = packet_rows(variant)
    cover_md = os.path.join(work, f"print-packet-{variant}.md")
    with open(cover_md, "w", encoding="utf-8") as f:
        f.write(packet_markdown(rows, variant))
    cover = os.path.join(work, f"packet-cover-{variant}.pdf")
    print_pdf(browser, page_html([cover_md], header, "Print Packet"), cover)
    from pypdf import PdfReader
    items = [(cover, range(len(PdfReader(cover).pages)), "even")]
    for _label, pdf, pages, copies, _note, f in rows:
        items += [(pdf, pages, "backs" if f in GAME_PIECES else "even")] * copies
    write_pdf(items, os.path.basename(dst), dst)
    return dst


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--only", nargs="*", default=[], help="build only files whose name contains one of these")
    ap.add_argument("--html-only", action="store_true", help="write the HTML to a temp folder instead of printing")
    a = ap.parse_args()
    picks = [r for r in RELEASES if not a.only or any(o.lower() in r[1].lower() for o in a.only)]
    work = tempfile.mkdtemp(prefix="mw-pdf-")
    if a.html_only:
        for folder, name, header, sources in picks:
            if isinstance(sources, str) and sources.startswith("packet"):
                continue
            md = [s for s in expand(sources) if isinstance(s, str)]
            if md:
                p = os.path.join(work, name.replace(".pdf", ".html"))
                open(p, "w", encoding="utf-8").write(page_html(md, header, os.path.splitext(name)[0]))
                print(p)
        return
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH") or None)
        for folder, name, header, sources in picks:
            os.makedirs(os.path.join(FIN, folder), exist_ok=True)
            dst = build_one(browser, folder, name, header, sources, work)
            print("wrote", os.path.relpath(dst, ROOT))
        browser.close()
    shutil.rmtree(work, ignore_errors=True)
    if not a.only:
        remove_stale()


def remove_stale():
    """Delete release files that RELEASES no longer makes (the Player Rules Handbook after a
    switch to the basic rules), so an old file never goes out with a release folder."""
    made = {(folder, name) for folder, name, _h, _s in RELEASES}
    for folder in {f for f, _n in made}:
        for name in os.listdir(os.path.join(FIN, folder)):
            if (folder, name) not in made and os.path.isfile(os.path.join(FIN, folder, name)):
                os.remove(os.path.join(FIN, folder, name))
                print("removed", os.path.relpath(os.path.join(FIN, folder, name), ROOT))


if __name__ == "__main__":
    main()
